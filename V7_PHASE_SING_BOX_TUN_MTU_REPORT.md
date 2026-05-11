# V7 Sing-Box Tun MTU Hardening

Дата: 2026-05-12

## Зачем

Telegram через V7 начал работать после MSS clamp. Это подтвердило, что проблема была не просто в egress-канале, а в V7 client path:

```text
phone -> wg0 -> V7 -> tun0 -> vless
```

На V7 `tun0` был поднят с MTU `9000`. Для агрегатора с двойным туннелем это риск: TCP можно смягчить MSS clamp, но лучше убрать сам источник риска.

## Что сделано

Добавлен безопасный инструмент:

- `/usr/local/bin/v7-sing-box-tun-mtu-set`

Он:

- делает backup `/etc/sing-box/config.json`;
- меняет только `inbounds[].mtu` у tun inbound `tun0`;
- проверяет временный конфиг через `sing-box check`;
- не печатает секреты;
- restart делает только если `V7_SING_BOX_RESTART=1`.

## Целевое значение

```text
tun0 mtu = 1400
```

MSS clamp `1240` остаётся дополнительной защитой.

## Применение на VPS

Команда применена на новом VPS:

```text
V7_SING_BOX_RESTART=1 v7-sing-box-tun-mtu-set 1400
```

Результат:

```text
V7_SING_BOX_TUN_MTU_SET=OK
backup=/etc/sing-box/config.json.backup.v7-tun-mtu.20260512-020614
interface=tun0
mtu=1400
restart=OK
```

После restart был выполнен `v7-routing-sync`, чтобы восстановить per-user route tables/rules.

## Проверки

```text
sing-box tun inbound: mtu=1400
ip link tun0: mtu 1400
sing-box: active
Telegram через VLESS socks: code=200 total=0.359474s
v7-path-sanity-check: V7_PATH_SANITY=OK
v7-user-desired-state: V7_USER_DESIRED_STATE=OK
v7-system-check: V7_RESULT=OK
```

Также исправлена ложная тревога в `v7-killswitch-check` и `v7-path-sanity-check`: проверки nft-правил больше не используют опасный `nft | grep -q` при `pipefail`, из-за которого существующее правило могло ошибочно считаться отсутствующим.

## Вывод

Тормоза Telegram были связаны с V7 client path, а не обязательно с плохим egress-каналом.

Теперь V7 контролирует этот слой отдельно:

```text
client -> wg0 -> V7 routing -> tun0/awg2/ens3
```

MTU `tun0=1400` + MSS clamp `1240` уменьшают риск зависаний на HTTPS/Telegram/похожих сервисах при двойной туннелизации.
