# Z8.10 Binary And Operation Wiring Forensics

## Hash comparison

| Component | Production hash | Authoritative local hash | Verdict |
| --- | --- | --- | --- |
| `v7-users-autoswitch` | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | `a5480fdfe33c3618aeea345899b98cfad259001576069e9f3721ce01add5d0d3` | MISMATCH |
| `v7-audit-log` | `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86` | `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86` | MATCH |
| `v7-admin-api` | `acbdce035c6f33ad28bd40abb8b76ac1887db9e57f87d696eae98633d760345a` | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` | MISMATCH |

## Operation wiring

Production `/usr/local/bin/v7-users-autoswitch` was searched for the Z7/Z8 markers:

- `operation_id`: not found
- `operation_owner`: not found
- `runtime_operation_terminal`: not found
- `closure_target`: not found

Local `tools/v7-users-autoswitch` contains all four marker families. Therefore production autoswitch is stale relative to the authoritative local branch.

## Verdict

Production binary hash is known, but production binary match is false for autoswitch and admin API.

