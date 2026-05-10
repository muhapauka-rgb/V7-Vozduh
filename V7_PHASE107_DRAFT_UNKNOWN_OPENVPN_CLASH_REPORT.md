# V7 Phase 107 — Draft Unknown / OpenVPN / Clash Detection

Дата: 2026-05-10

## Что добавлено

- Админка теперь распознаёт OpenVPN `.ovpn` как отдельный тип draft:
  - `protocol=openvpn`
  - `runtime_mode=interface`
  - проверяются базовые признаки: `client`, `remote`, `dev`, auth material
  - scripts/hooks помечаются как blocker

- Админка теперь распознаёт Clash YAML как отдельный тип draft:
  - `protocol=clash_yaml`
  - `runtime_mode=proxy_or_tun`
  - показывает, что нужен будущий converter в V7-managed sing-box profile

- Неизвестный формат теперь можно сохранить как безопасный черновик:
  - `status=draft_unknown`
  - `validation=draft_unknown`
  - `pool_action=not_added`
  - тесты и добавление в pool блокируются до исправления/адаптера

## Safety

- Такие черновики не попадают в рабочий routing.
- Они не меняют `egress.registry`.
- Они не меняют kill switch.
- Они не получают пользователей.
- OpenVPN/Clash preflight намеренно BLOCKED, пока нет безопасного runtime adapter/converter.

## Проверки

- `python3 -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper`
- smoke-test:
  - OpenVPN preview → `protocol=openvpn`
  - Clash YAML preview → `protocol=clash_yaml`
  - unknown text → `validation=draft_unknown`
- `git diff --check`
- `tests/run-local-checks.sh`
- VPS deploy:
  - `/usr/local/bin/v7-admin-api` обновлён
  - `v7-admin-api.service` active

## Что дальше

- Сделать отдельную красивую UI-подсказку для `draft_unknown` и `draft_incomplete`.
- Добавить OpenVPN normalizer:
  - запрет/изоляция scripts
  - route normalization
  - credentials handling
  - temporary interface cleanup
- Добавить Clash YAML converter в sing-box outbound draft.
