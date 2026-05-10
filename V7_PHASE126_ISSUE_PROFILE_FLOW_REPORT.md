# V7 Phase 126 — Issue Profile Flow

Date: 2026-05-11

## Goal

Make the first real operator workflow easier: issue a user profile without forcing the operator to understand every technical field.

## What Changed

- Added a compact guide at the top of the profile issue workspace:
  - user source;
  - route mode;
  - primary channel;
  - one-time delivery link.
- Added dynamic hints for:
  - source selection;
  - route mode selection;
  - preview vs real issue.
- Added explicit buttons:
  - `Preview`;
  - `Выдать профиль`.
- Updated delivery result wording:
  - send only the one-time link;
  - do not send raw profile contents or private keys;
  - if the user gets distracted or the link is not activated, issue a new link/profile.

## Safety

- UI-only workflow improvement.
- No backend endpoint changes.
- No profile-generation semantics changed.
- Preview remains read-only.
- Real issue still goes through the existing guarded backend flow.

## Operator Meaning

The operator now starts from the job they need to do: choose a user, choose the client/mode, run preview if needed, then issue a one-time link.

