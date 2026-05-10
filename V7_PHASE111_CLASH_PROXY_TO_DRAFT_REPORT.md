# V7 Phase 111 — Clash Proxy To V7 Draft

Дата: 2026-05-10

## Что сделано

- Добавлен следующий безопасный шаг для Clash YAML:

```text
Clash YAML draft
→ Convert preview
→ выбрать один READY proxy
→ Create Draft
→ новый отдельный V7 draft
```

- Новый endpoint:
  - `POST /api/actions/egress-draft-clash-create-proxy-draft`
- В `admin-v2` в таблице `Clash Converted Proxies` добавлена кнопка `Create Draft` для `READY` proxy.
- Создаваемый child draft хранит sing-box JSON с одним выбранным outbound.
- Child draft получает ссылку на источник:
  - `source_clash_draft_id`
  - `source_proxy_index`
  - `source_proxy_name`
  - `converted_from`

## Безопасность

- Действие требует подтверждение:
  - `CREATE_CLASH_PROXY_DRAFT`
- Новый draft не запускает runtime.
- Новый draft не добавляется в pool.
- Пользователи не переносятся.
- Routing не меняется.
- Kill switch не меняется.
- Реальный секрет хранится только в `config.input` root-only.
- API response секрет не возвращает.

## Проверки

Локально:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
node --check /private/tmp/v7-admin-v2-phase111.js
git diff --check
tests/run-local-checks.sh
```

Unit-smoke:

- Создан временный Clash YAML draft.
- Выполнен convert preview.
- Из первого `ss` proxy создан отдельный child draft.
- Проверено:
  - child protocol = `shadowsocks_or_outline`;
  - child validation = `detected_required_fields`;
  - секрет есть только в root-only `config.input`;
  - секрет не попал в JSON response.

## Следующий шаг

Теперь child draft идет по уже существующей цепочке:

```text
Preflight
→ isolated Runtime
→ Quarantine
→ Add Disabled
→ Runtime Provision
→ Enable Readiness
→ отдельное Enable
```

Следующая разработческая фаза: улучшить runtime/provisioning для sing-box child drafts так, чтобы выбранный proxy из Clash проходил тот же полный lifecycle, что и vless/vmess/trojan/ss ссылки.
