# V7 Diagnosis Record Contract

Status: CANONICAL_CONTRACT_DRAFT

Schema: `v7.diagnosis-owner-resolution.v1`

Date: 2026-07-07

## 1. Executive Summary

This document defines the canonical contract for the executable read-only Diagnosis / Owner Resolution Record.

The record exists because Domain 11 — Diagnosis is architecturally correct but not yet implementation-certified. V7 already has health diagnosis, diagnostic read models, Owner Resolution laws, Engineering Reports, Current Program State fields, and read-only Engineering Automation models. What is missing is one stable machine-readable projection that connects those existing parts.

The Diagnosis Record is that projection.

It does not create a new Runtime, Planner, Authority, owner, service, database, mutation path, or execution flow. It defines the minimum object that existing owners must produce and consume so that Diagnosis can move from report/manual/Codex-driven work to a closed read-only implementation contract.

The record answers:

- what object is being diagnosed;
- what symptom or blocker was observed;
- what evidence supports the diagnosis;
- whether root cause is proven or unknown;
- which owner is responsible;
- which Owner Resolution terminal classification applies;
- what required resolution follows;
- which consumers may read the result.

The record is read-only. It never authorizes mutation, never moves users, never bypasses Authority, never bypasses Restore Barrier, never bypasses Runtime, and never replaces Verification or Rollback.

## 2. Architecture Position

Diagnosis sits after Observation, Health Evidence, and Incident, and before Decision Model, Planner, Authority, OMP, Current Program State, Production Maturity, Engineering Automation, and Engineering Reports consume diagnostic truth.

Canonical position:

```text
Observation
  -> Health Evidence
  -> Incident
  -> Diagnosis Record
  -> Owner Resolution
  -> Decision Model / Planner / Authority / OMP / CPS / Production Maturity
```

Diagnosis owns explanation, not action.

Diagnosis may classify:

- observed symptom;
- blocker;
- unknown;
- missing evidence;
- first divergence;
- root cause when proven;
- blocking owner;
- Owner Resolution state;
- required resolution.

Diagnosis must not own:

- action ranking;
- authority admission;
- approved plan lock;
- restore barrier;
- runtime apply;
- verification result production;
- rollback execution;
- learning mutation;
- production movement.

## 3. Contract Discovery

Repository discovery found existing partial contracts. This contract reuses them and fills only the missing object boundary.

