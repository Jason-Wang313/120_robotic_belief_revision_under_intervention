# Submission Readiness Audit v5

Date: 2026-06-23

Paper: 120 robotic_belief_revision_under_intervention

Method: `causal_intervention_belief_revision_v5`

Decision: STRONG_REVISE

ICLR-main ready: no

## Passed Local Gates

- Hard success margin over strongest non-oracle baseline: `0.072040`.
- Hard utility margin over strongest non-oracle baseline: `0.352219`.
- Paired hard success wins: `10/10`.
- Paired hard utility wins: `10/10`.
- False-revision delta: `-0.096660`.
- Missed-violation delta: `-0.105869`.
- Belief-consistency delta: `+0.128339`.
- Recovery-success delta: `+0.121875`.
- Causal-attribution-F1 delta: `+0.106198`.
- Damage-rate delta: `-0.042723`.
- Intervention-cost delta: `-0.048074`.
- Revision-calibration-error delta: `-0.014953`.
- Unsafe-revision delta: `-0.078804`.
- Best ablation success/utility gaps: `0.037416` / `0.077831`.
- Stress endpoint success/utility margins: `0.087832` / `0.410389`.
- Fixed-risk coverage/breach/gated success: `1.000000` / `0.000000` / `0.729172`.

## Artifact Checks

- PDF: `C:/Users/wangz/Downloads/120.pdf`.
- PDF SHA256: `6E548A1B553C9B739DCA90CCDF3CEE7F53FB18EED1BAB4A37DE41F4C4D3DDF17`.
- PDF size: `588060` bytes.
- PDF pages: `25`.
- Numbered PDF placement: Downloads only.
- Desktop numbered PDF: absent.
- Validator: passed.
- Visual QA: pages 1, 4, 8, 14, 21, and 25 inspected.

## Scope Blockers

- No real robot rollouts.
- No accepted high-fidelity belief-revision simulation.
- No released belief or world-model checkpoints.
- No calibrated contact-force, camera, or state logs.
- No hardware rollout videos.
- No independent baseline implementations.
- Manual related-work pass is not yet full-paper complete.

Conclusion: the package is a strong local submission candidate, but hostile review would still be justified in rejecting an ICLR-main claim on external-evidence grounds.
