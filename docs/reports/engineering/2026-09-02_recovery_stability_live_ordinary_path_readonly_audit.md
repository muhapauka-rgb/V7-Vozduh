# Recovery Stability — live ordinary-path read-only audit

Date: 2026-09-02
Mission: `V7_RECOVERY_STABILITY_HARDENING_AND_STATE_SEQUENCE_SOAK`
Block: current Runtime ordinary-path eligibility audit

## Purpose

Check whether a current live ordinary recovery can be credited without
manufacturing an incident, target, Candidate, Packet, Lease, Barrier or route
mutation.

## Read-only evidence

The existing production `v7-users-autoswitch --pretty` planner was read
through the configured `v7-vps` production alias without `--apply`.

- The planner returned zero selected moves: there was no current eligible
  ordinary recovery transaction at this read.
- Its terminal was `DRY_RUN`; no governed Apply, route change or user movement
  occurred.
- The planner exposed expired intelligence/trust snapshots.  This makes the
  broad advisory dry-run stop, but it is not by itself evidence that a current
  ordinary recovery is blocked.

The deployed ordinary-failure branch already contains the required limited
exception: after fresh Matrix proof and an existing selected ordinary move,
stale advisory snapshots are deferred to the existing Candidate/Packet/Lease/
Barrier rechecks.  Matrix, current Authority, exact target eligibility, route
writer and required-service S11 remain mandatory; stale advisory data gets no
Apply exemption.

## Runtime alignment

Independent `v7-truth-check --all` passed in its authorised read-only network
context.  The live Matrix owner is proven active and the Runtime remains on
the last deployed functional code commit `75fe43e3`.  Local test/report-only
commits are explicitly non-deployable and therefore do not represent a
production-code mismatch.

## Boundary

This audit does not create ordinary live-path acceptance credit: no current
ordinary failure/recovery transaction existed.  The Program law forbids Codex
from creating one or manually advancing its recovery.  Final live evidence
therefore requires an operator-created lawful bad placement of an existing
ordinary-approved identity, followed solely by the normal `v7-health` caller.
Until an existing owner proves a bounded test identity is ordinary-semantics
equivalent, certification identities cannot substitute for that event.

## Safety and simplification

No Runtime code, configuration, Matrix state, timer, Authority, registry,
route or customer assignment was changed.  The audit reused the existing
planner and truth-check owners and added no state or process.
