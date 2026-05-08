# V7 Identity and User Onboarding Plan

Дата: 2026-05-08

## Цель

Добавить в V7 слой авторизации пользователей, onboarding и управления устройствами перед выдачей VPN-конфига.

Это не заменяет текущий V7-core. Новый слой должен работать поверх существующих компонентов:

- `users.registry` остается runtime-реестром VPN peer/IP/table.
- `v7-user-create` остается безопасным provisioning-командным слоем.
- smart profiles и one-time delivery используются для выдачи профиля.
- route policy/groups связываются с уже существующей service-aware маршрутизацией.

## Главная модель

```text
Person / identity user
  phone, name, organization, group, status, max_devices
        |
        v
Device / VPN peer
  device_name, public_key, assigned_vpn_ip, table, config, client_app
        |
        v
V7 runtime
  users.registry + wg0 peer + route table + smart client profile
```

## Этап 1: Identity Foundation

- SQLite база: `/opt/v7/admin/v7-identity.db`
- Таблицы:
  - `identity_users`
  - `allowed_users`
  - `organizations`
  - `groups`
  - `devices`
  - `access_settings`
  - `onboarding_attempts`
  - `admin_table_settings`
- Нормализация телефонов.
- Хранение connection password только как PBKDF2 hash.
- Admin API для:
  - просмотра identity state;
  - добавления allowed phone;
  - добавления организации;
  - добавления группы;
  - смены connection password.

## Этап 2: Admin UI

- Раздел Identity / Onboarding в админке.
- Allowed Phones.
- Organizations.
- Groups.
- Access Password.
- Users/Devices summary.

## Этап 3: `/connect` MVP

- Public-safe страница `/connect`.
- Пользователь вводит:
  - имя;
  - телефон;
  - организацию;
  - пароль подключения.
- Проверки:
  - телефон есть в active whitelist;
  - пароль подключения совпадает;
  - пользователь не blocked/disabled;
  - лимит устройств не превышен;
  - организация найдена.
- После успеха:
  - создать/обновить identity user;
  - создать device через `v7-user-create`;
  - сгенерировать smart profile;
  - создать one-time delivery link.

## Этап 4: Devices and Limits

- Один device = один VPN peer/config.
- `max_devices` по умолчанию 3.
- Уменьшение лимита не удаляет существующие устройства.
- Новые устройства запрещаются при превышении лимита.
- Revoked device должен отключаться на WireGuard/V7 runtime уровне.

## Этап 5: Import/Export

- CSV/TXT сначала.
- XLSX/VCF позже.
- Preview перед сохранением.
- Deduplication по `phone_normalized`.
- Экспорт whitelist.

## Этап 6: Hardening

- Rate limit по IP/телефону.
- Onboarding attempts log.
- Temporary lockout.
- Device revoke audit.
- Table settings.
- External `/connect` and `/profile-delivery/<token>` через reverse proxy, но без внешнего доступа к `/api/*` и полной админке.

## Правила безопасности

- Не печатать private keys/profile contents в чат.
- Не хранить connection password открытым текстом.
- Не ломать существующие выданные конфиги при смене connection password.
- Не удалять устройства автоматически при изменении лимитов.
- Не открывать всю админку наружу.
