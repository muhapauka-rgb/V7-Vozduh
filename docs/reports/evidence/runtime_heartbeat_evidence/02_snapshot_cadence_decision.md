# Runtime Heartbeat Evidence 02 - Snapshot Cadence Decision

Two approaches were evaluated.

## Approach A: Standalone `v7-intelligence-snapshot-refresh.service/timer`

Pros:

- Clear snapshot owner.
- Refresh can happen outside planner.

Cons:

- Creates a second scheduler/heartbeat beside the active planner heartbeat.
- Requires new production systemd units.
- Violates the program preference to avoid a second heartbeat system unless unavoidable.
- Does not automatically couple planner decisions to a just-refreshed snapshot.

Verdict: rejected for this program.

## Approach B: Governed Pre-Planner Refresh Gate

Pros:

- Reuses the existing active planner heartbeat.
- Reuses the existing snapshot writer CLI.
- Does not create a second scheduler.
- Does not create a second truth source or snapshot root.
- Couples planner decision to refresh evidence in the same plan output.
- Can fail closed before selected moves or apply.

Cons:

- Must be timeout-bounded so planner remains lightweight.
- Must remain planner-only and forbidden with `--apply`.

Verdict: selected.

Final cadence decision:

```text
SNAPSHOT_CADENCE_DECISION=APPROACH_B
```

