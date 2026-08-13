# RS6.1 Targeted Provenance and Responsibility Closure Report

**Status:** `NOT_READY_FOR_RS6_PHYSICAL_MINIMIZATION`
**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## 1. CPS successor and scope

The CPS Section 0 frontier is unchanged: RS6 is active and its exact successor
remains `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. The prompt's proposed
RS6.3 duplicates RS6.1 provenance closure and RS6.2 interaction closure, so
no new phase was created. This report is the final targeted logical projection
inside existing RS6.1.

Evidence is current tracked source, current manifest, historical hash
provenance and direct read-only production observation at
`2026-08-13T21:50:38Z`. Services, timers, files, deploy, Runtime, Production
and Authority were not changed.

## 2. Targeted closure

| Component | Provenance and lifecycle | Responsibility / consumer / effect | Classification and exact residual |
| --- | --- | --- | --- |
| `v7-state-merge` | live `/usr/local/bin` SHA-256 `216a…bdfb`; no current tracked source, manifest or unit | health loop calls it every ~30 seconds; reads benchmark/stability/status/load/diagnosis state; writes `summary.state` for history, diagnose, state JSON, Admin/state and stale-check readers | `UNKNOWN_REQUIRES_EVIDENCE`; existing health/state plus deploy/package owners must locate/version source or retain it explicitly with reproducible deployment evidence |
| `v7-path-guard-repair` | current tracked `hardening/v7-path-guard-repair` hash matches live `894a…074c7`; unit/timer are live but not current manifested | timer -> guard -> path sanity -> conditional Routing Sync/kill-switch/Direct action -> post-check; writes guard state | `KEEP_RUNTIME`; repair action succeeds, but post-check remains `v7_path_risk`. Required owners: recovery/path-safety, desired-state and Matrix. Re-enter after `desired_state_unknown` and `egress_service_matrix=FAIL` are reconciled; no guard behavior change is authorized |
| `v7-direct-auto-sync` | tracked source hash matches live `f58d…228c4`; static service and enabled 10-minute timer are live; unit/deploy input absent | timer and optional guard caller; Direct domains/config -> DNS render/dnsmasq; writes autosync state; latest sample state `OK`, `changed=0`, eight checks pass | `LEGACY_EXCEPTION`; existing Direct product plus deploy/package owners must preserve current unit, consumer and rollback mapping or issue a different owner-backed disposition |
| `v7-path-sanity-check` | live hash `567a…c890`, static service and enabled 5-minute timer; no current source/manifest | timer and guard call it; writes path-sanity state consumed by guard | `UNKNOWN_REQUIRES_EVIDENCE`; existing path-safety/recovery plus deploy/package owners; re-enter with versioned source/unit mapping |
| `v7-traffic-snapshot` | live hash `b42c…46c23` equals historical `hardening/v7-traffic-snapshot` hash; current source/manifest absent; static service and enabled 15-minute timer live | reads nft counters/registries; writes traffic SQLite/history; Admin API is a direct reader | `KEEP_RUNTIME` with source/deploy residual; traffic/accounting, Admin and deploy/package owners must establish current reproducible source/deploy mapping |
| `v7-api.service` | enabled, active; `/usr/local/bin/v7-api` hash observed; current tracked source/manifest absent | depends on health and Routing Sync; local API effect is observed but current source consumer map is not | `UNKNOWN_REQUIRES_EVIDENCE`; existing API plus deploy/package owners |
| `v7-benchmark.service` | enabled, active; shell loop executes `v7-egress-benchmark-all` every 300 s; helper source/manifest absent | measurement producer, ordered after Routing Sync | `UNKNOWN_REQUIRES_EVIDENCE`; existing benchmark/measurement plus deploy/package owners |
| `v7-killswitch.service` | enabled, active exited; current `hardening/v7-killswitch-enable` hash equals live `2782…6638`; unit input absent | boot safety boundary and path-guard/egress-state callers; applies leak guard before routing/health/API | `KEEP_RUNTIME`; existing safety plus deploy/package owners must preserve unit provenance |
| `v7-mss-clamp.service` | enabled, active exited; live binary observed, source/manifest absent | kernel MSS safety; path guard is a conditional caller | `UNKNOWN_REQUIRES_EVIDENCE`; existing network-safety plus deploy/package owners |
| `v7-proxy-inbound-happ-test.service` | enabled, active; starts sing-box with runtime config and privileged route setup; source/config provenance incomplete | product ingress/proxy boundary with ip-rule lifecycle | `UNKNOWN_REQUIRES_EVIDENCE`; existing proxy/ingress plus deploy/package owners |
| `v7-public-gateway.service` | enabled, active; current `tools/v7-public-gateway` hash equals live `0ea5…d123`; unit input absent | public `/connect` and profile delivery -> required Admin API upstream | `KEEP_RUNTIME`; existing gateway/Admin plus deploy/package owners must map the unit deployment source |
| `v7-egress-openvpn@v7edb0c189291.service` | active instance uses tracked `systemd/v7-egress-openvpn@.service`; instance config is external Runtime input | OpenVPN egress process reads instance config and state directory | `KEEP_RUNTIME`; existing egress/deploy owner must retain instance-config lifecycle mapping |
| Seven backup autoswitch executables | no active systemd reference; no current active-owner invocation found; one governance check contains historical backup-path text | no current Runtime consumer is proved; dynamic/manual invocation remains unproven | `UNKNOWN_REQUIRES_EVIDENCE`; existing autoswitch plus deploy/package owners require an exact full invocation/lifecycle search before residue disposition |

## 3. Recovery-chain root cause

```text
timer
  -> v7-path-guard-repair
  -> v7-routing-sync = OK
  -> post v7-path-sanity-check = FAIL / v7_path_risk
  -> V7_PATH_GUARD_REPAIR = NEEDS_ATTENTION
