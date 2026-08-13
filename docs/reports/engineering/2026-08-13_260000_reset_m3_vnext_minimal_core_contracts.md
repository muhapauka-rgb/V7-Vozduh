# RESET-M3 vNext Architecture and Minimal Core Contracts Engineering Report

Status: `RESET_M3_VNEXT_POSITIVE_NEGATIVE_RECOVERY_AND_COMPLEXITY_CONTRACTS_ACCEPTED`

Intent closed: the future Core is specified before code as one compact five-stage contract under existing Runtime/policy/Authority/assignment/verifier owners. The new module is justified only as the isolated replacement boundary required to remove engineering-plane work from the synchronous routing lifecycle; it is not a new Program, Planner, scheduler, truth source or Authority owner.

## Positive contract

Input envelope `v7.routing-core-input.v1` contains immutable `generation`, `observed_at`, bounded freshness deadline, current assignments, health/capacity receipts, policy generation, Authority generation, operation/lease identity and exact scope. All identities are strings; cohorts are bounded and deterministically ordered.

1. `OBSERVE` validates schema, generation, identity and freshness and returns a normalized immutable receipt.
2. `STATE` validates one authoritative value per M2 fact and derives no historical/engineering state.
3. `PLAN` is pure and deterministic: eligible healthy targets with reserve are ranked by declared policy; output is only the minimal desired-assignment delta.
4. `APPLY` contract accepts current generation, operation id, idempotency key and fencing token; M4 shadow implementation emits no effect. Later effectful adapters must use the existing assignment/kernel writer.
5. `VERIFY` contract binds assignment, kernel visibility, exact user routing context, expected egress and payload result to the same operation/generation.

Mandatory gates: exact source/target identity, lawful target, capacity reserve, current policy/Authority generations, bounded scope, one active operation, CAS/fencing, idempotency, cooldown/anti-flap, circuit breaker/blast radius, rollback or forward-recovery readiness, route visibility and exact payload proof.

## Negative contract

Core must not read or execute OMP, CPS progression, Reports, Production Maturity, Learning, Replay, Polygon, historical incident reconciliation, campaign/certification history, full Matrix when a compatible fresh receipt exists, broad inventory refresh, Planner subprocess chains, expanded Outcome/closure objects or engineering scheduling. It cannot grant Authority, write policy, create users/targets, invent health/capacity, infer fresh truth from history or mutate during shadow mode.

## Recovery clock

Canonical end-to-end clock: `FIRST_QUALIFYING_FAILURE_EVIDENCE -> EXACT_CLIENT_NETWORK_CONTEXT_TARGET_PAYLOAD_RECOVERY`.

| Span | Initial hard budget |
| --- | ---: |
| failure receipt publication | 500 ms |
| input/state validation | 100 ms |
| deterministic plan | 100 ms |
| Authority/fencing/pre-apply validation | 200 ms |
| assignment/kernel apply | 1,000 ms |
| kernel visibility | 300 ms |
| exact-context payload verification | 800 ms |
| total initial production gate | `<3,000 ms` |

Prepared compatible warm-path target is `p95 <1,000 ms` end to end with a 1,500 ms hard ceiling. Lifecycle closure is separately measured and never substitutes for traffic recovery.

## Freshness decisions

Every health/capacity/policy/Authority/identity/membership/target receipt has owner, generation, `observed_at`, maximum age and invalidators. Exactly one result is legal: `USE_FRESH_PREPARED_RECEIPT`, `BOUNDED_SYNCHRONOUS_REVALIDATION`, `FALLBACK_TO_LEGACY`, or `STOP_SAFE`. Missing identity/policy/Authority/fencing is always `STOP_SAFE`; stale compatible health may use bounded existing-owner revalidation; unavailable Core or unsupported scope is `FALLBACK_TO_LEGACY`; no stale input triggers broad Core-side reconciliation.

## Single writer and crash recovery

Legacy remains sole production writer through M5. Shadow Core has `effects=ZERO`. Later ownership is scope-specific and atomic: a current generation plus operation id plus fencing token admits exactly one writer; stale Legacy/Core tokens reject before mutation. A compact apply receipt records intended delta, committed assignment/kernel identity and verification obligation. Restart reconciles receipt with assignment/kernel truth, then resumes verify, rollback or forward recovery and emits exactly one asynchronous closure obligation. `APPLY_SUCCEEDED_CLOSURE_LOST` is forbidden.

## Preserve/exclude and complexity budget

Preserve policy/Authority, assignment truth, health/capacity/freshness, cooldown/anti-flap, circuit breaker/blast radius, idempotency/fencing, rollback/forward recovery, route/payload verification and append-only outcome lineage. Exclude all engineering-plane surfaces named by the negative contract.

M3 baseline remains: 129,532 production Python/tool LOC in the audited scope; 17+ state surfaces; at least nine pre-apply hops; at least six pre-apply durable writes; 69 explicit subprocess/discovery sites; 58.761588 s observed lifecycle versus approximately 0.878 s mutation/visibility. M4 Core budget: one module, no process/timer/store/owner, zero effectful subprocesses, zero durable writes/locks/network calls in shadow planning, and a focused pure-contract test surface. Every later delta must reduce total active hot-path surface before completion.

Owner: existing `admin_core` Runtime model namespace, existing policy/Authority/assignment/verifier owners. Core earns effect Authority only through M4-M6 evidence.

Evidence: RESET Master Audit, RESET-M2 state-owner report and existing Reset Program contracts.

Residual: implement the effect-free pure Core, tests and shadow comparator within the accepted budget.

Exact successor: `EXECUTE_RESET_M4_EFFECT_FREE_SHADOW_CORE_IMPLEMENTATION_AND_GATES`.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.
