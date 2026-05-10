# V7 Admin Redesign Checkpoint

Date: 2026-05-10

## Current Fixed Point

Current engineering point before admin redesign:

- Git commit: `f047403 Add identity device quality table`
- Admin API deployed on VPS and active.
- Identity/onboarding work is paused intentionally, not abandoned.

## Paused Current Horizon

We paused the user identity/onboarding improvement track at this point:

1. Add plain-language reasons to `Device Quality` statuses.
2. Improve per-user readiness summary.
3. Connect readiness to route reality and leak-risk checks.
4. Make the user detail modal/card the main operator workspace for a person.
5. Continue safe egress onboarding wizard.
6. Continue service-aware routing and policy groups.

## New Focus

The new active work track is admin redesign and navigation rethink.

Required workflow:

1. Read the provided HTML design file.
2. Compare the design with the currently implemented admin features.
3. Identify implemented, missing, and unaccounted functionality.
4. Propose where missing functionality should live in the redesigned admin.
5. Keep the new design consistent with the provided design language.
6. Ask only for decisions that affect navigation, ergonomics, or risk of breaking the product idea.
7. Then implement the approved redesign plan step by step with checks.

## Safety Rule

Do not remove existing admin capabilities during redesign. If a feature does not have a clear place in the new layout, preserve it in a safe operator section until it is intentionally redesigned.
