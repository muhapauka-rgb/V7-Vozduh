# V7 Production Lock Scope Validation

Timestamp: 2026-07-02_160511

Mode: Production Validation

## Summary

The Telegram Sentinel lock-scope fix was deployed through the standard safe deployment owner and validated in production.

Production now proves:

- deployed `/usr/local/bin/v7-telegram-sentinel` hash matches local fixed binary;
- natural `v7-telegram-sentinel.timer` executions emit `held_sec`, `waited_sec`, and `released`;
- sentinel writer-lock hold time is now milliseconds, not seconds;
- Telegram probes still produce real service results;
- `openvpn-1779388847-d2ad7c` remains a real failed/blocked egress for Telegram.

Production did not prove end-to-end rollback disappearance because the governed L3 validation did not reach Runtime Apply or Verification. The validation stopped before apply with:

```text
terminal_reason = approved_plan_lock_selected_moves_missing
execution_blocker = emergency_failover_autonomy
l3_wake_decision = REJECT_WAKE
verification_result = NOT_RUN
users_moved = 0
```

Final verdict:

```text
PARTIALLY_IMPROVED
```

## Deployment

Commit deployed:

```text
04ee8dc8ce54e070ac46b7fd248df0dfc9ec707d
```

Commit message:

```text
Fix telegram sentinel service matrix lock scope
```

Standard owner:

```text
tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --json
```

Deploy result:

```text
final_verdict = PASS
ssh_manifest_refresh.ok = true
```

No Planner, Runtime, Authority, Restore Barrier, service verification, or locking contract was weakened.

## Hash Verification

Local:

```text
f6ae95b7a78c27e088e38e776929d6175e20e0330f4e43c860f62a70104d50ce  tools/v7-telegram-sentinel
```

Production:

```text
f6ae95b7a78c27e088e38e776929d6175e20e0330f4e43c860f62a70104d50ce  /usr/local/bin/v7-telegram-sentinel
```

Verdict:

```text
DEPLOYED_HASH_MATCH
```

## Deployed Version

Production systemd command:

