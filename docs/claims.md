# Claims

- Mechanism claim: robot beliefs should be revised when an intervention reveals a violated physical assumption, not merely when uncertainty or prediction error is high.
- Evidence claim: the v4 benchmark tests 6 task families, 8 intervention/violation regimes, 5 deployment splits, 9 revision methods, and 7 paired seeds.
- Result claim: under combined stress, the proposed method reaches `0.727 +/- 0.006` success versus `0.624 +/- 0.005` for `human_intervention_revision`, with `0.103 +/- 0.006` paired success gain and 7/7 seed wins.
- Mechanism-diagnostic claim: the proposed method lowers false revisions by `0.095`, lowers missed violations by `0.093`, improves belief consistency by `0.202`, improves recovery success by `0.157`, lowers damage by `0.027`, and lowers intervention cost by `0.134`.
- Scope claim: the evidence supports `STRONG_REVISE`, not final ICLR-main readiness.
- Unsupported claim explicitly avoided: no claim of state-of-the-art real-robot interactive world-model performance.
