# BLOCK E25.3 — WireGuard Target Stability Recovery or Retargeting for First Movement Report

## Verdict

`e25_3_completed=true`

E25.3 found that `wireguard-1779454504-c43409` is not permanently broken, but it is quality-spiky. It failed E25.2 execution-time readiness with fresh low quality metrics, then recovered and held 16 consecutive GO samples across a 15-minute observation window.

The governance layer is valid. The execution-time readiness gate correctly prevented unsafe movement. The remaining blocker is target quality stability, not operator execution governance.

## Final Answers

- `runtime_mutation_performed=false`
- `user_movement_performed=false`
- `routing_mutation_performed=false`
- `candidate_user=10.7.0.11`
- `current_wireguard_target=wireguard-1779454504-c43409`
- `wireguard_target_structurally_stable=false`
- `wireguard_target_temporarily_unstable=true`
- `wireguard_target_unsuitable_for_first_movement=true`
- `readiness_gate_correct=true`
- `helper_false_no_go=false`
- `metrics_stale=false`
- `measurement_noise_detected=false`
- `real_network_degradation_detected=true`
- `best_first_movement_target=wireguard-1779454504-c43409_CONDITIONAL`
- `dedicated_execution_egress_required=true`
- `governance_layer_valid=true`
- `unsafe_mutation_prevented=true`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
- `runtime_checkers_ok=true`
- `recommended_next_block=E25_4_DEDICATED_EXECUTION_EGRESS_PREPARATION`

## Evidence Artifacts

- `docs/track7/productization/e25_3-evidence/wg-long-window-raw.log`
- `docs/track7/productization/e25_3-evidence/wg-long-window-observation.md`
- `docs/track7/productization/e25_3-evidence/metric-source-investigation.md`
- `docs/track7/productization/e25_3-evidence/network-quality-investigation.md`
- `docs/track7/productization/e25_3-evidence/target-comparison-matrix.md`
- `docs/track7/productization/e25_3-evidence/governance-safety-review.md`
- `docs/track7/productization/e25_3-evidence/recovery-or-retarget-decision.md`
- `docs/track7/productization/e25_3-evidence/tests.md`

## Long Window Observation

Window:

- start: `2026-05-28T11:15:00Z`
- end: `2026-05-28T11:30:08Z`
- samples: `16`

Results:

- GO samples: `16`
- NO-GO samples: `0`
- `min_mbps` range: `16.81` to `19.54`
- `stability` range: `0.655310` to `0.771378`
- target remained zero-user
- diagnose stayed OK
- load stayed OK
- hidden movers absent

This proves recovery after the E25.2 abort, but not structural stability.

## E25.2 Failure Context

E25.2 fresh execution-time readiness failed with:

- `min_mbps=4.61`
- `stability≈0.30`
- helper verdict: `NO-GO`
- selected target: `NONE`

The source files were fresh, and quality summary also showed a degraded short window:

- 5m `min_mbps=8.895`
- 5m `stability=0.4104`
- trend `degrading`

The NO-GO was valid.

## Metric Source Review

`v7-second-canary-target-readiness` uses:

1. `egress-stability.state` if present.
2. `stability.state` if present.
3. `egress-quality-summary.json` only as fallback.

In this runtime, `stability.state` exists and is authoritative for movement-critical readiness.

Thresholds:

- `avg_mbps >= 15.0`
- `min_mbps >= 10.0`
- `stability >= 0.45`

No threshold weakening is justified. The helper is strict, but correct.

## Network Quality Classification

Classification:

`TARGET_GENERALLY_OK_BUT_SPIKY`

Evidence:

- E25.2: fresh short-window degradation below movement floors.
- E25.3: 15-minute recovery window with all samples GO.
- Interface counters showed no RX/TX errors or drops in sampled output.
- WireGuard handshakes remained regular.

Not proven:

- packet loss root cause
- provider throttling root cause
- MTU/MSS fault

## Target Comparison

Latest comparison:

- `wireguard-1779454504-c43409`: only existing target that can satisfy all gates when quality is above floor; spiky history.
- `openvpn-1779388847-d2ad7c`: zero-user but diagnose SUSPECT/interface unknown.
- `awg0`: occupied, HARD_FULL, route exclusions missing, quality below floor in final check.
- `awg3`: occupied, HARD_FULL, route exclusions missing, quality below floor in final check.
- `vless`: diagnose SUSPECT, load nonzero, exclusions missing.

No existing alternate target is cleaner than WireGuard.

## Decision

Primary decision:

`OPTION_C: CREATE_DEDICATED_EXECUTION_ONLY_EGRESS`

Secondary conditional path:

`OPTION_A: WAIT_AND_RECOVER_CURRENT_WG_TARGET`

The current WireGuard target may be used only if the next execution block requires a fresh sustained GO window immediately before movement and still performs the final execution-time recheck.

## Governance Safety Review

The governance layer did exactly what it should:

- E25 aborted before mutation on stale/unsafe gates.
- E25.1 refreshed the packet without movement.
- E25.2 aborted before mutation on fresh target NO-GO.
- E25.3 remained read-only.

Final runtime safety:

- `10.7.0.11` remained on `1`.
- WireGuard target remained zero-user.
- `selected_moves=0`.
- hidden movers absent.
- runtime checkers OK.
- registry hashes unchanged.

## Test Summary

- `py_compile`: PASS.
- targeted helper/operator tests: PASS, `26 tests`.
- full unittest discovery: PASS, `116 tests`.
- target readiness helper: PASS.
- restore-settle helper: PASS.
- runtime checkers: PASS.
- hidden mover scan: PASS.
- credential scan: PASS.
- dangerous-call scan: PASS with expected negative/doc-only matches.
- `git diff --check`: PASS.

## Recommended Next Block

Preferred:

`E25_4_DEDICATED_EXECUTION_EGRESS_PREPARATION`

Purpose:

- prepare a dedicated zero-user execution egress,
- prove a longer stable readiness window,
- avoid first-movement dependency on a spiky shared candidate.

Allowed conditional alternative:

`E25_4_FIRST_MOVEMENT_WITH_RECOVERED_TARGET`

Required gates:

- fresh 15-30 minute sustained GO window,
- no sample below quality floor,
- target readiness GO immediately before execution,
- restore-settle GO,
- selected_moves=0,
- hidden movers absent,
- runtime checkers OK.

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
