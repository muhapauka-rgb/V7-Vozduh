# V7 Vozduh - Current Reality Documentation

Date: 2026-06-04

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Current production-aligned commit: `67ee9965f4d759f9a9d0bb90b893a9c024701307`

This document describes the current proven state of the V7 Vozduh project: what really exists, how it works, what is production-confirmed, what is local/report-only, what functions are working, and what remains to do.

## 1. Short Human Summary

V7 Vozduh is no longer just a collection of scripts. It is a governed runtime control plane for user routing across egress channels, with:

- a runtime planner/executor;
- admin control surface;
- governance and approval packet flow;
- restore-barrier and generation checks;
- rollback certification;
- audit and closure records;
- service-aware routing;
- capacity-aware routing;
- Routing Intelligence advisory layer;
- intelligence snapshot subsystem;
- safe deploy and convergence verification tooling.

The most important current fact:

`CONV.2` proved that local, GitHub, and production are aligned at commit `67ee9965f4d759f9a9d0bb90b893a9c024701307`.

`v7-truth-check --all` returned `PASS / FULLY_ALIGNED`.

`v7-convergence-status` returned `PASS / ALIGNED`.

Therefore the old Z9 NO-GO confusion is superseded by later certified C.2, D.1, CONV.1, and CONV.2 results.

## 2. Current Git And Workspace Reality

Current branch:

```text
Updatesystem
```

Current aligned production commit:

```text
67ee9965f4d759f9a9d0bb90b893a9c024701307
```

Important note:

At the time this document was prepared, CONV.2 report/evidence files were staged but not committed:

- `PROGRAM_CONV2_PRODUCTION_ALIGNMENT_AND_PERF4_CONVERGENCE_REPORT.md`
- `conv2_evidence/*`
- `z8_11-evidence/runtime_convergence_snapshot.json`

They were intentionally not committed during CONV.2 because a new documentation commit would make local/GitHub ahead of production and would break the freshly proven alignment.

This is not a runtime problem. It is a release-process detail.

## 3. Canonical Truth Model

The canonical development workspace is:

```text
/Users/ponch/Documents/New project
```

The canonical working branch is:

```text
Updatesystem
```

The canonical deploy source is:

```text
origin/Updatesystem
```

The canonical safe deploy tool is:

```text
tools/v7-safe-deploy
```

The canonical truth gate is:

```text
tools/v7-truth-check
```

The canonical convergence view is:

```text
tools/v7-convergence-status
```

The canonical runtime fingerprint is:

```text
/opt/v7/runtime-fingerprint.json
```

The production runtime root is:

```text
/opt/v7
```

The runtime state root is generally:

```text
/opt/v7/egress/state
```

The intelligence snapshot root is:

```text
/opt/v7/egress/state/intelligence
```

## 4. Production Alignment Status

CONV.2 certified:

```text
perf4_deployed=true
runtime_fingerprint_active=true
snapshot_subsystem_verified=true
truth_check_pass=true
local_github_aligned=true
github_production_aligned=true
local_github_production_aligned=true
safe_to_begin_RI4=true
```

Production deploy identity:

```text
deploy-z8-14-Updatesystem-67ee996-20260603T170801
```

Production is deployed to:

```text
67ee9965f4d759f9a9d0bb90b893a9c024701307
```

Runtime fingerprint is active at:

```text
/opt/v7/runtime-fingerprint.json
```

The PERF.4 snapshot subsystem was verified on production. The refresh CLI generated six required snapshot files:

- `service-scores.json`
- `channel-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `overview-summary.json`

The refresh operation reported:

```text
runtime_behavior_changed=false
governance_behavior_changed=false
users_moved=false
warnings=[]
snapshot_count=6
```

Known follow-up:

`v7-intelligence-snapshot-refresh.service` and `v7-intelligence-snapshot-refresh.timer` are not installed yet. That is now a known follow-up, not an alignment blocker.

## 5. Runtime Ownership Model

The project does not have a separate new full Runtime Orchestrator service.

It has an existing partial orchestrator ownership chain:

```text
systemd/v7-users-autoswitch.timer
  -> systemd/v7-users-autoswitch.service
  -> tools/v7-users-autoswitch
  -> v7-user-switch
  -> verification / rollback
  -> audit
  -> closure / operator observability
