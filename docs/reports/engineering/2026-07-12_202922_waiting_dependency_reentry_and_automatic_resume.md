# Waiting Dependency Reentry And Automatic Resume

Mission ID: `V7_OMP_WAITING_DEPENDENCY_REENTRY_AND_AUTOMATIC_RESUME_V1`  
Run nonce: `V7_OMP_REENTRY_V1_8C42A71D59EF`  
Started: `2026-07-12T20:29:22+0700`  
Mode: discovery, reuse validation, fail-closed certification  
Final verdict: `FUNDAMENTAL_ARCHITECTURE_BOUNDARY`

## Summary

V7 already preserves WAITING capabilities in the CPS dependency graph and requires a reentry condition. It also has deterministic READY-frontier calculation and fail-closed completion ordering. It does not have an existing event-to-OMP execution trigger that can wake the Codex OMP consumer after a `REAL_WORLD_LIMIT` program terminal.

The requested no-operator automatic resume cannot be implemented inside the permitted scope. Connecting a production evidence producer to Codex continuation would create a scheduler, watcher, event bridge, queue, or would turn a Runtime transaction owner into a Mission scheduler. Every such option is explicitly forbidden by this Mission and by the existing OMP Self-Continuation Contract.

No CPS, OMP, Runtime, routing, policy, authority, action-class, producer, consumer, or validator semantics were changed. No Candidate, packet, Authority request, production mutation, or deployment was performed.

## Existing Model

The existing owner-backed chain is:

```text
active Codex Continue OMP invocation
-> read CPS dependency graph
-> preserve WAITING capabilities
-> propagate BLOCKED_BY_DEPENDENCY
-> calculate READY frontier
-> continue while an executable frontier exists
-> stop at REAL_WORLD_LIMIT when the frontier is empty
```

Existing implementation evidence:

- OMP section 14.1 defines the execution consumer as the existing Codex OMP consumer.
- `admin_core/operator_execution_pipeline.py` is explicitly a transaction owner and must not become a Mission scheduler.
- `tools/v7_sync_lib.py::capability_dependency_consistency` validates graph state, reentry presence, execution prohibition, completion order, CPS projections, and READY-frontier continuation.
- `tools/v7_sync_lib.py::omp_self_continuation_consistency` prevents premature operator return while the current invocation has executable work.
- `tools/v7_sync_lib.py::atomic_reconcile_cps` has no production caller; its callers are tests only.
- Existing systemd services produce Runtime evidence but do not invoke CPS reconciliation or the Codex OMP consumer.
- Current production truth classifies the autoswitch scheduler as inactive approved manual mode.

## Waiting Capability Audit

| Capability | Current state | Existing reentry meaning | Current deterministic limitations | Blocked dependents |
| --- | --- | --- | --- | --- |
| `CAP-U02` | `WAITING_EXTERNAL_DEPENDENCY` | qualifying movement-protection production evidence | no structured dependency owner, generation, evidence identity, baseline fingerprint, or trigger-to-Codex path | `CAP-U09` |
| `CAP-U05` | `WAITING_EXTERNAL_DEPENDENCY` | qualifying rollback or certified no-rollback outcome | no structured baseline fingerprint or trigger-to-Codex path | `CAP-U02,U03,U08,U09,U10` |
| `CAP-U06` | `WAITING_EXTERNAL_DEPENDENCY` | qualifying recovered channel with service/quality windows | no structured evidence generation/freshness binding or trigger-to-Codex path | `CAP-U02,U03,U08,U09` |
| `CAP-U07` | `WAITING_EXTERNAL_DEPENDENCY` | new material governed outcomes consumed by Learning/B13 | accepted U01 evidence is preserved, but no external event can wake Codex after program terminal | `CAP-U04,U08,U09,U12,U17,U18,U22` |

All four capabilities can describe the semantic condition that may permit reevaluation. None can answer the complete executable question `what exact event invokes the existing continuation consumer after the external change?` without introducing a forbidden mechanism.

## Required Reentry Contract

The proposed structured fields are valid as a future contract shape but are insufficient by themselves:

```text
DEPENDENCY_TYPE
DEPENDENCY_OWNER
DEPENDENCY_FINGERPRINT
WAIT_START_STATE
EXPECTED_EXTERNAL_CHANGE
EVIDENCE_REQUIRED
REENTRY_CONDITION
NEXT_STATE
NEXT_CONSUMER
```

Materializing these fields in CPS would improve representation only. It would not create the missing invocation edge:

```text
external evidence producer
-> CPS reconciliation trigger
-> Codex OMP consumer wakeup
```

Claiming `AUTOMATIC_RESUME_SUPPORTED=TRUE` after a documentation/validator-only change would therefore be false certification.

## Reuse And Boundary Analysis

Reusable existing owners:

- evidence producers own fresh production observations;
- capability owners decide evidence sufficiency;
- CPS owns volatile capability state;
- OMP owns dependency lifecycle and continuation rules;
- Codex owns OMP Mission execution;
- `v7_sync_lib` owns source-governance validation.

