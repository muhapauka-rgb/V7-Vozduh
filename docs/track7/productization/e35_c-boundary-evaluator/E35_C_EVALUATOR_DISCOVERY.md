# E35.C Evaluator Discovery

## Scope

E35.C defines a runtime-neutral decision engine:

- Boundary Evaluator;
- Conflict Resolver;
- Authority Verdict Engine.

It does not implement autoswitch, scoring, route selection, service matrix, capacity logic, runtime mutation or user movement.

## Existing Decision Points

| Existing Check | Current Location | Evaluator Relationship | Classification |
|---|---|---|---|
| Autoswitch basic gates | `tools/v7-users-autoswitch` `_gate_basic` | Input: channel basic eligibility | Reuse |
| Autoswitch group gates | `_gate_org` | Input: group boundary | Reuse |
| Autoswitch service gates | `_gate_service` | Input: required service status | Reuse |
| Autoswitch quality gates | `_gate_quality` | Input: quality floor status | Reuse |
| Autoswitch load gates | `_gate_load` | Input: capacity/load status | Reuse |
| Autoswitch safety gates | `_gate_safety` | Input: safety status | Reuse |
| Approval packet validation | `admin_core/operator_execution.py` | Input: governance state | Reuse |
| Packet replay denial | `DENY_REPLAY` | Input: governance hard deny | Reuse |
| Registry hash mismatch | `DENY_HASH_MISMATCH` | Input: stale runtime/governance deny | Reuse |
| Selected moves hash/count | `selected_moves_state` | Input: runtime drift/hidden work | Reuse |
| Restore-settle | previous governance helpers | Input: runtime stabilization | Reuse |
| Runtime Trust | Wave 3 trust surface | Input: system trust | Reuse |
| Release Trust | Wave 3 trust surface | Input: release/runtime match | Reuse |
| Manual switch | Admin `user-switch` action | Consumer of evaluator output | Extend |
| Rollback paths | admin and governance rollback | Consumer/emergency action | Extend |
| Quarantine/anti-flap | autoswitch safety state | Input: safety/emergency | Reuse |
| Proposal | Wave 2 proposal surface | Input context only | Do Not Touch |
| Score/speed | autoswitch ranking | Outside evaluator | Do Not Touch |

## Inputs To Evaluator

The evaluator should consume statuses produced elsewhere:

- authority state;
- group constraints;
- required service result;
- suitability result;
- capacity result;
- governance result;
- runtime trust;
- restore-settle;
- selected moves/hidden movers;
- emergency context;
- proposal/evidence context.

It must not recompute those systems internally.

## Outside Evaluator

Remain outside:

- target selection;
- speed scoring;
- service matrix probing;
- capacity probing;
- actual movement;
- policy apply;
- routing sync;
- kill switch mutation.

## Discovery Verdict

```text
evaluator_discovery_complete=true
existing_inputs_identified=true
outside_evaluator_boundaries_identified=true
```
