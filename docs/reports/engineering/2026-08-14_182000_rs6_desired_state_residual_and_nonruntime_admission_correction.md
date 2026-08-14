# RS6 Desired-State Residual and Non-Runtime Admission Correction

**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`  
**CPS stage / exact successor:** `RS6_RUNTIME_PACKAGE_MINIMIZATION` / `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `RS6_PHYSICAL_MINIMIZATION_NOT_READY; SAFETY_RESIDUAL_CONFIRMED`  
**Runtime / Production / Authority effects:** existing fail-closed
desired-state projection corrected / `NONE` / `NONE`
**Deployment effect:** the existing helper and its existing saver were
synchronized through the approved manifest; no service, timer, route, policy
or user operation was invoked.

## Decision-relevant recheck

Fresh read-only truth on `2026-08-14` is `FULLY_ALIGNED`: workspace and
GitHub are at `a1b529a0`; Runtime's deployable code is at `d8a4eb29`, with
the sole difference a documentation-only report. Safe-deploy preflight found
the eleven previously recovered RS6 source/unit artifacts byte-identical to
their live counterparts. There is therefore no pending artifact deployment
and no basis to count provenance recovery as physical package reduction.

The remaining recovery residual is live, not historical:

```text
v7-path-guard-repair.timer
  -> v7-path-guard-repair
  -> v7-routing-sync = OK
  -> v7-path-sanity-check = FAIL (v7_path_risk)
  -> user_policy_routes = desired_state_unknown
```

The path-sanity state was fresh at observation. The saved desired-state
projection was stale, and its current direct read-only producer exited with
status `1`; the health service remained running because its loop continues
after that child failure. The Matrix state separately remains an old failed
direct-egress observation. Neither fact is a proof of end-user-path failure,
but together they block removal, disablement or package exclusion of the
recovery path.

## Root cause and owner-boundary result

The current, hash-equal `v7-user-desired-state` source has two coupled
correctness defects in the observed warning/failure branch:

1. `warn()` can return the false status of its conditional assignment after
   the aggregate result is already `WARN`; under `set -e` this aborts the
   checker before its terminal `V7_USER_DESIRED_STATE=...` line.
2. A later route-get mismatch assigns `WARN` over an already detected `FAIL`,
   so severity is not monotonic.

This is a Control/Recovery safety observation, not a permissible generic RS7
simplification item. Existing health/state and recovery/path-safety owners
retain the component. Re-entry requires one owner-backed correctness Mission
with: a fail-closed severity test matrix, preserved route/health semantics,
consumer and rollback proof, a fresh Matrix observation, and only then the
existing deploy/Runtime validation. No change to the helper, service, timer,
routing, state, Production or Authority was made here.

## Admission-contract correction

The existing RS7 lifecycle binding had an implementation-only restriction to
`MANAGEMENT_PLANE`, although its Program contract allows bounded non-Runtime
Engineering simplification. It now accepts exactly `MANAGEMENT_PLANE` or
`ENGINEERING_PLANE` when the existing packet proves Runtime, Production and
Authority impact are all `NONE`. `CONTROL_PLANE`, `DATA_PLANE`, recovery and
Authority-boundary work still fails closed through their current owners.

This permits a future fully evidenced `v7_sync_lib.py` Engineering-interface
candidate to use the existing lifecycle; it does not create a Mission, alter
CPS, authorize the desired-state repair, or broaden the current RS6 frontier.
The existing safe-deploy owner synchronized only this approved library after
the commit; post-deploy Runtime truth is aligned to `054bd117`.

## Validation and delta

```text
Focused lifecycle tests: 40 PASS
Local CPS/OMP consistency: PASS
GitHub / workspace / Runtime truth: FULLY_ALIGNED
CPS frontier changed: 0
Safe-deploy delta: one Engineering library; service/timer restart: 0
```

