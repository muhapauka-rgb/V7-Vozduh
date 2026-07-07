# V7 Stage 1 Diagnosis Implementation Mission

Created: 2026-07-07

Stage: `Stage 1.2`

Domain: `11 — Diagnosis`

Target status transition: `NOT CERTIFIED -> CERTIFIED`

Mode: Implementation Mission only. No implementation is performed by this document.

## 1. Executive Summary

Domain 11 is architecturally correct but not implementation-certified because V7 does not yet have an executable, read-only Diagnosis / Owner Resolution Record producer.

The missing implementation is not a new Runtime, Planner, Authority, Wake owner, Restore Barrier owner, service, database, or execution path. The smallest sufficient change is to extend the existing Engineering Automation / OMP read-model owner, `admin_core/autonomy_trust_acceleration.py`, so it can build and validate a machine-readable record with schema `v7.diagnosis-owner-resolution.v1`.

The implementation must consume existing evidence only, preserve unknown states when evidence is insufficient, claim root cause only when evidence proves it, expose owner-resolution terminal classification, and project the same diagnosis truth to OMP, Current Program State, Production Maturity, Engineering Reports, Engineering Automation, Governance Check, and future certification.

The implementation must also add regression and contract tests in the existing autonomy trust acceleration test surface. A small read-only governance projection in `tools/v7-control-plane-governance-check` is required only to satisfy the existing Governance Check consumer contract; it must not recompute conflicting diagnosis truth.

Expected result after implementation and acceptance: Domain 11 becomes `CERTIFIED`, and Stage 1.2 becomes `COMPLETE`.

## 2. Mission Scope

This mission implements only the missing executable read-only projection required by:

- `docs/reports/research/V7_STAGE1_DIAGNOSIS_RECOVERY_DISCOVERY.md`
- `docs/reference/V7_DIAGNOSIS_RECORD_CONTRACT.md`
- `docs/process/V7_DIAGNOSIS_IMPLEMENTATION_ACCEPTANCE.md`

In scope:

- Produce `v7.diagnosis-owner-resolution.v1` records.
- Validate required schema fields and enums.
- Preserve evidence references.
- Preserve unknown states when evidence is missing, stale, conflicting, or not investigated.
- Preserve root-cause discipline: no root cause claim without direct evidence.
- Preserve Owner Resolution terminal classifications.
- Preserve optional first divergence only when proven.
- Expose downstream consumer projection from the same record.
- Prove mutation boundaries with tests.
- Prove no new owner is introduced.

Out of scope:

- Runtime mutation.
- Planner mutation.
- Authority expansion.
- Restore Barrier writes.
- User movement.
- Synthetic evidence creation.
- New truth source creation.
- New service, database, daemon, or execution flow.
- Architecture redesign.
- Contract modification.
- OMP, SYSTEM_MAP, Production Maturity, or Canonical Reference synchronization.

## 3. Files To Modify

