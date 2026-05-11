# V7 Service Matrix Monitor

Дата: 2026-05-12

## Зачем

После проблемы с Telegram стало понятно, что общий speed/health egress не всегда показывает реальную пригодность канала для конкретного сервиса.

Пример:

- внешний канал может быть быстрым в обычном тесте;
- YouTube и Google могут открываться;
- но Telegram или WhatsApp на этом же канале могут виснуть.

Поэтому добавлен лёгкий фоновый контроль сервисов.

## Что добавлено

- `/usr/local/bin/v7-service-matrix-refresh-all`
- `/etc/systemd/system/v7-service-matrix-refresh.service`
- `/etc/systemd/system/v7-service-matrix-refresh.timer`

Таймер запускается каждые 15 минут и проверяет включённые egress-каналы через существующий `v7-service-matrix-test`.

Проверяемые сервисы сейчас:

- YouTube
- Telegram
- WhatsApp
- Google
- Apple
- Cloudflare

## Что не меняется

Мониторинг:

- не переключает пользователей;
- не меняет маршруты;
- не меняет firewall;
- не перезапускает туннели.

Он только обновляет state:

- `/opt/v7/egress/state/service-matrix.json`
- `/opt/v7/egress/state/service-matrix-refresh.state`

## Текущий результат

```text
vless: OK
awg2: WARN
```

`vless`:

- YouTube OK
- Telegram OK
- WhatsApp OK
- Google OK
- Apple OK
- Cloudflare OK

`awg2`:

- YouTube OK
- Google OK
- Apple OK
- Cloudflare OK
- Telegram timeout
- WhatsApp timeout в одном из прогонов

## Вывод

Похожая проблема найдена: `awg2` сейчас не является хорошим каналом для мессенджеров.

Для активного телефона `10.0.0.3` уже выбран `vless`, поэтому Telegram работает хорошо.

## Следующий правильный шаг

Сделать service-aware правило:

```text
Telegram / WhatsApp / messaging -> лучший стабильный канал
```

То есть не обязательно переключать всего пользователя на другой egress. В будущем V7 должен сам выбирать канал по типу сервиса:

- RU-сайты -> direct РФ;
- Telegram/WhatsApp -> стабильный канал;
- YouTube/video -> быстрый канал;
- остальной трафик -> sticky user default.