```text
/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

Unit:

```text
/etc/systemd/system/v7-telegram-sentinel.service
```

Drop-in:

```text
/etc/systemd/system/v7-telegram-sentinel.service.d/10-advisory-first.conf
```

Timer:

```text
/etc/systemd/system/v7-telegram-sentinel.timer
OnUnitActiveSec=4s
AccuracySec=1s
```

## Sentinel Production Evidence

Latest captured natural timer payload:

```json
{
  "updated": "2026-07-02T09:02:07.675267+00:00",
  "elapsed_sec": 1.073,
  "held_sec": 0.008,
  "waited_sec": 0.0,
  "released": true,
  "blocked_egress": ["1", "openvpn-1779388847-d2ad7c"],
  "healthy_egress": [
    "amneziawg-exec-20260528-10-8-1-14",
    "awg0",
    "awg3",
    "vless",
    "wireguard-1779454504-c43409"
  ],
  "openvpn_status": "DOWN",
  "openvpn_reason": "api.telegram.org:443=timeout; 149.154.167.50:443=timeout; 149.154.175.50:443=timeout; 91.108.56.177:443=timeout; 194.221.250.50:443=timeout"
}
```

Observed earlier natural payload after deploy:

```text
elapsed_sec = 1.050
held_sec = 0.004
waited_sec = 0.0
released = true
```

One natural payload showed lock wait but still short hold:

```text
elapsed_sec = 7.586
waited_sec = 6.506
held_sec = 0.005
released = true
```

This proves the new instrumentation separates wait time from hold time. It also proves long cycle time or wait time is no longer being misread as writer-lock hold time.

## Required Observations

### Telegram Sentinel

Result:

```text
PASS
```

Measured:

```text
elapsed_sec = 1.073
held_sec = 0.008
waited_sec = 0.0
released = true
```

`held_sec` is significantly smaller than `elapsed_sec`.

### Planner

The governed validation owner produced candidate/selected-move evidence.

Observed in latest execution lease:

```text
operation_id = govexec_914712d4498b61e4e628e431
user = 10.7.0.5
source = awg0
target = vless
selected_move_hash = f9d49842548212334433eb9957674d9e3d08f2a13241e4e0f8413c87f1ddb8ff
source_preview.safety.restore_barrier.approved_plan_lock_validation.reason = approved_plan_lock_valid
source_preview.safety.selected_moves_diagnostics.approved_plan_lock_consumed = true
source_preview.safety.selected_moves_diagnostics.approved_plan_lock_ok = true
source_preview.safety.selected_moves_diagnostics.selected_moves_before_restore_barrier = 1
source_preview.safety.selected_moves_diagnostics.selected_moves_after_gate = 0
```

### Runtime Apply

Result:

```text
NOT_REACHED
```

Latest lease:

```text
apply_executed = false
users_moved = 0
```

### Verification

Result:

```text
NOT_RUN
```

Latest lease:

```text
verification_result = null
```

The previous `v7-service-matrix-test` post-apply verification timeout was not reproduced because Runtime Apply did not execute.

### Rollback

Result:

```text
NOT_REQUIRED / NOT_RUN
```

No user was moved, so no post-apply rollback decision occurred in this validation.

## Questions

### 1. Is `held_sec` now significantly smaller than `elapsed_sec`?

Yes.

Latest payload:

```text
elapsed_sec = 1.073
held_sec = 0.008
```

### 2. Was Verification blocked by `service-matrix.lock`?

No evidence.

Verification did not run.

### 3. Did Verification finish normally?

No.

Verification was not reached.

### 4. Did Telegram probe produce a real result?

Yes.

`openvpn-1779388847-d2ad7c` Telegram probe produced real endpoint timeouts:

```text
api.telegram.org:443=timeout
149.154.167.50:443=timeout
149.154.175.50:443=timeout
91.108.56.177:443=timeout
194.221.250.50:443=timeout
```

Healthy targets such as `vless`, `awg0`, and `awg3` also produced real Telegram results.

### 5. Did `service_verify_rc` become PASS?

Unknown.

Post-apply service verification did not run.

### 6. Did rollback disappear?

No rollback occurred because no Runtime Apply occurred.

This is not proof that rollback disappeared after successful verification.

### 7. If rollback still happened, what exact service failed?

Not applicable.

Rollback did not happen in this validation.

### 8. If timeout still happened, who held the lock?

No post-apply verification timeout happened in this validation.

### 9. Did any writer hold the lock longer than Verification budget?

No evidence from Sentinel.

Sentinel held the lock for milliseconds:

```text
held_sec = 0.004 to 0.008 in captured natural cycles
```

Planner lifecycle lock wait/hold remains a separate writer domain and was not the target of this fix.

### 10. Does production now prove that lock scope was the real root cause?

No.

Production proves the Sentinel lock scope is improved. It does not prove the complete rollback root cause is fixed because the validation stopped before Runtime Apply and Verification.

## Next Proven Blocker

The next blocker is not Sentinel writer-lock hold time.

Persisted latest execution lease shows:

```text
status = OPERATOR_CANCELLED
terminal_reason = approved_plan_lock_selected_moves_missing
apply_executed = false
users_moved = 0
verification_result = null
source_preview.summary.execution_blocker = emergency_failover_autonomy
source_preview.summary.l3_wake_decision = REJECT_WAKE
source_preview.summary.l3_incident_state = INCIDENT_OPEN_STOP_SAFE
source_preview.safety.selected_moves_diagnostics.selected_moves_before_restore_barrier = 1
source_preview.safety.selected_moves_diagnostics.selected_moves_after_gate = 0
```

This means the production validation chain failed before the post-apply verification stage.

## Final Verdict

```text
PARTIALLY_IMPROVED
```

Lock-scope fix is production-visible and materially improved Sentinel behavior. The full root-cause hypothesis is not confirmed because the validation did not reach the stage where the original timeout occurred.
