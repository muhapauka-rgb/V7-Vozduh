# P3.B Hook Observability Model

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Operator Questions

Hook observability must answer:

- What happened?
- What was observed?
- What would happen?
- Why?
- Which evidence supports it?
- How confident is the model?
- What would be needed to verify it?
- What rollback would look like if this were real?

## Admin Placement

Use existing `/admin-v2` surfaces. Do not add a new top-level section.

| Existing surface | Hook observability content |
| --- | --- |
| Execution Preview | Hook contract, decision, gates, simulations and verification plan. |
| Candidate Workflow | Candidate-specific hook decision and evidence lineage. |
| Approval Preview | Review/approval consequences without approval execution. |
| Governance Preview | Authority, policy, trust and audit explanation. |
| Rehearsal Preview | Would-happen narrative, blast radius and rollback simulation. |
| Checks | Freshness, health, capacity, required services and trust gates. |
| Logs | Source event refs and verification timeline. |

## Visible Fields

- Hook contract id.
- Trigger type.
- Decision.
- Confidence.
- Gate status.
- Blocking reasons.
- Freshness summary.
- Evidence refs.
- Simulation summary.
- Verification plan.
- Rollback simulation.
- Expiry/retention class.
- Safety flags.

## Forbidden UI Controls

- Execute.
- Apply.
- Route.
- Autoswitch apply.
- Move user.
- Write decision state.
- Register authoritative runtime hook.

## Observability Verdict

`hook_observability_defined=true`

