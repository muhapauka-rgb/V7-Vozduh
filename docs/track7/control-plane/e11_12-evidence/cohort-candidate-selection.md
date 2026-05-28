# E11.12 Two-User Candidate Selection

candidate_selection_completed=true
execution_allowed_now=false
mini_cohort_execution_performed=false

## Fresh Runtime Binding

Fresh state root: `docs/track7/control-plane/e11_12-evidence/current-state/`

```text
users.registry_sha256=27e42d79bd073b7ad4934814958ab9301d46f4b730074fe9cc3f9b3d70410be7
egress.registry_sha256=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
wireguard_users=0
wireguard_reserved=true
target_readiness=GO
restore_settle_gate=GO
selected_moves=0
```

E11.12 does not reuse the old E11.10 `10.7.0.3 -> awg0` candidate truth. Fresh
runtime shows `10.7.0.3` is currently on target `1`, so it is rejected for this
approval packet.

## Selected Candidates

| User | Current egress | Route table | Rollback target | Route evidence | Selection reason |
| --- | --- | --- | --- | --- | --- |
| `10.7.0.11` | `1` | `1009` | `1` | `default dev v7e356a192b79`; `route_get` from `10.7.0.11` uses table `1009` | enabled, stable current egress, `switches_1h=0`, no recent WireGuard target in `last_targets`, rollback is direct table restore |
| `10.7.0.12` | `1` | `1010` | `1` | `default dev v7e356a192b79`; `route_get` from `10.7.0.12` uses table `1010` | enabled, stable current egress, `switches_1h=0`, no recent WireGuard target in `last_targets`, rollback is direct table restore |

selected_candidates=10.7.0.11,10.7.0.12
selected_target=wireguard-1779454504-c43409
rollback_targets=1,1
blast_radius=2_users_max

Expected forward route target:

```text
wireguard_interface=v7e06a394c478
10.7.0.11 expected_forward_table=default dev v7e06a394c478 scope link
10.7.0.12 expected_forward_table=default dev v7e06a394c478 scope link
```

## Rejected Candidates

| User(s) | Rejection reason |
| --- | --- |
| `10.0.0.2`, `10.0.0.3`, `10.0.0.6` | recent churn/freeze pressure: `switches_1h=2`, current target `awg3` |
| `10.7.0.2`, `10.7.0.9`, `10.7.0.10` | fresh runtime drift moved them from `awg0` to `1`; `switches_1h=2` |
| `10.7.0.3`, `10.7.0.4`, `10.7.0.5`, `10.7.0.6`, `10.7.0.8` | recent movement to target `1`; `switches_1h=1` |
| `10.7.0.7` | disabled user |
| `10.7.0.13`, `10.7.0.14`, `10.7.0.15` | `switches_1h=0`, but `last_targets` includes `wireguard-1779454504-c43409`; higher attribution risk for a fresh mini-cohort |

## Verdict

candidate_selection_verdict=GO_FOR_APPROVAL_PACKET_ONLY

The candidate pair is suitable for a future two-user mini-cohort approval
because both users are stable in the latest state and have direct rollback to
their current egress. Execution remains forbidden by E11.12.