| Surface | Before | After | Delta |
| --- | --- | --- | --- |
| Product/runtime source | unchanged | unchanged | `0` lines/files/services/timers changed for the recovery residual |
| RS7 admission validator | Management-only | Management + Engineering non-Runtime scopes | one scope guard generalized; Control/Data/Recovery remain blocked |
| Tests | existing Admin lifecycle cases | plus Engineering acceptance and Control rejection | `+2` cases |
| Runtime deployment | previous admission library | existing admission library at `054bd117` | one approved Engineering library copied; no process/service/timer change |

**Next frontier:** retain `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`; do not
advance CPS. The smallest material re-entry is an existing-owner safety
admission for the desired-state helper and stale Matrix evidence, not physical
cleanup and not a generic RS7 Mission.

## Execution addendum — fail-closed projection persistence

The owner-backed correction described above was subsequently executed as two
small, reversible commits: `49b55345` and `84550530`. It fixes only the
existing `v7-user-desired-state` and `v7-user-desired-state-save` chain:

```text
v7-user-desired-state
  -> terminal V7_USER_DESIRED_STATE=OK|WARN|FAIL
  -> existing v7-user-desired-state-save
  -> existing user-desired-state.state
  -> existing health/path-sanity readers
```

The checker no longer exits before its terminal line when more than one
warning occurs, and a later route-get warning cannot lower a prior `FAIL`.
The saver now persists a syntactically complete terminal projection even when
the checker returns `1` for a real `FAIL`, then preserves that non-zero exit
for the existing health lifecycle. No new writer, state surface, consumer,
service, timer, owner, routing operation or Authority path was added.

### Evidence and validation

| Check | Result |
| --- | --- |
| Focused fail-severity/persistence tests | `3 PASS` (`WARN`, monotonic `FAIL`, persisted `FAIL`) |
| Target CPS/OMP and deploy tests | `69 PASS` |
| Shell syntax and diff whitespace | `PASS` |
| Safe deploy | `deploy-z8-14-Updatesystem-8455053-20260814T121932`; no service/timer restart |
| Runtime/GitHub/CPS truth after deployment | `FULLY_ALIGNED` / `PASS` / CPS frontier unchanged |
| Direct read-only checker | terminal `V7_USER_DESIRED_STATE=FAIL` (real failure is now observable) |
| Existing saver invocation | `SAVE_EXIT=1`, fresh state with `errors=124`, `V7_USER_DESIRED_STATE=FAIL` |

The pre-existing saved projection had remained at `2026-08-13 13:47:07` with
`V7_USER_DESIRED_STATE=OK`. The corrected existing saver wrote a fresh
projection at `2026-08-14 12:21:25` with `FAIL`. This is a truthful state
refresh by the existing owner, not a routing, policy, user-movement or
Authority effect. The health service was active and its deployed `ExecStart`
and saver hash matched source; its observed loop cadence remains a separate
runtime-lifecycle residual and was not changed by this bounded correction.

### Before / after / delta

| Surface | Before | After | Delta |
| --- | --- | --- | --- |
| Checker terminal on warning/failure branch | could abort or downgrade `FAIL` | terminal always emitted; severity monotonic | fail-closed result restored |
| Saved desired-state projection after real `FAIL` | stale historical `OK` | fresh terminal `FAIL` persisted | existing writer completes its state contract |
| Runtime files/services/timers | existing | existing | `0` created/removed/restarted |
| Source/test change across both commits | baseline | 5 files touched | `+157 / -3` lines; one test file added |
| Routing / policy / user movement / Authority | unchanged | unchanged | `NONE` |

