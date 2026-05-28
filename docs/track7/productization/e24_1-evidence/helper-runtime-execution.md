# E24.1 Helper Runtime Execution

Executed on VPS after bounded deploy.

## `v7-second-canary-target-readiness --pretty`

Key output:

- `runtime_commands_executed=False`
- `candidate_user=10.7.0.11`
- `candidate_still_valid=True`
- `current_egress=1`
- `selected_target=wireguard-1779454504-c43409`
- `approval_status=GO`
- `second_canary_readiness=GO`
- `zero_user_targets=openvpn-1779388847-d2ad7c,wireguard-1779454504-c43409`
- `execution_allowed_now=False`

WireGuard target row:

- `egress_id=wireguard-1779454504-c43409`
- `status=GO`
- `zero_user=True`
- `diagnose=OK`
- `avg_mbps=48.9927`
- `min_mbps=46.48`
- `stability=0.948713`
- `reason=ready`

## `v7-second-canary-target-readiness --json`

Key JSON fields:

- `tool=v7-second-canary-target-readiness`
- `state_dir=/opt/v7/egress/state`
- `read_only=true`
- `mutation=false`
- `runtime_commands_executed=false`
- `forbidden_commands_called=false`
- `candidate_still_valid=true`
- `selected_target=wireguard-1779454504-c43409`
- `approval_status=GO`
- `second_canary_readiness=GO`
- `execution_allowed_now=false`

Verdict:

- Live-runtime based: YES.
- Current output usable for target readiness: YES.

## `v7-restore-settle-gate --pre-restore --pretty`

Default output on VPS:

- `runtime_commands_executed=False`
- `mode=pre-restore`
- `gate_status=NO-GO`
- `sample_count=0`
- `required_samples=3`
- `apply_timer_intervals_covered=0.0`
- `required_apply_timer_intervals=2`
- `checkers_ok=False`
- `recommended_action=no_go_review_restore_settle_evidence`
- `execution_allowed_now=False`

Reasons:

- `sample_count_below_required:0<3`
- `apply_timer_intervals_below_required:0.00<2`
- `runtime_checker_failure_observed`

Default state dir resolved to:

- `docs/track7/control-plane/e11_13-evidence/restore-settle-samples`

VPS does not have this repo evidence directory, so the default run is not a usable live settle verdict.

## `v7-restore-settle-gate --pre-restore --state-dir /opt/v7/egress/state --pretty`

Explicit runtime-state output:

- `runtime_commands_executed=False`
- `mode=pre-restore`
- `gate_status=CONDITIONAL`
- `sample_count=1`
- `required_samples=3`
- `selected_moves_by_sample=[0]`
- `telegram_hard_blocked_by_sample=[False]`
- `egress_1_eligible_by_sample=[True]`
- `movement_count_by_sample=[0]`
- `checkers_ok=True`
- `hidden_movers_observed=False`
- `recommended_action=extend_sampling_window_before_restore_decision`
- `execution_allowed_now=False`

Reason:

- `sample_count_below_required:1<3`
- `apply_timer_intervals_below_required:0.00<2`

Sample source:

- `/opt/v7/egress/state/path-samples.json`

Sample file metadata:

- mode/owner: `-rw-r--r-- root root`
- mtime: `2026-05-21T21:41Z`
- sha256=`48d968204edf7fe7063cee329d081d005be09533bf02e2219fa0f7cef4bd1ab1`
- JSON keys: `history`, `latest`, `schema`, `updated`

Verdict:

- Helper executable availability: YES.
- Helper read-only semantics: YES.
- Default helper output live-runtime based: NO.
- Explicit runtime-state output current enough for E25 GO: NO.
- Restore-settle is not yet E25-execution-sufficient because a fresh 3-sample settle window is missing.
