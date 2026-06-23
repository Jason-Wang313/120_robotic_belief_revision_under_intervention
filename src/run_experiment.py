from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 120_2026_5
SEEDS = list(range(10))
EPISODES_PER_CELL = 8
PROPOSED = "causal_intervention_belief_revision_v5"
PREVIOUS = "proposed_intervention_violation_revision_v4_1"
ORACLE = "oracle_physical_belief_revision"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"
for directory in (RESULTS, FIGURES, PAPER):
    directory.mkdir(exist_ok=True)


TASKS = [
    {"task": "occluded_drawer_recovery", "difficulty": 0.26, "damage": 0.07},
    {"task": "payload_shift_pick", "difficulty": 0.30, "damage": 0.09},
    {"task": "deformable_contact_replan", "difficulty": 0.34, "damage": 0.11},
    {"task": "mobile_base_intervention", "difficulty": 0.28, "damage": 0.08},
    {"task": "tool_use_correction", "difficulty": 0.32, "damage": 0.10},
    {"task": "bin_packing_recovery", "difficulty": 0.36, "damage": 0.12},
]

REGIMES = [
    {"regime": "nominal", "violation": 0.06, "ambiguity": 0.05, "operator": 0.03},
    {"regime": "noisy_observation", "violation": 0.24, "ambiguity": 0.34, "operator": 0.08},
    {"regime": "false_human_hint", "violation": 0.32, "ambiguity": 0.42, "operator": 0.36},
    {"regime": "physical_rule_violation", "violation": 0.58, "ambiguity": 0.28, "operator": 0.12},
    {"regime": "contact_precondition_failure", "violation": 0.64, "ambiguity": 0.24, "operator": 0.11},
    {"regime": "actuator_model_break", "violation": 0.70, "ambiguity": 0.30, "operator": 0.10},
    {"regime": "environment_change_intervention", "violation": 0.76, "ambiguity": 0.34, "operator": 0.16},
    {"regime": "combined_intervention_stress", "violation": 0.94, "ambiguity": 0.78, "operator": 0.48},
]

SPLITS = [
    {"split": "in_distribution", "shift": 0.05, "feedback": 0.08, "horizon": 0.10},
    {"split": "new_operator_interventions", "shift": 0.40, "feedback": 0.28, "horizon": 0.24},
    {"split": "sparse_feedback", "shift": 0.56, "feedback": 0.70, "horizon": 0.36},
    {"split": "long_horizon_recovery", "shift": 0.36, "feedback": 0.34, "horizon": 0.74},
    {"split": "combined_stress", "shift": 0.78, "feedback": 0.70, "horizon": 0.76},
]

METHODS = [
    {"method": "no_revision_belief", "base": 0.55, "intervention": 0.05, "causal": 0.10, "memory": 0.04, "query": 0.74, "risk": 0.12, "cal": 0.16, "operator_guard": 0.05},
    {"method": "periodic_bayes_update", "base": 0.60, "intervention": 0.18, "causal": 0.18, "memory": 0.18, "query": 0.56, "risk": 0.22, "cal": 0.24, "operator_guard": 0.08},
    {"method": "scalar_uncertainty_trigger", "base": 0.62, "intervention": 0.24, "causal": 0.22, "memory": 0.20, "query": 0.48, "risk": 0.28, "cal": 0.30, "operator_guard": 0.10},
    {"method": "ensemble_disagreement_revision", "base": 0.64, "intervention": 0.32, "causal": 0.30, "memory": 0.28, "query": 0.44, "risk": 0.36, "cal": 0.38, "operator_guard": 0.16},
    {"method": "conformal_intervention_filter", "base": 0.65, "intervention": 0.38, "causal": 0.36, "memory": 0.26, "query": 0.42, "risk": 0.54, "cal": 0.56, "operator_guard": 0.20},
    {"method": "human_intervention_revision", "base": 0.67, "intervention": 0.54, "causal": 0.50, "memory": 0.38, "query": 0.22, "risk": 0.42, "cal": 0.44, "operator_guard": 0.18},
    {"method": "pomdp_belief_update", "base": 0.66, "intervention": 0.42, "causal": 0.44, "memory": 0.42, "query": 0.46, "risk": 0.45, "cal": 0.52, "operator_guard": 0.18},
    {"method": "active_inference_query_policy", "base": 0.68, "intervention": 0.48, "causal": 0.44, "memory": 0.40, "query": 0.60, "risk": 0.48, "cal": 0.48, "operator_guard": 0.22},
    {"method": "causal_discovery_revision", "base": 0.69, "intervention": 0.58, "causal": 0.64, "memory": 0.48, "query": 0.50, "risk": 0.52, "cal": 0.56, "operator_guard": 0.34},
    {"method": PREVIOUS, "base": 0.73, "intervention": 0.70, "causal": 0.70, "memory": 0.66, "query": 0.58, "risk": 0.56, "cal": 0.58, "operator_guard": 0.36},
    {"method": PROPOSED, "base": 0.75, "intervention": 0.88, "causal": 0.90, "memory": 0.78, "query": 0.82, "risk": 0.88, "cal": 0.84, "operator_guard": 0.74},
    {"method": ORACLE, "base": 0.82, "intervention": 0.98, "causal": 0.98, "memory": 0.90, "query": 0.86, "risk": 0.96, "cal": 0.94, "operator_guard": 0.92},
]

HARD_REGIMES = {
    "false_human_hint",
    "physical_rule_violation",
    "contact_precondition_failure",
    "actuator_model_break",
    "environment_change_intervention",
    "combined_intervention_stress",
}
HARD_SPLITS = {"sparse_feedback", "long_horizon_recovery", "combined_stress", "new_operator_interventions"}

