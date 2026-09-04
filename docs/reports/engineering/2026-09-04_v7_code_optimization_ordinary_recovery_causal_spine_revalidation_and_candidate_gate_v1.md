# V7 Code Optimization — Ordinary Recovery Causal-Spine Revalidation and Candidate Gate V1

Date: `2026-09-04`
Mission: `V7_CODE_OPTIMIZATION_ORDINARY_RECOVERY_CAUSAL_SPINE_REVALIDATION_AND_CANDIDATE_GATE_V1`
Class: `READ_ONLY_ENGINEERING_EVIDENCE`; no CPS, Runtime, Authority, Packet, Lease, Barrier, route or user effect.

## Outcome

`EXISTING_OWNER_FOUND_DOMAIN_SPINE_REVALIDATION_REQUIRED`.

The existing durable owner is
`docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md`, V5.3
N0–N11.  It defines the current ordinary-recovery causal contract and exact
server-side S11 terminal; it is not necessary or lawful to create an Agent,
Coordinator, Agent Frontier, parallel causal graph, or new recovery owner.

The bounded Code Optimization audit has therefore been corrected to consume
that already-existing Program as a canonical input.  It now returns
`CANONICAL_DURABLE_CAUSAL_SPINE_REVALIDATED`, rather than falsely describing
the durable spine as absent.  It still returns `INSUFFICIENT_EVIDENCE` with
zero candidates: a durable contract and static source reachability do not
prove a current ordinary Runtime caller/consumer chain, fresh execution
receipt, all-member S11 terminal, or a semantic counterfactual.

## Current-state isolation

`docs/programs/V7_CURRENT_PROGRAM_STATE.md` remains the live volatile owner:

| CPS fact | Observed value |
| --- | --- |
| active Program | `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` |
| active scope | `V5_3_RECOVERY_LATENCY_SLO_FINAL_EXECUTION` |
| active frontier | `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE` |
| active mission state | `MISSION_ACTIVE` |
| current safe next action | normal V7 Runtime caller obtains one fresh failure-to-all-affected-required-service-S11 sample; first repair a measured generic residual |

No CPS bytes, runtime command, unit action, route writer, Packet, Lease,
Barrier, Authority record or user assignment was created or changed.

## Revalidated causal spine

| Spine segment | Existing owner / source | Evidence class | Result |
| --- | --- | --- | --- |
| first valid observation and `T0` | Program V5.3; Matrix is the sole `T0` writer | canonical durable | defined; Runtime occurrence not revalidated |
| affected scope and target readiness | existing Matrix / governed recovery roles | canonical durable + static source | defined; current live scope not observed |
| Authority → Planner → Candidate → Packet → Lease → Barrier → Apply | Program V5.3 and existing autoswitch materializer | canonical durable + static source | ordered contract present; no fresh identity-bound receipt |
| assignment and kernel route verification | existing autoswitch route verifier | static source | fail-closed implementation surface present; no execution observed |
| required profile service via exact moved-client context | existing Matrix verifier / S11 law | canonical durable + static source | exact S11 requirement present; no current S11 receipt |
| global terminal | `T_END =` last affected enabled identity reaches exact S11 | canonical durable | defined; all-member aggregation not observed |

The durable acceptance origin is exactly:

```text
health -> Matrix -> affected scope -> Authority -> Planner
-> Candidate -> Packet -> Lease -> Barrier -> Apply -> required-service S11
```

It requires `T_FIRST_VALID_FAILURE_OBSERVATION` through
`T_GLOBAL_ALL_AFFECTED_RECOVERED`, P95 `<= 7000 ms`, maximum `<= 8000 ms`.
It does not permit a generic target check to substitute for S11 or relabel
server-side S11 as client-side T11.

## Static path evidence and limits

- `systemd/v7-health.service` declares the persistent Matrix role and the
  role-based health loop. It is a deployment declaration, not evidence that a
  caller ran in this audit.
- `tools/v7-users-autoswitch` materializes the existing Packet/Lease/Barrier
  only from a signed current contract and selected plan, then applies existing
  route and required-service verification. These branches were read only.
- Per-user route verification and selected profile-service verification are
  explicitly separate: Matrix path evidence cannot replace the moved user's
  policy-table route binding.
- The fresh bounded responsibility subgraph was `PASS`: 34 nodes, 58 static
  edges, 439 unresolved references; generated
  `2026-09-04T09:57:12.716842+00:00`, expiring
  `2026-09-04T10:12:12.716842+00:00`.

The 439 unresolved references and the absence of a fresh normal-Runtime
receipt mean no file, function, process hop, lock, lease, state surface or
compatibility branch may be called redundant from this result.

## Existing-profile correction

`tools/v7_sync_lib.py` now adds the active Service Failure Program to the
existing Code Optimization canonical input list and revalidates six exact
durable markers: current architecture identity, V5.3 N0–N11,
first-observation clock, global recovery clock, S11 definition and the
Candidate→Packet→Lease→Barrier→Apply→S11 chain.

The audit preserves the legal zero-candidate terminal and now exposes the
actual missing facts instead of a false missing-spine claim:

```text
runtime_caller_consumer_and_s11_receipt_unproven
counterfactual_semantic_candidate_unproven
```

The corresponding unit test asserts this distinction.  This is an extension
of the existing read-only evidence producer only; it changes no recovery
owner, policy, Runtime behavior or admission state.

## Candidate gate and exact re-entry

`ranked_candidates=[]`; `selected_first_candidate=null`; no PHASE2 or cleanup
was opened.

The blocking evidence is one fresh, owner-produced ordinary recovery receipt
from the normal health caller, bound to the same incident and identities,
showing: first valid Matrix observation, canonical `T0`, current affected
scope, Authority/Planner consumption, Candidate/Packet/Lease/Barrier/Apply,
per-identity route evidence, required-service S11 for every affected member,
the last-member `T_END`, and the immutable latency clock.  It must be consumed
by the existing OMP/CPS path, not manufactured through Codex, a manual route
writer, injected target or user move.

Only after that receipt and one explicit counterfactual hypothesis may the
existing Code Optimization profile rank at most one
`ACTIVE_BUT_REDUNDANT_CANDIDATE` or `SUPERSEDED_CANDIDATE`.  Until then the
legal terminal is `INSUFFICIENT_EVIDENCE`.

## Review and validation

Architecture review: PASS for reuse of the current Program owner and strict
owner/state boundaries.
Evidence review: PASS for the durable-spine/static-source distinction and the
zero-candidate stop.
Safety self-check: PASS; no runtime or canonical mutation path was invoked.

These are local engineering reviews bound by the existing profile schema;
they do not claim independent external model review or production validation.

Validation passed:

```text
python3 -m unittest tests.unit.test_omp_code_optimization_profile
# 6 tests, OK

python3 tools/v7-truth-check --omp-code-optimization-profile-proof
# code_optimization_profile=PASS
# audit_terminal=INSUFFICIENT_EVIDENCE
# selected_candidate_count=0
# no_cps_effect=True
```
