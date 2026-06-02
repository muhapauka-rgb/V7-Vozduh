# PROGRAM A.B — Service-Aware Policy Remediation, Shadow Validation And Execution Recovery

Project: V7 Vozduh  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Mode: bounded implementation + local shadow validation  
Production deploy: not performed  
Autoswitch apply: not performed  
User movement: not performed

## Result

Local remediation PASS.

Production execution recovery BLOCKED pending explicit approval for runtime-critical safe release sync apply.

Single proven external blocker:

`explicit_user_approval_required_for_runtime_critical_safe_release_sync_apply`

The code now restores `vless` as a safe local shadow candidate under conservative service-aware policy. It does not admit weak AWG channels, does not bypass reservation, does not bypass manual/reserve gates, and does not move users.

## Evidence

Evidence folder: `program_ab_evidence`

- `program_ab_evidence/discovery_duplication_audit.md`
- `program_ab_evidence/test_results.md`
- `program_ab_evidence/shadow_replay_new_policy.json`
- `program_ab_evidence/release_sync_gate.md`

## What Changed In Human Language

V7 no longer treats every speed-floor miss or every `SUSPECT` label as the same kind of fatal truth.

The planner now separates:

1. Real hard safety failures.
2. Protocol diagnostic limitations.
3. Required-service quality.
4. Generic channel quality.
5. Relative movement improvement.

This means V7 can prefer "the channel that works for the user's services" instead of blindly choosing by generic Mbps. Generic speed still matters, but it is not the first truth source.

## What Changed Technically

Changed file:

- `tools/v7-users-autoswitch`

Added:

- service quality policy defaults;
- per-service quality profile metadata for Telegram, YouTube, Instagram, and ChatGPT;
- typed severity classification;
- service suitability scoring from `service-matrix.json`;
- explicit missing-required-service handling;
- contextual quality floor behavior;
- candidate JSON explainability fields:
  - `severity_classification`
  - `service_suitability`
  - `quality_decision`

Added test file:

- `tests/unit/test_service_aware_policy.py`

Preserved:

- hard blocks for `severity_FAIL`;
- canary reservation block;
- `manual_only`;
- `reserve_only`;
- `execution_reserved`;
- production assignment denial;
- Telegram hard-down when required;
- route-class `FAIL`;
- service multiple critical failure;
- relative improvement threshold;
- sticky/current and anti-flap behavior.

## Per-Service Explanation

Telegram:

- Uses existing Telegram sentinel and service matrix data.
- Hard-down remains a hard block when Telegram is required.
- Degraded Telegram remains a warning/penalty.
- Suitability includes availability, latency where present, score, failure samples, and confidence.

YouTube:

- Uses existing service matrix checks.
- A single weak/degraded sample is not automatically fatal unless required-service policy says so.
- Suitability is 0-100, with latency and failures reducing score.
- Weak YouTube evidence can reduce candidate quality without becoming generic Mbps.

Instagram:

- Uses existing service matrix checks.
- Existing behavior is preserved: one degraded sample is penalty-only; persistent failure can block.
- Suitability tracks availability, latency, score, failure samples, and confidence.

ChatGPT:

- Uses existing service catalog/service matrix capability where present.
- Missing ChatGPT evidence is not treated as PASS.
- If ChatGPT is explicitly required and evidence is absent, candidate is blocked with `service_chatgpt_evidence_unknown`.

## Candidate Matrix Before / After

Before A.B, from A.2/A.3:

| Candidate | Current policy result | Main reason |
|---|---|---|
| `1` | blocked | health/service/Telegram/quality failure |
| `openvpn-1779388847-d2ad7c` | blocked | health/service/Telegram/quality failure |
| `awg0` | blocked | avg/min quality floors |
| `awg3` | blocked | avg/min quality floors |
| `amneziawg-exec-20260528-10-8-1-14` | blocked | manual/reserve/canary/quality |
| `wireguard-1779454504-c43409` | blocked | canary reservation plus quality floors |
| `vless` | blocked | `severity_SUSPECT`, min floor, stability floor |

After A.B local shadow replay:

