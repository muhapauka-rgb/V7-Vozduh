# PROGRAM TRUST CALIBRATION, OPERATOR CALIBRATION AND TRUSTED STATE CERTIFICATION REPORT

Project: V7 Vozduh

Workspace: /Users/ponch/Documents/New project

Branch: Updatesystem

Program status: PASS

Evidence folder: trust_calibration_operator_certification_evidence/

Implementation commit: 76307a2dae868f5a84787d59d0487a6df0233218

## 1. Production Truth Snapshot

Production truth was collected from the current runtime state before changing trust logic.

Initial convergence context:

- local and GitHub were aligned on the documentation-only report commit before this program.
- production was on the latest deployable code commit from the previous channel-state program.
- convergence classified that as DOCS_ONLY_MISMATCH / no deploy-required before this program.

After implementation and safe deploy:

- truth-check final verdict: PASS
- convergence status: ALIGNED
- runtime action status: READY_FOR_RUNTIME_ACTION
- local commit: 76307a2dae868f5a84787d59d0487a6df0233218
- GitHub commit: 76307a2dae868f5a84787d59d0487a6df0233218
- production commit: 76307a2dae868f5a84787d59d0487a6df0233218
- runtime access status: READY
- runtime truth status: KNOWN
- state truth status: KNOWN

Evidence:

- trust_calibration_operator_certification_evidence/pre_truth_check.json
- trust_calibration_operator_certification_evidence/pre_convergence_status.json
- trust_calibration_operator_certification_evidence/post_deploy_truth_check.json
- trust_calibration_operator_certification_evidence/post_deploy_convergence_status.json

## 2. Transition Audit

The audit found that the prior trust model kept production-proven healthy channels in WATCH because successful channel arrivals from switch history were not counted as positive channel feedback.

Before calibration:

- channel_count=7
- WATCH=5
- QUARANTINED=2
- TRUSTED=0

After calibration against production evidence:

- channel_count=7
- TRUSTED=5
- QUARANTINED=2
- WATCH=0

Validated transitions:

- vless: WATCH -> TRUSTED
- awg0: WATCH -> TRUSTED
- awg3: WATCH -> TRUSTED
- amneziawg-exec-20260528-10-8-1-14: WATCH -> TRUSTED
- wireguard-1779454504-c43409: WATCH -> TRUSTED

Validated non-transitions:

- 1 remained QUARANTINED because current service score remained very low and hard service gaps remained present.
- openvpn-1779388847-d2ad7c remained QUARANTINED because current service score remained very low and hard service gaps remained present.

Evidence:

- trust_calibration_operator_certification_evidence/production_trust_inputs.json
- trust_calibration_operator_certification_evidence/local_recalibrated_production_trust_snapshot.json
- trust_calibration_operator_certification_evidence/calibration_transition_audit.json

## 3. Calibration Decision

The calibration was justified.

The previous model treated only a narrow class of normalized feedback as success evidence. Production history also contains successful channel arrivals through switch history records, including autoswitch rebalance, autoswitch failover, manual switch, and admin manual switch events.

The safe correction was to count channel-arrival switch-history records as successful channel feedback when:

- the record has a channel target;
- the record is a switch/failover/rebalance/manual-arrival event;
- the record is not a rollback event;
- normalized outcome evidence does not already provide a more explicit result.

Rollback switch-history records remain excluded from positive success counts and continue to count through rollback evidence.

This is advisory-only trust calibration. It does not change planner ownership, governance ownership, execution ownership, rollback ownership, routing mutation behavior, user movement, or autoswitch apply behavior.

Files changed:

- admin_core/intelligence_workers.py
- admin_core/operator_decision_surface.py
- tests/unit/test_channel_trust_recovery.py

Evidence:

- trust_calibration_operator_certification_evidence/implementation_diff.patch

## 4. Watch State Review

WATCH remains valid as a transitional state.

The program did not remove or weaken WATCH. It corrected the input path that prevented proven successful channel-arrival history from moving stable channels from WATCH to TRUSTED.

Validated semantics:

- WATCH remains appropriate for incomplete positive evidence, mixed evidence, or insufficient confidence.
- TRUSTED now requires high current score plus successful channel feedback.
- QUARANTINED remains dominant over success history when hard service gaps or very low current quality are present.

