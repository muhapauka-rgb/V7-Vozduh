# V7 Responsibility Subgraph Existing Discovery Owner Admission and Minimum Producer Decision

Status: `EXTEND_EXISTING_DISCOVERY_OWNER`

Date: `2026-09-04`

Mission: `V7_RESPONSIBILITY_SUBGRAPH_EXISTING_DISCOVERY_OWNER_ADMISSION_AND_MINIMUM_PRODUCER_DECISION`

## Scope and preserved frontier

This was a read-only owner/producer/consumer audit. The amended Mission rules
were applied: this report is its only new file; a review is valid only as an
immutable structured result consumed by the completion gate; `EXTEND` was a
falsifiable hypothesis, not a desired verdict; and no Runtime observation or
invocation was performed.

`docs/programs/V7_CURRENT_PROGRAM_STATE.md` remains unchanged. Its authoritative
frontier is `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`. CPS, OMP
frontier, Matrix, Planner, Authority, SYSTEM_MAP, Canonical Reference, Runtime,
production, deployment, routes and users were not changed.

## Prior stop-safe and exact distinction

The preceding Mission correctly returned
`STOP_SAFE_EXISTING_FUNCTION_GRAPH_PRODUCER_UNPROVEN`: the historical Appendix
has no current executable producer/caller/consumer chain. That does **not**
prove V7 lacks an existing owner that can own a minimal on-demand extension.

The reusable current owner is not Stage 2 itself. Stage 2 is
`LOCKED_KNOWLEDGE`; it defines Discovery Index rules but has no current
Function-Graph executor. The owner-compatible execution surface is the
existing OMP engineering-evidence/verification boundary:

`tools/v7_sync_lib.py` → `tools/v7-truth-check` → bounded read-only profile
→ immutable review → `mission_completion_evidence_gate`.

It is already a current OMP implementation surface, not a new coordinator,
graph owner, canonical knowledge owner, or Runtime owner.

## Candidate producer matrix

| Candidate | Current owner / entrypoint | Caller and consumer evidence | Subgraph coverage | Verdict |
| --- | --- | --- | --- | --- |
| Historical Function Graph Appendix | Historical Step 1C artifacts only. | No executable current producer, caller, validator or execution consumer. | Broad historical static index; stale scope. | `HISTORICAL_ONLY` |
| `.understand-anything/knowledge-graph.json` | Local generated analysis artifact; `autoUpdate=false`, last analysed 2026-08-14 at commit `18f8839`. | No repository caller or OMP/completion consumer found. | Nodes/edges only; stale against current `96260e3`. | `HISTORICAL_ONLY`, `NO_REAL_CONSUMER` |
| Stage 2 Knowledge / Discovery Index rules | Locked knowledge/program documentation. | Defines navigation, classification and non-canonical-use law; no executable generator. | Owner/relationship policy, not fresh source analysis. | `DOCUMENTATION_ONLY` |
| `python_function_call_sites` | `tools/v7_sync_lib.py::python_function_call_sites`. | Current source callers include `tools/v7-truth-check:1767` and three `v7_sync_lib.py` callers; test callers are separately labelled. | One named Python call target; no domain graph, state/systemd/deploy join, expiry or review binding. | `HELPER_ONLY` |
| Proactive verification discovery | `tools/v7_sync_lib.py::discover_proactive_verification_inputs`. | Existing OMP Engineering Polygon source/BDP chain and tests prove deterministic fingerprint/replay/consumer patterns. | AST scan of eligible unittest methods only. | `HELPER_ONLY`, reusable pattern |
| OMP completion/profile chain | `admit_execution_profile_contract`, `execution_profile_completion_binding`, `mission_completion_evidence_gate`, exposed through `tools/v7-truth-check`. | Existing machine-consumed completion gate; the bounded profile contract test passes. | Does not derive source structure. | `REAL_CONSUMER_ONLY`, reusable |
| Admin endpoint inventory | `tools/v7-admin-endpoint-inventory`. | Executable local CLI and contract tests; output is one admin API inventory. No OMP completion consumer found. | Endpoints, coarse state/command references for one file only. | `INSUFFICIENT_COVERAGE` |
| Runtime/package tools | `v7-runtime-repo-diff`, `v7-runtime-tool-enumerate`, infrastructure/readiness reviews. | Read-only operational/package tools; no subgraph completion consumer. | Runtime/deployment/systemd subsets, not functions/call graph. | `HELPER_ONLY` |
| Trust evidence inventory | `admin_core/autonomy_trust_acceleration.py` + `v7-autonomy-trust-evidence-inventory`. | Current read-only Runtime/evidence owner with explicit consumers. | Runtime/evidence maturity, not repository responsibility derivation; outside this Mission's no-observation scope. | `NOT_OWNER_COMPATIBLE` |
| BDP / AEP discovery documents | Existing program routes. | Can consume certified evidence through OMP, but do not produce fresh source-subgraphs. | Candidate/gap routing only. | `REAL_CONSUMER_ONLY` |

## Real caller and consumer proof

The current call-site helper scanned `201` files and found four non-test
callers of `program_execution_reconciliation`:

- `tools/v7-truth-check:1767`;
- `tools/v7_sync_lib.py:10913`;
- `tools/v7_sync_lib.py:21260`;
- `tools/v7_sync_lib.py:24631`.

It separately returned four `TEST_ONLY` callers. This proves the OMP
engineering-evidence boundary is executable and source-consumed, while also
proving why a test-only caller may not be promoted to a production/engineering
caller.

The future subgraph's lawful consumer is already present: an OMP-admitted
`GPT_DECISION_REVIEW` result binds its input/output fingerprint, independent
review, and `mission_completion_evidence_gate`. The profile contract's focused
test suite passed `16/16`; CPS SHA-256 remained
`e8412c5e944538be6e628088b589bc48f91bbb24d6f94f12f3fcf3c2409a953a`.

