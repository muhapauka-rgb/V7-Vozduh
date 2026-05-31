# V7 Speed-Based Channel Switching Rules

## Purpose

This document answers where current V7 speed-related channel switching rules live and what they actually do today.

## Source Files

Primary movement selector:

- `tools/v7-users-autoswitch`

Admin policy defaults and UI/API:

- `admin/v7-admin-api`

Related E35 audit:

- `docs/track7/productization/e35_0_1-audit/speed-policy-audit.md`
- `docs/track7/productization/e35_0_1-audit/current-priority-chain.md`

## Rule 1: Minimum Average Speed Floor

Current default:

```text
min_avg_mbps = 15.0
```

Where defined:

- `tools/v7-users-autoswitch`, `DEFAULT_QUALITY_POLICY`
- `admin/v7-admin-api`, `DEFAULT_POLICY`

Where enforced:

```python
if egress.avg_mbps < min_avg:
    self._block(candidate, "avg_mbps_below_floor")
```

Meaning:

If a candidate channel average speed is below 15 Mbps, it is hard-blocked as a movement target.

This is not a score penalty. It disqualifies the candidate before ranking.

## Rule 2: Minimum Floor Speed

Current default:

```text
min_floor_mbps = 10.0
```

Where enforced:

```python
if egress.min_mbps < min_floor:
    self._block(candidate, "min_mbps_below_floor")
```

Meaning:

If a candidate channel's minimum observed speed is below 10 Mbps, it is hard-blocked as a movement target.

This prevents choosing a channel that has good average speed but bad floor performance.

## Rule 3: Stability Floor

Current default:

```text
min_stability = 0.45
```

Where enforced:

```python
if egress.stability and egress.stability < min_stability:
    self._block(candidate, "stability_below_floor")
```

Meaning:

If a channel has measured stability below 0.45, it is hard-blocked. Stability can therefore override raw speed.

## Rule 4: Better Candidate Must Beat Current by Score Threshold

Current defaults:

```text
min_score_improvement_pct = 0.20
min_score_delta = 50.0
```

Where enforced:

```python
return best.score >= current.score * (1.0 + improvement_pct) and (best.score - current.score) >= min_delta
```

Meaning:

For a planned switch, a better channel must beat the current channel by both:

- at least 20% total score improvement;
- at least 50 score points.

This is not purely a speed comparison. It is total candidate score.

## How Speed Contributes to Score

Speed is one score component after hard gates pass:

```python
"speed": ((egress.avg_mbps / max_avg) * 120.0)
       + ((egress.min_mbps / max_min) * 60.0)
       + ((egress.client_mbps / max_client) * 20.0 if max_client else 0.0)
```

Meaning:

- average speed can add up to 120 points;
- minimum speed can add up to 60 points;
- client-observed speed can add up to 20 points;
- total direct speed contribution is about 200 points.

Speed can help a candidate win, but only after the candidate passes health, service, quality, capacity, group, and safety gates.

## Is There a Current "x2 Faster" Rule?

Current direct x2 speed rule found:

```text
false
```

A search in current autoswitch/admin code did not find a direct rule like:

- switch if candidate Mbps >= current Mbps * 2
- switch if faster than x2
- switch if speed ratio >= 2.0

The closest current behavior is score-based:

```text
candidate total score >= current total score * 1.20
AND
candidate total score - current total score >= 50
```

So if earlier product thinking used "x2 faster", it is not currently implemented as a direct Mbps ratio in the inspected selector. It may have been replaced by the broader score model.

## Operator Interpretation

Current speed behavior:

1. Do not use channels below floor:
   - avg < 15 Mbps blocks candidate;
   - min < 10 Mbps blocks candidate.

2. Above the floor, speed is a preference:
   - faster channel gets more score;
   - speed does not override required services, capacity, health, stability, group constraints, or safety.

3. Planned switch requires meaningful total improvement:
   - 20% score improvement;
   - 50 score points.

## Admin Surface

Current admin exposes the speed floors in `Настройки` / policy controls:

- `min_avg_mbps`
- `min_floor_mbps`
- `min_stability`

Current admin also shows:

- quality threshold as `15/10 Mbps`
- speed/stability in autoswitch plan explanations.

## Summary

speed_floor_rule_exists=true
speed_floor_avg_mbps=15.0
speed_floor_min_mbps=10.0
stability_floor_exists=true
stability_floor=0.45
score_improvement_rule_exists=true
score_improvement_pct=0.20
score_delta=50.0
direct_x2_speed_rule_found=false

## Final Mutation Statement

Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
