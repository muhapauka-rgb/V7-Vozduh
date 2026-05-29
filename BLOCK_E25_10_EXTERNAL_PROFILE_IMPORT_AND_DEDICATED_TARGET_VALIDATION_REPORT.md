# BLOCK E25.10 External Profile Import And Dedicated Target Validation Report

## Verdict

`e25_10_completed=true`

`new_profile_found=true`

`profile_path=/Users/ponch/Downloads/amnezia_for_awg (1) (1).conf`

`profile_reused_known_dead=false`

`runtime_mutation_performed=true`

`runtime_mutation_scope=operator-provided profile import to VPS, normalized config creation, target-local interface activation, temporary execution-target metadata append, metadata/interface rollback`

`user_movement_performed=false`

`routing_mutation_for_users=false`

`endpoint_self_reference=false`

`safe_for_normalization=true`

`handshake_successful=true`

`rx_packets_present=true`

`target_connectivity_usable=true`

`dedicated_execution_target_created=false`

`target_readiness_final_status=NO-GO`

`sustained_go=false`

`no_sample_below_floor=false`

`candidate_user=10.7.0.11`

`candidate_still_on_1=true`

`first_movement_ready=false`

`recommended_target=NONE`

## Summary

E25.10 successfully imported the new operator-provided external AmneziaWG profile and proved it is not another dead/self-referential profile.

The normalized wrapper worked:

- raw profile was not executed;
- DNS side effect was removed;
- `Table=off` prevented global route takeover;
- route/nft hooks were absent;
- empty optional AmneziaWG `I1`-`I5` fields were removed after a fail-closed parse error;
- `v7execwg0` reached handshake;
- RX packets appeared;
- ping through the interface succeeded.

However, promoting the working profile into active dedicated egress metadata is not yet production-safe. When the execution-only row was added to `egress.registry`, runtime checkers correctly failed because `v7execwg0` did not have kill-switch/provisioning NAT/MSS integration. The metadata row and active interface were rolled back immediately, and runtime returned to clean state.

## Artifacts

- `docs/track7/productization/e25_10-evidence/profile-presence-check.md`
- `docs/track7/productization/e25_10-evidence/quarantine-safety-analysis.md`
- `docs/track7/productization/e25_10-evidence/v7-normalization.md`
- `docs/track7/productization/e25_10-evidence/target-local-activation.md`
- `docs/track7/productization/e25_10-evidence/dedicated-target-metadata.md`
- `docs/track7/productization/e25_10-evidence/long-window-validation.md`
- `docs/track7/productization/e25_10-evidence/final-safety-validation.md`
- `docs/track7/productization/e25_10-evidence/tests.md`
- `docs/track7/productization/e25_10-evidence/quarantine/amnezia_for_awg.redacted.conf`

## Key Evidence

- provided profile SHA256: `d6029f2b6e4d33afd458d3b9a4bd18ad436c1b4de4a6ee78b4194213f8448ce8`
- normalized config SHA256 after remediation: `1016222374577511ac3292f8d30b899ca1d6c95d6b3ede7299e69cf8e504f41d`
- target-local interface: `v7execwg0`
- target-local address: `10.8.1.14/32`
- connectivity probe: `3 packets transmitted, 3 received, 0% packet loss`
- RX/TX after probe: `476 B received, 728 B sent`
- final `users.registry` SHA256: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- final `egress.registry` SHA256: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

## Blockers

`EXECUTION_TARGET_NAT_MSS_INTEGRATION_MISSING`

`EXECUTION_TARGET_DIAGNOSE_LOAD_READINESS_INTEGRATION_MISSING`

`READINESS_HELPER_DOES_NOT_YET_SUPPORT_EXECUTION_ONLY_TARGET_AS_MOVEMENT_DESTINATION`

The target-local profile works, but it cannot be used for first governed user movement until the execution-only target is integrated with:

- NAT/MSS kill-switch expectations;
- provisioning reconcile expectations;
- diagnose/load/quality state;
- readiness helper semantics for manual/reserved execution-only targets.

## Tests

- py_compile relevant admin/operator files: PASS
- targeted operator tests: PASS, `25 tests`
- full unittest discover: PASS, `116 tests`
- endpoint inventory command: PASS
- runtime checkers after rollback: PASS
- credential scan: PASS, only redacted placeholders matched
- dangerous-call scan: PASS, no user movement/autoswitch/kill-switch mutation
- `git diff --check`: PASS
- static `/admin-v2` render smoke: not applicable; no UI touched

## Recommendation

`recommended_next_block=E25_11_EXECUTION_ONLY_EGRESS_NAT_MSS_AND_READINESS_INTEGRATION`

Do not attempt first user movement yet. The next block should integrate the working external profile as an execution-only egress in the runtime governance layer without exposing it to autoswitch/rebalance.

## Final Mutation Statement

Runtime mutation performed: YES

If YES: only new external profile import, normalized config creation, target-local activation/validation, temporary metadata append, and rollback/removal.

User movement performed: NO

Routing mutation for users performed: NO

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort performed: NO
