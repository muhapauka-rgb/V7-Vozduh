# N10 — ускорение критического пути и исправление учёта контрольного опыта

Дата: 2026-08-24 19:25 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Блок: N10 — измерение реального пути `failure → Matrix → decision → Packet → lease → apply → verification`

## Краткий итог

В этом блоке подготовлен и развёрнут новый вариант критического пути. Он не меняет обычных клиентов и не включает переключение в production для реальных пользователей. Polygon использует одного выделенного synthetic-клиента `10.7.0.92`.

Сделаны три оптимизации:

1. Matrix передаёт Planner уже подтверждённую цепочку Authority вместо повторного чтения и распаковки старой истории.
2. Между Planner и route-writer повторная проверка управляющего файла заменена на проверку его SHA-256 и точных полей; при любой неполноте или изменении файла остаётся прежний fail-closed валидатор.
3. Для точного клиентского доказательства выбран быстрый UDP STUN-запрос внутри namespace клиента. HTTPS-проверка сохранена как fail-closed fallback.

Отдельно исправлен обнаруженный разрыв: новая бронь контрольного опыта создавалась после загрузки Planner и не была видна его уже загруженному списку. Теперь именно строка, возвращённая существующим Authority-owner после append/fsync, добавляется в тот же in-process Planner. Само правило проверки не ослаблено.

## Что было до изменений

Последний валидный baseline был снят на прежнем fingerprint:

| Показатель | Значение |
|---|---:|
| Полное переключение одного Polygon-клиента | 4920,353 ms |
| До решения | 3273,761 ms |
| Запись назначения | 959,244 ms |
| Видимость маршрута | 30,361 ms |
| Проверка клиентского payload | 639,828 ms |
| Подготовка Matrix | 157,955 ms |
| Выбор Matrix | 51,928 ms после предыдущего исправления |

Целевой барьер N10: не менее пяти валидных опытов, минимум один cold и два warm, минимум две owner-backed generation, один implementation fingerprint, p95 total не выше 3000 ms, ни одного опыта выше 5000 ms.

## Изменения

### 1. Reuse уже подтверждённой Authority lineage

Изменены существующие владельцы:

- `tools/v7-service-matrix-refresh-all` передаёт Matrix lineage в существующий Planner;
- `tools/v7-governed-canary-dry-run-cycle` принимает и переносит эту lineage в in-process Planner;
- `tools/v7-users-autoswitch` не сбрасывает подтверждённую immutable lineage в уже связанном exact Packet.

Новый owner, очередь, registry, источник истины или параллельное состояние не добавлялись.

### 2. Fail-closed fast path для execution control

`tools/runtime-support/v7-user-switch` теперь может пропустить третий Python-import только когда одновременно подтверждены:

- SHA-256 управляющего файла совпадает с хэшем, переданным Planner;
- состояние файла `CLOSED`;
- scope — `operation`;
- совпадают generation, operation id, action class, move hash, source/snapshot bundle hashes;
- `max_users == 1`.

Если `jq`, хэш или любое поле отсутствуют/изменились, запускается прежний валидатор и операция останавливается при отказе.

### 3. Быстрое точное доказательство клиента

В existing client-speed owner добавлен `STUN_XOR_MAPPED_ADDRESS` для exact namespace клиента. Ответ проверяется по типу, cookie, transaction id, длине, адресу и хэшу payload. При сбое STUN разрешён только установленный HTTPS fallback; это не превращает ошибку в положительный результат.

### 4. Исправление reservation → validation

После создания `ct_m0f_standing_validation_sample_reserved` существующим Authority-owner его hash-bearing record теперь добавляется в cache уже созданного Planner. Повторная запись не дублируется. Неполная запись без `record_hash` игнорируется, поэтому validation по-прежнему fail-closed.

## Проверки

- До исправления reservation: **421 unit-тест пройден**.
- После исправления reservation: **352 unit-теста пройдено**.
- `bash -n` для shell owner — PASS.
- AST/syntax-проверка изменённых Python owners — PASS.
- `git diff --check` — PASS.
- Safe-deploy allowlist — PASS, blockers: 0.
- GitHub branch `Updatesystem` выровнена.
- Production `v7-health.service`: `active`, MainPID `3717685`, Nice `0`.
- Production hashes после последнего deploy совпадают с локальными для ключевых owners:
  - `v7-governed-canary-dry-run-cycle`: `1adda45aaa2fb81a81c2775b36c164eb2e606dcc45d26e9c748ab4bbbde5096b`;
  - `v7-users-autoswitch`: `b0fde85db18628d4c801470ac0861c9885dbbabfefa3a9c930540c311b4c3b2e`.

## Реальный Polygon-опыт

Первый холодный опыт нового fingerprint был намеренно проведён на выделенном клиенте `10.7.0.92`. Источник: `amneziawg-exec-20260528-10-8-1-14`, target: `awg0`, reservation: `ctm0fsample_13ff6ac4d7092f48c003f452`.

Маршрут клиента фактически оказался на `awg0`, но опыт **не засчитан**. Existing consumer правильно выдал:

`CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID`

Причина: `ct_m0f_standing_sample_reservation_missing_or_duplicate`. В момент validation Planner видел старый список Authority lineage и не видел только что записанную бронь. Это не было принято за успех и не было превращено в измерение latency.

Опыт закрыт штатным terminal:

`CT_M0F_STANDING_SAMPLE_SAFELY_RECONCILED_INVALID`

Обычные клиенты не менялись. Источник снова включён, Matrix и health-owner оставлены рабочими. После закрытия исходный .92 остаётся на `awg0`, что является безопасным baseline для следующего governed Polygon-цикла.

## Коммиты и deploy

- `3ccf9068` — supporting Authority proof on live recovery path;
- `b7bff7d3` — три ускорения критического пути;
- `e67e7e6e` — передача exact sample reservation в reused Planner.

Оба последних коммита опубликованы в `Updatesystem` и прошли штатный `tools/v7-safe-deploy`; production truth — `PASS`.

## Ограничения и текущий статус

Новый latency пока не объявляется доказанным: первый опыт после ускорений отклонён как недоказанный, а не как valid sample. Поэтому N10 не закрыт и общий прогресс остаётся `99,99999997%`.

Отдельный production Matrix timer остаётся выключенным по ранее принятому решению. Текущий официальный health-owner — `v7-health.service`; обычные маршруты и клиенты не затрагивались.

## Следующий точный шаг

Повторить cold Polygon-цикл на новом implementation fingerprint после последнего deploy, убедиться, что reservation и forward evidence видны одному Planner, и получить первый valid sample. Затем последовательно собрать пять valid samples (cold/warm, минимум две generation) и проверить SLO N10. Только после этого закрыть N10 и перейти к availability-first closure и N11 residue cleanup.

