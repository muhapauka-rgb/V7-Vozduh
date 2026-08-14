# PROGRAM Z8.7 - Canonical Source Of Truth Establishment Report

Project: V7 Vozduh
Date: 2026-06-02

## Executive Verdict

Z8.7 establishes the permanent source-of-truth protocol for V7 Vozduh.

No Z9 work was attempted. No production execution, certification, deployment, git pull, git push, merge, runtime mutation, service restart, systemd modification, cleanup, or rollback was performed.

## Primary Question

What must become the single permanent source of truth for V7 Vozduh?

Answer:

```text
AUTHORITATIVE_WORKSPACE=/Users/ponch/Documents/New project
AUTHORITATIVE_BRANCH=Updatesystem
AUTHORITATIVE_REMOTE=https://github.com/muhapauka-rgb/V7-Vozduh.git
AUTHORITATIVE_RUNTIME_ROOT=/opt/v7
AUTHORITATIVE_STATE_ROOT=/opt/v7/egress/state
```

Important nuance: `Updatesystem` is the immediate canonical branch because it currently contains the latest Z7/Z8 operation-aware work. A later approved GitHub convergence action may rename or fold it into another branch, but from this point forward there must be exactly one active runtime-authority branch.

## Evidence Folder

- `docs/reports/evidence/z8_7-evidence/00_discovery_inventory.md`
- `docs/reports/evidence/z8_7-evidence/01_duplication_audit.md`
- `docs/reports/evidence/z8_7-evidence/02_truth_manifest_design.md`
- `docs/reports/evidence/z8_7-evidence/03_convergence_gate_design.md`
- `docs/reports/evidence/z8_7-evidence/04_v7_truth_check_design.md`
- `docs/reports/evidence/z8_7-evidence/05_retirement_plan.md`
- `docs/reports/evidence/z8_7-evidence/06_future_rules.md`

## Phase 1 - Authoritative Workspace Decision

```text
AUTHORITATIVE_WORKSPACE=/Users/ponch/Documents/New project
```

Why:

- It is the current working repository.
- It is on `Updatesystem`.
- It contains latest Z7/Z8 operation-aware work at commit `d61480dea6de67ea9d2cfd5c3440d93896076178`.
- It contains operation wiring markers: `operation_id`, `operation_owner`, `runtime_snapshot_hash`, `finalize_operation`, `runtime_operation_terminal`, `closure_target`.

Rejected alternatives:

- `/private/tmp/v7-convergence-c`: branch `v7-next`, stale for operation wiring.
- `/private/tmp/v7-vozduh-main`: prunable/missing detached worktree.

## Phase 2 - Authoritative Branch Decision

```text
AUTHORITATIVE_BRANCH=Updatesystem
```

Why:

- Local `Updatesystem@d61480d` contains latest Z7/Z8 operation-aware work.
- Remote `Updatesystem@7c84354` is behind local by one commit.
- `v7-next@c40cae1` lacks the latest operation wiring markers.
- `main@593619d` is stale for runtime orchestration work.

Branch policy:

- `Updatesystem` survives as the immediate active canonical branch.
- `v7-next` is retired from active runtime authority unless an explicit future convergence action moves `Updatesystem` into it.
- `main` remains a public/default branch only until a governance decision changes it; it is not runtime authority.
- A new canonical branch is optional, but only if it replaces both `Updatesystem` and `v7-next` as the sole active runtime-authority branch.

## Phase 3 - Authoritative Runtime Root

```text
AUTHORITATIVE_RUNTIME_ROOT=/opt/v7
AUTHORITATIVE_STATE_ROOT=/opt/v7/egress/state
```

Expected runtime locations:

- runtime root: `/opt/v7`
- state root: `/opt/v7/egress/state`
- event root: `/opt/v7/events`
- audit root: `/opt/v7/audit`
- admin root: `/opt/v7/admin`
- release root: `/opt/v7/releases`
- current release: `/opt/v7/releases/current`
- deploy manifest: `/opt/v7/deploy-manifest.json`

Expected binary locations:

- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-audit-log`

Expected service locations:

- `/etc/systemd/system/v7-users-autoswitch.service`
- `/etc/systemd/system/v7-users-autoswitch.timer`

Runtime truth is still unknown until read-only production access is fixed.

## Phase 4 - Source Of Truth Manifest

Manifest design:

```text
V7_TRUTH_MANIFEST
```

Required fields:

- canonical workspace
- canonical branch
- canonical remote
- runtime root
- runtime release root
- current release link
- deploy manifest
- state root
- event root
- audit root
- admin root
- expected services
- expected binaries
- expected truth checks
- expected runtime checks
- unknown handling policy

Design target:

```text
docs/track7/runtime-convergence/V7_TRUTH_MANIFEST.json
```

No manifest file was implemented in Z8.7; this block is design only.

## Phase 5 - Permanent Convergence Gate

Gate:

```text
V7_PERMANENT_CONVERGENCE_GATE
```

Mandatory before:

- deploy
- runtime certification
- one-user execution
- rollback certification
- production certification
- operator approval
- Z9 retry

Verdict rule:

```text
Any UNKNOWN = NO-GO
Any branch mismatch = NO-GO
Any commit mismatch without approved deploy manifest = NO-GO
Any binary hash mismatch = NO-GO
Any unknown service status = NO-GO
Any unknown/active restore barrier = NO-GO
Any missing audit or closure availability = NO-GO
Otherwise PASS
```

## Phase 6 - v7-truth-check Design

Permanent command:

```text
v7-truth-check
```

Purpose:

- one command
- one verdict
- current workspace
- current branch
- current commit
- runtime branch
- runtime commit
- runtime status
- state status
- convergence status
- final PASS/FAIL

Modes:

```text
v7-truth-check --local
v7-truth-check --github
v7-truth-check --runtime-readonly
v7-truth-check --all
v7-truth-check --json
```

No implementation was created in Z8.7.

## Phase 7 - Retirement Plan

Active:

- `/Users/ponch/Documents/New project`
- local `Updatesystem`

Retire/archive candidates:

- `/private/tmp/v7-convergence-c`
- `/private/tmp/v7-vozduh-main`
- remote `v7-next` as runtime authority
- root-level report sprawl

Forbidden future behavior:

- edit stale worktrees as current
- use `v7-next` as current without reconciliation
- use `main` as runtime authority while latest work is elsewhere
- infer production truth from local reports

## Phase 8 - Future Project Rules

1. No live action without truth check.
2. No certification without convergence check.
3. No deployment without runtime manifest.
4. No branch may become active runtime authority without explicit designation.
5. Only one canonical branch may exist.
6. Unknown runtime truth is always NO-GO.
7. Runtime state is server-owned and cannot be inferred from local reports.
8. Reports are evidence, not runtime truth.
9. Worktrees must be inventoried before runtime work.
10. Stale worktrees may not receive new runtime changes.
11. `v7-truth-check` must run before Z8.5, Z9, deployment, rollback certification, and production certification.
12. The canonical branch must match GitHub before production deployment.
13. Runtime binary hashes must match an approved deploy manifest before execution.
14. Restore barrier unknown or active means STOP.
15. Audit and closure availability unknown means STOP.

## Final Verdicts

```text
authoritative_workspace_defined=true
authoritative_branch_defined=true
authoritative_runtime_root_defined=true
truth_manifest_defined=true
convergence_gate_defined=true
v7_truth_check_defined=true
retirement_plan_defined=true
future_rules_defined=true
safe_to_fix_convergence=true
safe_to_retry_Z8_5=false
```

## Next Allowed Work

The next allowed work is convergence fixing only:

1. Decide whether to keep `Updatesystem` as canonical or rename/fold it into one canonical branch.
2. Clean or intentionally scope the current workspace.
3. Configure bounded read-only production truth access.
4. Implement `V7_TRUTH_MANIFEST` and `v7-truth-check` in a separate approved implementation block.
5. Rerun Z8.5 only after the truth-check access exists.

Z9 remains blocked.
