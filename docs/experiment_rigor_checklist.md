# Experiment Rigor Checklist

- [x] Paper-specific benchmark replacing the shared v3 template.
- [x] 6 task families, 8 intervention regimes, 5 deployment splits.
- [x] 9 revision methods including strong non-oracle baselines and an oracle upper bound.
- [x] 7 paired seeds with 72 rollout episodes per group.
- [x] Strongest-baseline comparison selected by combined-stress success.
- [x] Paired-seed statistics reported for all baselines.
- [x] Mechanism metrics beyond success: false revision, missed violation, belief consistency, recovery success, damage, intervention cost, calibration error.
- [x] Ablations for intervention gate, violation classifier, causal consistency, recovery memory, cost-aware querying, and uncertainty-only trigger.
- [x] Stress sweep over intervention ambiguity and hidden physical-assumption violations.
- [x] 8 failure cases documented.
- [x] Terminal gates computed in `results/summary.txt`.

Residual risk: all evidence remains local. Real robot or external high-fidelity validation is still required before an ICLR-main submission claim.
