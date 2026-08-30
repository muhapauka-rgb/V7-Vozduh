# Packet-lock → Apply handoff: completed; next live boundary recorded

Date: 2026-08-30 (MSK)  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Scope: live ordinary VLESS failed-source recovery; no manual operational recovery.

## Outcome of this block

The exact selection made by V7 is now carried from Packet through the governed
Apply handoff without being lost when the Barrier view is reconstructed.  The
change was deployed as commit `8605a50a0c561baedd2f3a8b2b2f67d9835d0081`.

The normal Runtime caller then created a new operation itself at
`2026-08-30T13:24:36.471409+00:00`; no user, source, target, Packet, Lease,
Barrier, or route was selected or advanced by Codex.

## Live input and evidence

* Fresh Matrix evidence classified `vless` as unsuitable for the affected
  ordinary profiles: YouTube, Google, Google Auth and Instagram were failed
  (Telegram alone was available).
* The live affected ordinary scope was two enabled identities currently on
  VLESS: `10.7.0.126` and `10.7.0.127`.
* The normal owner selected the healthy existing target
  `wireguard-1779454504-c43409` for both identities.
* The post-deploy Packet was `pkt_77a4a330c5c507ace3eb5485`; its exact
  selected-move hash and Authority generation were retained through the
  Packet/Barrier handoff.

## Repair

The existing governed executor now supplies its in-memory Packet lock to the
existing Apply validation.  Apply accepts it only when Packet, operation,
Barrier, selected-move hash, Authority/generation and cohort all match.  A
foreign or incomplete lock stops safely.  No new owner, state store, route
writer, timer, planner or source of truth was added.

Focused verification passed: 639 tests, including the two-member recovery of
a lossy Barrier reconstruction and rejection of a foreign Barrier.

Deployment used the existing `tools/v7-safe-deploy` owner:
`deploy-z8-14-Updatesystem-8605a50-20260830T162226`.  Local, GitHub and
Runtime hashes aligned at `8605a50…`; `v7-health.service` was active.

## Result after the repair

`approved_plan_lock_selected_moves_missing` did not recur.  The automatic
transaction proceeded to the next independent safety guard and stopped before
any assignment or route change with:

`core_primary_cohort_not_admissible_before_authority_consumption`.

This is not a recovery success and no seven-second result is claimed.

## Exact next frontier

The current Core-primary route-class derivation assigns marks by the sorted
set of egresses occupied by enabled users.  Moving the last two enabled VLESS
members would retire that class and renumber unrelated classes, so the
affected-cohort-only commit correctly refuses it.  The next work is to inspect
and reuse the existing route-class policy/owner to make class identity stable
without restoring a per-switch global rebuild or widening this operation.
Only after that generic repair can the normal V7 Runtime re-enter and provide
a valid all-affected recovery timing result.
