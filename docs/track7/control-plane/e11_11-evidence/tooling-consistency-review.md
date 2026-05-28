# E11.11 Tooling Consistency Review

tooling_review_completed=true

## Evidence Inputs

- `full-governance-snapshot.txt`
- `current-state/`
- `current-autoswitch-plan.pretty.json`
- `current-target-readiness.txt`
- `current-restore-settle-gate.txt`
- `default-target-readiness-after-fix.txt`
- `default-restore-settle-after-fix.txt`

## Stale-Tooling Risks Found

| Risk | Evidence | Operational impact | False result risk | Fix |
|---|---|---|---|---|
| Target readiness defaulted to old E9 candidate/state | Pre-fix default behavior pointed at historical `10.7.0.14/vless` fixture path | Operator could see NO-GO after live E11.10 closeout was clean | False negative | Default candidate/current now `10.7.0.3/awg0`; default state search now prefers E11.11 current state, then E11.10, then historical fixtures |
| Target readiness ignored `egress-quality-summary.json` | Live runtime state has quality JSON but no `egress-stability.state` | Clean live target looked low-quality because metrics were `None` | False negative | Readiness checker now flattens `egress-quality-summary.json` when token stability state is absent |
| Target readiness required `interface-state.state` even when diagnose was OK | Live runtime did not expose `interface-state.state`; diagnose had `OK` and fresh WireGuard handshake | Clean target looked unknown-interface | False negative | Readiness checker now infers interface UP from diagnose `OK` with `handshake_age_seconds=` and emits warning |
| Restore-settle default searched old E9 evidence first | Default `tools/v7-restore-settle-gate --pre-restore` could classify historical NO-GO | Operator could confuse historical delayed-movement evidence with current E11.10/E11.11 settle | False negative | Default state search now prefers E11.11 settle samples, then E11.10 closeout, then historical E9 |
| Operator habit used unsupported live flags | Live snapshot attempted `v7-users-autoswitch --dry-run --json`; runtime help shows default is read-only without `--apply` | Snapshot parser failed even though timer journal and local plan showed selected moves zero | Evidence collection false negative | Evidence now uses `v7-users-autoswitch --pretty` locally on copied live state; docs call out no `--dry-run` flag |
| Operator habit used positional `v7-egress-diagnose <id>` | Live `v7-egress-diagnose` is whole-state writer with `--state-dir/--output`, not a positional query | Could be mistaken for diagnose failure | Evidence collection false negative | Treat diagnose state file as source of truth; do not use positional diagnose calls |

## Post-Fix Tooling Truth

`tools/v7-second-canary-target-readiness --pretty` now returns:

- `candidate_user=10.7.0.3`
- `current_egress=awg0`
- `selected_target=wireguard-1779454504-c43409`
- `approval_status=GO`
- `execution_allowed_now=False`

`tools/v7-restore-settle-gate --pre-restore --pretty` now returns:

- `gate_status=GO`
- `selected_moves_by_sample=[0, 0, 0]`
- `registry_stable=True`
- `hidden_movers_observed=False`
- `execution_allowed_now=False`

## Remaining Stale Risk

stale_tooling_risks_remaining=LOW_DOC_OPERATOR_RISK_ONLY

The remaining risk is operator misuse of live runtime tools with old flags or positional arguments. Repo defaults and E11.11 evidence now point at current state, but production operator runbooks must keep documenting that autoswitch is read-only unless `--apply` is present and diagnose is whole-state oriented.
