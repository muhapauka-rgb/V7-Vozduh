# RT2-PR2 Engine Relationship and Runtime Package Audit

Status: `RT2_PR2_READ_ONLY_AUDIT_COMPLETE_MUTATION_AND_PROFILE_TERMINAL_BLOCKED`

Scope: only OMP §28.9 `RT2 Post-Reset Operating Profile`. This report consumes the Reset terminal and the PR1 baseline. It does not execute another OMP capability, change Runtime, grant Authority, generate traffic, or treat a report as admission.

## Decision

The current Core-primary dataplane is compact and correctly separated, but the installed operating package is materially wider than the simplified M10 projection. The correct optimization is not wholesale deletion of the large legacy files. It is to preserve the 210-line Core writer, make the real asynchronous/mutation-capable package boundary explicit, and admit only owner-backed changes that remove a proven duplicate consumer or mixed responsibility.

The attempted narrow CPS activation of RT2 was rejected and reverted after `v7-truth-check` proved that Section 0 alone would diverge from active WIP, registry, mission identity and OMP terminal projections. Therefore read-only analysis is legal, while PR2/PR3 source, package and Runtime mutation remains blocked until the existing OMP/CPS owner performs one complete admission transaction.

## Reproducible coverage

The confirmed `.understandignore` excluded `docs/`, evidence/artifact trees, secrets, logs, caches, generated binaries and dependency directories from code-depth analysis. Historical root documents were classified at sufficient documentation depth; production and mutation-capable paths received deeper static and live inspection.

| Evidence | Result |
| --- | ---: |
| Repository entries ignored by the confirmed scope rules | 7,462 |
| In-scope files scanned exactly once | 1,076 |
| Graph nodes | 3,585 |
| Graph edges | 3,979 |
| File/config/document/pipeline nodes | 1,076 |
| Function/class nodes | 2,509 |
| Architectural layers | 8 |
| Guided trace steps | 11 |
| Import edges recovered by deterministic scan | 95 |
| Skipped batches/files | 0 / 0 |
| Validation issues | 0 |
| Edge-less node warnings | 858; retained as orphan candidates, not auto-deletion proof |

Permanent generated evidence: `.understand-anything/knowledge-graph.json`, `meta.json`, `fingerprints.json` and `intermediate/scan-result.json`. Raw batch/analysis material was moved into the skill-prescribed delayed-cleanup `.trash-*` area. Every file-level node belongs to exactly one architectural layer; all layer and tour references resolve.

## Responsibility and interaction findings

| Surface | Real caller / consumer / effect | Classification | Disposition | Removal or recheck trigger |
| --- | --- | --- | --- | --- |
| `tools/runtime-support/v7-routing-sync` (210 LOC) | `v7-routing-sync.service`, path guard on detected routing fault, user-key rotation; programs nft/ip and verifies class state | Data Plane primary, single routing lock, explicit fallback | `KEEP` | only a proven replacement with equivalent atomic apply, verify, fencing and fallback |
| `admin_core/routing_core.py` (265 LOC) | tests, shadow/certification adapters; produces effect-free plan/contracts | Control Plane decision contract | `KEEP` | none; no duplicate live writer proven |
| nft `user_class`/`class_egress`, six fwmark rules/tables | production kernel forwarding for 124 members | Data Plane primary | `KEEP` | proven replacement plus real-traffic observation |
| `v7-users-autoswitch` (23,639 LOC; 317 defs) | governed/manual planning, passive event consumption and bounded `v7-user-switch`; not current primary Core writer | `RESPONSIBILITY_MIXING`; legacy/fallback plus Engineering Plane | `SHRINK/FUTURE_REVIEW`, not whole-file delete | exact function consumers mapped and legal mutation Mission admitted; preserve rollback/Authority paths |
| `v7_sync_lib.py` (25,379 LOC; 306 defs) | truth, deploy, OMP, Polygon and continuation CLIs; writes engineering documents/state, not packet forwarding | `RESPONSIBILITY_MIXING`, Engineering Plane | `SHRINK/FUTURE_REVIEW` | split only where an existing owner consumes a coherent responsibility and tests prove no CLI break |
| `admin/v7-admin-api` (41,024 LOC; 719 defs; 16,528-line HTML function) | active admin service and operator consumers | `RESPONSIBILITY_MIXING`, API/UI/control boundary | `SHRINK/FUTURE_REVIEW` | UI/API extraction under existing admin owner with compatibility tests; unrelated to routing hot path |
| `admin_core/operator_execution.py` + pipeline (14,064 LOC) | Packet/lease/barrier, governed apply, validation, rollback and exact action class | Control Plane safety owner; excluded from primary forwarding | `KEEP` | equivalent bounded Authority, crash recovery and rollback production proof |
| `v7-user-switch` (135 LOC) | governed/manual per-user movement and rollback | fallback mutation adapter | `LEGACY_EXCEPTION` | no remaining bounded movement/rollback consumer |
| `v7-autoswitch-planner.timer` -> Matrix consumer | active every 30s; service consumes existing service-failure events and may enter only governed standing-policy path | name is historical; real edge is Control/Engineering async, not primary writer | `KEEP`, rename only if it removes operator ambiguity without deployment risk | consumer superseded or naming change admitted with unit/deploy proof |
| `v7-service-matrix-refresh.timer` and Telegram sentinel | active async health writers/consumers; sentinel deployed with `--no-autoswitch` | Control Plane observation | `KEEP` | equivalent freshness and failure-event consumer exists |
| `v7-health.service` | active loop for history/stability/load/diagnose/state projections | Control Plane observation with multiple state outputs | `KEEP/SHRINK_REVIEW` | per-output consumer map plus restart/freshness proof |
| `v7-direct-autosync.timer` | active every 10m; can update Direct domain config, restart dnsmasq and write state | `HIDDEN_RUNTIME_DEPENDENCY` relative to M10 compact projection; separate Direct product behavior | `KEEP` under existing Direct owner, explicitly outside routing Core | Direct feature retired or equivalent idempotent config owner proven |
| `v7-path-guard-repair.timer` -> `--apply` | active every 2m; may run sysctl, MSS clamp, Core sync, killswitch, Direct autosync and optional MTU repair | `HIDDEN_RUNTIME_DEPENDENCY`; recovery/safety mutation chain | `LEGACY_EXCEPTION`, no blind disable | failure scenarios, Authority envelope and equivalent recovery consumer proven before any narrowing |
| OMP/reports/history | no import/startup edge to Core writer | Engineering/Historical only | `KEEP_OUTSIDE_RUNTIME` | none |

