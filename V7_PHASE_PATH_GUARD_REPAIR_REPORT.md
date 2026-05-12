# V7 Path Guard Repair

Дата: 2026-05-12

## Зачем

V7 может выглядеть для пользователя как "режет трафик", если живые сетевые правила отличаются от желаемого состояния.

Это не логика блокировки сайтов. Это технический дрейф в слоях:

```text
client -> wg0 -> V7 policy routing -> tun0/awg2/ens3 -> internet
```

Критичные примеры:

- после restart интерфейса пропал `ip rule` пользователя;
- после rebuild firewall пропали DNS-capture правила;
- пропал MSS clamp и TCP начинает зависать на двойном туннеле;
- отключился `net.ipv4.ip_forward`;
- kill-switch потерял allow/drop правила.

## Что добавлено

Добавлен safe repair guard:

- `/usr/local/bin/v7-path-guard-repair`
- `/etc/systemd/system/v7-path-guard-repair.service`
- `/etc/systemd/system/v7-path-guard-repair.timer`

Он сначала запускает `v7-path-sanity-check`, а затем чинит только безопасные и однозначные случаи:

| Проблема | Автоматическое действие |
| --- | --- |
| `ip_forward=FAIL` | `sysctl -w net.ipv4.ip_forward=1` |
| MSS clamp missing | `v7-mss-clamp-enable` |
| user policy routes failed | `v7-routing-sync` |
| DNS-capture / kill-switch rules missing | `v7-killswitch-enable`, затем `v7-direct-auto-sync` |

## Что не чинится автоматически

`tun0` MTU repair через restart sing-box не включён по умолчанию, потому что restart может коротко оборвать активные пользовательские сессии.

Если когда-нибудь потребуется разрешить это guard-у:

```text
V7_PATH_GUARD_FIX_MTU=1 v7-path-guard-repair --apply
```

Сейчас MTU уже закреплён в `/etc/sing-box/config.json`, поэтому штатно это не нужно.

## Почему это безопасно

- guard не переключает пользователей между каналами;
- guard не запускает rebalance;
- guard не меняет egress assignment;
- guard не трогает секреты;
- guard пишет состояние в `/opt/v7/egress/state/v7-path-guard-repair.state`;
- guard использует lock, чтобы два ремонта не шли одновременно.

## Проверки

```text
v7-path-guard-repair --dry-run
systemctl enable --now v7-path-guard-repair.timer
systemctl start v7-path-guard-repair.service
systemctl status v7-path-guard-repair.timer
cat /opt/v7/egress/state/v7-path-guard-repair.state
v7-path-sanity-check
v7-killswitch-check
v7-system-check
```

Ожидаемый итог:

```text
V7_PATH_GUARD_REPAIR=OK
V7_PATH_SANITY=OK
V7_KILLSWITCH_CHECK=OK
V7_RESULT=OK
```

## Фактический деплой

На VPS guard установлен и включён:

```text
systemctl enable --now v7-path-guard-repair.timer
systemctl start v7-path-guard-repair.service
```

Фактический результат:

```text
V7_PATH_GUARD_REPAIR=OK
mode=apply
before=OK
after=OK
actions=0
failures=0

V7_PATH_SANITY=OK
V7_KILLSWITCH_CHECK=OK
V7_RESULT=OK
```

Текущий guard ничего не менял, потому что V7 уже был в правильном состоянии. Теперь если безопасная часть пути выпадет, guard восстановит её сам.
