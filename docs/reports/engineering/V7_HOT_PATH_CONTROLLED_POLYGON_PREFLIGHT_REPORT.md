# V7 Hot-Path Controlled Polygon Preflight Report

Date: 2026-08-14  
Mission: `V7_HOT_PATH_CONTROLLED_FAILOVER_PREFLIGHT_V1`  
Classification: `READ_ONLY_CONTROLLED_CERTIFICATION_ADMISSION_CHECK`

## Purpose

Determine whether the existing Polygon-selected, controlled-production path can
produce a real bounded `channel hard-fail failover` timing receipt without
waiting for a natural ordinary-user failure. This is an admission check only;
it is not a Polygon runtime execution path.

## Evidence checked

| Check | Result |
| --- | --- |
| CPS Section 0 | `PASS`; active Program remains RS6 and its successor remains `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. |
| Runtime truth access | `PASS`; Matrix timer is active and runtime provenance is known. |
| Standing delegated policy | `PASS`; `channel hard-fail failover` is in the existing policy scope, serial execution is enforced, and controlled-certification runtime scope is bounded. |
| Ordinary-user protection | `PASS`; the existing policy requires zero ordinary-user delta for the controlled path. |
| Controlled campaign admission | `STOP_SAFE`; no exact current campaign/substrate authority binding exists. |
| CT-M0F one-user standing-source selection | `STOP_SAFE`; no eligible source/identity/target triple is currently selected. |

## What is available

The existing owners already provide the intended legal chain:

```text
Polygon scenario selection
-> Controlled Production Certification owner
-> Matrix observation
-> fresh Situation / Decision / Candidate / Packet / lease
-> governed apply / verification / rollback or restoration
-> timing receipt and Outcome Passport
```

Polygon is therefore an Engineering Plane selector and acceptance corpus. It
does not synchronously make a routing decision or directly move a client.

## Admission verdict

`STOP_SAFE_NOT_READY_FOR_CONTROLLED_FAILOVER_EXECUTION`

The read-only CT-M0F selector reported these exact blockers:

1. `no_healthy_isolated_controlled_source_with_group_aligned_certification_identity`
2. `no_exact_certification_identity_for_controlled_condition`
3. `no_distinct_controlled_contract_admitted_target`

The production status does show an existing isolated source with certification
users and a healthy execution-only target, but their current group/contract
admission is not the exact one-user CT-M0F binding. Treating those facts as an
implicit binding would bypass the existing certification-pool and target
owners, so it is prohibited.

## Effects and delta

| Dimension | Result |
| --- | --- |
| Runtime effects | `NONE` |
| Production effects | `NONE` |
| Authority effects | `NONE` |
| Candidate / Packet / lease | `NONE CREATED` |
| Routing / user movement | `NONE` |
| CPS frontier | unchanged |
| Source LOC / runtime files | unchanged |

## Exact next step

Use the existing controlled-certification pool/topology owner to establish an
exact group-aligned certification identity plus an independently admitted
controlled target. This must be represented through the existing owner-backed
authority/admission flow; it must not be inferred from historical pool members
or accomplished by moving an ordinary customer. Then rerun
`--ct-m0f-standing-source-selection`; only a `PASS` result may open one fresh,
serial controlled failover transaction.

Natural L8 observation remains a separate passive lane. This controlled L7
path removes the need to wait indefinitely for it, but cannot be labelled as
natural-production evidence.
