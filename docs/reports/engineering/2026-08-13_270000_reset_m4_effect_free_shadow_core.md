# RESET-M4 Effect-Free Shadow Core Engineering Report

Status: `RESET_M4_EFFECT_FREE_SHADOW_CORE_FUNCTIONAL_AND_COMPLEXITY_GATES_PASS`

What changed: one new 220-LOC pure module, `admin_core/routing_core.py`, implements the accepted OBSERVE -> STATE -> PLAN -> shadow APPLY -> VERIFY contract. One 100-LOC focused test module covers determinism, immutability, stale input, fencing, Authority scope/blast, target eligibility, capacity and engineering-plane exclusion.

Intent closed: Core can produce a deterministic minimal desired-assignment delta from one generation-bound envelope while proving `effects=ZERO`. Legacy remains sole writer and the module has no file/network/process/lock/durable-state behavior.

Evidence:

- `python3 -m unittest tests.unit.test_routing_core`: 8/8 PASS.
- 1,000 in-process shadow runs: p50 0.0661 ms, p95 0.0688 ms, max 0.1128 ms; effects ZERO; stable two-move plan.
- static source check: no I/O, subprocess, lock, network or OS mutation imports/calls.
- deterministic fingerprint binds generation, policy generation, Authority generation, operation and desired delta.

Complexity BEFORE: no Core; audited 129,532 LOC; 17+ state surfaces; >=9 pre-apply hops; >=6 durable writes; 69 subprocess/discovery sites. AFTER M4 source: Core 220 LOC, one module, zero new process/timer/store/owner/state surface/subprocess/lock/durable write/network call. Runtime hot path delta = 0 because Shadow Core is not deployed or wired.

Risk closed: a future decision comparator can test Core logic without creating a second writer or allowing CPS/OMP/history/campaign inputs into routing decisions.

Owner: existing `admin_core` namespace; existing policy, Authority, assignment and verification owners remain authoritative.

Residual: compare Core and legacy decisions across replay/Polygon cases, classify every divergence, and consume the result without reproducing legacy defects.

Exact successor: `EXECUTE_RESET_M5_DECISION_EQUIVALENCE_AND_POLYGON_VALIDATION`.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.
