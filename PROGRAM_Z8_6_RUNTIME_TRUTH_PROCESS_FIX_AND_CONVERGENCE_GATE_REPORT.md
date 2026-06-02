# PROGRAM Z8.6 - Runtime Truth Process Fix And Convergence Gate Report

Project: V7 Vozduh
Date: 2026-06-02

## Executive Verdict

Z8.6 defines the permanent convergence process required before any Z9 retry.

This is a process-fix block, not a runtime action block. No deploy, git pull, git push, merge, runtime mutation, user movement, autoswitch apply, service restart, systemd modification, cleanup, rollback, or reconfiguration was performed.

The systemic failure is confirmed: local workspace, GitHub branch truth, local worktree truth, and production runtime truth are not converged.

## Phase 1 - Local Truth Map

### Local Copies / Worktrees

| Path | Branch | Commit | Remote | Status | Z7/Z8 operation wiring | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| `/Users/ponch/Documents/New project` | `Updatesystem` | `d61480dea6de67ea9d2cfd5c3440d93896076178` | `origin=https://github.com/muhapauka-rgb/V7-Vozduh.git` | dirty: modified `admin/v7-admin-api`, many untracked reports/evidence | present | `CURRENT_WORK` |
| `/private/tmp/v7-convergence-c` | `v7-next` | `c40cae13298594b7ad7040df4b19306c4e2c29d4` | same origin | dirty: untracked Z5/Z5.5 docs | absent in autoswitch/test marker scan | `STALE` |
| `/private/tmp/v7-vozduh-main` | detached in worktree record | `593619d494e215d11fd826086593527a4a555690` | unknown | prunable; path missing | unknown | `DO_NOT_TOUCH` |

### Latest Local Work

Latest Z7/Z8 operation-aware work is in:

```text
/Users/ponch/Documents/New project
branch=Updatesystem
commit=d61480dea6de67ea9d2cfd5c3440d93896076178
```

This copy contains:

- `operation_id`
- `operation_owner`
- `runtime_snapshot_hash`
- `finalize_operation`
- `runtime_operation_terminal`
- `closure_target`

### Stale Local Work

`/private/tmp/v7-convergence-c` is stale for Z7/Z8 operation wiring. It may still contain useful historical Z5 material, but it must not be used as the runtime-convergence source without explicit reconciliation.

### Copy Rules

| Copy | Action |
| --- | --- |
| `/Users/ponch/Documents/New project` | Keep as `CURRENT_WORK`; no production use until clean and pushed/approved |
| `/private/tmp/v7-convergence-c` | Archive candidate after preserving any unique docs; do not edit for new runtime work |
| `/private/tmp/v7-vozduh-main` | Prunable/missing; do not touch in this block |

## Phase 2 - GitHub Truth Map

GitHub repository:

```text
muhapauka-rgb/V7-Vozduh
default_branch=main
```

Read-only remote refs:

| Branch | Remote commit | Classification |
| --- | --- | --- |
| `main` | `593619d494e215d11fd826086593527a4a555690` | `STALE` for Z7/Z8 runtime orchestration |
| `v7-next` | `c40cae13298594b7ad7040df4b19306c4e2c29d4` | `STALE` for latest Z7/Z8 operation wiring |
| `Updatesystem` | `7c843545271e903b5017cac583b8571870f05629` | `PARTIAL`; behind local `Updatesystem` by one commit |
| `convergence/admin-api-2026-05` | `afcdd9cc61b7a1302c8785489991b0eac217b395` | `UNKNOWN`; convergence side branch |
| `codex/dynamic-load-autoswitch` | `0ea6d4ef82abaad26b0609d254bb6cf297db6432` | `UNKNOWN`; feature branch |
| `codex/integratsiya-tunelya` | `a0e689c67ef7d47e7f04e5c30e5430acd05752cb` | `UNKNOWN`; feature branch |

### Branch Authority Decision

Current latest code authority for Z7/Z8 work is local `Updatesystem@d61480d`.

GitHub authority is not converged because:

- GitHub default is `main`, but `main` is stale for Z7/Z8 operation wiring.
- `v7-next` exists but lacks latest operation wiring.
- remote `Updatesystem` exists but is one commit behind local.

### Required Non-Read-Only Future Decision

After this read-only block, a separate approved GitHub convergence action must choose one of these paths:

1. Promote `Updatesystem` as the canonical runtime-convergence branch.
2. Move the latest `Updatesystem` work onto `v7-next` and make `v7-next` canonical.
3. Create a new clearly named canonical branch, for example `runtime-convergence`, and retire both ambiguous paths from active use.

