# E35.0.1 Stability Policy Audit

## Scope

Audit question: how stability and degradation participate.

## Stability Inputs

stability_policy_audited=true

Stability appears in:

- egress live state `stability`
- `egress-speed.json` fallback stability
- `egress-quality-summary.json` window stability
- quality score trend
- safety state anti-flap and pair reversal windows
- service failure persistence
- Telegram soft/hard status

## Hard Stability Floor

Autoswitch hard-blocks a candidate when:

- `egress.stability` exists and is below `min_stability`

Default:

- `min_stability`: 0.45

## Stability Score

If the candidate passes hard gates:

- direct `stability` score contributes up to 150 points.
- quality history contributes fail-rate and window stability:
  - fail rate can reduce up to 80 points.
  - window stability can add up to 60 points.
  - degrading trend subtracts 40.
  - improving trend adds 20.

## Degradation Semantics

Service degradation is not always hard failure:

- Telegram hard down is hard.
- Telegram degraded is soft penalty.
- a single non-persistent non-Telegram service failure is soft degradation.
- persistent service failure is hard.
- multiple critical service failures are hard.

Safety degradation can hard-block:

- user frozen by switch frequency
- egress quarantine
- failed verification limit
- pair reversal stability window
- target blocked for user

## Can Stability Override Speed?

stability_can_override_speed=true

Stability can override speed in two ways:

- hard floor: low stability disqualifies a channel before score.
- score: stability and quality history can outweigh speed after gates.

## Audit Verdict

stability_measured=true
stability_hard_floor=true
stability_score_component=true
degradation_can_be_soft_or_hard=true
stability_overrides_speed_when_below_floor=true
