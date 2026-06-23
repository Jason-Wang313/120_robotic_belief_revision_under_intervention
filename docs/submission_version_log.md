# Submission Version Log

## Superseded Local Builds

- Earlier archive and local-continuation builds were superseded by the v5 expansion.
- Their useful role is now historical only: they established the paper topic, rough mechanism, and prior proposed baseline.
- Their old page counts, hashes, row counts, and baseline statistics should not be used for the current paper state.

## v5_expanded

- Rebuilt the method as `causal_intervention_belief_revision_v5`.
- Added physical-violation hypothesis graphs, intervention evidence parsing, counterfactual consistency, belief-delta memory, cost-aware querying, fixed-risk acceptance, and calibration.
- Expanded to 12 methods, 10 paired seeds, 230,400 main cells, 38,400 ablation cells, 161,280 stress cells, 107,520 fixed-risk cells, and 24 failure cases.
- Selected the strongest non-oracle baseline from the hard aggregate; it is `proposed_intervention_violation_revision_v4_1`.
- Reported hard success, hard utility, mechanism diagnostics, ablations, stress endpoints, fixed-risk coverage/breach/gated success, and scope blockers.
- Generated a 25-page ICLR-style PDF with bright boxed clickable citations.
- Terminal decision remains STRONG_REVISE.
- ICLR main readiness remains no pending real robot or accepted high-fidelity validation, released checkpoints/logs, hardware videos, independent baselines, and full manual related work.
