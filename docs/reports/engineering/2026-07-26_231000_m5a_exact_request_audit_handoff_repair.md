# M5a: repair exact request -> Authority owner handoff

## Причина

Read-only M5a producer корректно формировал short-lived request, но вывод только ID/hash не оставлял существующему Authority owner проверяемого preimage. Повторный producer call неизбежно создавал новый timestamp-bound hash; одобрение нельзя было безопасно перенести на него.

## Исправление

Расширен только существующий append-only `operator-execution-audit` owner:

1. он принимает validated M5a request preimage и сохраняет immutable `current_action_class_contract_request_emitted` record;
2. это не policy write, не contract issuance, не Authority grant и не execution artifact;
3. existing issuer может получить только одну exact unexpired запись по request ID/hash;
4. issuer повторно валидирует hash, TTL, source/incident generation, policy generation, scope, verification, rollback, cooldown, anti-flap и stop conditions под existing policy lock;
5. APPROVE/DECLINE и one-use consumption остаются append-only/exact-once.

Новый registry, planner, queue, Runtime и Authority owner не создавались.

## Проверка

`tests.unit.test_operator_execution_packet` + `tests.unit.test_service_failure_automation_evolution`: `73/73 PASS`.

Новые тесты доказывают request preimage recovery, zero policy write at registration, exact audit issuance and rejection повторного decision.

## Следующая граница

После deploy production owner может зарегистрировать новый fresh request без contract/policy/runtime effect. Только затем exact user approval ID/hash может быть consumed existing Authority issuer. Packet, lease, restore barrier, routing, user movement и rollback остаются вне данного repair и запрещены.
