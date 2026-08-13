# RS6.1 Runtime Provenance Closure Report

**Status:** `RS6_1_READ_ONLY_RECONCILIATION_COMPLETE_NOT_READY_FOR_PHYSICAL_MINIMIZATION`
**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## 1. CPS and method

The CPS Section 0 projection is unchanged: active Program `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`, stage `RS6_RUNTIME_PACKAGE_MINIMIZATION`, successor `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. This is the read-only `RS6.1` gate; it neither changes CPS nor admits RS7/physical minimization.

Evidence compared tracked source, current `tools/v7_sync_lib.py` manifest, the retained deployment snapshot `/opt/v7/ops/deploy-baseline/20260523T122251Z`, and a direct read-only production observation at `2026-08-13T21:24:01Z`. The snapshot supplies history/hash provenance only; current `systemctl` and binary output supply lifecycle truth.

## 2. Runtime provenance map

| Component | Source → deployed artifact → lifecycle | Owner, caller/consumer, state/effect | Classification / remaining gap |
| --- | --- | --- | --- |
| `v7-path-guard-repair` | Current `hardening/v7-path-guard-repair` SHA-256 equals live binary (`894a…074c7`); current manifest has no entry, historical baseline records binary/unit/timer. Enabled persistent 2-minute timer; static service currently failed exit 1. | Existing recovery/restore-barrier/path-safety owners; timer caller; reads/writes path-sanity evidence and writes `v7-path-guard-repair.state`; may call sysctl, MSS clamp, Routing Sync, killswitch, Direct autosync and optional TUN repair. | `KEEP_RUNTIME`; unit-source/deploy reproducibility and failed recovery result are `RUNTIME_PROVENANCE_GAP`. Re-enter with existing recovery plus deploy/package owners. |
| `v7-direct-auto-sync` | Current `tools/runtime-support/v7-direct-auto-sync` SHA-256 equals live binary (`f58d…228c4`); current manifest/unit source absent, historical baseline records binary. Static service with enabled persistent 10-minute timer; last run exited 0. | Existing Direct policy/product and deploy/package owners; timer and optional path-guard caller; reads policy domains, writes Direct config plus `direct-ru-autosync.state`, renders DNS and may restart dnsmasq; no Core forwarding consumer found. | `LEGACY_EXCEPTION`; current source-to-unit deployment mapping, consumer/rollback contract and retained disposition missing. |
| `v7-health.service` | Tracked `systemd/drafts/v7-health.service` matches observed seven-command loop; six helpers have source, `v7-state-merge` does not; unit is absent from current deploy manifest. Enabled and active. | Existing health/state and deploy/package owners; it calls history, stability, load, diagnose, state merge, desired-state save and JSON save; creates control-plane projections only. | `KEEP_RUNTIME`; incomplete helper/unit provenance forbids package exclusion. |
| `v7-state-merge` | No current tracked source or manifest; live SHA-256 `216a…bdfb` matches retained deployment snapshot. Called by health every ~30 seconds and diagnostic system check. | Existing health/state owner; reads benchmark, stability, status, load and diagnosis; writes `summary.state`, consumed by history, diagnose, state JSON, admin/state readers and stale check. | `UNKNOWN_REQUIRES_EVIDENCE`; live behavior exists but reproducible source/deploy input does not. |
| `v7-path-sanity-check` | No current tracked source or manifest; live SHA-256 `567a…c890` matches retained snapshot. Static service plus enabled persistent 5-minute timer; last run succeeded. | Existing path-safety/recovery owners; timer and path guard call it; reads desired-state and Matrix state, writes `v7-path-sanity.state`, consumed by path guard. | `UNKNOWN_REQUIRES_EVIDENCE`; source and unit deployment input missing. |
| `v7-traffic-snapshot` | No current tracked source or manifest; live SHA-256 `b42c…46c23` matches retained snapshot. Static service plus enabled persistent 15-minute timer; last run succeeded. | Existing traffic/accounting and admin API owners; reads nft counters and registries, writes traffic SQLite/history; `admin/v7-admin-api` declares both database and binary as consumer inputs. | `KEEP_RUNTIME`; real consumer/effect proven, source/deploy input missing. |
| Retained backup executables | Seven `v7-users-autoswitch.*backup*` binaries remain in `/usr/local/bin`; current unit files reference none. | Existing autoswitch and deploy/package owners; no systemd consumer found, but dynamic/manual invocation is not disproved. | `UNKNOWN_REQUIRES_EVIDENCE`; retain unchanged until full invocation/lifecycle search reaches owner-backed residue disposition. |
| Other active units without complete current package mapping | `v7-api`, `v7-benchmark`, `v7-killswitch`, `v7-mss-clamp`, `v7-proxy-inbound-happ-test`, `v7-public-gateway`, `v7-egress-openvpn@v7edb0c189291` are live. | Their existing component plus deploy/package owners; API, measurement, safety, ingress/gateway and egress-support effects were observed, not inferred from reports. | One `RUNTIME_PROVENANCE_GAP` per unit: `UNKNOWN_REQUIRES_EVIDENCE`; re-enter with exact source, deploy, caller, consumer and lifecycle proof. |

## 3. Health state writer/reader map

| State | Writer | Verified reader/consumer | Residual |
| --- | --- | --- | --- |
| `egress-history.jsonl` | `v7-egress-history` | `v7-egress-stability` | source and direct reader mapped |
| `stability.state`, `egress-load.state`, `egress-diagnose.state` | respective health helpers | `v7-state-merge`, readiness/governed consumers | merge source provenance missing |
| `summary.state` | `v7-state-merge` | history, diagnose, `v7-state-json`, admin/state readers, stale check | writer source missing; no claim that hidden/manual readers are absent |
| `user-desired-state.state` | `v7-user-desired-state-save` | `v7-state-json` | observed stale from 13:47 MSK while health is live: `MISSING_RUNTIME_EVIDENCE` |
| `v7-state.json` | `v7-state-json-save` | API, intelligence and governed runtime validation | source/reader mapped and observed fresh |

The table maps named health-loop writers and direct readers only. It does not prove the absence of hidden writers/readers and grants no merge, disablement or deletion authority.

## 4. Re-entry and verdict

```text
NOT_READY_FOR_RS6_PHYSICAL_MINIMIZATION
```

Two previously ambiguous binaries are now source-to-live-hash matched. The stricter gate remains open: path-guard is actively failing; live `v7-state-merge`, path sanity and traffic collector lack current source/unit deploy provenance; Direct autosync lacks unit/rollback disposition; desired-state freshness is unproven; and listed active/backup objects remain unresolved. `REMOVE_CANDIDATE = NONE`.

Required existing owners and re-entry: recovery/restore-barrier/path-safety plus deploy/package must reconcile path-guard failure and unit provenance; Direct policy/product plus deploy/package must reconcile Direct unit/rollback/lifecycle; health/state, path-safety and traffic/accounting plus deploy/package must locate/version source or issue retained disposition; desired-state owner must prove a fresh successful writer or exact failure consequence; each remaining active/backup object needs its affected component owner plus deploy/package map.

No source, Runtime, Production or Authority state was changed. No service or timer was started, stopped, enabled, disabled or restarted. The exact successor remains `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`; its next legal work is reconciliation only, not physical minimization.

## 5. Program-contract change delta

The existing OMP Program gained one `RS6.1` subphase row, a compact evidence-field rule and the corresponding completion gate. No Program, owner, truth source, Runtime, audit framework or registry was added. This report and contract change are documentation-only: product/runtime files, services, timers, dependencies and routing behavior changed by this stage: `0`.
