# E35.0 Organizations / Groups Audit

## Scope

Audit question: what are "Организация" and "Группа" today, how are they stored, displayed, and used.

## Findings

organization_exists=true
group_exists=true
separate_group_concept_exists=true

Current code has a separate identity SQLite schema in `admin/v7-admin-api`:

- `groups(id, name, description, route_policy, created_at, updated_at)`
- `organizations(id, name, short_name, aliases, group_id, created_at, updated_at)`
- `allowed_users(... organization_id, group_id ...)`
- `identity_users(... organization_id, group_id ...)`

An organization is currently an identity/admin entity. It is not itself a runtime route, channel, or movement authority.

A group is also an identity/admin entity. It carries `route_policy`, and that value is used by `identity_effective_smart_mode()` as the default smart client mode source when a user/allowed phone belongs to a group.

## Storage

Authoritative storage:

- Identity DB: `IDENTITY_DB_FILE`
- Schema is created by `IDENTITY_SCHEMA` in `admin/v7-admin-api`.

Organization fields:

- `id`
- `name`
- `short_name`
- `aliases`
- `group_id`
- timestamps

Group fields:

- `id`
- `name`
- `description`
- `route_policy`
- timestamps

## Admin Surface

Organizations and groups are visible in current V7 Admin under:

- `Пользователи`
- workspace/tab: `Организации`
- identity/access controls table renders both groups and organizations.

Channel onboarding also has an organization scope picker (`organization_scope`) for egress drafts.

## Runtime Use

Confirmed current use:

- Group route policy can override requested smart mode during identity/connect flow.
- Organization can link to a group.
- Organization scope can be stored on channel metadata/drafts.

Not confirmed as hard runtime authority:

- No evidence that organization alone hard-gates channel selection for every routing/proposal path.
- No explicit per-user organization allowlist/denylist enforcement was found in the user movement path.

## Audit Verdict

organizations_groups_audit_complete=true
organization_current_role=IDENTITY_AND_ADMIN_METADATA
group_current_role=IDENTITY_GROUP_WITH_ROUTE_POLICY_DEFAULT
runtime_authority=PARTIAL

## E35 Implication

E35 can reuse existing organizations and groups, but should not assume they already implement full production group constraints. The missing product layer is explicit group constraint enforcement and visibility in routing/proposal decisions.