| File | Existing owner | Current implementation | Required change | Functions to modify | New functions to add | Functions to reuse | Functions to leave unchanged | Tests to update | Expected output | Reason |
|---|---|---|---|---|---|---|---|---|---|---|
| `admin_core/autonomy_trust_acceleration.py` | Engineering Automation / OMP read-only model owner | Contains read-only autonomy trust, evidence, attribution, policy, freshness, runtime enablement, and diagnostic-adjacent models. Existing `build_observed_degradation_attribution` explicitly avoids root-cause claims and mutation. | Add a pure read-only Diagnosis / Owner Resolution Record builder, validator, and consumer projection. | None required initially; avoid changing existing model behavior. Optionally expose the new record in an existing inventory only if acceptance requires inventory visibility. | `build_diagnosis_owner_resolution_record`; `validate_diagnosis_owner_resolution_record`; `build_diagnosis_owner_resolution_consumer_projection`; small private normalization helpers if needed. | Existing `_text`, existing read-only patterns, existing evidence attribution style, existing mutation-boundary flags. | Runtime enablement, planner-related models, authority models, existing B5 attribution, inventory models unless explicitly necessary. | `tests/unit/test_autonomy_trust_acceleration.py` | JSON-compatible record with schema `v7.diagnosis-owner-resolution.v1`, validation result, and consumer projection. | This is the smallest existing owner that already owns read-only Engineering Automation / OMP projections without mutation authority. |
| `tests/unit/test_autonomy_trust_acceleration.py` | Unit test owner for Engineering Automation read-models | Already verifies read-only trust acceleration models, no synthetic evidence, no runtime mutation, no authority expansion, and no root-cause claims for B5. | Add contract, negative, unknown-state, owner-resolution, consumer, and mutation-boundary tests for the Diagnosis Record. | Existing test class only; no production functions. | Test methods for valid record, invalid schema, missing evidence, terminal classifications, first divergence, consumer projection, and mutation boundary. | Existing test style and fixture pattern. | Existing tests unchanged. | Same file. | PASS evidence for acceptance gate. | Keeps testing in the existing owner test surface and avoids creating a parallel test owner. |
| `tools/v7-control-plane-governance-check` | Read-only governance projection owner | Already reads local artifacts and reports root-cause/status/governance fields. It does not mutate runtime or call routing tools. | Add a minimal read-only projection that exposes or points to the Diagnosis Record without recomputing conflicting truth. | Add one projection function and one output block only if needed by acceptance. Do not change existing status decisions. | `diagnosis_owner_resolution_projection_status` or equivalent small status function. | Existing `read_text`, artifact status pattern, local JSON/dict output pattern. | All existing egress/root-cause/governance status functions and GO/NO-GO logic. | Existing governance-check test if present; otherwise add coverage through `tests/unit/test_autonomy_trust_acceleration.py` plus a direct CLI fixture test only if the repository already has a matching governance-check test pattern. | Governance output includes or points to the same `v7.diagnosis-owner-resolution.v1` record. | Acceptance requires Governance Check visibility. This is a consumer projection, not a new diagnosis owner. |

Files explicitly left unchanged:

| File / owner | Reason |
|---|---|
| `tools/v7-users-autoswitch` | Already produces incident, blocker, wake, selected-move, and apply evidence. Domain 11 needs a read-only projection over evidence, not a new autoswitch behavior. |
| `tools/v7-egress-diagnose` | Already performs health diagnosis. Domain 11 missing part is Owner Resolution record closure, not health probe behavior. |
| `admin_core/diagnostic_views.py` | Existing admin diagnostic schema is a UI/read-model pattern, not the canonical Owner Resolution record. No change is required for minimum certification. |
| `admin_core/operator_execution_pipeline.py` | Runtime/decision pipeline must remain unchanged. Diagnosis implementation must not alter governed execution. |
| `docs/reference/V7_DIAGNOSIS_RECORD_CONTRACT.md` | Contract is complete and must not be modified during implementation. |
| `docs/process/V7_DIAGNOSIS_IMPLEMENTATION_ACCEPTANCE.md` | Acceptance authority is complete and must not be modified during implementation. |

## 4. Implementation Plan