| Contract element | Existing location | Status | Reuse decision |
| --- | --- | --- | --- |
| Admin diagnostic read-only schema | `admin_core/diagnostic_views.py`, `diagnostic_schema_contracts`, schema `v7.admin.diagnostic.v1` | IMPLEMENTED | Reuse read-only schema pattern; do not reuse as Domain 11 record because it is admin diagnostic visibility, not owner-resolution truth. |
| Egress health diagnosis | `tools/v7-egress-diagnose`, `tests/unit/test_v7_egress_diagnose.py` | IMPLEMENTED | Reuse as input evidence only. |
| Current-channel failure evidence | `tools/v7-users-autoswitch._current_channel_failure_evidence` | IMPLEMENTED | Reuse `schema_version`, `source_object`, `owner`, `diagnose_reason`, `affected_users_on_channel` as evidence inputs. |
| Selected move/blocker diagnostics | `tools/v7-users-autoswitch` safety and selected move diagnostics | IMPLEMENTED | Reuse blockers/reasons as diagnosis inputs. |
| Local root-cause governance projections | `tools/v7-control-plane-governance-check` root-cause status helpers | PARTIAL | Reuse projection style and report artifact reading; not sufficient as general record. |
| Read-only Engineering Automation attribution | `admin_core/autonomy_trust_acceleration.py`, schema `v7.b5.observed-degradation-attribution.v1` | PARTIAL | Reuse read-only/no-root-cause-without-proof pattern. |
| Owner Resolution terminal classifications | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`; `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`; `docs/reports/engineering/2026-07-03_084803_owner_resolution_law.md` | IMPLEMENTED | Reuse exact terminal classification vocabulary. |
| Current Program State fields | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | PARTIAL | Reuse `Blocking Owner`, `Owner Resolution State`, `Terminal Root Cause`, `Required Resolution`, `Expected Next Engineering Step` as consumer fields. |
| Owner Resolution record | `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`, Owner Mapping says `NEEDED_IMPLEMENTATION`; Owner Resolution Law report says concrete projection/storage is missing | MISSING | Define here as `v7.diagnosis-owner-resolution.v1`. |
| First divergence field | Engineering forensic reports | PARTIAL | Define optional field; required only when proven. |
| Evidence quality / confidence fields | Local root-cause helpers and certification reports | PARTIAL | Define normalized fields for the record. |
| Machine-readable Diagnosis Record | Repository search found no closed record contract | MISSING | Define here. |

Discovery conclusion:

The repository already contains most semantics. It does not contain one canonical machine-readable Diagnosis / Owner Resolution Record contract. This document adds that missing contract without changing architecture.

## 4. Producer Contract

Canonical producer:

`Engineering Automation / OMP read-only diagnosis projection`

Expected implementation owner:

`admin_core.autonomy_trust_acceleration`

Allowed supporting projection owner:

`tools/v7-control-plane-governance-check`

Allowed evidence lookup support:

`admin_core.operator_observability`

The producer must:

1. consume existing evidence and report artifacts;
2. preserve source object identity;
3. produce one read-only diagnosis record;
4. classify owner resolution only from evidence;
5. preserve unknown instead of inventing root cause;
6. expose consumer fields without triggering mutation;
7. set all no-mutation fields explicitly.

The producer must not:

- run Runtime apply;
- call Authority promotion;
- write Restore Barrier;
- create synthetic evidence;
- move users;
- recompute Planner decisions;
- rewrite incident identity;
- claim root cause without evidence.

Truth Source:

The Diagnosis Record is not the original truth source. It is the canonical read-only projection over existing truth sources.

Allowed truth sources:

- Observation evidence;
- Health Evidence;
- Incident context;
- Runtime blockers;
- Verification blockers;
- Rollback/closure outcomes;
- Engineering Reports;
- owner maps;
- governance projections;
- Current Program State fields;
- production artifacts and logs already captured by existing owners.

The record must always point back to source evidence through `evidence_refs`.

## 5. Consumer Contract

Consumers may read the Diagnosis Record. They may not reinterpret diagnosis truth.

| Consumer | Allowed use | Forbidden use |
| --- | --- | --- |
| OMP | Convert `required_resolution` into the next engineering mission; route `terminal_classification` into continuation, hold, policy decision, implementation mission, or canonical impossibility handling. | Do not invent another root cause if the record already classifies it. |
| Current Program State | Project `blocking_owner`, `owner_resolution_state`, `terminal_root_cause`, `required_resolution`, and `expected_next_engineering_step`. | Do not maintain conflicting manual root-cause state for the same diagnosis object. |
| Production Maturity | Consume diagnosis evidence as maturity/capability evidence and blocker evidence. | Do not treat unproven root cause as capability evidence. |
| Engineering Reports | Quote or embed the Diagnosis Record and add human-readable analysis around it. | Do not replace the record with narrative-only truth. |
| Engineering Automation | Use records as read-only input for automation debt, workflow debt, analyzer backtesting, and implementation mission generation. | Do not use the record as direct authority for production mutation. |
| Governance Check | Print or expose the record as status/projection. | Do not recompute conflicting diagnosis truth in the projection layer. |
| Future Certification | Use the record to prove Domain 11 implementation closure. | Do not certify Diagnosis from reports alone when the record is missing. |

Consumer rule:

If a consumer disagrees with a Diagnosis Record, it must create a new diagnosis investigation or evidence update. It must not silently reinterpret the same record.

## 6. Schema Contract

Schema name:

`v7.diagnosis-owner-resolution.v1`

Top-level object type:

JSON-compatible dictionary.

Read-only:

Always `true`.

Required top-level fields:

| Field | Meaning | Producer | Consumer | Required | Optional | Allowed values | Validation | Evidence requirement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `schema_version` | Contract version. | Diagnosis producer | All consumers | YES | NO | `v7.diagnosis-owner-resolution.v1` | Exact string. | None. |
| `record_id` | Stable id for this diagnosis projection. | Diagnosis producer | All consumers | YES | NO | Stable string, preferably content/identity-derived. | Non-empty; stable for same subject/evidence set. | Source identity inputs. |
| `generated_at` | UTC generation time. | Diagnosis producer | All consumers | YES | NO | ISO-8601 UTC string. | Parseable timestamp. | Producer clock. |
| `producer` | Concrete producing owner/function. | Diagnosis producer | All consumers | YES | NO | Existing owner path string. | Must not name new owner. | Function/module evidence. |
| `read_only` | Declares no mutation behavior. | Diagnosis producer | All consumers | YES | NO | `true` | Must be true. | Producer contract. |
| `subject` | Object being diagnosed. | Diagnosis producer | OMP, CPS, PM, reports | YES | NO | Object dictionary. | Must include `type` and `id`. | Incident/execution/blocker evidence. |
| `source_object` | Canonical source object pointer. | Diagnosis producer | All consumers | YES | NO | String or object pointer. | Non-empty. | Must reference original evidence object. |
| `evidence_refs` | Evidence backing the diagnosis. | Diagnosis producer | All consumers | YES | NO | List of evidence references. | Non-empty unless status is `NO_EVIDENCE`. | Every claim must point here. |
| `diagnosis_status` | State of diagnosis. | Diagnosis producer | All consumers | YES | NO | `PROVEN`, `UNKNOWN`, `PARTIAL`, `NO_EVIDENCE`, `CONFLICTING_EVIDENCE` | Exact enum. | Evidence completeness. |
| `symptom` | Observed symptom/blocker. | Diagnosis producer | OMP, reports, CPS | YES | NO | Object with `type`, `value`, `producer`. | Non-empty for blocker/incident diagnoses. | Observation/blocker evidence. |
| `root_cause` | Root cause claim or empty/unknown. | Diagnosis producer | All consumers | YES | NO | String; `UNKNOWN` allowed. | If not `UNKNOWN`, `root_cause_proven` must be true. | Direct supporting evidence required. |
| `root_cause_proven` | Whether root cause is proven. | Diagnosis producer | All consumers | YES | NO | `true` / `false` | Boolean. | Must be false without direct evidence. |
| `unknown_state` | Unknown/missing evidence state. | Diagnosis producer | All consumers | YES | NO | `NONE`, `MISSING_EVIDENCE`, `STALE_EVIDENCE`, `CONFLICTING_EVIDENCE`, `NOT_INVESTIGATED`, `UNKNOWN_OWNER` | Exact enum. | Required when diagnosis not proven. |
| `blocking_owner` | Existing owner that blocked or owns the condition. | Diagnosis producer | OMP, CPS, PM | YES | NO | Existing owner id/path, or `NONE`, or `UNKNOWN`. | Must not create new owner. | Owner map or blocker evidence. |
| `owner_resolution_state` | Owner Resolution state. | Diagnosis producer | OMP, CPS, PM, reports | YES | NO | `NOT_REQUIRED`, `REQUIRED`, `RESOLVED`, `UNKNOWN` | Exact enum. | Must be `REQUIRED` when `blocking_owner` is not `NONE` and no terminal classification exists. |
| `terminal_classification` | Final Owner Resolution classification when available. | Diagnosis producer | OMP, CPS, PM | YES | NO | `NONE`, `POLICY_PROHIBITION`, `IMPLEMENTATION_MISSING`, `OWNER_INVOCATION_MISSING`, `IMPLEMENTATION_DEFECT`, `CANONICAL_IMPOSSIBILITY`, `UNKNOWN` | Exact enum. | Required evidence for any value except `NONE`/`UNKNOWN`. |
| `required_resolution` | Next required action or policy outcome. | Diagnosis producer | OMP, CPS, reports | YES | NO | String/object. | Non-empty unless `terminal_classification` is `NONE` and no resolution required. | Must follow terminal classification. |
| `consumers` | Downstream consumers intended to consume this record. | Diagnosis producer | All consumers | YES | NO | List of known consumers. | Must include at least one consumer. | Consumer contract. |
| `mutation_boundary` | Explicit no-mutation flags. | Diagnosis producer | Authority/Runtime/PM | YES | NO | Object. | Must block runtime/authority/apply/user movement. | Producer contract. |

Optional fields:

| Field | Meaning | Producer | Consumer | Required | Optional | Allowed values | Validation | Evidence requirement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `incident` | Incident identity/context. | Diagnosis producer | Incident, Planner, OMP | NO | YES | Object. | If present, must preserve incident key/source/scope. | Incident evidence. |
| `operation_id` | Execution/operation id. | Diagnosis producer | Reports, CPS, OMP | NO | YES | String. | Stable id. | Execution artifact. |
| `packet_id` | Packet identity if execution-bound. | Diagnosis producer | Runtime/Restore Barrier reports | NO | YES | String. | Stable id. | Packet artifact. |
| `selected_move_hash` | Selected move identity if relevant. | Diagnosis producer | Planner/Runtime reports | NO | YES | String. | Hash must match source evidence. | Selected move evidence. |
| `first_divergence` | First proven divergence. | Diagnosis producer | Reports, OMP | NO | YES | Object or `UNKNOWN`. | If object, must include `producer`, `consumer`, `field`, `before`, `after`, `evidence_ref`. | Forensic evidence. |
| `confidence` | Diagnosis confidence. | Diagnosis producer | OMP, PM, Reports | NO | YES | `VERY_HIGH`, `HIGH`, `MEDIUM`, `LOW`, `UNKNOWN` | Must depend on evidence quality. | Evidence quality. |
| `evidence_quality` | Quality of evidence used. | Diagnosis producer | OMP, PM, Reports | NO | YES | `HIGH`, `MEDIUM`, `LOW`, `UNKNOWN` | Must not exceed weakest critical evidence. | Evidence refs. |
| `hypotheses_rejected` | Rejected alternate explanations. | Diagnosis producer | Reports, future certification | NO | YES | List. | Each item must include reason/evidence. | Investigation evidence. |
| `compatibility` | Compatibility metadata. | Diagnosis producer | Future consumers | NO | YES | Object. | Must not change meaning of required fields. | Versioning evidence. |
| `backtesting` | Analyzer backtesting metadata. | Diagnosis producer | Engineering Automation, PM | NO | YES | Object. | Required before analyzer output influences blocking decisions. | Backtesting corpus. |
| `projection_refs` | Where this record was projected. | Projection owner | CPS, PM, Reports | NO | YES | List. | Must not be source truth. | Projection evidence. |

`mutation_boundary` required object:

| Field | Required value |
| --- | --- |
| `runtime_apply_allowed` | `false` |
| `authority_expanded` | `false` |
| `restore_barrier_written` | `false` |
| `users_moved` | `0` |
| `synthetic_evidence_created` | `false` |
| `new_owner_created` | `false` |
| `new_runtime_created` | `false` |
| `new_planner_created` | `false` |

Minimal valid example:

```json
{
  "schema_version": "v7.diagnosis-owner-resolution.v1",
  "record_id": "diag_owner_resolution_001",
  "generated_at": "2026-07-07T00:00:00Z",
  "producer": "admin_core.autonomy_trust_acceleration.build_diagnosis_owner_resolution_record",
  "read_only": true,
  "subject": {
    "type": "execution_block",
    "id": "example_blocker"
  },
  "source_object": "engineering_report:example#owner-resolution",
  "evidence_refs": [
    {
      "type": "report",
      "path": "docs/reports/engineering/example.md",
      "section": "Owner Resolution"
    }
  ],
  "diagnosis_status": "PROVEN",
  "symptom": {
    "type": "blocking_owner",
    "value": "V7_EGRESS_GUARD=BLOCK reason=users_assigned",
    "producer": "v7-egress-guard"
  },
  "root_cause": "policy_prohibits_egress_maintenance_with_assigned_enabled_users",
  "root_cause_proven": true,
  "unknown_state": "NONE",
  "blocking_owner": "v7-egress-guard",
  "owner_resolution_state": "RESOLVED",
  "terminal_classification": "POLICY_PROHIBITION",
  "required_resolution": "Use existing owners to define a legal controlled source degradation path or enter policy HOLD.",
  "consumers": [
    "OMP",
    "Current Program State",
    "Production Maturity",
    "Engineering Reports",
    "Engineering Automation",
    "Governance Check",
    "Future Certification"
  ],
  "mutation_boundary": {
    "runtime_apply_allowed": false,
    "authority_expanded": false,
    "restore_barrier_written": false,
    "users_moved": 0,
    "synthetic_evidence_created": false,
    "new_owner_created": false,
    "new_runtime_created": false,
    "new_planner_created": false
  }
}
```

## 7. Lifecycle Contract

Lifecycle:

```text
Evidence available
  -> Diagnosis producer reads evidence
  -> Diagnosis Record generated
  -> Validation checks pass
  -> Record projected to consumers
  -> Consumers synchronize from the record
  -> Required Resolution becomes the next engineering mission when applicable
