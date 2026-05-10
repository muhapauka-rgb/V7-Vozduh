# V7 Phase 122 — Settings Guide

Date: 2026-05-11

## Goal

Bring the Settings section to the same compact admin UX model as Channels, Routing, Checks, and Security.

## What Changed

- Added a Settings hero action: `Карта настроек`.
- Added a focused drawer guide for policy controls:
  - switching cooldown;
  - quality thresholds;
  - stability threshold;
  - load and manual rebalance;
  - health and benchmark loops;
  - client route modes;
  - informational service recommendations.
- Reused the same settings-control model for the guide and the user-impact table.
- Added a Settings overview card that opens the guide.

## Safety

- No routing changes.
- No systemd changes.
- No firewall or kill-switch changes.
- No user/channel state changes.
- UI-only explanation layer around existing settings.

## Operator Meaning

Settings now explain what each control does before the operator edits it. Runtime interval changes still require preview and guarded apply.

