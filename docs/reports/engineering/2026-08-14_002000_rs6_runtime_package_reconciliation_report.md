# RS6 Runtime Package Reconciliation Report

**Status:** `RS6_0_READ_ONLY_RECONCILIATION_COMPLETE_NOT_READY_FOR_PHYSICAL_MINIMIZATION`  
**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`  
**Runtime effects:** `NONE`  
**Production effects:** `NONE`  
**Authority effects:** `NONE`

## 1. Current CPS successor

`ACTIVE_PROGRAM = V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`; `CURRENT_PROGRAM_STAGE = RS6_RUNTIME_PACKAGE_MINIMIZATION`; `CURRENT_COMPLETION_VERDICT = RS6_PREPARED_NOT_ACTIVE`; exact successor remains `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. Local CPS/OMP consistency is `PASS`. This report does not change that frontier.

## 2. Scope and method

Read-only reconciliation compared historical RS1A/RS6 claims, current source, the `tools/v7_sync_lib.py` deploy manifest, the local runtime snapshot, and direct read-only production observation of unit definitions, lifecycle, processes, binary presence, state freshness and the path-guard journal. No command was started, stopped, enabled, disabled, restarted or deployed.

The older local runtime snapshot is a valid identity/hash projection but its systemd observations date from 2026-06-03. It is not used as a substitute for the fresh production lifecycle observation below.

## 3. Services and timers inventory

| Runtime object | Live lifecycle | Current source / manifest | ExecStart or primary consumer | Classification |
| --- | --- | --- | --- | --- |
| `v7-routing-sync.service` | enabled, active `exited` | binary manifest: yes; unit manifest: no | `v7-routing-sync` → nft/ip/kernel | `KEEP_RUNTIME` |
| `v7-health.service` | enabled, active running | `systemd/drafts/v7-health.service`; manifest: no | seven-command health loop, 30 s | `KEEP_RUNTIME` |
| `v7-service-matrix-refresh.timer` | enabled, active waiting | source + Matrix binary manifest | 15 min → Matrix refresh | `KEEP_RUNTIME` |
| `v7-telegram-sentinel.timer` | enabled, active running | source + binary manifest | 4 s → sentinel `--no-autoswitch` | `KEEP_RUNTIME` |
| `v7-autoswitch-planner.timer` | enabled, active running | service source + manifest; timer absent from manifest | 30 s → Matrix event-only consumer → autoswitch child | `KEEP_RUNTIME` |
| `v7-direct-autosync.timer` | enabled, active waiting | source/unit/manifest absent | 10 min → `v7-direct-auto-sync` → dnsmasq | `LEGACY_EXCEPTION` |
| `v7-path-guard-repair.timer` | enabled, active waiting | source/unit/manifest absent | 2 min → `v7-path-guard-repair --apply` | `LEGACY_EXCEPTION` |
| `v7-users-autoswitch.timer` | enabled but inactive; service inactive | source + binary/unit manifest | guarded canary entry; component also runs through Matrix event consumption | `FALLBACK_ONLY` |
| `v7-egress-quality-compact.timer` | enabled, active waiting | source + binary manifest; unit not manifested | quality compaction | `KEEP_RUNTIME` |
| `v7-path-sanity.timer` / `v7-traffic-collector.timer` | enabled, active waiting | no current source/manifest mapping | safety/traffic observation units | `UNKNOWN_REQUIRES_EVIDENCE` |
| `v7-admin-api`, `v7-client-speed-api` | enabled, active running | source + binary manifest | management/read API | `KEEP_RUNTIME` |
| `v7-api`, `v7-benchmark`, `v7-killswitch`, `v7-mss-clamp`, `v7-proxy-inbound-happ-test`, `v7-public-gateway`, `v7-egress-openvpn@…` | enabled, active (or active exited) | only OpenVPN template is in source; no full current manifest mapping for the remainder | network, ingress, safety or product support | `UNKNOWN_REQUIRES_EVIDENCE` |

