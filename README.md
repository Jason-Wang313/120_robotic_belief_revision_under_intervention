# 120 Robotic Belief Revision Under Intervention

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild expands the paper into a 25-page, CPU-only, RAM-light submission package for causal intervention-gated robot belief revision. The v5 method, `causal_intervention_belief_revision_v5`, revises action-critical physical beliefs only when intervention evidence supports a physical-violation hypothesis and a fixed-risk screen accepts the update. The package is stronger and more reviewer-ready than the earlier local continuation, but it is still not ICLR-main ready because the evidence remains local and synthetic rather than real robot or independently accepted high-fidelity validation.

## Evidence Snapshot

- Design: 6 task families x 8 intervention regimes x 5 deployment splits x 12 methods x 10 paired seeds, with 230,400 main episode cells.
- Strongest non-oracle baseline: `proposed_intervention_violation_revision_v4_1`.
- Hard aggregate success: proposed `0.739175` vs strongest baseline `0.667135`; margin `0.072040`, with `10/10` paired-seed wins.
- Hard aggregate utility: proposed `0.907176` vs strongest baseline `0.554958`; margin `0.352219`, with `10/10` paired-seed wins.
- Mechanism deltas vs strongest baseline: false revision `-0.096660`, missed violation `-0.105869`, belief consistency `+0.128339`, recovery success `+0.121875`, causal-attribution F1 `+0.106198`.
- Risk/cost deltas: damage `-0.042723`, intervention cost `-0.048074`, revision calibration error `-0.014953`, unsafe revision `-0.078804`.
- Best ablation gaps: success `0.037416`, utility `0.077831`.
- Stress endpoint margins: success `0.087832`, utility `0.410389`.
- Fixed-risk audit at risk budget `0.15`: coverage `1.000000`, breach `0.000000`, gated success `0.729172`, utility margin `0.355573`.
- Evidence coverage: 230,400 main cells, 38,400 ablation cells, 161,280 stress cells, 107,520 fixed-risk cells, and 24 documented failure cases.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
python scripts\generate_manuscript.py
python scripts\validate_submission_artifacts.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/120.pdf`

PDF SHA256: `6E548A1B553C9B739DCA90CCDF3CEE7F53FB18EED1BAB4A37DE41F4C4D3DDF17`

PDF size: `588060` bytes.

PDF pages: `25`.

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.
