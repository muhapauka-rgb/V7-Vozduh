# E32.4.B Production Pool Compatibility

production_pool_compatible=true

## Capacity Program Compatibility

Concurrency operations preserve capacity gates:

- CAPACITY_RESERVATION prevents double-spending certified capacity;
- reservation conflicts deny forward movement;
- stale reservations deny forward movement;
- target overcommit remains impossible if reservation ledger is atomic;
- rollback remains allowed for exact known scope.

## Execution Batches Compatibility

Concurrency operations preserve batch lifecycle:

- BATCH_LOCK serializes state transitions;
- owner transfer records scheduler and executor handoffs;
- PACKET_LOCK protects packet consumption;
- USER_LOCKS preserve blast radius;
- failure modes map to FAILED_CLOSED, REPLAY_DENIED, CANCELLED, or rollback states.

## Policy Engine Compatibility

Concurrency operations preserve policy boundaries:

- policy_is_authority=false;
- policy_is_runtime_mutation=false;
- policy_is_admission_logic=true;
- policy decisions may deny, allow, require review, or require additional gates;
- policy cannot acquire runtime lock ownership.

## Scheduler Compatibility

Scheduler may:

- request reservations;
- hold scheduler-owned batch locks during scheduling windows;
- transfer ownership to executor with audit proof;
- release reservations on cancellation or expiry.

Scheduler may not:

- bypass packet consumption;
- bypass execution-time recheck;
- execute with stale locks;
- move users outside batch scope.

## Production Pool Compatibility

The operations model supports production-pool needs:

- concurrent batch admission;
- capacity reservation ledger;
- scheduler/operator conflict handling;
- stale lock recovery;
- owner transfer auditability;
- fail-closed conflict handling;
- operator observability for blocked resources.

production_pool_compatible=true
