# E25.12 Replacement Profile Option

## Decision

`replacement_profile_used=false`

`replacement_target_name=NONE`

`operator_replacement_profile_required=false`

## Reason

The current execution target recovered after bounded target-local quality recovery:

- MTU changed from `1280` to `1200` on `v7execwg0`
- 20-sample sustained window completed
- avg Mbps final: `27.12`
- min Mbps final: `10.67`
- stability final: `1.000`
- no sample below floor: `true`
- explicit execution-target readiness: `GO`
- restore-settle gate: `GO`

Because the current target now satisfies the movement readiness quality floors, E25.12 did not import or activate a replacement profile.

## Residual Note

The recovered target passed by a narrow hard-min margin: the lowest observed sample was `10.67 Mbps` against a `10.0 Mbps` floor. E25.13 must still regenerate a fresh approval packet and E25.14/E25 execution must still perform execution-time readiness rechecks before any user movement.
