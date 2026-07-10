# V7 BDP Implementation Candidate Classification Refinement Report

Date: 2026-07-09

Status: `PASS`

Scope:

- Updated only `docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md`.
- Did not change AEP, OMP, Engineering Chain, Runtime, owners, or architecture.
- Created no new program, owner, architecture, Runtime, Planner, or truth source.

## 1. Summary

Behaviour Discovery Program was refined to classify every real `Implementation Candidate Instance` through a deterministic Candidate Classification and Candidate Coverage model.

The refinement makes BDP able to:

- assign exactly one Primary Class to every Implementation Candidate Instance;
- record Secondary Classes without double-counting;
- place every candidate in a Candidate Coverage Matrix;
- determine whether the Execution Certification Ladder can use the candidate as evidence;
- prevent documents, owners, reports, models, sections, rules, Function Graph nodes, or canonical sources from being counted as Candidate Instances;
- identify unmapped engineering situations through `CANDIDATE_CLASS_UNKNOWN_WITH_REASON`.

## 2. Existing Mechanisms Reused

| Existing mechanism | Reused responsibility |
| --- | --- |
| LOCKED_KNOWLEDGE Engineering Entity Model | Confirms `Implementation Candidate Class` and `Implementation Candidate Instance` as existing engineering entities. |
| Engineering Chain Model | Supplies Engineering Intent, affected chain segment, producer, consumer, terminal state, and closure semantics. |
| Existing BDP Implementation Readiness Model | Supplies owner, producer, consumer, scope, verification, rollback, authority, OMP consumer, Codex readiness, and blockers. |
| Existing BDP Automation Readiness Model | Supplies automation status, machine-checkable predicate, execution/verification/rollback/authority blockers. |
| Existing BDP Engineering Logic Coverage Model | Supplies coverage semantics and progress measurement without creating a truth source. |
| OMP Candidate Identity and Admission | Remains responsible for admission after BDP handoff. |
| Action Class / Authority Model | Remains authority classification, not Candidate Classification. |
| Execution Certification Ladder | Supplies Execution Depth and certification compatibility. |

No duplicate gate was created. BDP classifies candidates before handoff; OMP still decides admission.

## 3. World Research Normalization

World research was used to normalize durable engineering patterns, not to copy vendor taxonomies.

Representative sources:

- Kubernetes controller model: current/desired state reconciliation and status loops.
- Google SRE monitoring and automation: observability, actionable signals, automation limits, and operational learning.
- IETF RFC 8326: graceful BGP shutdown as evidence for policy, convergence, drain, and maintenance boundaries.
- Envoy runtime configuration: runtime guards and quick disable paths for risky change.
- NGINX health checks: active/passive upstream health verification.

Normalized V7 patterns:

- observation and evidence refresh;
- interpretation and advisory decision;
- authority and policy boundary;
- packet/lease execution gating;
- runtime/service mutation;
- verification and convergence;
- rollback/containment/recovery;
- consumer confirmation and chain closure;
- learning and maturity feedback;
- canonical sync;
- discovery index and traceability;
- bounded existing-owner implementation;
- architecture boundary / gap proof.

## 4. Added Candidate Classes

The official BDP class list now contains 13 canonical Implementation Candidate Classes:

| Class | Role |
| --- | --- |
| `OBSERVATION_EVIDENCE_REFRESH` | Current evidence production without mutation. |
| `INTERPRETATION_DECISION_ADVISORY` | Evidence interpretation and advisory decision support. |
| `POLICY_AUTHORITY_BOUNDARY` | Authority, policy, allow/stop/hold resolution. |
| `EXECUTION_PACKET_LEASE_GATE` | Exact executable packet / lease / identity binding. |
| `RUNTIME_APPLY_OR_SERVICE_MUTATION` | Bounded runtime or service mutation under authority. |
| `VERIFICATION_TRUTH_CONVERGENCE` | Truth, verification, tests, and convergence proof. |
| `ROLLBACK_CONTAINMENT_RECOVERY` | Rollback, containment, restore, and recovery readiness. |
| `CONSUMER_CONFIRMATION_CHAIN_CLOSURE` | Proof that producer output was consumed and chain closed. |
| `LEARNING_FEEDBACK_MATURITY` | Outcome learning, feedback, and maturity signal. |
| `KNOWLEDGE_CANONICAL_SYNC` | Canonical knowledge synchronization through owners. |
| `DISCOVERY_INDEX_TRACEABILITY` | Discovery index use and traceability without truth creation. |
| `IMPLEMENTATION_OWNER_EXTENSION` | Bounded implementation inside an existing owner. |
| `ARCHITECTURE_BOUNDARY_OR_GAP_PROOF` | Proof that existing architecture cannot express a situation. |

