# E11.17 Generation Governance Matrix

## Verdict

classification=GENERATION_GOVERNANCE_CONDITIONAL
unattended_apply_safe=false_for_unbounded_clearance
bounded_clearance_budget_safe=true
mini_cohort_promotion_clean=true_for_two_user_bounded_lifecycle
larger_cohort_justified=false

## Evidence Anchors

- Pre-rehearsal live state: `pre-rehearsal-snapshot.txt`
- Current clearance weakness on full copied state: `full-copy-clearance-counterfactual-before-fix.txt`
- Bounded runtime fix deploy: `runtime-fix-deploy.txt`
- Post-fix copied-state proof: `post-fix-clearance-budget-counterfactual.txt`
- Live fail-closed timer rehearsal: `fail-closed-rehearsal.txt`
- Live clearance budget rehearsal: `generation-clearance-rehearsal.txt`
- Multi-interval observations: `observation-A.txt` through `observation-E.txt`

## Matrix

| Theory | Tested | Evidence | Operational Impact | Production Risk | Remaining Risk | Larger Cohort Relevance |
|---|---:|---|---|---|---|---|
| barrier expiry leaks movement | yes | expired uncleared live rehearsal: `selected_moves=0`, hash stable, switch-history 2698 | fail-closed barrier works | controlled | none for expired uncleared state | does not justify larger cohort |
| generation clearance unlocks stale movement | yes | copied-state pre-fix clearance produced `selected_moves=3` | plain clearance is unsafe | high without budget | bounded by E11.17 budget guard | blocks larger cohort without separate capacity governance |
| planner generation missing | yes | no persisted planner/apply generation ID exists; budget guard is count-based | ownership remains partial | medium | full generation-token model still optional future hardening | larger cohorts should wait |
| apply generation missing | yes | systemd apply recomputes live plan; no generation binding | apply can legitimately see fresh pressure | medium | budget guard prevents movement above approved budget | larger cohorts need explicit movement budget |
| stale replay | yes | switch-history count stayed 2698; users hash stable | no replay observed | low for this rehearsal | no immutable replay token yet | monitor |
| delayed recompute | yes | sample E saw live pressure: `candidate_moves_total=7`, before guard `3`, selected `0` | recompute occurred but was bounded | controlled | pressure can recur; apply must stay governed | important blocker for larger cohort |
| rebalance leak | yes | rebalance candidates remained `0` in collected plans | no rebalance leak observed | low | none observed | monitor |
| service-signal failover | yes | egress `1` remained telegram-down; budget guard suppressed selected failover | service pressure remains real | controlled with budget | unsafe if clearance lacks budget | blocks unbounded apply |
| selected_moves invalidation | yes | selected remained `0` in all live samples; no stale selected cache file caused movement | no stale selected cache observed | low | no persisted selected_moves ownership yet | monitor |
| timer overlap | yes | multiple timer intervals ran; users hash and switch-history stable | no overlap movement observed | low | timer should remain held after rehearsal | larger cohort still no-go |
| hidden apply | yes | process scans only showed expected timer/apply context, no `v7-user-switch` or routing-sync | no hidden mover | low | continue hidden scan in future blocks | required gate |
| restore lifecycle ownership | yes | E11.17 barrier state explicitly records expired cleared budget-zero rehearsal | ownership improved | controlled | full generation IDs not yet implemented | future hardening |

## Final Classification

readiness_classification=GENERATION_GOVERNANCE_CONDITIONAL
operational_maturity_status=BOUNDED_APPLY_GOVERNANCE_REHEARSED_BUT_UNBOUNDED_CLEARANCE_FORBIDDEN
recommended_next_block=E11.18_TWO_USER_MINI_COHORT_PROMOTION_CLEAN_APPROVAL_OR_GENERATION_TOKEN_DESIGN