### Actual production dependency projection

```text
CLIENT PACKETS
  -> nft user_class/class_egress
  -> six fwmark rules/tables
  -> egress interface

ASYNC CONTROL / RECOVERY
  Telegram sentinel -> Matrix state/event
  Matrix timer -> full refresh
  30s planner-named timer -> existing-event consumer -> governed policy path only
  health/quality/benchmark timers -> health and capacity state
  path sanity -> path guard --apply -> bounded repair commands -> routing-sync when required
  Direct autosync -> Direct DNS/config state

ENGINEERING
  OMP / CPS / Reports / Polygon / Learning / Replay
  -X-> synchronous packet forwarding
```

No OMP/report/history import or startup edge into `v7-routing-sync` was found. The principal correction is that `path-guard --apply` and Direct autosync are real installed mutation-capable dependencies even though they are not continuous packet-forwarding dependencies.

## Mature-system fit analysis

Only architectural principles were consumed:

| Reference principle | V7 fit / material gap | Disposition |
| --- | --- | --- |
| Junos separates Routing Engine and Packet Forwarding Engine, keeps forwarding tables local and updates forwarding without interrupting packets | V7 fits through prepared class state -> compact nft/ip writer -> kernel forwarding; Engineering Plane is absent from packet lookup | `KEEP` |
| IOS XR uses modular control processes and a hardware-abstraction boundary that programs the dataplane from RIB state | V7 has a valid small adapter, but large control/engineering executables mix many responsibilities | keep adapter; shrink monoliths only behind existing interfaces and tests |
| FRR zebra owns the RIB/FIB boundary and feeds the kernel through Netlink while protocols remain separate | V7 class state -> one routing writer -> Linux kernel matches the dependency direction | `KEEP`; do not add FRR-like daemons |
| Linux exposes route configuration through rtnetlink and keeps kernel forwarding state distinct from userspace control | V7 `ip`/`nft` adapter is the correct boundary; verification must remain explicit | `KEEP` |
| Cloudflare combines passive/fast failover signals with health checks and load-balancing decisions | V7's sentinel + Matrix + governed consumer is directionally correct; it must not turn the fast signal into unbounded movement Authority | `KEEP` with current fail-closed gate |

Primary references: Juniper Junos OS Architecture Overview (`https://www.juniper.net/documentation/us/en/software/junos/junos-overview/topics/concept/junos-software-architecture.html`); Cisco IOS XR Data Sheet (`https://www.cisco.com/c/en/us/products/collateral/ios-nx-os-software/ios-xr-software/datasheet-c78-743014.html`); FRRouting Zebra documentation (`https://docs.frrouting.org/en/stable-7.2/zebra.html`); Linux `rt-route` Netlink specification (`https://docs.kernel.org/next/netlink/specs/rt-route.html`); Cloudflare health/failover description (`https://blog.cloudflare.com/new-tools-to-monitor-your-server-and-avoid-downtime/`). Architectural difference alone produced no rewrite verdict.

