# V7 Memory Architecture Discovery

Status: `RESEARCH_DISCOVERY_COMPLETE`
Date: `2026-07-08`
Scope: Existing V7 memory architecture only.

## 1. Purpose

This discovery answers one question:

```text
What memory already exists in V7?
```

This document does not design new memory, create Experience, create a new owner, create storage, create Runtime, create Planner, or create a new architecture.

## 2. Discovery Sources

| Source | Memory Evidence Used |
| --- | --- |
| `LOCKED_KNOWLEDGE` / Canonical Knowledge | Durable accepted engineering truth, provenance, historical/superseded boundary. |
| Canonical Reference / SYSTEM_MAP | Canonical ownership, current source/consumer relationships, document lifecycle, report role. |
| AEP / AOS | Autonomous behaviour, Reality, learning, OMP continuation, current-state and owner boundaries. |
| Behaviour Discovery Program | Behaviour identity, completeness, traceability, truth hierarchy, evolution support. |
| Current Autonomous Behaviour Reality | Behaviour Instance Registry, Behaviour Definition Catalogue, Coverage, Graph, Reality completeness. |
| OMP / CPS | Execution continuation and volatile current-state memory. |
| Runtime Model / Decision Model | Runtime state, decision lifecycle, freshness, packet/lease, verification, rollback, learning-time evidence. |
| Production Maturity Model | Maturity decision memory and current maturity state. |
| Runtime Persistence / Safe State Persistence docs | Authoritative, rebuildable, cached, ephemeral state rules; backup/atomic/audit rules. |
| Long-Term Learning Foundation | Bounded summary memory for transparent learning. |
| Function Graph | Implementation relationship index and historical relationship evidence. |
| Reports / evidence directories | Engineering, production, runtime, verification, rollback, trust, prediction, deployment evidence. |
| Implementation | `admin_core`, `tools`, tests: state readers, archives, snapshots, feedback/trust/prediction, TTL/lease patterns. |

## 3. Memory Inventory