## Pilot-domain capability check

`ORDINARY_SERVICE_FAILURE_GOVERNED_RECOVERY_EXECUTION` is a valid future
validation target, not a derived result in this Mission. The proposed extension
can be domain-scoped from supplied entrypoints and trace across Matrix/health,
scope handoff, Planner/autoswitch, governed execution, Packet/Lease/Barrier,
operation control, route writers/Core-primary, verification/S11, outcome/OMP,
tests and static `systemd/` sources. Each non-static, shell, deployment,
dynamic-import, or unknown edge must remain `UNKNOWN` unless joined from an
existing official source. No live Runtime input is required for the first
read-only proof.

## Minimum producer design for the next Mission

| Contract item | Minimum lawful design |
| --- | --- |
| Owner | Existing OMP engineering-evidence / completion owner implemented in `tools/v7_sync_lib.py`; Stage 2 remains a source/owner-reference authority, not the executor. |
| Entrypoint | Add one on-demand read-only `tools/v7-truth-check` proof boundary that calls one bounded `v7_sync_lib` derivation helper. This is a new entrypoint under an existing owner, not a new owner. |
| Reused helpers | `python_function_call_sites` classification discipline; deterministic AST/discovery and corpus-fingerprint patterns from proactive verification; existing profile/result/review/completion binding. |
| Input | Mission/run/profile identity, `DOMAIN_ID`, bounded seed entrypoints, canonical owner/plane references, repository fingerprint, and explicit source paths. Deployment is `DEPLOYMENT_FINGERPRINT_UNAVAILABLE` unless an existing read-only evidence owner supplies it. |
| Output | In-memory structured `DERIVED_ENGINEERING_EVIDENCE` projection, `CANONICAL=false`, `DISCARDABLE=true`, `DECISION_AUTHORITY=NONE`, `RUNTIME_EFFECT=NONE`, `CPS_EFFECT=NONE`; no registry or standing file is required. |
| Validation | Deterministic schema, identity, freshness/expiry, repository fingerprint, domain scope, typed evidence class/status, and sorted subgraph fingerprint. |
| Review / completion | Existing `GPT_DECISION_REVIEW` plus immutable `ARCHITECTURE_REVIEW`; completion gate binds Mission/run/profile/input/repository/domain/subgraph/freshness/review fingerprints. |
| Anti-regrowth | The same on-demand producer accepts future BEFORE/CHANGE/AFTER inputs and deterministically emits structural delta plus bounded typed signals. No watcher or second mechanism. |
| Removal | Remove the one helper, one CLI branch and its tests; no state migration, Runtime rollback or CPS repair is needed. |

The expected source implementation surface is `tools/v7_sync_lib.py` plus the
existing `tools/v7-truth-check` CLI boundary. No new source owner is required.
A dedicated unit-test file is appropriate; it is a test surface, not an owner.
No generated graph needs persistence beyond the immutable Mission result and
compact report/evidence convention.

## What is still missing before Code Optimization

`PRODUCER_IMPLEMENTATION` only. The existing owner, read-only OMP/operator
boundary, profile/review/completion consumer, fingerprint discipline and
non-canonical law are present. The next Mission must implement and test one
domain-scoped derivation helper; it must not start Code Optimization, derive a
whole-repository permanent graph, call Runtime, or mutate CPS.

## Cost and security boundaries

The producer is bounded by supplied domain entrypoints and local source/systemd
paths; it must impose a deterministic call-expansion limit and report scanned
files, parsed AST files, edges, elapsed time and output bytes. It must never
treat comments, docs, logs, generated strings or repository content as Mission
or Authority instructions. It parses typed structural evidence only; profile
and completion contracts bind the authorized Mission and reject mismatched or
stale results.

## Verification and known quality blocker

- `tests.unit.test_omp_bounded_execution_profile`: `16/16 PASS`.
- A focused run of the pre-existing
  `tests.unit.test_omp_functional_footprint` returned `5 PASS / 4 FAIL`.
  It expects exactly three non-test callers but the current helper correctly
  observes four. Its negative tests also expect `NO-GO` where the current
  implementation returns `PASS`. This Mission did not alter that code or tests;
  the stale expectations are a separate quality reconciliation item and do not
  prove a responsibility-subgraph producer.
- No Runtime observation was invoked. No production/test/source/canonical file
  was changed by this Mission; this report is the only new file.

## Reviews

- Architecture: `PASS` — the existing OMP engineering-evidence owner is
  admitted for a later bounded extension; Stage 2 is not reopened, no graph
  owner/coordinator/frontier is added, and derived output will remain
  non-canonical.
- Quality: `PASS_WITH_EXISTING_TEST_DEBT` — candidate limitations, caller class,
  historical state and unknown edges are explicit; no helper was promoted to a
  ready producer.
- Security: `PASS` — future input is typed/untrusted structural data only; no
  Authority or Runtime capability is introduced.
- Self review: `PASS` — no producer, Code Optimization, refactor, deploy,
  Runtime observation, CPS effect or product effect was implemented.

## Exact next Mission and re-entry condition

`V7_EXISTING_DISCOVERY_OWNER_DOMAIN_RESPONSIBILITY_SUBGRAPH_PRODUCER_V1`

It may start only with the minimum contract above: one on-demand,
domain-scoped, non-canonical, expiring derivation under the existing OMP
engineering-evidence owner; exact profile/review/completion consumption; tests
for stale/mismatched identity, unknown-edge retention, cross-file scope,
anti-regrowth delta and no-CPS effect. Code Optimization remains inadmissible
until that producer result is actually consumed.
