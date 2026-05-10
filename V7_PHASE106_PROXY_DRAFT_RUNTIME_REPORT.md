# V7 Phase 106 — Proxy Draft Runtime Test

Дата: 2026-05-10

## Что добавлено

- `v7-egress-draft-runtime-helper` теперь поддерживает isolated runtime-test для proxy-based egress:
  - VLESS
  - VMess
  - Trojan
  - Shadowsocks / Outline-like `ss://`
  - sing-box JSON outbound

## Как это работает

1. Черновик канала уже должен пройти preflight.
2. Helper создаёт временный sing-box профиль в каталоге тестового запуска.
3. sing-box запускается отдельно от рабочего сервиса, на случайном `127.0.0.1:<port>`.
4. Проверяется:
   - `sing-box check`
   - что временный SOCKS listener поднялся
   - внешний IP через временный SOCKS
   - сервисная матрица при quarantine test
   - cleanup после теста
5. Канал не добавляется в routing, не меняет kill switch и не получает пользователей.

## Safety

- Рабочий `/etc/sing-box/config.json` не трогается.
- Рабочий `sing-box.service` не перезапускается.
- Пользовательские маршруты не меняются.
- Временный процесс завершается в `finally`.
- Runtime config и log остаются в root-only test directory для аудита.
- Секреты не выводятся в UI/JSON как raw config.

## Проверки

- `python3 -m py_compile hardening/v7-egress-draft-runtime-helper admin/v7-admin-api`
- unit parse smoke-test для VLESS share
- `git diff --check`
- `tests/run-local-checks.sh`
- VPS deploy smoke-test в `/tmp`:
  - временный Shadowsocks draft
  - `sing-box check = OK`
  - temporary SOCKS listener поднялся
  - внешний IP ожидаемо не прошёл из-за несуществующего endpoint
  - cleanup = OK

## Что осталось дальше

- Добавить полноценный runtime adapter для OpenVPN.
- Добавить Clash YAML import/conversion в sing-box draft.
- Улучшить UI-карточку proxy runtime результата отдельными русскими пояснениями для `proxy_ready`, `external_ip`, `service_matrix`.
