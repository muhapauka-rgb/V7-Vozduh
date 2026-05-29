# E32.1.6 Confidence Visibility Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

confidence_visibility_defined=true

## Confidence Levels

| Confidence | Display | Meaning | Inspectable Evidence |
| --- | --- | --- | --- |
| LOW | Low confidence | Static or incomplete evidence only. | Metadata review, partial checks. |
| MEDIUM | Validation confidence | Target-local and long-window validation passed. | Probe summary, long-window summary, readiness/restore-settle outputs. |
| HIGH | Execution confidence | Governed movement, rollback, replay, and audit proof passed. | Packet, forward proof, rollback proof, delayed monitoring, replay proof, audit chain. |
| VERY_HIGH | Production confidence | Repeated success plus certified production-pool controls. | Repeated cycles, scheduler/reservation/audit volume evidence. |

## Current Target

```text
target=amneziawg-exec-20260528-10-8-1-14
confidence=HIGH
reason=CLASS_10 governed execution, rollback, replay, delayed monitoring, and E31 certification passed
```

## Display Rules

- Show confidence separately from status.
- Do not render HIGH confidence as automatic eligibility.
- Show evidence links near the confidence label.
- Show confidence drop reasons when confidence changes.

## Operator Drill-Down

For HIGH confidence, operator should be able to inspect:

- certification report;
- approval packet id;
- movement proof;
- rollback proof;
- replay denial;
- audit hashes;
- validation summaries.

