# E35.B Group Boundaries

## Product Meaning

Groups are routing/policy containers.

They define shared constraints for users.

## Group Rights

| Question | Answer |
|---|---|
| Can group restrict channels? | Yes. `allowed_egress` and `excluded_egress` are hard boundaries. |
| Can group require services? | Yes. Group required services become baseline user requirements. |
| Can group force AUTO? | It can define default routing mode AUTO for members without explicit user override. |
| Can group forbid MANUAL? | It may require governance/operator review before MANUAL, but should not silently forbid emergency/manual containment. |
| Can group forbid OPERATOR_PINNED? | It may require review; hard forbid is allowed only for regulated groups and must be explicit. |
| Can group force channel selection? | No. It can constrain eligible channels and set soft preference, but selection remains suitability/authority/execution-driven. |
| Can group override operator? | Only if group policy explicitly marks operator override forbidden and governance enforces it. Default: operator can request override with audit/review. |
| Can operator override group? | Only with explicit override reason and audit; never if Safety/Governance denies. |
| Can safety override group? | Yes. |
| Can containment override group? | Yes, but emergency only and temporary. |

## Non-Negotiable Group Limits

Group cannot:

- bypass safety;
- bypass governance scope;
- move users directly;
- turn soft preference into hidden hard lock without admin visibility;
- remove required service requirements silently;
- override containment during emergency.

## Admin Surface

Settings:

- group boundary defaults;
- allowed/excluded channels;
- required services;
- default routing mode;
- operator override policy.

Users:

- effective group boundary;
- group conflict reason.

Channels:

- groups allowed/blocked for channel.

## Runtime Mapping

Group boundaries map to:

- org egress policy groups;
- autoswitch `_gate_org`;
- required services model;
- future authority evaluator.

## Storage Impact

Extend org policy group records with explicit boundary semantics:

- `operator_override_policy`;
- `default_routing_mode`;
- `required_services`;
- `allowed_egress`;
- `excluded_egress`.

## API Impact

Future boundary read APIs must expose:

- effective group rules;
- conflicts;
- override requirements.

## Tests

- group allowed channel respected;
- group excluded channel blocks autoswitch and governance unless explicit override;
- group required service blocks unsuitable channel;
- group preference does not force movement;
- containment can temporarily override group in emergency.

## Verdict

```text
group_boundaries_defined=true
```
