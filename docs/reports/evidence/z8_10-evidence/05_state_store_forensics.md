# Z8.10 State Store Forensics

## Existing state roots

- `/opt/v7/egress/state`: exists
- `/opt/v7/audit`: exists
- `/opt/v7/events`: exists
- `/opt/v7/admin`: exists

Important existing files include:

- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/egress.registry`
- `/opt/v7/egress/state/v7-state.json`
- `/opt/v7/egress/state/summary.state`
- `/opt/v7/egress/state/egress-status.state`
- `/opt/v7/egress/state/autoswitch-safety.json`
- `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- `/opt/v7/audit/audit.jsonl`
- `/opt/v7/audit/operator-execution-audit.jsonl`
- `/opt/v7/audit/operator-runtime-governance-actions.jsonl`

## Missing operation/execution stores

The following Z7/Z8 operation stores were not found:

- `/opt/v7/egress/state/closure-records.jsonl`
- `/opt/v7/egress/state/execution-contracts.json`
- `/opt/v7/egress/state/execution-events.jsonl`
- `/opt/v7/egress/state/selected-moves.json`
- `/opt/v7/egress/state/autoswitch-selected-moves.json`

## Restore barrier

`/opt/v7/egress/state/autoswitch-restore-barrier.json` exists. Its state was inspected read-only in prior Z8.9/Z8.10 collection and remains known. No restore barrier mutation was performed.

## Verdict

State root is known. Audit path is available. Closure and execution store availability is false, which blocks Z9.

