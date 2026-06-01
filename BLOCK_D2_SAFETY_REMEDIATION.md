# Block D2 Safety Remediation

Date: 2026-06-01

## Change

Updated `tools/v7-autoswitch-safety-review` to parse both:

- current KV registry rows, for example `id=awg0 enabled=1`
- legacy two-column rows, for example `awg0 enabled`

## Behavior After Fix

- Egress identity resolves from `id`, then `ip`, then legacy `name`.
- Enabled state resolves from `enabled`, then legacy `value`, then `state`.
- Truthy enabled values: `enabled`, `active`, `1`, `true`, `yes`, `on`.
- Parse errors remain fail-closed and excluded from active/enabled counts.

## Tests

Added `tests/unit/test_v7_autoswitch_safety_review.py`.

Covered:

- KV registry enabled egress detection.
- Active user counting from KV registry rows.
- Legacy two-column compatibility.
- No false critical finding when enabled egress exists.

## Runtime Certification

The fixed tool was executed against live state without deployment:

- `status=ok`
- `enabled_egress=7`
- `users=18`
- `critical=0`

## Verdict

safety_parser_fixed=true

