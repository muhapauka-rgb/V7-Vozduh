# V7 OMP AEP BDP Alignment Report

Status: `PASS`
Date: `2026-07-09`
Program: `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`

## 1. Summary

Operational Maturity Program was aligned with the current AEP -> BDP -> OMP operating model.

OMP now explicitly consumes accepted Behaviour Discovery Program outputs as implementation input while remaining the only execution operating system of the project.

Canonical chain integrated:

```text
Reality
  -> AEP
  -> Behaviour Discovery Program
  -> Implementation Candidate Catalogue
  -> OMP
  -> Mission
  -> Codex
  -> Implementation
  -> Verification
  -> Reality
```

No new OMP, Backlog, owner, queue, Runtime, Planner, Discovery program, or architecture was created.

## 2. Existing Mechanisms Found

The existing OMP already contained strong mechanisms that covered part of the new model:

| Existing Mechanism | Existing Coverage | Result |
| --- | --- | --- |
| Engineering Control Loop | Already routes work through ECR, Knowledge, OMP, implementation, verification, report, CPS, and continuation. | Extended with BDP candidate consumption and Mission Formation. |
| Behavior Architecture Completion Rule | Already requires producer/consumer closure and behavior change before completion. | Reused for Mission closure. |
| Document Lifecycle Rule | Already classifies implementation artifacts and blocks reports/policies/architecture from generating implementation directly. | Extended to distinguish BDP candidate input from Backlog registry. |
| Implementation Backlog discipline | Already prevents free-form implementation and parallel queues. | Reframed as post-admission Mission/Implementation registry. |
| Product Execution Contract | Already defines OMP as the normal execution workflow after MASTER 4. | Extended with BDP Implementation Candidate and Codex handoff. |
| Resilience Invariants | Already prohibit duplicate OMP, roadmap, queue, runtime, planner, and owner. | Preserved and clarified. |
| Engineering Language | Already defines OMP vocabulary. | Extended with Behaviour Discovery, Implementation Candidate, OMP Mission, and Automation Break. |

No complete BDP Implementation Candidate consumption mechanism existed before this refinement.

## 3. Reused Mechanisms

The refinement reused:

- OMP Engineering Control Loop;
- OMP Document Lifecycle Rule;
- Implementation Backlog / Priority Model;
- Current Program State;
- Behaviour Architecture Completion Rule;
- Product Execution Contract;
- Architecture Closed by Default;
- Existing Owner Check;
- Authority, Verification, Rollback, Runtime, Production, and STOP_SAFE gates;
- Codex execution contract;
- Engineering Report and Canonical Update lifecycle.

## 4. Extended Sections

| Section | Change |
| --- | --- |
| Program introduction | Added V4.1 alignment with AEP and BDP. |
| Continue OMP Engineering Control Loop | Added BDP Implementation Candidate Consumption and Mission Formation. |
| Autonomous Execution Canonical Consumption | Added AEP and BDP as canonical inputs consumed by OMP. |
| Document Lifecycle Rule | Reframed `IMPLEMENTATION` class as approved Mission/Implementation registry. |
| Permanent Rules | Replaced manual backlog-only generation with OMP Mission admission from Backlog, existing owner, or certified BDP Implementation Candidate. |
| BDP Implementation Candidate Consumption Rule | Added canonical OMP admission model for BDP outputs. |
| Product Execution Contract | Added admitted Mission path from BDP candidate to Codex, implementation, verification, and Reality. |
| OMP Engineering Language | Added terms for Behaviour Discovery, Implementation Candidate, OMP Mission, and Automation Break. |
| Resilience Invariants | Clarified Backlog as post-admission registry, not candidate source. |

## 5. How OMP Uses BDP Now

BDP remains the discovery program.

OMP consumes only accepted BDP outputs:

- Implementation Candidate Catalogue;
- Automation Break evidence;
- Engineering Intent;
- Expected Intent Closure;
- Codex Implementation Input;
- Engineering Logic Coverage evidence where relevant.

OMP must run every candidate through:

```text
Implementation Candidate
  -> Candidate Evidence Review
  -> Existing Owner Check
  -> Dependency Review
  -> Authority Review
  -> Verification Review
  -> Rollback / STOP_SAFE Review
  -> Runtime Boundary Review
  -> Production Boundary Review
  -> OMP Admission Decision
  -> Mission or Rejection / Hold
```

Only `MISSION_ACCEPTED` may proceed to implementation.

## 6. Backlog Role

Backlog is no longer described as the source of engineering work.

Backlog is now the post-admission implementation registry:

- it records approved OMP Missions;
- it records implementation state;
- it records owner mapping;
- it records priority;
- it records verification and closure;
- it does not discover candidates;
- it does not replace BDP;
- it does not self-authorize implementation.

This preserves the no-new-queue invariant.

## 7. Codex Role

Codex remains an implementation assistant.

Codex may receive work only through an approved OMP Mission and operator/OMP assignment.

Codex is not:

- a Runtime actor;
- an owner;
- a Planner;
- an authority source;
- a backlog owner;
- a production dependency.

## 8. Continuous Engineering

After Mission completion, OMP can continue through:

```text
Mission Terminal State
  -> Verification
  -> Engineering Report
  -> Current Program State
  -> Reality evidence updated when applicable
  -> BDP refresh when AEP/OMP/operator requires new Behaviour evidence
  -> new Implementation Candidate Catalogue only if BDP produces one
  -> OMP admission
  -> next Mission or terminal stop
```

OMP may request or consume refreshed BDP output, but OMP does not run BDP Discovery and does not automatically create Missions from refreshed candidates.

## 9. Boundary Confirmation

The refinement did not:

- create a new OMP;
- create a new Backlog;
- create a new owner;
- create a new queue;
- create a new Runtime;
- create a new Planner;
- create a new Discovery system;
- create a new architecture;
- change AEP;
- change BDP;
- change locked architecture;
- change locked knowledge.

## 10. Reviews

| Review | Verdict |
| --- | --- |
| OMP Alignment Review | `PASS` |
| BDP Consumer Review | `PASS` |
| Implementation Candidate Review | `PASS` |
| Mission Review | `PASS` |
| Backlog Review | `PASS` |
| Reuse Review | `PASS` |
| Architecture Review | `PASS` |
| No New Owner Review | `PASS` |
| No New Queue Review | `PASS` |
| No New Runtime Review | `PASS` |
| No New Planner Review | `PASS` |
| Quality Review | `PASS` |
| Self Review | `PASS` |

## 11. Final Verdict

```text
OMP_AEP_BDP_ALIGNMENT_PASS
```

OMP now naturally consumes BDP Implementation Candidates through Mission admission while preserving its role as the only execution operating system and preserving Backlog as a post-admission implementation registry.
