# E8.5 Evidence - Post-Split Quiet-Window Rehearsal

This directory contains evidence from the bounded live E8.5 rehearsal.

Permitted live mutation was limited to temporary hold and restore of:

```text
v7-autoswitch-planner.timer
v7-autoswitch-planner.service
v7-users-autoswitch.timer
v7-users-autoswitch.service
```

`v7-health.service` remained active.

## Files

| File | Purpose |
|---|---|
| `pre-hold.txt` | pre-hold runtime/service/check snapshot |
| `hold-confirmation.txt` | first hold attempt evidence; guard false-positive caused immediate restore |
| `hold-confirmation-2.txt` | corrected authoritative hold confirmation |
| `quiet-sample-A.txt` | quiet-window sample A |
| `quiet-sample-B.txt` | quiet-window sample B |
| `quiet-sample-C.txt` | quiet-window sample C |
| `post-restore.txt` | immediate post-restore evidence |
| `post-restore-settled.txt` | settled post-restore evidence |

## Verdict

```text
quiet_window_verified=true
autoswitch_fully_quiet=true
v7-health_stayed_active=true
users.registry_stable=true
egress.registry_stable=true
reconcile_under_quiet=STABLE_FAIL
user_route_check=OK
killswitch_check=OK
provisioning_reconcile_check=OK
```

The first hold guard self-matched its own command string. The corrected no-self guard evidence is in `hold-confirmation-2.txt` and quiet samples A/B/C.
