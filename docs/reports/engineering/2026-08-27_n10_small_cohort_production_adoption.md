# N10 small-cohort production adoption

Mission ID: `V7_N10_SMALL_COHORT_PRODUCTION_ADOPTION`  
Run nonce: `v53_n10_small_cohort_20260827`

## Starting evidence

- Canonical truth check was `FINAL PASS; FULLY_ALIGNED` at entry; CPS frontier was `N10_SMALL_COHORT_AUTHORITY_CONTRACT`.
- The Runtime health owner was active; the old standalone full-Matrix timer was intentionally disabled.
- A read-only normal Planner invocation scanned 126 identities and constructed 125 decisions before an intelligence-snapshot STOP_SAFE.  That is valid diagnostic evidence but is explicitly not an acceptable small-cohort recovery hot path.
- The existing Matrix-owned prepared projection already contained seven semantic classes.  One current class had exactly three members on one source; its target remained an existing Planner proposal, never an operator selection.

## Change in this block

Extended existing owners only:

1. `AutoswitchPlanner`'s Matrix-owned prepared-class projection now carries a deterministic maximum-four-member slice and its fingerprint.  It still does not persist complete raw member lists, create a new state store, select a server manually, or grant execution.
2. The established current-action Authority contract now accepts a distinct `N10_SMALL_COHORT` action class: exactly 2–4 named identities, one source, one concurrent transaction, a target deliberately unbound until fresh Planner consumption, and exact membership/source generations.
3. The existing planner derives the cohort scope from that issued contract rather than a CLI source/user argument.  It therefore limits decision construction to the contract members and retains the normal fresh candidate, Packet, Lease, Barrier, verifier, rollback, and sole `v7-user-switch` path.
4. Consumption checks the complete sorted membership set, source and current generation.  Any member drift, source drift, missing/ambiguous prepared class, target divergence, capacity/service failure, or first apply failure stays STOP_SAFE and prevents remaining forward actions.

No route, user assignment, Matrix cadence, timer, target eligibility policy, Planner owner, state source, or route writer was changed in this block.

## Verification before publication

- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_operator_execution_packet`: **316 passed**.
- Added tests prove that a cohort request is generated only from one prepared class without a manually passed user/source/target, and that Authority issuance/consumption rejects any membership mismatch while allowing exactly the issued group and one fresh target.
- `py_compile` and `git diff --check`: passed.

## Exact next action

Run the existing safe-deploy gate, publish/deploy this bounded implementation, independently compare local/GitHub/Runtime hashes, then ask the existing Matrix/Planner owner for the new small-cohort Authority request.  Only if that request is fresh and issued through the existing Authority owner may the governed multi-member transaction run.

