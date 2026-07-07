# V7 Diagnosis Implementation Acceptance

Status: CANONICAL_ACCEPTANCE_CONTRACT

Domain: 11 — Diagnosis

Target Contract: `docs/reference/V7_DIAGNOSIS_RECORD_CONTRACT.md`

Target Schema: `v7.diagnosis-owner-resolution.v1`

Date: 2026-07-07

## 1. Purpose

This document is the official engineering acceptance authority for the Domain 11 Diagnosis implementation.

It does not define architecture. It does not provide a coding plan. It does not authorize production mutation. It decides whether the implementation of the executable read-only Diagnosis / Owner Resolution Record is complete.

Domain 11 is accepted only when every criterion in this document passes. There is no partial acceptance.

## 2. Acceptance Inputs

Acceptance must use these inputs:

- `docs/reports/research/V7_STAGE1_DIAGNOSIS_RECOVERY_DISCOVERY.md`
- `docs/reference/V7_DIAGNOSIS_RECORD_CONTRACT.md`
- Domain 11 certification in `docs/reports/research/V7_PHASE1_DOMAIN_CERTIFICATION.md`
- Function Graph Appendix and Function Graph JSON
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`
- relevant Engineering Reports and implementation evidence produced by the implementation mission

Acceptance must verify persisted implementation reality. It must not accept intent, TODOs, narrative-only reports, or unexecuted plans.

## 3. Acceptance Model

Acceptance sequence:

```text
Implementation Evidence
  -> Contract Compliance
  -> Test Acceptance
  -> Consumer Acceptance
  -> Regression Protection
  -> Domain 11 Certification Gate
