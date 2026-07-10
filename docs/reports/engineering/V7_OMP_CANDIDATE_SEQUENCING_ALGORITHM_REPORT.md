# V7 OMP Candidate Sequencing Algorithm Report

Date: 2026-07-10

Status: `PASS`

Scope:

- Updated only `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`.
- Did not change BDP, AEP, Runtime, owners, Current Program State, or architecture.
- Created no Planner, architecture, owner, program, queue, Runtime, or new entity.

## 1. Summary

OMP now contains a canonical `OMP Candidate Sequencing Algorithm`.

The algorithm selects the best implementation sequence from existing `Implementation Candidate Instance` records using certified BDP outputs and existing OMP gates.

It does not select by manual priority.

It does not create a Planner.

## 2. World Research Principles

World research across mature systems was normalized into V7 principles:

| Mature systems | Universal principle |
| --- | --- |
| Kubernetes Scheduler / scheduling framework | Filter feasible options before scoring; score only surviving options; reserve before bind; unreserve on failure. |
| Kubernetes Controllers | Continuously compare desired/current state and reconcile only through declared state and owner paths. |
| Google SRE | Automation must be scoped, consistent, and applied judiciously; monitoring must provide actionable signals. |
| BGP / IETF RFC 4271 | Decision process separates preference calculation, best route selection, and dissemination; ineligible routes do not proceed. |
| Envoy | Runtime guards allow risky behavior to be disabled quickly without new architecture. |
| NGINX / load balancers | Health checks and readiness gates prevent unsafe traffic placement. |
| Traffic engineering / routing systems | Policy, reachability, convergence, stability, and tie-breaking precede final placement. |

Canonical V7 principle:

```text
Eligibility and safety first.
Value only after eligibility.
Sequence before execution.
Mission Admission before implementation.
Verification before certification.
```

## 3. Reused OMP / V7 Mechanisms

| Existing mechanism | Reuse |
| --- | --- |
| BDP Implementation Candidate Consumption Rule | Existing BDP -> OMP boundary. |
| BDP-Derived Execution Sequencing Rule | Existing location for the algorithm. |
| Mission Admission | Legal boundary before implementation. |
| Behavior Enforcement Framework | Verifies Behavior Chain completion. |
| Architecture Closed by Default | Prevents Planner / architecture creation. |
| Execution Certification | Consumes completed evidence; not duplicated by sequencing. |
| Candidate Coverage Matrix | Supplies class/depth coverage state. |
| Progress Projection | Supplies next state, remaining path, blockers. |
| Engineering Chain Dependency Projection | Supplies Depends On, Unblocks, Critical Path, Root Cause, Final Consumer. |
| Engineering Value / System Engineering Value | Supplies computed value without manual priority. |
| Verification / Rollback / Authority / Runtime / Production boundaries | Supply hard filters and STOP conditions. |

## 4. Resulting Algorithm

Canonical OMP Candidate Sequencing Algorithm:

```text
Candidate Pool
  -> Validity Filter
  -> Safety Filter
  -> Authority Filter
  -> Runtime Filter
  -> Rollback / STOP_SAFE Filter
  -> Dependency Ordering
  -> Critical Path Detection
  -> Coverage Optimization
  -> Engineering Value Evaluation
  -> System Engineering Value Evaluation
  -> Sequence Optimization
  -> Mission Admission
  -> Execution / Hold / Rejection / Not Applicable
```

The algorithm chooses a sequence, not just one candidate.

## 5. Why Better Than Simple Priority

Simple priority fails because it can rank unsafe, unauthorized, blocked, or downstream work above necessary upstream work.

The OMP algorithm:

- removes invalid candidates before scoring;
- blocks unsafe candidates before scoring;
- stops at authority/runtime/rollback/production boundaries;
- orders dependencies through Engineering Chain evidence;
- accounts for candidates that unblock other candidates;
- accounts for critical path;
- evaluates direct and system engineering value;
- produces a Mission Admission input, not execution permission.

## 6. Why No Planner Was Needed

OMP already owns:

- scheduling / optimization;
- Mission Admission;
- candidate consumption;
- authority handling;
- verification and certification path;
- Current Program State continuation;
- stop conditions.

BDP already produces:

- candidates;
- coverage;
- progress;
- dependency projection;
- value.

A new Planner would duplicate OMP's existing execution responsibility and violate Architecture Closed by Default.

## 7. Sequence Decision Output

OMP must now answer:

- which candidate executes first;
- why;
- what it unblocks;
- what happens after execution;
- how Candidate Coverage Matrix changes;
- how Engineering Maturity changes;
- how Production Maturity changes;
- which candidates become available;
- which candidates remain blocked;
- which STOP applies.

## 8. Reviews

| Review | Result |
| --- | --- |
| World Research Review | `PASS` |
| Reuse Review | `PASS` |
| Algorithm Review | `PASS` |
| No Planner Review | `PASS` |
| No Duplicate Responsibility Review | `PASS` |
| Execution Review | `PASS` |
| Quality Review | `PASS` |
| Self Review | `PASS` |

## 9. Final Verdict

`PASS`

OMP now has a canonical Candidate Sequencing Algorithm that uses existing BDP data and OMP gates to compute the best implementation sequence without creating a new Planner, architecture, owner, queue, Runtime, or program.

## 10. Research Sources

- Kubernetes Scheduler: https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/
- Kubernetes Scheduling Framework: https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/
- Google SRE Automation at Google: https://sre.google/sre-book/automation-at-google/
- Google SRE Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
- IETF RFC 4271 BGP-4: https://datatracker.ietf.org/doc/html/rfc4271
- Envoy Runtime Configuration: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/operations/runtime
- NGINX HTTP Health Checks: https://docs.nginx.com/nginx/admin-guide/load-balancer/http-health-check/