```

The primary runtime owner is:

```text
tools/v7-users-autoswitch
```

This tool owns:

- runtime planning;
- selected move generation;
- selected move hashing;
- restore-barrier enforcement;
- generation checks;
- service-aware candidate evaluation;
- capacity-aware candidate evaluation;
- dynamic blast radius evidence;
- bounded apply when explicitly allowed;
- verification;
- rollback-on-verify-fail branch;
- runtime terminal result.

The design conclusion from Z6:

Do not create a parallel orchestrator.

Future orchestration work must extend and formalize the existing autoswitch-centered chain.

## 6. Runtime Cycle

Normal runtime cycle:

1. Signal tools refresh state and health evidence.
2. `v7-users-autoswitch.timer` starts the runtime cycle.
3. `v7-users-autoswitch.service` invokes the runtime tool.
4. `tools/v7-users-autoswitch` reads runtime truth:
   - users registry;
   - egress registry;
   - policy;
   - org policy;
   - service matrix;
   - quality summaries;
   - restore barrier;
   - safety state;
   - reconnect state;
   - intelligence snapshots where active.
5. The planner computes candidate decisions.
6. It selects bounded moves.
7. It computes selected move hash and generation facts.
8. If dry-run/no-op/blocked, it exits without mutation.
9. If apply is explicitly allowed and all gates pass, it calls `v7-user-switch`.
10. It verifies routes.
11. If verification fails and rollback branch applies, it rolls back the affected move.
12. It emits terminal JSON.
13. Audit and closure surfaces record/observe the result.

## 7. Governance And Safety

Normal movement is supposed to pass through:

```text
planner -> selected moves -> restore barrier/generation clearance -> governance approval -> runtime apply -> verify -> audit -> closure
```

Important certified safety properties:

- selected moves are bounded;
- generation drift can block execution;
- selected move hash mismatch can block execution;
- stale or missing restore-barrier clearance can block execution;
- missing governance packet can block execution;
- rollback packet absence blocks rollback execution;
- expired or unsafe intelligence snapshots can suppress selected moves;
- direct runtime mutation is not part of safe release/deploy flow.

Known risk:

There are still break-glass/manual paths in Admin and runtime tools. They are useful for emergency operations but must not become normal execution authority.

## 8. Rollback Status

C.2 certified a complete one-user lifecycle:

```text
Operation -> Execution -> Verification -> Audit -> Closure -> Rollback -> Rollback Audit -> Rollback Closure
```

Certified movement:

```text
10.0.0.2: awg3 -> vless -> awg3
```

C.2 final facts:

```text
one_user_execution_completed=true
rollback_completed=true
full_operation_lifecycle_certified=true
safe_to_continue_to_PROGRAM_D=true
Final status=PASS
```

This supersedes the old Z9 NO-GO reports for one-user lifecycle certification.

## 9. Runtime Platform Certification

D.1 certified the runtime platform:

```text
runtime_platform_certified=true
production_runtime_certified=true
```

Certified blast radius behavior:

- blast radius 5: PASS;
- blast radius 10: PASS;
- dynamic max-25 ceiling: PASS as 15 affected users under a max-25 governance ceiling.

D.1 also certified:

- service-aware routing;
- capacity-aware routing;
- best available pool selection;
- fail-closed behavior;
- governance ceiling expansion through policy, not bypass.

Important nuance:

The 25 phase did not move 25 fake users. Production had 18 active users and 15 affected candidate moves, so the max-25 ceiling was certified as 15/15 affected candidates under a 25 cap.

## 10. Routing Intelligence

Routing Intelligence is not the runtime authority.

It is an advisory intelligence layer.

RI.1 created the foundation:

- service history store;
- service intelligence engine;
- user service weights;
- execution trust model;
- dynamic blast radius model;
- prediction foundation, disabled;
- shadow replay CLI.

RI.2 connected those pieces into the Routing Brain:

```text
Raw runtime data
  -> service history
  -> service intelligence
  -> user weights
  -> execution trust
  -> dynamic blast advice
  -> planner advisory context
