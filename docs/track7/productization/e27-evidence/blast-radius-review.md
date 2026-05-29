# E27 Blast Radius Review

## Modeled Action

```text
10.7.0.11: 1 -> amneziawg-exec-20260528-10-8-1-14
10.7.0.12: 1 -> amneziawg-exec-20260528-10-8-1-14
```

## Expected Blast Radius

`blast_radius=2`

Allowed users would be exactly:

```json
["10.7.0.11", "10.7.0.12"]
```

Allowed target would be exactly:

```json
["amneziawg-exec-20260528-10-8-1-14"]
```

## Isolation Model

Only route tables `1009` and `1010` should change during forward movement. Rollback should restore both to `v7e356a192b79`.

All other users must remain unchanged, including:

```text
10.7.0.14
10.7.0.15
10.7.0.16
```

## Verdict

`blast_radius_model_complete=true`

`blast_radius_bounded_to_two_users=true`

`execution_allowed_now=false`

The model is complete, but execution readiness is blocked by target capacity `hard_limit=1`.

