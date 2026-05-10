# V7 Phase 127 — User Inspection Flow

Date: 2026-05-11

## Goal

Improve the second real operator workflow: inspect a user and understand what to do next.

## What Changed

- Added a user drawer operator snapshot:
  - overall verdict;
  - profile state;
  - route reality;
  - speed measurement state.
- Added an operator checklist:
  - profile;
  - connection;
  - route;
  - leak risk;
  - speed;
  - logs.
- Added direct actions in the user drawer:
  - check user;
  - request speed;
  - open logs;
  - issue/reissue profile;
  - generate Karing RU_LOCAL;
  - switch egress;
  - enable/disable preview.

## Safety

- UI-only inspection improvement.
- Read-only checks and drawers do not change routing.
- Speed request is still manual.
- Egress switch and enable/disable remain explicit guarded actions.

## Operator Meaning

The user drawer now answers the practical question: “Is this person connected and healthy, and what should I do next?”