| Memory Type | Purpose | Owner | Producer | Consumer | Lifetime | Freshness | Update Rule | Retention / Cleanup / Archive / TTL | Canonical Status | Evidence Level |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Locked Architecture Memory | Preserve accepted Stage 1 architecture. | Architecture/canonical owner. | Stage 1 certification corpus. | Stage 2, AEP, OMP, future architecture checks. | Permanent until governed architecture change. | Terminal. | Only official architecture-change path. | Historical evidence preserved; current truth is locked state. | Canonical. | Highest architecture truth. |
| Locked Knowledge / Canonical Architecture Knowledge | Permanent engineering memory from Stage 2. | Knowledge owner / canonical owner. | Stage 2 accepted/locked outputs. | OMP, AEP, BDP, engineers, Codex, audits. | Permanent baseline. | Terminal until Knowledge Evolution. | Knowledge Evolution only; no manual rewrite. | History preserved as provenance; superseded history not current truth. | Canonical. | Highest knowledge truth. |
| Canonical Reference Memory | Consolidated canonical project references and owner links. | Canonical Reference owner. | Canonical sync, OMP, engineering reports. | Engineers, OMP, SYSTEM_MAP, certification. | Durable. | Current when synced. | Canonical update after accepted evidence. | Historical reports remain evidence, not canonical truth. | Canonical. | Authoritative reference. |
| SYSTEM_MAP Memory | Owner, producer, consumer, source, and implementation relationship map. | SYSTEM_MAP owner. | Canonical sync, implementation/report updates. | OMP, BDP, AEP, owner lookup, audits. | Durable current map. | Current when updated. | Update when owner/current relationship changes. | Not an archive; points to reports/evidence. | Canonical map. | Owner/source authority, not behavioural truth alone. |
| Current Program State Memory | Current volatile operational/program state. | CPS owner. | OMP, Production Maturity, Engineering Reports. | OMP, dashboard, Product Observation, reports. | Volatile current state. | Must change after safe action or approved execution changing current state. | Update only when volatile operational state changes. | Not durable canonical truth; no independent retention model beyond current-state record. | Non-canonical volatile state. | Current-state evidence. |
| OMP Continuation Memory | Execution route, next action, capability transition, authority/maturity continuation. | OMP. | Engineering Reports, CPS, Production Maturity, owner decisions. | Implementation owners, CPS, Production Maturity, operator. | Durable program route plus current continuation. | Current through CPS/report updates. | Continue OMP after report/canonical/CPS update. | OMP records continuation; reports preserve history. | Canonical execution program. | Governance/continuation truth. |
| Behaviour Reality Memory | Current observed Behaviour Definitions, Instances, Coverage, Graph, Classification, Maturity. | AEP / Behaviour Reality owner path. | Phase 2/BDP discovery evidence. | AEP Phase 3, BDP, OMP, future Reality refinement. | Current Reality artifact; mutable by accepted refinement. | Evidence-scoped; stale/unavailable explicit. | Operator/program acceptance before update. | Unknown, unavailable, historical states recorded explicitly. | Accepted current reality when certified. | Behaviour truth, evidence-backed. |
| Behaviour Discovery Memory | Candidate, identity, completeness, traceability, truth hierarchy, evolution and validation records. | BDP. | BDP runs. | Reality Refinement, AEP, OMP, engineering reports. | Per discovery run plus report evidence history. | Run-scoped. | Discover -> validate -> proposal -> report. | No storage; outputs become reports/evidence and accepted Reality proposals. | Program output, not truth source alone. | Discovery/certification evidence. |
| Runtime Persistent State Memory | Authoritative runtime state surviving restart/backup. | Runtime/state owners. | Provisioning, runtime owners, admin/runtime tools. | Runtime readers, verification, OMP, admin views. | Persistent. | Must be validated after restart/restore. | Backup, atomic replace, validate, audit, rollback pointer. | Backup before dangerous write; corrupt files preserved for manual recovery. | Runtime authoritative state, not canonical docs. | Runtime truth when fresh/validated. |
| Runtime Rebuildable State Memory | Regenerable service matrix, compact quality, route reality, diagnostics, plan previews, path advice. | Existing read-model/snapshot owners. | Observation/read-model tools. | Planner, Runtime gates, admin views, OMP. | Rebuildable and freshness-bound. | Freshness/owner-issued version/lease/source hash where available. | Refresh from authoritative inputs. | Stale state forces refresh/stop; not permanent truth. | Derived read-model. | Strong when fresh and verified. |
| Runtime Cached / Ephemeral Memory | Speed samples, path samples, temporary helpers, PID/in-flight output, transient probes. | Runtime/helper owners. | Runtime/test/probe tools. | Diagnostics/read-only views. | Short-lived. | May disappear or become stale. | Rebuild/reprobe as needed. | May disappear after restart; no canonical retention. | Non-canonical. | Supporting evidence only. |
| Decision State Memory | Decision snapshots, planner decisions, candidate universes, packets, leases, authority generations. | Decision/Runtime/packet/lease owners. | Planner/read-model, packet owner, authority owner. | Runtime validation, OMP, verification, reports. | Valid while material assumptions remain identical. | Invalidated by freshness, material change, authority/rollback/verification mismatch, lease expiry. | Recompute, supersede, stop, consume, expire, reject, archive. | Packet/approval TTL and lease TTL exist; terminal result reuse supports idempotency. | Operational decision state. | Runtime/decision evidence. |
| Verification Memory | Terminal classification, truth/convergence, verification readiness and proof. | Verification owners. | Verification tools/reports/tests. | Production Maturity, CPS, OMP, reports. | Durable as evidence; current when fresh. | Action-specific. | Verify before promotion/consumption. | Reports/evidence directories preserve proof; no universal cleanup found. | Evidence, not owner of truth beyond scope. | High when current and owner-backed. |
| Rollback / Restore Memory | Restore barrier, rollback readiness, rollback/no-rollback evidence, rollback history. | Restore/rollback owners. | Restore barrier tools, execution owners, reports. | Runtime, OMP, verification, engineering reports. | Readiness is freshness-bound; history is evidence. | TTL/generation/restore-settle validity. | Recheck before action; preserve evidence. | Restore barrier/generation expires; reports preserve history. | Operational safety memory. | High for rollback readiness when fresh. |
| Production Evidence Memory | Production observe, convergence, safe deploy, trust inventory, quality, runtime snapshots. | Production/evidence owners. | Safe deploy, observe, truth/convergence, admin/runtime tools. | Production Maturity, OMP, CPS, reports. | Evidence history; current value freshness-bound. | Current/stale/historical explicit. | Produce during deploy/certification/verification. | Evidence directories preserve artifacts; cleanup policy uneven. | Evidence, not canonical truth alone. | High if observed and verified. |
| Engineering Report Memory | Historical engineering evidence, decisions, reviews, no-change, certification, recommendations. | Engineering report lifecycle / OMP. | Codex/engineer execution. | Canonical owners, OMP, CPS, Production Maturity, Learning. | Durable historical evidence. | Historical unless current and accepted. | Create after work/review/certification. | Reports are read only when evidence is required; never backlog/roadmap/truth owner. | Evidence, not durable truth owner. | Medium to high depending traceability. |
| Learning / Outcome Memory | Terminal outcomes, feedback, trust changes, prediction validation, future recommendation quality. | Learning/feedback/trust/prediction owners. | Execution feedback, intelligence workers, trust/prediction tools. | OMP, Production Maturity, Recommendation Intelligence, Behaviour Reality/BDP. | Long-lived but bounded/summary-oriented. | Outcome freshness and evidence quality matter. | Update only from real outcomes; no synthetic evidence. | Long-Term Learning Foundation specifies bounded summaries: hour/day/week/month. | Learning evidence, not authority. | High when real outcome-backed. |
| Trust / Prediction Memory | Trust scores, prediction confidence, forecast validation, drift, confidence history. | Trust/confidence/prediction owners. | Intelligence platform, shadow autonomy, evidence inventories. | Planner advice, OMP, dashboard, reports. | Evolving advisory memory. | Snapshot/freshness/confidence-bound. | Update from observed outcomes, comparisons, prediction-vs-reality evidence. | Snapshot/history exists; bounded windows appear in summaries; no universal retention policy found. | Advisory, not authority. | Supporting evidence; must not certify without outcome. |
| Deployment / Release Memory | Safe deploy manifests, release manifests, runtime snapshot path/seed, convergence evidence. | Safe deploy / deployment owner. | Deploy tools and reports. | Runtime truth, OMP, Production Maturity, engineering reports. | Release/evidence history durable; runtime snapshot current. | Current through convergence/truth checks. | Safe deploy -> convergence -> report. | Archive-only safety patterns exist; cleanup forbidden without replacement release in repo diff logic. | Evidence/release state. | High when convergence verified. |
| Function Graph Memory | Static relationship index: producers, consumers, mutation paths, tests, systemd, closures. | Function Graph owner. | Function graph generation. | BDP, AEP Phase 2, engineers. | Snapshot/index artifact. | Stale if implementation changes. | Regenerate/update when implementation relationships change. | `.md`/`.json` report artifacts preserve historical graph. | Discovery index, not truth source. | Supporting/index evidence. |
| Policy / ADR / Historical Memory | Decisions, policies, superseded context, historical warnings. | Policy/ADR owners. | ADR/policy process and reports. | OMP, engineers, canonical owners. | Durable history. | Current or superseded explicit. | ADR update/new ADR for changed decisions. | Superseded history preserved but not current truth. | Canonical if active; historical if superseded. | Governance evidence. |

