# Block D1 Safety Critical Analysis

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Symptom

`v7-autoswitch-safety-review` returns:

- `status=critical`
- finding: no enabled egress found for active users

## Exact Rule

In `v7-autoswitch-safety-review`, the bounded migration rule computes:

```text
enabled_egress = rows where row["value"] in {"enabled","active","1","true"}
```

The generic `read_registry()` stores:

```text
name = first token
value = second token
```

## Exact Source

Current `egress.registry` rows are KV lines:

```text
id=awg3 protocol=amneziawg type=interface interface=awg3 enabled=1 ...
```

The second token is `protocol=amneziawg`, not the enabled field.

## Evidence

Actual enabled egress count from KV parsing: `7`

Safety-review enabled egress count: `0`

## Classification

Logic/interpretation problem.

Not a real runtime absence of enabled egress.

## Fix

Update safety review registry parsing to use the shared KV parser style and read `enabled=1` from any token.

## Verdict

`safety_root_cause_known=true`

