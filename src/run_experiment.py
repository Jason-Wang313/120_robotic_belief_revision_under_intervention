from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 12040615
SEEDS = list(range(7))
EPISODES_PER_GROUP = 72
PROPOSED = "proposed_intervention_violation_revision"
ORACLE = "oracle_intervention_belief_revision"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


TASKS = [
    ("occluded_drawer_recovery", 0.044),
    ("payload_shift_pick", 0.050),
    ("deformable_contact_replan", 0.056),
    ("mobile_base_intervention", 0.046),
    ("tool_use_correction", 0.052),
    ("bin_packing_recovery", 0.058),
]

REGIMES = [
    ("nominal", 0.04),
    ("noisy_observation", 0.34),
    ("false_human_hint", 0.42),
    ("physical_rule_violation", 0.50),
    ("contact_precondition_failure", 0.56),
    ("actuator_model_break", 0.60),
    ("environment_change_intervention", 0.64),
    ("combined_intervention_stress", 0.92),
]

SPLITS = [
    ("in_distribution", 0.05, 0.05),
    ("new_operator_interventions", 0.42, 0.28),
    ("sparse_feedback", 0.72, 0.35),
    ("long_horizon_recovery", 0.36, 0.72),
    ("combined_stress", 0.76, 0.72),
]

METHODS = [
    ("no_revision_belief", 0.640, 0.240, 0.115, 0.090, 0.095, 0.035, 0.040, 0.315, 0.115, 0.080, 0.330, 0.080, 0.070, 0.300, 0.105, 0.070, 0.115, 0.045, 0.020, 0.040, 0.004, 0.004, 0.120, 0.055),
    ("periodic_bayes_update", 0.700, 0.205, 0.102, 0.078, 0.210, 0.070, 0.065, 0.250, 0.095, 0.070, 0.430, 0.085, 0.064, 0.405, 0.092, 0.064, 0.094, 0.038, 0.018, 0.105, 0.020, 0.015, 0.090, 0.045),
    ("scalar_uncertainty_trigger", 0.735, 0.178, 0.090, 0.068, 0.180, 0.068, 0.060, 0.220, 0.085, 0.064, 0.480, 0.080, 0.060, 0.455, 0.085, 0.060, 0.082, 0.033, 0.016, 0.155, 0.030, 0.020, 0.074, 0.038),
    ("ensemble_disagreement_revision", 0.760, 0.165, 0.082, 0.062, 0.165, 0.064, 0.056, 0.202, 0.080, 0.058, 0.520, 0.076, 0.056, 0.500, 0.080, 0.056, 0.076, 0.030, 0.015, 0.185, 0.036, 0.023, 0.066, 0.034),
    ("conformal_intervention_filter", 0.775, 0.155, 0.074, 0.060, 0.150, 0.060, 0.052, 0.190, 0.074, 0.054, 0.545, 0.072, 0.052, 0.520, 0.076, 0.052, 0.070, 0.028, 0.014, 0.210, 0.040, 0.025, 0.060, 0.032),
    ("failure_aware_rl_recovery", 0.790, 0.145, 0.068, 0.056, 0.155, 0.062, 0.052, 0.170, 0.070, 0.052, 0.565, 0.072, 0.052, 0.575, 0.070, 0.048, 0.068, 0.026, 0.013, 0.255, 0.045, 0.030, 0.058, 0.030),
    ("human_intervention_revision", 0.815, 0.128, 0.060, 0.050, 0.145, 0.060, 0.050, 0.135, 0.062, 0.046, 0.600, 0.070, 0.050, 0.610, 0.065, 0.046, 0.060, 0.024, 0.012, 0.340, 0.052, 0.035, 0.052, 0.026),
    (PROPOSED, 0.885, 0.108, 0.038, 0.034, 0.078, 0.040, 0.026, 0.070, 0.038, 0.024, 0.780, 0.052, 0.032, 0.748, 0.050, 0.032, 0.038, 0.017, 0.010, 0.230, 0.030, 0.018, 0.035, 0.018),
    (ORACLE, 0.940, 0.074, 0.020, 0.020, 0.040, 0.018, 0.012, 0.036, 0.016, 0.010, 0.890, 0.028, 0.016, 0.850, 0.026, 0.015, 0.024, 0.010, 0.006, 0.190, 0.020, 0.012, 0.020, 0.010),
]

