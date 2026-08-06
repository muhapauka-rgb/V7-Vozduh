# CT-M0F: one-generation validation admission producer и fresh request

Дата: `2026-08-06T06:30:09Z`

## Итог

Закрыт producer gap между CT-M0F Runtime consumer и существующим независимым
Authority audit. Широкий Tier-48 campaign request не переиспользован: он
разрешал бы лишние стадии и subscopes.

Существующий `admin_core.operator_execution` owner расширен узким профилем
`CT_M0F_ONE_GENERATION_KERNEL_CUTOVER_VALIDATION`. Он связывает текущую
standing policy, certification pool/registry fingerprints, один source,
`max_users=1`, `max_concurrent_transactions=1`, cold/warm kind, expiry и
one-use law. До независимого решения запрещены Candidate, Packet, lease,
controlled condition, apply и движение пользователя.

## Проверка и deploy

- focused request tests: `3 PASS`;
- полный `tests.unit.test_operator_execution_packet`: `82 PASS`;
- соседние substrate/request tests: `3 PASS`;
- широкий affected-suite остановлен после непропорционально долгого повторного
  AST-сканирования; failure не наблюдался, assertions не ослаблялись;
- commit: `feb0b862d0d090ae63ece5dd1b1749b1679e4792`;
- push: `Updatesystem`;
- deploy: только через `tools/v7-safe-deploy`, post-manifest `PASS`,
  `deployment_required=false`;
- production non-test producer: `PASS`.

## Fresh owner-backed request

- request_id: `ctm0fauth_r1_cda5955e978cc52c22477670`;
- request_hash: `cda5955e978cc52c22477670e616d719c81ef72691984e17ab7652df6e4960ca`;
- validation_generation_id: `ctm0fgen_df9d4f73470a1a64d5a02d16`;
- created_at: `2026-08-06T06:30:09.824288+00:00`;
- expires_at: `2026-08-06T06:45:09.824288+00:00`;
- source: `vless`;
- sample_kind: `cold`;
- max_users: `1`;
- max_concurrent_transactions: `1`;
- registration: `REGISTERED`.

Production effects:

- audit_write: `true`;
- policy_write: `false`;
- Candidate/Packet/lease: `false`;
- runtime_apply/routing_mutation/user_movement: `false/false/0`;
- Authority expansion: `false`;
- Production Maturity change: `false`;
- L7/L8 credit: `false`.

## Legal terminal

`ENGINEERING_AUTHORITY_CT_M0F_CONTROLLED_VALIDATION_DECISION_REQUIRED`.

Exact next consumer is the existing independent Authority owner. Approval is
one-use and does not itself execute. After approval the existing Matrix/
governed consumer must revalidate all live gates and create fresh
Candidate/Packet/lease for this generation. Decline or expiry returns to CPS
residual reconciliation without effects.
