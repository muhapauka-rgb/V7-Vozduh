# E11.9 Drain Strategy Matrix

Drain model selected: `sequential_manual_bounded_drain_with_apply_timer_held`.

Destination selected for every approved user: target `1`, interface `v7e356a192b79`.

| user | table | from | to | expected route diff | rollback path | risk |
|---|---:|---|---|---|---|---|
| `10.7.0.4` | `1002` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.4 wireguard-1779454504-c43409` | low |
| `10.7.0.6` | `1004` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.6 wireguard-1779454504-c43409` | low |
| `10.7.0.8` | `1006` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.8 wireguard-1779454504-c43409` | low |
| `10.7.0.9` | `1007` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.9 wireguard-1779454504-c43409` | low |
| `10.7.0.10` | `1008` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.10 wireguard-1779454504-c43409` | low |
| `10.7.0.11` | `1009` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.11 wireguard-1779454504-c43409` | low |
| `10.7.0.12` | `1010` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.12 wireguard-1779454504-c43409` | low |
| `10.7.0.13` | `1011` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.13 wireguard-1779454504-c43409` | low |
| `10.7.0.14` | `1012` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.14 wireguard-1779454504-c43409` | low |
| `10.7.0.15` | `1013` | `wireguard-1779454504-c43409` | `1` | default dev `v7e06a394c478` -> `v7e356a192b79` | `v7-user-switch 10.7.0.15 wireguard-1779454504-c43409` | low |

## Model Comparison

| model | decision |
|---|---|
| sequential manual bounded drain | selected; most deterministic, route verified after every user |
| planner-assisted drain | rejected; planner intentionally holds current reserved users pending separate drain approval |
| temporary target quarantine | rejected; E11.8 reservation is already the production-assignment block |
| staged mini-batch drain | rejected; no benefit over sequential verification for only 10 users |
| wait-for-natural-drain | rejected; reservation target would remain occupied indefinitely |
| hybrid | rejected; extra moving parts without better safety |

## Safety Notes

- Apply timer was held only during the sequential drain window to prevent concurrent timer-driven movement.
- Planner/health remained available for read-only state and post-drain verification.
- Apply timer was restored only after post-drain dry-run showed `selected_moves=0`.
