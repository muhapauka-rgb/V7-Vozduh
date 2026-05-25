# Quiet Window Verification

This checklist defines how to verify a future quiet-window rehearsal. It was not executed in Block E6.

## Before Hold

Verify:

- current autoswitch timer/service active/enabled state;
- Telegram sentinel timer/service active/enabled state;
- no currently running `v7-user-switch`;
- no currently running `v7-routing-sync`;
- current `users.registry` hash;
- current `ip -4 rule show`;
- current `ip -4 route show table all`;
- current switch-history tail;
- current autoswitch safety/reconnect/load state.

## During Hold

Verify:

- `v7-users-autoswitch.timer` inactive;
- `v7-users-autoswitch.service` inactive;
- no autoswitch/user-switch/routing-sync process;
- no switch-history entries added;
- `users.registry` hash unchanged;
- `ip -4 rule show` unchanged or acceptably explained;
- route table snapshot unchanged or acceptably explained;
- autoswitch safety/reconnect/load state not modified by planner writes.

## Reconcile Stability

Run at least two reconcile samples with ip-rule snapshots around them:

```text
ip-rules.before
reconcile.1
ip-rules.after-reconcile-1
reconcile.2
ip-rules.after-reconcile-2
```

Stable means the same expected rules exist before and after, and reconcile either passes or fails consistently with explainable evidence.

## After Restore

Verify:

- `v7-users-autoswitch.timer` restored to pre-hold state;
- service is not stuck active;
- no orphan autoswitch/user-switch/routing-sync process;
- users registry hash unchanged;
- no unexpected switch-history movement;
- route/rule snapshots still safe.

## Rehearsal Pass Criteria

```text
no users moved
autoswitch held
quiet interval observed
read-only checks completed
autoswitch restored
no unexpected drift
```

## Rehearsal Fail Criteria

- user assignment changed;
- switch-history changed unexpectedly;
- route/rule changed unexpectedly;
- autoswitch process active during window;
- restore failed;
- any mutation outside the approved hold occurred.
