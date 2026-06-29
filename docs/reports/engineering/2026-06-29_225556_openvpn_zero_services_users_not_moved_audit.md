# OpenVPN Zero Services / Users Not Moved Audit

Дата: 2026-06-29 22:55:56 +07

## Summary

Проверен вопрос: почему канал `openvpn-1779388847-d2ad7c` может отображаться как плохой по сервисам, но пользователи не переводятся автоматически на другой рабочий канал.

Короткий вывод: в текущей модели V7 плохая пригодность канала как target не равна автоматической эвакуации текущих пользователей. Перевод выполняется только если planner видит безопасный лучший target, проходит State Change Cost / cooldown / freeze / anti-flap / load / service / authority, и есть разрешенная execution authority. Runtime automation сейчас не включена.

## Action Performed

- Проверен существующий owner: `tools/v7-users-autoswitch`.
- Проверены сохраненные production evidence по каналу.
- Выполнена попытка read-only запроса к текущему production admin API.

## Objective Observations

1. Текущий production admin API без активной сессии вернул `unauthorized`, поэтому live UI-состояние не было подтверждено напрямую из этого окружения.
2. Сохраненный evidence `docs/capacity_1/evidence/production_decision_summary.json` показывает для `openvpn-1779388847-d2ad7c`:
   - `channel_state = QUARANTINED`;
   - `safe_now = Нет`;
   - `users = 0`;
   - `soft_limit = 1`;
   - `hard_limit = 2`.
3. Сохраненный evidence `docs/capacity_1/evidence/production_capacity_summary.json` показывает, что канал зарегистрирован как `GLOBAL_FAST`, не `manual_only`, не `reserve_only`, с service tags `google,telegram,instagram,global`.
4. UI evidence показывает канал как `Непригоден / Сбой сервисов` и action `Проверить сервисы`.
5. В `tools/v7-users-autoswitch` candidate pipeline всегда проверяет:
   - basic state;
   - reservation;
   - org policy;
   - quality;
   - service suitability;
   - load;
   - safety.
6. Load gate намеренно не применяется к `purpose="current"`: текущий пользователь может оставаться на текущем канале, даже если этот же канал нельзя выбрать как новый target.
7. Service gate блокирует неизвестные/плохие обязательные сервисы для candidate suitability, но не является самостоятельной командой `evacuate`.
8. Movement происходит только если:
   - current отсутствует или стал неeligible;
   - либо другой candidate существенно лучше текущего;
   - либо есть rebalance condition;
   - cooldown/freeze не блокируют;
   - выбранный target eligible;
   - authority позволяет движение.

## Engineering Conclusions

Если на `openvpn-1779388847-d2ad7c` действительно сейчас сидят пользователи, наиболее вероятные причины, почему V7 их не переводит автоматически:

1. Канал плохой как target, но текущие пользователи не эвакуируются без отдельного failover/rebalance решения.
2. Другой канал должен быть не просто "рабочий", а должен пройти service, quality, load, safety, anti-flap и authority gates.
3. Movement protection специально предпочитает `KEEP CURRENT STATE`, если нет доказанного net benefit выше стоимости смены состояния.
4. Runtime automation не включена, поэтому V7 не имеет права самостоятельно двигать пользователей без разрешенного governed execution path.
5. Если channel/service evidence stale или неполное, V7 должен fail closed / wait for refresh, а не двигать пользователей по сомнительному сигналу.

## Relevant Code Owners

- `tools/v7-users-autoswitch`
  - `_candidate`: общий candidate pipeline.
  - `_gate_service`: сервисная пригодность.
  - `_gate_load`: load/capacity gate.
  - `_beats_current`: минимальный порог улучшения.
  - decision logic: keep/switch/rebalance/failover.

## Key Code Evidence

- `tools/v7-users-autoswitch:5544` builds candidate and runs gates.
- `tools/v7-users-autoswitch:5598` skips load gate for `purpose="current"`.
- `tools/v7-users-autoswitch:5734` applies service suitability gate.
- `tools/v7-users-autoswitch:5944` applies cooldown.
- `tools/v7-users-autoswitch:5954` requires at least `20%` improvement and `50.0` score delta.
- `tools/v7-users-autoswitch:5278` triggers failover only when current is not eligible.
- `tools/v7-users-autoswitch:5319` switches only when best candidate beats current and safety allows.
- `tools/v7-users-autoswitch:5337` otherwise keeps current due stickiness.

## Impact

This behavior protects users from chaotic oscillation. It may look strange in UI because a channel can be shown as bad, but user movement is still blocked until V7 has a safe target and authority to move.

## Capability Progress

Affected capabilities:

- Movement Protection: behavior is consistent with current protection model.
- Runtime Eligibility: target eligibility is enforced.
- Authority Evolution: no autonomous movement is allowed without authority.
- Observability: operator UI may need clearer wording distinguishing "bad target" from "must evacuate now".

## Backlog Progress

No backlog change.

## Production Maturity

No maturity change.

## Canonical Knowledge

Durable knowledge already exists in existing owners:

- Movement Protection Model.
- Runtime Eligibility.
- Production Scale / Work Placement rules.
- OMP authority discipline.

No new owner required.

## Evidence

- Saved evidence: `docs/capacity_1/evidence/production_decision_summary.json`.
- Saved evidence: `docs/capacity_1/evidence/production_capacity_summary.json`.
- Saved UI evidence: `docs/uxc1_polish/screenshots/production_validation.json`.
- Code owner: `tools/v7-users-autoswitch`.
- Live API attempt: `https://v7-admin.195-2-79-116.sslip.io/api/egress` returned `unauthorized`.

## Next Step

Run a read-only current production why-card / autoswitch plan with an authenticated session or existing production owner to identify exact affected users and per-user blocker reasons:

- current channel;
- candidate target;
- blocked target reason;
- service suitability;
- cooldown/freeze;
- state change cost;
- authority state.

If movement is desired after that, prepare a governed operational transaction. Do not move users automatically from this audit.

## Re-audit Rule

Re-audit only if:

- authenticated live production state shows users currently on `openvpn-1779388847-d2ad7c`;
- planner says `keep` without a visible reason;
- target channels are eligible but movement is still not proposed;
- operator explicitly requests a governed movement transaction.

## Verdict

`USERS_NOT_MOVED_BECAUSE_BAD_TARGET_SIGNAL_DOES_NOT_AUTOMATICALLY_AUTHORIZE_EVACUATION`

Need New Owner: FALSE.

Need New Backlog Item: FALSE.

Runtime Behavior Changed: NO.

Users Moved: NO.
