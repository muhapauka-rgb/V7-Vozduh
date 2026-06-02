# Z8.12 Runtime Impact Model

## Categories

| Category | Paths | Impact | Gate |
| --- | --- | --- | --- |
| Runtime Critical | `admin/`, `tools/`, `runtime/`, `systemd/`, deployment paths, systemd unit suffixes, truth manifest | Can affect runtime, deployment, execution, rollback, or truth | FAIL |
| Runtime Relevant | `tests/`, `fixtures/` | Can affect validation confidence but not production runtime directly | WARN |
| Documentation Only | `docs/`, generated `*_REPORT.md`, `PROGRAM_*.md`, `*-evidence`, `*_evidence`, `evidence` paths, `.md`, `.txt` | Does not affect runtime execution | INFO |
| Unknown | Any unclassified dirty path | Unknown impact | FAIL |

## Fail-closed preservation

Runtime critical and unknown paths still produce `dirty_workspace` and a specific blocker:

- `runtime_critical_dirty`
- `unknown_dirty`

Documentation-only paths produce `documentation_dirty_ignored` warning and do not block.

Runtime-relevant paths produce `runtime_relevant_dirty` warning and do not block by themselves.