## 4. Memory Owners

| Owner | Memory Owned |
| --- | --- |
| Canonical owners | Locked architecture, locked knowledge, canonical reference, active ADR/policy truth. |
| SYSTEM_MAP owner | Owner/source/consumer relationship memory. |
| OMP | Execution continuation, capability transition, mission/next-action governance memory. |
| CPS | Volatile current program/product/operational state. |
| Production Maturity | Maturity decision memory and maturity-state outputs. |
| Runtime/state owners | Persistent runtime state, rebuildable state, cached state, ephemeral state. |
| Decision/packet/lease owners | Decision snapshots, packets, leases, authority generations. |
| Verification owners | Truth/convergence/terminal proof memory. |
| Rollback/restore owners | Restore barrier and rollback/no-rollback evidence. |
| Learning/trust/prediction owners | Outcome feedback, trust evolution, prediction validation. |
| Engineering report lifecycle | Historical evidence and certification reports. |
| BDP / AEP Reality owners | Behaviour discovery and current autonomous behaviour reality artifacts. |
| Function Graph owner | Relationship index memory. |

## 5. Memory Producers And Consumers

| Producer | Produced Memory | Consumers |
| --- | --- | --- |
| Engineering Reports | Evidence, certification results, review outcomes, no-change decisions. | Canonical owners, OMP, CPS, Production Maturity, Learning. |
| Runtime/read-model tools | Runtime state, observations, snapshots, freshness/readiness. | Planner, Runtime gates, OMP, admin views, reports. |
| Safe deploy / convergence tools | Deployment state, release/convergence evidence. | Production Maturity, OMP, reports, canonical sync if durable. |
| Verification tools | Terminal proof, truth/convergence, scoped verification. | OMP, Production Maturity, CPS, reports. |
| Rollback/restore tools | Restore barrier, rollback readiness, rollback/no-rollback proof. | Runtime, OMP, reports. |
| Feedback/intelligence workers | Outcome, learning, trust/prediction updates. | OMP, planners/read models, Production Maturity, reports. |
| BDP/AEP | Behaviour candidates, Reality proposals, Behaviour Reality. | AEP Phase 3, OMP, future Reality refinement. |
| Stage 2 / Knowledge Evolution | Locked knowledge and future knowledge changes. | OMP, AEP, BDP, engineers. |

