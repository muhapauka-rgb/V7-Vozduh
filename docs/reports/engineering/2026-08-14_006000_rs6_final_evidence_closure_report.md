# RS6 Final Evidence Closure Report

**Status:** `NOT_READY_FOR_RS6_PHYSICAL_MINIMIZATION`
**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## 1. CPS successor and scope

CPS Section 0 remains authoritative: `RS6_RUNTIME_PACKAGE_MINIMIZATION` is
the current stage and its exact successor remains
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. RS6.1 already provides final
Runtime provenance/responsibility closure and RS6.2 already provides bounded
interaction closure. No RS6.3, new Program, owner, truth source, registry or
audit framework was created.

This report closes only the already recorded residual set. It reuses the
current tree at `70714225`, historical tracked deployment commits where named,
and the direct read-only Runtime observation captured at
`2026-08-13T21:50:38Z` in the preceding RS6.1 report. This task made no
Runtime/deploy change; it does not assert that the observed server remained
unchanged after that capture. Historical evidence narrows provenance only; it
never proves present removability.

## 2. Previous blockers and their final disposition

`UNKNOWN_REQUIRES_EVIDENCE` is not converted into a false removal decision.
Where current source or deploy provenance is still absent, the final
classification is `OWNER_BACKED_EXCEPTION`: retain unchanged, identify the
existing owner, name the missing evidence and state an exact re-entry
condition. It grants neither delete nor disable authority.

## 3. Targeted closure

### v7-state-merge

The observed health loop calls `v7-state-merge` about every 30 seconds:

```text
health/stability/status/load/diagnosis inputs
  -> v7-state-merge
  -> summary.state
  -> history, diagnose, state JSON, Admin/state and stale-check readers
```

The live SHA-256 (`216a…bdfb`) matches the retained Runtime snapshot, but no
current tracked source, deploy manifest or unit source exists. The existing
health/state plus deploy/package owners retain it as
`OWNER_BACKED_EXCEPTION`. Re-enter only when they can supply a versioned source
and reproducible source-to-`/usr/local/bin` deployment chain; until then it is
not a removal candidate.

### Path guard

```text
enabled timer -> v7-path-guard-repair -> v7-routing-sync = OK
  -> v7-path-sanity-check = FAIL / v7_path_risk
  -> V7_PATH_GUARD_REPAIR = NEEDS_ATTENTION
```

The current `hardening/v7-path-guard-repair` source matched the observed live
hash (`894a…074c7`). Its historical tracked unit/timer came from commit
`af552e30`; current package provenance is absent. The post-check did not show
an invoked recovery failure: it recorded `user_policy_routes=FAIL`
(`desired_state_unknown`) and `egress_service_matrix=FAIL`, whose sanity
output is direct-egress scope rather than a full client-path proof.
`KEEP_RUNTIME` is the only safe classification: existing recovery/path-safety,
desired-state and Matrix owners must reconcile those two outputs before a
physical-change proposal. This does not authorize a recovery change.

### Direct autosync

`tools/runtime-support/v7-direct-auto-sync` matched the observed live hash
(`f58d…228c4`); the live service and enabled ten-minute timer had a successful
sample (`OK`, `changed=0`, eight checks passing). Its tracked historical unit
source is commit `546886cc`, but no current deploy input maps that unit.
The existing Direct product and deploy/package owners retain it as
`LEGACY_EXCEPTION` with the proven DNS render/dnsmasq effect. Re-enter only
with current unit deployment and rollback mapping. Direct behaviour is
unchanged.

### Backup executables

The seven retained `v7-users-autoswitch.*backup*` binaries have no current
systemd reference and no current active-owner invocation was found. A literal
historical backup path in a governance check is not an invocation; dynamic or
manual use was not disproved. They are therefore a single
`OWNER_BACKED_EXCEPTION` under the existing autoswitch and deploy/package
owners, not `REMOVE_CANDIDATE`. Re-enter after their exact dynamic/manual
invocation and lifecycle search produces either a real consumer or a negative
proof across the deployment boundary.

## 4. Final Runtime responsibility matrix

