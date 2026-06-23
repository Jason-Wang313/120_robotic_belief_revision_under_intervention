# Claims

- Mechanism claim: robots should revise action-critical physical beliefs only when intervention evidence supports a physical-violation hypothesis and a fixed-risk screen accepts the update.
- Evidence claim: the v5 benchmark tests 6 task families, 8 intervention regimes, 5 deployment splits, 12 methods, 10 paired seeds, 230,400 main episode cells, 38,400 ablation cells, 161,280 stress cells, and 107,520 fixed-risk cells.
- Result claim: on hard aggregate settings, `causal_intervention_belief_revision_v5` reaches `0.739175` success versus `0.667135` for `proposed_intervention_violation_revision_v4_1`, with `0.072040` paired success margin and `10/10` paired-seed wins.
- Utility claim: on the same hard aggregate, v5 reaches `0.907176` utility versus `0.554958` for the strongest non-oracle baseline, with `0.352219` paired utility margin and `10/10` paired-seed wins.
- Mechanism-diagnostic claim: v5 lowers false revision by `0.096660`, missed violation by `0.105869`, damage by `0.042723`, intervention cost by `0.048074`, revision calibration error by `0.014953`, and unsafe revision by `0.078804`; it improves belief consistency by `0.128339`, recovery success by `0.121875`, and causal-attribution F1 by `0.106198`.
- Fixed-risk claim: with a strict revision-risk budget of `0.15`, v5 covers `1.000000` of candidate revisions, breaches the budget at `0.000000`, and achieves gated success `0.729172`.
- Scope claim: the evidence supports `STRONG_REVISE`, not final ICLR-main readiness.
- Unsupported claim explicitly avoided: no claim of deployed robot belief revision, hardware safety, universal causal discovery, or state-of-the-art interactive robotics.