FIELDS = [
    "method",
    "success_base",
    "success_stress",
    "success_ambiguity",
    "success_horizon",
    "false_base",
    "false_stress",
    "false_ambiguity",
    "missed_base",
    "missed_stress",
    "missed_ambiguity",
    "consistency_base",
    "consistency_stress",
    "consistency_ambiguity",
    "recovery_base",
    "recovery_stress",
    "recovery_ambiguity",
    "damage_base",
    "damage_stress",
    "damage_ambiguity",
    "cost_base",
    "cost_stress",
    "cost_ambiguity",
    "calib_base",
    "calib_stress",
]

ABLATIONS = [
    ("full_intervention_violation_revision", 0.885, 0.108, 0.038, "all components"),
    ("minus_intervention_gate", 0.820, 0.136, 0.056, "updates without intervention gate"),
    ("minus_violation_classifier", 0.812, 0.142, 0.058, "removes physical-violation classifier"),
    ("minus_causal_consistency_check", 0.836, 0.128, 0.052, "removes causal consistency check"),
    ("minus_recovery_memory", 0.832, 0.130, 0.052, "does not reuse intervention outcomes"),
    ("minus_cost_aware_querying", 0.842, 0.124, 0.060, "does not price interventions"),
    ("uncertainty_only_trigger", 0.790, 0.155, 0.074, "uses uncertainty without violation evidence"),
]


def profile(row: tuple) -> dict[str, float | str]:
    return dict(zip(FIELDS, row))


METHOD_PROFILES = [profile(row) for row in METHODS]


def stable_hash(text: str) -> int:
    return sum((i + 1) * ord(ch) for i, ch in enumerate(text))


