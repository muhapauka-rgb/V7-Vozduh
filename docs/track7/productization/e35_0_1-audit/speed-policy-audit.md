# E35.0.1 Speed Policy Audit

## Scope

Audit question: how speed participates in channel selection.

## Speed Inputs

speed_policy_audited=true

Autoswitch loads speed from:

- `v7-state.json` egress live fields: `avg_mbps`, `min_mbps`
- `egress-speed.json`: `server_v7_mbps`, `server_v7_min_mbps`, `stability`
- `client-speed.json`: per-user/client observed V7 speed per egress
- `egress-quality-summary.json`: quality history windows and trends

## Hard Speed Floors

Speed is binary/hard at candidate gate time:

- `avg_mbps < min_avg_mbps` -> `avg_mbps_below_floor`
- `min_mbps < min_floor_mbps` -> `min_mbps_below_floor`

Default policy floors in autoswitch:

- average Mbps: 15
- minimum Mbps: 10

Admin policy update also exposes these floors.

## Speed Score

If the channel passes hard gates, speed contributes to score:

- avg Mbps normalized against max avg among egress -> up to 120 points
- min Mbps normalized against max min among egress -> up to 60 points
- client Mbps normalized against max client Mbps -> up to 20 points

Total direct speed contribution can be up to about 200 score points.

## Can Speed Override Suitability?

speed_can_override_hard_suitability=false

Speed is only scored after hard gates. A fast channel cannot beat:

- disabled/quarantine state
- health failure
- quality floor failure
- required service hard block
- hard capacity full
- group exclusion
- safety quarantine

## Score Thresholds

For planned movement, best candidate must beat current by both:

- percentage improvement threshold
- absolute score delta

Defaults:

- `min_score_improvement_pct`: 0.20
- `min_score_delta`: 50

## Audit Verdict

speed_measured=true
speed_hard_floor=true
speed_score_component=true
speed_tie_breaker_only=false
speed_override_hard_blocks=false
