# Final Audit

Submission-hardening version: v5_expanded

Decision: STRONG_REVISE

The v5 rebuild clears every predefined local gate and expands the manuscript to a 25-page ICLR-style package. The proposed `causal_intervention_belief_revision_v5` beats the strongest non-oracle baseline, `proposed_intervention_violation_revision_v4_1`, by `0.072040` hard success and `0.352219` hard utility with `10/10` paired-seed wins on both measures. It also reduces false revisions, missed violations, damage, intervention cost, calibration error, and unsafe revisions while improving belief consistency, recovery success, and causal-attribution F1.

Continuation audit additions:

- Main evidence coverage: 230,400 episode-level cells and 2,880 task/regime/split/method groups.
- Hard aggregate coverage: 120 hard-seed rows and 11 pairwise baseline comparisons.
- Ablation coverage: 38,400 cells, 100 seed rows, and 10 method summaries.
- Stress coverage: 161,280 cells, 1,680 seed rows, and 168 endpoint summaries.
- Fixed-risk coverage: 107,520 cells, 280 seed rows, 28 metric summaries, and 24 pairwise comparisons.
- Failure cases: 24 documented intervention-gated belief-revision boundaries.
- Numeric integrity: validator passed with no missing required outputs, invalid numeric values, or artifact-placement violations.
- Canonical PDF: `C:/Users/wangz/Downloads/120.pdf`.
- PDF SHA256: `6E548A1B553C9B739DCA90CCDF3CEE7F53FB18EED1BAB4A37DE41F4C4D3DDF17`.
- PDF size: `588060` bytes.
- PDF pages: `25`.
- Desktop PDF copy: absent.

The paper is not ICLR-main ready yet. Missing items remain:

- real robot validation;
- accepted high-fidelity simulator validation;
- released trained belief/world-model checkpoints;
- calibrated contact-force, camera, or state logs;
- hardware rollout videos;
- independent implementations of all major baselines;
- full manual related-work synthesis beyond the local pool.

Recommended action: preserve as a strong-revise submission candidate and do not represent it as a final main-conference paper until the scope evidence is supplied.
