# E35.0.1 Channel Selection Code Audit

## Scope

Audit question: where is channel selection implemented today.

## Primary Selection Path

selection_logic_audited=true

The primary real user/channel movement selector is `tools/v7-users-autoswitch`.

It loads:

- `users.registry`
- `egress.registry`
- `v7-state.json`
- `egress-speed.json`
- `client-speed.json`
- `service-matrix.json`
- `service-preferences.json`
- `egress-quality-summary.json`
- `telegram-sentinel.json`
- `autoswitch-safety.json`
- `/etc/v7/policy.json`
- `/etc/v7/org-egress-policy.json`
- restore barrier state

Admin exposes this through:

- `GET /api/autoswitch-plan`
- `POST /api/actions/autoswitch-dry-run`
- `POST /api/actions/autoswitch-apply-guarded`

The admin action eventually calls `v7-users-autoswitch --mode guarded --apply --pretty`, but no such action was executed in this audit.

## Primary Algorithm Shape

For each active user:

1. Load important services.
2. Infer route class from services.
3. Build candidates for all egress channels.
4. Apply hard gates.
5. If still eligible, compute score.
6. Compare best candidate with current channel.
7. Choose one of:
   - keep
   - failover
   - planned switch
   - reconnect rotation
   - rebalance
8. Select bounded moves by move type and projected capacity.

The core functions are:

- `_decision_for_user()`
- `_candidate()`
- `_gate_basic()`
- `_gate_reservation()`
- `_gate_org()`
- `_gate_quality()`
- `_gate_service()`
- `_gate_load()`
- `_gate_safety()`
- `_score_parts()`
- `_select_moves()`

## Secondary Selection / Suitability Path

There is a separate route-class/service-aware selector in `admin/v7-admin-api`:

- `service_aware_route_dry_run()`
- `egress_candidate_score()`
- `service_aware_apply_preview()`
- `service_aware_apply_guarded()`

This path selects route-class egress for policy routes, not direct per-user movement. It scores enabled egress by health, role, service matrix fitness, Telegram state, tags, priority, weight, and speed.

## Proposal Path

Proposal generation is in `generated_proposals()` and `service_recommendations()`.

This path is non-authoritative. It can recommend or observe, but it does not move users.

## Audit Verdict

where_channel_selection_is_implemented=tools/v7-users-autoswitch
service_aware_route_selection_exists=true
proposal_selection_exists=true
proposal_selection_is_authoritative=false

## Notes

Current "channel selection" is not one single function. There are three related layers:

- autoswitch movement planner: actual movement selection
- service-aware route-class selector: route class target selection
- proposal generator: operator-facing recommendation
