# V7 Phase 1 - Core Routing and Safety Stabilization Report

## Scope

Phase 1 in this repository pass was intentionally bounded.

Implemented:

- routing state source-of-truth model;
- reconciliation mismatch taxonomy;
- kill switch hardening model;
- unified route verification model;
- formal route class semantics;
- direct/RU safety model;
- unified health model;
- runtime critical read-only test plan;
- state contract validation model;
- operator visibility foundation;
- auditability contract;
- read-only runtime contract validator.

Not changed:

- datapath;
- nftables;
- route tables;
- autoswitch logic;
- provisioning logic;
- admin API behavior;
- systemd units;
- transport runtime.

## Findings From Inspection

The project already has important Phase 1 foundations:

- `hardening/v7-killswitch-check` performs read-only kill switch and route table verification.
- `hardening/v7-provisioning-reconcile-check` compares registry state with runtime routes/interfaces.
- `tools/v7-egress-set-state` defaults to dry-run and requires `--apply` for mutation.
- `tools/v7-users-autoswitch` already contains safety files, quarantine concepts, cooldowns, and non-apply modes.
- `admin/v7-admin-api` exposes policy, direct/RU, autoswitch, audit, and route-check surfaces.

Main gaps formalized in this pass:

- state layers were not documented as desired/runtime/observed/effective;
- route classes needed authoritative safety semantics;
- health categories needed one shared vocabulary;
- runtime contract validation needed a read-only corruption/consistency helper;
- direct/RU failure needed explicit "degraded/blocker, not unsafe fallback" language.

## Verification Principle

Phase 1 verification must prove:

`policy intent -> Linux runtime -> effective datapath`

It must not stop at "tunnel is alive".

## Next Phase Gate

Do not proceed to Phase 2 until explicitly instructed.
