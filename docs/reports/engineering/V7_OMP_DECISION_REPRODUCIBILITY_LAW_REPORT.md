# V7 OMP Decision Reproducibility Law Engineering Report

Date: 2026-07-10
Status: `PASS`
Scope: `OPERATIONAL_MATURITY_PROGRAM_ONLY`

## Summary

Operational Maturity Program updated to `V4.6`.

Added canonical `Decision Reproducibility Law` inside existing OMP.

The law requires identical canonical OMP decision inputs to produce identical:

- Decision Trace;
- Decision Fingerprint;
- sequence;
- Mission Admission result;
- STOP result;
- Final Verdict.

If identical inputs produce different outputs, OMP must classify the event as `NON_DETERMINISTIC_DECISION` and stop further execution until an existing owner identifies and corrects the source.

No new architecture, Planner, Decision Engine, Replay Engine, owner, program, model, Runtime path, or truth source was created.

## Discovery And Reuse

Existing mechanisms found and reused:

| Mechanism | Location | Reuse |
| --- | --- | --- |
| Deterministic tie-breaking | OMP Candidate Sequencing Algorithm | Reused as existing selection determinism rule. |
| OMP Decision Trace Contract | OMP `V4.5` | Extended as the canonical explanation and replay basis. |
| Decision Lifecycle / Decision Freshness | Runtime Model + Decision Model references | Reused for decision object lifecycle and freshness semantics. |
| Scheduler Determinism Algorithm | `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md` | Reused when an OMP decision becomes an admitted Mission. |
| Timeline Replay / Mission Replay | `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md` | Reused for mission execution replay; OMP law stays at decision level. |
| Behavior Enforcement Framework | OMP | Reused as Behavior Chain evidence. |
| Execution Certification certificate consumption | OMP | Reused for post-execution evidence eligibility. |
| Engineering Report Lifecycle | OMP | Extended with Decision Fingerprint, Replay Status, and Decision Drift fields. |
| Dashboard Dual-View Model | OMP | Reused as future read-only display consumer. |

No fully equivalent OMP-level law existed before this update. Existing replay/determinism mechanisms covered Runtime/Mission execution or local decision explanations, but not the canonical requirement that OMP itself must reproduce the same candidate decision from the same canonical inputs.

## What Changed In OMP

Updated:

- `Version: 4.5` -> `Version: 4.6`.
- Version history now records `Decision Reproducibility Law`.
- Added `Decision Reproducibility Law` after `OMP Decision Trace Contract`.
- Extended `Engineering Report Lifecycle` with:
  - Decision Fingerprint;
  - Replay Status;
  - Decision Drift status;
  - Difference Explanation.

## How Reproducibility Is Ensured

OMP now defines a canonical input set for every decision:

- Candidate Pool;
- BDP Certificate;
- OMP Certificate;
- Behavior Chain;
- Current Program State;
- Authority Boundary;
- Verification;
- Rollback Boundary;
- Production Boundary;
- Runtime Boundary;
- Engineering Chain;
- Candidate Coverage Matrix;
- Engineering Value;
- System Engineering Value;
- OMP Version;
- canonical owner pointers.

If this input set is identical, OMP must produce the same decision outputs.

If any output differs, OMP must prove which input changed. If no input changed, the result is `NON_DETERMINISTIC_DECISION`.

## Decision Fingerprint

Decision Fingerprint is a deterministic identifier computed only from existing canonical OMP decision inputs.

It may include normalized candidate IDs, certificate hashes/pointers, Behavior Chain status, CPS state hash/pointer, authority/verification/rollback/production/runtime boundaries, Engineering Chain state, coverage/value inputs, OMP version, and canonical owner pointers.

It must not include random values, wall-clock timestamps, session IDs, chat IDs, temporary identifiers, generated prose, non-normalized file order, or environment-specific path noise.

Timestamp may exist in Decision Trace as history, but it cannot affect the fingerprint.

## Decision Drift

Decision Drift means two decisions for the same candidate set or mission context produce different outputs.

Drift is allowed only when at least one canonical input changed.

OMP must identify the changed category, such as Candidate Pool, authority, verification, rollback, production, runtime, Behavior Chain, CPS, Engineering Chain, Candidate Coverage Matrix, Engineering Value, System Engineering Value, OMP version, or canonical owner pointer.

If OMP cannot identify a changed canonical input, the drift is non-determinism and execution must stop.

## Decision Replay

Replay reconstructs the decision from Decision Trace and canonical input snapshot.

Replay must rebuild:

- Candidate Pool;
- filter stages;
- stage outcomes;
- rejection reasons;
- selection reasons;
- alternative explanations;
- sequence;
- Mission Admission result;
- STOP result;
- Final Verdict.

Allowed replay results:

- `REPLAY_PASS`;
- `REPLAY_FAIL`;
- `REPLAY_BLOCKED_MISSING_INPUT`;
- `REPLAY_NOT_APPLICABLE`.

Replay is audit only. It does not decide, rank, admit, execute, certify, mutate Runtime, expand authority, or create candidates.

## Why New Architecture Was Not Needed

The project already had enough pieces:

- OMP owns candidate sequencing and Mission Admission;
- Decision Trace explains OMP decisions;
- Runtime Model owns decision lifecycle / freshness semantics;
- Execution Mission Protocol owns mission replay after admission;
- Engineering Reports preserve historical evidence;
- Dashboard already has read-only Operator View / Engineering View.

The missing piece was only an OMP-level invariant connecting these existing mechanisms into a reproducibility law. Therefore extension inside OMP was sufficient.

## Reviews

| Review | Verdict | Notes |
| --- | --- | --- |
| Reuse Review | `PASS` | Existing OMP, Runtime Model, Decision Model, Mission Replay, Behavior Enforcement, Execution Certification, and Engineering Report mechanisms reused. |
| Determinism Review | `PASS` | Identical canonical inputs must produce identical outputs; deterministic fingerprint excludes unstable data. |
| Replay Review | `PASS` | Replay reconstructs trace, filters, reasons, sequence, admission, STOP, and verdict as audit only. |
| Decision Audit Review | `PASS` | Decision Trace + Replay answer why, repeatability, inputs, drift, alternatives, and STOP. |
| No Duplicate Responsibility Review | `PASS` | Replay does not replace BDP, OMP Admission, Execution Certification, Runtime, or Dashboard. |
| OMP Review | `PASS` | OMP remains the permanent production execution program and scheduler/optimizer. |
| Quality Review | `PASS` | Law includes canonical inputs, fingerprint rules, drift handling, non-determinism stop, and report linkage. |
| Self Review | `PASS` | No new architecture, Planner, owner, program, model, Replay Engine, Decision Engine, Runtime path, or truth source created. |

## Final Verdict

`PASS`

OMP now has a canonical `Decision Reproducibility Law`.

Every OMP decision must be explainable, reproducible, deterministic, and auditable. If that guarantee fails under identical canonical inputs, OMP must stop with `NON_DETERMINISTIC_DECISION` and route correction through existing owners.
