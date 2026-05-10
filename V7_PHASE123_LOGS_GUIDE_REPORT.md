# V7 Phase 123 — Logs Guide

Date: 2026-05-11

## Goal

Bring the Logs section to the same compact admin UX model as the rest of Admin V2.

## What Changed

- Added a Logs hero action: `Карта логов`.
- Replaced static summary cards with reusable log-guide cards.
- Added a focused drawer explaining:
  - where user access logs live;
  - where egress/channel logs live;
  - where routing logs live;
  - where security/guarded-action logs live;
  - where disk/log retention is controlled.
- Kept raw event details behind row click/drawer behavior.

## Safety

- No event API changes.
- No retention or cleanup changes.
- No routing/systemd/firewall/user/channel changes.
- UI-only structure and navigation improvement.

## Operator Meaning

Logs now behave like a calm investigation center: short summaries in rows, focused filters by area, and technical details only when opened intentionally.

