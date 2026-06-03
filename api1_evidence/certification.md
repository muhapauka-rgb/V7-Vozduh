# API.1 Certification

## Questions

Can decomposition begin safely?

Yes, but only as a constrained read-only extraction program.

What should be extracted first?

1. Registry read/view helpers over `admin_core.registry_readers`.
2. Operator observability serializers already aligned with `admin_core.operator_observability`.
3. Event/audit/evidence read-only builders.
4. Small pure validators and serializers.

What must never be extracted first?

- `Handler.do_GET`;
- `Handler.do_POST`;
- auth/session/RBAC/CSRF;
- `run_action`;
- runtime apply handlers;
- user movement;
- rollback apply;
- policy/direct/trusted RU apply;
- audit writer;
- closure writer;
- identity/profile issuance writes;
- the whole embedded UI function.

What must remain runtime authority?

- runtime-support tools for runtime changes;
- `tools/v7-users-autoswitch` for planner/autoswitch execution semantics;
- `/opt/v7/egress/state` registries for users and egresses;
- `/etc/v7` policy/config files;
- `admin_core.operator_execution` for execution packet contract model;
- `admin_core.routing_brain` and `admin_core.routing_intelligence` for RI advisory contracts.

## Final API.1 Verdicts

| Verdict | Value |
|---|---|
| endpoint_inventory_complete | true |
| truth_source_map_complete | true |
| dependency_graph_complete | true |
| ownership_map_complete | true |
| read_write_boundary_map_complete | true |
| safe_extraction_candidates_identified | true |
| performance_audit_complete | true |
| decomposition_plan_complete | true |
| performance_foundation_plan_complete | true |
| safe_to_begin_api2 | true, with read-only scope only |

## Safety

| Safety item | Value |
|---|---|
| runtime_behavior_changed | false |
| governance_behavior_changed | false |
| runtime_mutation_performed | false |
| routing_changed | false |
| users_moved | false |
| deploy_performed | false |
| systemd_changed | false |

## Certification Statement

API.1 produced an authoritative decomposition map and safe extraction roadmap for `admin/v7-admin-api`. It did not refactor, extract, rewrite, deploy, mutate runtime state, alter governance behavior, alter routing, or move users.
