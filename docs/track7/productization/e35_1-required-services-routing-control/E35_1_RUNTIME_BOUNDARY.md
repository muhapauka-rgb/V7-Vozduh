# E35.1 Runtime Boundary

Runtime mutation: NO
User movement: NO
Routing/apply/autoswitch apply: NO

## Allowed In E35.1

- Repository discovery.
- Documentation.
- Architecture and implementation planning.
- Storage/API/UI contract definition.
- Test plan definition.
- Static scans.

## Forbidden In E35.1

- Live user movement.
- `v7-user-switch`.
- `v7-routing-sync`.
- `v7-users-autoswitch --apply`.
- Broad routing sync.
- Policy apply.
- Direct RU mutation.
- Trusted RU refresh/diagnostic mutation.
- Kill switch mutation.
- Service restart.
- Runtime file mutation under `/opt/v7`, `/etc/v7`, `/etc/wireguard`.

## Future Execution Boundary

Required Services & Routing Control can influence future execution only through:

```text
Evidence
-> Proposal
-> Policy admission
-> Capacity gate
-> Concurrency/reservation gate
-> Approval packet
-> Execution-time recheck
-> Governed execution
-> Verification
-> Rollback capability
```

No E35.1 model field is authority by itself.
