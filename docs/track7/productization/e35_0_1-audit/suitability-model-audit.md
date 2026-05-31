# E35.0.1 Suitability Model Audit

## Scope

Audit question: what makes a channel suitable, and what completely disqualifies it.

## Candidate Gate Order

suitability_model_audited=true

Autoswitch candidate suitability is built in `_candidate()`:

1. `_gate_basic`
2. `_gate_reservation`
3. `_gate_org`
4. `_gate_quality`
5. `_gate_service`
6. `_gate_load`
7. `_gate_safety`
8. `_score_parts` only if still eligible

This means hard gates execute before scoring. A faster channel cannot win if a hard gate has made it ineligible.

## Hard Suitability Criteria

A channel can be hard-blocked by:

- disabled egress
- state `maintenance`, `disabled`, or `quarantine`
- `manual_only`
- non-200 health code
- diagnose severity outside `OK`/`WARN`
- static-mode hard full
- reserve-only for planned movement
- canary reserved target unless it is the user's current channel
- group allowlist mismatch
- group exclusion
- exclusive group mismatch
- egress group ACL mismatch
- exclusive isolation conflict
- average Mbps below policy floor
- minimum Mbps below policy floor
- stability below policy floor
- trusted-RU route class without trusted RU metadata
- Telegram hard-blocked when required
- route class fitness `FAIL`
- multiple critical service failures
- persistent service failure
- planned hard capacity full
- failover hard capacity full
- egress safety quarantine
- egress failed verification limit
- target blocked for user
- pair reversal stability window

## Soft Suitability Criteria

Soft criteria do not necessarily block selection. They affect reasons and score:

- Telegram degraded
- one non-persistent non-Telegram service failure
- route class fitness `WARN`
- quality history fail rate advisory
- group preferred egress
- reserve-only penalty when not hard-blocked for the move type
- priority
- weight
- speed
- stability score
- quality trend
- load score
- latency score
- sticky current channel bonus

## Fallback Criteria

Fallback behavior:

- If current channel is eligible and no candidate beats it by score threshold, keep current.
- If current channel is not eligible, attempt failover to best eligible failover candidate.
- If service-only failure happens during restore stage without approval, failover can be suppressed.
- If no eligible failover target exists, no movement is selected.

## Audit Verdict

hard_gates_before_score=true
speed_can_override_hard_gate=false
current_channel_has_sticky_bias=true
fallback_is_keep_or_fail_closed=true
