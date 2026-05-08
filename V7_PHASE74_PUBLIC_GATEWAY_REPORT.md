# V7 Phase 74: Public Gateway Boundary

Дата: 2026-05-08

## Что реализовано

Добавлен отдельный публичный gateway:

```text
/usr/local/bin/v7-public-gateway
/etc/systemd/system/v7-public-gateway.service
```

Gateway слушает:

```text
0.0.0.0:80
```

И проксирует только user-facing пути на локальную админку:

```text
127.0.0.1:7080
```

## Разрешенные публичные пути

- `GET /connect`
- `POST /connect`
- `HEAD /connect`
- `GET /profile-delivery/<token>`
- `HEAD /profile-delivery/<token>`
- `GET /health`

## Запрещенные публичные пути

Все остальные пути возвращают:

```text
404
```

В частности:

- `/`
- `/login`
- `/api/*`
- `/api/overview`
- `/api/session`

## Проверки на VPS

- `v7-public-gateway.service`: active
- слушает `0.0.0.0:80`
- `http://127.0.0.1/connect`: `200`
- `http://127.0.0.1/api/overview`: `404`
- `http://195.2.79.116/connect`: `200`
- `http://195.2.79.116/api/overview`: `404`
- `http://195.2.79.116:7080/health`: connection refused

## Безопасность

- Полная админка остается local-only на `127.0.0.1:7080`.
- Gateway не пересылает client `Cookie` и `Authorization` на upstream.
- Gateway не возвращает `Set-Cookie` наружу.
- Gateway не публикует `/api/*`.
- systemd service запускается от `nobody:nogroup`.
- Для bind порта 80 выдана только `CAP_NET_BIND_SERVICE`.
- Включены базовые sandbox-настройки systemd.

## Важный результат

Теперь можно давать пользователю ссылку:

```text
http://195.2.79.116/connect
```

При этом админка остается доступной только через SSH tunnel:

```text
ssh -L 7080:127.0.0.1:7080 root@195.2.79.116
http://127.0.0.1:7080/login
```

## Следующий шаг

Phase 75:

- провести controlled real onboarding test для одного тестового пользователя;
- добавить тестовый phone whitelist / organization / connection password;
- пройти `/connect`;
- убедиться, что создан device/peer/config/profile/delivery;
- проверить, что новый пользователь появляется в Identity UI и V7 routing.
