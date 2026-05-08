# V7 Phase 73: Identity Admin Users and Devices

Дата: 2026-05-08

## Что реализовано

Расширен раздел админки:

```text
Identity / Onboarding
```

Теперь он показывает:

- identity users;
- devices;
- allowed phones;
- organizations;
- groups;
- access password status.

## Users

В таблице identity users видно:

- status;
- name;
- phone;
- organization;
- group;
- devices `active / max`;
- actions.

Добавлены действия:

- изменить `max_devices`;
- block user;
- unblock user;
- открыть профиль identity user.

Если новый `max_devices` меньше текущего количества активных устройств, API требует явное подтверждение:

```text
LOWER_DEVICE_LIMIT
```

Существующие устройства при этом не удаляются автоматически.

## Devices

В таблице devices видно:

- status;
- device name;
- user;
- VPN IP;
- route table;
- VPN client;
- created time.

Добавлен controlled revoke:

1. `identity-device-revoke-preview`
2. `identity-device-revoke-apply`

Runtime-отзыв устройства использует существующую команду:

```text
v7-user-disable <ip>
```

Это важно: админка не дублирует WireGuard/V7 логику, а вызывает уже проверенный lifecycle script.

## Admin API

Добавлены endpoints:

- `POST /api/actions/identity-user-update`
- `POST /api/actions/identity-device-revoke-preview`
- `POST /api/actions/identity-device-revoke-apply`

## Безопасность

- Mutating actions требуют admin role.
- Apply revoke требует подтверждение:

```text
REVOKE_DEVICE
```

- Admin Safe Mode блокирует apply revoke и user update.
- Preview revoke не меняет runtime.
- Apply revoke делает backup через существующий `v7-user-disable`.

## Следующий шаг

Phase 74:

- подготовить public reverse proxy boundary:
  - наружу только `/connect`;
  - наружу только `/profile-delivery/<token>`;
  - `/api/*`, `/`, `/login` остаются local-only / через SSH tunnel;
- после этого можно тестировать реальный onboarding для одного тестового пользователя.
