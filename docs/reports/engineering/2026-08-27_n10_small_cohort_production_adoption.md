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

## Deployment and live result

Published and deployed commits: `9582fbed`, `9bda78e7`, `a905bc2a`, `24a7d9c9`, `ee262106`, `f47c3113`, `bdd225ec`, and `e17f1cbe`.  Each deployment passed the existing safe-deploy gate; the final Runtime hash, local hash and GitHub commit were aligned. `v7-health.service` was active; the obsolete standalone full-Matrix timer remained disabled.

The live Matrix owner then rebuilt the prepared projection in observation-only mode. It automatically excluded certification identity `10.7.0.19` and registered one exact two-member request for `10.7.0.33` and `10.7.0.68`, both on `openvpn-1779388847-d2ad7c`. No user, route, Candidate, Packet or Lease was created during preparation.

The existing Authority owner issued one exact 15-minute, one-use contract (`acc_dedd67a17e836c53db52b364`), with source, two names, membership fingerprint, maximum two users, maximum one concurrent transaction, rollback and per-member S11 requirements. Issuance wrote policy/audit only; it did not move users.

The governed live invocation then performed the bounded fresh decision path for exactly two members:

- active scope: `2` users;
- candidate evaluation: `35.773 ms` for two decisions;
- authority/capacity validation: `0.151 ms`;
- no route writer invocation and `0` users moved.

It stopped before Apply with `n10_packet_bound_restore_barrier_required`. The direct measured cause is that the existing N10 Packet/Lease/Barrier producer still materializes an exact single-device approved barrier only; the new two-member contract is correctly recognised by Planner and Authority, but does not yet receive the corresponding existing-owner cohort Packet/Barrier bundle. This is a bounded implementation gap, not a safety bypass and not an external dependency.

## Verification

- Focused unit suite after the final change: **317 passed**.
- All safe-deploy gates: **PASS**.
- Final live attempt: **DENIED before Apply**, so no ordinary-client route or assignment changed.
- The decision invocation also exposed stale intelligence snapshot source hashes; this was independently STOP_SAFE and remains a required freshness repair before any cohort retry.

## Exact next action

Extend the existing Packet/Lease/Barrier owner (not a new owner) to materialize and validate one exact common-target cohort bundle for the already-issued `N10_SMALL_COHORT` contract. It must bind the two exact members, one Planner-selected target, current source generation and one operation; it must stop remaining forwards on the first failure. Then refresh the existing intelligence snapshots, issue a fresh one-use contract (the current one must not be reused), and rerun the same bounded transaction.
