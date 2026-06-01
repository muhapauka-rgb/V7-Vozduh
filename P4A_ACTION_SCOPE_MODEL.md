# P4.A Action Scope Model

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Scope

Selected first action scope:

`runtime_governance.zero_move_state_transition`

## Target

Append-only governance/audit record target in the future authorized runtime governance store.

## Affected Entities

- Users affected: `0`
- Routes affected: `0`
- Services affected: `0`
- Systemd units affected: `0`
- Autoswitch state affected: `0`
- Policy state affected: `0`
- Runtime governance/audit lineage affected: `1 append-only record` in a later action block

## Blast Radius

Blast radius is governance-record-only. It does not alter traffic, assignment, capacity, route policy, service configuration or user-visible behavior.

## Constraints

- selected move budget must be `0`
- allowed users must be empty
- allowed targets must be empty
- selected move hash must equal empty selected-moves hash
- approval must be dual operator
- packet must be unexpired
- runtime registry hashes must match
- dry-run verification must be current
- rollback is compensating record only

## Verdict

`action_scope_defined=true`

