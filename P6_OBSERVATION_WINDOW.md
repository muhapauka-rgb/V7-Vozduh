# P6 Observation Window

Project: V7 Vozduh

Block: P6

## Before

- candidate current: `1`
- target users: `0`
- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- route table `1009`: `default dev v7e356a192b79 scope link`
- audit count: `8`
- switch history count: `2738`

## After

- candidate current: `amneziawg-exec-20260528-10-8-1-14`
- target users: `1`
- users registry hash: `256c20b85442caea1de7bd7501b95c22bd39f2ee7eb92241c304458d2f76afcc`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- route table `1009`: `default dev v7execwg0 scope link`
- audit count after forward audit: `9`
- switch history count: `2739`

## Delayed / Final

- candidate remained on target: true
- target users: `1`
- route table `1009`: `default dev v7execwg0 scope link`
- selected moves count: `0`
- admin health: `OK`
- autoswitch timer: `inactive`
- final audit count: `12`
- final switch history count: `2739`

## Outside Scope

- users outside candidate hash before: `864fa66d68514f0c958bff07c33b8780da201f635446714bf4475d80947acc59`
- users outside candidate hash after: `864fa66d68514f0c958bff07c33b8780da201f635446714bf4475d80947acc59`
- routes outside scope hash before: `637ec5536b408883788a5a79c7b6ba2afb7cb8f196416e508112d2aca177e5f3`
- routes outside scope hash after: `637ec5536b408883788a5a79c7b6ba2afb7cb8f196416e508112d2aca177e5f3`
- ip rule hash before: `7a24985200ad990402f479e8bb613e126efe9efa60c0bb1bb978492c27a998a7`
- ip rule hash after: `7a24985200ad990402f479e8bb613e126efe9efa60c0bb1bb978492c27a998a7`

## Checkers

- `v7-user-route-check`: `OK`
- `v7-killswitch-check`: `OK`
- `v7-provisioning-reconcile-check`: `OK`

## Verdict

- observation_completed=true
- users_outside_scope_untouched=true
- routing_changed_outside_scope=false
- selected_moves_unchanged=true