Each class now has a full contract:

- Purpose;
- Typical Engineering Intent;
- Typical Engineering Chain;
- Typical Automation Break;
- Typical Behaviour;
- Typical Verification;
- Typical Terminal State;
- Typical OMP Consumption;
- Typical Execution Certification;
- Production Impact;
- Runtime Impact;
- Authority Boundary.

## 5. Candidate Coverage Matrix

BDP now maintains a Candidate Coverage Matrix:

```text
Y-axis: Implementation Candidate Class
X-axis: Execution Depth L1-L6
```

Allowed cell statuses:

```text
NOT_STARTED
DISCOVERED
IMPLEMENTED
CERTIFIED
PRODUCTION_CERTIFIED
NOT_APPLICABLE
```

Matrix rules prevent false coverage:

- context artifacts cannot fill matrix cells;
- Secondary Classes cannot double-count a candidate;
- `CERTIFIED` requires Behavior Chain completion or legal terminal consumer verification;
- `PRODUCTION_CERTIFIED` requires Production Maturity or production certification evidence;
- the matrix is a BDP progress view, not a truth source.

## 6. No-Gap Result

No real V7 engineering situation was found that cannot map to the official class set.

Situations that appear unmapped must now be handled by:

1. `CANDIDATE_CLASS_UNKNOWN_WITH_REASON`;
2. proof that every existing class fails;
3. artifact-vs-candidate check;
4. existing-owner expression check;
5. only then a future BDP refinement proposal.

This avoids premature class creation while preserving a safe escape path.

## 7. No-Duplication Result

The refinement avoids overlap by selecting Primary Class through dominant engineering responsibility.

Examples:

- authority questions use `POLICY_AUTHORITY_BOUNDARY`, not `RUNTIME_APPLY_OR_SERVICE_MUTATION`;
- packet/lease identity uses `EXECUTION_PACKET_LEASE_GATE`, not generic implementation;
- discovery indexes use `DISCOVERY_INDEX_TRACEABILITY`, but cannot become Candidate Instances by themselves;
- architecture gaps use `ARCHITECTURE_BOUNDARY_OR_GAP_PROOF` as legal stop evidence, not as implementation completion.

## 8. Execution Certification Compatibility

Execution Certification now consumes classified candidates through compatibility rules:

- no-mutation/read-only classes are certifiable through L1-L6 when chain closure exists;
- runtime mutation is limited by authority, rollback, and production boundaries;
- canonical sync requires canonical owner acceptance;
- discovery index evidence is supporting only and cannot be counted as a candidate;
- architecture boundary/gap proof is not implementation evidence, but can be a canonical stop.

This prevents a repeat of the earlier invalid counting pattern where documents or owners were treated as Candidate Instances.

## 9. Sections Strengthened

Updated sections in BDP:

- `Implementation Candidate Instance Schema`;
- `Candidate Reality Gate`;
- new integrated `Implementation Candidate Classification Model`;
- `Validation Model`;
- `Certification Model`;
- `Outputs`;
- `Chain Closure`;
- `Completion Criteria`.

No parallel classification pipeline was added.

## 10. Reviews

| Review | Result |
| --- | --- |
| World Research Review | `PASS` |
| Reuse Review | `PASS` |
| Coverage Review | `PASS` |
| No Gap Review | `PASS` |
| No Duplication Review | `PASS` |
| Candidate Classification Review | `PASS` |
| Execution Certification Compatibility Review | `PASS_WITH_LIMITS` |
| Quality Review | `PASS` |
| Self Review | `PASS` |

`PASS_WITH_LIMITS` for Execution Certification Compatibility means runtime mutation, canonical sync, production maturity, and authority-affecting classes remain bounded by existing owners and existing STOP conditions.

## 11. Final Verdict

`PASS`

BDP now has a complete Implementation Candidate Classification and Candidate Coverage model.

No new architecture was created.

No new owner was created.

No new pipeline was created.

No uncovered real engineering situation remains identified at the time of refinement.

Future BDP runs can classify, cover, and hand off fully classified Candidate Instances to OMP without duplicating OMP admission or Execution Certification responsibility.

## 12. Research Sources

- Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/
- Google SRE Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
- Google SRE Automation at Google: https://sre.google/sre-book/automation-at-google/
- IETF RFC 8326 Graceful BGP Session Shutdown: https://datatracker.ietf.org/doc/html/rfc8326
- Envoy Runtime Configuration: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/operations/runtime
- NGINX HTTP Health Checks: https://docs.nginx.com/nginx/admin-guide/load-balancer/http-health-check/