| Step | Current implementation | Required change | Reason | Consumer | Expected outcome | Acceptance criteria satisfied |
|---|---|---|---|---|---|---|
| 1. Diagnosis Record constants | No executable schema constants for `v7.diagnosis-owner-resolution.v1`. | Add schema version and allowed-value constants in `admin_core/autonomy_trust_acceleration.py`. | Validation must be deterministic and contract-aligned. | Validator, tests, future certification. | Stable local schema vocabulary. | Diagnosis Record Schema, Compatibility Rules. |
| 2. Diagnosis Record builder | Evidence and root-cause-adjacent models exist, but no canonical Diagnosis Record producer exists. | Add `build_diagnosis_owner_resolution_record(...)` as a pure function over provided subject/evidence/owner-resolution fields. | Domain 11 failed because no executable producer existed. | OMP, CPS, Production Maturity, Engineering Reports, Engineering Automation, Governance Check, future certification. | Deterministic JSON-compatible Diagnosis Record. | Diagnosis Record Producer, Evidence Consumption, Evidence References, Root Cause Rules, Unknown Rules, Owner Resolution Rules. |
| 3. Mutation boundary fields | Existing read-only models expose no-mutation flags, but Diagnosis Record has no implemented mutation boundary. | Builder must always emit `read_only=true` and `mutation_boundary` with Runtime/Planner/Authority/Restore Barrier/user movement/synthetic evidence/new owner flags set to safe false/zero values. | Domain 11 must never become a mutation path. | Acceptance, Function Graph, future certification. | Machine-readable no-mutation proof. | Mutation Boundary, Regression Protection. |
| 4. Root cause and unknown rules | Existing B5 model avoids root-cause claims; Owner Resolution terminal states exist in documents. | Builder must set `root_cause_proven=false` unless evidence references directly support a cause. Missing/stale/conflicting evidence must produce explicit unknown state. | Prevents symptom, blocker, or operator narrative from becoming false root cause. | OMP, CPS, reports, future certification. | Unknown remains unknown; proven cause has evidence. | Root Cause Rules, Unknown Rules, Terminal Classification Rules. |
| 5. First divergence | Forensic reports compute first divergence manually; no reusable field exists. | Add optional `first_divergence` field only when caller supplies proven evidence. Otherwise preserve absence or `UNKNOWN` without inference. | First divergence is useful but dangerous if guessed. | Engineering Reports, Future Certification. | First divergence is present only when proven. | First Divergence Rules, Evidence Rules. |
| 6. Validator | No contract validator exists for this schema. | Add `validate_diagnosis_owner_resolution_record(record)`. It must return deterministic validation status and errors without mutation. | Acceptance requires contract compliance evidence. | Tests, acceptance, future certification. | Invalid records fail predictably; valid records pass. | Validation Rules, Contract Compliance. |
| 7. Consumer projection | Consumer fields exist in contracts and Current Program State, but no shared projection exists. | Add `build_diagnosis_owner_resolution_consumer_projection(record)` that maps the same record into OMP/CPS/Production Maturity/Engineering Reports/Engineering Automation/Governance/Future Certification views. | Consumers must not reinterpret diagnosis truth. | All listed consumers. | One canonical record feeds every consumer view. | Consumer Contract, OMP Consumption, CPS Consumption, Production Maturity Consumption, Engineering Reports Consumption. |
| 8. Governance Check projection | Governance check currently reports many root-cause statuses from local artifacts but not the canonical Diagnosis Record. | Add a small read-only projection/status that includes or points to the same Diagnosis Record. It must not recompute conflicting truth. | Acceptance explicitly requires Governance Projection. | Governance Check, acceptance. | Governance output preserves record fields. | Governance Projection. |
| 9. Unit and contract tests | Existing tests cover read-only trust acceleration but not Diagnosis Record contract. | Add tests covering schema, required fields, terminal classifications, unknown state, root-cause evidence, mutation boundary, consumer projection, compatibility, and regression invariants. | Implementation cannot be accepted without tests. | Acceptance, future recertification. | All mandatory test groups PASS. | Test Acceptance, Regression Protection. |
| 10. Domain 11 recertification | Domain 11 currently remains `NOT CERTIFIED`. | After implementation and tests, rerun Domain 11 certification using the canonical engine. | Certification status can change only after implementation evidence exists. | Stage 1.2. | Domain 11 becomes `CERTIFIED` if acceptance passes. | Domain Certification Acceptance Gate. |

## 5. Dependency Graph

```text
Diagnosis Record Contract
  -> Implementation Acceptance Contract
    -> admin_core.autonomy_trust_acceleration constants
      -> build_diagnosis_owner_resolution_record
        -> validate_diagnosis_owner_resolution_record
          -> build_diagnosis_owner_resolution_consumer_projection
            -> governance-check read-only projection
              -> unit / contract / negative / consumer / mutation-boundary tests
                -> Implementation Acceptance PASS
                  -> Domain 11 recertification
                    -> Domain 11 CERTIFIED
                      -> Stage 1.2 COMPLETE
```

Implementation dependencies:

