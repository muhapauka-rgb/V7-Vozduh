# V7 Auth/AI Stability Check

Дата: 2026-05-12

## Почему проверяли

Пользователь заметил: при прямом подключении к внешнему WireGuard ChatGPT и Google identification работают нормально, а через V7 иногда могли сбоить.

После фикса Telegram стало ясно, что такие проблемы надо разделять:

```text
egress работает сам по себе
```

и

```text
client -> wg0 -> V7 -> egress работает как полный путь
```

## Текущая проверка

На VPS проверены:

- `v7-path-sanity-check`
- `v7-system-check`
- route_get для активных пользователей
- OpenAI/Google endpoints через:
  - direct `ens3`;
  - `vless` через socks `127.0.0.1:1080`;
  - `awg2` через interface.

Результат на момент проверки:

```text
V7_PATH_SANITY=OK
V7_RESULT=OK

chatgpt.com через vless: reachable
auth.openai.com через vless: reachable
accounts.google.com через vless: 204
www.google.com через vless: 204

chatgpt.com через awg2: reachable
auth.openai.com через awg2: reachable
accounts.google.com через awg2: 204
www.google.com через awg2: 204
```

`403` на OpenAI/ChatGPT в curl считается reachability OK для этой проверки: это ответ сервиса/edge, а не таймаут TCP/TLS.

После расширения матрицы выполнен `v7-service-matrix-refresh-all`:

```text
V7_SERVICE_MATRIX_REFRESH=OK
checked=2
ok=2
warn=0
fail=0

vless chatgpt: OK first_byte=0.698s
vless google_auth: OK first_byte=0.522s
vless openai_auth: OK first_byte=0.777s

awg2 chatgpt: OK first_byte=0.126s
awg2 google_auth: OK first_byte=0.190s
awg2 openai_auth: OK first_byte=0.162s
```

Оба egress работают, но для auth/AI на момент проверки `awg2` быстрее и выглядит более стабильным кандидатом.

## Что усилено

Расширен service matrix:

- `google_auth` -> `https://accounts.google.com/generate_204`
- `chatgpt` -> `https://chatgpt.com/`
- `openai_auth` -> `https://auth.openai.com/`

Теперь регулярный `v7-service-matrix-refresh.timer` будет проверять не только YouTube/Telegram/Google, но и auth/AI endpoints.

## Реальный риск

Даже при OK по TCP/TLS браузерная авторизация может иногда сбоить из-за:

- QUIC/UDP 443 через двойной туннель;
- смены egress-IP между попытками входа;
- чувствительности Google/OpenAI к IP reputation;
- старого MTU/MSS дрейфа, который теперь закрыт;
- временного дрейфа V7 policy/routing, который теперь чинит `v7-path-guard-repair`.

## Вывод

На момент проверки V7 не режет ChatGPT/Google TCP/TLS.

Чтобы исключать повторение, auth/AI endpoints добавлены в регулярную матрицу. Если снова будет сбой именно в браузере/приложении, следующий безопасный шаг:

1. проверить, через какой egress идёт конкретный пользователь;
2. сравнить `google_auth/chatgpt/openai_auth` по `vless` и `awg2`;
3. если проблема повторяется только на `vless`, закрепить auth/AI route class за более стабильным `awg2` или включить управляемый TCP-first режим для auth/AI.
