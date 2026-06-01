# P6.A Runtime Audit

Project: V7 Vozduh

Block: P6.A

## Runtime Source

- runtime truth source: `/opt/v7/egress/state`
- users registry: present
- egress registry: present
- selected moves source: `missing_treated_as_empty`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`

## Registry Hashes

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`

## Health

- admin health: `OK`
- autoswitch timer: `inactive`

## Capacity

Capacity source: `/opt/v7/egress/state/egress-load-summary.json`

- capacity operator status: `ok`
- active users: `18`
- total channels: `7`
- healthy channels: `2`
- working channels: `1`
- destination candidate users: `0`

## Trust

- trusted RU decision exists: true
- trusted RU decision overall: `NEEDS_ATTENTION`
- trusted RU diagnostic exists: true

The first movement design excludes `TRUSTED_RU_SENSITIVE` and `DIRECT_RU` route classes and uses a normal user currently on `1`, not a trusted/direct special route.

## Runtime Facts A Movement Must Trust

A future movement certification must trust only fresh values for:

- users registry row for the candidate
- candidate route table
- destination egress registry row
- destination interface
- destination capacity and quality
- selected moves count/hash
- autoswitch safety state
- route table/rule snapshot
- user-route/killswitch/provisioning checker results
- approval TTL and packet hash

## Verdict

- runtime_audit_complete=true
- selected_moves_zero=true
- capacity_ok=true
- movement_runtime_truth_available=true
