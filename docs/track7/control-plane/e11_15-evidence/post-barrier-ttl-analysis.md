# E11.15 Post-Barrier TTL Analysis

## TTL State

barrier_ttl_status=ACTIVE_NOT_EXPIRED_NOT_OBSERVED_POST_TTL

Evidence:

- Barrier file: `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- Barrier active during pre-rehearsal, dry-run, immediate restore, and observations A-E.
- `expires_at=2026-05-28T10:52:27.369480+00:00`
- Rehearsal observation window: 2026-05-27T14:33:22+03:00 through 2026-05-27T14:36:35+03:00.

TTL expiry was not within a reasonable bounded E11.15 window. Per block constraints, E11.15 did not wait indefinitely and did not mutate the barrier file.

## Production Recovery Risk

While active, the barrier intentionally suppresses failover movement. That is correct for post-restore containment, but it also means apply-timer production recovery is over-suppressed until the barrier expires or is explicitly cleared by a future governed block.

This is why E11.15 restored the apply timer only for a bounded rehearsal and then returned it to hold.

## Post-TTL Requirement

Future validation is still required for:

- normal no-op behavior after TTL expiry;
- absence of delayed non-cohort movement after barrier expiry;
- whether a generation-token model is required to distinguish intended restore generations from fresh apply recompute cycles.

post_ttl_validation_completed=false
apply_timer_can_remain_active_unattended=false
apply_timer_final_state=held