**Historical residual and exact re-entry:** at this observation point,
`errors=124` was the reported desired-state failure and blocked any package
removal. The execution addenda below supersede its legacy-route interpretation
with Core-primary evidence. The stale/failed Matrix evidence and the observed
health-loop cadence required the existing health/recovery and Matrix owners to
provide fresh lifecycle evidence before a physical RS6 minimization decision.
CPS remains at
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`; no RS6 completion or frontier
advance is claimed.

## Execution addendum — canonical Matrix path-safety reader

The Matrix timer and writer were not stale: the observed timer invocation ran
successfully and the canonical `service-matrix.json` was fresh. The stale
artifact was the legacy `service-matrix-refresh.state` reader in the existing
`v7-path-sanity-check`; it still contained a May `FAIL` while the canonical
Matrix reported current per-egress `OK`, `WARN` and `FAIL` facts. Other current
Control/Management consumers already use the canonical JSON.

Commit `12aa5271` makes the existing observer read that canonical JSON first,
aggregate its item statuses conservatively (`FAIL` > `WARN` > `OK`), and emit
`UNKNOWN` rather than fall back to a stale legacy `OK` when a present canonical
file is empty or malformed. The old state file remains a compatibility
fallback only when the canonical file is absent. This changes no Matrix writer,
timer, consumer, routing decision, recovery action, policy, user or Authority
boundary.

```text
Matrix timer -> v7-service-matrix-refresh-all -> service-matrix.json
  -> v7-path-sanity-check -> v7-path-sanity.state -> existing path guard reader
```

| Check | Result |
| --- | --- |
| New canonical precedence/fallback tests | `3 PASS` |
| Combined desired-state, path-sanity, CPS/OMP and deploy tests | `75 PASS` |
| Safe deploy | `deploy-z8-14-Updatesystem-12aa527-20260814T124841`; no restart |
| Direct existing path-sanity observation | canonical Matrix note present; `egress_service_matrix=FAIL` and `V7_PATH_SANITY=FAIL` |

The final `FAIL` is intentional and truthful: the fresh canonical Matrix has
at least one current failed egress and desired-state has real errors. The
change removes a stale input, not the safety residual. Physical delta is one
existing observer modified plus one test file: `+119 / -2` lines; files,
services, timers, state surfaces, routes, users and Authority boundaries
created/removed/changed: `0` except the observer's own refreshed diagnostic
projection. The remaining exact RS6 blocker is actual health/admission and
Matrix recovery evidence, not the former stale Matrix read path.

## Provenance addendum — state merge and residue

`v7-state-merge` is no longer an unknown source/provenance blocker. Its tracked
`tools/runtime-support/v7-state-merge` source is in the existing approved
deploy manifest and its SHA-256 exactly matches `/usr/local/bin/v7-state-merge`.
The existing active health loop calls it; it atomically writes fresh
`summary.state` from benchmark, stability, status, load and diagnosis inputs.
Observed existing readers are egress history, diagnose, state JSON and stale
check. Its disposition is therefore `KEEP_RUNTIME`, not a removal candidate:
it is a live Control-plane aggregation writer with known source, deploy,
caller, state and readers.

During this targeted verification, `v7-system-check` was identified as a
state-refreshing diagnostic rather than a read-only command because its source
calls existing stability and merge writers. Its invocation was stopped and is
not used as evidence; it performed no routing, policy, user, service, timer or
Authority operation. The existing health service remained active and its
atomic `summary.state` projection stayed fresh. One exact old orphan file,
`summary.state.tmp.2634283` (dated `2026-07-29`, with no live writer PID), was
removed after verification. No current writer temp or durable state was
removed.

This closes only the state-merge provenance classification. At this point the
Matrix/desired-state observations, path-sanity unit provenance and other named
RS6 owner-backed exceptions remained; later execution addenda record the
desired-state/path-guard correction. No physical minimization or CPS advance
is claimed.

## Execution addendum — Core-primary desired-state semantics

The remaining `desired-state` failure was not a missing route repair. The
existing Core-primary owner correctly reported, in a direct read-only verify,
`CORE_PRIMARY_VERIFY_PASS`: `124` compatible users are mapped through `6`
classes, the Core nft table exists, all required fwmark rules exist, and legacy
per-user primary rules are intentionally absent. The prior desired-state helper
was therefore checking a retired primary mechanism and reporting every enabled
user as failed (`ip_rule_missing`, `table_route_mismatch`,
`route_get_mismatch`). Creating those old rules again would have violated the
Core-primary architecture.

Commit `3a87e078` reuses the existing `v7-routing-sync
--core-primary-verify --json` owner. When it returns
`CORE_PRIMARY_VERIFY_PASS`, desired-state verifies shared Core routing and
retains real per-user WireGuard/configuration checks, but no longer requires
retired per-user route rules. A non-passing Core verifier with no proven legacy
primary rules remains `CORE_PRIMARY_UNVERIFIED -> FAIL`; legacy validation is
used only when the existing verifier proves legacy primary rules are live.

| Check | Result |
| --- | --- |
| Core verify, deployed Runtime | `CORE_PRIMARY_VERIFY_PASS`; 124 users, 6 classes, no missing marks |
| Target regression suite | `79 PASS` |
| Safe deploy | `deploy-z8-14-Updatesystem-3a87e07-20260814T130003`; no restart |
| Direct desired-state | `CORE_PRIMARY_CLASS_ROUTING`, `errors=0`, terminal `OK` |
| Direct path-sanity | `user_policy_routes=OK`; canonical Matrix remains `FAIL`; overall `WARN` |
| Next existing path-guard timer | `WARN -> WARN`, actions `0`, failures `0`, `V7_PATH_GUARD_REPAIR=OK` |

The Matrix residual is now correctly isolated: current failed channel `1` has
`0` enabled users, while `vless=WARN` has `11`; neither fact caused a route,
policy, user-movement or Authority action. The existing path guard accepts the
result as `v7_path_watch`, rather than issuing the former unnecessary routing
sync. This closes the desired-state/path-guard false-failure chain. Physical
delta for this correction is two existing files changed, `+71 / -10` lines;
no files/services/timers/state surfaces/owners were created or removed.

The Program remains at `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. The next
work is still bounded provenance/residue closure for remaining live units and
legacy exceptions; it is not a routing recovery or permission to remove a
runtime package.