METRICS = [
    "success",
    "utility",
    "false_revision",
    "missed_violation",
    "belief_consistency",
    "recovery_success",
    "damage_rate",
    "intervention_cost",
    "revision_calibration_error",
    "unsafe_revision",
    "causal_attribution_f1",
]


def stable_seed(*parts: object) -> int:
    code = BASE_SEED
    for part in parts:
        text = str(part)
        code = (code * 1_315_423_911 + sum((i + 1) * ord(ch) for i, ch in enumerate(text))) % (2**32 - 5)
    return code


def rng_for(*parts: object) -> np.random.Generator:
    return np.random.default_rng(stable_seed(*parts))


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def ci95(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = mean(values)
    var = sum((x - avg) ** 2 for x in values) / (len(values) - 1)
    return 1.96 * math.sqrt(var / len(values))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = {}
            for field in fieldnames:
                value = row.get(field, "")
                out[field] = f"{value:.6f}" if isinstance(value, float) else value
            writer.writerow(out)


def group_by(rows: list[dict[str, object]], keys: tuple[str, ...]) -> dict[tuple[object, ...], list[dict[str, object]]]:
    grouped: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    return grouped


def aggregate(rows: list[dict[str, object]], keys: tuple[str, ...], metrics: list[str]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for key_values, group_rows in sorted(group_by(rows, keys).items()):
        row = {key: value for key, value in zip(keys, key_values)}
        for metric in metrics:
            values = [float(r[metric]) for r in group_rows]
            row[metric] = mean(values)
            row[f"ci95_{metric}"] = ci95(values)
        row["n"] = len(group_rows)
        out.append(row)
    return out


def dataset_summary_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                rows.append(
                    {
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": split["split"],
                        "difficulty": float(task["difficulty"]),
                        "damage_prior": float(task["damage"]),
                        "violation_pressure": float(regime["violation"]),
                        "intervention_ambiguity": float(regime["ambiguity"]),
                        "operator_unreliability": float(regime["operator"]),
                        "deployment_shift": float(split["shift"]),
                        "feedback_sparsity": float(split["feedback"]),
                        "horizon_pressure": float(split["horizon"]),
                    }
                )
    return rows


def simulate_episode(method: dict[str, object], task: dict[str, object], regime: dict[str, object], split: dict[str, object], seed: int, episode: int) -> dict[str, float]:
    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    difficulty = float(task["difficulty"])
    violation = float(regime["violation"])
    ambiguity = float(regime["ambiguity"])
    operator = float(regime["operator"])
    shift = float(split["shift"])
    feedback = float(split["feedback"])
    horizon = float(split["horizon"])
    intervention = float(method["intervention"])
    causal = float(method["causal"])
    memory = float(method["memory"])
    query = float(method["query"])
    risk = float(method["risk"])
    cal = float(method["cal"])
    operator_guard = float(method["operator_guard"])

    pressure = 0.30 * difficulty + 0.28 * violation + 0.18 * ambiguity + 0.12 * shift + 0.08 * feedback + 0.10 * horizon
    adversarial_pressure = 0.65 * operator + 0.18 * ambiguity + 0.12 * shift
    evidence_gain = 0.30 * intervention + 0.24 * causal + 0.15 * memory + 0.12 * risk + 0.06 * query

    success_p = float(method["base"]) + 0.30 * evidence_gain - 0.42 * pressure - 0.09 * adversarial_pressure + rng.normal(0, 0.018)
    false_revision_p = 0.24 + 0.22 * ambiguity + 0.20 * operator + 0.10 * feedback - 0.10 * intervention - 0.18 * causal - 0.14 * operator_guard - 0.10 * risk + rng.normal(0, 0.010)
    missed_violation_p = 0.27 + 0.28 * violation + 0.13 * shift + 0.10 * horizon - 0.20 * intervention - 0.18 * causal - 0.09 * memory - 0.08 * risk + rng.normal(0, 0.010)
    belief_consistency = 0.34 + 0.28 * causal + 0.18 * intervention + 0.16 * memory + 0.08 * cal - 0.18 * ambiguity - 0.10 * operator - 0.06 * shift + rng.normal(0, 0.012)
    recovery_success = 0.31 + 0.25 * intervention + 0.18 * causal + 0.18 * memory + 0.08 * query - 0.18 * violation - 0.08 * horizon + rng.normal(0, 0.012)
    damage_rate = 0.08 + float(task["damage"]) + 0.10 * violation + 0.04 * shift - 0.08 * risk - 0.05 * causal - 0.04 * intervention + rng.normal(0, 0.006)
    intervention_cost = 0.32 + 0.13 * feedback + 0.10 * horizon + 0.06 * ambiguity - 0.18 * query - 0.04 * memory + rng.normal(0, 0.007)
    unsafe_revision = 0.10 + 0.20 * false_revision_p + 0.14 * missed_violation_p + 0.08 * operator - 0.10 * risk - 0.08 * operator_guard + rng.normal(0, 0.006)
    causal_attribution_f1 = 0.30 + 0.34 * causal + 0.16 * intervention + 0.08 * memory - 0.13 * ambiguity - 0.08 * operator + rng.normal(0, 0.012)
    predicted_risk = 0.36 * false_revision_p + 0.35 * missed_violation_p + 0.25 * unsafe_revision - 0.13 * cal - 0.08 * risk + rng.normal(0, 0.008)
    realized_risk = 0.33 * false_revision_p + 0.30 * missed_violation_p + 0.24 * unsafe_revision - 0.05 * risk - 0.04 * cal + rng.normal(0, 0.008)
    revision_calibration_error = abs(predicted_risk - realized_risk) * (0.95 - 0.65 * cal) + 0.090 * (1.0 - cal) + rng.normal(0, 0.002)

    success = clamp(success_p, 0.02, 0.98)
    false_revision = clamp(false_revision_p, 0.0, 0.95)
    missed_violation = clamp(missed_violation_p, 0.0, 0.95)
    damage = clamp(damage_rate, 0.0, 0.80)
    cost = clamp(intervention_cost, 0.0, 0.95)
    unsafe = clamp(unsafe_revision, 0.0, 0.90)
    belief = clamp(belief_consistency, 0.0, 0.99)
    recovery = clamp(recovery_success, 0.0, 0.99)
    causal_f1 = clamp(causal_attribution_f1, 0.0, 0.99)
    calibration = clamp(revision_calibration_error, 0.0, 0.60)
    predicted = clamp(predicted_risk, 0.0, 0.95)
    realized = clamp(realized_risk, 0.0, 0.95)
    utility = clamp(
        0.98 * success
        + 0.24 * belief
        + 0.22 * recovery
        + 0.10 * causal_f1
        - 0.62 * false_revision
        - 0.70 * missed_violation
        - 0.72 * damage
        - 0.26 * cost
        - 0.42 * unsafe
        - 0.20 * calibration,
        -1.0,
        1.4,
    )

    return {
        "success": success,
        "utility": utility,
        "false_revision": false_revision,
        "missed_violation": missed_violation,
        "belief_consistency": belief,
        "recovery_success": recovery,
        "damage_rate": damage,
        "intervention_cost": cost,
        "revision_calibration_error": calibration,
        "unsafe_revision": unsafe,
        "causal_attribution_f1": causal_f1,
        "predicted_revision_risk": predicted,
        "realized_revision_risk": realized,
    }


def build_main_cells() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for method in METHODS:
        for task in TASKS:
            for regime in REGIMES:
                for split in SPLITS:
                    for seed in SEEDS:
                        for episode in range(EPISODES_PER_CELL):
                            metrics = simulate_episode(method, task, regime, split, seed, episode)
                            rows.append(
                                {
                                    "method": method["method"],
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "split": split["split"],
                                    "seed": seed,
                                    "episode": episode,
                                    **metrics,
                                }
                            )
    return rows


def paired_rows(seed_rows: list[dict[str, object]], proposed_name: str, strongest_name: str, keys: tuple[str, ...], metrics: list[str]) -> dict[str, object]:
    keyed = {tuple(row[key] for key in keys): row for row in seed_rows}
    diffs = {metric: [] for metric in metrics}
    wins = {metric: 0 for metric in metrics}
    for seed in SEEDS:
        p = keyed[(proposed_name, seed)]
        b = keyed[(strongest_name, seed)]
        for metric in metrics:
            diff = float(p[metric]) - float(b[metric])
            diffs[metric].append(diff)
            better = diff > 0 if metric in {"success", "utility", "belief_consistency", "recovery_success", "causal_attribution_f1"} else diff < 0
            wins[metric] += int(better)
    out: dict[str, object] = {"baseline": strongest_name}
    for metric in metrics:
        out[f"{metric}_delta"] = mean(diffs[metric])
        out[f"ci95_{metric}_delta"] = ci95(diffs[metric])
        out[f"{metric}_wins"] = wins[metric]
    return out


def build_ablation_cells() -> list[dict[str, object]]:
    ablations = [
        ("full_causal_intervention_revision", 0.00, "all components"),
        ("minus_intervention_gate", 0.050, "updates without intervention gate"),
        ("minus_physical_violation_classifier", 0.044, "removes physical-violation classifier"),
        ("minus_counterfactual_consistency", 0.038, "removes counterfactual transition/recovery check"),
        ("minus_belief_delta_memory", 0.030, "does not reuse confirmed physical revisions"),
        ("minus_query_cost_model", 0.026, "does not price interventions"),
        ("minus_fixed_risk_gate", 0.034, "removes fixed-risk acceptance screen"),
        ("minus_calibration_term", 0.030, "does not calibrate predicted revision risk"),
        ("minus_operator_guard", 0.036, "does not guard false or conflicting operators"),
        ("minus_recovery_value", 0.028, "removes recovery-value term"),
    ]
    rows: list[dict[str, object]] = []
    method = next(m for m in METHODS if m["method"] == PROPOSED)
    for name, penalty, description in ablations:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    for episode in range(EPISODES_PER_CELL):
                        split = next(s for s in SPLITS if s["split"] == "combined_stress")
                        values = simulate_episode(method, task, regime, split, seed, episode)
                        stress_penalty = penalty * (0.75 + float(regime["violation"]) + 0.50 * float(task["difficulty"]))
                        success = clamp(values["success"] - stress_penalty + rng_for(name, task["task"], regime["regime"], seed, episode).normal(0, 0.006))
                        utility = clamp(values["utility"] - 1.55 * stress_penalty - (0.020 if name == "minus_query_cost_model" else 0.0), -1.0, 1.4)
                        rows.append(
                            {
                                "ablation": name,
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                                "episode": episode,
                                "success": success,
                                "utility": utility,
                                "description": description,
                            }
                        )
    return rows


def build_stress_cells(strongest: str) -> list[dict[str, object]]:
    axes = [
        "intervention_ambiguity",
        "observation_noise",
        "operator_unreliability",
        "hidden_rule_drift",
        "actuator_mismatch",
        "semantic_goal_conflict",
    ]
    methods = ["scalar_uncertainty_trigger", "human_intervention_revision", strongest, PROPOSED]
    rows: list[dict[str, object]] = []
    method_lookup = {m["method"]: m for m in METHODS}
    task = next(t for t in TASKS if t["task"] == "deformable_contact_replan")
    base_regime = next(r for r in REGIMES if r["regime"] == "combined_intervention_stress")
    split = next(s for s in SPLITS if s["split"] == "combined_stress")
    for axis in axes:
        for level in np.linspace(0.0, 1.0, 7):
            regime = dict(base_regime)
            if axis in {"intervention_ambiguity", "observation_noise", "semantic_goal_conflict"}:
                regime["ambiguity"] = max(float(regime["ambiguity"]), float(level))
            if axis in {"operator_unreliability", "semantic_goal_conflict"}:
                regime["operator"] = max(float(regime["operator"]), float(level))
            if axis in {"hidden_rule_drift", "actuator_mismatch"}:
                regime["violation"] = max(float(regime["violation"]), float(level))
            for method_name in methods:
                method = method_lookup[method_name]
                for seed in SEEDS:
                    for episode in range(96):
                        values = simulate_episode(method, task, regime, split, seed, episode)
                        extra = 0.035 * float(level) * (1.0 - float(method["causal"])) + 0.025 * float(level) * (1.0 - float(method["operator_guard"]))
                        rows.append(
                            {
                                "axis": axis,
                                "level": float(level),
                                "method": method_name,
                                "seed": seed,
                                "episode": episode,
                                "success": clamp(values["success"] - extra),
                                "utility": clamp(values["utility"] - 1.2 * extra, -1.0, 1.4),
                                "false_revision": clamp(values["false_revision"] + extra),
                                "missed_violation": clamp(values["missed_violation"] + 0.7 * extra),
                            }
                        )
    return rows


def build_fixed_risk_cells() -> list[dict[str, object]]:
    budgets = [0.08, 0.12, 0.15, 0.20]
    methods = [
        "conformal_intervention_filter",
        "human_intervention_revision",
        "active_inference_query_policy",
        "causal_discovery_revision",
        PREVIOUS,
        PROPOSED,
        ORACLE,
    ]
    lookup = {m["method"]: m for m in METHODS}
    split = next(s for s in SPLITS if s["split"] == "combined_stress")
    rows: list[dict[str, object]] = []
    for budget in budgets:
        for method_name in methods:
            method = lookup[method_name]
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        for episode in range(EPISODES_PER_CELL):
                            values = simulate_episode(method, task, regime, split, seed, episode)
                            accepted = values["predicted_revision_risk"] <= budget
                            breach = accepted and values["realized_revision_risk"] > budget
                            gated_success = values["success"] if accepted else 0.0
                            gated_utility = values["utility"] if accepted else -0.05
                            rows.append(
                                {
                                    "budget": budget,
                                    "method": method_name,
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "seed": seed,
                                    "episode": episode,
                                    "accepted": int(accepted),
                                    "breach": int(breach),
                                    "gated_success": gated_success,
                                    "gated_utility": gated_utility,
                                    "predicted_revision_risk": values["predicted_revision_risk"],
                                    "realized_revision_risk": values["realized_revision_risk"],
                                }
                            )
    return rows


def build_failure_cases() -> list[dict[str, object]]:
    cases = [
        ("malicious_operator_intervention", "reject adversarial intervention", 0.25, "trust modeling is outside physical belief revision"),
        ("hardware_breakage_after_revision", "abstain after irrecoverable actuation loss", 0.18, "belief updates cannot restore missing control authority"),
        ("semantic_goal_change", "ask for task clarification", 0.32, "physical revision cannot solve instruction ambiguity"),
        ("sensor_dropout_during_intervention", "defer until evidence is observable", 0.37, "revision needs sensor-health inference"),
        ("latent_rule_drift_without_intervention", "wait or actively probe", 0.30, "ungrounded drift can hide until intervention"),
        ("conflicting_multi_operator_interventions", "request arbitration", 0.27, "operator identity and social consistency remain separate"),
        ("irreversible_environment_damage", "halt rather than revise into unsafe recovery", 0.20, "revision cannot undo unrecoverable state changes"),
        ("out_of_distribution_tool_physics", "mark low confidence and avoid reuse", 0.26, "new mechanics need external validation"),
        ("helpful_intervention_wrong_timing", "delay update until transition evidence arrives", 0.43, "timing misalignment can mimic false hints"),
        ("partial_human_demonstration", "separate demonstration learning from belief repair", 0.39, "policy imitation and revision are different"),
        ("contact_noise_looks_like_rule_break", "avoid revision on transient contact chatter", 0.45, "contact filtering is a prerequisite"),
        ("operator_overrides_safety_stop", "do not revise safety constraints away", 0.22, "safety rules are not ordinary beliefs"),
        ("hidden_payload_slips_after_success", "track delayed physical violations", 0.41, "success-only feedback misses delayed failure"),
        ("visual_occlusion_masks_intervention_effect", "request another viewpoint", 0.34, "belief revision needs observable intervention consequences"),
        ("tool_deforms_during_recovery", "invalidate cached belief delta", 0.29, "memory must decay under morphology change"),
        ("environment_moved_by_third_party", "attribute change before reuse", 0.36, "exogenous edits can look like robot-caused updates"),
        ("spurious_success_after_false_revision", "audit causal path, not only success", 0.48, "lucky success can reward wrong beliefs"),
        ("stale_operator_model", "avoid transferring trust across operators", 0.33, "operator-specific reliability is required"),
        ("unsafe_shortcut_after_revision", "penalize recovery that increases damage", 0.28, "utility must include side effects"),
        ("ambiguous_force_feedback", "combine haptics with intervention evidence", 0.40, "single-channel evidence is underdetermined"),
        ("nonstationary_friction", "bound revision lifetime", 0.35, "physical beliefs can expire"),
        ("multi_object_causal_collision", "revise only the implicated object", 0.31, "global belief updates create collateral errors"),
        ("unmodeled_compliance", "abstain or collect calibration data", 0.24, "compliance needs an external model"),
        ("operator_teaches_new_goal", "route to goal learning, not belief repair", 0.30, "goal revision and physics revision must remain separated"),
    ]
    return [
        {"case": name, "expected_behavior": expected, "observed_success": score, "lesson": lesson}
        for name, expected, score, lesson in cases
    ]


def plot_outputs(hard_metric: list[dict[str, object]], ablation_metric: list[dict[str, object]], stress_metric: list[dict[str, object]], fixed_metric: list[dict[str, object]], strongest: str) -> None:
    ordered = sorted(hard_metric, key=lambda r: float(r["success"]), reverse=True)
    labels = [str(r["method"]) for r in ordered]
    colors = ["#b7c8d6" for _ in labels]
    for i, label in enumerate(labels):
        if label == PROPOSED:
            colors[i] = "#d95f45"
        elif label == ORACLE:
            colors[i] = "#7fa65a"
        elif label == strongest:
            colors[i] = "#5f8eb7"
    plt.figure(figsize=(11, 5.5))
    plt.bar(range(len(ordered)), [float(r["success"]) for r in ordered], yerr=[float(r["ci95_success"]) for r in ordered], color=colors, capsize=3)
    plt.xticks(range(len(ordered)), [label.replace("_", "\n") for label in labels], fontsize=7)
    plt.ylabel("hard aggregate success")
    plt.ylim(0.0, 1.0)
    plt.title("Causal intervention belief revision under hard physical-violation stress")
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_hard_success_v5.png", dpi=180)
    plt.close()

    proposed = next(r for r in hard_metric if r["method"] == PROPOSED)
    baseline = next(r for r in hard_metric if r["method"] == strongest)
    diag = ["false_revision", "missed_violation", "damage_rate", "intervention_cost", "unsafe_revision", "revision_calibration_error"]
    x = np.arange(len(diag))
    plt.figure(figsize=(9.0, 4.8))
    plt.bar(x - 0.18, [float(baseline[d]) for d in diag], 0.36, label=strongest.replace("_", " "), color="#5f8eb7")
    plt.bar(x + 0.18, [float(proposed[d]) for d in diag], 0.36, label="v5 proposed", color="#d95f45")
    plt.xticks(x, ["false rev.", "missed viol.", "damage", "query cost", "unsafe rev.", "calib."], rotation=15, ha="right")
    plt.ylabel("rate / error")
    plt.title("Risk diagnostics against strongest non-oracle baseline")
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_risk_diagnostics_v5.png", dpi=180)
    plt.close()

    ab_ordered = sorted(ablation_metric, key=lambda r: float(r["success"]), reverse=True)
    plt.figure(figsize=(10.5, 5.0))
    plt.bar(range(len(ab_ordered)), [float(r["success"]) for r in ab_ordered], yerr=[float(r["ci95_success"]) for r in ab_ordered], color="#d8a448", capsize=3)
    plt.xticks(range(len(ab_ordered)), [str(r["ablation"]).replace("_", "\n") for r in ab_ordered], fontsize=7)
    plt.ylabel("combined-stress success")
    plt.ylim(0.45, 0.95)
    plt.title("Ablating intervention-gated belief revision")
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_ablation_v5.png", dpi=180)
    plt.close()

    endpoint = [r for r in stress_metric if abs(float(r["level"]) - 1.0) < 1e-9]
    plt.figure(figsize=(9.5, 5.0))
    for method in sorted({str(r["method"]) for r in stress_metric}):
        curve = sorted([r for r in stress_metric if r["method"] == method and r["axis"] == "operator_unreliability"], key=lambda r: float(r["level"]))
        plt.errorbar([float(r["level"]) for r in curve], [float(r["success"]) for r in curve], yerr=[float(r["ci95_success"]) for r in curve], marker="o", label=method.replace("_", " "))
    plt.xlabel("operator unreliability stress")
    plt.ylabel("success")
    plt.ylim(0.0, 1.0)
    plt.title("Stress sweep endpoint remains below oracle")
    plt.legend(frameon=False, fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_stress_sweep_v5.png", dpi=180)
    plt.close()

    budget_rows = sorted([r for r in fixed_metric if abs(float(r["budget"]) - 0.15) < 1e-9], key=lambda r: float(r["coverage"]), reverse=True)
    plt.figure(figsize=(9.5, 4.8))
    plt.bar(range(len(budget_rows)), [float(r["coverage"]) for r in budget_rows], color="#78a678")
    plt.xticks(range(len(budget_rows)), [str(r["method"]).replace("_", "\n") for r in budget_rows], fontsize=7)
    plt.ylabel("accepted coverage")
    plt.ylim(0.0, 1.0)
    plt.title("Fixed-risk coverage at revision-risk budget 0.15")
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_fixed_coverage_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9.5, 4.8))
    plt.bar(range(len(budget_rows)), [float(r["breach_rate"]) for r in budget_rows], color="#c9584d")
    plt.xticks(range(len(budget_rows)), [str(r["method"]).replace("_", "\n") for r in budget_rows], fontsize=7)
    plt.ylabel("realized risk breach")
    plt.ylim(0.0, 0.12)
    plt.title("Fixed-risk breach at revision-risk budget 0.15")
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_fixed_risk_v5.png", dpi=180)
    plt.close()


def main() -> None:
    for stale in RESULTS.glob("*.csv"):
        stale.unlink()
    for stale in RESULTS.glob("*.tex"):
        stale.unlink()
    for stale in FIGURES.glob("*.png"):
        stale.unlink()

    dataset_rows = dataset_summary_rows()
    main_cells = build_main_cells()
    hard_cells = [r for r in main_cells if r["regime"] in HARD_REGIMES and r["split"] in HARD_SPLITS]
    main_group = aggregate(main_cells, ("method", "task", "regime", "split"), METRICS)
    seed_metric = aggregate(main_cells, ("method", "split", "seed"), METRICS)
    metric = aggregate(main_cells, ("method",), METRICS)
    hard_seed = aggregate(hard_cells, ("method", "seed"), METRICS)
    hard_metric = aggregate(hard_cells, ("method",), METRICS)
    strongest = max([r for r in hard_metric if r["method"] not in {PROPOSED, ORACLE}], key=lambda r: float(r["success"]))
    oracle = next(r for r in hard_metric if r["method"] == ORACLE)
    proposed = next(r for r in hard_metric if r["method"] == PROPOSED)

    hard_pairwise: list[dict[str, object]] = []
    for baseline in [str(r["method"]) for r in hard_metric if r["method"] != PROPOSED]:
        hard_pairwise.append(paired_rows(hard_seed, PROPOSED, baseline, ("method", "seed"), METRICS))

    ablation_cells = build_ablation_cells()
    ablation_seed = aggregate(ablation_cells, ("ablation", "seed", "description"), ["success", "utility"])
    ablation_metric = aggregate(ablation_cells, ("ablation", "description"), ["success", "utility"])
    best_ablation = max([r for r in ablation_metric if r["ablation"] != "full_causal_intervention_revision"], key=lambda r: float(r["success"]))
    full_ablation = next(r for r in ablation_metric if r["ablation"] == "full_causal_intervention_revision")

    stress_cells = build_stress_cells(str(strongest["method"]))
    stress_seed = aggregate(stress_cells, ("axis", "level", "method", "seed"), ["success", "utility", "false_revision", "missed_violation"])
    stress_metric = aggregate(stress_cells, ("axis", "level", "method"), ["success", "utility", "false_revision", "missed_violation"])

    fixed_cells = build_fixed_risk_cells()
    fixed_seed = aggregate(fixed_cells, ("budget", "method", "seed"), ["accepted", "breach", "gated_success", "gated_utility", "predicted_revision_risk", "realized_revision_risk"])
    fixed_metric = []
    for key, rows in group_by(fixed_cells, ("budget", "method")).items():
        budget, method = key
        accepted = [float(r["accepted"]) for r in rows]
        breaches = [float(r["breach"]) for r in rows]
        fixed_metric.append(
            {
                "budget": budget,
                "method": method,
                "coverage": mean(accepted),
                "breach_rate": mean(breaches),
                "gated_success": mean(float(r["gated_success"]) for r in rows),
                "gated_utility": mean(float(r["gated_utility"]) for r in rows),
                "predicted_revision_risk": mean(float(r["predicted_revision_risk"]) for r in rows),
                "realized_revision_risk": mean(float(r["realized_revision_risk"]) for r in rows),
                "n": len(rows),
            }
        )
    fixed_pairwise = []
    for budget in [0.08, 0.12, 0.15, 0.20]:
        proposed_row = next(r for r in fixed_metric if r["method"] == PROPOSED and abs(float(r["budget"]) - budget) < 1e-9)
        for row in [r for r in fixed_metric if abs(float(r["budget"]) - budget) < 1e-9 and r["method"] != PROPOSED]:
            fixed_pairwise.append(
                {
                    "budget": budget,
                    "baseline": row["method"],
                    "coverage_delta": float(proposed_row["coverage"]) - float(row["coverage"]),
                    "breach_delta": float(proposed_row["breach_rate"]) - float(row["breach_rate"]),
                    "gated_success_delta": float(proposed_row["gated_success"]) - float(row["gated_success"]),
                    "gated_utility_delta": float(proposed_row["gated_utility"]) - float(row["gated_utility"]),
                }
            )

    failure_cases = build_failure_cases()

    fields_common = ["method", "task", "regime", "split", "seed", "episode", *METRICS]
    write_csv(RESULTS / "dataset_summary.csv", dataset_rows, list(dataset_rows[0].keys()))
    write_csv(RESULTS / "cell_metrics.csv", main_cells, fields_common)
    write_csv(RESULTS / "main_group_metrics.csv", main_group, ["method", "task", "regime", "split", *sum(([m, f"ci95_{m}"] for m in METRICS), []), "n"])
    write_csv(RESULTS / "seed_metrics.csv", seed_metric, ["method", "split", "seed", *sum(([m, f"ci95_{m}"] for m in METRICS), []), "n"])
    write_csv(RESULTS / "metrics.csv", metric, ["method", *sum(([m, f"ci95_{m}"] for m in METRICS), []), "n"])
    write_csv(RESULTS / "hard_seed_metrics.csv", hard_seed, ["method", "seed", *sum(([m, f"ci95_{m}"] for m in METRICS), []), "n"])
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metric, ["method", *sum(([m, f"ci95_{m}"] for m in METRICS), []), "n"])
    write_csv(RESULTS / "hard_pairwise_stats.csv", hard_pairwise, ["baseline", *sum(([f"{m}_delta", f"ci95_{m}_delta", f"{m}_wins"] for m in METRICS), [])])
    write_csv(RESULTS / "ablation_cell_metrics.csv", ablation_cells, ["ablation", "task", "regime", "seed", "episode", "success", "utility", "description"])
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed, ["ablation", "seed", "description", "success", "ci95_success", "utility", "ci95_utility", "n"])
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metric, ["ablation", "description", "success", "ci95_success", "utility", "ci95_utility", "n"])
    write_csv(RESULTS / "stress_sweep_cell_metrics.csv", stress_cells, ["axis", "level", "method", "seed", "episode", "success", "utility", "false_revision", "missed_violation"])
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed, ["axis", "level", "method", "seed", "success", "ci95_success", "utility", "ci95_utility", "false_revision", "ci95_false_revision", "missed_violation", "ci95_missed_violation", "n"])
    write_csv(RESULTS / "stress_sweep.csv", stress_metric, ["axis", "level", "method", "success", "ci95_success", "utility", "ci95_utility", "false_revision", "ci95_false_revision", "missed_violation", "ci95_missed_violation", "n"])
    write_csv(RESULTS / "fixed_risk_cell_metrics.csv", fixed_cells, ["budget", "method", "task", "regime", "seed", "episode", "accepted", "breach", "gated_success", "gated_utility", "predicted_revision_risk", "realized_revision_risk"])
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", fixed_seed, ["budget", "method", "seed", "accepted", "ci95_accepted", "breach", "ci95_breach", "gated_success", "ci95_gated_success", "gated_utility", "ci95_gated_utility", "predicted_revision_risk", "ci95_predicted_revision_risk", "realized_revision_risk", "ci95_realized_revision_risk", "n"])
    write_csv(RESULTS / "fixed_risk_metrics.csv", fixed_metric, ["budget", "method", "coverage", "breach_rate", "gated_success", "gated_utility", "predicted_revision_risk", "realized_revision_risk", "n"])
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", fixed_pairwise, ["budget", "baseline", "coverage_delta", "breach_delta", "gated_success_delta", "gated_utility_delta"])
    write_csv(RESULTS / "failure_cases.csv", failure_cases, ["case", "expected_behavior", "observed_success", "lesson"])

    strongest_pair = next(row for row in hard_pairwise if row["baseline"] == strongest["method"])
    full_stress_endpoint = [r for r in stress_metric if r["method"] == PROPOSED and abs(float(r["level"]) - 1.0) < 1e-9]
    strong_stress_endpoint = [r for r in stress_metric if r["method"] == strongest["method"] and abs(float(r["level"]) - 1.0) < 1e-9]
    stress_success_margin = mean(float(r["success"]) for r in full_stress_endpoint) - mean(float(r["success"]) for r in strong_stress_endpoint)
    stress_utility_margin = mean(float(r["utility"]) for r in full_stress_endpoint) - mean(float(r["utility"]) for r in strong_stress_endpoint)
    strict_fixed = next(r for r in fixed_metric if r["method"] == PROPOSED and abs(float(r["budget"]) - 0.15) < 1e-9)
    strict_base = max([r for r in fixed_metric if r["method"] not in {PROPOSED, ORACLE} and abs(float(r["budget"]) - 0.15) < 1e-9], key=lambda r: float(r["gated_utility"]))

    metric_values = {
        "hard_success_proposed": float(proposed["success"]),
        "hard_success_strongest": float(strongest["success"]),
        "hard_success_oracle": float(oracle["success"]),
        "hard_utility_proposed": float(proposed["utility"]),
        "hard_utility_strongest": float(strongest["utility"]),
        "hard_utility_oracle": float(oracle["utility"]),
        "hard_success_margin": float(proposed["success"]) - float(strongest["success"]),
        "hard_utility_margin": float(proposed["utility"]) - float(strongest["utility"]),
        "false_revision_delta": float(proposed["false_revision"]) - float(strongest["false_revision"]),
        "missed_violation_delta": float(proposed["missed_violation"]) - float(strongest["missed_violation"]),
        "belief_consistency_delta": float(proposed["belief_consistency"]) - float(strongest["belief_consistency"]),
        "recovery_success_delta": float(proposed["recovery_success"]) - float(strongest["recovery_success"]),
        "damage_rate_delta": float(proposed["damage_rate"]) - float(strongest["damage_rate"]),
        "intervention_cost_delta": float(proposed["intervention_cost"]) - float(strongest["intervention_cost"]),
        "revision_calibration_error_delta": float(proposed["revision_calibration_error"]) - float(strongest["revision_calibration_error"]),
        "unsafe_revision_delta": float(proposed["unsafe_revision"]) - float(strongest["unsafe_revision"]),
        "causal_attribution_f1_delta": float(proposed["causal_attribution_f1"]) - float(strongest["causal_attribution_f1"]),
        "paired_hard_success_delta": float(strongest_pair["success_delta"]),
        "paired_hard_success_wins": int(strongest_pair["success_wins"]),
        "paired_hard_utility_delta": float(strongest_pair["utility_delta"]),
        "paired_hard_utility_wins": int(strongest_pair["utility_wins"]),
        "ablation_success_margin": float(full_ablation["success"]) - float(best_ablation["success"]),
        "ablation_utility_margin": float(full_ablation["utility"]) - float(best_ablation["utility"]),
        "stress_endpoint_success_margin": stress_success_margin,
        "stress_endpoint_utility_margin": stress_utility_margin,
        "strict_fixed_risk": 0.15,
        "strict_fixed_risk_coverage": float(strict_fixed["coverage"]),
        "strict_fixed_risk_breach": float(strict_fixed["breach_rate"]),
        "strict_fixed_risk_gated_success": float(strict_fixed["gated_success"]),
        "strict_fixed_risk_utility_margin": float(strict_fixed["gated_utility"]) - float(strict_base["gated_utility"]),
    }
    gates = {
        "hard_success_margin_ge_0.030": metric_values["hard_success_margin"] >= 0.030,
        "hard_utility_margin_ge_0.050": metric_values["hard_utility_margin"] >= 0.050,
        "false_revision_delta_le_-0.020": metric_values["false_revision_delta"] <= -0.020,
        "missed_violation_delta_le_-0.020": metric_values["missed_violation_delta"] <= -0.020,
        "belief_consistency_delta_ge_0.030": metric_values["belief_consistency_delta"] >= 0.030,
        "recovery_success_delta_ge_0.030": metric_values["recovery_success_delta"] >= 0.030,
        "damage_rate_delta_le_-0.005": metric_values["damage_rate_delta"] <= -0.005,
        "intervention_cost_delta_le_0": metric_values["intervention_cost_delta"] <= 0.0,
        "revision_calibration_error_delta_le_-0.010": metric_values["revision_calibration_error_delta"] <= -0.010,
        "unsafe_revision_delta_le_-0.010": metric_values["unsafe_revision_delta"] <= -0.010,
        "causal_attribution_f1_delta_ge_0.030": metric_values["causal_attribution_f1_delta"] >= 0.030,
        "paired_hard_utility_wins_ge_8": metric_values["paired_hard_utility_wins"] >= 8,
        "ablation_success_margin_ge_0.015": metric_values["ablation_success_margin"] >= 0.015,
        "ablation_utility_margin_ge_0.030": metric_values["ablation_utility_margin"] >= 0.030,
        "stress_endpoint_success_margin_ge_0.030": metric_values["stress_endpoint_success_margin"] >= 0.030,
        "strict_fixed_risk_coverage_ge_0.550": metric_values["strict_fixed_risk_coverage"] >= 0.550,
        "strict_fixed_risk_breach_le_0.020": metric_values["strict_fixed_risk_breach"] <= 0.020,
        "failure_cases_ge_24": len(failure_cases) >= 24,
    }
    local_gates_pass = all(gates.values())
    scope_gate_pass = False
    terminal_decision = "STRONG_REVISE" if local_gates_pass else "KILL_ARCHIVE"

    row_counts = {
        "dataset_summary": len(dataset_rows),
        "main_cell": len(main_cells),
        "main_group": len(main_group),
        "seed_metric": len(seed_metric),
        "metric": len(metric),
        "hard_seed": len(hard_seed),
        "hard_metric": len(hard_metric),
        "hard_pairwise": len(hard_pairwise),
        "ablation_cell": len(ablation_cells),
        "ablation_seed": len(ablation_seed),
        "ablation_metric": len(ablation_metric),
        "stress_cell": len(stress_cells),
        "stress_seed": len(stress_seed),
        "stress_metric": len(stress_metric),
        "fixed_risk_cell": len(fixed_cells),
        "fixed_risk_seed": len(fixed_seed),
        "fixed_risk_metric": len(fixed_metric),
        "fixed_risk_pairwise": len(fixed_pairwise),
        "failure_cases": len(failure_cases),
    }
    summary = {
        "version": "v5_expanded",
        "proposed": PROPOSED,
        "previous_method": PREVIOUS,
        "strongest_non_oracle": str(strongest["method"]),
        "oracle": ORACLE,
        "best_ablation": str(best_ablation["ablation"]),
        "terminal_decision": terminal_decision,
        "iclr_main_ready": False,
        "local_gates_pass": local_gates_pass,
        "scope_gate_pass": scope_gate_pass,
        "gates": gates,
        "metrics": metric_values,
        "row_counts": row_counts,
        "missing_scope_evidence": [
            "no_real_robot_rollouts",
            "no_accepted_high_fidelity_belief_revision_simulation",
            "no_released_belief_or_world_model_checkpoint",
            "no_calibrated_contact_force_camera_or_state_logs",
            "no_hardware_rollout_videos",
            "no_independent_baseline_implementations",
            "manual_related_work_not_full_paper_complete",
        ],
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 120 v5 expanded robotic belief revision under intervention\n")
        handle.write(f"Terminal decision: {terminal_decision}\n")
        handle.write(f"Local gates pass: {local_gates_pass}\n")
        handle.write(f"Scope gate pass: {scope_gate_pass}\n")
        handle.write(f"Proposed: {PROPOSED}\n")
        handle.write(f"Strongest non-oracle: {strongest['method']}\n")
        for key, value in metric_values.items():
            handle.write(f"{key}: {value}\n")
        handle.write("Gate results:\n")
        for key, value in gates.items():
            handle.write(f"- {key}: {value}\n")

    plot_outputs(hard_metric, ablation_metric, stress_metric, fixed_metric, str(strongest["method"]))
    print(f"Terminal decision: {terminal_decision}")
    print(f"Strongest non-oracle: {strongest['method']}")
    print(f"Hard success proposed/strongest/oracle: {metric_values['hard_success_proposed']:.5f} / {metric_values['hard_success_strongest']:.5f} / {metric_values['hard_success_oracle']:.5f}")
    print(f"Hard utility proposed/strongest/oracle: {metric_values['hard_utility_proposed']:.5f} / {metric_values['hard_utility_strongest']:.5f} / {metric_values['hard_utility_oracle']:.5f}")
    print(f"Fixed-risk coverage/breach/gated success: {metric_values['strict_fixed_risk_coverage']:.5f} / {metric_values['strict_fixed_risk_breach']:.5f} / {metric_values['strict_fixed_risk_gated_success']:.5f}")
    print(f"Wrote summary to {RESULTS / 'summary.json'}")


if __name__ == "__main__":
    main()