| Component | Responsibility / layer | Existing owner | Source / deploy / lifecycle | Caller -> consumer | State / effect | Final classification / gap |
| --- | --- | --- | --- | --- | --- | --- |
| `v7-state-merge` | Control: health-state aggregation | health/state; deploy/package | live hash observed; current source/deploy absent; health loop | health loop -> state/history/Admin readers | inputs -> `summary.state`; read model | `OWNER_BACKED_EXCEPTION`; versioned source + reproducible deploy |
| `v7-path-guard-repair` | Control: recovery verification | recovery/path-safety; desired-state; Matrix | tracked source/live hash match; historical unit/timer; enabled timer | timer -> guard -> Routing Sync/path sanity | guard state; bounded repair/verification | `KEEP_RUNTIME`; reconcile desired-state/Matrix post-check |
| `v7-path-sanity-check` | Control: path verification | path-safety/recovery; deploy/package | live hash, static service + timer; source/deploy absent | timer/guard -> guard | `v7-path-sanity.state`; verification | `OWNER_BACKED_EXCEPTION`; source/unit mapping |
| `v7-direct-auto-sync` | Control: Direct DNS/config convergence | Direct product; deploy/package | tracked source/live hash match; historical unit/timer; enabled timer | timer/guard -> dnsmasq | autosync state; DNS effect | `LEGACY_EXCEPTION`; current unit + rollback mapping |
| `v7-traffic-snapshot` | Management: traffic accounting | traffic/accounting; Admin API; deploy/package | historical tracked source hash/live hash match; service/timer observed; current manifest absent | timer -> Admin API reader | traffic SQLite/history; accounting | `KEEP_RUNTIME`; reproducible deploy mapping |
| `v7-api.service` | Management: local API | `admin/v7-admin-api`; deploy/package | active/enabled binary; current source/deploy absent | health/Routing Sync order -> local API consumers | local API state/effect observed | `OWNER_BACKED_EXCEPTION`; current source/consumer/deploy map |
| `v7-benchmark.service` | Control: egress measurement | benchmark/measurement; deploy/package | active/enabled loop; helper source/deploy absent | service -> health/Matrix inputs | benchmark state; measurement | `OWNER_BACKED_EXCEPTION`; helper provenance + consumer map |
| `v7-killswitch.service` | Data safety boundary | `hardening/v7-killswitch-enable`; deploy/package | tracked source/live hash match; active exited; unit input absent | path guard/egress-state -> routing/health/API ordering | nft leak guard | `KEEP_RUNTIME`; unit provenance |
| `v7-mss-clamp.service` | Data safety boundary | network-safety; deploy/package | active exited; source/deploy absent | path guard conditional caller -> client path | kernel MSS clamp | `OWNER_BACKED_EXCEPTION`; source/deploy + lifecycle |
| `v7-proxy-inbound-happ-test.service` | Management: proxy ingress | proxy/ingress; deploy/package | active; sing-box config and unit provenance incomplete | service -> ingress clients | privileged ip-rule lifecycle | `OWNER_BACKED_EXCEPTION`; config/unit/source mapping |
| `v7-public-gateway.service` | Management: public gateway | `tools/v7-public-gateway`; Admin API; deploy/package | tracked source/live hash match; active; unit input absent | gateway -> Admin API upstream | `/connect` and profile delivery | `KEEP_RUNTIME`; unit deployment mapping |
| `v7-egress-openvpn@v7edb0c189291.service` | Data: managed egress | egress/deploy | tracked `systemd/v7-egress-openvpn@.service`, installed by existing installer; active external instance config | `v7-egress-set-state` -> OpenVPN | egress interface/state directory | `KEEP_RUNTIME`; retain external config lifecycle |
| backup executables | Engineering/legacy residue | autoswitch; deploy/package | retained live binaries; no current unit/consumer proved | no active caller proved | no current Runtime effect proved | `OWNER_BACKED_EXCEPTION`; full dynamic/manual lifecycle proof |

## 5. Remaining blockers and readiness

| Component | Missing evidence | Existing owner | Re-entry condition |
| --- | --- | --- | --- |
| state merge / path sanity / benchmark / MSS | current source-to-deploy mapping | respective component owner plus deploy/package owner | versioned source, deployed artifact and current consumer chain agree |
| API / proxy ingress | current source, unit/config and consumer mapping | Admin API or proxy/ingress owner plus deploy/package owner | source, unit/config, caller and consumer are jointly evidenced |
| path guard | desired-state and Matrix post-check remain unresolved | recovery/path-safety, desired-state and Matrix owners | these outputs reconcile without changing guard behaviour in this closure |
| Direct / traffic / killswitch / public gateway | missing current unit/deploy mapping | named component owner plus deploy/package owner | reproducible unit deployment is evidenced |
| backup executables | dynamic/manual lifecycle unknown | autoswitch plus deploy/package owners | full invocation search proves consumer or negative residue proof |

```text
NOT_READY_FOR_RS6_PHYSICAL_MINIMIZATION
REMOVE_CANDIDATE = NONE
```

All objects in the known RS6 residual set now have a disposition and an exact
re-entry condition. That closes classification, not missing provenance. The
remaining owner-backed exceptions are exact blockers to any physical removal
or package exclusion; they do not open a new audit or change the CPS frontier.

## 6. No-mutation verification

```text
CPS_FRONTIER_CHANGED = 0
NEW_PROGRAM = 0
NEW_OWNER = 0
NEW_TRUTH_SOURCE = 0
RUNTIME_BEHAVIOR_CHANGED = 0
PRODUCTION_EFFECT = NONE
AUTHORITY_EFFECT = NONE
```
