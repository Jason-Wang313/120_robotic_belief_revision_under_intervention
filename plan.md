# Paper 120 Expanded-Standard v5 Plan

Goal: rebuild `robotic_belief_revision_under_intervention` into a 25+ page, CPU-only, RAM-light, hostile-review submission package. The output must stay honest: local evidence can justify `STRONG_REVISE`, but not ICLR-main readiness without real robot or independently accepted high-fidelity validation.

## Frozen Protocol

1. Keep the canonical numbered PDF at `C:/Users/wangz/Downloads/120.pdf` only.
2. Do not copy numbered PDFs to the Desktop, factory root, or child repo root.
3. Predefine all local result gates before interpreting final results.
4. Select the strongest non-oracle baseline automatically after the full run.
5. Retain `proposed_intervention_violation_revision` as a named prior-method baseline.
6. Report every predefined metric, including weaknesses, oracle gaps, failure cases, abstention, and scope blockers.
7. Keep CPU/RAM usage light: deterministic NumPy/CSV generation, single-process execution, no model downloads, no GPU assumptions.
8. Use real, checkable references and bright boxed clickable citation links.

## Method Upgrade

Develop v5 as `causal_intervention_belief_revision_v5`, not a renamed continuation script. The method must add:

- Physical-violation hypothesis graph over action preconditions, contact assumptions, object state, tool affordances, actuator state, and environment changes.
- Intervention evidence parser that distinguishes helpful interventions from noisy observations, false hints, malicious hints, and semantic-goal changes.
- Counterfactual consistency score: revise only when the intervention explains both the failed transition and the recovery branch better than preserving the prior belief.
- Belief-delta memory that reuses confirmed revisions while decaying unconfirmed or operator-specific revisions.
- Cost-aware query/act policy that prices interventions and avoids asking for help when physical evidence is insufficient.
- Fixed-risk acceptance screen for unsafe revision, missed physical violation, and false-revision risk.
- Conservative fallback/abstention when the violation evidence is underdetermined.
- Calibration term so predicted revision risk must match realized false/missed revision risk.

## Theory Upgrade

- Define robotic belief revision as a constrained update from prior physical belief `b_t` to revised belief `b'_t` under intervention evidence `i_t`.
- Formalize a revision score using physical-violation likelihood, counterfactual recovery value, causal consistency, memory reliability, query cost, and risk budget.
- State a safe-revision condition: update only when causal intervention evidence improves predicted recovery while keeping false-revision and missed-violation risk below the declared budget.
- State a failure condition: semantic goal change, malicious or conflicting operators, broken hardware, irreversible damage, or unobserved rule drift requires abstention or external replanning.
- Keep theory bounded to the local benchmark; do not claim universal robot belief correctness or hardware safety.

## Experiment Upgrade

Run a new v5 suite with:

- Main benchmark: task families, intervention regimes, deployment splits, methods, paired seeds, and raw episode cells.
- Baselines: no revision, periodic Bayesian update, scalar uncertainty trigger, ensemble disagreement, conformal intervention filter, human-intervention revision, failure-aware RL recovery, POMDP-style belief update, active-inference query policy, causal-discovery update, prior proposed v4.1 method, v5 proposed method, and oracle.
- Hard aggregate: false hints, sparse interventions, contact-precondition failure, actuator-model break, environment change, long-horizon recovery, malicious/conflicting operators, and combined physical-violation stress.
- Paired-seed comparisons against every non-oracle baseline.
- Ablations: remove intervention gate, physical-violation classifier, counterfactual consistency, belief-delta memory, query-cost model, fixed-risk gate, calibration, adversarial-operator guard, and recovery-value term.
- Stress sweeps: intervention ambiguity, observation noise, operator unreliability, hidden rule drift, actuator mismatch, semantic-goal conflict, and calibration shift.
- Fixed-risk deployment audit: coverage, breach, false-revision risk, missed-violation risk, gated success, gated utility, and abstention.
- Failure cases: at least 24 concrete boundary cases.

## Manuscript Upgrade

Generate a 25+ page ICLR-style PDF with:

- Abstract, contribution statement, claim/scope boundary, and hostile-review summary.
- Formal problem setup, method derivation, theory/intuition, and failure-mode analysis.
- Related work grounded in real belief revision, POMDPs, Bayesian filtering, interactive/assistive robotics, causal intervention learning, safety filters, failure recovery, and robot world-model references.
- Tables and figures generated from v5 CSV outputs only.
- Explicit statement that the evidence is local/synthetic and not final ICLR-main-ready.
- Bright boxed clickable citations that jump to the bibliography.

## Validation Gates

The rebuild only counts as complete if all required artifacts pass:

- `python -m py_compile src/run_experiment.py scripts/generate_manuscript.py scripts/validate_submission_artifacts.py`
- v5 experiment run completes under thread caps.
- CSV row-count and numeric-integrity checks pass.
- PDF compiles with LaTeX/BibTeX and has at least 25 pages.
- BibTeX has zero warnings.
- Visual QA checks representative pages.
- `C:/Users/wangz/Downloads/120.pdf` exists and no numbered copies exist elsewhere.
- Public GitHub repo is updated and the pushed commit is verified.
- Root ledgers are updated only after local validation passes.
