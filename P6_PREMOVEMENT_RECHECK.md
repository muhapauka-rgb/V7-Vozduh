# P6 Pre-Movement Recheck

Project: V7 Vozduh

Block: P6

## Recheck Immediately Before Movement

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`
- candidate current: `1`
- candidate table: `1009`
- target users: `0`
- route table `1009`: `default dev v7e356a192b79 scope link`

## Movement Preview

Read-only preview:

- mutation: false
- runtime_commands_executed: false
- errors: `[]`
- warnings: `[]`
- blast_radius: `one_user`
- target_interface: `v7execwg0`
- route would change: `ip route replace default dev v7execwg0 table 1009`
- ip rules would change: `[]`

## Verdict

- runtime_recheck_passed=true
- hashes_unchanged=true
- selected_moves_unchanged=true
- target_still_go=true
- candidate_unchanged=true
