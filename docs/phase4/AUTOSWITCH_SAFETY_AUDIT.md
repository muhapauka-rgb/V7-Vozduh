# V7 Phase 4 - Autoswitch Safety Audit

## Purpose

Every switch action must be auditable.

## Required Fields

Switch audit must include:

- actor;
- reason;
- confidence;
- user;
- route class;
- current egress;
- target egress;
- before state;
- after state;
- selected move type;
- verification result;
- rollback context;
- correlation id.

## Current Implementation Notes

Current autoswitch:

- sets `V7_SWITCH_REASON=autoswitch_<reason>` for `v7-user-switch`;
- can run route verification after apply;
- can rollback on verification failure;
- updates safety state after successful moves;
- exposes explanations in JSON plan.

## Gap To Close Later

Switch history/audit should persist confidence and explanation summary, not only command-level reason.

## Phase 4 Boundary

This file defines audit requirements. It does not alter existing audit logging.
