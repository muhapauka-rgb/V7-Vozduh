# E35.0 Channel Suitability Audit

## Scope

Audit question: what happens today if Telegram, Google Auth, YouTube, Instagram, ChatGPT, Claude, or another required service is unavailable on a channel.

## Service Matrix

service_matrix_exists=true

`service_matrix_state()` reads `SERVICE_MATRIX_FILE` and normalizes per-channel service rows.

Each channel row receives:

- `services`
- `ok_count`
- `total`
- `status`: `OK`, `WARN`, `FAIL`, `UNKNOWN`
- `route_class_fitness`

## Route Class Fitness

`service_matrix_route_fitness()` maps service results to route classes. It handles:

- missing services
- failed services
- Telegram hard down
- Telegram degraded
- OK/WARN/FAIL/UNKNOWN status

Telegram hard-down is treated specially:

- `telegram_status_is_hard()`
- `service_matrix_telegram_state()`
- hard down can make route fitness FAIL.

Telegram degraded is not the same as hard down. It produces WARN-style semantics.

## Proposal Effects

If user-required services fail on current egress and another egress satisfies them, generated proposals can recommend review/movement.

If no egress satisfies required services, generated proposals produce observation requiring operator review rather than movement.

## Routing Effects

service_aware_route_dry_run_exists=true
service_aware_apply_preview_exists=true
service_aware_apply_guarded_exists=true

Service-aware route flows exist, but they are explicit admin actions and guarded/prechecked. This audit did not find that required service failure globally blocks all user movement paths yet.

## Audit Verdict

channel_suitability_audit_complete=true
service_matrix_drives_suitability=true
telegram_hard_down_special_case=true
service_failure_can_create_proposal=true
global_hard_gate_for_required_services=false

## E35 Implication

E35 should define a single operator-visible suitability verdict per channel/user pair:

- suitable
- degraded
- blocked
- unknown

and define exactly which verdict blocks proposals, packets, and execution-time recheck.
