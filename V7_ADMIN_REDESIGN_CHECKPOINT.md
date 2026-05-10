# V7 Admin Redesign Checkpoint

Date: 2026-05-10

## Current Fixed Point

Current engineering point before admin navigation redesign:

- Latest pushed Git commit before this navigation map: `a623333 Show user onboarding stages`
- Admin API deployed on VPS and active.
- `/admin-v2` was browser-smoke-tested through the VPS tunnel after adding onboarding stages.
- Current `Users` grid shows readiness and onboarding stage separately.
- Current dashboard distinguishes real operator blockers from normal waiting-for-user states.
- Identity/onboarding work is not being expanded further before navigation redesign.

## Paused Current Horizon

We paused the user identity/onboarding improvement track at this point:

1. Add plain-language reasons to deeper `Device Quality` statuses if still needed after navigation merge.
2. Continue safe egress onboarding wizard.
3. Continue service-aware routing and policy groups.
4. Continue server-side Sensitive RU abroad/strict path later.

Do not expand profile delivery before navigation redesign. The approved delivery rule is intentionally simple: user presses connect, downloads the profile, can repeat if distracted, and unused links expire after one day.

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

## Approved Navigation Map

The lossless navigation map is now captured in:

- `V7_ADMIN_NAVIGATION_MAP.md`

Target top navigation:

1. `Главная`
2. `Пользователи`
3. `Каналы`
4. `Маршруты`
5. `Проверки`
6. `Безопасность`
7. `Настройки`
8. `Логи`

Important approved changes:

- Merge current `Users` and `Identity` into `Пользователи`.
- Keep `Add Channel` as a full staged section inside `Каналы`.
- Put RU/Gosuslugi/bank behavior under `Маршруты`, not a separate page.
- Keep simple delivery link states only: issued, downloaded, expired, issue again.
