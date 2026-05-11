# V7 Direct RU Autosync

Дата: 2026-05-12

## Что сделано

Добавлен фоновый механизм, который держит серверный direct-RU runtime в актуальном состоянии.

Цель простая: если RU-сайт после клиентского фильтра всё-таки попал на V7, V7 выпускает его напрямую через российский серверный интерфейс, а не через внешний VPN-egress.

## Файлы

- `/usr/local/bin/v7-direct-auto-sync`
- `/etc/systemd/system/v7-direct-autosync.service`
- `/etc/systemd/system/v7-direct-autosync.timer`

## Логика

- базовые suffix-правила `.ru` и `.xn--p1ai` добавляются в `/etc/v7/direct/domains.conf`;
- домены из `/etc/v7/policy/direct_ru_domains.conf` синхронизируются в runtime direct-list;
- при изменениях пересобирается `/etc/dnsmasq.d/v7-direct.conf`;
- `dnsmasq` перезапускается только если были изменения;
- состояние пишется в `/opt/v7/egress/state/direct-ru-autosync.state`;
- timer запускает sync каждые 10 минут.

## Проверки на VPS

Контрольный прогон:

```text
V7_DIRECT_AUTOSYNC=OK
changed=0
dnsmasq=active
checked_count=6
ok_count=6
stale_count=0
failed_count=0
sample_1=gosuslugi.ru OK
sample_2=yandex.ru OK
sample_3=vk.com OK
sample_4=lamoda.ru OK
sample_5=sberbank.ru OK
sample_6=tinkoff.ru OK
```

`v7-system-check`:

```text
V7_RESULT=OK
```

Timer:

```text
v7-direct-autosync.timer active
```

## Важно

Это не заменяет клиентский bypass. Правильная основная схема остаётся такой:

- RU-сайты по возможности обходят V7 прямо на устройстве клиента;
- если RU-трафик всё-таки пришёл на V7, сервер выпускает его напрямую через РФ-интерфейс;
- остальной трафик продолжает идти через выбранный egress.
