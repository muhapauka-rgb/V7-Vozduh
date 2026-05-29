# BLOCK E25.12 Execution Target Quality Recovery Or Replacement Report

## Verdict

`e25_12_completed=true`

`runtime_mutation_performed=true`

`runtime_mutation_scope=target-local MTU recovery for v7execwg0 plus measured execution-target quality state refresh`

`user_movement_performed=false`

`routing_mutation_for_users=false`

`candidate_user=10.7.0.11`

`candidate_still_on_1=true`

`current_target=amneziawg-exec-20260528-10-8-1-14`

`current_target_recovered=true`

`quality_root_cause=MEASUREMENT_NOISE_AND_HOST_LOAD_CONTENTION_WITH_MTU_1280_INSTABILITY`

`quality_recovery_attempted=true`

`quality_recovery_successful=true`

`avg_mbps_final=27.12`

`min_mbps_final=10.67`

`stability_final=1.000`

`target_readiness_final_status=GO`

`sustained_go=true`

`no_sample_below_floor=true`

`replacement_profile_used=false`

`replacement_target_name=NONE`

`selected_moves_zero=true`

`hidden_movers_absent=true`

`runtime_checkers_ok=true`

`first_movement_ready=true`

`recommended_target=amneziawg-exec-20260528-10-8-1-14`

## Summary

E25.12 recovered the already-integrated execution-only AmneziaWG target without moving users.

The root cause was not a dead peer, missing NAT/MSS, or governance failure. The target had working handshake/RX/connectivity, but the `MTU=1280` configuration produced quality dips below the readiness floor during E25.11. E25.12 tested bounded target-local MTU variants and selected `MTU=1200`, which eliminated floor breaches in the sustained validation window.

After recovery:

- `v7execwg0` remained up and target-local only;
- default route did not change;
- DNS did not change;
- user route table `1009` did not change;
- `10.7.0.11` stayed on `1`;
- selected moves stayed zero;
- hidden movers stayed absent;
- all runtime checkers stayed OK;
- explicit execution-target readiness returned `GO`;
- restore-settle returned `GO`.

## Artifacts

- `docs/track7/productization/e25_12-evidence/quality-root-cause-snapshot.md`
- `docs/track7/productization/e25_12-evidence/quality-recovery-attempts.md`
- `docs/track7/productization/e25_12-evidence/current-target-revalidation-window.md`
- `docs/track7/productization/e25_12-evidence/replacement-profile-option.md`
- `docs/track7/productization/e25_12-evidence/governance-safety-validation.md`
- `docs/track7/productization/e25_12-evidence/first-movement-readiness-decision.md`
- `docs/track7/productization/e25_12-evidence/tests.md`
- `docs/track7/productization/e25_12-evidence/quality-samples.tsv`
- `docs/track7/productization/e25_12-evidence/final-readiness.pretty`
- `docs/track7/productization/e25_12-evidence/final-readiness.json`
- `docs/track7/productization/e25_12-evidence/restore-settle-gate.pretty`
- `docs/track7/productization/e25_12-evidence/restore-settle-gate.json`
- `docs/track7/productization/e25_12-evidence/restore-settle-samples/`

## Recovery Performed

Selected change:

```text
interface=v7execwg0
config=/etc/amnezia/v7execwg0.conf
old_mtu=1280
new_mtu=1200
backup=/etc/amnezia/v7execwg0.conf.e25_12_mtu1280_backup
```

Safety verification immediately after change:

```text
default_route_unchanged=true
dns_unchanged=true
table_1009_unchanged=true
users_registry_unchanged=true
v7_reconcile_check=OK
v7_user_route_check=OK
v7_killswitch_check=OK
v7_provisioning_reconcile_check=OK
```

## Sustained Window

- sample count: `20`
- window start UTC: `2026-05-28T17:38:51Z`
- window end UTC: `2026-05-28T18:00:40Z`
- span seconds: `1309`
- avg Mbps: `27.12`
- min Mbps: `10.67`
- stability: `1.000`
- samples below `10 Mbps`: `0`
- target users: `0` in every sample
- selected moves: `0` in every sample
- hidden movers: `0` in every sample
- runtime checkers: OK in every sample

The final explicit readiness result:

```text
selected_target=amneziawg-exec-20260528-10-8-1-14
approval_status=GO
execution_allowed_now=False
```

## Restore-Settle

Fresh restore-settle gate on the E25.12 sample set:

- gate status: `GO`
- sample count: `20`
- samples span seconds: `1309`
- apply timer intervals covered: `65.45`
- registry stable: `true`
- egress registry stable: `true`
- checkers OK: `true`
- hidden movers observed: `false`
- moved users: none

## Tests

- py_compile relevant files: PASS
- targeted unit tests: PASS, `33 tests`
- full unittest discover: PASS, `119 tests`
- endpoint inventory: PASS, `211 endpoints`
- explicit readiness helper pretty/json: PASS
- restore-settle helper pretty/json: PASS
- runtime checkers: PASS
- hidden mover scan: PASS
- credential scan: PASS
- dangerous-call scan: PASS
- route side-effect scan: PASS
- DNS side-effect scan: PASS
- `git diff --check`: PASS

## Remaining Blockers

`FRESH_APPROVAL_PACKET_REQUIRED_FOR_MOVEMENT`

`EXECUTION_TIME_RECHECK_STILL_REQUIRED_BEFORE_ANY_USER_MOVEMENT`

`MOVEMENT_PACKET_CONSUMER_STILL_NOT_CONNECTED_FOR_USER_MOVEMENT`

The target is ready for a fresh first-movement approval packet. This block does not authorize immediate movement.

## Recommendation

`recommended_next_block=E25_13_FRESH_APPROVAL_PACKET_FOR_FIRST_MOVEMENT_WITH_EXECUTION_TARGET`

E25.13 should generate a fresh movement approval packet for `10.7.0.11 -> amneziawg-exec-20260528-10-8-1-14`, using the recovered target state and requiring a new execution-time recheck in the eventual movement block.

## Final Mutation Statement

Runtime mutation performed: YES

If YES: only execution target quality recovery and validation:

- `v7execwg0` MTU changed to `1200`
- `/etc/amnezia/v7execwg0.conf` MTU changed to `1200`
- `/opt/v7/egress/state/egress-stability.state` refreshed from the E25.12 measured quality window

User movement performed: NO

Routing mutation for users performed: NO

Kill switch control/toggle mutation performed: NO

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort performed: NO
