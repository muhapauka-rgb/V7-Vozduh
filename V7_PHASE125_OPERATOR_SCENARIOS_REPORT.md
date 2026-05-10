# V7 Phase 125 — Operator Scenarios

Date: 2026-05-11

## Goal

Validate the admin redesign against real operator workflows and make frequent actions easier to find.

## What Changed

- Added a top `Сценарии` action.
- Added an overview block `Сценарии оператора`.
- Added a focused drawer with common workflows:
  - issue a user profile;
  - inspect a user;
  - inspect an egress channel;
  - check routing policy;
  - run diagnostics;
  - investigate logs.

## Safety

- UI-only shortcut layer.
- No user, egress, route, firewall, systemd, or state changes.
- Scenarios open existing guarded workspaces and drawers.
- Dangerous actions still require preview, backup, audit log, or typed confirmation.

## Operator Meaning

The admin now has a practical starting point for day-to-day work: an operator can choose the job they are trying to do instead of hunting through sections.

