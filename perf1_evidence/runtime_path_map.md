# PERF.1 Runtime Path Map

## Planner Path

Owner: `tools/v7-users-autoswitch`

Inputs:

- state JSON files
- policy JSON files
- safety state
- service matrix summary
- quality summary
- client speed summary
- users and egress registries
- restore barrier
- bounded switch history
- RI advisory result

Commands:

- none in normal `plan()` path

Network probes:

- none in normal `plan()` path

Estimated latency:

- target: under 250 ms for 2000 users when reading compact summaries
- current risk: scales with active user decision loop and any in-process RI advisory expansion

Classification:

- Fast Runtime candidate if it reads compact summaries only.

## Execution Path

Owner: `AutoswitchPlanner.apply()`

Inputs:

- selected moves from plan
- operation id/hash
- verification flags

Commands:

- user switch command per selected move
- optional route verification command
- optional rollback switch command

Network probes:

- none expected directly; route verification may depend on kernel route checks

Estimated latency:

- target: under 2 seconds per selected user excluding external command delays
- bounded by blast radius and selected move cap

Classification:

- Runtime action path; must never run Heavy Brain calculations.

## Governance Path

Owner: operator/governance flow

Inputs:

- operation packet
- selected move hash/count
- runtime snapshot hash
- restore barrier state

Commands:

- governance validation tools where explicitly invoked

Estimated latency:

- target: under 150 ms for local packet validation if summaries are precomputed

Classification:

- Fast validation path; should consume packet metadata and snapshots.

## Rollback Path

Owner: `AutoswitchPlanner` rollback model and runtime rollback tools

Inputs:

- source operation
- selected move hash
- rollback packet
- current route state

Commands:

- switch back per rollback row
- post-rollback verification

Estimated latency:

- target: under 2 seconds per rollback user excluding command delays

Classification:

- Emergency path; no history scans, no service intelligence, no network matrix tests.

## Audit Path

Owner: `v7-audit-log` plus audit/event stores

Inputs:

- terminal operation metadata
- selected move hash/count
- rollback verdict

Commands:

- `v7-audit-log` only on apply terminal emission

Estimated latency:

- target: under 100 ms append path

Classification:

- Append-only terminal record; aggregation must be background.

## Closure Path

Owner: `admin/v7-admin-api` and `admin_core/operator_observability.py`

Inputs:

- audit status
- operation id
- terminal state

Estimated latency:

- target: under 100 ms for closure state read

Classification:

- Fast read/record path; no large audit scan during runtime.
