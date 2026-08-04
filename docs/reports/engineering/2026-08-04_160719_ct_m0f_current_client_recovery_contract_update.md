# Engineering Report: CT-M0F current-client recovery contract update

Дата: 2026-08-04T16:07:19Z

## Результат

Существующая программа `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
обновлена до V4.3 без создания нового Program, owner, store, daemon, Planner,
Runtime или Authority-системы.

Устранено противоречие: прежний CT-M0F запрещал любые production effects, но
одновременно должен был доказать реальное ускорение текущего клиентского пути.
CT-M0F теперь является одной Mission с двумя внутренними фазами:

- `CT-M0F-E_ENGINEERING` — reuse/extend существующих owners, реализация,
  тестирование и deploy без routing mutation и user movement;
- `CT-M0F-V_CONTROLLED_VALIDATION` — только после успешной фазы E и только через
  существующий Controlled Production owner, для одной certification identity и
  одной одновременной транзакции.

## Измеряемый completion gate

CT-M0F нельзя закрыть тестами, Polygon evidence или deploy-фактом. Существующий
Time owner должен потребить не менее трёх валидных route-bound samples, включая
один cold и два warm samples:

- `CLIENT_TRAFFIC_RECOVERY_LATENCY` p95 <= 10 000 ms;
- ни один валидный sample > 15 000 ms;
- тяжёлая verification/Outcome/Replay/Learning/closure работа выведена из
  клиентского critical path;
- forward и reset clocks измерены раздельно;
- safety, Authority и ordinary-user guards не ослаблены.

Baseline 141.353447 s сохранён как полный forward-plus-reset lifecycle и больше
не интерпретируется как уже измеренное ускорение или как чистое время отсутствия
трафика.

## Evidence boundary

Контракт не выполнял production transaction, не двигал пользователей, не
создавал Candidate/Packet/lease, не писал restore barrier, не расширял Authority
и не менял Production Maturity. CT-M0F-V не даёт CT-M8/class/L8 credit.

## Текущее состояние и следующий шаг

- `CT-M0F-E_ENGINEERING`: READY;
- `CT-M0F-V_CONTROLLED_VALIDATION`: FORMED_DEPENDENCY_BLOCKED;
- CT-M1: FORMED_DEPENDENCY_BLOCKED до потребления обоих CT-M0F этапов;
- exact next action:
  `V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1`,
  начиная только с `CT-M0F-E_ENGINEERING`.

Terminal этого изменения программы:
`CT_M0F_CURRENT_CLIENT_RECOVERY_COMPLETION_CONTRACT_UPDATED`.