| Candidate | New local shadow result | Reason |
|---|---|---|
| `1` | blocked | real hard safety/service failures remain |
| `openvpn-1779388847-d2ad7c` | blocked | real hard safety/service failures remain |
| `awg0` | blocked | representative avg/min failure remains |
| `awg3` | blocked | representative avg/min failure remains |
| `amneziawg-exec-20260528-10-8-1-14` | blocked | manual/reserve/canary gates remain |
| `wireguard-1779454504-c43409` | blocked | canary reservation remains |
| `vless` | eligible in shadow | typed protocol-limited severity + service/quality evidence |

## Why VLESS Is Allowed In Shadow

`vless` is not allowed because it is fast in raw Mbps.

It is allowed in shadow because:

- health code is `200`;
- severity is classified as `protocol_diagnostic_limited_suspect`;
- diagnose reason is `handshake_unsupported_for_protocol_vless`;
- Telegram is OK;
- route-class status is WARN, not FAIL;
- required service evidence is not missing;
- service suitability aggregate is `76.1`;
- one-hour avg is `37.242 Mbps`;
- one-hour min is `16.25 Mbps`;
- instant min/stability misses are downgraded to contextual warnings;
- no reservation/manual/governance bypass is used.

Shadow replay result:

- `healthy_egress_total=1`
- `candidate_moves_total=15`
- `selected_moves=15` in policy-only dry-run shadow
- terminal reason: `dry_run_selected_moves_available`

This is still dry-run only.

## Why Weak AWG Channels Stay Blocked

`awg0` and `awg3` still fail representative quality:

- canonical avg/min are far below floors;
- one-hour quality remains weak;
- A.2 targeted raw probes were also weak;
- no typed diagnostic exception applies.

They do not become eligible merely because quality floor semantics are softer.

## Why Reserved WireGuard Stays Blocked

`wireguard-1779454504-c43409` remains blocked by `canary_reserved_production_assignment_blocked`.

A.B did not weaken:

- canary reservation;
- production assignment governance;
- current-hold/drain separation.

## Tests Run

Passed:

- `python3 -m unittest tests/unit/test_service_aware_policy.py`
- `python3 -m unittest tests/unit/test_v7_users_autoswitch_policy.py`
- `python3 -m unittest tests/unit/test_v7_truth_check.py`
- `python3 -m unittest tests/unit/test_v7_sync_tools.py`

Total local tests covered in A.B: 60.

## Truth Check Result

Initial pre-change truth check:

- `tools/v7-truth-check --all`
- PASS
- local/GitHub/runtime/state aligned

Post-change truth check:

- NO-GO
- reason: local runtime-critical dirty workspace before commit/deploy
- blockers include `dirty_workspace` and `runtime_critical_dirty`

This is expected after local runtime-critical implementation and before safe release sync apply.

## Release Sync Result

Dry-run:

- commit stage: PASS
- sync tests: PASS
- deployment required: `v7-users-autoswitch` only
- service restart required: false
- safe deploy manifest confirms no autoswitch apply/user movement/routing mutation

Apply:

- Not executed.
- Blocked by sandbox auto-review because production deploy of runtime-critical binary requires explicit user approval.

## Program A Retry Readiness

Program A is not yet safe to retry in production.

Readiness after explicit deploy approval would require:

1. Run `v7-release-sync --apply --confirm RELEASE_SYNC_APPROVED --allow-runtime-critical`.
2. Run `v7-truth-check --all`.
3. Run production planner dry-run only.
4. Confirm service-aware policy active in runtime planner output.
5. Confirm restored candidate and selected move hash.
6. Prepare fresh approval packet.
7. Prepare fresh restore barrier generation clearance.
8. Verify rollback/audit/closure paths.
9. Only then retry Program A.

## Final Verdicts

policy_remediation_implemented=true

service_aware_foundation_implemented=true

typed_severity_implemented=true

quality_floor_semantics_fixed=true

hard_safety_gates_preserved=true

reservation_gates_preserved=true

relative_improvement_preserved=true

tests_pass=true

truth_check_all_pass=false

candidate_restored=true

selected_moves_present=true

safe_to_retry_PROGRAM_A=false

## Blocker

Production deployment and production shadow validation remain blocked until the user explicitly approves runtime-critical safe release sync apply.