## 6. Memory Lifetime

| Lifetime Class | Examples | Rule |
| --- | --- | --- |
| Permanent canonical | Locked Architecture, Locked Knowledge, Canonical Reference, active ADR/policy. | Changes only through governed canonical/knowledge/architecture path. |
| Durable evidence history | Engineering reports, production evidence, verification/rollback/deploy reports. | Preserved as evidence; not current truth by default. |
| Volatile current state | CPS, current maturity/blocker/next action. | Current only; not durable canonical truth. |
| Freshness-bound operational state | Decision snapshots, packets, leases, readiness, restore barrier, runtime snapshots. | Valid while material assumptions remain unchanged and TTL/freshness gates pass. |
| Rebuildable derived state | Service matrix, quality compact, route reality, diagnostics, plan previews. | Refresh/rebuild from authoritative inputs. |
| Cached/ephemeral | Probe output, PID files, temporary helper outputs. | May disappear; never canonical. |
| Bounded learning summaries | Long-term learning hour/day/week/month summaries. | Transparent summaries; not opaque ML. |

## 7. Memory Lifecycle

Observed V7 memory flow:

```text
Runtime / Production / Engineering Event
  -> Observation / Runtime State / Evidence
  -> Verification / Rollback / Terminal Classification
  -> Engineering Report
  -> Production Maturity Decision when applicable
  -> Current Program State volatile update when applicable
  -> OMP continuation
  -> Learning / Trust / Prediction update when real outcome exists
  -> Canonical Sync / Knowledge Evolution only when durable truth changes
```

Behaviour-specific flow:

```text
Observed Behaviour Evidence
  -> BDP Candidate / Identity / Traceability / Truth Hierarchy
  -> Behaviour Reality Refinement Proposal
  -> Acceptance / Reality update if approved
  -> OMP / AEP consumer path
  -> Learning / Experience evidence when real outcomes exist
  -> Knowledge Evolution only if canonical knowledge changes
```

## 8. Memory Retention