## Targeted provenance closure — Direct/RU autosync

`v7-direct-autosync` is a proven live Direct/RU runtime component, not an
unknown unit and not a physical-minimization candidate. The tracked source
`tools/runtime-support/v7-direct-auto-sync` and deployed
`/usr/local/bin/v7-direct-auto-sync` have the identical SHA-256
`f58d3f845022ea6deadb999feddadc0ba55341198b7eb95f342639af363228c4`.
Its existing owner is `Direct/RU`; the canonical lineage record classifies it
as `authoritative_runtime`, `runtime-critical`, and release-owned.

```text
v7-direct-autosync.timer (enabled, active, waiting)
  -> v7-direct-autosync.service (oneshot)
  -> /usr/local/bin/v7-direct-auto-sync
  -> Direct/RU domain inputs + policy direct-domain input
  -> direct domain file / autosync state
  -> dnsmasq render and restart only when the domain configuration changes
```

The source also has a guarded recovery caller from
`v7-path-guard-repair`, after a successful existing killswitch repair. The
observed service completed successfully at `2026-08-14 12:59:15+03:00`; the
active enabled timer triggered it, and its fresh state reported `changed=0`,
`render=SKIPPED`, `dnsmasq=active`, eight checked samples, and zero stale or
failed samples. This was observation only: the autosync itself was never run
manually in this recheck.

| Component | Owner | Source/deploy/lifecycle evidence | Effect | Final classification |
| --- | --- | --- | --- | --- |
| `v7-direct-auto-sync` | existing `Direct/RU` owner | source/live hash equal; existing lineage; enabled timer -> successful oneshot service | may update Direct/RU domains and restart `dnsmasq` only on a real configuration change | `KEEP_RUNTIME` / high-risk Direct/RU boundary |

There is no missing owner, caller, consumer class, deploy provenance or
rollback ambiguity that a generic RS6 package change can safely solve. Any
future change requires the existing Direct/RU owner, explicit policy-domain
consumer analysis, and `dnsmasq` rollback validation. It is therefore excluded
from the current physical-minimization admission, with no change to Runtime,
Production, Authority, route policy, service, timer, or CPS frontier.

