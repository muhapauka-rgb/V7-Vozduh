# E11.16 Root-Cause Matrix

| Row | Observed | Evidence | Operational Impact | Production Risk | Regression Risk | Fix Required | Generation Relevance |
|---|---:|---|---|---|---|---:|---|
| barrier expiry | yes, counterfactual | expired-barrier dry-run selected 3 moves | post-TTL apply would move users | high if apply active | low after fail-closed fix | yes | explicit clearance required |
| planner generation | no persisted generation | code computes fresh plan per run | no stale planner replay file | medium | low | design required | generation ID would improve attribution |
| apply generation | fresh recompute | apply command runs same planner with `--apply` | apply can diverge from prior settle sample | high | medium | yes | apply must be bound to restore clearance |
| stale selected_moves | not observed | no selected_moves file; selected in memory | not root cause | low | low | no | generation still useful for proof |
| delayed recompute | observed/inferred | E11.14 live movement and E11.16 expired simulation | can move non-cohort users after clean gate | high | medium | yes | core driver |
| service-signal failover | observed | target `1` Telegram hard/down signals recur | moves users from otherwise healthy target | high | medium | yes | requires bounded restore clearance |
| non-service failover | possible | E11.14 v1 found non-service pressure path | can bypass service-only fix | medium | medium | yes | failover quarantine must cover all failover |
| target pressure | observed | quality/load scoring changes across samples | can make new targets attractive | medium | medium | yes | apply generation must be bounded |
| rebalance | not observed | `rebalance_candidates=0` in samples | no current movement path | low | low | no immediate | keep tests |
| planner cache | not observed | no persisted selected plan used by apply | no cache replay | low | low | no | not primary |
| restore ownership | missing | TTL expiry previously implied clearance | apply lifecycle lacks owner | high | low | yes | primary governance gap |
| generation mismatch | governance risk | settle sample and later apply are independent runs | sample may not bind future apply | high | medium | yes | generation token recommended |
| timer overlap | not observed | timers held/active as expected | no concurrent apply found | medium | low | no immediate | monitor |
| governance gap | observed | E11.14 live, E11.16 counterfactual | unsafe unattended post-TTL apply | high | low | yes | fixed with fail-closed clearance |

classification=CONDITIONAL_WITH_GENERATION_GOVERNANCE

