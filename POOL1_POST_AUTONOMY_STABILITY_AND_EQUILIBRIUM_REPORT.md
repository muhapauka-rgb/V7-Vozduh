# POOL.1 POST-AUTONOMY STABILITY AND EQUILIBRIUM REPORT

Дата: 2026-06-13

Проект: V7 Vozduh

Ветка: Updatesystem

Режим: read-only certification.

Итог: `POOL_STABLE`

Пользователи не двигались. `apply` не запускался. Routing, policy, autonomy и deploy не менялись.

## 1. Current Pool Snapshot

Truth gate свежий:

- truth-check: `PASS`
- convergence: `FULLY_ALIGNED`
- runtime_action_safe: `true`
- runtime_action_status: `READY_FOR_RUNTIME_ACTION`

Текущий planner snapshot из BA6 показывает:

- users_total: `26`
- egress_total: `7`
- healthy_egress_total: `3`
- candidate_moves_total: `0`
- selected_moves: `0`
- authority_class: `POOL`
- current_allowed_user_budget: `25`

Текущее распределение:

| Канал | Пользователи | Eligible | Soft limit | Состояние |
|---|---:|---:|---:|---|
| `awg3` | 8 | да | 15 | healthy |
| `wireguard-1779454504-c43409` | 8 | да | 15 | healthy |
| `vless` | 10 | да | 15 | healthy |
| `awg0` | 0 | нет | 15 | `min_mbps_below_floor`, `stability_below_floor` |
| `1` | 0 | нет | 15 | down/fail |
| `amneziawg-exec-20260528-10-8-1-14` | 0 | нет | 15 | manual/reserve/canary/stability block |
| `openvpn-1779388847-d2ad7c` | 0 | нет | 15 | down/fail |

Evidence:

- `POOL1_EVIDENCE/phase1/truth_check_network.json`
- `POOL1_EVIDENCE/phase1/convergence_status_network.json`
- `POOL1_EVIDENCE/phase1/current_pool_snapshot.json`

## 2. Zero Candidate Root Cause

`candidate_moves_total=0` не является техническим blocker.

Причина:

- 26 из 26 пользователей имеют `action=keep`;
- 26 из 26 имеют `move_type=none`;
- recommended distribution совпадает с current distribution;
- нет пользователя, у которого `recommended_egress != current_egress`.

Сводка причин:

- `sticky_keep_current`: 18
- `current_is_best`: 8

Это означает: планировщик видит, что текущие назначения уже достаточно хороши, и не создает искусственные перемещения.

Evidence:

- `POOL1_EVIDENCE/phase2/zero_candidate_user_reasons.json`

## 3. Equilibrium Audit

Классификация: `stable`.

Почему:

- есть 3 healthy eligible канала;
- нагрузка распределена 8/8/10;
- все три рабочих канала ниже soft limit `15`;
- candidate pressure равен нулю;
- snapshot gate в BA6 был чистый: `source_mismatch_families=[]`;
- планировщик не подавлен лимитом: BA6 временно принимал planned limit `25`, но кандидатов все равно было `0`.

Это не похоже на скрытую поломку candidate generation. Это похоже на достижение равновесного состояния после BA3/BA4.

Осторожность: равновесие зависит от того, что `awg3`, `wireguard` и `vless` останутся healthy. Если один из них выпадет, кандидаты снова появятся.

Evidence:

- `POOL1_EVIDENCE/phase3/equilibrium_audit.json`

## 4. Autonomy Impact Timeline

Краткая линия:

| Этап | Итог |
|---|---|
| WireGuard promotion | pool expanded; planner видел до `26` candidates |
| BA1 | 1 пользователь: `vless -> awg3` |
| BA2 | 2 пользователя: `vless -> awg0` |
| BA3 retry | 5 пользователей, WireGuard/awg3 стали рабочими целями |
| BA4 | 10 пользователей на `awg3` и `wireguard` |
| BA6 | `candidate_moves_total=0`; новых движений не требуется |

