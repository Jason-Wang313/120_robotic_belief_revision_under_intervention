# ICLR Main Gate

Paper: 120 robotic_belief_revision_under_intervention

v5 gate verdict: STRONG_REVISE

Local evidence digest:

- Proposed method: `causal_intervention_belief_revision_v5`.
- Strongest non-oracle baseline: `proposed_intervention_violation_revision_v4_1`.
- Hard success: proposed `0.739175` vs strongest baseline `0.667135`; margin `0.072040`, wins `10/10`.
- Hard utility: proposed `0.907176` vs strongest baseline `0.554958`; margin `0.352219`, wins `10/10`.
- False-revision delta: `-0.096660`.
- Missed-violation delta: `-0.105869`.
- Belief-consistency delta: `+0.128339`.
- Recovery-success delta: `+0.121875`.
- Causal-attribution-F1 delta: `+0.106198`.
- Damage-rate delta: `-0.042723`.
- Intervention-cost delta: `-0.048074`.
- Revision-calibration-error delta: `-0.014953`.
- Unsafe-revision delta: `-0.078804`.
- Best ablation success gap: `0.037416`.
- Best ablation utility gap: `0.077831`.
- Stress endpoint success margin: `0.087832`.
- Fixed-risk coverage/breach/gated success: `1.000000` / `0.000000` / `0.729172`.
- Evidence coverage: 230,400 main cells, 38,400 ablation cells, 161,280 stress cells, 107,520 fixed-risk cells, and 24 failure cases.

Local gate result: pass.

Scope gate result: fail.

ICLR main ready: no. Real robot rollouts, accepted high-fidelity validation, released belief/world-model checkpoints, calibrated robot logs, videos, independent baselines, and a full manual related-work pass are still missing.
