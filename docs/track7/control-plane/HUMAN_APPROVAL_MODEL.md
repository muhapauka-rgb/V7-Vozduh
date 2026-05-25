# Human Approval Model

This model defines who must approve future rehearsal and canary operations. It does not approve them.

## Approval Classes

| Action | Required approval |
|---|---|
| quiet-window rehearsal | operator approval |
| autoswitch hold | operator approval |
| autoswitch restore | included in rehearsal approval |
| one-user canary | separate operator approval after rehearsal success |
| rollback for approved canary | pre-approved with canary packet |
| routing-sync | separate high-risk approval |
| policy/Direct/RU/proxy mutation | separate high-risk approval |
| kill-switch rebuild/disable | emergency/high-risk approval |

## Human Must Confirm

For rehearsal:

- hold affects autoswitch authority platform-wide;
- no users will be switched;
- exact restore command is known;
- maximum duration is known;
- evidence directory and capture commands are understood.

For canary:

- candidate user;
- current egress;
- target egress;
- rollback egress;
- rollback command;
- blast radius one user;
- autoswitch hold confirmed;
- target health;
- kill switch OK;
- route checks OK.

For rollback:

- rollback command;
- expected previous state;
- post-rollback checks;
- no routing-sync fallback unless separately approved.

## Approval Record

Every live operation packet must include:

```text
approver
timestamp
scope
allowed commands
forbidden commands
rollback path
maximum duration
stop conditions
```

## Non-Delegation

Approval for rehearsal does not approve canary. Approval for canary does not approve routing-sync, autoswitch apply, policy apply, or broad rollback.
