# 120 Robotic Belief Revision Under Intervention

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild replaces the archive scaffold with a paper-specific local benchmark for intervention-gated robotic belief revision. The v4.1 continuation audit reruns the benchmark under low-RAM caps and expands the documented failure boundary while preserving the honest strong-revise direction: the proposed method revises action-critical beliefs when interventions reveal violated physical assumptions, rather than revising on uncertainty alone. It is not yet ICLR-main ready because it lacks real robot or external high-fidelity validation.

## Evidence Snapshot

- Design: 6 task families x 8 intervention regimes x 5 deployment splits x 9 methods, 7 paired seeds, 72 rollout episodes per group.
- Strongest non-oracle baseline: `human_intervention_revision`.
- Combined-stress success: proposed `0.727 +/- 0.006` vs baseline `0.624 +/- 0.005`.
- Paired difference: `0.103 +/- 0.006`, wins `7/7` seeds.
- False-revision delta: `-0.095`; missed-violation delta: `-0.093`.
- Belief-consistency delta: `+0.202`; recovery-success delta: `+0.157`.
- Damage-rate delta: `-0.027`; intervention-cost delta: `-0.134`.
- Best ablation gap: `0.065`.
- Raw evidence coverage: `15,120` task/regime/split/method/seed rows, `2,352` ablation rows, and `210` stress-sweep seed rows.
- Failure cases: `8` documented intervention-gated belief-revision boundary cases.
- Latest rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/120_robotic_belief_revision_under_intervention_continuation_rerun_20260615.log`.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/120.pdf`

PDF SHA256: `C8DD82DE1602750D805D762719DCAE5963C783BC015A7839BC4FB4F88185FBD5`

PDF size: `330921` bytes.

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.
