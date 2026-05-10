# V7 Phase 109 — OpenVPN Normalize Preview

Дата: 2026-05-10

## Что добавлено

- Для OpenVPN draft добавлен read-only normalizer preview:
  - endpoint: `/api/actions/egress-draft-openvpn-normalize-preview`
  - кнопка `Normalize` в таблице draft-каналов `admin-v2`
  - результат показывается в wizard card

## Что проверяет normalizer

- OpenVPN client profile detected.
- Наличие обязательных полей:
  - `client`
  - `remote`
  - `dev`
  - auth material: `auth-user-pass` или `cert/key`
- Dangerous scripts/hooks:
  - `script-security`
  - `up`
  - `down`
  - `route-up`
  - `route-pre-down`
  - другие hook-директивы
- Route ownership:
  - `redirect-gateway`
  - `route`
  - `route-ipv6`
  - `pull-filter`
  - `route-nopull`

## Safety

- Preview не пишет runtime profile.
- Preview не запускает OpenVPN.
- Preview не меняет routes, kill switch, registry или users.
- Secret blocks редактируются:
  - `<key>`
  - `<tls-auth>`
  - `<tls-crypt>`
  - `<auth-user-pass>`

## Почему это важно

OpenVPN часто несёт route/script поведение внутри `.ovpn`. Для V7 это опасно, потому что маршрутизацией должен управлять V7, а не сторонний конфиг. Normalizer preview показывает, что будет нужно убрать/изолировать перед будущим runtime adapter.

## Проверки

- `python3 -m py_compile admin/v7-admin-api`
- unit smoke-test OpenVPN normalizer:
  - route/script blockers detected
  - secret block redacted
  - no write/runtime flags
- extract `admin-v2` JavaScript
- `node --check /private/tmp/v7-admin-v2-phase109.js`
- `git diff --check`
- `tests/run-local-checks.sh`
- VPS deploy:
  - backup `/root/v7-admin-api.bak.<timestamp>.phase109`
  - `v7-admin-api.service` active

## Следующий шаг

- Clash YAML converter preview:
  - распознать proxies;
  - предложить V7-managed sing-box outbound draft;
  - ничего не запускать и не добавлять в pool до отдельного adapter test.
