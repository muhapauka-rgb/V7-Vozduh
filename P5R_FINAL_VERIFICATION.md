# P5R Final Verification

Project: V7 Vozduh

Block: P5 RETRY

## Final Runtime State

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected move count: `0`
- selected move hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`
- route table hash: `04b2279db976810ff7aaada7908dddc1d48c1aeaa7dfea371252798a434ccfe2`
- ip rule hash: `e8902acd1be10b6f7df14c23f557136a8453ba5b8520393d63b4a689334354ff`
- autoswitch timer: `inactive`
- local admin health: `OK`

## Final Audit Stores

- audit records: `8`
- audit store hash: `166e36646a85450d3c14af9b91ade7df4541bffcf6b3aae7ef9f4877daa0ab0c`
- governance records: `1`
- governance store hash: `493e6f1ed6b3881f0f36b902f266499475d5877b46c8e22bc03979d66b5c231d`

## Required Verdicts

- packet_created=true
- approval_valid=true
- runtime_recheck_passed=true
- action_executed=true
- governance_record_appended=true
- audit_record_appended=true
- users_unchanged=true
- routing_unchanged=true
- autoswitch_unchanged=true
- runtime_state_preserved=true
- replay_protection_verified=true
- rollback_preview_verified=true
- first_runtime_action_successful=true

## Safety Verdict

- users_moved=false
- routing_changed=false
- autoswitch_apply_run=false
- deploy_performed=false
- rollback_executed=false
- scope_expanded=false

Only `ZERO_MOVE_GOVERNANCE_STATE_TRANSITION` executed.
