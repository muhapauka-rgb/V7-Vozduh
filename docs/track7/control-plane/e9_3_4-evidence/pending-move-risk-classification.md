# E9.3.4 Pending Move Risk Classification

Mode: read-only analysis. No apply restore was executed.

## Evidence Inputs

| Evidence | Path |
|---|---|
| Current authority snapshot | `docs/track7/control-plane/e9_3_4-evidence/current-authority-snapshot.txt` |
| Current target readiness JSON | `docs/track7/control-plane/e9_3_4-evidence/current-target-readiness.json` |
| Pending moves sample A | `docs/track7/control-plane/e9_3_4-evidence/pending-moves-A.md` |
| Pending moves sample B | `docs/track7/control-plane/e9_3_4-evidence/pending-moves-B.md` |
| Full planner journal probe | `docs/track7/control-plane/e9_3_4-evidence/planner-journal-json-30.txt` |

## Current Authority Truth

```text
v7-health.service=active/enabled
v7-autoswitch-planner.timer=active/enabled
v7-autoswitch-planner.service=inactive/static
v7-users-autoswitch.timer=inactive/enabled
v7-users-autoswitch.service=inactive/static
apply_restore_current_status=HELD
planner_only_active=true
apply_timer_held=true
```

No `v7-user-switch`, `v7-routing-sync`, or manual `v7-users-autoswitch --apply` process was observed in the E9.3.4 samples.

## Registry / Routing Health

```text
users.registry_sha256=045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222
egress.registry_sha256=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

The registry hashes remained stable across current-authority, sample A, and sample B evidence.

## Pending Moves Refresh

Fresh planner-only journal reconstruction showed three planner runs with:

```text
candidate_moves=0
candidate_moves_total=0
selected_moves=0
apply_requested=false
apply_result.applied=false
apply_result.reason=dry_run
```

The prior E9.3.3 planner-only pending moves were:

```text
10.7.0.5: 1 -> awg3
10.0.0.2: 1 -> awg3
10.0.0.3: 1 -> awg3
```

E9.3.4 did not reproduce those selected moves. The pending movement set is therefore not stable; it appears transient and tied to the previous Telegram/down signal window and anti-flap state.

## Per-Move Classification

| User | From | To | Current E9.3.4 Status | Risk | Safe To Apply Now? |
|---|---|---|---|---|---|
| `10.7.0.5` | `1` | `awg3` | not selected in fresh samples | previous non-canary movement; target has quality-floor conflict | no explicit approval |
| `10.0.0.2` | `1` | `awg3` | not selected in fresh samples | previous non-canary movement; target has quality-floor conflict | no explicit approval |
| `10.0.0.3` | `1` | `awg3` | not selected in fresh samples | previous non-canary movement; target has quality-floor conflict | no explicit approval |

## AWG3 Eligibility Conflict

`awg3` remains an eligibility conflict:

- the strict second-canary watcher rejects `awg3` because it is below the canary quality floor and lacks the required sensitive route-class exclusions in its registry row;
- the previous E9.3.3 planner-only stage nevertheless exposed `awg3` as a possible autoswitch target under a transient failover condition;
- E9.3.4 fresh planner samples no longer select `awg3`, so the conflict is not currently actionable but remains a governance mismatch.

## Apply Restore Decision

```text
pending_moves_visible=false
pending_moves_count=0_current
pending_moves_stable=false
pending_moves_safe_to_apply=false_without_separate_operator_approval
awg3_eligibility_conflict=true
approval_status=CONDITIONAL
execution_allowed_now=false
```

Apply restore is not approved by this packet. The safest path is to keep apply held until a separate bounded live apply-restore block repeats one final planner-only sample and receives explicit operator acceptance of either:

- zero current selected moves; or
- an exact accepted movement list and maximum movement count.