Z8.6 policy recommendation: make `Updatesystem` the immediate `CURRENT_WORK` source, then deliberately converge into a single canonical branch before production deployment. Do not keep both `Updatesystem` and `v7-next` as active runtime authority branches.

## Phase 3 - Production Access Fix Design

### Required Access Model

Codex must not receive broad interactive root access for routine truth validation.

Required model:

- bounded read-only command runner
- explicit allowlist
- no shell expansion beyond the approved command
- no write paths
- no service mutation
- no deploy commands
- no `--apply`
- auditable command output

### Minimum Read-Only Command Allowlist

```text
hostname
date -Is
pwd
ls -la /opt/v7
git -C /opt/v7 branch --show-current
git -C /opt/v7 rev-parse HEAD
git -C /opt/v7 status --short
sha256sum /usr/local/bin/v7-users-autoswitch
sha256sum /usr/local/bin/v7-audit-log
systemctl status v7-users-autoswitch.service --no-pager
systemctl status v7-users-autoswitch.timer --no-pager
test -x /usr/local/bin/v7-users-autoswitch
test -x /usr/local/bin/v7-audit-log
/usr/local/bin/v7-users-autoswitch --pretty
```

### Safer Implementation Options

Option A: restricted SSH forced command.

- Create a dedicated read-only audit user.
- Use `authorized_keys` forced command to call a server-side `v7-readonly-truth-audit` wrapper.
- Wrapper accepts only named subcommands from the allowlist.
- Wrapper must reject any argument containing shell metacharacters, `--apply`, `systemctl restart`, `systemctl enable`, `git pull`, `git checkout`, `git merge`, `git push`, `rm`, `cp`, `mv`, or redirection.

Option B: server-side static truth bundle endpoint.

- A root-owned timer writes a read-only JSON truth snapshot.
- Codex reads the JSON over HTTPS or SSH.
- Snapshot includes branch, commit, hashes, service states, state freshness, restore barrier state, audit path, closure path, and operation wiring markers.

Option C: manual operator paste.

- Operator runs the allowlisted command set on the server.
- Operator pastes outputs into Codex.
- Acceptable only as an interim bridge, not permanent automation.

### Production Read-Only Access Status

Defined: `true`

Ready now: `false`

Reason: current SSH access still fails non-interactively, and no bounded read-only runner is confirmed installed.

## Phase 4 - Permanent Convergence Gate

Every future live action must pass this gate before any execution planning.

### Gate Inputs

Repository:

- local path
- local branch
- local commit
- local `git status --short`
- local operation wiring markers

GitHub:

- canonical branch name
- canonical branch commit
- remote/default branch mismatch status

Runtime code:

- runtime root
- runtime branch
- runtime commit
- hash of `/usr/local/bin/v7-users-autoswitch`
- hash of `/usr/local/bin/v7-audit-log`
- hash or version marker for active `admin/v7-admin-api`
- operation envelope marker present
- audit wiring marker present

Runtime services:

- `v7-users-autoswitch.service` status
- `v7-users-autoswitch.timer` status
- last run timestamp/result
- service `ExecStart`

Runtime state:

- `/opt/v7/egress/state/users.registry` freshness/hash
- `/opt/v7/egress/state/egress.registry` freshness/hash
- restore barrier state
- audit path availability
- closure path availability
- operation lineage availability

### Gate Verdict Logic

If any required input is `UNKNOWN`, verdict is `STOP`.

If local canonical branch and GitHub canonical branch differ, verdict is `STOP`.

If GitHub canonical commit and runtime commit differ, verdict is `STOP`, unless a deployment manifest explicitly proves the deployed runtime commit and its approved divergence.

If binary hashes do not match the expected commit/build manifest, verdict is `STOP`.

If restore barrier is active or unreadable, verdict is `STOP`.

If audit path or closure path is missing/unreadable, verdict is `STOP`.

If service status or timer authority is unknown, verdict is `STOP`.

Only when every required field is known and aligned may a Z9 live-readiness attempt begin.

## Phase 5 - Single Source Of Truth Policy

### Development Workspace

Development happens in:

```text
/Users/ponch/Documents/New project
```

This path is `CURRENT_WORK`, not production authority.

### Canonical Branch

Temporary process decision:

```text
canonical_runtime_convergence_branch=Updatesystem
```

Reason: it contains the latest Z7/Z8 operation-aware work.

Permanent branch decision must be made in a separate GitHub convergence action: either keep `Updatesystem` as canonical or intentionally move the work to `v7-next`/new branch. Until then, `v7-next` must not be treated as current.

### Runtime Code Movement

Code must move to runtime only through an approved deployment step that records:

- source branch
- source commit
- artifact/binary hashes
- deployed runtime root
- deploy actor
- deploy time
- service status after deploy
- rollback material
- audit record

