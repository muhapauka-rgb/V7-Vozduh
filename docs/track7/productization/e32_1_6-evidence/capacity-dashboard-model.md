# E32.1.6 Capacity Dashboard Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_dashboard_defined=true

## Dashboard Sections

### Target Summary

Purpose: identify what target the operator is looking at.

Fields:

- target id;
- protocol;
- interface;
- role;
- reservation owner;
- autoswitch allowed;
- rebalance allowed;
- production assignment allowed.

### Capacity Summary

Purpose: show the current capacity envelope.

Fields:

- capacity class;
- certified capacity;
- hard limit;
- active policy cap;
- effective batch cap;
- available capacity;
- current users;
- reserved capacity;
- max concurrent batches.

### Certification Summary

Purpose: show whether capacity is certified and usable.

Fields:

- capacity status;
- confidence;
- validation time;
- stale after;
- expiration;
- certification authority;
- evidence links.

### Validation Summary

Purpose: show latest validation health.

Fields:

- readiness status;
- restore-settle status;
- runtime checker status;
- last target-local validation summary;
- last long-window summary;
- last movement proof summary.

### Risk Summary

Purpose: show why the operator should or should not proceed.

Fields:

- active blockers;
- stale/degraded/expired reason;
- policy cap blockers;
- isolation blockers;
- rollback availability;
- next safe action.

## Operator Actions

Actions should be shown separately from metrics:

- `Prepare approval packet`
- `Run freshness refresh`
- `Run recertification`
- `View evidence`
- `View rollback manifest`
- `Escalate incident`

Actions must be disabled when governance gates fail.

## Display Rule

The dashboard must never show a single green state that hides a failing gate. It should expose each gate and the blocking reason.

