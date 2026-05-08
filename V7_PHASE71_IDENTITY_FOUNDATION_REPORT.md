# V7 Phase 71: Identity Foundation

Дата: 2026-05-08

## Что реализовано

Добавлен первый слой identity/onboarding control-plane поверх существующего V7-core.

Новая база:

```text
/opt/v7/admin/v7-identity.db
```

Таблицы:

- `identity_users`
- `allowed_users`
- `organizations`
- `groups`
- `devices`
- `access_settings`
- `onboarding_attempts`
- `admin_table_settings`

## Важно по архитектуре

`users.registry` остается runtime-файлом V7:

- VPN IP;
- current egress;
- routing table;
- enabled flag.

Новая БД отвечает за людей, организации, whitelist телефонов, устройства и будущий `/connect`.

## Admin API

Добавлены endpoints:

- `GET /api/identity`
- `POST /api/actions/identity-init`
- `POST /api/actions/identity-access-password-set`
- `POST /api/actions/identity-group-upsert`
- `POST /api/actions/identity-organization-upsert`
- `POST /api/actions/identity-allowed-phone-upsert`

## Admin UI

Добавлен раздел:

```text
Identity / Onboarding
```

В нем сейчас:

- статус identity DB;
- connection password status;
- groups;
- organizations;
- allowed phones;
- форма задания connection password;
- быстрые формы добавления группы, организации и телефона.

## Безопасность

- Connection password хранится только как PBKDF2 hash.
- Password hash не возвращается в API.
- Мутирующие identity-действия блокируются Admin Safe Mode.
- Смена connection password не ломает уже выданные VPN-конфиги.

## Следующий шаг

Phase 72:

- `/connect` MVP;
- проверка whitelist phone + connection password;
- создание identity user;
- проверка device limit;
- создание device через существующий `v7-user-create`;
- генерация smart profile;
- выдача через one-time delivery.
