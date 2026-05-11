# V7 Telegram Double-Tunnel MSS Fix

Дата: 2026-05-12

## Симптом

Telegram через внешний VPN напрямую с телефона работает быстро, но через V7 начинает подключаться медленно.

## Вывод

Проблема находится не во внешнем VPN как таковом, а в дополнительном участке:

```text
phone -> V7 WireGuard -> V7 egress tunnel -> Telegram
```

На V7 было обнаружено:

- `wg0` MTU: 1420;
- `awg2` MTU: 1420;
- `ens3` MTU: 1500;
- `tun0` sing-box MTU: 9000;
- TCP MSS clamp отсутствовал.

Для агрегатора с двойным туннелем это риск подвисаний из-за слишком крупных TCP-сегментов и фрагментации.

## Что сделано

Добавлен и включён MSS clamp:

- `/usr/local/bin/v7-mss-clamp-enable`
- `/etc/systemd/system/v7-mss-clamp.service`

Правила:

```text
wg0 -> tun0  MSS 1240
wg0 -> awg2  MSS 1240
wg0 -> ens3  MSS 1240
```

Сервис включён в systemd и переживает reboot.

## Проверки

```text
v7-mss-clamp.service active (exited)
iptables mangle FORWARD contains TCPMSS --set-mss 1240
v7-system-check: V7_RESULT=OK
```

Активный пользователь `10.0.0.3` сейчас направлен через `vless/tun0`, потому что Telegram через `awg2` показывал таймауты, а через `vless` отвечал быстро.

## Что проверить руками

На телефоне:

1. Закрыть Telegram полностью.
2. Открыть снова через V7.
3. Проверить подключение, загрузку чатов и медиа.

Если проблема останется, следующий слой диагностики:

- проверить UDP/MTProto поведение Telegram через V7;
- сделать service-aware правило `Telegram -> GLOBAL_STABLE/vless`;
- отдельно привести `tun0` MTU sing-box к более нормальному значению после backup и controlled restart.
