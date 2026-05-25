# V7 Phase 5 Multi-Tenant Model

## Purpose

Phase 5 turns the existing identity layer into an explicit multi-tenant contract without rewriting runtime behavior.

V7 remains an internet access routing platform. Users and organizations should never need to understand route internals.

## Entities

### Organization

An organization is the commercial and policy boundary.

It owns:

- users;
- allowed phone entries;
- device eligibility;
- route access policy;
- diagnostics visibility;
- future subscription/commercial hooks.

Current storage:

- SQLite `organizations`;
- SQLite `allowed_users.organization_id`;
- SQLite `identity_users.organization_id`;
- `/etc/v7/org-egress-policy.json`.

### Group

A group is an operator-controlled policy bundle.

It may define:

- default route mode;
- route access class;
- allowed egress family;
- future quotas or commercial tier.

Current storage:

- SQLite `groups`;
- SQLite `organizations.group_id`;
- SQLite `allowed_users.group_id`;
- SQLite `identity_users.group_id`.

### User

A user represents a person or account, not a network route.

Current storage:

- SQLite `identity_users`;
- registry metadata in `/opt/v7/egress/state/users.registry`;
- optional `user_metadata` compatibility table.

### Device

A device represents one access profile on one endpoint.

Current storage:

- SQLite `devices`;
- generated client artifacts under `V7_CLIENT_ROOT`;
- smart profiles under `V7_SMART_CLIENT_ROOT`;
- active runtime assignment in `users.registry`.

### Policy

Policy controls what access is allowed.

Policy must not be bypassed by:

- onboarding;
- profile issuance;
- autoswitch;
- direct routing;
- trusted RU behavior.

## Source Of Truth

Identity DB is the authority for organization, user, device, pending profile, and onboarding lifecycle.

Runtime registries are the authority for active datapath assignment.

Profile delivery tokens are one-time access material, not identity authority.

## Tenant Boundary Rule

No feature may mix organizations implicitly.

Cross-organization sharing must be explicit, operator-visible, policy-driven, and auditable.

