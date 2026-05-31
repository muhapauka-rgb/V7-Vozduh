# E35.0.1 Hard vs Soft Rules Matrix

hard_soft_matrix_defined=true

| Condition | Current Behavior | Rule Type | Evidence Path |
|---|---|---|---|
| Egress disabled | Candidate blocked | Hard | `_gate_basic` |
| Egress maintenance/disabled/quarantine | Candidate blocked | Hard | `_gate_basic` |
| `manual_only` | Candidate blocked | Hard | `_gate_basic` |
| Health code non-200 | Candidate blocked | Hard | `_gate_basic` |
| Severity not OK/WARN | Candidate blocked | Hard | `_gate_basic` |
| Canary reserved target | Candidate blocked except current hold | Hard | `_gate_reservation` |
| Group allowed pool mismatch | Candidate blocked | Hard | `_gate_org` |
| Group excluded egress | Candidate blocked | Hard | `_gate_org` |
| Exclusive group mismatch | Candidate blocked | Hard | `_gate_org` |
| Average Mbps below floor | Candidate blocked | Hard | `_gate_quality` |
| Min Mbps below floor | Candidate blocked | Hard | `_gate_quality` |
| Stability below floor | Candidate blocked | Hard | `_gate_quality` |
| Trusted RU required but target not trusted | Candidate blocked | Hard | `_gate_service` |
| Telegram hard down | Candidate blocked | Hard | `_gate_service` |
| Route class fitness FAIL | Candidate blocked | Hard | `_gate_service` |
| Multiple critical service failures | Candidate blocked | Hard | `_gate_service_failures` |
| Persistent service failure | Candidate blocked | Hard | `_gate_service_failures` |
| Planned target at hard limit | Candidate blocked | Hard | `_gate_load` |
| Failover target at failover hard limit | Candidate blocked | Hard | `_gate_load` |
| Egress safety quarantine | Candidate blocked | Hard | `_gate_safety` |
| Failed verification limit | Candidate blocked | Hard | `_gate_safety` |
| Target blocked for user | Candidate blocked | Hard | `_gate_safety` |
| Pair reversal window | Candidate blocked | Hard | `_gate_safety` |
| Telegram degraded | Score penalty/reason | Soft | `_gate_service`, `_score_parts` |
| Single transient service failure | Degraded reason and score penalty | Soft | `_gate_service_failures`, `_service_scores` |
| Route class fitness WARN | Reason/score impact | Soft | `_gate_service`, `egress_candidate_score` |
| Quality history high fail rate | Advisory reason/score impact | Soft | `_gate_quality`, `_score_parts` |
| Low speed but above floor | Lower score | Soft | `_score_parts` |
| Lower stability but above floor | Lower score | Soft | `_score_parts` |
| High latency | Lower score | Soft | `_service_scores` |
| Higher load below hard limit | Lower score / projected selection | Soft | `_score_parts`, `_pick_projected_moves` |
| Group preferred egress | Positive reason/score | Soft | `_gate_org`, `_score_parts` |
| Current channel | Sticky score bonus | Soft | `_score_parts` |
| Candidate barely better than current | Keep current | Soft threshold | `_beats_current` |

## Audit Verdict

hard_rules_exist=true
soft_preferences_exist=true
binary_and_score_layers_both_exist=true
speed_low_below_floor_is_hard=true
speed_low_above_floor_is_soft=true
service_failure_can_be_hard_or_soft=true
