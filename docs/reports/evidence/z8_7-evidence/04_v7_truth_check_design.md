# Z8.7 Evidence 04 - v7-truth-check Design

## Command

```text
v7-truth-check
```

## Purpose

One command, one verdict.

It proves current workspace, current branch, current commit, runtime branch, runtime commit, runtime status, state status, convergence status, and final PASS/FAIL.

## Modes

```text
v7-truth-check --local
v7-truth-check --github
v7-truth-check --runtime-readonly
v7-truth-check --all
v7-truth-check --json
```

## Non-Mutation Rules

The command must never:

- deploy
- run autoswitch apply
- move users
- mutate routes
- restart services
- change systemd
- write runtime state
- run git pull
- run git push
- merge
- cleanup

## Required Final Output

```text
project=V7 Vozduh
canonical_workspace=/Users/ponch/Documents/New project
canonical_branch=Updatesystem
workspace_branch=<value>
workspace_commit=<value>
workspace_status=<clean|dirty|scoped_dirty>
github_commit=<value>
runtime_root=<value>
runtime_branch=<value|UNKNOWN>
runtime_commit=<value|UNKNOWN>
autoswitch_hash=<value|UNKNOWN>
audit_hash=<value|UNKNOWN>
autoswitch_service=<active|inactive|failed|UNKNOWN>
autoswitch_timer=<active|inactive|failed|UNKNOWN>
state_freshness=<OK|STALE|UNKNOWN>
restore_barrier=<clear|active|UNKNOWN>
audit_availability=<OK|UNKNOWN>
closure_availability=<OK|UNKNOWN>
operation_wiring=<present|missing|UNKNOWN>
verdict=<PASS|NO-GO>
```

## Design Status

Defined only. No implementation was created in Z8.7.