1. Constants must exist before builder validation can be stable.
2. Builder must exist before validator and consumer projection can be tested.
3. Validator must exist before acceptance can prove contract compliance.
4. Consumer projection must exist before OMP/CPS/Production Maturity/Engineering Reports/Governance consumption can be accepted.
5. Tests must pass before recertification.
6. Recertification must happen only after persisted implementation evidence exists.

## 6. Risk Analysis

| Change | Possible regression | Affected owners | Affected Runtime | Affected Planner | Affected Authority | Affected consumers | Mitigation |
|---|---|---|---|---|---|---|---|
| Add builder in `admin_core/autonomy_trust_acceleration.py` | Existing inventory output could change if the new model is wired into a broad inventory too early. | Engineering Automation / OMP read-model owner. | None expected. | None expected. | None expected. | OMP, CPS, Production Maturity, Reports, future certification. | Add pure functions first. Do not alter existing inventory output unless acceptance requires visibility. Tests must assert existing read-only flags and no runtime mutation. |
| Add validator | Over-strict validation could reject valid future-compatible optional fields. | Engineering Automation / OMP read-model owner. | None. | None. | None. | Tests, acceptance, future certification. | Validate required fields and known enums; allow optional extension fields per compatibility contract. |
| Add consumer projection | Consumer mapping could drift from contract names. | Engineering Automation / OMP read-model owner; OMP/CPS/Production Maturity as consumers. | None. | None. | None. | OMP, CPS, Production Maturity, Engineering Reports, Engineering Automation, Governance Check, Future Certification. | Use field names from `V7_DIAGNOSIS_RECORD_CONTRACT.md`; tests must assert projections read from the same record. |
| Add governance-check projection | CLI output could be interpreted as new governance truth. | Governance Check owner. | None. | None. | None. | Governance Check, acceptance. | Projection must include or point to the same Diagnosis Record and explicitly avoid recomputation. No GO/NO-GO logic changes. |
| Add tests | Test suite could become slow or brittle if it depends on live artifacts. | Test owner. | None. | None. | None. | Acceptance. | Use fixture dictionaries and pure functions. No production file reads unless a governance-check fixture test already exists. |

## 7. Minimality Review

| Proposed change | Can this change be made smaller? | Minimality decision |
|---|---|---|
| Add Diagnosis Record builder in `admin_core/autonomy_trust_acceleration.py` | NO | A concrete producer is the exact missing implementation. Without it Domain 11 remains report-only and cannot be certified. |
| Add schema constants | NO | The schema version and enum vocabulary must be stable for validation and compatibility. |
| Add validator | NO | Acceptance requires contract compliance, invalid fixture rejection, and validation evidence. Unit assertions alone are not enough because consumers need a reusable compliance result. |
| Add consumer projection | NO | Consumer contract requires OMP, CPS, Production Maturity, Engineering Reports, Engineering Automation, Governance Check, and Future Certification to consume the same diagnosis truth. A projection function is the smallest reusable proof. |
| Add governance-check projection | NO, if Governance Projection acceptance remains mandatory | Acceptance explicitly requires Governance Check visibility. The smallest form is read-only exposure or pointer to the same record, without changing existing governance decisions. |
| Add tests in existing test file | NO | Tests are mandatory. Reusing `tests/unit/test_autonomy_trust_acceleration.py` is smaller than creating a separate test owner. |
| Leave Runtime/Planner/Authority unchanged | YES, no change needed | The missing gap is a read-only Diagnosis projection. Runtime, Planner, and Authority are consumers/downstream safety owners, not the missing producer. |
| Leave contracts unchanged | YES, no change needed | Contract and acceptance are already complete. Modifying them would reopen architecture work and violate the mission. |

## 8. Acceptance Mapping

