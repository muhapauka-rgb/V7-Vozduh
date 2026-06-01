# P5R Runtime Audit

Project: V7 Vozduh

Block: P5 RETRY

## Fresh Runtime Hashes

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves source: `missing_treated_as_empty`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`

## Health

- local admin health: `OK`
- public admin health: `OK`
- admin local-only: true
- admin auth configured: true

## Capacity

- capacity source: `/opt/v7/egress/state/egress-load-summary.json`
- capacity source hash before action: `2f016adb487c9a95c6cc76424d4609dd1c013757638369d07001fdbb8bd1092b`
- capacity summary status: `ok`
- active users: `18`
- total channels: `7`
- healthy channels: `2`
- working channels: `1`
- reserve channels: `1`

## Trust

- trusted RU decision state exists: true
- trusted RU decision hash: `4767b2302304ef3990ef08726754ac6817d613ab57af619bb81067e8ca861f9d`
- trusted RU diagnostic state exists: true
- trusted RU diagnostic hash: `3a394645a8c8a674b84dc0de7e17d983af9f634f821cc03d0ca97fe9bcff650e`

## Routing And Autoswitch Baseline

- route table hash: `04b2279db976810ff7aaada7908dddc1d48c1aeaa7dfea371252798a434ccfe2`
- ip rule hash: `e8902acd1be10b6f7df14c23f557136a8453ba5b8520393d63b4a689334354ff`
- autoswitch timer: `inactive`

## Audit Stores Before Action

- audit store: `/opt/v7/audit/operator-execution-audit.jsonl`
- audit records before: `0`
- governance store: `/opt/v7/audit/operator-runtime-governance-actions.jsonl`
- governance records before: `0`

## Verdict

- runtime_audit_complete=true
- selected_moves_zero=true
- health_ok=true
- capacity_ok=true
- trust_sources_present=true
