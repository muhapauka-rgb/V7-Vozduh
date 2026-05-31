# E35.0 Channel Constraints Audit

## Scope

Audit question: can organizations or users restrict channel usage today, and what allowlist/denylist/suitability logic exists.

## Existing Constraint Sources

channel_constraint_sources_found=true

Current egress/channel metadata supports:

- `role`
- `priority`
- `weight`
- `soft_limit`
- `hard_limit`
- `manual_only`
- `reserve_only`
- `service_tags`
- `exclude_route_classes`
- `organization_scope`

These are normalized in `egress_usage_policy_from_data()` and `egress_organization_scope_from_data()`.

## Organization Policy File

`/api/org-egress-policy` exists, and admin can save `org-egress-policy.json` through `/api/actions/org-egress-policy-update`.

The policy shape includes organization/group/egress concepts. This is a policy surface, but current audit did not find proof that it is a universal hard gate for all channel selection and user movement.

## User-Level Constraints

explicit_user_channel_allowlist_found=false
explicit_user_channel_denylist_found=false
preferred_channel_field_found=false

Users currently carry their active assignment in `users.registry` as `current=<egress>` with a route table. This is a persisted assignment, but not a separate allowlist/denylist/preference model.

## Suitability Logic

Suitability exists through:

- egress role matching
- route class fitness from service matrix
- Telegram hard/soft state
- service tags
- excluded route classes
- manual-only/reserve-only flags
- health/readiness/speed/load inputs

`egress_candidate_score()` rejects disabled egress, excluded route classes, manual-only candidates, and strict trusted-RU mismatches. It scores health, role, service matrix, Telegram status, priority, weight, speed, and reserve penalty.

## Audit Verdict

channel_constraints_audit_complete=true
org_constraints_exist=PARTIAL
user_constraints_exist=PARTIAL
hard_allowlist_denylist_model_exists=false
channel_suitability_logic_exists=true

## E35 Implication

Current system has the ingredients for constraints, but not a clear product-grade rule:

`user/group requires service X`
down to
`only these channels are eligible`
down to
`movement/proposal cannot use any other channel`.

E35 should formalize this without replacing existing metadata.
