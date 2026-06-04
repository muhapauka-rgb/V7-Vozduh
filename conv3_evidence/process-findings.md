# CONV.3 Process Findings

## Finding 1: Safe Deploy Had A Wrong Default Target

The deploy tool could run correctly only when `V7_PROD_SSH_TARGET=v7-vps` was supplied.

This was a process bug because the operator should not have to remember the production SSH alias after convergence automation exists.

Resolution:

- `production_ssh_target` is now declared in the runtime truth manifest;
- safe deploy reads the manifest target when the environment variable is not set.

## Finding 2: Runtime Snapshot Was Written To Tracked Evidence

`--update-local-snapshot` updated:

```text
z8_11-evidence/runtime_convergence_snapshot.json
```

That file is historical evidence and is tracked by Git. Updating it after deploy created a dirty workspace even when convergence was successful.

Resolution:

- operational snapshot path moved to `.v7/runtime_convergence_snapshot.json`;
- `.v7/` is ignored by Git;
- historical evidence remains available as seed snapshot.

## Finding 3: Operator Needed One Owner Command

Before CONV.3, the operator had to interpret multiple commands:

- `git status`
- `tools/v7-truth-check --all`
- `tools/v7-convergence-status --json`
- deploy output
- push output

Resolution:

- `tools/v7-convergence-owner` provides a single status and next required action.