### Runtime State

Runtime state remains server-owned:

```text
/opt/v7/egress/state
/opt/v7/events
/opt/v7/audit
/opt/v7/admin
```

Local reports must never be treated as runtime state truth.

### Reports And Evidence

Reports/evidence should be stored under a predictable project path, preferably:

```text
docs/track7/runtime-convergence/<program>/
```

Root-level report sprawl should stop. Existing root-level reports are retained until a separate archive action is approved.

### Old Worktrees

Old worktrees must be inventoried and then archived only in a separate approved cleanup/archive block.

Current policy:

- do not edit `/private/tmp/v7-convergence-c` for new runtime work
- do not touch `/private/tmp/v7-vozduh-main` in this block
- do not remove anything without explicit archive approval

### How Codex Knows Current Branch / Path

Every runtime program must begin with:

```text
pwd
git branch --show-current
git rev-parse HEAD
git status --short
git worktree list --porcelain
git ls-remote origin <canonical refs>
```

This is mandatory before planning live actions.

## Phase 6 - Fix Plan

### Step 1 - Freeze Live Execution

Keep Z9 blocked until convergence is fixed.

### Step 2 - Choose Canonical Branch

Decision required:

- Prefer `Updatesystem` as immediate source of latest work.
- Decide whether `Updatesystem` remains canonical or is deliberately folded into `v7-next`.
- Do not use both as live-authority branches.

### Step 3 - Clean Current Workspace

Separate approved action:

- review `admin/v7-admin-api` uncommitted diff
- decide keep/commit/discard without losing user changes
- move root-level report sprawl into an agreed evidence/docs path or leave untouched
- do not delete anything during Z8.6

### Step 4 - Archive Stale Worktrees

Separate approved archive action:

- preserve unique Z5/Z5.5 docs from `/private/tmp/v7-convergence-c`
- mark `/private/tmp/v7-convergence-c` as stale
- remove/prune only after explicit approval
- record worktree archive evidence

### Step 5 - Configure Production Read-Only Access

Install or prepare one of:

- forced-command SSH read-only wrapper
- server truth snapshot endpoint
- interim operator-pasted command output process

Required output must include the allowlisted command results.

### Step 6 - Run Z8.5 Again

After read-only access is ready, rerun Z8.5 to prove:

- runtime truth known
- state truth known
- repository/runtime match known
- runtime/state match known
- operation wiring present on production
- runtime owner confirmed

### Step 7 - Retry Z9 Only After Z8.5 Passes

Z9 remains forbidden until:

- convergence gate passes
- restore barrier is known
- audit path is known
- closure path is known
- operation wiring is known on production
- one-user candidate is selected from fresh runtime truth

## Copy Classification Summary

| Copy | Classification | Keep | Sync | Archive | Do not touch |
| --- | --- | --- | --- | --- | --- |
| `/Users/ponch/Documents/New project` | `CURRENT_WORK` | yes | after branch decision | no | no |
| remote `Updatesystem` | `PARTIAL` | yes | needs local `d61480d` after approval | no | no |
| remote `v7-next` | `STALE` for operation wiring | maybe historical | only if chosen canonical | possible | no |
| remote `main` | `STALE` for operation wiring / default public branch | yes as public default until decision | maybe later | no | no |
| `/private/tmp/v7-convergence-c` | `STALE` | preserve unique docs | no new work | yes after approval | currently yes |
| `/private/tmp/v7-vozduh-main` | `UNKNOWN/DO_NOT_TOUCH` | unknown | no | possible prune later | yes |
| production runtime `/opt/v7` | `UNKNOWN` | yes | unknown | no | no mutation until truth known |
| `/usr/local/bin/v7-users-autoswitch` | `UNKNOWN runtime binary` | unknown | unknown | no | no mutation |
| `/usr/local/bin/v7-audit-log` | `UNKNOWN runtime binary` | unknown | unknown | no | no mutation |

## Final Verdicts

```text
local_truth_known=true
github_truth_known=true
runtime_access_plan_defined=true
production_readonly_access_ready=false
authoritative_branch_defined=true
authoritative_workspace_defined=true
stale_worktrees_identified=true
permanent_convergence_gate_defined=true
safe_to_fix_convergence=true
safe_to_retry_Z8_5=false
safe_to_retry_Z9=false
```

## Absolute Rule For Future Work

Do not attempt Z9 again until:

1. One canonical branch is selected and aligned.
2. Current workspace is clean or intentionally scoped.
3. Production read-only truth access is working.
4. Z8.5 rerun proves runtime and state truth.
5. Permanent convergence gate returns PASS.