## Targeted provenance closure — path-sanity observer

`v7-path-sanity-check` is a proven diagnostic observer/producer and not an
unknown runtime artifact. The tracked
`tools/runtime-support/v7-path-sanity-check` source and deployed
`/usr/local/bin/v7-path-sanity-check` have the identical SHA-256
`4e6fa4e20afb50a88f2780a97c7fd8097abe4a4dc62a69d6f5250e8839dfc09a`.
The existing manifest maps the source to that deployed binary. Its enabled
active timer triggers a successful static oneshot service every existing
five-minute lifecycle; `v7-path-guard-repair` is the confirmed recovery
consumer that reads its result before deciding whether its own existing owner
may act.

```text
v7-path-sanity.timer -> v7-path-sanity.service
  -> v7-path-sanity-check
  -> v7-path-sanity.state
  -> v7-path-guard-repair (existing decision/repair owner)
```

The observed fresh projection at `2026-08-14 13:06:23+03:00` has
`user_policy_routes=OK`, `warnings=1`, `errors=0`, and
`V7_PATH_SANITY=WARN`. The warning is attributable to the missing optional
`awg2` interface and the separately reported canonical Matrix direct-egress
fact; the projection explicitly marks the latter as not a full client-path
decision. The observer did not mutate routes, policy, users, services,
timers, Authority or Production.

| Component | Owner / role | Evidence | Final classification |
| --- | --- | --- | --- |
| `v7-path-sanity-check` | existing path-safety/guard boundary; diagnostic state producer | source/live hash equal; approved manifest mapping; enabled timer -> successful service; known recovery reader | `KEEP_RUNTIME` observer; not a routing writer |

`runtime-enumeration.json` contains an older historical hash and
`repo_present=false` snapshot for this executable. It is historical evidence,
not current Architecture Truth, and is not changed to manufacture a new
runtime claim. The current source/deploy/consumer chain above is the durable
fact used for this RS6 classification. Physical minimization remains
unadmitted for the path-safety boundary; no CPS frontier, Runtime, Production
or Authority change is claimed.

## Targeted residue closure — retained autoswitch backups

Seven dated `v7-users-autoswitch` backup executables remain in
`/usr/local/bin`, all from `2026-05-23` through `2026-05-27`. A direct
read-only Runtime check found no literal reference to any of them in
`/etc/systemd/system` and no active process command line. The current
`v7-users-autoswitch.timer` is enabled but inactive; its service is likewise
inactive and its configured command is the existing
`v7-governed-canary-dry-run-cycle --execute-l3-production-validation ...
--max-users 0`, not an autoswitch backup.

| Residue group | Proved absent | Not disproved | Existing owner / disposition |
| --- | --- | --- | --- |
| seven dated `v7-users-autoswitch.*backup*` executables | systemd reference and live-process consumer | dynamic/manual/deploy-boundary invocation | existing autoswitch + deploy/package owners; `OWNER_BACKED_EXCEPTION` |

This is a genuine reduction of the unknown surface, not a deletion decision.
An exact future removal Mission must first complete the existing owners'
negative dynamic/manual invocation and deployment-retention proof, define a
recoverable archive/delete action, and validate the governed autoswitch
contract. Until then all seven files are retained unchanged. No Runtime,
Production, Authority, route, user, service, timer or CPS change occurred.

## Targeted recovery closure — path guard post-correction lifecycle

`v7-path-guard-repair` is now a proven, healthy safety boundary rather than a
failed recovery residual. The tracked `hardening/v7-path-guard-repair` source
and deployed `/usr/local/bin/v7-path-guard-repair` have the identical SHA-256
`894a347a7e24e3d1ee10513cc7f0be7fdfce523e2711c8db6415695543f074c7`.
Its existing enabled two-minute timer invokes the static oneshot service with
the existing `--apply` mode.

The two latest naturally scheduled executions, including the run observed at
`2026-08-14 13:08:17+03:00`, completed successfully with the same result:

