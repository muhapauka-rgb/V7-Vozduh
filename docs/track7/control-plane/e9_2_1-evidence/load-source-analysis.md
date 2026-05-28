# E9.2.1 Load Source Analysis

Mode: static/read-only analysis.

## `v7-egress-load`

Repo source: `tools/runtime-support/v7-egress-load`.

Relevant behavior:

```text
USERS_REG="${STATE_DIR}/users.registry"
OUT="${STATE_DIR}/egress-load.state"
count=$(grep -c "current=${id}" "$USERS_REG" 2>/dev/null || true)
echo "${id}_users=${count}" >> "$TMP"
```

Conclusion:

- `egress-load.state` counts `users.registry` rows matching `current=<egress-id>`.
- It does not read route tables, desired state, reconnect state, or historical assignments for the count.
- It writes static per-egress limits from `V7_LOAD_SOFT_LIMIT` / `V7_LOAD_HARD_LIMIT`, currently observed as `1` and `2`.
- Therefore `1_users=1` in `egress-load.state` means at least one current users.registry row contains `current=1`.

## `v7-users-autoswitch`

Repo source: `tools/v7-users-autoswitch`.

Relevant behavior:

```text
self.users = self._load_users()
self.egress = self._load_egress()
self._sync_egress_user_counts()
self.dynamic_load = self._dynamic_load_summary()
```

`_load_users()` reads `state.users` from `v7-state.json` if present, otherwise parses `users.registry`.

`_sync_egress_user_counts()` sets `egress.users` by counting enabled users by `user.current`.

`_persist_dynamic_load_summary()` writes `egress-load-summary.json` with `source=v7-users-autoswitch` and `authority=capacity_signal`.

Conclusion:

- `egress-load-summary.json` is planner-derived, but it still counts active user current assignments.
- It can use `v7-state.json` as its source, which itself is generated from state files and `users.registry`.
- In the observed E9.2.1 state, both static load and planner summary agree that target `1` has one user.

## `v7-state-json`

Repo source: `tools/runtime-support/v7-state-json`.

Relevant behavior:

- emits egress `users` from summary state fields such as `${id}_users`;
- emits users directly from `users.registry`;
- includes desired-state rows from `user-desired-state.state`.

Conclusion:

- state JSON can propagate load-state into planner inputs;
- it does not create the `10.7.0.5 current=1` assignment by itself.

## Answered Questions

| Question | Answer |
|---|---|
| Where does `1_users=1` come from? | Current registry assignment: `10.7.0.5 current=1`. |
| Does it count `users.registry`? | Yes. `v7-egress-load` counts `current=<id>` in `users.registry`; autoswitch sync also counts active users by current egress. |
| Does it count desired state? | Desired state mirrors the registry/route reality here; it is not needed to explain the count. |
| Does it count historical/current route table? | Static `v7-egress-load` does not. Runtime route table independently confirms the assignment. |
| Does it count reconnect state? | Not for the observed load count. |
| Does it count last assignment? | Assignment file matches registry for `10.7.0.5`; no stale-only source is needed. |
| Does it include disabled users? | Current evidence points to enabled users only for autoswitch; `v7-egress-load` grep is textual and would count disabled `current=1` rows if present, but no disabled `current=1` row was observed. |
| Does it include stale post-canary target? | No. The counted user is `10.7.0.5`, not first canary user `10.7.0.15`. |
| Does it round/estimate capacity differently? | Yes. `egress-load.state` uses static soft/hard `1/2`; dynamic summary reports soft/hard `19/24` and target status `OK`. |

## Source Analysis Verdict

The target-1 load signal is real current assignment/load, not a stale E9 canary artifact and not a calculator bug.
