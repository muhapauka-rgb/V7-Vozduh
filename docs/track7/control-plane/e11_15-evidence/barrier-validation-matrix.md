# E11.15 Restore Barrier Validation Matrix

| Theory | Tested | Evidence | Result | Remaining Risk |
|---|---:|---|---|---|
| barrier active but not consumed | yes | timer journal shows `restore_barrier.active=true`, decisions include `restore_barrier_failover_suppressed` | pass | none in rehearsal window |
| barrier TTL expired too early | yes | barrier remained active through precheck and observations A-E | pass | post-TTL behavior not observed |
| apply ignores barrier | yes | timer-triggered apply run had `apply_requested=true`, `selected_moves=0`, `apply_result.reason=no_selected_moves` | pass | generation-token model still stronger |
| planner respects barrier but apply recomputes differently | yes | dry-run and apply-timer generation both produced selected_moves=0 | pass | no post-TTL proof |
| failover suppressed but rebalance still moves users | yes | every sample had `rebalance_candidates=0`, `selected_moves=0` | pass | continue targeted tests |
| selected_moves generated from non-failover path | yes | candidate_moves_total=0 and selected_moves=0 in all samples | pass | none observed |
| Telegram service signal still causes moves | yes | apply journal showed Telegram degraded/down-grace reasons but failover stayed suppressed | pass | post-TTL may resume normal failover |
| non-service pressure causes moves | yes | E11.14 v2 fixed non-service failover pressure; E11.15 timer run still selected 0 | pass | none in rehearsal window |
| generation mismatch | partially | barrier protected timer generations during rehearsal | conditional | explicit generation token still recommended |
| apply timer race | yes | multiple timer intervals completed with stable hash/count | pass | longer unattended window not approved |
| stale barrier file | yes | barrier hash stable and parser reported active | pass | file lifecycle after TTL still needs validation |
| barrier parse bug | yes | plan output contained active barrier metadata | pass | none observed |
| barrier path permission bug | yes | runtime read `/opt/v7/egress/state/autoswitch-restore-barrier.json` successfully | pass | none observed |
| apply restore order bug | yes | `systemctl start v7-users-autoswitch.timer` caused timer run without user movement | pass | post-TTL order still untested |
| hidden mover | yes | hidden scans found no `v7-user-switch` or `v7-routing-sync`; one `v7-telegram-sentinel --no-autoswitch` was non-mutating | pass | normal process hygiene still required |
| routing-sync interference | yes | no routing-sync process observed; switch-history count stable | pass | routing-sync remains forbidden |
| restore-settle false GO | yes | restore-settle can be GO while future apply generation needs barrier | conditional | settle gate alone remains insufficient |
| delayed movement after barrier sample window | yes for bounded window | five intervals completed with no registry/switch drift | pass | longer/post-TTL window untested |
| barrier leaves system frozen after TTL | no | TTL was next day, not observed | open | requires E11.16 or scheduled post-TTL block |
| production autoswitch recovery blocked too strongly | yes | active barrier suppresses failover by design | conditional | apply timer must remain held unless explicitly cleared/validated |

## Classification

readiness_classification=APPLY_RESTORE_BARRIER_CONDITIONAL

The restore barrier passed the bounded apply timer rehearsal. It did prevent delayed non-cohort movement across multiple apply intervals. It is not yet sufficient to leave apply active unattended because TTL expiry and generation lifecycle behavior remain unobserved.