## 5. Recovery Model Review

The recovery model remains valid.

The calibration did not force degraded or quarantined channels into normal use. Production validation confirmed that channels with hard service gaps remained QUARANTINED even when some history contained successful arrivals.

This means the trust model now distinguishes:

- healthy channel with positive channel feedback -> TRUSTED
- channel with hard service gap or very low current quality -> QUARANTINED

Production examples:

- vless: TRUSTED, trust_score=78.959
- awg0: TRUSTED, trust_score=86.046
- awg3: TRUSTED, trust_score=86.09
- 1: QUARANTINED, trust_score=37.996
- openvpn-1779388847-d2ad7c: QUARANTINED, trust_score=31.196

Evidence:

- trust_calibration_operator_certification_evidence/production_validation_after.json

## 6. Operator Explainability Review

Operator-facing copy was updated so the admin surface explains TRUSTED using positive channel feedback rather than a narrower "governed feedback" phrase.

Production validation confirmed that the operator decision surface is preview-only and does not allow execution from trust state alone.

Production validation:

- surface_preview_only=true
- execution_allowed_now=false

Operator examples:

- vless: TRUSTED, safe_now="Yes, within existing planner and governance limits."
- awg0: TRUSTED, safe_now="Yes, within existing planner and governance limits."
- awg3: TRUSTED, safe_now="Yes, within existing planner and governance limits."
- 1: QUARANTINED, safe_now="No."
- openvpn-1779388847-d2ad7c: QUARANTINED, safe_now="No."

This confirms that trust explainability remains an operator advisory surface, not an execution authority.

## 7. Tests

Validation completed:

- py_compile: PASS
- targeted channel trust/recovery tests: PASS, 43 tests
- full unittest suite: PASS, 382 tests

New tests prove:

- switch-history channel arrival counts as successful channel feedback;
- rollback switch-history does not count as successful channel feedback;
- TRUSTED reason is emitted as high_score_with_successful_channel_feedback;
- existing recovery and quarantine semantics remain intact.

Evidence:

- trust_calibration_operator_certification_evidence/py_compile.txt
- trust_calibration_operator_certification_evidence/targeted_tests.txt
- trust_calibration_operator_certification_evidence/full_unittest.txt

## 8. Deploy And Production Validation

Safe deploy was executed through the approved V7 safe deploy path.

Safe deploy result:

- final_verdict=PASS
- deploy_id=deploy-z8-14-Updatesystem-76307a2-20260608T001658
- deployed commit=76307a2dae868f5a84787d59d0487a6df0233218
- blockers=[]

Post-deploy snapshot refresh:

- snapshot_count=11
- source_stable=true
- warnings=[]
- runtime_behavior_changed=false
- governance_behavior_changed=false
- users_moved=false

Important boundary:

- safe deploy was run.
- autoswitch apply was not run.
- no users were moved.
- no routing mutation was performed by this program.

Evidence:

- trust_calibration_operator_certification_evidence/safe_deploy.json
- trust_calibration_operator_certification_evidence/production_snapshot_refresh_after.json
- trust_calibration_operator_certification_evidence/production_validation_after.json

## 9. Certification

The calibration is certified.

Reason:

The old WATCH result for healthy channels was not a real production warning. It was a feedback interpretation gap. Production switch history already contained successful channel arrivals that should count as positive channel feedback. After calibration, healthy production channels become TRUSTED while truly unhealthy channels remain QUARANTINED.

No duplicate trust system was created.

No duplicate recovery model was created.

No duplicate explainability system was created.

No duplicate truth source was created.

The existing channel trust/recovery/explainability architecture was extended in place.

## 10. Final Verdicts

trust_snapshot_complete=true

transition_audit_complete=true

trust_calibrated=true

watch_state_validated=true

recovery_model_validated=true

operator_explainability_validated=true

operator_calibration_complete=true

tests_pass=true

deploy_pass=true

production_validation_complete=true

trust_calibration_certified=true

recovery_model_certified=true

operator_explainability_certified=true

routing_behavior_changed=false

users_moved=0

apply_executed=false

SAFE_NEXT_STEP=GOVERNED_EXECUTION_LOOP_READINESS_REVIEW

