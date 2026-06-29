# OpenVPN Live Audit Auth Blocked

Дата: 2026-06-29 23:29:51 +07

## Summary

Запрошен read-only live audit канала `openvpn-1779388847-d2ad7c`, потому что production UI показывает пользователей на канале с `0 services / service failure / непригоден`.

Live audit не завершен, потому что в текущей Codex-сессии нет безопасного authenticated production/session context.

## Action Performed

- Открыт production UI через in-app browser.
- Проверен production admin API без cookie.
- Проверен production SSH target из существующего V7 owner.
- Проверен существующий autoswitch owner локально.
- Исторические session cookie обнаружены, но не использованы.

## Live State

Не подтвержден.

Причина:

- Browser navigation открыл `https://v7-admin.195-2-79-116.sslip.io/login#channels`, то есть текущей browser session нет.
- `curl https://v7-admin.195-2-79-116.sslip.io/api/egress` вернул `unauthorized`.
- `ssh root@195.2.79.116` вернул `Permission denied (publickey,password)`.
- Использование сохраненных cookie из historical evidence было заблокировано как небезопасное session reuse без отдельного явного разрешения.

## Affected Users

Не подтверждены live.

Требуется authenticated read-only доступ к одному из:

- production UI/API session;
- production SSH read-only state files;
- existing approved production state owner.

## Per-user Why Cards

Не построены live.

Причина: нет доступа к актуальным `users.registry`, `egress.registry`, `service-matrix.json`, `egress-load-summary.json`, `egress-quality-summary.json` и `/api/autoswitch-plan`.

## Exact Blocker Reasons

Auth blockers:

1. `browser_session_missing`.
2. `admin_api_unauthorized`.
3. `ssh_permission_denied`.
4. `historical_session_cookie_reuse_not_allowed_without_explicit_operator_authorization`.

Known implementation facts from existing owner:

- `tools/v7-users-autoswitch` builds current and target candidates separately.
- `_gate_load` skips load gate for `purpose="current"`, so target overload semantics do not automatically evacuate current users.
- `_gate_service` can block unsuitable target candidates, but live proof is needed to determine whether it also makes the current channel ineligible for the affected users.
- decision logic only proposes movement when current is not eligible, or a better eligible target beats current and movement protection allows it.

## Is This Expected Behavior?

Unknown until live state is confirmed.

Expected if:

- current users are not actually on this channel;
- UI read model is stale;
- service matrix used by UI differs from planner truth source;
- movement protection/cooldown/freeze/authority blocks movement after planner explains it.

Potential bug if:

- live users are on `openvpn-1779388847-d2ad7c`;
- channel has true `0 services` / service failure in planner truth source;
- current candidate remains eligible;
- planner does not produce at least a governed evacuation proposal;
- no explicit blocker explains why.

## Is This A Bug?

Not determined.

Live authenticated read-only audit is required before classifying.

## Minimal Patch Proposal

None.

No patch may be proposed until live planner/current eligibility evidence is captured.

## Required Governed Operator Transaction

None yet.

If live audit proves real affected users and valid evacuation target, the next safe action is a governed operator transaction, not runtime automation.

## Canonical Knowledge Changes

NONE.

## Verdict

`LIVE_AUDIT_BLOCKED_PENDING_AUTHENTICATED_SESSION`

Need New Owner: FALSE.

Need New Backlog Item: FALSE.

Runtime Behavior Changed: NO.

Users Moved: NO.
