# Paper 120 Expanded Submission Plan 2026-06-23

This plan freezes the rebuild scope for `robotic_belief_revision_under_intervention` before code execution.

## Target

- Produce a 25+ page ICLR-style STRONG_REVISE manuscript.
- Keep evidence CPU-only, deterministic, and RAM-light.
- Keep the numbered PDF in Downloads only.
- Preserve honesty: local evidence can pass local gates but cannot imply ICLR-main readiness without real robot or accepted high-fidelity validation.

## Method

The v5 method is `causal_intervention_belief_revision_v5`.

It revises action-critical robot beliefs only when intervention evidence supports a physical-violation hypothesis and the fixed-risk screen accepts the update. It must compete against the prior proposed method and other strong non-oracle baselines.

## Evidence Required

- Main evidence cells, hard aggregate, paired-seed comparisons, ablations, stress sweeps, fixed-risk deployment audit, and failure-case audit.
- Strongest non-oracle baseline selected after generation.
- All predefined gates reported, including failures.
- Scope blockers documented in the manuscript and child status files.

## Artifact Requirements

- `results/summary.json` is the source of truth.
- Generated tables live under `paper/`.
- Figures come only from v5 CSV outputs.
- Bright boxed citation links must be enabled in the PDF.
- Validator must confirm page count, hash, CSV row counts, numeric integrity, and PDF placement.

## Completion Definition

Complete means: validated Downloads-only `120.pdf`, clean LaTeX/BibTeX scan, visual PDF QA, updated child docs, committed and pushed public GitHub repo, and root ledgers updated to frontier `Papers 61-120`.
