# Z8.5 Evidence 01 - Local Worktree Duplication

## Worktrees / Branches Observed

Current workspace:

```text
path=/Users/ponch/Documents/New project
branch=Updatesystem
commit=d61480dea6de67ea9d2cfd5c3440d93896076178
```

Separate worktree:

```text
path=/private/tmp/v7-convergence-c
branch=v7-next
commit=c40cae13298594b7ad7040df4b19306c4e2c29d4
```

## v7-next Worktree Status

`/private/tmp/v7-convergence-c` is not clean; it contains untracked Z5/Z5.5 documentation files.

## Operation Wiring Marker Scan

Current `Updatesystem` workspace contains Z7/Z8 operation wiring markers:

- `operation_id`
- `operation_owner`
- `runtime_snapshot_hash`
- `finalize_operation`
- `runtime_operation_terminal`
- `closure_target`

`/private/tmp/v7-convergence-c` marker scan returned no matches for the same operation wiring markers in:

- `/private/tmp/v7-convergence-c/tools/v7-users-autoswitch`
- `/private/tmp/v7-convergence-c/tests/unit/test_v7_users_autoswitch_policy.py`

## Classification

| Copy | Classification | Reason |
| --- | --- | --- |
| `/Users/ponch/Documents/New project` | PARTIAL / current local Z7-Z9 work | Contains operation wiring commit but dirty and not proven runtime |
| `/private/tmp/v7-convergence-c` | STALE for Z7/Z8 operation wiring | Branch is `v7-next`, but lacks recent operation wiring markers |
| Production runtime | UNKNOWN | SSH/live truth not proven |
