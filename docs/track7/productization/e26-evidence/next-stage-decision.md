# E26 Next Stage Decision

`recommended_next_block=E27_TWO_USER_GOVERNED_MOVEMENT_PREPARATION`

## Options Reviewed

| Option | Decision | Reason |
|---|---:|---|
| `E27_TWO_USER_GOVERNED_MOVEMENT_PREPARATION` | Selected | Natural next scale step after a certified one-user movement. It preserves bounded blast radius while testing multi-user packet semantics and rollback. |
| `E27_LARGER_COHORT_GOVERNANCE_PREPARATION` | Not selected | Cohort movement is too large a jump from one-user proof. |
| `E27_RUNTIME_REPO_CONVERGENCE_AND_RELEASE_PROVENANCE` | Not selected as next block | Useful productization track, but not the next governance capability proof. It can run in parallel or after two-user preparation. |

## Required E27 Preparation Themes

- Select exactly two low-risk users.
- Use the same execution-only target model only if capacity permits.
- Define per-user rollback.
- Enforce movement budget `2`.
- Prove no third user can move.
- Keep autoswitch apply forbidden.
- Keep execution-time recheck mandatory.
- Keep replay denial mandatory.

