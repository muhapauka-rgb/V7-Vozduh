# P6 Runtime Audit

Project: V7 Vozduh

Block: P6

## Fresh Hashes Before Movement

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`

## Health And Capacity

- admin health before movement: `OK`
- autoswitch timer before movement: `inactive`
- target users before movement: `0`
- capacity acceptable: true

## Trust

Trusted RU state was present. The approved movement is not a trusted/direct route-class movement.

## Baselines

- candidate current before: `1`
- candidate table: `1009`
- route table before: `default dev v7e356a192b79 scope link`
- users outside candidate hash: `864fa66d68514f0c958bff07c33b8780da201f635446714bf4475d80947acc59`
- routes outside scope hash: `637ec5536b408883788a5a79c7b6ba2afb7cb8f196416e508112d2aca177e5f3`
- ip rule hash: `7a24985200ad990402f479e8bb613e126efe9efa60c0bb1bb978492c27a998a7`

## Verdict

- runtime_audit_complete=true
- selected_moves_zero=true
- admin_health_ok=true
- capacity_acceptable=true
