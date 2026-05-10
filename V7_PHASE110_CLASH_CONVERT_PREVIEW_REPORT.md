# V7 Phase 110 — Clash YAML Convert Preview

Дата: 2026-05-10

## Что сделано

- Добавлен read-only preview-конвертер Clash YAML drafts.
- Поддержан разбор `proxies:` для:
  - Shadowsocks / `ss`
  - VLESS
  - VMess
  - Trojan
- Добавлен endpoint:
  - `POST /api/actions/egress-draft-clash-convert-preview`
- В `admin-v2` добавлена кнопка `Convert` для Clash YAML draft.
- UI показывает:
  - какие proxy можно конвертировать;
  - какие proxy пока не поддержаны;
  - какие обязательные поля отсутствуют;
  - redacted sing-box outbound preview.

## Безопасность

- Preview не пишет runtime-файлы.
- Preview не запускает sing-box/xray.
- Preview не меняет routing.
- Preview не меняет kill switch.
- Preview не добавляет канал в pool.
- Секреты в preview заменяются на `[REDACTED]`.

## Дополнительно исправлено

- Исправлен JS-фрагмент `identityProfileFlow`, чтобы админский script проходил syntax-check.
- Проверено, что OpenVPN normalize preview не сломан и продолжает блокировать небезопасные route/script-директивы.

## Проверки

Локально:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
node --check /private/tmp/v7-admin-v2-phase110.js
git diff --check
tests/run-local-checks.sh
```

Unit-smoke:

- Clash YAML с `ss`, `vless`, `hysteria2`.
- Проверено:
  - найдено 3 proxy;
  - 2 proxy convertible;
  - unsupported proxy сохранен как unsupported;
  - пароль и UUID не попали в JSON-ответ.
- OpenVPN preview smoke:
  - route directive блокируется как `BLOCKED`.

## Деплой

После локальных проверок `admin/v7-admin-api` установлен на VPS с backup предыдущего файла и restart `v7-admin-api`.

## Следующий шаг

Сделать выбор одного proxy из Clash YAML и превратить его в отдельный V7-managed sing-box draft:

```text
Clash YAML draft
→ Convert preview
→ operator selects one proxy
→ create V7 proxy draft
→ preflight
→ isolated runtime test
→ quarantine
→ add disabled
```

Это остается staged-flow: рабочие каналы и пользователи не затрагиваются.
