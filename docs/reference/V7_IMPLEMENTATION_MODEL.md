# V7 Implementation Model

Status: canonical
Program: `V7.IMPLEMENTATION.PROGRAM`
Need New Owner: FALSE

Supersession note:
`docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` Version `4.0` is the single permanent production execution program for V7. This model remains a supporting implementation reference under OMP and must not be used as a separate roadmap authority.

## Purpose

V7 Implementation Model defines how implementation work is selected, prioritized, finished, and fed back into OMP.

Architecture is complete.
Future work is implementation-first.

This model does not implement runtime code, daemon, timer, apply, user movement, planner redesign, governance redesign, execution redesign, truth-source creation, synthetic evidence, or architecture research.

## Selection Rule

Implementation work is selected by Production Leverage.

Production Leverage means:

```text
production autonomy gain
  + safety gain
  + verifiability gain
  + learning gain
  + operator effectiveness gain
  + implementation readiness gain
  - risk
  - effort
```

The selected task must:

1. address the current bottleneck or nearest safe implementation blocker;
2. reuse an existing owner;
3. avoid forbidden boundaries;
4. be testable;
5. be verifiable;
6. move V7 closer to Production Autonomy.

## Prioritization Rule

Implementation work is prioritized in this order:

1. Existing owner implementation.
2. Existing owner integration.
3. Existing owner optimization.
4. Read-model improvements.
5. Testing.
6. Certification.

The optimizer must not choose architecture redesign unless implementation evidence proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Implementation Classes

Each task must be classified as one primary implementation class:

- `IMPLEMENT_RUNTIME`
- `IMPLEMENT_BACKGROUND`
- `IMPLEMENT_READ_MODEL`
- `IMPLEMENT_TEST`
- `IMPLEMENT_VERIFICATION`
- `IMPLEMENT_OBSERVABILITY`
- `IMPLEMENT_UI`
- `IMPLEMENT_DOCUMENTATION`
- `IMPLEMENT_CERTIFICATION`

Classification happens before code changes.

## Semantic Reuse Rule

Before implementation:

1. find the existing owner;
2. find semantically equivalent owners;
3. find whether a composition of existing owners already implements the capability;
4. estimate semantic coverage;
5. set `Need New Owner`;
6. choose `REUSE`, `EXTEND`, `MERGE`, or `CREATE_NEW`.

`CREATE_NEW` is allowed only when `Need New Owner = TRUE`.

## Finish Rule

Implementation work finishes only after:

1. code is implemented or the task stops at an allowed stop condition;
2. focused tests are run;
3. verification is run;
4. truth passes;
5. convergence passes;
6. certification is recorded when required;
7. Current Program State is updated if bottleneck, HLA, authority boundary, metrics, packet, or stop reason changed;
8. OMP is updated only if scheduler/optimizer meaning changed;
9. Canonical Reference, SYSTEM_MAP, or ADRs are updated if system meaning changed.

## OMP Update Rule

Implementation updates OMP when one of these changes:

- implementation optimizer question;
- implementation prioritization;
- implementation classes;
- stop conditions;
- new-owner gate;
- duplicate detector;
- current highest implementation leverage;
- production leverage calculation.

Implementation does not update OMP merely because code changed.
Routine volatile state belongs in Current Program State.

## Current Highest Implementation Leverage

Current HIL is volatile state and lives in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

This model defines how OMP selects implementation work; it does not preserve an independent current-task queue.

## Recommended First Coding Task

Read OMP and Current Program State, then execute the current OMP-selected highest implementation leverage task unless it crosses an allowed stop condition.

Required output fields:

- lifecycle id;
- decision id;
- operation id;
- packet id;
- idempotency key fingerprint;
- current state generation;
- selected move hash;
- runtime stage;
- stage owner;
- input generation;
- stop reason;
- authority status;
- packet freshness;
- duplicate work status;
- loop guard status;
- verification status;
- rollback status;
- outcome status;
- learning status;
- OMP notification status.

The implementation must not apply, move users, write restore barrier, enable daemon/timer, mutate event consumers, or create a truth source.