The active processes corroborate the unit map: health loop, planner Matrix consumer, autoswitch event-consumption child, sentinel, APIs, benchmark loop, dnsmasq, OpenVPN and proxy processes are present. No OMP, report, learning or Polygon process was observed as a synchronous Core writer.

## 4. Known-blocker resolution

| Component | Current fact | Owner / consumer / effect | Final disposition |
| --- | --- | --- | --- |
| `v7-path-guard-repair` | live binary and active timer exist; its unit is currently `failed` after `v7-routing-sync` returned `OK`, but post-repair path sanity remained `FAIL` / `v7_path_risk` | existing recovery/safety chain; calls `sysctl`, `v7-routing-sync`, optional Direct autosync; writes `v7-path-guard-repair.state` and audit | `LEGACY_EXCEPTION`; **no removal**. `BLOCKED_BY_RUNTIME_DEPENDENCY` and `BLOCKED_BY_AUTHORITY`: source/deploy provenance and recovery owner must reconcile the continuing failed safety path. |
| `v7-direct-auto-sync` | live binary, static service and active timer exist; last run succeeded | existing Direct owner; writes `direct-ru-autosync.state`, renders Direct DNS configuration and restarts dnsmasq; not a Core forwarding consumer | `LEGACY_EXCEPTION`; **no removal**. `BLOCKED_BY_MISSING_EVIDENCE`: no current source/unit/manifest mapping. |
| `v7-autoswitch-planner.service` | live timer active; service consumes Matrix events and currently spawns `v7-users-autoswitch --consume-service-failure-automation-only` | Matrix producer → existing autoswitch governed consumer; no unconditional planner loop | `KEEP_RUNTIME`; timer must be added to lifecycle/deploy reconciliation before any package exclusion. |
| `v7-health.service` | active 30-second loop; all called executables exist live | produces summary, history, stability, load, diagnostic, desired-state and JSON projections | `KEEP_RUNTIME`; only `v7-egress-load` is in the current deploy manifest. Other command provenance is incomplete. |

## 5. Health / Matrix writer and reader map

| State | Writer | Verified readers / consumer | Owner and lifecycle | Effect / status |
| --- | --- | --- | --- | --- |
| `egress-history.jsonl` | `v7-egress-history` | stability, Matrix refresh, recent-performance | health loop, every ~30 s | history/stability input; fresh |
| `stability.state` | `v7-egress-stability` | state merge, canary readiness | health loop, every ~30 s | admission-quality input; fresh |
| `egress-load.state` | `v7-egress-load` | state merge, canary readiness | health loop, every ~30 s | capacity input; fresh |
| `egress-diagnose.state` | `v7-egress-diagnose` | state merge, autoswitch, canary readiness | health loop, every ~30 s | path/handshake diagnostic; fresh |
| `summary.state` | `v7-state-merge` from benchmark, stability, status, load and diagnostic inputs | history, diagnose, state JSON, admin/decision readers | health loop, every ~30 s | aggregate health projection; fresh; upstream writers for `benchmark.state` and `egress-status.state` not reconciled here |
| `user-desired-state.state` | `v7-user-desired-state-save` → `v7-user-desired-state` | `v7-state-json` | health loop nominally invokes it | writer file is stale relative to the fresh loop; `MISSING_RUNTIME_EVIDENCE` |
| `v7-state.json` | `v7-state-json-save` → `v7-state-json` | API, intelligence, governed canary, autoswitch, runtime validation | health loop; fresh | broad derived-state projection |
| `service-matrix.json` | Matrix owner; sentinel delegates to that canonical writer rather than creating a second decision owner | planner/autoswitch, API, intelligence and governed consumers | Matrix timer plus sentinel | Control Plane health/event input; writer boundary tests passed |
| `telegram-sentinel.json` | Telegram sentinel | autoswitch/governed and observability readers | 4-second timer | fast signal, not direct forwarding |
| `v7-path-guard-repair.state` | path guard | audit/recovery evidence; no safe removal consumer proven | 2-minute timer | safety outcome; current result `NEEDS_ATTENTION` |

