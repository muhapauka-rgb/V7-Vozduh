# V7 Hot-Path Fresh Obligation OMP Decoupling — Admission Report

**Mission:** `V7_HOT_PATH_FRESH_OBLIGATION_OMP_DECOUPLING_V1`  
**Verdict:** `READY_FOR_BOUNDED_IMPLEMENTATION`

## Admitted slice

Only the branch where `service_failure_obligation_from_advisory()` returns a
fresh, well-formed obligation is admitted. The existing executor receives that
object directly. It validates its identity, current scope, standing contract,
target and governed Packet/lease/barrier flow itself; it does not use the OMP
receipt as an input.

The implementation may move the existing OMP receipt consumer from before the
bounded executor to immediately after it, only for this fresh-obligation
branch. OMP remains exact-once Engineering/receipt consumption. It does not
move into the executor and no replacement is created.

## Explicitly preserved branches

| Branch | Required order | Reason |
| --- | --- | --- |
| Fresh advisory obligation | executor → OMP receipt | executor already owns the exact fresh obligation |
| No fresh obligation; receipt-bound handoff | OMP receipt → handoff → executor | existing receipt may be the owner-backed predecessor |
| Packet / lease / barrier / apply / verify | unchanged inside executor | safety boundary |
| Legacy cohort reconciliation | unchanged | current stop-safe re-entry |

## Implementation contract

1. No new function owner, queue, worker, truth source or state store.
2. Fresh obligation identity/scope passed to executor is byte-for-byte the
   existing value.
3. OMP receipt still runs once after the fresh executor attempt when it was
   previously eligible.
4. OMP failure after the attempt is reported as receipt failure; it cannot
   retroactively cancel or reinterpret the executor result.
5. Non-fresh receipt-bound handoff ordering remains identical.
6. Rollback is one commit revert.

## Validation contract

- unit proof of order for fresh and non-fresh branches;
- source compile and targeted service-failure tests;
- no change to Packet/lease/barrier arguments or routing calls;
- safe deploy and production hash verification;
- observation from event to executor start, without synthetic failure.

Runtime effect is limited to removing the OMP receipt wait from the fresh
execution order. Production routing and Authority effects are not claimed by
admission; they require implementation validation. CPS is unchanged.