```text
before=WARN / v7_path_watch
after=WARN / v7_path_watch
actions=0
failures=0
V7_PATH_GUARD_REPAIR=OK
```

The source only enters its existing mutation calls (`sysctl`, MSS clamp,
Routing Sync, killswitch or Direct autosync) for a non-safe pre-check state.
Those calls were not taken in the observed successful runs. The current
`WARN` is therefore a truthful monitoring classification, not evidence of a
failed repair or permission to simplify the recovery path.

| Component | Existing role and evidence | Final classification |
| --- | --- | --- |
| `v7-path-guard-repair` | enabled timer -> successful `--apply` oneshot; source/live hash equal; consumes path-sanity result and may invoke bounded existing recovery only when unsafe | `KEEP_RUNTIME` safety/recovery boundary |

The service still consumes material CPU time while it performs its existing
checks (roughly 25–27 CPU seconds in the observed cycles). That is a measured
performance observation, not a removal or tuning authorization: any change
must first retain the current path-safety owner, prove equivalent checks,
rollback and no loss of recovery coverage. No service, timer, path guard,
routing, Runtime, Production, Authority or CPS change was made by this
verification.

## Targeted provenance closure — traffic accounting path

`v7-traffic-snapshot` is a proven product/runtime accounting path, not an
unowned binary. Its deployed SHA-256
`b42c6c1c82c78234007ae5fc3430375bcb0338ec0a5fb81183f16cb310746c23`
exactly matches the existing Git source at
`b8358323:hardening/v7-traffic-snapshot`. That same historical commit contains
the currently observed `v7-traffic-collector.service` and timer definitions;
the source is historical rather than a present tracked file, so this is
provenance recovery, not a claim that it has been reintroduced into the
current package.

```text
enabled 15-minute timer -> traffic-collector.service
  -> v7-traffic-snapshot --collect
  -> nft traffic counters + traffic.sqlite
  -> Admin traffic read model and read-only live endpoint calls
```

The live timer's latest successful run refreshed
`/opt/v7/traffic/traffic.sqlite` at `2026-08-14 13:01:14+03:00`. The existing
Admin API reads its `traffic_snapshots` and `traffic_totals` tables and uses
the binary only through the established `run_readonly` calls for live user or
egress views. The matched source shows why this is not removable: `--collect`
can ensure the existing nft accounting counter table/rules before writing the
SQLite snapshots. The systemd unit is deliberately low-priority (`Nice=10`,
best-effort I/O), but that is scheduling policy, not an exemption from the
product/accounting boundary.

| Component | Owner / consumers / effect | Final classification |
| --- | --- | --- |
| `v7-traffic-snapshot` plus collector unit/timer | existing traffic/accounting and Admin owners; scheduled counters + SQLite, Admin read model + read-only live calls | `KEEP_RUNTIME`; historical source/unit provenance retained |

Any future change must use the existing traffic/accounting, Admin and
deploy/package owners, preserve both retained traffic data and live read
responses, explicitly address the nft-counter side effect, and provide a
rollback path. No counter, SQLite, service, timer, Runtime, Production,
Authority or CPS state was changed in this recheck.

## Targeted provenance closure — active runtime-unit batch

Six previously incomplete unit mappings are now current source-to-Runtime
facts. Their tracked executable and unit definitions match the deployed
artifacts byte-for-byte; all are live in their expected long-running or
`RemainAfterExit` lifecycle. They are not removal candidates.

