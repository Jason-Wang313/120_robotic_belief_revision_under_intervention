# ICLR Main Gate

Paper: 120 robotic_belief_revision_under_intervention

Previous v3 decision: KILL_ARCHIVE

V4.1 gate verdict: STRONG_REVISE

Evidence digest:

- Proposed success: `0.727 +/- 0.006`.
- Strongest non-oracle baseline: `human_intervention_revision` at `0.624 +/- 0.005`.
- Paired difference: `0.103 +/- 0.006`, wins `7/7`.
- False-revision delta: `-0.095`.
- Missed-violation delta: `-0.093`.
- Belief-consistency delta: `+0.202`.
- Recovery-success delta: `+0.157`.
- Damage-rate delta: `-0.027`.
- Intervention-cost delta: `-0.134`.
- Best ablation gap: `0.065`.
- Raw evidence coverage: `15,120` task/regime/split/method/seed rows.
- Ablation coverage: `2,352` task/regime/seed rows.
- Stress-sweep coverage: `210` method/stress/seed rows.
- Failure cases: `8` documented intervention-gated belief-revision boundaries.

Gate result: all local gates pass.

ICLR main ready: no. External validation and real robot or accepted high-fidelity simulator evidence are still missing.