```

Allowed final outcomes:

- `PASS`
- `FAIL`

`PASS` means Domain 11 implementation is complete and ready for recertification as `CERTIFIED`.

`FAIL` means at least one blocking criterion failed. The acceptance report must identify the smallest corrective action.

## 4. Acceptance Criteria

Every acceptance item below is mandatory.

| Acceptance item | Requirement | Reason | Expected Behaviour | Verification Method | Evidence Required | Pass Condition | Fail Condition | Blocking Severity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Diagnosis Record Producer | A concrete existing owner produces a Diagnosis Record. | Domain 11 failed because no executable diagnosis projection existed. | Producer emits a JSON-compatible record with schema `v7.diagnosis-owner-resolution.v1`. | Inspect code, run unit/contract tests, inspect Function Graph after implementation. | Function path, test output, sample record. | Existing owner produces record deterministically. | No producer, manual-only output, or producer is a new owner. | BLOCKING |
| Diagnosis Record Schema | Record matches `V7_DIAGNOSIS_RECORD_CONTRACT.md`. | Consumers require stable fields. | All required fields exist and enums are valid. | Contract validator or unit assertions. | Valid sample record and failing negative fixtures. | Schema validation passes. | Missing required field, wrong schema version, invalid enum. | BLOCKING |
| Evidence Consumption | Producer consumes existing evidence, blockers, reports, and owner maps without recomputing Planner/Runtime decisions. | Diagnosis is a read-only projection over existing truth sources. | Record points back to source evidence. | Test fixtures and code review. | Evidence input fixtures and output record. | Inputs are existing artifacts; no new truth source. | Synthetic evidence, hidden recomputation, missing source identity. | BLOCKING |
| Evidence References | Every claim has evidence refs. | Detection is not diagnosis; claims need proof. | `evidence_refs` is non-empty for `PROVEN` diagnosis. | Contract tests. | Records with evidence refs; negative tests without refs. | Proven claims include refs. | Root cause or terminal classification without refs. | BLOCKING |
| Root Cause Rules | Root cause is claimed only when proven. | Prevents symptom/blocker from becoming false cause. | `root_cause_proven=false` unless direct evidence supports root cause. | Unit and negative tests. | Proven and unknown fixtures. | Unknown stays unknown; proven cause has evidence. | Guessing root cause or treating blocker label as root cause. | BLOCKING |
| Unknown Rules | Unknown, missing, stale, or conflicting evidence is preserved. | Unknown is not pass and not fail. | `unknown_state` reflects missing/stale/conflicting evidence. | Unknown-state tests. | Missing/stale/conflicting evidence fixtures. | Unknown cases do not become pass/fail/root cause. | Unknown masked as root cause or success. | BLOCKING |
| Owner Resolution Rules | Blocking owner is classified or marked required/unknown. | Owner block is not terminal explanation. | Record includes `blocking_owner`, `owner_resolution_state`, `terminal_classification`, `required_resolution`. | Owner Resolution tests. | Fixtures for every terminal state. | Every owner block has valid owner-resolution state. | `BLOCKED`, `STOP_SAFE`, or `BLOCKED_BY_SAFETY_OWNER` accepted as final. | BLOCKING |
| Terminal Classification Rules | Terminal classification uses only canonical states. | Keeps OMP and CPS behavior deterministic. | Allowed values: `POLICY_PROHIBITION`, `IMPLEMENTATION_MISSING`, `OWNER_INVOCATION_MISSING`, `IMPLEMENTATION_DEFECT`, `CANONICAL_IMPOSSIBILITY`, plus `NONE`/`UNKNOWN` where applicable. | Contract tests. | Positive and negative enum fixtures. | Only allowed values appear. | Any non-canonical terminal classification appears. | BLOCKING |
| First Divergence Rules | First divergence is present only when proven. | Prevents fake forensic precision. | `first_divergence` includes producer, consumer, field, before/after, evidence ref when known; otherwise `UNKNOWN` or omitted. | Unit/fixture tests. | Proven divergence and no-divergence fixtures. | Proven divergence is evidence-backed; unknown remains unknown. | Divergence invented or missing evidence ref. | HIGH |
| Mutation Boundary | Record and producer are read-only. | Diagnosis must not become Runtime or Authority. | No Runtime apply, no Planner mutation, no Authority expansion, no Restore Barrier write, no user movement, no synthetic evidence. | Static inspection, tests, Function Graph, no-mutation assertions. | Code paths, Function Graph node status, test output. | All mutation flags false and no mutation calls reachable. | Any mutation path or authority expansion is reachable. | BLOCKING |
| Existing Owners Reused | Implementation uses existing owners. | Existing Owner Before New Owner. | Expected owner is Engineering Automation / OMP read-only path, with optional governance projection. | Code and Function Graph review. | Owner path and no-new-owner evidence. | No new owner/service/database/execution flow. | New owner introduced without explicit architecture approval. | BLOCKING |
| Consumer Contract | Consumers read the record without reinterpretation. | Diagnosis Record is canonical projection. | OMP, CPS, Production Maturity, Engineering Reports, Engineering Automation, Governance Check, Future Certification consume record fields. | Consumer contract tests and projection inspection. | Consumer outputs referencing same record. | Consumers synchronize from same record. | Consumer invents conflicting diagnosis truth. | BLOCKING |
| OMP Consumption | OMP can turn `required_resolution` into next engineering mission. | OMP owns continuation. | OMP uses terminal classification and required resolution from record. | Consumer test or evidence report. | OMP projection or fixture. | OMP consumption passes. | OMP cannot consume record or ignores terminal classification. | BLOCKING |
| Current Program State Consumption | CPS can project current blocker/root-cause fields from the record. | CPS must expose current truth without manual drift. | CPS fields map to `blocking_owner`, `owner_resolution_state`, `terminal_classification`, `required_resolution`. | Consumer test or projection evidence. | CPS projection sample. | CPS reads same record. | CPS maintains conflicting manual-only state. | HIGH |
| Production Maturity Consumption | Production Maturity consumes record as evidence, not permission. | Maturity consumes capability evidence; it is not Authority. | PM records maturity/blocker evidence without granting action. | Consumer test or report evidence. | PM evidence sample. | PM consumption does not authorize mutation. | PM treats diagnosis as authority. | BLOCKING |
| Engineering Reports Consumption | Reports embed or reference the record. | Reports preserve evidence but must not replace the record. | Reports include machine-readable record or stable reference. | Report review. | Engineering report sample. | Report uses record as source projection. | Report narrative is the only diagnosis truth. | HIGH |
| Governance Projection | Governance Check exposes the record without recomputing conflicting truth. | Existing governance projection can make record visible. | CLI/status output includes or points to the record. | CLI/fixture test or captured output. | Governance projection sample. | Projection preserves record fields. | Projection recomputes or contradicts record. | HIGH |
| Validation Rules | Invalid records are rejected. | Prevents partial or unsafe acceptance. | Validator/test suite rejects wrong schema, missing evidence, bad enums, mutation flags. | Negative tests. | Failure fixtures and test output. | All invalid fixtures fail. | Invalid record passes. | BLOCKING |
| Compatibility Rules | Required v1 fields remain stable and unknown optional fields are ignored. | Future extensions must not break consumers. | Consumers tolerate extra optional fields. | Backward compatibility tests. | v1 record plus extended record fixtures. | v1 and extended-compatible records pass. | Optional fields change required meaning. | HIGH |
| Regression Protection | Existing governed L3, health diagnosis, Runtime, Authority, Verification, Rollback behavior remains unchanged. | Domain 11 must not disturb downstream execution contracts. | Existing tests pass; no unrelated execution path changes. | Affected test suite and diff review. | Test output and implementation diff. | No behavioral regression. | Downstream owner contracts changed. | BLOCKING |

## 5. Implementation Acceptance Checks

Implementation Acceptance is `PASS` only when all checks below pass:

| Check | Pass condition |
| --- | --- |
| Diagnosis Record exists | At least one implementation path produces `v7.diagnosis-owner-resolution.v1`. |
| Correct schema version | `schema_version == "v7.diagnosis-owner-resolution.v1"`. |
| All required fields present | Every required field from the contract exists. |
| No prohibited fields | No field grants mutation, authority, runtime apply, restore clearance, or planner ranking. |
| Read-only guarantee | Producer and projection are read-only. |
| No Runtime mutation | No Runtime apply path is invoked. |
| No Planner mutation | No Planner state/ranking is mutated by diagnosis. |
| No Authority expansion | No Authority budget or approval is changed. |
| No Restore Barrier writes | No restore barrier file or clearance is written by diagnosis. |
| No user movement | `users_moved == 0` and no apply path invoked. |
| No synthetic evidence | Producer does not fabricate evidence. |
| Existing owners reused | Implementation uses existing Engineering Automation / OMP / governance read-model owners. |
| Consumers synchronized | OMP, CPS, Production Maturity, Engineering Reports, Engineering Automation, Governance Check and Future Certification can consume the same record. |
| Validation passes | Contract validator/tests accept valid records and reject invalid records. |
| Contract compliance passes | The implementation proves compliance with `V7_DIAGNOSIS_RECORD_CONTRACT.md`. |

Any failed check is blocking.

## 6. Test Acceptance

Mandatory test groups:

| Test group | Requirement | Minimum coverage | Pass condition | Blocking Severity |
| --- | --- | --- | --- | --- |
| Unit tests | Test producer and field generation directly. | Valid record, required fields, source identity, no mutation flags. | All pass. | BLOCKING |
| Contract tests | Validate schema and enum rules. | Valid v1 record and invalid fixture set. | Valid passes, invalid fails. | BLOCKING |
| Consumer tests | Prove consumers read same record. | OMP, CPS, PM, Engineering Reports, Engineering Automation, Governance Check. | No consumer reinterpretation. | BLOCKING |
| Regression tests | Existing behavior unchanged. | Existing affected tests for health diagnosis, autoswitch, governed chain, Authority, Runtime, Verification, Rollback. | All affected tests pass. | BLOCKING |
| Negative tests | Reject unsafe records. | Wrong schema, missing evidence, bad terminal classification, mutation flags true, new owner named. | All invalid records rejected. | BLOCKING |
| Unknown-state tests | Preserve unknown. | Missing evidence, stale evidence, conflicting evidence, unknown owner. | Unknown is preserved; no fake root cause. | BLOCKING |
| Owner Resolution tests | Classify terminal states. | `POLICY_PROHIBITION`, `IMPLEMENTATION_MISSING`, `OWNER_INVOCATION_MISSING`, `IMPLEMENTATION_DEFECT`, `CANONICAL_IMPOSSIBILITY`, unresolved required state. | All classifications correct. | BLOCKING |
| Mutation boundary tests | Prove no mutation. | No Runtime apply, Planner mutation, Authority expansion, Restore Barrier writes, user movement, synthetic evidence. | All no-mutation assertions pass. | BLOCKING |
| Backward compatibility tests | Consumers tolerate compatible extensions. | v1 record plus extra optional fields. | Consumers ignore unknown optional fields. | HIGH |

Test output must be persisted in the implementation evidence report.

## 7. Domain Certification Acceptance Gate

Domain 11 becomes eligible for `CERTIFIED` only when:

| Gate | Required result |
| --- | --- |
| Implementation Acceptance | PASS |
| All tests | PASS |
| Contract compliance | PASS |
| Recovery Discovery gap closed | PASS |
| No architecture changes introduced | PASS |
| Existing owners reused | PASS |
| Consumer synchronization | PASS |
| Function Graph shows closed read-only projection | PASS |
| No new Runtime/Planner/Authority/Owner/Service/Database/Execution flow | PASS |

If any gate is not `PASS`, Domain 11 remains `NOT CERTIFIED`.

## 8. Acceptance Evidence Requirements

The implementation acceptance report must include:

- changed files;
- producer function/module;
- sample valid Diagnosis Record;
- validation output;
- test commands and results;
- consumer projection evidence;
- no-mutation evidence;
- Function Graph evidence after implementation;
- statement that no new architecture was introduced;
- statement that existing owners were reused;
- Domain 11 certification rerun result.

Evidence may be rejected if it is narrative-only and does not include inspectable implementation or test output.

## 9. Blocking Conditions

The following always block acceptance:

- no Diagnosis Record producer exists;
- schema version is missing or wrong;
- required fields are missing;
- record is not machine-readable;
- root cause is claimed without evidence;
- unknown is converted into pass/fail/root cause;
- owner block remains `BLOCKED`, `STOP_SAFE`, or `BLOCKED_BY_SAFETY_OWNER` without terminal Owner Resolution classification or required state;
- mutation boundary is violated;
- Runtime, Planner, Authority, Restore Barrier or user movement behavior changes;
- new owner/service/database/execution path is introduced;
- consumers reinterpret diagnosis truth;
- reports remain the only diagnosis truth;
- tests are absent or failing;
- Function Graph cannot show a closed read-only projection.

## 10. Final Verdict

Can implementation begin?

`YES`

Expected result after successful implementation:

Domain 11:

`CERTIFIED`

Stage 1.2:

`COMPLETE`
