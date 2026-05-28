# E25.7 Dedicated Target Metadata

## Result

- `dedicated_execution_target_created=false`
- `active_egress_registry_row_written=false`
- `target_zero_user=true`
- `governance_reserved=false`
- `autoswitch_excluded=false`
- `rebalance_excluded=false`
- `production_assignment_blocked=false`

## Reason

Active metadata was not written because target-local connectivity failed immediately after normalized activation.

There is also a governance-tooling conflict that must be resolved before a future successful activation can be considered production-ready:

- generic `v7-second-canary-target-readiness` rejects `manual_only=true`;
- generic `v7-second-canary-target-readiness` rejects `reserve_only=true`;
- an execution-only target is expected to be manual/reserved by governance.

Therefore the next block needs a dedicated execution-target readiness mode or by-id validator that understands `role=EXECUTION_ONLY` instead of relying only on the generic second-canary selector.

