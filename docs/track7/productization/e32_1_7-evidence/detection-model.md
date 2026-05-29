# E32.1.7 Detection Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

detection_model_defined=true

## Detection Matrix

| Failure Mode | Detection Source | Source Of Truth | Detection Type | Confidence |
| --- | --- | --- | --- | --- |
| CAPACITY_STALE | Clock vs `capacity_stale_after` | Capacity metadata | Automatic | High |
| CAPACITY_DEGRADED | Readiness, restore-settle, runtime checkers, quality samples | Helpers/checkers | Automatic plus operator review | High when helper-backed |
| CAPACITY_EXPIRED | Clock vs `capacity_expiration`, schema/profile diff | Capacity metadata and target metadata | Automatic | High |
| CAPACITY_REVOKED | Audit/replay/rollback/blast-radius validation | Audit and governance review | Manual or automatic trigger plus human review | High after review |
| CAPACITY_UNKNOWN | Missing or unparsable metadata | Capacity view model | Automatic | High |
| CAPACITY_CONFLICT | Cross-field consistency checks | Metadata plus evidence references | Automatic plus human review | High |
| CAPACITY_EVIDENCE_MISSING | Evidence path/hash validation | Evidence store | Automatic | High |
| CAPACITY_CONFIDENCE_DROP | Confidence recomputation, incidents, repeated failures | Certification lifecycle | Automatic signal plus authority decision | Medium to high |
| CAPACITY_POLICY_CAP_EXCEEDED | Requested movement vs active policy cap | Policy engine or policy config | Automatic | High |
| CAPACITY_RESERVATION_CONFLICT | Reservation ledger, active packets, audit | Reservation ledger | Automatic plus human review on disagreement | Medium until ledger is certified |

## Detection Sources

Primary sources:

- capacity metadata;
- generated capacity view model;
- readiness helper;
- restore-settle helper;
- runtime checkers;
- evidence store;
- audit store;
- policy cap source;
- future reservation ledger.

## Confidence Rule

Automatic detection may demote or block execution. Promotion or restoration to CERTIFIED requires authority acceptance, not automatic inference alone.

