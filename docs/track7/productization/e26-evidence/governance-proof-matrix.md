# E26 Governance Proof Matrix

| Capability | Status | Evidence | Notes |
|---|---:|---|---|
| Approval packet | Proven | E25.13 packet, E25.15 refreshed packet | Packet bound action, user, target, rollback, registry hashes, selected moves hash, and execution-only target state. |
| Execution-time recheck | Proven | `docs/track7/productization/e25_15-evidence/execution-time-recheck.md` | Recheck authorized only after fresh hash match, target GO, restore-settle GO, selected_moves=0, hidden movers absent, and runtime checkers OK. |
| Blast radius enforcement | Proven | E25.15 forward/rollback verification | Only `10.7.0.11` changed; `10.7.0.16` stayed on `vless`; no other users moved. |
| Replay protection | Proven | E25.15 replay validation | Replayed packet produced `DENY_REPLAY`; no movement and no routing mutation during replay. |
| Rollback | Proven | E25.15 rollback execution and verification | `10.7.0.11` returned to `1`; table `1009` restored to `v7e356a192b79`; target users returned to 0. |
| Delayed movement protection | Proven for one-user case | E25.15 delayed monitoring A/B/C; E26 runtime review | No delayed movement, no out-of-scope movement, selected_moves stayed 0. |
| Restore-settle | Proven | E25.15 post-rollback settle, E26 fresh restore samples | E26 fresh samples returned `gate_status=GO`, `sample_count=3`, `apply_timer_intervals_covered=2.85`. |
| Execution-only target isolation | Proven | E25.11, E25.12, E25.13, E26 runtime review | Target has `role=EXECUTION_ONLY`, `manual_only=1`, `reserve_only=1`, `production_assignment_allowed=false`. |
| Autoswitch exclusion | Proven | E25.11 isolation validation, E26 runtime review | Target metadata has `autoswitch_allowed=false` and `rebalance_allowed=false`; selected_moves remained 0. |
| Governance isolation | Proven for one-user raw-fallback governed execution | E25.15 audit and verification | Movement used approved raw fallback after governance gates; UI execution and autoswitch apply remained disabled/unused. |

## Certification Boundary

The proof covers one-user operator-governed movement with default rollback. It does not certify two-user, cohort, autonomous, or large-scale movement.