## PR4-PR7 independent evidence consumption

The focused routing, Core promotion, routing-sync, autoswitch policy, user-switch, quality, load-policy and 10k/50 scale unittest set passed with exit 0. No pytest package was available, so the repository's unittest-compatible modules were executed directly. This proves existing technical contracts, not real production traffic or admission.

| Gate | Current result |
| --- | --- |
| `PRE_MUTATION_BASELINE_CAPTURED` | `PASS` |
| `EXHAUSTIVE_V7_ENGINE_COMPONENT_COVERAGE_PASS` | `PASS_FOR_CONFIRMED_SCOPE`; 1,076/1,076 file nodes classified |
| `V7_REAL_CODE_RELATIONSHIP_GRAPH_COMPLETE` | `PASS_WITH_DYNAMIC_RUNTIME_SUPPLEMENT`; static imports alone are not treated as full truth |
| `SYSTEM_WIDE_DEPENDENCY_INTERACTION_GRAPH_COMPLETE` | `PASS_FOR_CRITICAL_RUNTIME_AND_MUTATION_PATHS` |
| `RESPONSIBILITY_AUDIT_COMPLETE` | `PASS` |
| `REFERENCE_SYSTEM_COMPONENT_BOUNDARY_COMPARISON_COMPLETE` | `PASS` |
| `DECISION_RELEVANT_ANALYSIS_PRESERVED` | `PASS` |
| `LEGACY_SURFACE_REDUCTION_PASS` | `NOT_PROVEN`; no deletion justified or admitted |
| `RUNTIME_PACKAGE_MINIMAL_PASS` | `FAIL_CURRENT_PROJECTION_INCOMPLETE`; active package is wider than M10 description |
| `ROUTING_LATENCY_BASELINE_CONFIRMED` | existing M6/M7 evidence retained; PR1 real packet outcome still open |
| `CHANNEL_ADMISSION_MODEL_STABLE` | controlled/unit evidence retained; natural real-traffic outcome open |
| `SCALE_BOUNDARY_CONFIRMED` | test evidence passes for 10k+/50+ contract; production-scale consumption not re-created |
| `ARCHITECTURE_DRIFT_PROTECTION_ACTIVE` | contract active; final alignment blocked by package mismatch |
| `REAL_USER_CONNECTIVITY_OUTCOME_CONFIRMED` | `NOT_PROVEN`; two bounded nft counter reads were zero |
| `AUTOMATIC_INTERNET_OPERATION_READY` | `NOT_PROVEN` |

## Exact blockers and successor

1. `RT2_ADMISSION_PROJECTION_REQUIRED`: the existing OMP/CPS owner must create one consistent Mission/registry/Section 0 transition; a report cannot do this and a partial CPS patch failed closed.
2. `REAL_TRAFFIC_OBSERVATION_REQUIRED`: next ordinary production packet must be observed through the existing class nft/routing verification owner; no traffic or user movement may be manufactured.
3. `RUNTIME_PACKAGE_PROJECTION_RECONCILIATION_REQUIRED`: existing Canonical/SYSTEM_MAP owners must acknowledge path guard, Direct autosync, health/Matrix and planner-named event consumer as actual production dependencies before a minimality terminal.
4. Only after 1–3 may an owner-backed PR3 Mission decide whether any exact responsibility is removed, split, renamed or retained. The present audit authorizes no code, unit or Runtime change.

This is a bounded legal terminal for the current read-only execution, not completion of RT2-PR1 -> PR7 and not `STEADY_STATE_OPERATIONS` graduation.

## PROGRAMMATIC_CHANGE_DELTA

Program source LOC: `0 -> 0 -> 0`.

Documentation/report LOC: `0 -> 269 -> +269` across the PR1 and PR2 Engineering Reports (`118 + 151`).

Generated analysis/data LOC: 126,372 lines in the final graph, fingerprints and preserved scan inventory; reported separately and excluded from documentation/program LOC.

Test LOC: `0 -> 0 -> 0`; existing tests only executed.

Files added / modified / deleted / moved / runtime-excluded: program files `0 / 0 / 0 / 0 / 0`; generated analysis and Engineering Reports are evidence, not product implementation.

Functions/classes/entrypoints added / removed / moved / merged / changed: `0 / 0 / 0 / 0 / 0`.

Dependency edges added / removed / changed: `0 / 0 / 0`; 3,979 repository edges and live unit edges were observed, not mutated.

State writers/readers/surfaces added / removed / merged: `0 / 0 / 0`.

Runtime units/process/package delta: `0`; read-only census only.

Routing object/writer/planner delta: `0`; verification only.

Legacy physical removal vs logical/runtime exclusion: `0` removed; existing Core-primary exclusion remains unchanged.

`PROGRAMMATIC_CODE_EFFECT = NONE`.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`
