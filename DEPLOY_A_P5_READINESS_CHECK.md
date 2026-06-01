# DEPLOY A P5 Readiness Check

## Required P5 Runtime Truth

The server can now provide fresh runtime truth directly from:

`/opt/v7/egress/state`

Available values:

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`
- admin health: `OK`

## Boundary

P5 was not rerun.

No runtime action was executed.

## Verdicts

- p5_runtime_truth_available=true
- safe_to_rerun_p5=true
- p5_rerun_performed=false
- runtime_action_executed=false
