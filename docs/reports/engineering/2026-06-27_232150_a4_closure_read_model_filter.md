# A4 Closure Read Model Filter

Summary: Исправлен read-only owner A4 closure state: обычная audit/switch история больше не считается незакрытым production outcome.

Action Performed: В `admin_core.autonomy_trust_acceleration.build_decision_outcome_closure` добавлен фильтр closure-candidate records. Closure state теперь строится только по записям с outcome/feedback/verification/rollback/learning семантикой.

Objective Observations:

| Field | Value |
| --- | --- |
| Root cause | `decision_records` смешивал closure records с audit/switch/history записями. |
| Production symptom | `77` valid closures и `8321` non-closure records давали `closure_state=PARTIAL`. |
| Owner reused | `admin_core.autonomy_trust_acceleration` |
| New owner | `NO` |
| New backlog | `NO` |
| Runtime behavior changed | `NO` |
| Users moved | `0` |
| Authority expanded | `NO` |

Engineering Conclusions: A4 was blocked by read-model over-counting, not by missing governed outcomes. Non-closure history remains available as historical evidence, but cannot make outcome closure partial.

Impact: A4 certification validation can now evaluate real closed outcomes without being held by unrelated history records.

Capability Progress: A4 inventory signal is complete; A4 closure validation is ready for production replay after deploy.

Backlog Progress: Tier A remains `3 / 6` until production validation confirms whether A4 can be marked `DONE`.

Production Maturity: Remains `24.0%` until A4 completion is certified.

Canonical Knowledge: No new canonical owner required. Existing certification truth rule preserved.

Evidence:

- `python3 -m unittest tests.unit.test_autonomy_trust_acceleration`
- `python3 -m unittest tests.unit.test_autonomy_trust_acceleration tests.unit.test_governed_canary_cli tests.unit.test_operator_execution_pipeline`

Post-deploy refinement: production replay showed remaining false candidates from identity-only audit records. The filter was tightened so `packet_id`, `operation_id`, `decision_id`, and `object_id` alone do not make a record an outcome closure candidate. Terminal closure records are validated through `outcome_status`, `outcome_quality`, `closure_state`, learning, and observed outcome fields.

Next Step: deploy through existing safe deploy owner, then run production action-class evidence inventory and truth/convergence.

Re-audit Rule: Re-audit only if decision outcome closure sources change or closure records gain a new durable schema.
