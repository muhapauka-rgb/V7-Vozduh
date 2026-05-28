# E25.1 Refreshed Packet Denial Tests

## Scope

These tests validated the refreshed E25.1 movement approval packet without executing movement. They used an in-memory packet validator for the movement packet shape because the existing production packet consumer is intentionally zero-movement only.

Packet under test:

`docs/track7/productization/e25_1-evidence/fresh-movement-approval-packet.json`

## Expected Valid Packet

`ALLOW`

Validated fields:

- `runtime_action=BOUNDED_USER_MOVEMENT`
- `execution_method=APPROVED_RAW_FALLBACK_PREPARED`
- `ui_execution_allowed=false`
- `execution_allowed_now=false`
- `movement_budget=1`
- `allowed_users=["10.7.0.11"]`
- `allowed_targets=["wireguard-1779454504-c43409"]`
- `from_egress=1`
- `rollback_target=1`
- `fresh_users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `fresh_egress_registry_hash=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- `live_selected_moves_hash=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- `generation_id=E25_1_FIRST_BOUNDED_USER_MOVE_10_7_0_11_TO_WIREGUARD_20260528T103331Z`

## Denial Matrix

| Mutation | Expected | Actual |
|---|---:|---:|
| Expired packet | DENY | DENY |
| Unauthorized user | DENY | DENY |
| Unauthorized target | DENY | DENY |
| `movement_budget=2` | DENY | DENY |
| Stale users.registry hash | DENY | DENY |
| Stale egress.registry hash | DENY | DENY |
| Stale selected-move hash | DENY | DENY |
| Missing second confirmation | DENY | DENY |
| Wrong generation id | DENY | DENY |
| UI execution enabled | DENY | DENY |
| Autoswitch apply allowed | DENY | DENY |
| Kill switch mutation allowed | DENY | DENY |

## Harness Note

The first local in-memory validator pass exposed a harness gap: a wrong-generation packet was incorrectly allowed because the harness only checked that the field was non-empty. The harness was corrected to require the exact E25.1 generation id, then the denial matrix was re-run and all denial tests passed.

This did not affect runtime state and did not execute any movement.

## Result

`all_denial_tests_pass=true`

`runtime_mutation_performed=false`

`user_movement_performed=false`

`routing_mutation_performed=false`
