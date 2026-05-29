# E32.1.6 Certification History Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

certification_history_defined=true

## History Events

Operators need a timeline of:

- promotion;
- demotion;
- recertification;
- expiration;
- degradation;
- revocation;
- evidence refresh;
- policy cap change;
- confidence change.

## Event Fields

Each history event should include:

- timestamp;
- target id;
- previous class;
- new class;
- previous status;
- new status;
- previous confidence;
- new confidence;
- authority;
- reason;
- evidence links;
- registry hashes if available;
- audit ids or hashes if available.

## Promotion Display

Promotion must show:

- requested class;
- evidence passed;
- movement proof status;
- rollback proof status;
- replay proof status;
- authority accepting evidence.

## Demotion Display

Demotion must show:

- trigger;
- automatic or operator-reviewed;
- affected class;
- forward execution status;
- required recovery action.

## Recertification Display

Recertification must show:

- stale/degraded/expired reason;
- refresh method;
- evidence freshness;
- whether confidence changed.