| Mechanism | Retention Finding |
| --- | --- |
| Canonical memory | Permanent until governed change; history preserved as provenance only. |
| Reports/evidence directories | Durable historical evidence; no universal cleanup TTL found. |
| CPS | Current-state surface; volatile, not canonical. |
| Runtime persistent state | Survives restart; backup/restore required for dangerous writes. |
| Runtime rebuildable/cached state | Refresh/rebuild; freshness-bound. |
| Decision/packet/lease | TTL and material-identity invalidation exist. |
| Capacity/action-class metadata | TTL/stale/expiration patterns exist in productization evidence. |
| Learning summaries | Bounded summaries: last hour/day/week/month. |
| Trust/prediction snapshots | Snapshot and history mechanisms exist; retention is family-specific. |

## 9. Memory Cleanup

Cleanup is not a single global service.

Observed cleanup / expiration mechanisms:

- runtime ephemeral state may disappear after restart;
- stale runtime/readiness evidence blocks mutation and requires refresh;
- packet/approval/lease TTL expires operational eligibility;
- capacity expiration/stale-after patterns exist in productization evidence;
- reports and canonical history are preserved, not cleaned as active state;
- repo diff logic treats cleanup as archive-only/freeze unless replacement release is verified;
- corrupt critical state must be preserved for manual recovery, not silently regenerated;
- bounded learning summaries imply aggregation/compaction, not deletion of canonical evidence.

Gap:

```text
UNIFIED_RETENTION_CLEANUP_POLICY_NOT_FOUND
```

This is not a proof that a new memory architecture is required. It means retention/cleanup rules are distributed by owner and unevenly formalized.

## 10. Memory Relationships

| Relationship | Meaning |
| --- | --- |
| Runtime State -> Evidence | Runtime/read-only observations become evidence when captured with owner/freshness/provenance. |
| Evidence -> Verification | Evidence must be verified before promotion/consumption. |
| Verification -> Report | Terminal proof is preserved in engineering/production reports. |
| Report -> Production Maturity | Maturity consumes certified reports and decides accept/partial/block/no-change/invalid. |
| Production Maturity -> CPS | CPS records volatile current state when maturity/current context changes. |
| Report -> Learning | Reports/outcomes may trigger learning/trust/prediction update. |
| Report -> Canonical Sync | Durable accepted conclusions may update canonical owners. |
| Behaviour Evidence -> Behaviour Reality | BDP/AEP convert observed behaviour evidence into current reality only after validation/acceptance. |
| Function Graph -> Discovery | Function Graph helps find relationships but does not create truth. |

## 11. Memory Hierarchy

| Rank | Memory | Authority |
| --- | --- | --- |
| 1 | Locked Architecture / Locked Knowledge | Highest stable truth inside their scope. |
| 2 | Active Canonical Reference / SYSTEM_MAP / active ADR/policy | Authoritative current references and owner maps. |
| 3 | Observed verified production/runtime evidence | Strongest current operational truth. |
| 4 | Verified implementation/tests/evidence reports | Engineering evidence, scoped by provenance. |
| 5 | Current Program State / Production Maturity current outputs | Current operational/maturity state, not canonical truth. |
| 6 | Behaviour Reality | Accepted current behaviour reality, evidence-backed. |
| 7 | Learning/trust/prediction summaries | Advisory learning memory from real outcomes. |
| 8 | Historical reports/superseded evidence | Historical/provenance only unless revalidated. |
| 9 | Hypothesis/synthetic/architecture-only expectation | Cannot prove current Behaviour or production capability. |

## 12. Potential Place For Long-Term Behaviour Experience

Long-term Behaviour Experience should not be created as a new owner or store by this discovery.

Existing natural placement already exists through a composition:

```text
Observed Behaviour Instance
  -> Evidence / Verification / Outcome
  -> Engineering Report
  -> Learning / Trust / Prediction summaries
  -> Behaviour Reality / BDP traceability
  -> Production Maturity / CPS if current state changes
  -> Knowledge Evolution / Canonical Knowledge only if durable truth changes
```

