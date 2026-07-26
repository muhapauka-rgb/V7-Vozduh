# Отчёт: Auto-safe OMP continuation и heartbeat

Дата: 2026-07-26

## Результат

Существующий `CODEX_AUTOMATION_PLATFORM` heartbeat обновлён для текущего V7
task. Он запускается каждые пять минут и привязан к актуальному task
`019f651d-542b-7c53-9a6c-504648e692ee`.

Каждый wake сначала читает свежие CPS и Program, затем вызывает существующий
OMP heartbeat/re-entry owner. При существовании safe successor он продолжает
полный existing-owner цикл без ручного сообщения `продолжай`: repair, tests,
commit/push, проверенный safe deploy, production caller/consumer verification,
replay/Learning, truth/convergence, CPS/OMP/report projection и перерасчёт
остатка.

## Safety contract

Heartbeat не получает новой Authority и не является Runtime. Он не проходит
через независимые boundaries: `ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY`,
restore-barrier write, Packet execution, routing/user mutation, rollback,
Authority/Production Maturity change, external owner/access input и Natural L8.
На такой границе он может только собрать owner-backed read-only request и
зафиксировать re-entry condition.

Для предотвращения бесконечного цикла установлено правило: три wake без
owner-backed progress переводят одинаковый successor в exact blocker terminal
без churn. Existing exact-once lease, duplicate suppression и fresh CPS
revalidation остаются обязательными.

## Изменённый canonical contract

В `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md` добавлен раздел
`Auto-safe continuation execution policy`. Он явно определяет, что обрыв
соединения, завершение ответа или context compaction не являются Program
terminal и требуют watchdog re-entry, когда доступен safe successor.

## Ограничение

Документ и heartbeat устраняют необходимость вручную нажимать «продолжить» для
инженерной работы. Они не превращают предыдущую общую авторизацию в bypass
fresh owner-issued one-use contracts: production-impacting действие всё равно
исполняется только при всех актуальных owner gates.
