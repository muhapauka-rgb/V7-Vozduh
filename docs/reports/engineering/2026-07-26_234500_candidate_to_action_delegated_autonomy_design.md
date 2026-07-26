# Candidate-to-action delegated autonomy design

Дата: 2026-07-26
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Current truth

CPS уже фиксирует для `single-user governed candidate failover`:

- `DELEGATED_AUTONOMY_POLICY=APPROVED`;
- `CANDIDATE_APPROVAL_REQUIRED=NO`;
- `PACKET_APPROVAL_REQUIRED=NO`;
- scope `max_users=1`, `max_concurrent_transactions=1`;
- fresh Candidate/Packet and all live gates mandatory.

Но действующий policy `dap_default_tier1_readonly` не даёт Runtime mutation.
Поэтому подготовительная цепочка может идти автоматически, а фактическое
перемещение продолжает останавливаться на Operational Authority boundary.

## Target behavior

Один независимый Authority decision создаёт standing delegated operational
contract только для существующего Action Class. После этого каждый новый
owner-backed Candidate автоматически проходит:

`Situation -> Decision Trace -> Candidate -> M5b -> Packet -> lease ->`
`policy-derived one-use operational token -> restore barrier -> bounded apply ->`
`verification -> rollback/no-rollback -> Outcome -> Learning -> OMP/CPS -> next event`.

Ручное подтверждение Candidate, Packet или их hash не требуется.

## Mandatory envelope

- action class: `single-user governed candidate failover`;
- source must be currently ineligible by fresh service evidence;
- target must be healthy, service-suitable and within capacity;
- exact one user; one concurrent transaction;
- current incident, Situation, Decision, source/snapshot generation;
- fresh Packet and lease only;
- cooldown and anti-flap mandatory;
- restore barrier, immediate verification and temporal observation mandatory;
- verifier-triggered rollback/containment mandatory;
- token is exact-once and cannot be reused after success, failure or interruption;
- no Authority self-expansion and no Production Maturity self-promotion.

## Automatic versus external terminals

Automatically execute only inside the standing envelope. Stop for independent
Authority when any of these changes: more than one user, wider concurrency,
new action class, deliberate production degradation, source/target family not
covered by policy, missing rollback/verification, unknown evidence, policy
expiry/revocation, or requested Authority/Production Maturity expansion.

## Implementation frontier

First close `V7_SERVICE_FAILURE_M5A_M5B_ATOMIC_HANDOFF_LIVENESS_REPAIR_V1`.
Then activate a separate bounded Mission
`V7_SINGLE_USER_SERVICE_FAILURE_STANDING_DELEGATED_OPERATIONAL_POLICY_V1`.
It must extend the existing policy, operator-execution, autoswitch, Packet,
lease, restore-barrier, verification, Outcome, Learning, OMP and CPS owners;
no new watcher, queue, planner, Runtime, registry or Authority owner is allowed.