```

The guard did not fail because its invoked Routing Sync action failed. Current
post-check evidence attributes the remaining condition to
`user_policy_routes=FAIL reason=desired_state_unknown` and
`egress_service_matrix=FAIL`; the current sanity output explicitly notes that
its Matrix value is direct-egress scope, not a full client-path proof. The
recovery/path-safety, desired-state and Matrix owners must reconcile that
post-verification condition. This report does not diagnose a code fix or
change the recovery behavior.

## 4. Final Runtime responsibility matrix and unknown closure

| Layer | Components with classified current role | Remaining unknown owner/re-entry |
| --- | --- | --- |
| Data | Routing Sync; OpenVPN egress | none in this bounded set beyond normal external instance config lifecycle |
| Control | health helpers, state merge, path guard, path sanity, Direct, benchmark, killswitch, MSS clamp, Matrix | health/state source; recovery desired-state/Matrix condition; Direct unit/rollback; benchmark/MSS source-deploy evidence |
| Management | API, Admin traffic read, public gateway, proxy ingress | API/proxy source-deploy/consumer maps |
| Engineering | CPS/OMP/deploy support and reports remain outside observed synchronous Core path | no Runtime classification is inferred from historical evidence |

Every unknown now has an exact existing owner class and re-entry condition.
This is a disposition, not proof that the missing evidence has appeared.

## 5. Verdict and no-mutation gate

```text
NOT_READY_FOR_RS6_PHYSICAL_MINIMIZATION
REMOVE_CANDIDATE = NONE
```

Blockers are limited to: missing current source/deploy provenance for the
listed live helpers/units; path guard's unresolved post-verification state;
Direct unit/rollback provenance; desired-state freshness; and unknown
backup-lifecycle/dynamic invocation evidence. No new Program, owner, truth
source, registry or Runtime component was created.

`CPS_FRONTIER_CHANGED=0`; `FILES_CHANGED=0` for product/runtime source;
`SERVICES_CHANGED=0`; `TIMERS_CHANGED=0`; `RUNTIME_BEHAVIOR_CHANGED=0`;
`PRODUCTION_EFFECT=NONE`; `AUTHORITY_EFFECT=NONE`.

## 6. Programmatic change delta

The OMP change adds one compact clarification to existing RS6.1. This one
report was added. Product code, deploy files, services, timers, processes,
state, routing objects and dependency edges changed: `0`.
