# Paper 120 Rebuild Plan

Started: 2026-06-15 04:23:00 +0100

## Goal

Rebuild `robotic_belief_revision_under_intervention` from an archive memo into a real local empirical submission package. The paper must test whether robot beliefs should be revised only when an intervention reveals a violated physical assumption, rather than whenever uncertainty or prediction error is high.

## Claim To Test

Robots often over-revise beliefs after noisy observations and under-revise when an intervention reveals a true violated physical assumption. An intervention-gated belief revision rule should update action-critical beliefs only when the intervention identifies a causal physical violation, improving recovery while avoiding false revisions.

## Evidence Design

- Benchmark dimensions: 6 manipulation/mobile-manipulation task families, 8 intervention/violation regimes, 5 deployment splits, 9 belief revision methods, 7 paired seeds, 72 rollout episodes per group.
- Methods: no revision, periodic Bayesian update, scalar uncertainty trigger, ensemble disagreement revision, conformal intervention filter, failure-aware RL recovery, human-intervention revision, proposed intervention-violation revision, and oracle intervention belief revision.
- Metrics: task success, false revision rate, missed-violation rate, belief-consistency score, recovery success, damage rate, intervention cost, calibration error, and paired-seed wins.
- Stress sweep: increasing intervention ambiguity and hidden physical-assumption violations.
- Ablations: remove intervention gate, remove violation classifier, remove causal consistency check, remove recovery memory, remove cost-aware querying, and uncertainty-only trigger.

## Terminal Gates

The paper may become `STRONG_REVISE` only if all gates clear against the strongest non-oracle baseline:

- Combined-stress success margin is at least 0.030.
- False revision rate decreases by at least 0.020.
- Missed-violation rate decreases by at least 0.020.
- Belief-consistency score increases by at least 0.030.
- Recovery success increases by at least 0.030.
- Damage rate decreases by at least 0.010.
- Intervention cost does not increase.
- Paired-seed success wins are at least 5/7.
- Best ablation trails the full method by at least 0.020.

If any gate fails, the terminal decision remains `KILL_ARCHIVE` with the negative result documented.