Вывод: автономные этапы реально изменили распределение. После этого candidate pool исчез не из-за ошибки, а потому что пользователи уже разложены по рабочим каналам.

Evidence:

- `POOL1_EVIDENCE/phase4/autonomy_impact_timeline.json`

## 5. Load Distribution

Рабочая тройка:

- `awg3`: 8/15, headroom 7
- `wireguard-1779454504-c43409`: 8/15, headroom 7
- `vless`: 10/15, headroom 5

Ни один рабочий канал не перегружен по soft limit.

Неиспользуемые каналы сейчас не являются production targets:

- `awg0` блокируется качеством транспорта;
- `openvpn` и `1` имеют fail/down признаки;
- `amneziawg-exec...` не production pool.

Evidence:

- `POOL1_EVIDENCE/phase5/load_distribution_review.json`

## 6. Stability Analysis

Текущий state выглядит устойчивым, но не окончательным “навсегда”.

Ожидание:

- если здоровье `awg3/wireguard/vless` сохранится, planner продолжит оставлять пользователей на местах;
- если один из рабочих каналов деградирует, появятся failover candidates;
- если `awg0` восстановится выше floor, могут появиться новые rebalance candidates, но это требует отдельного channel recovery evidence.

Evidence:

- `POOL1_EVIDENCE/phase6/stability_window_analysis.json`

## 7. Counterfactual Analysis

Если planner rerun now:

- moves: `0`
- причина: current route уже совпадает с recommended route.

Если `awg0` восстановится:

- возможны новые rebalance moves;
- сейчас это не доказано, потому что `awg0` блокируется `min_mbps_below_floor` и `stability_below_floor`.

Если `awg3` “восстановится”:

- это уже произошло: `awg3` eligible и несет 8 пользователей.

Если WireGuard исчезнет:

- pool diversity упадет с 3 до 2;
- 8 пользователей на WireGuard вероятно станут failover candidates.

Evidence:

- `POOL1_EVIDENCE/phase7/counterfactual_analysis.json`

## 8. Pool Health Score

Оценка:

- pool diversity: good;
- channel quality: good для `awg3/wireguard/vless`;
- distribution: good;
- candidate pressure: low;
- autonomy effectiveness: proven by disappearance of real move demand after BA3/BA4;
- residual risk: medium-low, because 4 из 7 каналов сейчас не production-eligible.

Evidence:

- `POOL1_EVIDENCE/final/pool_health_score.json`

## 9. Final Classification

Final classification:

`POOL_STABLE`

Ответ на главный вопрос:

V7 успешно пришла к здоровому operating equilibrium после автономных execution этапов.

Дальнейшее перераспределение сейчас не требуется.

Почему не `POOL_NEEDS_MORE_EXECUTION`:

- нет real planner-selected candidates;
- все пользователи уже на recommended channels;
- текущие рабочие каналы не перегружены.

Почему не `POOL_NEEDS_REBALANCE`:

- load 8/8/10 при soft limit 15;
- rebalance candidates отсутствуют.

Почему не `POOL_NEEDS_RECOVERY`:

- production pool из 3 каналов здоров;
- recovery нужна только для расширения резерва (`awg0` и старые каналы), но не для текущей стабильной работы.

## 10. Recommended Next Stage

Рекомендуемый следующий этап:

`POOL_OBSERVATION_THEN_CHANNEL_RECOVERY`

Практически:

1. Наблюдать pool stability window без перемещений.
2. Отдельно заняться recovery для `awg0` как резервного production capacity.
3. Не запускать 25-user autonomy, пока `candidate_moves_total < 25`.
4. Hybrid batch sizing можно проектировать как runtime model, но не как повод двигать пользователей без реальной planner demand.

Final verdict:

`POOL_STABLE`

Final flags:

- pool_stable=true
- equilibrium_reached=true
- further_redistribution_required=false
- candidate_moves_total=0
- selected_moves=0
- users_moved=0
- apply_executed=false
- routing_changed=false
- policy_changed=false
- autonomy_changed=false
- next_stage=`POOL_OBSERVATION_THEN_CHANNEL_RECOVERY`

