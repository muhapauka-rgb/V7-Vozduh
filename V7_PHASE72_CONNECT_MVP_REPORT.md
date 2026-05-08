# V7 Phase 72: `/connect` MVP

Дата: 2026-05-08

## Что реализовано

Добавлена пользовательская страница:

```text
/connect
```

Назначение: web-onboarding перед выдачей VPN-профиля.

Пользователь вводит:

- имя;
- телефон;
- организацию;
- пароль подключения;
- клиентское приложение.

## Логика проверки

Перед созданием VPN device сервер проверяет:

- identity DB инициализирована;
- телефон нормализуется;
- телефон есть в active whitelist;
- connection password совпадает с PBKDF2 hash;
- организация существует;
- организация совпадает с whitelist, если телефон привязан к конкретной организации;
- пользователь не `blocked` / `disabled`;
- лимит активных устройств не превышен;
- нет rate-limit по повторным ошибкам.

## Provisioning

После успешной проверки:

1. Создается или обновляется `identity_user`.
2. Выполняется preflight:
   - `v7-user-create <device> --egress <default> --dry-run`
3. Создается реальный VPN peer/device:
   - `v7-user-create <device> --egress <default>`
4. Генерируется smart profile:
   - `v7-smart-client-profile-generate --adapter karing --mode RU_LOCAL`
5. Проверяется профиль:
   - `sing-box check -c <profile>`
6. Создается one-time delivery link.
7. В identity DB записывается device.

## Безопасность

- `/connect` не требует входа в админку, но не открывает `/api/*`.
- При включенном Admin Safe Mode `/connect` блокирует создание устройства.
- Connection password не хранится открытым текстом.
- Ошибочные попытки пишутся в `onboarding_attempts`.
- Добавлен базовый rate limit: слишком много ошибок по телефону/IP временно блокирует попытки.
- Ответ не печатает private key/profile contents.

## Что пока не реализовано

- Импорт allowed phones из файлов.
- Пользовательский выбор между несколькими режимами профиля.
- OTP/SMS/Telegram подтверждение владения телефоном.
- Отзыв device из identity UI с отключением WG peer.
- Настраиваемая таблица identity users.

## Следующий шаг

Phase 73:

- улучшить Identity Admin UI:
  - список users/devices;
  - inline max_devices;
  - фильтры;
- профиль пользователя;
- revoke device preview/apply;
- затем подготовить безопасный reverse proxy, который наружу публикует только `/connect` и `/profile-delivery/<token>`.
