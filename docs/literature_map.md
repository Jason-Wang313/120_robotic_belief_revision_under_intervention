# Literature Map

## Crowded Areas

- Classical belief revision and theory change.
- POMDP filtering and planning.
- Probabilistic robotics.
- Robot learning from human correction and shared autonomy.
- Causal intervention learning.
- Safety filters and safe reinforcement learning.
- Robot failure recovery and world-model repair.

## Local Novelty Boundary

The paper should claim causal intervention-gated physical belief revision for robot recovery. It should not claim a new universal POMDP solver, a new VLA model, a human-teaching system, or real-robot safety.

The closest defensible contribution is: revise action-critical physical beliefs only when intervention evidence supports a physical-violation hypothesis, improves counterfactual recovery, and passes a fixed-risk acceptance screen.

## Evidence Needed For Final Main-Conference Readiness

- Transfer to an external benchmark or high-fidelity simulator.
- Real robot interventions with replayable logs.
- Manual related-work synthesis against accepted belief revision, POMDP, shared autonomy, causal intervention, and safety-filter baselines.
- Released belief/world-model checkpoints and independent baseline implementations.
