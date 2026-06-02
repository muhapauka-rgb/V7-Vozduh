# Convergence A System Inventory

Project: V7 Vozduh
Program: Project Convergence
Block: Convergence A
Mode: Audit / Discovery / Convergence Planning
Date: 2026-05-31

## Reality Baseline

| Area | Evidence |
| --- | --- |
| Runtime Admin API | `/usr/local/bin/v7-admin-api`, hash `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04`, active `v7-admin-api.service` |
| Runtime counts | `/usr/local/bin` 181 files, `/etc/systemd/system` 45 files, `/etc/v7` 90 files, `/opt/v7` 509 files at maxdepth 3 |
| Local Admin API | `admin/v7-admin-api`, hash `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e`, dirty |
| GitHub development source | `origin/Updatesystem`, branch SHA `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`, Admin API hash `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` |
| GitHub release history | `origin/main`, branch SHA `593619d494e215d11fd826086593527a4a555690`, Admin API hash `7f33f9721777e726c81617e984fd581cc9b5c1c3e2ecc7f74726b18b2a580977` |

## Subsystem Inventory

| Subsystem | Purpose | Owner | Truth Source | Runtime Presence | Local Presence | GitHub Presence |
| --- | --- | --- | --- | --- | --- | --- |
| Authority | define operator/runtime authority boundaries | Admin/Governance | runtime behavior plus `Updatesystem` source | present through governance/operator surfaces | present | `Updatesystem` baseline |
| Candidate | candidate review and approval pipeline | Admin P2.6/P2.7 | local candidate until reviewed | partial/absent P2.7 workflow | present | absent from `Updatesystem` |
| Execution | read-only execution visibility and future preview model | Admin P2.1-P2.7 | runtime for deployed read APIs, local for extensions | runtime read APIs present | expanded local work | absent from `Updatesystem` read API patch |
| Execution Contracts | contracts and contract drafts | Admin Execution | runtime read model plus local draft model | read APIs present | drafts and read model present | absent/partial |
| Execution Events | execution event timeline | Admin Execution | runtime event read model | present | present | absent from `Updatesystem` |
| Simulation | outcome/blast-radius/service-impact previews | Admin P2.5 | local candidate | absent/limited | present | absent |
| Readiness | validation/readiness preview and operational readiness | Admin P2.3 | local candidate plus runtime general readiness | general runtime readiness | expanded local execution readiness | partial baseline |
| Approval Center | operator/candidate approval views | Admin P2.7 | local candidate plus existing operator preview | operator approval preview | candidate approval center present | operator preview baseline |
| Governance Preview | non-executable governance preview | Admin/Governance | shared source | present | present | present in `Updatesystem` |
| Rehearsal Preview | non-executable rehearsal preview | Admin/Governance | shared source | present | present | present in `Updatesystem` |
| Validation Preview | validation gates/previews | Admin P2.3 | local candidate | absent | present | absent |
| Rollback Preview | rollback readiness/impact previews | Admin P2.4/P2.5 | hybrid | runtime rollback/explain read model | expanded preview/impact | partial/operator baseline |
| Operator Workflow | operator overview/timeline/evidence and candidate workflow | Admin UI | hybrid | operator observability present | expanded candidate workflow | `Updatesystem` baseline |
| Evidence | evidence bundles and evidence archive | Admin/Governance | runtime stores/source readers | present | present | `Updatesystem` baseline |
| Proposal | proposal records and detail/timeline | Admin/Governance | proposal stores/source readers | present | present | `Updatesystem` baseline |
| Runtime Trust | runtime fingerprint/drift/convergence visibility | Admin Trust | runtime trust store + source | present | present | `Updatesystem` baseline |
| Release Trust | release current/history visibility | Admin Trust | release trust store + Git refs | present | present | `Updatesystem` baseline |
| Users | live users and client state | Runtime | production `/opt/v7` state | present | readers only | source readers only |
| Channels | egress/channel state | Runtime | production `/opt/v7` and `/etc/v7` state | present | readers/tools only | source readers/tools only |
| Routing | live route state and policy | Runtime | production runtime state | present | readers/previews | source tools/baseline |
| Events | operational and execution events | Runtime/Admin | runtime event stores | present | readers present | partial source |
| Audit | audit logs and operator audit search | Runtime/Admin | production audit files + source readers | present | present | `Updatesystem` baseline |
| Admin UI | `/admin-v2` operator interface | Admin | hybrid | present | expanded local UI | `Updatesystem` baseline |
| APIs | authenticated admin JSON endpoints | Admin | hybrid | present | expanded local API set | `Updatesystem` baseline |
| Tools | runtime `v7-*` command set | Runtime/Tools | runtime hashes plus repo tools | 181 `/usr/local/bin` files | `tools/*` and `tools/runtime-support/*` | mostly `Updatesystem` |
| Runtime Support | helper scripts for policy, state, profile, maintenance | Runtime/Tools | repo plus runtime hash verification | present | `tools/runtime-support/*` | `Updatesystem` |
| Systemd | service/timer orchestration | Runtime | production `/etc/systemd/system` | present | partial `systemd/*` | partial |

inventory_complete=true
