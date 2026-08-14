# BLOCK E9.2.2 - Second Canary Target Selection Refresh

Mode: read-only / target selection only.

Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO

## Executive Verdict

```text
candidate_user=10.7.0.14
candidate_still_valid=true
selected_target=NONE
selected_target_ready=false
selected_target_zero_user=false
target_1_ready_now=false
target_1_current_user=10.7.0.5
approval_status=NO-GO
execution_allowed_now=false
```

E9.2.2 found no safe zero-user target for the second one-user canary.

The candidate user remains valid:

```text
10.7.0.14 current=vless table=1012 enabled=1
route_get from 10.7.0.14 -> dev tun0 table 1012
```

The target is the blocker:

- target `1` is still occupied by real user `10.7.0.5`;
- `awg0` and `awg3` are zero-user but below quality floor;
- OpenVPN and WireGuard fast targets are zero-user but diagnose `SUSPECT` because handshake is stale.

## Fresh Snapshot

```text
captured_utc=2026-05-25T15:31:42Z
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Runtime assignment summary:

```text
10.7.0.5 current=1 table=1003 enabled=1
10.7.0.14 current=vless table=1012 enabled=1
```

Target `1`:

```text
interface=v7e356a192b79
interface_state=UP,LOWER_UP
diagnose=OK
avg_mbps=59.868
min_mbps=51.33
stability=0.857386
registry_users=1
load_users=1
static_load_status=SOFT_FULL
```

## Target Candidate Matrix

| Egress | Zero User | Interface | Diagnose | Quality | Sensitive-Class Exclusion | Verdict |
|---|---|---|---|---|---|---|
| `1` | no | UP | OK | good | yes | reject: occupied by `10.7.0.5` |
| `awg0` | yes | UP | OK | below floor | no explicit exclusion | reject: avg/min/stability too low |
| `awg3` | yes | UP | OK | below floor | no explicit exclusion | reject: avg/min too low |
| `openvpn-1779388847-d2ad7c` | yes | UP | SUSPECT | good | yes | reject: stale handshake |
| `wireguard-1779454504-c43409` | yes | UP | SUSPECT | good | yes | reject: stale handshake |

Full matrix:

```text
docs/track7/control-plane/e9_2_2-evidence/target-candidate-matrix.md
```

## Preview Result

No executable forward preview was generated because no safe target was selected.

Artifacts are still present and explicitly marked non-actionable:

```text
docs/track7/control-plane/e9_2_2-evidence/forward-preview.json
docs/track7/control-plane/e9_2_2-evidence/rollback-preview.json
```

Forward preview status:

```text
preview_generated=false
error=no_safe_zero_user_target
would_run_command=null
```

Rollback preview status:

```text
preview_generated=false
error=forward_target_not_selected
would_run_command=v7-user-switch 10.7.0.14 vless
note=candidate already on vless
```

## Rejected Targets

```text
1: occupied by real user 10.7.0.5; static load SOFT_FULL
awg0: below quality floor; avg=11.909 min=4.17 stability=0.350155
awg3: below quality floor; avg=5.62633 min=4.39
openvpn-1779388847-d2ad7c: diagnose SUSPECT; handshake stale
wireguard-1779454504-c43409: diagnose SUSPECT; handshake stale
```

## Canary Implication

E9.3 should not run now.

The second-canary experiment needs either:

1. target `1` returns to zero users and is revalidated;
2. OpenVPN/WireGuard diagnose becomes OK in a future read-only snapshot;
3. a separate operator approval accepts a non-clean target, with the understanding that the test is no longer a clean zero-user second mechanics canary.

The safest path is option 1 or 2, not waiver.

## Exact Next Recommended Step

```text
Wait for a clean target state, then rerun E9.2.2 target selection refresh.
```

If the operator wants to proceed sooner, prepare a new approval packet with an explicit waiver. That waiver must state which target is accepted despite the blocker and why the experiment remains bounded.

## Final Answers

```text
candidate_user=10.7.0.14
candidate_still_valid=true
selected_target=NONE
selected_target_ready=false
selected_target_zero_user=false
target_1_ready_now=false
target_1_current_user=10.7.0.5
rejected_targets=1,awg0,awg3,openvpn-1779388847-d2ad7c,wireguard-1779454504-c43409
approval_status=NO-GO
execution_allowed_now=false
recommended_next_step=wait_for_clean_target_or_rerun_read_only_target_selection
runtime_mutation_performed=NO
user_movement_performed=NO
routing_mutation_performed=NO
canary_performed=NO
```
