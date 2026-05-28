# E24.1 E24 Execution Readiness Recheck

## E24 Packet Inputs Rechecked

E24 packet:

- candidate user: `10.7.0.11`
- selected target: `wireguard-1779454504-c43409`
- rollback target: `1`
- movement budget: `1`

Current live state after E24.1 deploy:

- candidate still on `1`: YES
- WireGuard target ready by helper: YES
- WireGuard target zero-user: YES
- WireGuard target reserved: YES
- selected_moves=0: YES
- hidden movers absent: YES
- runtime checkers OK: YES
- users registry hash unchanged: YES
- egress registry hash unchanged: YES

## Runtime/Repo Convergence Status

Resolved:

- `v7-second-canary-target-readiness` now available on VPS.
- `v7-second-canary-target-readiness` output is live-runtime based.
- `v7-restore-settle-gate` now available on VPS.

Not fully resolved:

- `v7-restore-settle-gate --pre-restore` default output on VPS is not live-runtime based.
- `v7-restore-settle-gate --pre-restore --state-dir /opt/v7/egress/state` is only `CONDITIONAL` because it has `sample_count=1<3` and `apply_timer_intervals_covered=0.00<2`.
- The only runtime sample source detected is `/opt/v7/egress/state/path-samples.json`, mtime `2026-05-21T21:41Z`, which is not an E24/E25 fresh restore-settle sample set.

## E25 Readiness Classification

Classification:

- `CONDITIONAL_REQUIRES_FRESH_RESTORE_SETTLE_SAMPLE_WINDOW`

Answers:

- `runtime_repo_convergence_sufficient_for_approval_packet=true`
- `runtime_repo_convergence_sufficient_for_execution_next=false`
- `e24_packet_still_valid=true`
- `e25_execution_packet_ready=false`

## Required Before E25

Before first operator-driven bounded user movement execution:

1. Generate a fresh restore-settle sample set that satisfies `v7-restore-settle-gate` semantics.
2. Run:
   - `v7-restore-settle-gate --pre-restore --state-dir <fresh-sample-dir> --pretty`
   - `v7-restore-settle-gate --pre-restore --state-dir <fresh-sample-dir> --json`
3. Require:
   - `gate_status=GO`
   - `sample_count>=3`
   - `apply_timer_intervals_covered>=2`
   - `selected_moves_by_sample` all zero
   - `hidden_movers_observed=false`
   - `checkers_ok=true`
4. Refresh E24 approval packet hashes if runtime registries change before E25.

No user movement is allowed until this gate is fresh and GO.
