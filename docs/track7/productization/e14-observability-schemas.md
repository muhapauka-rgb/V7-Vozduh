# E14 Observability Schemas

## Purpose

Observability objects normalize runtime truth into stable read models. They
support overview, target pool, evidence viewer, timelines, and delayed movement
monitoring without exposing raw logs as the primary interface.

## Common Observability Envelope

```json
{
  "required": [
    "schema_version",
    "object_type",
    "object_id",
    "collected_at",
    "state_source",
    "freshness",
    "source_refs",
    "operator_summary"
  ],
  "properties": {
    "schema_version": { "type": "string" },
    "object_type": { "type": "string" },
    "object_id": { "type": "string" },
    "collected_at": { "type": "string", "format": "date-time" },
    "state_source": { "enum": ["live", "copied_state", "simulation", "historical"] },
    "freshness": { "type": "object" },
    "source_refs": { "type": "array", "items": { "type": "string" } },
    "operator_summary": {
      "type": "object",
      "required": ["status", "headline", "safe_next_action"]
    }
  }
}
```

## 1. RuntimeSnapshot

Canonical fields:

- users registry hash;
- egress registry hash;
- users per egress;
- planner state id;
- apply state id;
- selected move set id;
- target readiness summary;
- restore-settle summary;
- barrier summary;
- generation governance summary;
- runtime health id;
- governance verdict id;
- execution allowed now.

Stale detection:

- registry hash drift;
- checker age above threshold;
- selected moves older than planner generation;
- unknown timer state.

## 2. TargetReadiness

Canonical fields:

- target id;
- protocol family;
- reserved flag;
- current users;
- soft limit;
- hard limit;
- readiness status;
- route class eligibility;
- service signal status;
- diagnose summary;
- blocker list;
- evidence refs.

Operator summary:

- `GO`, `CONDITIONAL`, `NO_GO`, or `STALE`.

## 3. RestoreSettleState

Canonical fields:

- gate status;
- sample count;
- required sample count;
- registry hash sequence;
- switch-history sequence;
- selected moves sequence;
- hidden mover sequence;
- runtime checker sequence;
- associated restore id;
- delayed monitoring required.

Invalidation:

- new switch-history row;
- registry hash drift;
- selected moves nonzero;
- hidden mover detected;
- sample window expired.

## 4. PlannerState

Canonical fields:

- timer state;
- service state;
- last planner run;
- planner generation id;
- output hash;
- selected move set id;
- candidate moves total;
- blocked reasons;
- source refs.

## 5. ApplyState

Canonical fields:

- timer state;
- service state;
- last apply run;
- apply generation id;
- last outcome;
- consumed approval id;
- manual apply observed;
- recompute observed;
- barrier behavior.

## 6. SelectedMoveSet

Canonical fields:

- selected move set id;
- planner generation id;
- selected moves count;
- candidate moves total;
- selected-move fingerprint;
- movement types;
- users;
- from targets;
- to targets;
- budget applied;
- blocked reasons;
- state source.

## 7. OperationTimeline

Canonical fields:

- operation id;
- operation type;
- phase;
- events;
- approvals;
- movements;
- restore ids;
- evidence refs;
- final verdict.

Event fields:

- event id;
- timestamp;
- actor/source;
- event type;
- state hash;
- generation id;
- mutation statement if present.

## 8. MovementLineage

Canonical fields:

- movement id;
- user id;
- from target;
- to target;
- reason;
- approval id;
- selected-move fingerprint;
- switch-history ref;
- route verification refs;
- rollback target;
- approved yes/no.

## 9. RestoreLineage

Canonical fields:

- restore id;
- source operation id;
- rollback/keep decision;
- planner restore event;
- restore-settle state id;
- apply restore event;
- restore barrier id;
- generation clearance id;
- delayed monitoring id;
- closeout verdict.

## 10. GenerationLineage

Canonical fields:

- planner generation id;
- apply generation id;
- restore generation id;
- token id;
- selected-move fingerprint;
- token status;
- token expiry;
- token consumed at;
- replay rejection events;
- mismatch reasons.

## 11. TargetPressureState

Canonical fields:

- target id;
- pressure type: service_signal, failover, rebalance, capacity, reservation;
- severity;
- affected users;
- candidate move count;
- selection outcome;
- blocked reasons;
- evidence refs.

Pressure is evidence only. It is not an approval.

## 12. DelayedMovementState

Canonical fields:

- monitor id;
- operation id;
- sample sequence;
- registry hash sequence;
- switch-history count sequence;
- selected moves sequence;
- hidden mover sequence;
- runtime health sequence;
- movement observed yes/no;
- closeout status.

## 13. RuntimeHealth

Canonical fields:

- reconcile status;
- route status;
- kill-switch status;
- provisioning reconcile status;
- system failed units summary;
- hidden mover scan;
- current blockers;
- confidence.

## 14. GovernanceVerdict

Canonical fields:

- verdict id;
- maturity status;
- execution allowed now;
- current blockers;
- safe next stage;
- latest authoritative report;
- remaining runtime blockers;
- operator action eligibility.

## Observability Verdict

These objects turn evidence into queryable truth while preserving source
lineage. Raw files remain audit material; operator screens consume normalized
objects.

