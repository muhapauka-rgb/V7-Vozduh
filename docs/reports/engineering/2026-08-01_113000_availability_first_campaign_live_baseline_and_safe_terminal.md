# Availability-first campaign: live baseline and safe terminal

Date: 2026-08-01  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission class: existing-owner reconciliation; no new Program or Mission  
Verdict: `CURRENT_SOURCE_SCOPE_EMPTY_WITH_DURABLE_AUTOMATIC_REENTRY`

## Live owner-backed baseline

- CPS generation: `cpsgen_SFA_SDPC_285AF5FC6F4D_AVAILABILITY_STAGE_25`;
- live standing contract: `sdpc_285af5fc6f4de20415c3e5b1`, expiry
  `2026-08-29T16:56:59.965252+00:00`;
- envelope: fresh existing-Planner target only, at most 48 controlled
  identities, one concurrent transaction, fresh Candidate/Packet/lease and
  all live verification, capacity, cooldown, anti-flap and rollback gates;
- current VLESS incident: `sfinc_be20296fba3d8a6a33e58a583f1b58db`;
- current route-backed scope: affected `0`, protected `0`, unresolved `0`,
  excluded/recovered `0`;
- current incident frontier: `CURRENT_SOURCE_SCOPE_EMPTY`.

## Reuse result

The deployed existing Matrix -> availability allocation -> serialized
packet-set -> Outcome/Replay/Learning -> baseline-reset -> stage-receipt
chain already provides the requested serial cohort semantics, exact-once
protection and partial-cohort recovery.  Commit
`ca4667289b495f0096b1c8e0596626ada4d1d892` repaired the only discovered
avoidably repeated recovery work by reusing immutable forward lineage inside
one Matrix Mission while retaining fresh per-member live gates.

No new executor, queue, registry, watcher, Planner, Runtime, Authority owner
or policy store is required.  No generic ladder certification was rerun.

## Effects deliberately absent

No manual Matrix invocation, Candidate, Packet, lease, restore-barrier write,
Runtime apply, routing mutation, user movement, rollback apply, policy write,
Authority expansion, Production Maturity change, fault injection or Natural
L8 manufacture occurred.

Starting Stage 25 or Stage 48 with no eligible source identity would create
the condition instead of consuming it and is forbidden.  Multi-user packets
or concurrency above one remain separately classified Authority boundaries;
they are not inferred from the active serial envelope.

## Re-entry

The existing ordinary Service Matrix observation is the sole producer of the
next matching positive-scope successor.  A fresh source degradation with an
eligible source identity, healthy distinct target, sufficient live capacity
and all standing-policy gates will re-enter the existing serial cohort path
automatically.  A fresh source baseline remains required for the currently
isolated controlled campaign source.

## Verification

- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`: `ALIGNED`;
- local/GitHub commit: `b8c6a466452c290fea1c4823cf94513d7503f91d`;
- deployed Runtime binary provenance: `ca4667289b495f0096b1c8e0596626ada4d1d892`;
- local/report-only commit difference from Runtime: accepted `DOCS_ONLY_MISMATCH`.