| Component | Current source / unit / live effect | Classification |
| --- | --- | --- |
| `v7-api.service` | `v7-api` source hash and tracked unit match; active local API is ordered after health and Routing Sync; Admin reports it as a service dependency | `KEEP_RUNTIME` Management/local API boundary |
| `v7-benchmark.service` | tracked benchmark helper hash and unit match; active five-minute measurement loop is ordered after Routing Sync | `KEEP_RUNTIME` measurement producer |
| `v7-killswitch.service` | tracked binary and unit match; active-exited boot leak guard precedes Routing Sync, benchmark, health and API, and is a guarded path-guard/egress-state recovery caller | `KEEP_RUNTIME` Data/Recovery safety boundary |
| `v7-mss-clamp.service` | tracked binary and unit match; active-exited client TCP MSS safety and conditional path-guard repair target | `KEEP_RUNTIME` network-safety boundary |
| `v7-public-gateway.service` | tracked binary and unit match; active `/connect` and profile gateway requires existing Admin API upstream | `KEEP_RUNTIME` public product ingress boundary |
| `v7-egress-openvpn@v7edb0c189291.service` | tracked template unit matches; active instance has explicit external `.ovpn` Runtime configuration and is governed by existing egress lifecycle tooling | `KEEP_RUNTIME` egress Data-plane support |

The seventh unit, `v7-proxy-inbound-happ-test.service`, is deliberately
separate but now has a complete existing-owner chain: the active `sing-box`
configuration is an external Runtime-generated artifact, while current
Admin owner-gates, candidate/identity/guard helpers and the guarded rollback
helper are source-to-deployed hash-equal. It remains `KEEP_RUNTIME` as a
public ingress boundary; this is not a removal or disablement authority.

This recheck closes source/deploy ambiguity for the six proven components and
narrows the remaining ingress residual to one exact owner-backed Runtime
configuration boundary. It made no changes to services, timers, processes,
kernel rules, routes, Runtime, Production, Authority or CPS.

## Targeted runtime observation — proxy ingress retained boundary

`v7-proxy-inbound-happ-test.service` is confirmed as a live public ingress,
not a stale unit name. Its active `sing-box` process listens on
`0.0.0.0:1443` from the external Runtime configuration
`/etc/v7/inbound-runtime/happ-test/public-candidate/sing-box.json`
(observed SHA-256 `98a4bcdd050a28487d5cb27040c3bd1d5e67a7af20f8673f806c00f6baf08b9b`).
The sanitised configuration exposes a VLESS inbound and several direct egress
route tags; no credentials or configuration secrets were collected. The unit
also owns its existing `uidrange 995-995 lookup 100` and public-source
ip-rule lifecycle.

| Component | Proved current effect | Disposition / exact re-entry |
| --- | --- | --- |
| `v7-proxy-inbound-happ-test.service` | active public listener + external Runtime configuration + privileged ip-rule lifecycle | `KEEP_RUNTIME`; external config is rendered and governed by existing Admin/proxy owners with deployed candidate, guard and rollback helpers |

This evidence eliminates the possibility of treating the unit as a dormant
test artifact. It does not evaluate configuration quality, infer unused route
tags, reveal secrets, or authorize changes to proxy, routes, Runtime,
Production, Authority or CPS.

## Current RS6 decision after targeted closures

The bounded rechecks have converted the previously broad runtime inventory
into decision-ready dispositions: Direct autosync, path sanity, path guard,
traffic accounting, API, benchmark, killswitch, MSS clamp, public gateway,
OpenVPN and proxy ingress are `KEEP_RUNTIME`; only the seven dated autoswitch
backups retain `OWNER_BACKED_EXCEPTION` status. No checked object has earned
`REMOVE_CANDIDATE` status.

```text
RS6 physical minimization verdict = NOT_READY
CURRENT CPS successor = EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION
NEXT LEGAL WORK = existing autoswitch + deploy/package owner archive/delete
packet after an explicit manual-operation retention decision
```

The order is intentional: the backup proof does not permit removal by itself;
it must first produce an existing-owner bounded Mission with Product Contract,
consumer migration (if any), validation, rollback and residue closure. CPS
remains the sole authority to admit that future physical work.

## Final targeted recheck — proxy validation and backup automation scope

