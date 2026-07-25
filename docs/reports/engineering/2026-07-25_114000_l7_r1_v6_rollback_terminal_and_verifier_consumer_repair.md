Mission ID: `V7_L7_R1_V6_ROLLBACK_TERMINAL_AND_VERIFIER_CONSUMER_REPAIR_V1`
Run Nonce: `V7_L7_R1V6_ROLLBACK_REPAIR_20260725T114000+0700`

# Engineering Report: v6 rollback terminal и repair verifier/evidence consumers

## Production terminal

Fresh v6 request `engauth_r1_837eda5cb8700534622a5d8e` был потреблён ровно один раз. Owner создал Packet `pkt_preview_d2b1e202fa0e65635c1ccb24`, operation `govdry_eeb93084de4b694456919162`, nonce `5f4d5d659ec1f4d0a81a20663eff4f33426ad7d848a4f8a7` и выполнил один failover для certification user `10.7.0.16`.

- forward apply: `true`;
- users moved: `1`;
- rollback attempted: `true`;
- owner terminal: `ROLLBACK_SUCCESS`;
- rollback result: `ROLLBACK_COMPLETED`;
- Learning: `learn_d39d80e1fe2eda98c0294914`;
- cleanup: `CONTROLLED_CERTIFICATION_CLEANUP_COMPLETE`;
- final user route: `10.7.0.16`, table `1014`, `vless/tun0`, PASS;
- controlled source: enabled;
- final Safe Mode: `OPEN`;
- Authority expansion и Production Maturity change: `NONE`.

## Честная evidence-классификация

Existing Outcome Passport owner сформировал `outpass_c981a43ce6f653764caaa3ee`, core/replay/owner consumption присутствуют, но Passport пока `INELIGIBLE_EXACT_GAPS_RECORDED`. Отсутствуют delayed 5m, delayed 1h и steady-state observations.

Дополнительно обнаружены три last-responsible producer→consumer дефекта:

1. controlled verifier scope проверял pre-apply source после уже подтверждённого forward apply и поэтому выдавал `controlled_verifier_user_not_on_source`;
2. approved request `required_services` не переносились в selected move, из-за чего verifier получил `missing target or services`;
3. Passport terminal aggregator позволял более позднему `NO_EXECUTION` read-model row стереть material `ROLLBACK_SUCCESS`.

Failed controlled-condition activation также не должен превращаться в искусственную verifier failure. v6 terminal остаётся реальным owner-recorded rollback, но capability cell не закрывается до repair deploy, fresh consumer replay и due delayed observations.

## Repair

Через существующих owners:

- verifier scope после forward acknowledgement требует approved target, сохраняя immutable original source;
- `required_services` переносятся в Candidate/Packet semantics;
- failed condition activation подавляет induced failure вместо изготовления rollback;
- material terminal `ROLLBACK_SUCCESS` больше не стирается later `NO_EXECUTION`;
- delayed observation consumer поддерживает `ROLLBACK_SUCCESS` и сохраняет terminal semantics.

Focused verification: `424 tests`, PASS. Gate, Authority, max-one-user boundary, rollback decision owner и evidence separation не ослаблены.

## Legal terminal и next output

`R1_V6_ROLLBACK_SUCCESS_RECORDED_CONSUMER_REPAIR_READY_FOR_SAFE_DEPLOY`

Exact next output:

`DEPLOY_CONTROLLED_VERIFIER_AND_EVIDENCE_CONSUMER_REPAIR`
