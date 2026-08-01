# Engineering Report — live Matrix caller and controlled topology checkpoint

**Дата:** 2026-08-01T08:03:14Z  
**Программа:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Scope:** `ACTIVE_STANDING_TOPOLOGY_AUTHORITY_TO_CONTROLLED_CONDITION_SOURCE_REBIND_BINDING_V1`

## Итог на момент checkpoint

`REBIND_CONTROLLED_CERTIFICATION_SOURCE` уже покрыт действующим standing
contract `sdpc_285af5fc6f4de20415c3e5b1`
(`SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_AVAILABILITY_FIRST_V2`), а не
новой Authority. Contract допускает только один certification identity в
транзакции и один concurrent transaction; ordinary-user effect и
self-expansion запрещены.

Проверен и исправлен producer → consumer link: CPS указывает на
`tools/v7-service-matrix-refresh-all`, а production timer
`v7-service-matrix-refresh.timer` действительно `enabled` и `active`.
`tools/v7-truth-check` теперь снимает этот exact live status read-only, а не
доверяет неполному старому snapshot.

## Текущее production действие

Ничего не запускалось вручную. Existing Matrix timer самостоятельно запустил
bounded topology transaction для `10.7.0.103` (`awg3` → `vless`) с fresh
Candidate/Packet/lease. После его внутреннего topology шага тот же Matrix
cycle автоматически начал availability-first Stage 10 (`vless` → `awg3`).

На момент checkpoint `v7-service-matrix-refresh.service` остаётся active;
его не прерывали и второй transaction не создавали. Окончательный
Outcome/Replay/Learning и CPS reconciliation должны быть прочитаны только
после собственного bounded terminal этого owner.

## Топология и остаток

- `vless`: healthy, certification-only, 44 identities exact campaign group,
  ordinary users = 0; это допустимый controlled source, а не причина ждать
  исторический unhealthy source `1`.
- `awg3` и `amneziawg-exec-20260528-10-8-1-14` дают текущую capacity для
  этапов 5/10.
- Для Stage 25/48 текущий owner пока не доказывает target capacity/isolation:
  это не замаскировано под выполненную certification и не обходится новым
  server/profile/Authority.

## Изменение и проверка

- commit/deploy: `09e19066368611ce813fa1ac844df9e31c4374f6`;
- deploy: только `/usr/local/bin/v7-truth-check`;
- forbidden effects deploy: policy/routing/user movement/restore barrier =
  `false`;
- unit tests: `30` PASS;
- local/GitHub/production commit совпадают;
- `tools/v7-truth-check --all --json`: `PASS`,
  `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`: `PASS`, `ALIGNED`.

## Exact next step

Existing Matrix owner завершает уже начатый Stage 10. Затем existing
Outcome/Replay/Learning/CPS consumers должны атомарно зафиксировать result и
либо перейти к следующему live-admitted stage, либо выдать exact target
capacity/isolation blocker для Stage 25/48. Ни Codex, ни оператор не должны
вручную запускать Matrix или повторять active transaction.