Missing responsibility is not evidence evaluation. It is asynchronous activation of the Codex execution consumer after the consumer has terminated at a real-world boundary.

No existing owner is legally permitted to provide that activation:

- Runtime evidence producers cannot become Mission schedulers;
- `operator_execution_pipeline` cannot become a Mission scheduler;
- source validators do not monitor production state;
- CPS is state, not an active executor;
- OMP is a program contract, not a daemon;
- Codex cannot continue after its invocation ends without an external thread wakeup or scheduler.

Therefore this is not an `EXISTING_OWNER_EXTENSION` inside the allowed Mission scope. It is a proven execution-boundary requirement whose implementation would require explicit architecture/authority work outside this Mission.

## Safety Decision

The following requested assertions are not certifiable:

| Assertion | Result |
| --- | --- |
| `WAITING_HAS_REENTRY_CONTRACT` | `PARTIAL`; semantic conditions exist, executable trigger contract does not |
| `REAL_WORLD_LIMIT_IS_CAPABILITY_STATE` | `PASS` while another READY capability exists; remains program terminal when frontier is empty |
| `AUTOMATIC_RESUME_SUPPORTED` | `FALSE` after invocation termination |
| `MANUAL_CONTINUE_NOT_REQUIRED_FOR_REENTRY` | `FALSE` |
| `DEPENDENCY_GRAPH_PROTECTED` | `PASS` |
| `COMPLETION_ORDER_PROTECTED` | `PASS` |
| `PREMATURE_OPERATOR_RETURN` | `FALSE` for executable work in the active invocation; not applicable after a valid program terminal |

No manual READY override was introduced. Historical evidence remains non-reusable. Dependency fingerprints were not fabricated. Current WAITING state and the accepted CAP-U07 Learning chain remain unchanged.

## Verification

Focused tests:

```text
python3 -m unittest \
  tests.unit.test_omp_dependency_graph_completion_order \
  tests.unit.test_omp_self_continuation \
  tests.unit.test_cps_atomic_reconciliation

Ran 54 tests: PASS
```

Compile/import:

```text
PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m py_compile \
  tools/v7_sync_lib.py admin_core/operator_execution_pipeline.py

PASS
```

Current source-state validation before this report:

- CPS consistency: `PASS`
- dependency graph consistency: `PASS`
- completion order consistency: `PASS`
- self-continuation consistency: `PASS`
- local alignment: `PASS`
- Runtime alignment: `PASS`
- Post-delivery truth: `PASS`, `FULLY_ALIGNED`
- Post-delivery convergence: `PASS`, `ALIGNED`
- Local/GitHub evidence commit: `f31ae08852c5877819886d06143752e9f6c2c325`
- Runtime commit remains `f6313e4c8dd05e20dca5dbf2ec4af353a34c1e72`; the only delta is this Engineering Report, classified `DOCS_ONLY_MISMATCH`, `deployment_required=false`, Runtime `PASS`

Full regression:

```text
python3 -m unittest discover -s tests -q

880 tests: PASS
```

The suite emitted the existing `DeprecationWarning: invalid escape sequence \\d` from the embedded admin API HTML; it produced no test failure.

## Final Output

```text
MISSION_ID = V7_OMP_WAITING_DEPENDENCY_REENTRY_AND_AUTOMATIC_RESUME_V1
RUN_NONCE = V7_OMP_REENTRY_V1_8C42A71D59EF
WAITING_CAPABILITIES = CAP-U02,CAP-U05,CAP-U06,CAP-U07
REENTRY_CONTRACTS = PARTIAL_SEMANTIC_ONLY
DEPENDENCY_GRAPH_VERSION = v7.omp-capability-dependency-graph.v1
READY_FRONTIER_BEFORE = NONE
READY_FRONTIER_AFTER = NONE
AUTOMATIC_REENTRY_SUPPORTED = FALSE
MANUAL_RESUME_REQUIRED = TRUE
CAP_U02_STATE = WAITING_EXTERNAL_DEPENDENCY
CAP_U05_STATE = WAITING_EXTERNAL_DEPENDENCY
CAP_U06_STATE = WAITING_EXTERNAL_DEPENDENCY
CAP_U07_STATE = WAITING_EXTERNAL_DEPENDENCY
TARGETED_TESTS = 54_PASS
FULL_TESTS = 880_PASS
DEPLOY_ID = NONE
TRUTH_RESULT = PASS_FULLY_ALIGNED
CONVERGENCE_RESULT = PASS_ALIGNED_DOCS_ONLY_RUNTIME_DELTA
NEXT_OMP_ACTION = EXPLICITLY_DECIDE_WHETHER_AN_EXTERNAL_CODEX_WAKEUP_OWNER_IS_ALLOWED; DO_NOT_ADD_ONE_IMPLICITLY
FINAL_VERDICT = FUNDAMENTAL_ARCHITECTURE_BOUNDARY
```
