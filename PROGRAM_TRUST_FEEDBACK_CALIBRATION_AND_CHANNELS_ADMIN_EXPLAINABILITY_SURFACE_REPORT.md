# PROGRAM TRUST FEEDBACK CALIBRATION AND CHANNELS ADMIN EXPLAINABILITY SURFACE REPORT

Project: V7 Vozduh
Branch: Updatesystem
Date: 2026-06-07

## Mission Result

Channel trust/recovery calibration was implemented and surfaced in the existing admin Channels/Egress table.

No duplicate admin page was created.
No routing behavior was changed.
No users were moved.
No autoswitch apply was run.
No autonomy was enabled.
No planner, governance, execution, health, or truth owner was replaced.

## ADMIN_CHANNEL_SURFACE_AUDIT

Existing admin surface found and reused:

- Channels tab: `#tab-channels`
- Existing channels table: `#channelsTableV2`
- Existing column system: `CHANNEL_TABLE_COLUMN_DEFS`
- Existing channel state column id: `channel_state`
- Existing click handler: `openChannelStateDrawer`
- Existing API source: `/api/operator/decision-surface`
- Existing backend owner: `admin_core/operator_decision_surface.py`

Decision:

- REUSE existing Channels/Egress table
- EXTEND existing `channel_state` column
- EXTEND existing `openChannelStateDrawer`
- EXTEND existing `channels_by_id` API payload
- DO NOT create a duplicate UI or API truth source

## TRUST_CALIBRATION_AUDIT

Previous issue:

Production channels were mostly `NEW` because the first trust model required stronger positive channel feedback before considering a channel usable/trust-progressing.

Root cause:

`NEW` was doing too much. It represented both "insufficient positive governed history" and "not enough evidence", even when current service health was good.

Fix:

Healthy current channels without successful governed feedback now classify as `WATCH`, not `NEW`.

`TRUSTED` still requires current strength plus successful governed feedback. This avoids fake trust while preventing healthy channels from looking uninitialized forever.

## TIME_WINDOW_CALIBRATION

Practical windows defined in `CHANNEL_TRUST_TIME_WINDOWS`:

- Current Health: `5-15 minutes`
- Recent Stability: `6-24 hours`
- Initial Recovery: `24-72 hours`
- Trusted Window: up to `7 days`
- Maximum practical trust window: `7 days`

The model no longer implies that a channel needs a month of clean behavior before it can become trusted.

## STATE_EXPLANATION_MODEL

States exposed:

- `NEW`
- `TRUSTED`
- `WATCH`
- `DEGRADED`
- `RECOVERING`
- `QUARANTINED`

Each state now has:

- operator label
- short reason
- simple explanation
- safe-now text
- next step
- source owner

The explanation avoids raw metric dumps by default.

## API_EXTENSION_REPORT

Extended existing `channels_by_id` rows from `/api/operator/decision-surface`.

Added:

- `channel_state`
- `channel_state_label`
- `channel_state_reason_short`
- `channel_state_explanation`
- `channel_state_next_step`
- `channel_state_safe_now`
- `channel_state_source`
- `channel_state_policy`
- `channel_state_evidence_summary`
- `channel_state_raw_reason`

Compatibility preserved:

- existing `state`
- existing `state_reason`

## ADMIN_UI_IMPLEMENTATION_REPORT

Updated existing admin Channels/Egress table:

- Column label is now `Channel State`
- The column uses the existing `channel_state` id
- Clicking the state opens the existing channel state drawer
- Drawer answers:
  - Why this state?
  - What happened?
  - Is the channel safe now?
  - What must happen for recovery/trust?

No duplicate page, tab, table, modal system, or drawer system was added.

## TEST_REPORT

Validation:

- `py_compile`: PASS
- targeted tests: PASS, 41 tests
- full suite: PASS, 380 tests

Added/updated tests:

- trust calibration
- `WATCH` for healthy channels without success history
- maximum trust window = 7 days
- channel state API fields
- human-readable explanation text
- admin rendering smoke for existing column and drawer

## DEPLOY_REPORT

Implementation commit:

`303b014ecad95df5e35918021fc8dcd5b207e60b`

Deployment:

- safe deploy: PASS
- truth-check: PASS
- convergence-status: PASS

Final alignment:

- local: `303b014ecad95df5e35918021fc8dcd5b207e60b`
- GitHub: `303b014ecad95df5e35918021fc8dcd5b207e60b`
- production: `303b014ecad95df5e35918021fc8dcd5b207e60b`
- runtime action status: `READY_FOR_RUNTIME_ACTION`

## PRODUCTION_VALIDATION

Production snapshot refresh:

- snapshot_count: 11
- source_stable: true
- runtime_behavior_changed: false
- governance_behavior_changed: false
- users_moved: false
- warnings: []

Production channel API validation:

| Channel | State | Operator meaning |
| --- | --- | --- |
| `vless` | `WATCH` | Works now, needs more successful governed history before TRUSTED |
| `awg0` | `WATCH` | Works now, needs more successful governed history before TRUSTED |
| `awg3` | `WATCH` | Works now, needs more successful governed history before TRUSTED |
| `1` | `QUARANTINED` | Hard negative service/trust evidence |
| `openvpn-1779388847-d2ad7c` | `QUARANTINED` | Hard negative service/trust evidence |

Production admin UI validation:

- deployed `v7-admin-api` contains `Channel State`
- deployed `v7-admin-api` contains `openChannelStateDrawer`
- deployed `v7-admin-api` contains `channel_state_explanation`
- deployed `v7-admin-api` contains `channel_state_next_step`

External public API check returned `unauthorized`, so production API payload was validated read-only through the deployed backend module using production registries and snapshots.

## Evidence

Evidence folder:

`trust_feedback_calibration_admin_surface_evidence/`

Key evidence:

- `implementation_diff.patch`
- `py_compile.txt`
- `targeted_tests.txt`
- `full_unittest.txt`
- `local_snapshot_refresh_dry_run.json`
- `calibrated_watch_sample.json`
- `safe_deploy.json`
- `post_deploy_truth_check.json`
- `post_deploy_convergence_status.json`
- `production_snapshot_refresh.json`
- `production_channel_state_api_summary.json`
- `production_admin_binary_ui_probe.txt`
- `git_ls_remote_updatesystem.txt`

## Final Verdicts

admin_surface_audited=true

existing_ui_reused=true

trust_calibrated=true

max_trust_window_days=7

channel_state_api_added=true

channel_state_admin_column_added=true

state_click_explanation_added=true

explanations_human_readable=true

tests_pass=true

deploy_pass=true

production_validation_complete=true

routing_behavior_changed=false

users_moved=0

apply_executed=false

SAFE_NEXT_STEP=TRUSTED_STATE_EVIDENCE_ACCUMULATION_AND_OPERATOR_CALIBRATION_REVIEW