```

RI.3 integrated advisory scores into the runtime planner ranking path, while preserving authority:

```text
Routing Brain advises.
Planner decides.
Governance authorizes.
Runtime executes.
Audit records.
Closure records.
```

RI cannot:

- create candidates;
- approve execution;
- write selected moves;
- bypass hard gates;
- bypass governance;
- move users;
- mutate runtime state.

## 11. Performance And Intelligence Snapshots

PERF.1 defined the architecture:

```text
Brain may be heavy.
Runtime may not be heavy.
```

PERF.2 created the Intelligence Snapshot Store contract:

```text
/opt/v7/egress/state/intelligence/
```

Snapshot envelope fields include:

- schema;
- generated_at;
- expires_at;
- ttl_seconds;
- freshness_state;
- confidence;
- source_hashes;
- generator;
- item_count;
- warnings.

PERF.3 created Heavy Brain snapshot producers:

- service scores;
- channel service scores;
- trust summaries;
- risk summaries;
- blast radius summaries;
- overview summaries.

PERF.4 integrated runtime fast-path snapshot consumption into:

```text
tools/v7-users-autoswitch
```

When snapshots are valid:

- runtime consumes compact snapshot files;
- runtime avoids constructing heavy Routing Brain in the hot path;
- runtime avoids reading runtime history in the snapshot-backed path.

When snapshots are unsafe:

- selected moves are suppressed;
- terminal reason becomes snapshot-stop related;
- governance/execution/rollback are not touched.

Production confirmation:

CONV.2 proved PERF.4 is deployed and snapshot subsystem is verified.

## 12. Admin API Reality

The Admin API is still a large monolith:

```text
admin/v7-admin-api: 35747 lines
```

Current endpoint inventory:

```text
endpoint_count=264
GET=118
HEAD=8
POST=138
public=19
auth_required=245
csrf_required=133
safe_mode_blocked=86
read_api=109
action=133
page=14
public_api=3
public_delivery=5
critical_risk=13
high_risk=95
medium_risk=38
low_risk=118
```

What Admin API still owns:

- HTTP request routing;
- auth/RBAC/CSRF/session context;
- command read boundaries;
- action handlers;
- governance mutation surfaces;
- rollback/execution action surfaces;
- audit and closure writer calls;
- UI shell.

What has already been safely extracted into `admin_core`:

- registry read views;
- operator read views;
- service views;
- route views;
- summary builders;
- overview request snapshot foundation;
- performance summaries;
- runtime read views;
- route reality views;
- diagnostic views.

API.1 to API.5 completed the read-only decomposition track.

The monolith is still a problem, but not an immediate emergency. The safe strategy is staged extraction, read-only first, with endpoint parity tests after every step.

## 13. Admin Core Modules

Current important `admin_core` modules:

- `admin_core/operator_execution.py`: governance/approval packet model and recheck logic.
- `admin_core/operator_observability.py`: operator timeline, audit, evidence, operation detail.
- `admin_core/routing_intelligence.py`: RI foundation models.
- `admin_core/routing_brain.py`: advisory Routing Brain.
- `admin_core/intelligence_snapshots.py`: snapshot contracts and readers.
- `admin_core/intelligence_workers.py`: snapshot producers.
- `admin_core/admin_registry_views.py`: read-only registry serializers.
- `admin_core/operator_views.py`: operator read view facade.
- `admin_core/service_views.py`: service matrix/recommendation views.
- `admin_core/route_views.py`: route summary builders.
- `admin_core/summary_builders.py`: shared query/pagination/summary helpers.
- `admin_core/overview_views.py`: overview payload builders and request snapshot.
- `admin_core/performance_summaries.py`: performance architecture summaries.
- `admin_core/runtime_read_views.py`: runtime fingerprint/service/proxy read payloads.
- `admin_core/route_reality_views.py`: route status/direct routing summary parsing.
- `admin_core/diagnostic_views.py`: traffic, speed, killswitch, capacity diagnostic summaries.

## 14. Tooling

Important runtime/control tools:

- `tools/v7-users-autoswitch`: planner/executor core.
- `tools/v7-truth-check`: canonical truth gate.
- `tools/v7-convergence-status`: local/GitHub/production alignment view.
- `tools/v7-safe-deploy`: approved deploy/provenance tool.
- `tools/v7-release-sync`: end-to-end release gate wrapper.
- `tools/v7-safe-commit`: guarded commit helper.
- `tools/v7-safe-push`: guarded push helper.
- `tools/v7-sync-status`: read-only sync status.
- `tools/v7-intelligence-snapshot-refresh`: snapshot producer CLI.
- `tools/v7-routing-intelligence-shadow`: read-only RI shadow replay.
- `tools/v7-operator-execution-packet`: governance/execution packet builder.
- `tools/v7-service-matrix-refresh-all`: service matrix refresh.
- `tools/v7-service-matrix-test`: service matrix probe/testing.
- `tools/v7-egress-quality-compact`: quality summary compaction.
- `tools/v7-telegram-sentinel`: Telegram signal tool.

## 15. Systemd Units In Repository

Active/relevant unit files in repository:

- `systemd/v7-users-autoswitch.service`
- `systemd/v7-users-autoswitch.timer`
- `systemd/v7-egress-quality-compact.service`
- `systemd/v7-egress-quality-compact.timer`
- `systemd/v7-service-matrix-refresh.service`
- `systemd/v7-service-matrix-refresh.timer`
- `systemd/v7-telegram-sentinel.service`
- `systemd/v7-telegram-sentinel.timer`
- `systemd/v7-egress-openvpn@.service`

Draft/latent units:

- `systemd/drafts/v7-autoswitch-planner.service`
- `systemd/drafts/v7-autoswitch-planner.timer`
- `systemd/drafts/v7-health.service`

Missing but recommended future block:

- `v7-intelligence-snapshot-refresh.service`
- `v7-intelligence-snapshot-refresh.timer`

Those should be created only in a dedicated scoped systemd certification block.

## 16. What Is Working

Production-confirmed:

- local/GitHub/production convergence;
- production safe deploy path;
- runtime fingerprint;
- truth-check gate;
- convergence status gate;
- PERF.4 runtime fast path deployment;
- intelligence snapshot root and six snapshot files;
- one-user execution/rollback lifecycle from C.2;
- runtime platform certification from D.1;
- dynamic blast radius ceiling behavior;
- service-aware routing;
- capacity-aware routing;
- fail-closed checks;
- rollback packet path for certified lifecycle.

Locally implemented and tested:

- RI.1 foundation;
- RI.2 Routing Brain advisory integration;
- RI.3 advisory score integration;
- API.1 through API.5 read-only decomposition;
- PERF.1 through PERF.4 architecture, workers, fast path;
- safe commit/push/deploy/release-sync tooling;
- endpoint inventory tooling;
- admin_core read-only extraction modules.

Most recent full test count from CONV.2:

```text
249 tests OK
```

## 17. What Is Not Fully Done

### 17.1 Snapshot Refresh Systemd

The snapshot refresh CLI exists and works.

The production service/timer do not exist yet:

```text
v7-intelligence-snapshot-refresh.service: missing
v7-intelligence-snapshot-refresh.timer: missing
```

This is the clearest small next infrastructure follow-up.

### 17.2 Admin API Monolith

The Admin API is still 35,747 lines.

Not yet separated:

- action handlers;
- governance handlers;
- rollback handlers;
- execution handlers;
- audit writer calls;
- closure writer calls;
- full UI/API separation;
- auth/RBAC/CSRF.

Auth/RBAC/CSRF should not be touched casually. They need a dedicated phase with high safety gates.

### 17.3 Runtime Orchestrator Formalization

The autoswitch-centered runtime program exists and is certified in key flows, but the architecture still has formalization debt:

- audit completion is still distributed;
- closure ownership is still partly Admin-side;
- break-glass paths need stricter lineage expectations;
- generic rollback should remain constrained and not become normal execution.

### 17.4 Branch/Documentation Release Hygiene

Historical branch confusion existed:

- `main` was stale for recent runtime work;
- `v7-next` was stale for latest Z7/Z8+ work;
- `Updatesystem` became canonical current work.

CONV.1/CONV.2 fixed the live convergence, but documentation commits still need to be handled carefully so they do not constantly make local/GitHub ahead of production.

### 17.5 Capacity Forecast Snapshots

PERF.4 intentionally did not integrate `capacity-forecast-summaries`.

Reason:

The current runtime already owns load/capacity guards, and PERF.3 did not yet produce capacity forecast snapshots. Integrating them too early would create a false dependency.

## 18. What Should Happen Next

Recommended next sequence:

1. Begin RI.4.
   - Reason: CONV.2 final verdict says `safe_to_begin_RI4=true`.
   - Guardrail: RI.4 must not mutate runtime, move users, bypass governance, or create a second planner.

2. Create a separate snapshot refresh systemd block.
   - Add/certify `v7-intelligence-snapshot-refresh.service`.
   - Add/certify `v7-intelligence-snapshot-refresh.timer`.
   - Verify no autoswitch apply, no user movement, no route mutation.

3. Continue Admin API decomposition only through staged API blocks.
   - Next likely area: action boundary mapping, not action extraction.
   - Keep auth/RBAC/CSRF untouched until a dedicated security phase.

4. Continue Runtime Orchestrator formalization.
   - Reuse `tools/v7-users-autoswitch`.
   - Do not create a parallel orchestrator.
   - Tighten audit/closure/break-glass lineage.

5. Preserve convergence discipline.
   - Before live action: truth-check.
   - Before deploy: tests + safe deploy.
   - After deploy: truth-check + convergence-status.
   - If UNKNOWN appears: STOP.

## 19. What Should Not Happen

Do not rerun old Z9 just because old Z9 reports were NO-GO.

Do not create a new Runtime Orchestrator service.

Do not create duplicate selected move writers.

Do not create duplicate runtime truth stores.

Do not deploy by manually copying random files.

Do not use direct `v7-user-switch` as a normal path.

Do not use generic rollback as the normal rollback path.

Do not mix RI.4 with API.6 or systemd timer work.

Do not touch auth/RBAC/CSRF without a dedicated block.

Do not let documentation-only commits accidentally break production alignment without an explicit convergence plan.

## 20. Current High-Level Verdict

The project is in a good state to continue.

The runtime platform is certified.

The one-user lifecycle and rollback are certified.

Dynamic blast radius is certified.

Safe deploy and truth convergence are working.

PERF.4 is production-converged.

Routing Intelligence is ready for RI.4.

The main remaining debts are architectural cleanup and operational hardening, not a fundamental runtime failure:

- Admin API monolith;
- snapshot refresh timer;
- orchestrator lifecycle formalization;
- break-glass path constraints;
- disciplined documentation/release alignment.

The next correct product-development step is:

```text
RI.4
```

The next correct infrastructure-hardening step is:

```text
Snapshot refresh systemd certification block
```

The next correct Admin API step is:

```text
Continue staged decomposition, but do not touch auth/RBAC/CSRF or mutation handlers yet.
```