| Acceptance criterion | Implementation item | Evidence expected |
|---|---|---|
| Diagnosis Record Producer | `build_diagnosis_owner_resolution_record` | Function path, sample valid record, test output. |
| Diagnosis Record Schema | Schema constants and validator | Valid record test and invalid schema negative test. |
| Evidence Consumption | Builder accepts existing evidence refs and source object fields | Fixture with real-style evidence refs; no synthetic evidence flags. |
| Evidence References | Required `evidence_refs` validation | Negative test for missing refs when proof is claimed. |
| Root Cause Rules | `root_cause_proven` logic | Proven and unknown fixtures; no root-cause claim without evidence. |
| Unknown Rules | Unknown-state enum handling | Missing/stale/conflicting/not-investigated fixtures. |
| Owner Resolution Rules | `blocking_owner`, `owner_resolution_state`, `required_resolution` | Tests for owner-resolution fields. |
| Terminal Classification Rules | Terminal classification enum | Tests for `POLICY_PROHIBITION`, `IMPLEMENTATION_MISSING`, `OWNER_INVOCATION_MISSING`, `IMPLEMENTATION_DEFECT`, `CANONICAL_IMPOSSIBILITY`. |
| First Divergence Rules | Optional `first_divergence` handling | Test that field appears only when supplied with evidence; otherwise remains unknown/absent. |
| Mutation Boundary | Static no-mutation boundary and validator checks | Tests assert no Runtime/Planner/Authority/Restore Barrier writes, zero users moved, no synthetic evidence, no new owner. |
| Consumer Contract | Consumer projection function | Projection tests for all required consumers reading same record. |
| OMP Consumption | Consumer projection includes OMP fields | Test checks required resolution and next mission fields. |
| Current Program State Consumption | Consumer projection includes Blocking Owner, Owner Resolution State, Terminal Root Cause, Required Resolution, Expected Next Engineering Step | Test checks CPS projection fields. |
| Production Maturity Consumption | Consumer projection exposes evidence and maturity relevance without permission grant | Test checks PM projection does not grant authority. |
| Engineering Reports Consumption | Projection exposes record id and embeddable evidence refs | Test checks report projection references same record id. |
| Governance Projection | Governance-check read-only projection | CLI/status fixture or function test showing record included or pointed to. |
| Validation Rules | `validate_diagnosis_owner_resolution_record` | Valid/invalid tests. |
| Compatibility Rules | Validator allows optional future fields and rejects missing required fields | Backward compatibility and negative tests. |
| Regression Protection | Existing tests plus new no-mutation tests | Full affected unit test output and diff review. |

## 9. Execution Order

1. Add schema constants and allowed values in `admin_core/autonomy_trust_acceleration.py`.
2. Add `build_diagnosis_owner_resolution_record`.
3. Add `validate_diagnosis_owner_resolution_record`.
4. Add `build_diagnosis_owner_resolution_consumer_projection`.
5. Add minimal read-only Governance Check projection in `tools/v7-control-plane-governance-check`.
6. Add unit and contract tests in `tests/unit/test_autonomy_trust_acceleration.py`.
7. Add a governance projection test only if the existing test layout has a matching governance-check test pattern; otherwise prove governance projection through direct function/fixture output.
8. Run affected unit tests.
9. Run broader regression tests required by acceptance if available.
10. Run implementation acceptance against `docs/process/V7_DIAGNOSIS_IMPLEMENTATION_ACCEPTANCE.md`.
11. Regenerate or inspect Function Graph evidence to confirm a closed read-only node and no mutation edge.
12. Rerun Domain 11 certification using the locked certification engine.
13. Record expected Stage 1.2 completion evidence.

## 10. Expected Certification Result

After successful implementation:

- Implementation Acceptance: `PASS`
- Contract Compliance: `PASS`
- Required Tests: `PASS`
- Recovery Discovery gap closed: `PASS`
- Architecture changes introduced: `NO`
- New owner introduced: `NO`
- New Runtime introduced: `NO`
- New Planner introduced: `NO`
- New Authority introduced: `NO`
- Domain 11: `CERTIFIED`
- Stage 1.2: `COMPLETE`

Final review:

| Question | Answer |
|---|---|
| Ready for implementation? | YES |
| Expected result: Domain 11 | CERTIFIED |
| Expected result: Stage 1.2 | COMPLETE |

