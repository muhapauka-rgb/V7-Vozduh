# BLOCK E25.11 Execution-Only Egress NAT/MSS And Readiness Integration Report

## Verdict

`e25_11_completed=true`

`runtime_mutation_performed=true`

`runtime_mutation_scope=execution-only target activation, egress metadata append, nft NAT/MSS integration for v7execwg0, diagnose/load/readiness state integration, readiness helper deployment`

`user_movement_performed=false`

`routing_mutation_for_users=false`

`candidate_user=10.7.0.11`

`candidate_still_on_1=true`

`dedicated_execution_target_created=true`

`target_name=amneziawg-exec-20260528-10-8-1-14`

`interface_name=v7execwg0`

`handshake_successful=true`

`rx_packets_present=true`

`target_connectivity_usable=true`

`nat_integration_ok=true`

`mss_integration_ok=true`

`readiness_helper_supports_execution_only=true`

`target_readiness_final_status=NO-GO`

`autoswitch_excluded=true`

`rebalance_excluded=true`

`governance_isolation_valid=true`

`selected_moves_zero=true`

`hidden_movers_absent=true`

`runtime_checkers_ok=true`

`sustained_go=false`

`no_sample_below_floor=false`

`quality_spikes_detected=true`

`first_movement_ready=false`

## Summary

E25.11 completed the platform integration that E25.10 identified as missing.

The working external AmneziaWG profile is now integrated as an execution-only target:

- `v7execwg0` activates through the normalized wrapper;
- default route does not change;
- DNS does not change;
- user table `1009` does not change;
- `egress.registry` contains the execution-only target;
- NAT/MSS rules exist for `v7execwg0`;
- `v7-killswitch-check` is OK;
- `v7-provisioning-reconcile-check` is OK;
- default readiness mode still blocks the execution target;
- explicit operator execution readiness mode supports it safely.

However, the target is not ready for first movement because the 20-minute validation window found quality below floor:

- observed avg Mbps: `12.03 < 15.0`
- observed min Mbps: `5.08 < 10.0`
- final explicit readiness: `NO-GO`

This is now a quality/stability blocker, not a platform integration blocker.

## Artifacts

- `docs/track7/productization/e25_11-evidence/pre-integration-snapshot.md`
- `docs/track7/productization/e25_11-evidence/safe-activation.md`
- `docs/track7/productization/e25_11-evidence/execution-metadata-integration.md`
- `docs/track7/productization/e25_11-evidence/nat-mss-integration.md`
- `docs/track7/productization/e25_11-evidence/readiness-diagnose-load-integration.md`
- `docs/track7/productization/e25_11-evidence/governance-isolation-validation.md`
- `docs/track7/productization/e25_11-evidence/long-window-validation.md`
- `docs/track7/productization/e25_11-evidence/final-safety-validation.md`
- `docs/track7/productization/e25_11-evidence/tests.md`
- `docs/track7/productization/e25_11-evidence/restore-settle-samples/`
- `docs/track7/productization/e25_11-evidence/restore-settle-gate-result.md`
- `docs/track7/productization/e25_11-evidence/restore-settle-gate-result.json`

## Code Changes

- `tools/v7-second-canary-target-readiness`
  - added explicit `--execution-target-id` mode;
  - default mode still rejects `manual_only` and `reserve_only`;
  - explicit mode requires `role=EXECUTION_ONLY`, reservation metadata, autoswitch/rebalance/production assignment disabled;
  - quality summary now remains a per-key fallback when `egress-stability.state` exists.
- `tests/unit/test_v7_second_canary_target_readiness.py`
  - added execution-only helper tests;
  - added quality-summary fallback regression test.

## Runtime Integration

Execution-only target metadata:

```text
id=amneziawg-exec-20260528-10-8-1-14
protocol=amneziawg
interface=v7execwg0
role=EXECUTION_ONLY
manual_only=1
reserve_only=1
execution_reserved=true
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
```

NAT/MSS integration:

```text
V7 NAT users via v7execwg0
V7 MSS clamp users via v7execwg0
V7 allow users via v7execwg0
```

Final runtime checkers:

- `v7-reconcile-check=OK`
- `v7-user-route-check=OK`
- `v7-killswitch-check=OK`
- `v7-provisioning-reconcile-check=OK`

## Restore-Settle

Fresh E25.11 restore-settle gate:

- gate status: `GO`
- sample count: `3`
- samples span: `58 seconds`
- apply timer intervals covered: `2.9`
- selected moves: `[0, 0, 0]`
- hidden movers observed: `false`
- registry stable: `true`
- egress registry stable: `true`

## Tests

- py_compile relevant files: PASS
- targeted tests: PASS, `38 tests`
- full unittest discover: PASS, `119 tests`
- endpoint inventory command: PASS
- credential scan: PASS
- dangerous-call scan: PASS with expected normalized profile activation
- `git diff --check`: PASS
- static `/admin-v2` render smoke: not applicable

## Remaining Blockers

`EXECUTION_TARGET_QUALITY_BELOW_FLOOR`

`SUSTAINED_GO_NOT_PROVEN`

`FIRST_MOVEMENT_STILL_BLOCKED_BY_TARGET_QUALITY`

The target is integrated and governed, but movement must not proceed while explicit readiness is `NO-GO`.

## Recommendation

`recommended_next_block=E25_12_EXECUTION_TARGET_QUALITY_RECOVERY_OR_REPLACEMENT`

Do not run first governed user movement yet. The next block should either recover this execution target quality with a fresh sustained GO window, or import a stronger external execution profile using the now-proven E25.11 integration path.

## Final Mutation Statement

Runtime mutation performed: YES

If YES: only execution-only target platform integration and validation.

User movement performed: NO

Routing mutation for users performed: NO

Kill switch control/toggle mutation performed: NO

Kill-switch table NAT/MSS integration performed: YES, limited to `v7execwg0`

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort performed: NO
