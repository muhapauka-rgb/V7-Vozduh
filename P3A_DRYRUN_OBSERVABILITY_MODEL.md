# P3.A Dry-Run Observability Model

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Operator Visibility

Dry-run observability should make decisions explainable without creating action controls.

## Recommended Admin Placement

Use existing `/admin-v2` sections only.

| Existing area | Dry-run presentation |
| --- | --- |
| Execution | Dry-run contract preview, decision, gates, simulations and verification status. |
| Approval Center | Approval-related dry-run evidence and lineage. |
| Governance Preview | Authority, trust, policy and audit explanation. |
| Rehearsal Preview | Outcome, blast radius, service impact and rollback preview. |
| Checks | Runtime health, service matrix and freshness gates. |
| Logs | Source event references and verification timeline. |

No new top-level navigation section is required.

## Visible Fields

- Decision value.
- Gate status.
- Blocking reasons.
- Evidence references.
- Source freshness.
- Simulation summary.
- Verification state.
- Rollback readiness.
- Retention/expiry state.
- Safety flags.

## Hidden Or Excluded Fields

- Secrets.
- Raw credentials.
- Full private traces.
- Action-capable command lines.
- Apply, execute, move, route or autoswitch buttons.
- Hook registration controls.

## Observability Flags

Every view must show or expose:

- `preview_only=true`
- `non_authoritative=true`
- `execution_allowed_now=false`
- `runtime_hooks_implemented=false`

## Observability Verdict

`dryrun_observability_defined=true`