The mapping closes the group-level RS3 residual for the observed health states enough to identify writers/readers and freshness. It does **not** close provenance for all live writer binaries, nor does it prove every manual or legacy reader absent; therefore it grants no merge/delete authority.

## 6. Runtime classification

| Component | Type | Owner | Source / deployed status | Actual effect | Classification |
| --- | --- | --- | --- | --- | --- |
| Routing Core sync | Data Plane | Routing Core | source + deployed manifest | route/kernel apply and verification | `KEEP_RUNTIME` |
| Matrix + Sentinel | Control Plane | Matrix/Sentinel | source + deployed manifest | health/event state and bounded wake | `KEEP_RUNTIME` |
| Planner event consumer + autoswitch | Control/fallback | Matrix, autoswitch, Authority | service source; consumer live | event consumption and governed fallback, not primary apply | `FALLBACK_ONLY` |
| Direct autosync | Direct product Control Plane | existing Direct owner | deployed only in observed Runtime | DNS/config mutation and dnsmasq restart | `LEGACY_EXCEPTION` |
| Path guard repair | recovery safety | existing recovery/restore-barrier owners | deployed only in observed Runtime | guarded sysctl/Core/Direct repair | `LEGACY_EXCEPTION` |
| Health loop and helper writers | Control Plane observation | existing health/state owners | partial source; mostly deployed-only | health/capacity/diagnostic state | `KEEP_RUNTIME` with provenance residual |
| `tools/v7_sync_lib.py`, OMP, reports, Polygon, learning/replay | Engineering Plane | existing CPS/OMP/evidence owners | deploy support only; no synchronous Core edge | truth/deploy/evidence interfaces | `ENGINEERING_ONLY` |
| unmanaged active V7 units and backup/legacy executable copies | mixed | not established by this reconciliation | live inventory lacks source/manifest/lifecycle mapping | cannot infer necessity from existence | `UNKNOWN_REQUIRES_EVIDENCE` |

`REMOVE_CANDIDATE = NONE`: existence, inactive oneshot status or a smaller source manifest are not removal evidence.

## 7. Physical-readiness verdict

```text
NOT_READY_FOR_PHYSICAL_MINIMIZATION
```

| Blocker | Required existing owner | Re-entry condition |
| --- | --- | --- |
| failed active path-guard recovery | recovery/restore-barrier/path-sanity owner | current failure cause, safe recovery status and source/deploy provenance reconciled without changing the path during analysis |
| Direct autosync is live but unversioned/unmanifested | existing Direct owner and deploy/package owner | source, unit, caller, DNS restart/rollback and package lifecycle matched |
| active health helpers lack full source/manifest provenance | health/state and deploy/package owners | all loop commands and upstream state writers have source, deploy and lifecycle disposition |
| untracked active units and retained backup executables | existing deploy/package plus affected component owners | prove active consumer/lifecycle or classify an owner-backed retained exception; never delete from inventory alone |
| stale `user-desired-state.state` | desired-state/state owner | fresh writer success or exact declared failure/lifecycle evidence |

## 8. No-mutation gate and successor

`FILES_CHANGED = 0` for product/runtime source; `SERVICES_CHANGED = 0`; `TIMERS_CHANGED = 0`; `RUNTIME_BEHAVIOR_CHANGED = 0`; `PRODUCTION_EFFECT = NONE`; `AUTHORITY_EFFECT = NONE`. No canonical owner was changed: the new facts are current operational observations and require the listed existing owners to reconcile before promotion into durable architecture truth.

Exact CPS successor remains `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. It may continue only as reconciliation of these blockers; this report does not admit physical minimization or RS7.