Best existing mechanisms:

| Mechanism | Why It Fits |
| --- | --- |
| Learning / Outcome Memory | Stores real outcome-backed feedback and trust/prediction evolution. |
| Engineering Report Memory | Preserves evidence and decision context. |
| Behaviour Reality / BDP Traceability | Links behaviour identity, instances, evidence, implementation, verification, Reality, and consumers. |
| Production Maturity | Consumes certified evidence and records maturity impact. |
| Knowledge Evolution | Promotes durable accepted lessons only when they become canonical knowledge. |

Verdict:

```text
EXISTING_EXTENSION_POINT_FOUND
```

No new Behaviour Experience owner or memory architecture is required to locate long-term Behaviour Experience.

## 13. Memory Gaps

| Gap | Evidence | Impact | Required Kind Of Response |
| --- | --- | --- | --- |
| Unified retention/cleanup policy not found | Retention/TTL appears per owner: runtime TTL/lease, capacity expiration, learning summaries, reports as durable history. | Cross-family retention may be inconsistent. | Existing-owner policy/schema clarification if needed; not new architecture. |
| Behaviour Experience not present as a named canonical object | Existing learning/report/BDP/Reality/Knowledge paths can host it compositionally. | Operators may ask where long-term experience lives. | Use existing mechanisms; only formalize through existing owners if later required. |
| Cleanup/archive unevenly formalized | Archive-only patterns exist; corrupt state preserved; evidence dirs are durable, but global cleanup not found. | Storage hygiene may be operationally manual. | Existing evidence/report/runtime owner review. |
| Live runtime state unavailable in repository-only discovery | Discovery used repo/evidence snapshots, not live host state. | Current production memory may differ from repository evidence. | Runtime owner live verification if operational decision requires it. |

## 14. Potential Extension Points

These are not new designs. They are existing places where memory discipline can be extended if OMP later approves:

- BDP Traceability / Evolution matrices;
- Learning / Outcome summaries;
- Engineering Report schema;
- Production Maturity evidence economy;
- CPS current-state fields;
- Knowledge Evolution path;
- Runtime/Decision packet, lease, freshness, and TTL metadata;
- Function Graph refresh lifecycle;
- SYSTEM_MAP owner/source rows.

## 15. Independent Certification

| Review | Verdict | Notes |
| --- | --- | --- |
| Memory Architecture Review | `PASS` | Existing memory is multi-layered and owner-mapped; no new architecture required by this discovery. |
| Reuse Review | `PASS` | Canonical, CPS, Runtime, reports, learning, maturity, BDP, AEP, Function Graph, and SYSTEM_MAP mechanisms were reused. |
| Reality Review | `PASS_WITH_MINOR_RISKS` | Repository/evidence reality is strong; live runtime state was not queried. |
| Evidence Review | `PASS` | Findings are based on canonical docs, current programs, reports, implementation references, and evidence directories. |
| Owner Review | `PASS` | Existing owners cover memory families. No new owner created. |
| Duplication Review | `PASS` | No new store, owner, Runtime, Planner, or architecture proposed. |
| Quality Review | `PASS_WITH_MINOR_RISKS` | Retention/cleanup unevenness is explicitly recorded. |
| Self Review | `PASS` | Discovery stayed within requested boundaries. |

## 16. Final Answer

Existing V7 memory architecture is sufficient at the architecture/owner level to support long-term accumulation of Behaviour Experience through existing mechanisms.

However, support is compositional, not a single named `Experience` store.

```text
MEMORY_ARCHITECTURE_SUFFICIENT_FOR_BEHAVIOUR_EXPERIENCE_VIA_EXISTING_OWNERS
```

The only proven need is targeted strengthening of existing-owner retention/cleanup/summary discipline if future OMP work requires more formal long-term Behaviour Experience operations.

```text
NO_NEW_MEMORY_ARCHITECTURE_REQUIRED
NO_NEW_OWNER_REQUIRED
NO_NEW_STORAGE_REQUIRED
```