```

Allowed lifecycle states:

| State | Meaning |
| --- | --- |
| `DRAFT` | Record generated but not validated. |
| `VALIDATED` | Required fields and evidence rules passed. |
| `PROJECTED` | Record made available to consumers. |
| `CONSUMED` | At least one consumer synchronized from the record. |
| `SUPERSEDED` | Newer evidence generated a newer diagnosis record. |
| `INVALID` | Validation failed; consumers must not use it as diagnosis truth. |

Mutability:

The record is immutable after validation. New evidence must create a new record, not mutate an old record.

Persistence:

The contract does not require a new database. Persistence must reuse existing file/report/projection mechanisms. Implementation may store the record in existing Engineering Report artifacts, governance output, or existing read-model projection files, as long as the record is machine-readable and stable.

Versioning:

Schema version is explicit. Future versions must preserve required v1 fields or provide a compatibility adapter.

## 8. Validation Contract

Validation must reject a record when:

1. `schema_version` is not `v7.diagnosis-owner-resolution.v1`.
2. `read_only` is not true.
3. Any required field is missing.
4. `evidence_refs` is empty while `diagnosis_status` claims `PROVEN`.
5. `root_cause_proven` is true but `root_cause` is `UNKNOWN`.
6. `root_cause_proven` is true without evidence references.
7. `terminal_classification` is outside the allowed enum.
8. `blocking_owner` names a new owner instead of an existing owner, unless value is `NONE` or `UNKNOWN`.
9. `mutation_boundary` allows Runtime apply, Authority expansion, Restore Barrier write, synthetic evidence, new owner, or user movement.
10. Consumer projection rewrites or reclassifies the record.

Evidence rules:

- Every root-cause claim requires direct evidence.
- Missing evidence must produce `UNKNOWN` or `NO_EVIDENCE`, not a guessed cause.
- Conflicting evidence must produce `CONFLICTING_EVIDENCE` unless investigation resolves the conflict.
- Negative evidence is valid evidence and must be preserved.
- Reports may be evidence refs, but narrative reports alone do not replace the record.

Confidence rules:

- `VERY_HIGH`: direct source evidence plus owner confirmation or repeated matching artifacts.
- `HIGH`: direct evidence and no material contradiction.
- `MEDIUM`: indirect evidence or partial owner confirmation.
- `LOW`: weak evidence; record must not drive blocking decisions.
- `UNKNOWN`: no reliable confidence basis.

Unknown rules:

- Unknown is not pass.
- Unknown is not fail.
- Unknown is not canonical impossibility.
- Unknown must carry the missing/conflicting/stale evidence reason.

Root Cause rules:

- A symptom is not root cause.
- A blocker is not root cause until Owner Resolution classifies it.
- Root cause must identify the responsible owner or condition when known.
- Root cause must preserve the source object identity.

Owner Resolution rules:

Allowed terminal classifications:

- `POLICY_PROHIBITION`
- `IMPLEMENTATION_MISSING`
- `OWNER_INVOCATION_MISSING`
- `IMPLEMENTATION_DEFECT`
- `CANONICAL_IMPOSSIBILITY`

Intermediate observations such as `BLOCKED`, `STOP_SAFE`, `BLOCKED_BY_SAFETY_OWNER`, `OWNER_REQUIRED`, and `UNKNOWN_OWNER_BLOCK` are not terminal classifications.

First Divergence rules:

- `first_divergence` is optional.
- If present as a proven object, it must include producer, consumer, field, before value, after value, timestamp if known, and evidence reference.
- If not proven, it must be omitted or set to `UNKNOWN`.

## 9. Compatibility Contract

Backward compatibility:

- v1 required fields must remain stable.
- Consumers must ignore unknown optional fields.
- Producers may add optional fields only if they do not change required field meaning.
- New terminal classifications require a new schema version or explicit compatibility rule.
- Consumer projections must not depend on optional fields for core behavior.

Compatibility with existing architecture:

| Existing area | Compatibility rule |
| --- | --- |
| Runtime | Runtime does not consume this record as execution authority. |
| Planner | Planner may consume diagnosis context only through existing decision/evidence paths; it must not treat this record as target ranking. |
| Authority | Authority may consume diagnosis evidence; it must not treat diagnosis as approval. |
| Restore Barrier | No direct relationship; diagnosis must not write clearance. |
| Verification | Verification remains producer of verification result; diagnosis may explain verification blockers. |
| Rollback / Closure | Closure may consume terminal classification but does not delegate closure truth to diagnosis. |
| OMP | OMP may turn `required_resolution` into engineering mission. |
| CPS | CPS may project current owner/root-cause state from the record. |
| Production Maturity | PM may use record as evidence, not permission. |

## 10. Future Extension Rules

Future extensions may add:

- analyzer backtesting metadata;
- precision/recall fields;
- richer evidence graph links;
- multiple hypotheses;
- causal chain arrays;
- consumer synchronization status;
- supersession links;
- human reviewer approval metadata;
- production maturity evidence class.

Future extensions must not add:

- mutation authority;
- Runtime apply permissions;
- Planner ranking behavior;
- Authority bypass;
- Restore Barrier writes;
- new owner requirement;
- new database requirement;
- production service requirement.

If an extension requires mutation, it is no longer part of the Diagnosis Record Contract and must go through existing Authority, Runtime, Verification and Rollback contracts.

## 11. Relationship to Existing Architecture

This contract reuses existing owners:

- Engineering Automation read models;
- OMP;
- Current Program State;
- Production Maturity;
- Engineering Reports;
- Governance Check;
- existing evidence producers.

This contract does not change:

- Domain 11 architecture;
- Runtime;
- Planner;
- Authority;
- Restore Barrier;
- Verification;
- Rollback;
- Wake;
- Incident;
- Learning;
- production automation.

This contract closes only the object boundary identified by Stage 1.2 Recovery Discovery.

Relationship to Function Graph:

After implementation, Function Graph should show a read-only closed node or function family that produces `v7.diagnosis-owner-resolution.v1`, consumes existing evidence/report/status inputs, and has no mutation edge.

Relationship to Engineering Reports:

Engineering Reports may embed the record and explain it. They must not be the only diagnosis truth for a certified Domain 11 implementation.

Relationship to Current Program State:

Current Program State should project its blocking/root-cause fields from the record when a record exists. If no record exists, CPS must mark the source as report/manual or unknown rather than silently claiming canonical diagnosis truth.

## 12. Why this contract is sufficient for Domain 11 certification

Domain 11 was `NOT CERTIFIED` for two blocking gaps:

1. Implementation Gap: no single executable diagnosis owner/projection.
2. Ownership Gap: Owner Resolution existed canonically but lacked concrete executable record/projection.

This contract defines the missing projection without redesigning architecture.

It is sufficient because it:

- defines the schema of the missing object;
- reuses existing owners;
- defines producer and consumer boundaries;
- preserves read-only behavior;
- preserves Detection Is Not Diagnosis;
- preserves Unknown Is Not Pass And Not Fail;
- preserves Owner Resolution terminal classifications;
- prevents consumer reinterpretation;
- prevents Runtime/Authority/Planner/Restore Barrier bypass;
- gives implementation a minimal target;
- gives future certification a concrete object to verify.

Final review:

| Question | Answer |
| --- | --- |
| Does this contract introduce any new architecture? | NO |
| Does this contract reuse existing owners? | YES |
| Does this contract define the minimum contract required for Domain 11 certification? | YES |

Certification expectation:

If implemented exactly through existing owners and validated by tests, this contract should allow Domain 11 — Diagnosis to move from `NOT CERTIFIED` to `CERTIFIED`.
