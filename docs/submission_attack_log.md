# Submission Attack Log

## Attack 1: Strongest baseline selection

Mitigation: the strongest non-oracle baseline is selected after the full run from the hard aggregate. It is the prior proposed method, `proposed_intervention_violation_revision_v4_1`, so the v5 claim is measured against a hard internal baseline rather than a weak strawman.

## Attack 2: Success-only claim

Mitigation: the paper reports success, utility, false revision, missed violation, belief consistency, recovery success, damage, intervention cost, revision calibration error, unsafe revision, causal-attribution F1, paired-seed wins, ablations, stress sweeps, fixed-risk coverage, breach, gated success, and failure cases.

## Attack 3: Decorative intervention terms

Mitigation: all major components are ablated. The best removed-component variant trails the full method by `0.037416` success and `0.077831` utility.

## Attack 4: Risk gate hides weakness

Mitigation: the fixed-risk section reports both coverage and breach. At risk budget `0.15`, coverage is `1.000000` and breach is `0.000000`.

## Attack 5: Overclaiming ICLR readiness

Mitigation: all docs and the manuscript state `STRONG_REVISE`, not ICLR-main-ready. Real robot or accepted high-fidelity validation, released checkpoints/logs, independent baselines, videos, and full manual related work remain required.
