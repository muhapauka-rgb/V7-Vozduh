# BLOCK P6 - First User Movement Program Report

Project: V7 Vozduh

Program: P6

Block: P6

Mode: Certification / Execution / Observation / Verification

## 1. Reality Audit

Fresh runtime truth was collected from:

`/opt/v7/egress/state`

Candidate:

- user: `10.7.0.11`
- current egress before: `1`
- route table: `1009`
- enabled: `1`

Target:

- egress: `amneziawg-exec-20260528-10-8-1-14`
- interface: `v7execwg0`
- target users before: `0`

Existing runtime tooling was present and reused.

## 2. Conflict Audit

The existing movement path was reused:

`v7-user-switch`

No duplicate movement system, execution engine, runtime hook, autoswitch apply, rebalance, deploy, or systemd change was introduced.

## 3. Truth Source Audit

Canonical runtime sources were live files under `/opt/v7/egress/state`.

The packet, preview, readiness, verification, observation, and rollback reports were derived from live runtime data and command outputs.

No truth-source conflict was found.

## 4. Runtime Audit

Before movement:

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`
- admin health: `OK`
- autoswitch timer: `inactive`

## 5. Target Readiness

Target readiness passed:

- candidate_still_valid=true
- approval_status=GO
- second_canary_readiness=GO
- selected_target=`amneziawg-exec-20260528-10-8-1-14`
- runtime_commands_executed=false

## 6. Packet

Packet:

- packet_id: `packet-p6-5b8223b9d803f429b8a67b78`
- approval_id: `approval-p6-af5e2daa75c37706b4a73559`
- packet hash: `4652e77f81e1acf172e0a026b9e4b0ce45afbc8b032accc149be4d962f30cbe3`
- movement_budget: `1`
- allowed_users: `["10.7.0.11"]`
- allowed_targets: `["amneziawg-exec-20260528-10-8-1-14"]`
- rollback_target: `1`
- route_table: `1009`

## 7. Approval Validation

Approval validation passed:

- approval_valid=true
- errors=`[]`

## 8. Runtime Recheck

Immediate pre-movement recheck passed:

- hashes unchanged
- selected moves unchanged at `0`
- candidate unchanged on `1`
- target users `0`
- route table `1009` unchanged before movement

## 9. Movement Execution

Executed exactly:

`v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14`

Result:

- exit code: `0`
- final candidate egress: `amneziawg-exec-20260528-10-8-1-14`
- route table `1009`: `default dev v7execwg0 scope link`
- forward audit hash: `271cd889ade88fb8de175c79abb72407464bc2074411eca73c8a353f3b486501`

## 10. Observation Window

Observation showed:

- target users: `0 -> 1`
- switch history count: `2738 -> 2739`
- users outside candidate unchanged
- routing outside scope unchanged
- ip rule hash unchanged
- selected moves remained `0`
- admin health remained `OK`

Checkers:

- `v7-user-route-check`: `OK`
- `v7-killswitch-check`: `OK`
- `v7-provisioning-reconcile-check`: `OK`

## 11. Rollback Readiness

Rollback path is ready:

`v7-user-switch 10.7.0.11 1`

Rollback preview has no errors and would restore route table `1009` to `v7e356a192b79`.

Rollback was not executed.

## 12. Replay Test

Replay validation:

- used forward records: `1`
- verdict: `DENY_REPLAY`
- movement_executed_during_replay=false
- replay audit hash: `cbd5eae08adaed972fe4bbe02aa71ed1661e4c290c889fb7e45fce852d7a82a8`

Expired packet:

- verdict: `DENY_EXPIRED_PACKET`
- movement_executed=false

## 13. Fail Closed Review

Fail-closed states all abort:

- unknown
- missing
- stale
- expired
- invalid
- mismatched
- blocked

No movement was executed for fail-closed validation cases.

## 14. Final Verification

Final state:

- `10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14`
- table `1009` uses `v7execwg0`
- target users: `1`
- users outside scope untouched: true
- routing outside scope changed: false
- rollback available: true

## 15. Outcome

P6 first user movement succeeded.

Exactly one approved user moved to exactly one approved target.

No autoswitch apply, rebalance, policy apply, deploy, systemd change, runtime hook, or rollback execution occurred.

## 16. Remaining Risks

- The user remains on execution-only target until a later authorized rollback or next observation block.
- This certifies a single-user movement only; it does not authorize cohort movement.
- Direct/Trusted RU state still needs separate governance before any sensitive route-class movement.
- Replay protection is audit-gated for this movement program, not a general-purpose movement engine.

## 17. Recommendation For Next Block

Run a post-movement stability and rollback-decision block before expanding scope.

Recommended next block:

`P6.B POST FIRST USER MOVEMENT OBSERVATION AND ROLLBACK DECISION`

It should decide whether to hold, roll back, or certify readiness for a second user, based on fresh observation and explicit approval.

## Required Verdicts

- target_ready=true
- packet_created=true
- approval_valid=true
- runtime_recheck_passed=true
- movement_executed=true
- observation_completed=true
- rollback_ready=true
- replay_protection_verified=true
- fail_closed_verified=true
- first_user_movement_successful=true

## Safety Verdict

- scope_expanded=false
- users_moved_count=1
- routing_changed_outside_scope=false
- autoswitch_apply_run=false
- deploy_performed=false
- rollback_executed=false

Only approved packet scope executed.