The existing `sing-box` validator accepted the live proxy configuration
(`exit=0`) without starting or reloading any process. Redacted aggregate facts
are one inbound, twelve configured identities, five configured outbounds and
twelve route rules. The listener had zero established sessions at the sampled
instant; that is an observation, not evidence of no product consumer. The
external Runtime profile is not an orphan: current Admin owner-gates invoke
source-to-deployed candidate, identity and guard helpers, and the deployed
guard rollback helper exactly matches its tracked source. Together these facts
close its owner/config/consumer/rollback classification as `KEEP_RUNTIME`.

For the seven autoswitch backup executables, the negative search now covers
the existing automation and deployment surfaces: systemd, cron, current
`/opt/v7/ops` deployment manifests/checksums/unit summaries and current
`/usr/local/bin` executable scripts. It found zero literal backup references
and zero backup unit files, in addition to the already-proven absence from
live processes. This proves `NO_AUTOMATED_RUNTIME_CONSUMER_FOUND` for the
scoped surfaces. It deliberately does not claim that a human can never invoke
an absolute backup path, so the group remains `OWNER_BACKED_EXCEPTION` rather
than a removal decision.

| Residual | Current conclusion | Re-entry condition |
| --- | --- | --- |
| proxy ingress config | live, validator-accepted external Runtime boundary; existing Admin/proxy render, identity, guard and rollback chain source/deploy matched | `KEEP_RUNTIME`; no physical change candidate |
| autoswitch backups | no automated/deploy/process consumer found; manual invocation not negatively provable in this recheck | existing autoswitch + deploy/package owner archive/delete packet with manual-operation retention decision and recoverability proof |

The final RS6 result is unchanged: `NOT_READY_FOR_PHYSICAL_MINIMIZATION`,
`REMOVE_CANDIDATE = NONE`, and CPS successor
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. These checks performed no code,
config, service, timer, process, routing, policy, Runtime, Production or
Authority change.

## Final retention-contract check — autoswitch binary backups

No existing autoswitch/deploy/package retention, archive or deletion contract
for `/usr/local/bin/v7-users-autoswitch.*backup*` was found. The existing
`v7-maintenance-cleanup-preview` is deliberately not repurposed: it governs
only timestamped archive files in `/root/v7-backups` and explicitly does not
cover executable binaries. The sole historical governance-check reference to a
backup path is evidence text, not an invocation or retention policy.

Therefore the backup group remains an exact `OWNER_BACKED_EXCEPTION` with
`NO_AUTOMATED_RUNTIME_CONSUMER_FOUND`, not a self-authorized archive/delete
candidate. The smallest remaining implementation input is an explicit
existing autoswitch + deploy/package owner retention decision defining archive
location, recoverability period, rollback/restore procedure and post-action
negative consumer check. Until then `RS6_RUNTIME_PACKAGE_MINIMIZATION` is
correctly complete only as read-only evidence closure, not as physical
minimization authority.

## Existing OMP successor-consumer verification

The canonical source-side entrypoint
`tools/v7-truth-check --continue-omp --json` was invoked once without CPS
persistence. It returned `PASS` with
`RS_READ_ONLY_FRONTIER_PREEMPTS_GENERIC_OMP`, retained the current
read-only RS6 frontier, made no CPS write and returned the unchanged exact
successor `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. Its actual consumer is
`EXISTING_RS_READ_ONLY_PHASE_OWNER`.

The source contains no separate executable handler for the literal action
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. The existing
`--omp-permanent-polygon-consumer` is not such a handler: it consumes the
Permanent Polygon program's own obligation corpus. Invoking it for RS6 would
cross the active-Program boundary and would be invalid. No adapter, CPS
projection or substitute lifecycle was created.

| Fact | Result |
| --- | --- |
| standard OMP continuation | `PASS`; one acknowledgement only |
| CPS / Runtime / Production / Authority effect | `NONE / NONE / NONE / NONE` |
| exact RS6 physical decision | still blocked by the autoswitch backup retention decision |
| lawful re-entry | existing autoswitch + deploy/package owner supplies the retention packet, then the existing RS6 phase owner re-evaluates the same successor |

This is a closure of successor-routing evidence, not a new audit or a claim
that RS6 physical minimization is complete.
