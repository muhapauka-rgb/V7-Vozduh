# V7 BDP Engineering Chain Progress Projection Refinement Report

Date: 2026-07-09

Status: `PASS`

Scope:

- Updated only `docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md`.
- Did not change OMP, AEP, Engineering Chain, Runtime, LOCKED_KNOWLEDGE, owners, or architecture.
- Created no Dependency Graph, Progress Graph, Navigation Graph, Relationship Graph, Dependency Model, new owner, new model, new program, or new architecture.

## 1. Summary

Candidate Coverage Matrix and Progress Projection were extended so candidate dependencies are computed through the existing Engineering Chain.

Progress Projection now computes, for every applicable Implementation Candidate:

- `Depends On`;
- `Unblocks`;
- `Critical Path`;
- `Dependency Depth`;
- `Root Cause`;
- `Final Consumer`;
- `System Engineering Value`.

These fields are not a new graph. They are calculated from existing Engineering Chain Walk evidence.

## 2. Reused Mechanisms

| Existing mechanism | Reuse |
| --- | --- |
| LOCKED_KNOWLEDGE Engineering Chain Model | Canonical source for relationship semantics. |
| BDP Engineering Chain Discovery | Existing producer of Chain Walk, Forward Walk, Backward Walk, Middle-Out Walk, and Producer -> Consumer Walk. |
| BDP Progress Projection | Existing computed view over Candidate Coverage Matrix cells. |
| Candidate Coverage Matrix | Existing source of candidate class/depth coverage. |
| Intent Closure | Existing source for goal completion and Automation Break evidence. |
| Verification / Authority / Rollback / Production / Runtime evidence | Existing blocker and advancement evidence. |
| Execution Certification | Existing certification depth evidence. |
| OMP Root Cause / Dependency Review concepts | Reused as consumer-side alignment, not duplicated inside BDP. |

No new dependency mechanism was required because Engineering Chain already defines the canonical producer/consumer relationship model.

## 3. Dependency Calculation

BDP now computes dependency fields through Engineering Chain:

| Field | Calculation |
| --- | --- |
| `Depends On` | Upstream Implementation Candidate Instances or chain conditions required before the candidate can reach Next Status. Derived from Backward Walk and Producer -> Consumer Walk. |
| `Unblocks` | Downstream Implementation Candidate Instances or chain conditions that can advance after the candidate reaches Next Status. Derived from Forward Walk and Producer -> Consumer Walk. |
| `Dependency Depth` | Count of unresolved upstream dependency steps in the Engineering Chain. |
| `Final Consumer` | Terminal chain consumer affected by completion, terminal alternative, or stop. |

BDP must not infer dependencies from:

- name similarity;
- file proximity;
- class similarity;
- document order;
- report wording;
- Function Graph adjacency alone.

Function Graph may support trace evidence only after Engineering Chain Producer -> Consumer evidence confirms the relationship.

## 4. Why No New Dependency Graph Was Needed

Engineering Chain already supplies:

- Producer;
- Consumer;
- Chain Walk;
- Forward Walk;
- Backward Walk;
- Middle-Out Walk;
- Producer -> Consumer Walk;
- Chain Closure;
- Intent Closure;
- terminal state.

A new Dependency Graph would duplicate these semantics and create a second relationship source.

The refinement therefore keeps dependency navigation inside Progress Projection as a computed view over existing Engineering Chain evidence.

## 5. Critical Path Calculation

`Critical Path` is computed as `YES` when the candidate:

- lies on the longest unresolved Engineering Chain path to Production Certification;
- blocks the largest downstream progress path;
- or is the only path to a required Final Consumer.

Otherwise BDP records `NO` with reason.

Critical Path is not a new routing graph and does not grant OMP admission or implementation priority by itself.

## 6. Root Cause Calculation

`Root Cause` is the earliest evidence-backed unresolved blocker in the Backward Walk that prevents downstream progress.

Allowed sources:

- Engineering Chain blocker;
- Intent Closure blocker;
- Verification blocker;
- Authority blocker;
- Rollback / STOP_SAFE blocker;
- Runtime blocker;
- Production blocker;
- Consumer / Chain Closure blocker;
- evidence blocker.

If the root cause cannot be proven, BDP records:

```text
ROOT_CAUSE_NOT_DETERMINED_WITH_REASON
```

BDP must not invent a root cause.

## 7. System Engineering Value

Engineering Value now includes system effect:

```text
System Engineering Value =
  Engineering Value
  + normalized(Unblocked Candidate Count)
  + Critical Path Impact
  + normalized(Root Cause Impact)
```

System Engineering Value remains a navigation metric.

It does not:

- create OMP admission;
- create OMP sequencing;
- create missions;
- mutate backlog;
- assign Codex work;
- mutate Runtime;
- expand authority.

## 8. Project Navigation Capability

BDP can now answer:

- which candidate unblocks the largest number of candidates;
- which candidate lies on the critical path;
- which root cause blocks the largest part of the project;
- which existing owners are bottlenecks;
- which existing consumers stop Engineering Chain closure;
- which verification paths give maximum progress gain;
- which minimal existing work set maximizes maturity gain.

## 9. Reviews

| Review | Result |
| --- | --- |
| Reuse Review | `PASS` |
| Engineering Chain Reuse Review | `PASS` |
| Progress Projection Review | `PASS` |
| Critical Path Review | `PASS` |
| Root Cause Review | `PASS` |
| System Value Review | `PASS` |
| No New Graph Review | `PASS` |
| No New Architecture Review | `PASS` |
| Quality Review | `PASS` |
| Self Review | `PASS` |

## 10. Final Verdict

`PASS`

Candidate Coverage Matrix now shows not only where each candidate stands, but also which existing Engineering Chain relationships block it, what it depends on, what it unblocks, whether it is critical path, and what system-level value it carries.

No new graph or architecture was created.
