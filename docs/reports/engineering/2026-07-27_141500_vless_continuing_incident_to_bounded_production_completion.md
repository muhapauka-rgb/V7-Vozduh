# VLESS: от непрерывного incident к bounded production completion

Дата: 2026-07-27

## Итог

`PASS / FULLY_ALIGNED`. Реальный VLESS service-failure incident был вновь
наблюдён, дошёл до bounded delegated execution и завершился одной production
транзакцией. Пользователь `10.0.0.2` переведён с `vless` на
`wireguard-1779454504-c43409`; post-action verification `PASS`, rollback не
требовался.

## Реальная причинная цепочка

`SERVICE_FAILURE_REVALIDATED sfrev_6f9263b9885fd96cad86d0eb9bbc758f`
(`source_incident_id sfinc_be20296fba3d8a6a33e58a583f1b58db`)
→ passive consumer `PASS`
→ advisory `PASS`
→ OMP consumer `PASS`
→ fresh Candidate/Packet/lease
→ existing standing delegated policy admission `PASS`
→ bounded apply: `users_moved=1`
→ verification `PASS`
→ rollback `NOT_REQUIRED`
→ post-action OMP consumer `PASS`.

Ни Authority expansion, ни Production Maturity change не выполнялись.

## Устранённые реальные разрывы

1. `SERVICE_FAILURE_REVALIDATED` имел отдельную семантику Matrix и не
   принимался bounded-admission owner.
2. Повторная нормализация теряла canonical `object` (VLESS).
3. Общий tail-limit вытеснял VLESS-событие шумными событиями другого канала.
   Existing bounded reader теперь сохраняет последнее событие каждого
   `(event_type, affected channel)` без нового хранилища.
4. Runtime authority-budget gate ожидал устаревший one-use contract и не
   распознавал уже действующий owner-issued standing policy. Его per-action
   scope по-прежнему проверяет fresh executor; standing policy не стала
   неограниченным Packet grant.

## Изменения и проверка

- `257967c`: initial Matrix revalidation adapter.
- `18d8a665`: preserved normalized source binding.
- `44d0bdc8`: bounded per-channel event coverage.
- `6e057867`: standing-policy runtime gate binding.
- Focused regression suite: 239 tests `PASS`.
- Каждый production deploy выполнен только через `tools/v7-safe-deploy` с
  manifest `PASS` и без запрещённых effects до вызова штатного caller.
- Итог: local/GitHub/runtime на `6e057867`; `tools/v7-truth-check --all` =
  `PASS`, convergence = `FULLY_ALIGNED`.

## Точный current terminal

Данная bounded transaction завершена и потреблена. Future work не может
переиспользовать её Event, Candidate, Packet, lease или standing-policy
decision как одноразовое доказательство. Следующий OMP frontier выбирается
только из fresh CPS/owner-backed residual после очередного реального события
или independent safe product successor.
