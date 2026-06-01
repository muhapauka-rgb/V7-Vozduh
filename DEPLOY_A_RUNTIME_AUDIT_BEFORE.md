# DEPLOY A Runtime Audit Before

## Runtime State

- runtime state path: `/opt/v7/egress/state`
- users registry exists: true
- egress registry exists: true
- admin health before: `OK`

## Before Hashes

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- v7-state hash: `1f17855874f1184cce6e7dbdd76a466811ea546fd0ac72fe519e02fb22d32cf9`
- summary.state hash: `42317b0b50ae690adb045841719c5340d3e839ea8979a873ef337101efd40df8`
- egress-status.state hash: `b7e08f752d40a217c54cd247f1c91dfede231bd8e16e0299c12136a717380091`

## Selected Moves

- selected moves source: `missing_treated_as_empty`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`

## Routing Baseline

- ip rule digest: `7a24985200ad990402f479e8bb613e126efe9efa60c0bb1bb978492c27a998a7`
- ip route table-all digest: `45f16703587a3b07cdb7e6cbbbd423830683979fc3c5ec78e65a8d450f5a3bc9`

## Verdicts

- runtime_audit_before_complete=true
- runtime_state_missing=false
- selected_moves_count=0
- admin_health_before_ok=true
