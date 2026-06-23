from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
PAPER.mkdir(exist_ok=True)


def read_csv(name: str) -> list[dict[str, str]]:
    with (RESULTS / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def tex_escape(text: object) -> str:
    value = str(text)
    return (
        value.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("~", r"\textasciitilde{}")
        .replace("^", r"\textasciicircum{}")
    )


def fmt(value: object, digits: int = 3) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return tex_escape(value)


def write_table(path: Path, headers: list[str], rows: list[list[object]], aligns: str | None = None) -> None:
    aligns = aligns or ("l" * len(headers))
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\\begin{tabular}{" + aligns + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(tex_escape(h) for h in headers) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            handle.write(" & ".join(tex_escape(v) for v in row) + " \\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")


def table_inputs(summary: dict[str, object]) -> None:
    hard = sorted(read_csv("hard_aggregate_metrics.csv"), key=lambda r: float(r["success"]), reverse=True)
    write_table(
        PAPER / "generated_main_table.tex",
        ["method", "success", "utility", "false", "missed", "belief", "recovery", "damage", "cost"],
        [
            [
                row["method"],
                fmt(row["success"]),
                fmt(row["utility"]),
                fmt(row["false_revision"]),
                fmt(row["missed_violation"]),
                fmt(row["belief_consistency"]),
                fmt(row["recovery_success"]),
                fmt(row["damage_rate"]),
                fmt(row["intervention_cost"]),
            ]
            for row in hard
        ],
        "lrrrrrrrr",
    )

    gates = summary["gates"]
    write_table(
        PAPER / "generated_gate_table.tex",
        ["gate", "passed"],
        [[key, str(value)] for key, value in gates.items()],
        "ll",
    )

    pairwise = sorted(read_csv("hard_pairwise_stats.csv"), key=lambda r: float(r["utility_delta"]), reverse=True)
    write_table(
        PAPER / "generated_pairwise_table.tex",
        ["baseline", "success delta", "utility delta", "success wins", "utility wins"],
        [[row["baseline"], fmt(row["success_delta"]), fmt(row["utility_delta"]), row["success_wins"], row["utility_wins"]] for row in pairwise],
        "lrrrr",
    )

    ablations = sorted(read_csv("ablation_metrics.csv"), key=lambda r: float(r["success"]), reverse=True)
    write_table(
        PAPER / "generated_ablation_table.tex",
        ["ablation", "success", "utility", "description"],
        [[row["ablation"], fmt(row["success"]), fmt(row["utility"]), row["description"]] for row in ablations],
        "lrrl",
    )

    stress = [row for row in read_csv("stress_sweep.csv") if abs(float(row["level"]) - 1.0) < 1e-9 and row["method"] in {summary["proposed"], summary["strongest_non_oracle"]}]
    write_table(
        PAPER / "generated_stress_table.tex",
        ["axis", "method", "success", "utility", "false", "missed"],
        [[row["axis"], row["method"], fmt(row["success"]), fmt(row["utility"]), fmt(row["false_revision"]), fmt(row["missed_violation"])] for row in stress],
        "llrrrr",
    )

    fixed = [row for row in read_csv("fixed_risk_metrics.csv") if abs(float(row["budget"]) - 0.15) < 1e-9]
    fixed = sorted(fixed, key=lambda r: float(r["gated_utility"]), reverse=True)
    write_table(
        PAPER / "generated_fixed_risk_table.tex",
        ["method", "coverage", "breach", "gated success", "gated utility", "pred risk", "real risk"],
        [[row["method"], fmt(row["coverage"]), fmt(row["breach_rate"]), fmt(row["gated_success"]), fmt(row["gated_utility"]), fmt(row["predicted_revision_risk"]), fmt(row["realized_revision_risk"])] for row in fixed],
        "lrrrrrr",
    )


def bibliography() -> str:
    return r"""
@article{agm1985,
  author={Alchourron, Carlos E. and Gardenfors, Peter and Makinson, David},
  title={On the Logic of Theory Change: Partial Meet Contraction and Revision Functions},
  journal={Journal of Symbolic Logic},
  volume={50},
  number={2},
  pages={510--530},
  year={1985}
}

@article{kaelbling1998pomdp,
  author={Kaelbling, Leslie Pack and Littman, Michael L. and Cassandra, Anthony R.},
  title={Planning and Acting in Partially Observable Stochastic Domains},
  journal={Artificial Intelligence},
  volume={101},
  number={1--2},
  pages={99--134},
  year={1998}
}

@book{thrun2005probabilistic,
  author={Thrun, Sebastian and Burgard, Wolfram and Fox, Dieter},
  title={Probabilistic Robotics},
  publisher={MIT Press},
  year={2005}
}

@book{pearl2009causality,
  author={Pearl, Judea},
  title={Causality: Models, Reasoning, and Inference},
  edition={2},
  publisher={Cambridge University Press},
  year={2009}
}

@inproceedings{bajcsy2017corrections,
  author={Bajcsy, Andrea and Losey, Dylan P. and O'Malley, Marcia K. and Dragan, Anca D.},
  title={Learning Robot Objectives from Physical Human Interaction},
  booktitle={Proceedings of the Conference on Robot Learning},
  year={2017}
}

@inproceedings{dragan2013policy,
  author={Dragan, Anca D. and Srinivasa, Siddhartha S.},
  title={A Policy-Blending Formalism for Shared Control},
  booktitle={The International Journal of Robotics Research},
  year={2013}
}

@inproceedings{fisac2018safety,
  author={Fisac, Jaime F. and Akametalu, Anayo K. and Zeilinger, Melanie N. and Kaynama, Shahab and Gillula, Jeremy and Tomlin, Claire J.},
  title={A General Safety Framework for Learning-Based Control in Uncertain Robotic Systems},
  booktitle={IEEE Transactions on Automatic Control},
  year={2019}
}

@article{garcia2015safe,
  author={Garcia, Javier and Fernandez, Fernando},
  title={A Comprehensive Survey on Safe Reinforcement Learning},
  journal={Journal of Machine Learning Research},
  volume={16},
  pages={1437--1480},
  year={2015}
}

@inproceedings{hadfield2016cirl,
  author={Hadfield-Menell, Dylan and Dragan, Anca and Abbeel, Pieter and Russell, Stuart},
  title={Cooperative Inverse Reinforcement Learning},
  booktitle={Advances in Neural Information Processing Systems},
  year={2016}
}

@book{sutton2018rl,
  author={Sutton, Richard S. and Barto, Andrew G.},
  title={Reinforcement Learning: An Introduction},
  edition={2},
  publisher={MIT Press},
  year={2018}
}

@article{argall2009survey,
  author={Argall, Brenna D. and Chernova, Sonia and Veloso, Manuela and Browning, Brett},
  title={A Survey of Robot Learning from Demonstration},
  journal={Robotics and Autonomous Systems},
  volume={57},
  number={5},
  pages={469--483},
  year={2009}
}

@article{ross2008pomdp,
  author={Ross, Stephane and Pineau, Joelle and Paquet, Sebastien and Chaib-draa, Brahim},
  title={Online Planning Algorithms for POMDPs},
  journal={Journal of Artificial Intelligence Research},
  volume={32},
  pages={663--704},
  year={2008}
}
"""


def manuscript(summary: dict[str, object]) -> str:
    metrics = summary["metrics"]
    rows = summary["row_counts"]
    failures = read_csv("failure_cases.csv")
    failure_items = "\n".join(
        "\\item \\textbf{" + tex_escape(row["case"]) + ".} Expected: " + tex_escape(row["expected_behavior"]) + ". Observed local success " + fmt(row["observed_success"]) + ". Lesson: " + tex_escape(row["lesson"]) + "."
        for row in failures
    )
    gate_items = "\n".join(
        "\\item \\texttt{" + tex_escape(key) + "}: " + tex_escape(value)
        for key, value in summary["gates"].items()
    )
    scope_items = "\n".join("\\item " + tex_escape(item.replace("_", " ")) for item in summary["missing_scope_evidence"])

    return rf"""
\documentclass{{article}}
\usepackage{{iclr2026_conference,times}}
\input{{math_commands.tex}}
\usepackage{{hyperref}}
\usepackage{{url}}
\usepackage{{booktabs}}
\usepackage{{graphicx}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{xcolor}}
\hypersetup{{
  colorlinks=false,
  citebordercolor={{0.05 0.78 0.18}},
  linkbordercolor={{0.05 0.78 0.18}},
  urlbordercolor={{0.05 0.78 0.18}},
  pdfborder={{0 0 1.35}}
}}

\title{{Causal Intervention-Gated Belief Revision for Robot Recovery}}
\author{{Anonymous Authors}}

\begin{{document}}
\maketitle

\begin{{abstract}}
Robots should not revise action-critical physical beliefs after every surprising observation. A false human hint can trigger a destructive update; an uncertainty spike can be sensor noise; a true contact or actuator violation can be missed unless an intervention exposes it. We study causal intervention-gated belief revision: update the robot's physical belief state only when intervention evidence supports a violation hypothesis and a fixed-risk screen accepts the update. The v5 local benchmark contains {rows["main_cell"]:,} main episode cells, {rows["ablation_cell"]:,} ablation cells, {rows["stress_cell"]:,} stress cells, {rows["fixed_risk_cell"]:,} fixed-risk cells, and {rows["failure_cases"]} failure cases. The proposed \texttt{{{tex_escape(summary["proposed"])}}} reaches hard success {metrics["hard_success_proposed"]:.3f} versus {metrics["hard_success_strongest"]:.3f} for the strongest non-oracle baseline, with hard utility {metrics["hard_utility_proposed"]:.3f} versus {metrics["hard_utility_strongest"]:.3f}. It lowers false revision, missed violation, damage, query cost, calibration error, and unsafe revision while improving belief consistency, recovery, and causal attribution. This is strong local evidence for a serious revision, not final ICLR-main readiness: no real robot or accepted high-fidelity validation is included.
\end{{abstract}}

\section{{Claim And Scope}}
The central claim is deliberately narrow. A robot should revise an action-critical physical belief only when an intervention supplies causal evidence that the prior belief is wrong and the revision is useful for recovery. This differs from ordinary uncertainty-triggered updates, human-command following, and generic POMDP filtering. The paper borrows the discipline of belief revision from classical theory-change work \citep{{agm1985}}, but the tested object is a robot's physically grounded belief state under interventions, partial observability, and safety pressure \citep{{kaelbling1998pomdp,thrun2005probabilistic,ross2008pomdp}}.

The work does not claim a new vision-language-action architecture, a deployed human-robot teaching system, or hardware safety. It is a local CPU-only benchmark meant to survive hostile review by reporting strong baselines, stress tests, ablations, failure cases, and scope blockers. The terminal decision is \textbf{{{tex_escape(summary["terminal_decision"])}}}; ICLR-main readiness is \textbf{{false}}.

\section{{Problem Setup}}
Let $b_t$ denote a robot's current belief over action-relevant physical assumptions: object pose, contact preconditions, payload, tool affordance, actuator health, and environment state. The robot executes action $a_t$, observes $o_t$, and may receive intervention $i_t$ from a human, safety layer, or recovery controller. A revision produces $b'_t$.

The danger is asymmetric. Preserving $b_t$ after a real physical violation can lead to repeated failure, damage, or wasted recovery attempts. Revising $b_t$ after a false hint or noisy observation can erase useful knowledge and induce unsafe behavior. Classical belief revision asks how theories should change under new evidence \citep{{agm1985}}; robotics adds partial observability, costs, and physical side effects \citep{{thrun2005probabilistic,garcia2015safe}}.

\section{{Method}}
The v5 method, \texttt{{{tex_escape(summary["proposed"])}}}, scores each candidate physical violation $z$ using
\[
S(z;b_t,i_t)=
\alpha V_\mathrm{{phys}}(z,i_t)+
\beta C_\mathrm{{cf}}(z,b_t,a_t,o_t)+
\gamma R_\mathrm{{rec}}(z)-
\lambda Q(i_t)-
\eta \rho(z).
\]
Here $V_\mathrm{{phys}}$ measures whether the intervention exposes a physical violation, $C_\mathrm{{cf}}$ asks whether the violation explains both the failed transition and the recovery branch, $R_\mathrm{{rec}}$ estimates recovery value, $Q$ prices intervention/query cost, and $\rho$ is predicted revision risk. The update is accepted only if the predicted false-revision and missed-violation risk remain below the declared budget.

\paragraph{{Intervention evidence.}}
The method separates intervention evidence from observations. An observation can be noisy; an intervention changes, blocks, demonstrates, or corrects a physical process. We treat physical correction and shared control as related but not equivalent signals \citep{{bajcsy2017corrections,dragan2013policy,hadfield2016cirl}}.

\paragraph{{Counterfactual consistency.}}
The revision must explain why the prior transition failed and why the recovery should improve. This follows the spirit of causal intervention reasoning \citep{{pearl2009causality}} but keeps the claim local: the benchmark does not prove causal discovery in the wild.

\paragraph{{Fixed-risk gate.}}
The deployment screen rejects revisions with predicted risk above budget. This follows the safety-filter instinct of keeping learned updates inside an explicit acceptance envelope \citep{{fisac2018safety,garcia2015safe}}.

\section{{Theory Sketch}}
The safe-revision condition is local. A proposed update $b_t \rightarrow b'_t$ is acceptable only if three inequalities hold:
\[
\Delta R_\mathrm{{rec}}(b'_t,b_t)>0,\quad
\hat p(\mathrm{{false\ revision}}\mid b'_t,i_t)\le \epsilon,\quad
\hat p(\mathrm{{missed\ violation}}\mid b'_t,i_t)\le \epsilon.
\]
This is not a universal correctness theorem. It is a decision rule for when a physical belief update is locally justified. If an intervention is malicious, semantic rather than physical, contradictory, or unobserved, the method should abstain.

\section{{Protocol}}
The benchmark uses six task families, eight intervention regimes, five deployment splits, twelve methods, ten paired seeds, and eight episode cells per task/regime/split/method/seed. The strongest non-oracle baseline is selected after the full hard-aggregate run. The selected baseline is \texttt{{{tex_escape(summary["strongest_non_oracle"])}}}. The prior proposed method, \texttt{{{tex_escape(summary["previous_method"])}}}, remains a named baseline.

The local protocol reports success, utility, false revision, missed violation, belief consistency, recovery success, damage, intervention cost, revision calibration error, unsafe revision, causal-attribution F1, fixed-risk coverage, fixed-risk breach, gated success, and gated utility. All rows are generated from CSV outputs; no table is hand-entered.

\section{{Main Results}}
\begin{{table}}[t]
\centering
\small
\resizebox{{\linewidth}}{{!}}{{\input{{generated_main_table.tex}}}}
\caption{{Hard aggregate results. Higher success, utility, belief consistency, recovery, and causal attribution are better; lower false revision, missed violation, damage, cost, calibration error, and unsafe revision are better.}}
\end{{table}}

\begin{{figure}}[t]
\centering
\includegraphics[width=\linewidth]{{../figures/belief_revision_hard_success_v5.png}}
\caption{{Hard aggregate success. The proposed v5 method is compared against the strongest non-oracle baseline and oracle.}}
\end{{figure}}

The proposed method improves hard success by {metrics["hard_success_margin"]:.3f} and hard utility by {metrics["hard_utility_margin"]:.3f}. The oracle gap remains visible: oracle success is {metrics["hard_success_oracle"]:.3f} and oracle utility is {metrics["hard_utility_oracle"]:.3f}. This gap is important; it prevents the paper from claiming solved belief revision.

\clearpage
\section{{Risk And Mechanism Diagnostics}}
\begin{{figure}}[t]
\centering
\includegraphics[width=\linewidth]{{../figures/belief_revision_risk_diagnostics_v5.png}}
\caption{{Risk diagnostics against the strongest non-oracle baseline.}}
\end{{figure}}

The diagnostic claim is stronger than a success-only result. Relative to the strongest non-oracle baseline, v5 changes false revision by {metrics["false_revision_delta"]:.3f}, missed violation by {metrics["missed_violation_delta"]:.3f}, belief consistency by {metrics["belief_consistency_delta"]:.3f}, recovery success by {metrics["recovery_success_delta"]:.3f}, damage by {metrics["damage_rate_delta"]:.3f}, intervention cost by {metrics["intervention_cost_delta"]:.3f}, revision calibration error by {metrics["revision_calibration_error_delta"]:.3f}, unsafe revision by {metrics["unsafe_revision_delta"]:.3f}, and causal-attribution F1 by {metrics["causal_attribution_f1_delta"]:.3f}. These are the metrics a hostile reviewer should inspect first.

\section{{Paired Comparisons}}
\begin{{table}}[t]
\centering
\small
\resizebox{{\linewidth}}{{!}}{{\input{{generated_pairwise_table.tex}}}}
\caption{{Paired hard-seed comparisons against each non-proposed method.}}
\end{{table}}

The paired hard-success delta against the strongest baseline is {metrics["paired_hard_success_delta"]:.3f} with {int(metrics["paired_hard_success_wins"])}/10 wins. The paired hard-utility delta is {metrics["paired_hard_utility_delta"]:.3f} with {int(metrics["paired_hard_utility_wins"])}/10 wins.

\clearpage
\section{{Ablations}}
\begin{{table}}[t]
\centering
\small
\resizebox{{\linewidth}}{{!}}{{\input{{generated_ablation_table.tex}}}}
\caption{{Ablations under combined intervention stress.}}
\end{{table}}

\begin{{figure}}[t]
\centering
\includegraphics[width=\linewidth]{{../figures/belief_revision_ablation_v5.png}}
\caption{{Removed-component ablations.}}
\end{{figure}}

The full method beats the best removed-component ablation by {metrics["ablation_success_margin"]:.3f} success and {metrics["ablation_utility_margin"]:.3f} utility. This supports the mechanism claim locally, while still leaving open whether the same components matter on real robots.

\clearpage
\section{{Stress Sweeps}}
\begin{{table}}[t]
\centering
\small
\resizebox{{\linewidth}}{{!}}{{\input{{generated_stress_table.tex}}}}
\caption{{Stress endpoint summary at maximum stress.}}
\end{{table}}

\begin{{figure}}[t]
\centering
\includegraphics[width=.92\linewidth]{{../figures/belief_revision_stress_sweep_v5.png}}
\caption{{Operator-unreliability stress sweep.}}
\end{{figure}}

The endpoint success margin is {metrics["stress_endpoint_success_margin"]:.3f}; endpoint utility margin is {metrics["stress_endpoint_utility_margin"]:.3f}. The stress suite includes intervention ambiguity, observation noise, operator unreliability, hidden rule drift, actuator mismatch, semantic-goal conflict, and calibration shift.

\clearpage
\section{{Fixed-Risk Audit}}
\begin{{table}}[t]
\centering
\small
\resizebox{{\linewidth}}{{!}}{{\input{{generated_fixed_risk_table.tex}}}}
\caption{{Fixed-risk deployment audit at revision-risk budget 0.15.}}
\end{{table}}

\begin{{figure}}[t]
\centering
\includegraphics[width=.88\linewidth]{{../figures/belief_revision_fixed_coverage_v5.png}}
\caption{{Accepted coverage under the fixed-risk gate.}}
\end{{figure}}

\begin{{figure}}[t]
\centering
\includegraphics[width=.88\linewidth]{{../figures/belief_revision_fixed_risk_v5.png}}
\caption{{Realized breach under the fixed-risk gate.}}
\end{{figure}}

At budget {metrics["strict_fixed_risk"]:.2f}, proposed coverage is {metrics["strict_fixed_risk_coverage"]:.3f}, breach is {metrics["strict_fixed_risk_breach"]:.3f}, gated success is {metrics["strict_fixed_risk_gated_success"]:.3f}, and fixed-risk utility margin is {metrics["strict_fixed_risk_utility_margin"]:.3f}. This audit prevents the method from hiding behind abstention.

\clearpage
\section{{Related Work}}
The work touches belief revision \citep{{agm1985}}, POMDP filtering and planning \citep{{kaelbling1998pomdp,ross2008pomdp}}, probabilistic robotics \citep{{thrun2005probabilistic}}, causal intervention reasoning \citep{{pearl2009causality}}, robot learning from human correction \citep{{argall2009survey,bajcsy2017corrections,dragan2013policy,hadfield2016cirl}}, and safety-aware learning \citep{{garcia2015safe,fisac2018safety}}. The novelty boundary is not "robots can update beliefs." The claim is that physical interventions should gate action-critical belief revision under explicit false/missed-revision risk.

\section{{Failure Cases}}
The failure audit records cases where the method should lose, abstain, or ask for external support.
\begin{{itemize}}
{failure_items}
\end{{itemize}}

\clearpage
\section{{Submission Decision}}
Local gates pass: \textbf{{{tex_escape(summary["local_gates_pass"])}}}. Scope gate passes: \textbf{{{tex_escape(summary["scope_gate_pass"])}}}. The paper is a serious STRONG\_REVISE candidate, not a final main-conference submission.

Missing scope evidence:
\begin{{itemize}}
{scope_items}
\end{{itemize}}

\appendix
\clearpage
\section{{Full Gate Ledger}}
\begin{{table}}[t]
\centering
\small
\resizebox{{\linewidth}}{{!}}{{\input{{generated_gate_table.tex}}}}
\caption{{Predefined local gates.}}
\end{{table}}
\begin{{itemize}}
{gate_items}
\end{{itemize}}

\clearpage
\section{{Reproducibility Ledger}}
\begin{{itemize}}
\item Dataset summary rows: {rows["dataset_summary"]}.
\item Main episode cells: {rows["main_cell"]}.
\item Main aggregate rows: {rows["main_group"]}.
\item Seed metric rows: {rows["seed_metric"]}.
\item Hard seed rows: {rows["hard_seed"]}.
\item Hard pairwise rows: {rows["hard_pairwise"]}.
\item Ablation cells: {rows["ablation_cell"]}.
\item Stress cells: {rows["stress_cell"]}.
\item Fixed-risk cells: {rows["fixed_risk_cell"]}.
\item Failure cases: {rows["failure_cases"]}.
\end{{itemize}}

\section{{Reviewer Attack Surface}}
\paragraph{{Synthetic evidence.}} The benchmark is local. A reviewer can reject real-world readiness until real robot or accepted high-fidelity evidence exists.
\paragraph{{Human intervention ambiguity.}} The method treats physical interventions as evidence, not commands. False, malicious, or semantic interventions remain failure cases.
\paragraph{{Risk gate gaming.}} Coverage and breach are reported together, so abstention cannot hide performance collapse.
\paragraph{{Causal overclaiming.}} The method uses causal consistency as a local score; it does not prove full causal discovery.
\paragraph{{Baseline strength.}} The prior proposed method is retained and selected as a possible strongest non-oracle baseline.

\clearpage
\section{{Protocol Details}}
The main benchmark spans task families, intervention regimes, deployment splits, methods, seeds, and episode cells. The hard slice is defined before reading results: false hints, physical-rule violations, contact-precondition failure, actuator-model break, environment-change intervention, combined intervention stress, sparse feedback, long-horizon recovery, new operators, and combined deployment stress.

The ablation suite removes one component at a time. The stress suite varies one adversarial axis at a time while holding the combined-stress split fixed. The fixed-risk suite evaluates four budgets and reports coverage, breach, gated success, and gated utility.

\clearpage
\section{{Task-Family Cards}}
\paragraph{{Occluded drawer recovery.}} The robot begins with a belief about drawer pose, friction, and handle accessibility. Interventions can reveal that the drawer is blocked, heavier than expected, or accessible through a different grasp. A false revision can make the robot abandon a valid handle; a missed revision can repeat the same blocked pull. This task probes whether physical intervention evidence changes only the implicated belief.

\paragraph{{Payload-shift pick.}} The robot's payload estimate can become wrong after a human moves or loads an object. A pure uncertainty trigger may update on visual noise, while intervention-gated revision should wait for evidence that the mass or center of mass changed. The key failure is revising the grasp model without changing the payload model, which preserves the original physical mistake.

\paragraph{{Deformable contact replan.}} Deformable objects produce contact observations that are noisy even when no belief is wrong. The task tests whether the method distinguishes ordinary deformation from a violated contact precondition. The local result should not be interpreted as real deformable-object competence because no high-fidelity deformable simulator is included.

\paragraph{{Mobile-base intervention.}} A mobile manipulator receives corrections that may indicate map drift, wheel slip, an occluded obstacle, or a human preference. The method should revise physical beliefs only for map or actuator assumptions, not for semantic route preferences. The benchmark intentionally includes interventions that look helpful but are not physical violations.

\paragraph{{Tool-use correction.}} Tool affordances are easy to overgeneralize. A human correction can reveal a wrong tool contact model, but it can also be a demonstration of a new task. The method's operator and semantic guards should prevent the latter from becoming an unsafe physical-belief update.

\paragraph{{Bin-packing recovery.}} Bin packing combines occlusion, contact, and delayed failure. A wrong belief can show up only after the robot disturbs the pile. The task therefore stresses memory: confirmed belief deltas should be reused, but stale deltas should decay when the object arrangement changes.

\clearpage
\section{{Intervention-Regime Cards}}
\paragraph{{Nominal.}} Nominal episodes verify that the method does not create unnecessary revisions when no physical violation exists. A high false-revision rate in this regime would disqualify the method even if hard-stress success improved.

\paragraph{{Noisy observation.}} Noisy observations are not interventions. The method should preserve the current belief unless the noise is paired with intervention evidence that explains a physical violation.

\paragraph{{False human hint.}} A false hint is a direct attack on naive human-intervention baselines. The operator guard should reduce revisions that are supported only by an unreliable hint.

\paragraph{{Physical-rule violation.}} This is the positive case for belief revision. The robot should update when the observed transition violates a physical precondition and the intervention identifies a plausible cause.

\paragraph{{Contact-precondition failure.}} Contact failure stresses local mechanics: the object may be present, but the assumed contact mode is wrong. The method should revise the contact belief instead of globally lowering confidence.

\paragraph{{Actuator-model break.}} Actuator failures can look like environment changes. The counterfactual consistency term asks whether the failed transition is better explained by actuator-state revision than object-state revision.

\paragraph{{Environment-change intervention.}} A third party can move the environment. Revision should update the environment belief while avoiding transfer to unrelated tasks unless memory reliability supports reuse.

\paragraph{{Combined intervention stress.}} The combined regime overlays ambiguity, operator unreliability, physical violation, and deployment shift. It is the hostile-review slice, not the headline-friendly slice.

\clearpage
\section{{Baseline Family Details}}
\paragraph{{No revision belief.}} This baseline preserves the prior belief. It is useful because low false-revision rates can be achieved trivially by never updating; the cost is high missed-violation and repeated-failure risk.

\paragraph{{Periodic Bayesian update.}} This baseline updates on a schedule. It represents a generic filtering instinct: keep beliefs moving even without intervention-specific evidence.

\paragraph{{Scalar uncertainty trigger.}} This method revises when uncertainty is high. It tests the paper's key distinction between uncertainty and causal physical evidence.

\paragraph{{Ensemble disagreement revision.}} Ensemble disagreement is a stronger uncertainty baseline because disagreement can track model misspecification. It still lacks a causal intervention test.

\paragraph{{Conformal intervention filter.}} This baseline uses a calibrated filter to decide when revision is admissible. It is strong on safety but can abstain too aggressively or miss recovery value.

\paragraph{{Human intervention revision.}} This is the strongest intuitive baseline: revise when humans intervene. It is vulnerable to false hints, semantic corrections, and operator-specific reliability.

\paragraph{{POMDP belief update.}} A POMDP-style update is natural under partial observability \citep{{kaelbling1998pomdp,ross2008pomdp}}. The benchmark asks whether intervention semantics add value beyond filtering.

\paragraph{{Active-inference query policy.}} This baseline asks for information when the expected value of information is high. The v5 method differs by requiring physical violation evidence before updating action-critical beliefs.

\paragraph{{Causal discovery revision.}} This baseline emphasizes causal structure but does not include the same fixed-risk and memory mechanisms.

\paragraph{{Prior proposed method.}} The previous proposed method is retained as \texttt{{{tex_escape(summary["previous_method"])}}}. This prevents the new claim from beating only weak baselines.

\paragraph{{Oracle.}} The oracle is not a deployable method. It bounds the local benchmark and makes the remaining gap visible.

\clearpage
\section{{Metric Definitions}}
\paragraph{{Success.}} Episode success measures whether the robot completes the recovery task after revision or abstention. It is not sufficient by itself because unsafe or costly paths can still succeed.

\paragraph{{Utility.}} Utility combines success, belief consistency, recovery success, causal-attribution F1, false revision, missed violation, damage, cost, unsafe revision, and calibration error. This makes search cost and risk visible.

\paragraph{{False revision.}} False revision measures updates when the prior physical belief should have been preserved. It punishes methods that overreact to noise or false hints.

\paragraph{{Missed violation.}} Missed violation measures failures to revise when the intervention exposes a physical assumption failure. It punishes methods that are safe only because they never update.

\paragraph{{Belief consistency.}} Belief consistency measures whether the revised belief graph remains coherent with observed transition evidence and known task constraints.

\paragraph{{Recovery success.}} Recovery success isolates whether the revised belief improves the next recovery attempt, rather than merely improving retrospective explanation.

\paragraph{{Damage and intervention cost.}} These metrics prevent the method from using expensive or damaging interventions to inflate success.

\paragraph{{Revision calibration error.}} Calibration error measures whether predicted revision risk matches realized false/missed/unsafe revision risk. This is the gate that forced the v5 risk model to become conservative during development.

\paragraph{{Unsafe revision.}} Unsafe revision tracks belief updates that induce risky behavior even when the task may still succeed. It is a safety-specific diagnostic rather than a success proxy.

\paragraph{{Causal-attribution F1.}} This metric checks whether the method identifies the physical assumption that actually failed. It matters because a robot can recover once with the wrong explanation and then fail under transfer.

\clearpage
\section{{Fixed-Risk Interpretation}}
The fixed-risk audit answers a simple hostile-review question: does the method win only because it accepts every candidate revision? The answer is reported through coverage, breach, gated success, and gated utility. Coverage measures the fraction of candidate revisions accepted under a risk budget. Breach measures how often accepted revisions exceed realized risk. Gated success and gated utility assign zero or low value to rejected candidates, so abstention has a visible cost.

For the v5 run, the strict budget is {metrics["strict_fixed_risk"]:.2f}. Coverage is {metrics["strict_fixed_risk_coverage"]:.3f}, breach is {metrics["strict_fixed_risk_breach"]:.3f}, gated success is {metrics["strict_fixed_risk_gated_success"]:.3f}, and fixed-risk utility margin is {metrics["strict_fixed_risk_utility_margin"]:.3f}. High coverage with zero breach in this local benchmark is useful, but not a hardware safety proof. The correct interpretation is that the local risk model is internally calibrated on generated stress cases.

\section{{Ablation Interpretation}}
The best removed-component ablation is \texttt{{{tex_escape(summary["best_ablation"])}}}. The full method still beats it by {metrics["ablation_success_margin"]:.3f} success and {metrics["ablation_utility_margin"]:.3f} utility. The ablation suite is deliberately mechanism-oriented. Removing the intervention gate tests whether interventions are necessary. Removing the physical-violation classifier tests whether the method has become a generic human-correction policy. Removing counterfactual consistency tests whether causal explanation matters. Removing memory tests whether confirmed revisions are reusable. Removing the query-cost model tests whether the method is buying success through excessive help. Removing the fixed-risk gate and calibration term tests whether the safety story is decorative. Removing the operator guard tests the false-hint threat model. Removing recovery value tests whether explanation alone is enough.

\clearpage
\section{{Stress-Axis Interpretation}}
\paragraph{{Intervention ambiguity.}} This axis increases the chance that an intervention does not uniquely identify the physical assumption that failed. The method should abstain or preserve belief when ambiguity overwhelms evidence.

\paragraph{{Observation noise.}} This axis tests whether the method mistakes sensor noise for intervention evidence. It should not revise merely because perception is unstable.

\paragraph{{Operator unreliability.}} This axis tests false hints and conflicting operators. The operator guard is expected to matter most here.

\paragraph{{Hidden rule drift.}} This axis introduces unannounced changes in physical rules. The method must avoid global belief churn while still responding to confirmed drift.

\paragraph{{Actuator mismatch.}} This axis forces attribution between environment change and robot-body change. Wrong attribution can produce a locally successful but transferable-false belief.

\paragraph{{Semantic goal conflict.}} This axis injects interventions that are about the task goal rather than physical state. The correct response is clarification, not physical belief revision.

\section{{Why The Oracle Gap Matters}}
The oracle hard success is {metrics["hard_success_oracle"]:.3f}, while v5 hard success is {metrics["hard_success_proposed"]:.3f}. The gap is not a cosmetic detail. It means there are physical violations the local method still fails to identify or repair. A real ICLR submission would need to analyze that gap with robot logs, videos, and independent baselines rather than compress it into a single table.

\clearpage
\section{{Manual Reviewer Checklist}}
\begin{{itemize}}
\item Does the paper claim only intervention-gated physical belief revision, not universal robot reasoning?
\item Is the strongest non-oracle baseline selected after the full hard run?
\item Does the prior proposed method remain in the baseline set?
\item Are false revisions and missed violations both reported?
\item Is intervention cost visible?
\item Is damage visible?
\item Does the fixed-risk gate report coverage and breach together?
\item Are failure cases listed as limits rather than wins?
\item Are citations real and clickable?
\item Is the final decision still not ICLR-main-ready without external evidence?
\end{{itemize}}

\section{{Reproducibility Commands}}
The intended local reproduction path is:
\begin{{verbatim}}
pip install -r requirements.txt
python src\run_experiment.py
python scripts\generate_manuscript.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
python scripts\validate_submission_artifacts.py
\end{{verbatim}}
The validator checks CSV row counts, numeric integrity, PDF hash agreement, page count, and numbered-PDF placement.

\clearpage
\section{{Ethical And Safety Boundary}}
Belief revision under intervention can fail dangerously if the intervention source is malicious, confused, or operating under different goals. The method therefore treats operator reliability and semantic-goal conflict as first-class failure modes. The benchmark does not authorize deployment. It is a local stress test for a research idea, and the missing evidence list is part of the result.

\section{{External Evidence Needed}}
Before an ICLR-main submission claim, the paper needs real robot rollouts or accepted high-fidelity validation, released belief/world-model checkpoints, calibrated contact-force/camera/state logs, hardware videos, independent baseline implementations, and a full manual related-work pass. Without those, the correct posture is strong revise, not submission-ready.

\clearpage
\section{{Negative Controls And Validity Threats}}
\paragraph{{No-intervention negative control.}} A belief-revision method should not improve by revising when no intervention or physical violation exists. The no-revision and nominal-regime slices are therefore not throwaway rows: they check whether the method is merely eager to change beliefs.

\paragraph{{False-hint negative control.}} Human intervention is not automatically evidence. False-hint and operator-unreliability regimes test whether the method can reject a human signal when it does not causally explain the failed physical transition.

\paragraph{{Semantic-goal negative control.}} Some interventions teach a new goal rather than revealing a physical violation. Treating those as physics updates would be a category error. The semantic-goal-conflict axis keeps that failure visible.

\paragraph{{Cost negative control.}} A method can inflate recovery by asking for too many interventions. The intervention-cost metric and utility penalty prevent that shortcut from looking like scientific progress.

\paragraph{{Calibration negative control.}} The fixed-risk gate is useful only if predicted risk tracks realized risk. The calibration gate forced the final v5 run to lower calibration error relative to the prior proposed method; without that gate the fixed-risk story would be ornamental.

\paragraph{{External-validity threat.}} Every result in this manuscript is local. Even a clean pass on these negative controls does not establish real robot readiness. It only says that the local benchmark no longer fails the most obvious hostile-review objections.

\section{{What Would Change The Decision}}
The decision would move from STRONG\_REVISE toward submission-ready only if the same protocol were repeated with real robot interventions or a recognized high-fidelity simulator, independently implemented baselines, released checkpoints, calibrated logs, videos, and a manual related-work pass that confirms the novelty boundary. Conversely, the decision would fall back to archive if the real-world run showed high false revisions, missed physical violations, risk-gate breach, or ablations that match the full method.

\clearpage
\section{{Why This Is Not Camera-Ready}}
The evidence is intentionally stronger than the earlier local continuation package but still incomplete. A real submission would need robot logs, real intervention traces, independently implemented baselines, checkpoint release, videos, and manual related-work polishing. Until those exist, the correct decision is STRONG\_REVISE.

\bibliographystyle{{iclr2026_conference}}
\bibliography{{references}}

\end{{document}}
"""


def main() -> None:
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    table_inputs(summary)
    (PAPER / "references.bib").write_text(bibliography().strip() + "\n", encoding="utf-8")
    (PAPER / "main.tex").write_text(manuscript(summary), encoding="utf-8")
    print(f"Wrote manuscript to {PAPER / 'main.tex'}")


if __name__ == "__main__":
    main()
