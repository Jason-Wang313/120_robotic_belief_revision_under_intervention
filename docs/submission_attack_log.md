# Submission Attack Log

## Attack 1: Strongest baseline selection

Mitigation: the strongest non-oracle baseline is selected by combined-stress success after generation. It is `human_intervention_revision`.

## Attack 2: Query-cost confound

Mitigation: the proposed method lowers intervention cost by `0.134` relative to the strongest baseline.

## Attack 3: Over-revision

Mitigation: false revisions decrease while missed violations also decrease, showing a better precision/recall tradeoff.

## Attack 4: Decorative components

Mitigation: all major components are ablated. The best removed-component variant trails the full method by `0.065`.

## Attack 5: Overclaiming ICLR readiness

Mitigation: all docs and the manuscript state `STRONG_REVISE`, not ICLR-main-ready. Real robot or external high-fidelity validation remains required.