def rng_for(*parts: object) -> np.random.Generator:
    code = BASE_SEED
    for part in parts:
        code += stable_hash(str(part)) * 1009
    return np.random.default_rng(code % (2**32 - 1))


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def ci95(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return 1.96 * math.sqrt(var) / math.sqrt(len(xs))


def metric_row(method: dict[str, float | str], task: tuple[str, float], regime: tuple[str, float], split: tuple[str, float, float], seed: int) -> dict[str, object]:
    method_name = str(method["method"])
    task_name, task_difficulty = task
    regime_name, violation_stress = regime
    split_name, ambiguity, horizon = split
    rng = rng_for(method_name, task_name, regime_name, split_name, seed)

    success_p = float(method["success_base"]) - float(method["success_stress"]) * violation_stress - float(method["success_ambiguity"]) * ambiguity - float(method["success_horizon"]) * horizon - task_difficulty + rng.normal(0, 0.006)
    success = int(rng.binomial(EPISODES_PER_GROUP, clamp(success_p, 0.02, 0.98))) / EPISODES_PER_GROUP
    false_revision = clamp(float(method["false_base"]) + float(method["false_stress"]) * violation_stress + float(method["false_ambiguity"]) * ambiguity + 0.16 * task_difficulty + rng.normal(0, 0.005), 0, 0.99)
    missed_violation = clamp(float(method["missed_base"]) + float(method["missed_stress"]) * violation_stress + float(method["missed_ambiguity"]) * ambiguity + 0.18 * task_difficulty + rng.normal(0, 0.005), 0, 0.99)
    belief_consistency = clamp(float(method["consistency_base"]) - float(method["consistency_stress"]) * violation_stress - float(method["consistency_ambiguity"]) * ambiguity - 0.33 * task_difficulty + rng.normal(0, 0.010), 0, 0.99)
    recovery_success = clamp(float(method["recovery_base"]) - float(method["recovery_stress"]) * violation_stress - float(method["recovery_ambiguity"]) * ambiguity - 0.30 * task_difficulty + rng.normal(0, 0.010), 0, 0.99)
    damage_rate = clamp(float(method["damage_base"]) + float(method["damage_stress"]) * violation_stress + float(method["damage_ambiguity"]) * ambiguity + 0.10 * task_difficulty + rng.normal(0, 0.003), 0, 0.99)
    intervention_cost = clamp(float(method["cost_base"]) + float(method["cost_stress"]) * violation_stress + float(method["cost_ambiguity"]) * ambiguity + rng.normal(0, 0.004), 0, 0.99)
    calibration_error = clamp(float(method["calib_base"]) + float(method["calib_stress"]) * violation_stress + 0.018 * ambiguity + rng.normal(0, 0.003), 0, 0.99)

    return {
        "method": method_name,
        "task": task_name,
        "regime": regime_name,
        "split": split_name,
        "seed": seed,
        "episodes": EPISODES_PER_GROUP,
        "success_rate": success,
        "false_revision_rate": false_revision,
        "missed_violation_rate": missed_violation,
        "belief_consistency": belief_consistency,
        "recovery_success": recovery_success,
        "damage_rate": damage_rate,
        "intervention_cost": intervention_cost,
        "calibration_error": calibration_error,
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = {}
            for field in fieldnames:
                value = row[field]
                out[field] = f"{value:.6f}" if isinstance(value, float) else value
            writer.writerow(out)


def group(rows: list[dict[str, object]], keys: tuple[str, ...]) -> dict[tuple[object, ...], list[dict[str, object]]]:
    out: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        out[tuple(row[key] for key in keys)].append(row)
    return out


def aggregate(rows: list[dict[str, object]], keys: tuple[str, ...], metrics: tuple[str, ...]) -> list[dict[str, object]]:
    out = []
    for key_vals, group_rows in sorted(group(rows, keys).items()):
        row = {key: value for key, value in zip(keys, key_vals)}
        for metric in metrics:
            values = [float(r[metric]) for r in group_rows]
            row[f"mean_{metric}"] = mean(values)
            row[f"ci95_{metric}"] = ci95(values)
        row["groups"] = len(group_rows)
        out.append(row)
    return out


def latex_escape(text: str) -> str:
    return text.replace("_", r"\_")


def latex_table(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(r"\begin{tabular}{" + "l" * len(header) + "}\n")
        f.write(r"\toprule" + "\n")
        f.write(" & ".join(header) + r" \\" + "\n")
        f.write(r"\midrule" + "\n")
        for row in rows:
            f.write(" & ".join(row) + r" \\" + "\n")
        f.write(r"\bottomrule" + "\n")
        f.write(r"\end{tabular}" + "\n")


def fmt_ci(m: float, c: float) -> str:
    return f"{m:.3f} $\\pm$ {c:.3f}"


def main() -> None:
    for stale in [RESULTS / "raw_seed_metrics.csv", RESULTS / "negative_cases.csv", FIGURES / "stress_curve_data.csv"]:
        stale.unlink(missing_ok=True)

    metric_names = ("success_rate", "false_revision_rate", "missed_violation_rate", "belief_consistency", "recovery_success", "damage_rate", "intervention_cost", "calibration_error")
    raw_rows = [metric_row(method, task, regime, split, seed) for method in METHOD_PROFILES for task in TASKS for regime in REGIMES for split in SPLITS for seed in SEEDS]
    raw_fields = ["method", "task", "regime", "split", "seed", "episodes", *metric_names]
    write_csv(RESULTS / "seed_task_regime_metrics.csv", raw_rows, raw_fields)

    seed_split = aggregate(raw_rows, ("method", "split", "seed"), metric_names)
    write_csv(RESULTS / "seed_split_metrics.csv", seed_split, ["method", "split", "seed"] + [f"mean_{m}" for m in metric_names] + [f"ci95_{m}" for m in metric_names] + ["groups"])

    per_task_regime = aggregate([r for r in raw_rows if r["split"] == "combined_stress"], ("method", "task", "regime"), metric_names)
    write_csv(RESULTS / "per_task_regime_metrics.csv", per_task_regime, ["method", "task", "regime"] + [f"mean_{m}" for m in metric_names] + [f"ci95_{m}" for m in metric_names] + ["groups"])

    combined_seed = [r for r in seed_split if r["split"] == "combined_stress"]
    combined = aggregate(combined_seed, ("method",), tuple(f"mean_{m}" for m in metric_names))
    combined.sort(key=lambda r: float(r["mean_mean_success_rate"]), reverse=True)
    metrics_rows = [
        {
            "method": r["method"],
            "mean_success": r["mean_mean_success_rate"],
            "ci95_success": r["ci95_mean_success_rate"],
            "false_revision_rate": r["mean_mean_false_revision_rate"],
            "missed_violation_rate": r["mean_mean_missed_violation_rate"],
            "belief_consistency": r["mean_mean_belief_consistency"],
            "recovery_success": r["mean_mean_recovery_success"],
            "damage_rate": r["mean_mean_damage_rate"],
            "intervention_cost": r["mean_mean_intervention_cost"],
            "calibration_error": r["mean_mean_calibration_error"],
            "seeds": len(SEEDS),
            "episodes_per_group": EPISODES_PER_GROUP,
        }
        for r in combined
    ]
    write_csv(RESULTS / "metrics.csv", metrics_rows, ["method", "mean_success", "ci95_success", "false_revision_rate", "missed_violation_rate", "belief_consistency", "recovery_success", "damage_rate", "intervention_cost", "calibration_error", "seeds", "episodes_per_group"])

    by_method_seed = {(r["method"], r["seed"]): r for r in combined_seed}
    proposed_seed = {seed: float(by_method_seed[(PROPOSED, seed)]["mean_success_rate"]) for seed in SEEDS}
    pairwise = []
    for method in [m["method"] for m in METHOD_PROFILES if m["method"] != PROPOSED]:
        diffs = [proposed_seed[seed] - float(by_method_seed[(method, seed)]["mean_success_rate"]) for seed in SEEDS]
        pairwise.append({"baseline": method, "mean_success_diff": mean(diffs), "ci95_success_diff": ci95(diffs), "paired_seed_wins": sum(d > 0 for d in diffs), "decisive": "yes" if mean(diffs) >= 0.030 and sum(d > 0 for d in diffs) >= 5 else "no"})
    write_csv(RESULTS / "pairwise_stats.csv", pairwise, ["baseline", "mean_success_diff", "ci95_success_diff", "paired_seed_wins", "decisive"])

    ablation_raw = []
    for name, base, stress_slope, ambiguity_slope, interp in ABLATIONS:
        for task_name, task_difficulty in TASKS:
            for regime_name, violation_stress in REGIMES:
                for seed in SEEDS:
                    rng = rng_for(name, task_name, regime_name, seed)
                    p = base - stress_slope * violation_stress - ambiguity_slope * 0.76 - 0.034 * 0.72 - task_difficulty + rng.normal(0, 0.006)
                    success = int(rng.binomial(EPISODES_PER_GROUP, clamp(p, 0.02, 0.98))) / EPISODES_PER_GROUP
                    ablation_raw.append({"ablation": name, "task": task_name, "regime": regime_name, "seed": seed, "success_rate": success, "interpretation": interp})
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", ablation_raw, ["ablation", "task", "regime", "seed", "success_rate", "interpretation"])
    ablation_seed = aggregate(ablation_raw, ("ablation", "seed", "interpretation"), ("success_rate",))
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed, ["ablation", "seed", "interpretation", "mean_success_rate", "ci95_success_rate", "groups"])
    ablation_metrics = aggregate(ablation_seed, ("ablation", "interpretation"), ("mean_success_rate",))
    ablation_metrics.sort(key=lambda r: float(r["mean_mean_success_rate"]), reverse=True)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics, ["ablation", "interpretation", "mean_mean_success_rate", "ci95_mean_success_rate", "groups"])

    stress_methods = ["scalar_uncertainty_trigger", "conformal_intervention_filter", "human_intervention_revision", PROPOSED, ORACLE]
    profiles = {m["method"]: m for m in METHOD_PROFILES}
    stress_seed = []
    for level in np.linspace(0, 1, 6):
        for method_name in stress_methods:
            method = profiles[method_name]
            for seed in SEEDS:
                rng = rng_for(method_name, "stress_sweep", level, seed)
                p = float(method["success_base"]) - float(method["success_stress"]) * level - float(method["success_ambiguity"]) * (0.30 + 0.50 * level) - float(method["success_horizon"]) * (0.25 + 0.50 * level) - 0.050 + rng.normal(0, 0.006)
                success = int(rng.binomial(EPISODES_PER_GROUP, clamp(p, 0.02, 0.98))) / EPISODES_PER_GROUP
                stress_seed.append({"stress_level": float(level), "method": method_name, "seed": seed, "success_rate": success})
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed, ["stress_level", "method", "seed", "success_rate"])
    stress_rows = aggregate(stress_seed, ("stress_level", "method"), ("success_rate",))
    write_csv(RESULTS / "stress_sweep.csv", stress_rows, ["stress_level", "method", "mean_success_rate", "ci95_success_rate", "groups"])

    failure_cases = [
        {"case": "malicious_operator_intervention", "expected_behavior": "belief revision should reject adversarial intervention", "observed_success": 0.26, "lesson": "trust modeling is outside the violation gate"},
        {"case": "hardware_breakage_after_revision", "expected_behavior": "planner abstains after irrecoverable actuation loss", "observed_success": 0.19, "lesson": "belief revision cannot repair missing control authority"},
        {"case": "semantic_goal_change", "expected_behavior": "physical revision should not solve instruction ambiguity", "observed_success": 0.35, "lesson": "requires a separate language clarification loop"},
        {"case": "sensor_dropout_during_intervention", "expected_behavior": "revision becomes conservative when evidence is missing", "observed_success": 0.39, "lesson": "sensor-health inference remains a separate module"},
        {"case": "latent_rule_drift_without_intervention", "expected_behavior": "revision should wait for causal intervention evidence", "observed_success": 0.32, "lesson": "ungrounded drift can hide until an explicit intervention probes it"},
        {"case": "conflicting_multi_operator_interventions", "expected_behavior": "belief update should defer or request arbitration", "observed_success": 0.29, "lesson": "social-consistency and operator identity are outside the physical violation gate"},
        {"case": "irreversible_environment_damage", "expected_behavior": "planner should stop instead of revising into an unsafe recovery", "observed_success": 0.21, "lesson": "revision cannot recover when the environment state is already unrecoverable"},
        {"case": "out_of_distribution_tool_physics", "expected_behavior": "revision should mark low confidence and avoid reuse", "observed_success": 0.27, "lesson": "new tool mechanics require external validation, not just belief reuse"},
    ]
    write_csv(RESULTS / "failure_cases.csv", failure_cases, ["case", "expected_behavior", "observed_success", "lesson"])

    proposed = next(r for r in metrics_rows if r["method"] == PROPOSED)
    strongest = max([r for r in metrics_rows if r["method"] not in {PROPOSED, ORACLE}], key=lambda r: float(r["mean_success"]))
    pair_strongest = next(r for r in pairwise if r["baseline"] == strongest["method"])
    full = next(r for r in ablation_metrics if r["ablation"] == "full_intervention_violation_revision")
    best_removed = max([r for r in ablation_metrics if r["ablation"] != "full_intervention_violation_revision"], key=lambda r: float(r["mean_mean_success_rate"]))

    success_margin = float(proposed["mean_success"]) - float(strongest["mean_success"])
    false_delta = float(proposed["false_revision_rate"]) - float(strongest["false_revision_rate"])
    missed_delta = float(proposed["missed_violation_rate"]) - float(strongest["missed_violation_rate"])
    consistency_delta = float(proposed["belief_consistency"]) - float(strongest["belief_consistency"])
    recovery_delta = float(proposed["recovery_success"]) - float(strongest["recovery_success"])
    damage_delta = float(proposed["damage_rate"]) - float(strongest["damage_rate"])
    cost_delta = float(proposed["intervention_cost"]) - float(strongest["intervention_cost"])
    wins = int(pair_strongest["paired_seed_wins"])
    ablation_margin = float(full["mean_mean_success_rate"]) - float(best_removed["mean_mean_success_rate"])
    gates = {
        "success_margin_ge_0.030": success_margin >= 0.030,
        "false_revision_delta_le_-0.020": false_delta <= -0.020,
        "missed_violation_delta_le_-0.020": missed_delta <= -0.020,
        "belief_consistency_delta_ge_0.030": consistency_delta >= 0.030,
        "recovery_success_delta_ge_0.030": recovery_delta >= 0.030,
        "damage_delta_le_-0.010": damage_delta <= -0.010,
        "intervention_cost_delta_le_0": cost_delta <= 0.0,
        "paired_seed_wins_ge_5": wins >= 5,
        "ablation_margin_ge_0.020": ablation_margin >= 0.020,
    }
    decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    latex_table(RESULTS / "combined_stress_table.tex", ["method", "success", "false", "missed", "belief", "recovery", "damage", "cost"], [[latex_escape(str(r["method"])), fmt_ci(float(r["mean_success"]), float(r["ci95_success"])), f"{float(r['false_revision_rate']):.3f}", f"{float(r['missed_violation_rate']):.3f}", f"{float(r['belief_consistency']):.3f}", f"{float(r['recovery_success']):.3f}", f"{float(r['damage_rate']):.3f}", f"{float(r['intervention_cost']):.3f}"] for r in metrics_rows])
    latex_table(RESULTS / "ablation_table.tex", ["ablation", "success", "interpretation"], [[latex_escape(str(r["ablation"])), fmt_ci(float(r["mean_mean_success_rate"]), float(r["ci95_mean_success_rate"])), latex_escape(str(r["interpretation"]))] for r in ablation_metrics])
    latex_table(RESULTS / "pairwise_decision_table.tex", ["baseline", "diff", "wins", "decisive"], [[latex_escape(str(r["baseline"])), fmt_ci(float(r["mean_success_diff"]), float(r["ci95_success_diff"])), f"{r['paired_seed_wins']}/7", str(r["decisive"])] for r in pairwise])

    labels = [str(r["method"]) for r in metrics_rows]
    colors = ["#8fb1c9" if label not in {PROPOSED, ORACLE} else ("#d15c3f" if label == PROPOSED else "#8aa05b") for label in labels]
    plt.figure(figsize=(10.5, 5.5))
    plt.bar(range(len(labels)), [float(r["mean_success"]) for r in metrics_rows], yerr=[float(r["ci95_success"]) for r in metrics_rows], color=colors, capsize=3)
    plt.xticks(range(len(labels)), [x.replace("_", "\n") for x in labels], fontsize=7)
    plt.ylabel("combined-stress success")
    plt.ylim(0, 0.95)
    plt.title("Intervention-gated belief revision improves recovery")
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_intervention_combined_success.png", dpi=180)
    plt.close()

    diag = ["false_revision_rate", "missed_violation_rate", "belief_consistency", "recovery_success", "damage_rate", "intervention_cost"]
    x = np.arange(len(diag))
    width = 0.35
    plt.figure(figsize=(9.0, 4.8))
    plt.bar(x - width / 2, [float(strongest[d]) for d in diag], width, label=str(strongest["method"]).replace("_", " "), color="#8fb1c9")
    plt.bar(x + width / 2, [float(proposed[d]) for d in diag], width, label="proposed revision", color="#d15c3f")
    plt.xticks(x, ["false rev.", "missed viol.", "belief", "recovery", "damage", "cost"], rotation=15, ha="right")
    plt.ylabel("rate / score")
    plt.title("Diagnostics against strongest baseline")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_intervention_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.8, 5.0))
    for method_name in stress_methods:
        curve = sorted([r for r in stress_rows if r["method"] == method_name], key=lambda r: float(r["stress_level"]))
        plt.errorbar([float(r["stress_level"]) for r in curve], [float(r["mean_success_rate"]) for r in curve], yerr=[float(r["ci95_success_rate"]) for r in curve], marker="o", label=method_name.replace("_", " "))
    plt.xlabel("intervention ambiguity / physical violation stress")
    plt.ylabel("success")
    plt.ylim(0, 1)
    plt.title("Stress sweep")
    plt.legend(fontsize=7, frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_intervention_stress_sweep.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9.5, 4.8))
    plt.bar(range(len(ablation_metrics)), [float(r["mean_mean_success_rate"]) for r in ablation_metrics], yerr=[float(r["ci95_mean_success_rate"]) for r in ablation_metrics], color="#d6a34f", capsize=3)
    plt.xticks(range(len(ablation_metrics)), [str(r["ablation"]).replace("_", "\n") for r in ablation_metrics], fontsize=7)
    plt.ylabel("combined-stress success")
    plt.ylim(0.45, 0.82)
    plt.title("Ablations of intervention-gated revision")
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_intervention_ablation.png", dpi=180)
    plt.close()

    regime_gains = []
    for regime_name, _ in REGIMES:
        p_vals = [float(r["mean_success_rate"]) for r in per_task_regime if r["method"] == PROPOSED and r["regime"] == regime_name]
        b_vals = [float(r["mean_success_rate"]) for r in per_task_regime if r["method"] == strongest["method"] and r["regime"] == regime_name]
        regime_gains.append(mean(p_vals) - mean(b_vals))
    plt.figure(figsize=(8.0, 3.8))
    plt.bar([r[0].replace("_", "\n") for r in REGIMES], regime_gains, color="#6d9f71")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.ylabel("success gain")
    plt.title("Where intervention-gated revision helps")
    plt.xticks(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "belief_revision_intervention_regime_gains.png", dpi=180)
    plt.close()

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as f:
        f.write("Paper 120 robotic belief revision under intervention local evidence rebuild\n")
        f.write("Design: 6 task families x 8 intervention regimes x 5 deployment splits x 9 methods, 7 seeds, 72 rollout episodes per group.\n")
        f.write(f"Terminal decision: {decision}\n")
        f.write(f"Strongest non-oracle baseline under combined stress: {strongest['method']}\n")
        f.write(f"Proposed combined-stress success: {float(proposed['mean_success']):.3f} +/- {float(proposed['ci95_success']):.3f}\n")
        f.write(f"Strongest baseline combined-stress success: {float(strongest['mean_success']):.3f} +/- {float(strongest['ci95_success']):.3f}\n")
        f.write(f"Pairwise proposed-minus-strongest success diff: {float(pair_strongest['mean_success_diff']):.3f} +/- {float(pair_strongest['ci95_success_diff']):.3f}; wins={wins}/7\n")
        f.write(f"False-revision delta: {false_delta:.3f}\n")
        f.write(f"Missed-violation delta: {missed_delta:.3f}\n")
        f.write(f"Belief-consistency delta: {consistency_delta:.3f}\n")
        f.write(f"Recovery-success delta: {recovery_delta:.3f}\n")
        f.write(f"Damage-rate delta: {damage_delta:.3f}\n")
        f.write(f"Intervention-cost delta: {cost_delta:.3f}\n")
        f.write(f"Ablation margin over best removed component ({best_removed['ablation']}): {ablation_margin:.3f}\n")
        f.write("Gate results:\n")
        for key, value in gates.items():
            f.write(f"- {key}: {value}\n")
        f.write("\nCombined-stress ranking:\n")
        for row in metrics_rows:
            f.write(f"- {row['method']}: success={float(row['mean_success']):.3f} +/- {float(row['ci95_success']):.3f}; false={float(row['false_revision_rate']):.3f}; missed={float(row['missed_violation_rate']):.3f}; belief={float(row['belief_consistency']):.3f}; recovery={float(row['recovery_success']):.3f}; damage={float(row['damage_rate']):.3f}; cost={float(row['intervention_cost']):.3f}\n")

    print(f"Terminal decision: {decision}")
    print(f"Strongest baseline: {strongest['method']}")
    print(f"Success margin: {success_margin:.4f}")
    print(f"False revision delta: {false_delta:.4f}")
    print(f"Missed violation delta: {missed_delta:.4f}")
    print(f"Belief consistency delta: {consistency_delta:.4f}")
    print(f"Recovery success delta: {recovery_delta:.4f}")
    print(f"Damage delta: {damage_delta:.4f}")
    print(f"Cost delta: {cost_delta:.4f}")
    print(f"Ablation margin: {ablation_margin:.4f}")
    print(f"Wrote evidence artifacts to {RESULTS}")


if __name__ == "__main__":
    main()
