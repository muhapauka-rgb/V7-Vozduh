# E25.3 Recovery / Retarget Decision

## Decision

`OPTION_C: CREATE_DEDICATED_EXECUTION_ONLY_EGRESS`

Secondary allowed path:

`OPTION_A: WAIT_AND_RECOVER_CURRENT_WG_TARGET` only if the next execution block requires a fresh sustained GO window immediately before execution.

## Reasoning

The current WireGuard target is not permanently failed. E25.3 observed 16 consecutive GO samples over about 15 minutes, and the final safety check was GO.

However, the same target produced fresh NO-GO during E25.2 execution-time recheck:

- `min_mbps=4.61`
- `stability≈0.30`

That means the target is recoverable but spiky. For a first production-grade operator-driven movement, the target should not oscillate across the readiness boundary during the execution window.

## Existing Target Options

- Current WireGuard: best existing candidate, but conditional due quality spikes.
- OpenVPN: zero-user but diagnose SUSPECT/interface unknown.
- AWG targets: occupied and hard-full.
- VLESS: diagnose SUSPECT, load nonzero, exclusions missing.

## Operational Implication

The governance system is working: it prevented unsafe movement. The blocker is target quality, not execution governance.

## Recommended Next Block

`E25_4_DEDICATED_EXECUTION_EGRESS_PREPARATION`

If the operator wants to keep using the current WireGuard target anyway, use:

`E25_4_FIRST_MOVEMENT_WITH_RECOVERED_TARGET`

but require:

- a fresh 15-30 minute sustained GO window,
- no sample below floor,
- immediate execution-time target readiness GO,
- restore-settle GO,
- selected_moves=0,
- hidden movers absent,
- runtime checkers OK.

## Final Decision Flags

- `wait_and_recover_current_wg_target=conditional`
- `retarget_to_different_existing_egress=false`
- `create_dedicated_execution_only_egress=true`
- `rework_quality_scoring_before_first_movement=false`
- `no_go_current_architecture=false`
