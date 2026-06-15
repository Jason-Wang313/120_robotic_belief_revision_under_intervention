# Hostile Reviewer Response

## Attack: This is just human intervention or querying.

Response: The strongest non-oracle baseline is `human_intervention_revision`. The proposed method beats it by `0.103 +/- 0.006` success and lowers intervention cost by `0.134`.

## Attack: The method may overfit by revising too often.

Response: False revisions decrease by `0.095`, while missed violations decrease by `0.093`, so the local result is not explained by indiscriminate revision.

## Attack: The violation gate may be decorative.

Response: Removing cost-aware querying, causal consistency, recovery memory, intervention gating, violation classification, or replacing the method with an uncertainty-only trigger reduces combined-stress success. The best removed-component variant trails by `0.065`.

## Attack: The benchmark is still not enough for ICLR main.

Response: Agreed. The terminal decision is `STRONG_REVISE`, not final acceptance readiness. The work still needs real robot or external high-fidelity validation.
