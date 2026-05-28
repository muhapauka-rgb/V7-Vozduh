# E11.11 Lifecycle Consistency Review

lifecycle_review_completed=true

## Lifecycle Verdict

lifecycle_stable=true

The E11.10 lifecycle closed the full governed path: hold, one candidate move already executed, observation, rollback decision, rollback, planner restore, restore-settle gate, apply restore, and delayed monitoring. E11.11 review found no hidden mover, no selected moves in current planning, and no checker regression.

## Lifecycle Risk Matrix

| Stage | Required invariant | E11.11 evidence | Risk | Hardening result |
|---|---|---|---|---|
| Planner hold | Planner must not race with canary movement | E11.10 closeout started with planner held; E11.11 timers active only after closeout | Low | Keep hold-before-mutation rule |
| Apply hold | Apply must not move non-candidate users | E11.10 closeout held apply before rollback; E11.11 selected moves zero | Low | Keep apply held during future cohort mutation |
| Canary move | Only approved users may move | E11.10 report shows only `10.7.0.3` moved | Low for one-user, medium for cohort | Mini-cohort needs explicit movement list and per-user rollback |
| Observation | Route/checkers must stay OK | E11.10 A/B/C passed; E11.11 checkers OK | Low | Keep route/checker evidence per sample |
| Keep/rollback | Keep must be rejected on selected moves | E11.10 pre-rollback samples B/C had `selected_moves=1`; rollback selected | Low | Keep selected-move veto |
| Rollback | Rollback must affect only candidate users | E11.10 rollback diff showed only `10.7.0.3` | Low | Cohort rollback must validate exact N-user diff |
| Planner restore | Planner returns before apply | E11.10 restored planner first | Low | Keep staged restore |
| Restore-settle | Samples span multiple apply intervals | E11.10 and E11.11 settle gates span multiple intervals | Low | Tool default now points at current samples |
| Apply restore | Apply returns only after gate GO | E11.10 apply restore authorized after GO | Low | Keep no manual autoswitch apply |
| Delayed monitoring | Detect delayed movement after timers resume | E11.10 final monitoring: no delayed movement | Medium for cohort | Mini-cohort must monitor longer because N-user blast radius is higher |

## Race Windows

| Window | Current coverage | Residual risk |
|---|---|---|
| Timer fires while manual movement occurs | Covered by planner/apply hold | Low |
| Planner computes selected moves after rollback before apply restore | Covered by restore-settle gate | Low |
| Apply timer fires after clean immediate sample but before delayed degradation is visible | Covered by delayed monitoring; proven after E11.10 | Medium for cohort because more users increase rollback complexity |
| Hidden `v7-user-switch` or `v7-routing-sync` runs outside timer path | Process scan clean in E11.11 snapshot | Medium because tool lineage still has unresolved production-only entries |

## Required Mini-Cohort Additions

- Exact cohort user list and exact rollback target for each user.
- Movement budget cap `max_users=2` unless capacity is separately expanded.
- Per-user route and registry diff after forward and rollback.
- Delayed monitoring at least three samples after apply restore.
- No broad autoswitch apply and no routing-sync.
