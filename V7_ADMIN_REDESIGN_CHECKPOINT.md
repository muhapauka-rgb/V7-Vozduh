# V7 Admin Redesign Checkpoint

Date: 2026-05-10

## Current Fixed Point

Current engineering point before admin redesign:

- Git commit: `bf79083 Fix admin v2 rendered JavaScript`
- Admin API deployed on VPS and active.
- `/admin-v2` was browser-smoke-tested through the VPS tunnel after fixing rendered JavaScript.
- All primary tabs open without a persistent `loading` state.
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

## Default Decisions For The Next Implementation Pass

These defaults are chosen to keep moving without risking the product idea:

1. Keep a separate `Settings` tab.
   Reason: cooldowns, thresholds, intervals, route modes, language/theme, and service preferences are low-frequency controls. Putting them into Security or Routing would overload those pages.

2. Keep `Add Channel` as a full section inside `Channels`, not a small modal.
   Reason: the safe egress flow is long: source, detect, preflight, runtime test, quarantine/ready, add disabled, runtime profile, enable readiness, enable. A drawer is too small for this without hiding risk.

3. Put `happ`/`Karing` public access runtime under `Identity` and `Users`, not under Egress.
   Reason: this layer is about how clients enter V7 and receive profiles. It is not an external VPN channel.

4. Postpone free-form layout editing.
   Reason: the prototype has edit/reset layout controls, but production-like admin should first support stable column visibility and saved filters. Free dragging can create confusing operator screens.

5. Keep contextual logs beside the object they describe.
   Reason: channel logs live in channel drawer, user logs in user drawer, routing logs in routing drawer, with the full event stream kept under `Logs`.

6. Keep raw technical JSON collapsed by default.
   Reason: the operator should see plain-language state first; raw output is still available for engineering diagnosis.
