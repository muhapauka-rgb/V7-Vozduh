# Engineering Report: A3 Non-Material Snapshot Gate Apply Fix

## Summary

Исправлен существующий `tools/v7-users-autoswitch` owner для A3: approved locked selected move больше не подавляется на apply-пути, если snapshot gate не доказал material state change.

## Action Performed

- Расследован fail-closed результат A3 после approved packet `pkt_preview_5c4bcfaa59d769ced6d6e5dc`.
- Найдено, что `approved_plan_lock` был валиден и содержал selected move, но snapshot gate обнулял `selected_moves` при `snapshot_gate_material_change=false`.
- Расширен существующий autoswitch owner: на `--apply` пути non-material source mismatch теперь сохраняет approved selected move.
- Read-only readiness dry-run оставлен консервативным.

## Objective Observations

- До фикса: `selected_moves_before_restore_barrier=1`, `selected_moves_after_gate=0`.
- Причина отказа: `approved_plan_lock_snapshot_gate_stop_required`.
- Material state change: `false`.
- Approved plan lock: present, valid, consumed.

## Engineering Conclusions

Старое поведение смешивало non-material source mismatch с material unsafe state. Это правильно останавливало движение, но неправильно блокировало уже approved locked apply, когда пользователь, target, rollback target, authority generation и selected move hash не изменились.

## Impact

- Не создан новый planner.
- Не создан новый governance.
- Не создан новый execution owner.
- Не создан новый truth source.
- Runtime automation не включалась.
- Пользователи не двигались во время фикса.

## Capability Progress

- Movement Protection: прогресс не сертифицирован до реального A3 outcome.
- Rollback: ожидает реальный rollback/no-rollback outcome.
- Learning: ожидает реальное observed outcome.
- Authority Evolution: ожидает корректный governed execution path.

## Backlog Progress

- A3 остается `IN_PROGRESS`.
- A3 еще не `DONE`, потому что реальное production movement/outcome не завершено.

## Production Maturity

Production Maturity не повышалась: фиксация кода сама по себе не является production outcome certification.

## Canonical Knowledge

Durable knowledge: non-material snapshot/source mismatch must not invalidate an approved apply path when material state is unchanged. Read-only readiness remains conservative.

## Evidence

- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy` -> `OK`, 81 tests.
- `PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch` -> pass.

## Next Step

Deploy the tested fix through the existing safe deployment owner, then rerun the A3 governed canary flow. If the packet is still current and authority is required, stop at `OPERATIONAL_AUTHORITY`; if apply succeeds, verify immediately and close the real outcome.

## Re-audit Rule

Do not re-audit this behavior unless planner snapshot gate semantics, execution lease semantics, approved plan lock semantics, or production evidence changes materially.
