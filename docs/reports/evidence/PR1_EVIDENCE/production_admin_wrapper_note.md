# Production admin wrapper note

During PR.1 a read-only request to `/api/autoswitch-plan` was executed through the admin API.

The response returned `rc=0`, `action=autoswitch_plan`, and textual command output, but `plan` was `null` in the wrapper. Because that wrapper output is not a reliable machine-readable plan artifact, PR.1 detailed tables use the already captured valid production JSON samples:

- `docs/reports/evidence/CTR_FINAL_EVIDENCE/dry_runs/production_dry_run_01.json`
- `docs/reports/evidence/CTR_FINAL_EVIDENCE/production_observation_window.json`
- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/production_autoswitch_plan.json`

No apply was executed.
No users were moved.
No routing was changed.
