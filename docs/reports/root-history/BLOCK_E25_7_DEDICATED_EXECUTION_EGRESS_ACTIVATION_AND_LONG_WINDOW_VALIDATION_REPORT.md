# BLOCK E25.7 — Dedicated Execution Egress Activation And Long Window Validation Report

## Final Verdict

`e25_7_completed=true`

E25.7 proved that the V7-normalized activation path itself is side-effect clean, but the candidate profile failed target-local connectivity and was removed. Therefore the dedicated execution target is not ready for first movement.

The block did not move users, did not mutate user route tables, did not run autoswitch apply, did not execute the raw profile, and did not change the kill switch.

## Required Final Answers

- `runtime_mutation_performed=true`
- `runtime_mutation_scope=normalized v7execwg0 config creation, interface activation, connectivity probe, rollback/removal only`
- `user_movement_performed=false`
- `routing_mutation_for_users=false`
- `profile_activated=true`
- `profile_active_now=false`
- `candidate_user=10.7.0.11`
- `candidate_still_on_1=true`
- `source_profile=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf`
- `normalized_interface=v7execwg0`
- `dedicated_execution_target_name=wireguard-exec-20260528-10-89-0-2`
- `route_table=1250`
- `raw_profile_executed=false`
- `table_off_enforced=true`
- `dns_side_effect_blocked=true`
- `hooks_absent=true`
- `global_route_side_effects_prevented=true`
- `dedicated_execution_target_created=false`
- `target_users_zero=true`
- `governance_reserved=false`
- `autoswitch_excluded=false`
- `rebalance_excluded=false`
- `production_assignment_blocked=false`
- `target_readiness_final_status=NO-GO`
- `target_diagnose=FAIL_CONNECTIVITY`
- `target_load=UNKNOWN_NOT_REGISTERED`
- `dedicated_target_sustained_go=false`
- `quality_spikes_detected=unknown`
- `no_sample_below_floor=false`
- `restore_settle_gate_status=CONDITIONAL_SINGLE_SAMPLE`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
- `runtime_checkers_ok=true`
- `first_movement_ready=false`
- `recommended_target=NONE`
- `remaining_blockers=TARGET_LOCAL_CONNECTIVITY_FAILED, ACTIVE_METADATA_NOT_WRITTEN, LONG_WINDOW_NOT_COLLECTED, EXECUTION_TARGET_READINESS_MODE_MISSING`
- `recommended_next_block=E25_7_1_DEDICATED_PROFILE_CONNECTIVITY_FIX_OR_REPLACEMENT`

## What Worked

The normalized wrapper was created from the candidate profile:

- `source_hash=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1`
- `normalized_config_hash=c838438d6a6d5f82d8137c6d1aaa0682ccf52446c7bc563168009e2873ee16ed`
- `Table=off` present
- DNS mutation removed
- hooks absent

`wg-quick up v7execwg0` succeeded and only performed interface setup:

- add `v7execwg0`;
- set WireGuard config;
- assign `10.89.0.2/32`;
- set MTU `1280`;
- bring interface up.

No default route, DNS, registry hash, user route table, or candidate route changed.

## What Failed

Target-local connectivity failed:

```text
ping -c 3 -W 3 -I v7execwg0 1.1.1.1
3 packets transmitted, 0 received
ping_exit=1
```

WireGuard transmit bytes increased, but receive bytes stayed `0 B`. This means the interface can be activated safely, but this endpoint/profile did not prove usable as an execution egress.

Because of that, E25.7 did not write active egress metadata and did not run a long-window validation.

## Governance Tooling Finding

A second blocker was identified before writing metadata:

- generic `v7-second-canary-target-readiness` rejects `manual_only=true`;
- generic `v7-second-canary-target-readiness` rejects `reserve_only=true`;
- an execution-only target should be manual/reserved.

So a future successful activation should include an execution-target by-id readiness mode, or an equivalent validator that treats `role=EXECUTION_ONLY` as eligible only for explicitly approved operator movement and still blocked for production autoswitch/rebalance.

## Rollback / Removal

Because validation failed, the interface was removed:

- `wg_quick_down_exit=0`
- `interface_removed=true`
- active config removed from `/etc/wireguard/v7execwg0.conf`
- config archived on VPS at `/root/e25_7_v7execwg0.conf.removed.20260528T121350Z`

Post-removal verification:

- default route unchanged;
- DNS resolver hash unchanged;
- users registry hash unchanged;
- egress registry hash unchanged;
- `10.7.0.11` remained on `1`;
- route table `1009` unchanged;
- runtime checkers OK.

## Evidence

- `docs/track7/productization/e25_7-evidence/pre-activation-safety-snapshot.md`
- `docs/track7/productization/e25_7-evidence/normalized-config-creation.md`
- `docs/track7/productization/e25_7-evidence/interface-activation.md`
- `docs/track7/productization/e25_7-evidence/target-connectivity-readiness.md`
- `docs/track7/productization/e25_7-evidence/dedicated-target-metadata.md`
- `docs/track7/productization/e25_7-evidence/governance-isolation-validation.md`
- `docs/track7/productization/e25_7-evidence/dedicated-target-long-window.md`
- `docs/track7/productization/e25_7-evidence/runtime-safety-validation.md`
- `docs/track7/productization/e25_7-evidence/rollback-removal-plan.md`
- `docs/track7/productization/e25_7-evidence/tests.md`

## Tests

- `py_compile`: PASS
- targeted unit tests: PASS, 47 tests
- full unit test discovery: PASS, 116 tests
- credential scan: PASS
- route/DNS side-effect scan: PASS
- normalized config safety scan: PASS
- dangerous-call scan: PASS with expected checker-source references only
- VPS runtime checkers after rollback: PASS
- hidden mover scan: PASS
- `git diff --check`: PASS after report

## Recommended Next Block

`E25_7_1_DEDICATED_PROFILE_CONNECTIVITY_FIX_OR_REPLACEMENT`

Scope should be:

1. determine why the `10.89.0.2` WireGuard test profile sends but receives no traffic;
2. decide whether the peer/endpoint is stale, blocked, or missing server-side state;
3. either fix/replace the dedicated profile or acquire a new known-good outbound profile;
4. add an execution-target by-id readiness validator before retrying first movement.

## Final Mutation Statement

- `Runtime mutation performed: YES`
- `If YES: only normalized v7execwg0 execution-egress activation and rollback/removal; no user movement`
- `User movement performed: NO`
- `Routing mutation for users performed: NO`
- `Kill switch mutation performed: NO`
- `Autoswitch apply performed manually: NO`
- `Raw profile executed: NO`
- `Canary performed: NO`
- `Cohort performed: NO`

