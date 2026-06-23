# Experiment Rigor Checklist

- [x] Paper-specific benchmark replacing the shared archive template.
- [x] 6 task families, 8 intervention regimes, 5 deployment splits.
- [x] 12 methods including strong non-oracle baselines, the prior proposed method, and an oracle upper bound.
- [x] 10 paired seeds with raw episode-level cell outputs.
- [x] Strongest-baseline comparison selected by hard aggregate success after the full run.
- [x] Paired-seed statistics reported for all baselines.
- [x] Mechanism metrics beyond success: utility, false revision, missed violation, belief consistency, recovery success, damage, intervention cost, calibration error, unsafe revision, and causal-attribution F1.
- [x] Ablations for intervention gate, physical-violation classifier, counterfactual consistency, belief-delta memory, query-cost model, fixed-risk gate, calibration, operator guard, and recovery value.
- [x] Stress sweep over intervention ambiguity, observation noise, operator unreliability, hidden rule drift, actuator mismatch, and semantic goal conflict.
- [x] Fixed-risk deployment audit reports coverage, breach, gated success, gated utility, and pairwise comparisons.
- [x] 24 failure cases documented.
- [x] Terminal gates computed in `results/summary.json` and `results/summary.txt`.
- [x] 25-page PDF, BibTeX warning count zero, log warning scan clean, visual QA complete.

Residual risk: all evidence remains local. Real robot or external high-fidelity validation is still required before an ICLR-main submission claim.
