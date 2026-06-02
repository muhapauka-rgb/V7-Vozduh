# PROGRAM A.3 — Eligibility Policy Semantics Forensics, Shadow Redesign And Candidate Recovery

Project: V7 Vozduh  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Mode: shadow analysis only  
Production mutation: none  
Planner/policy/governance mutation: none

## Result

PASS for discovery and shadow analysis.

One proven policy blocker:

`vless` is blocked because the current runtime policy combines untyped `severity_SUSPECT` as a hard eligibility gate with instant-window quality floors as hard candidate disappearance gates. That behavior is faithfully implemented by the planner, but it does not fully match the reconstructed product intent of evidence-based, fail-closed-but-requalifiable routing.

Under current policy, Program A will not succeed.

Under the recommended shadow policy model, the first safe candidate is `vless`, without reservation bypass, governance bypass, manual override, planner override, or fake measurements. This is not permission to execute; it is a policy-change preparation finding.

## Evidence

Evidence folder: `program_a3_evidence`

- `program_a3_evidence/policy_forensics_inventory.md`
- `program_a3_evidence/duplication_audit.md`
- `program_a3_evidence/theory_matrix.md`
- `program_a3_evidence/shadow_replay.json`
- Source runtime data: `program_a2_evidence/a2_final_forensics_summary.json`
- Source before/after data: `program_a2_evidence/a2_eligibility_before_after_summary.json`

## Policy Forensics

The authoritative runtime movement planner is `tools/v7-users-autoswitch`.

Runtime policy defaults:

| Policy | Value | Location | Actual behavior |
|---|---:|---|---|
| `min_avg_mbps` | `15.0` | `tools/v7-users-autoswitch:52-57` | Hard eligibility gate |
| `min_floor_mbps` | `10.0` | `tools/v7-users-autoswitch:52-57` | Hard eligibility gate |
| `min_stability` | `0.45` | `tools/v7-users-autoswitch:52-57` | Hard eligibility gate when nonzero |
| `min_score_improvement_pct` | `0.20` | `tools/v7-users-autoswitch:42-50` | Migration threshold after eligibility |
| `min_score_delta` | `50.0` | `tools/v7-users-autoswitch:42-50` | Migration threshold after eligibility |

Execution path:

- `tools/v7-users-autoswitch:1315-1324` runs hard gates before scoring.
- `tools/v7-users-autoswitch:1324-1328` returns blocked candidates before score calculation.
- `tools/v7-users-autoswitch:1407-1417` applies quality floors as hard blocks.
- `tools/v7-users-autoswitch:1334-1345` hard-blocks severity outside `OK/WARN`.
- `tools/v7-users-autoswitch:1352-1359` hard-blocks non-current `canary_reserved`.
- `tools/v7-users-autoswitch:1454-1483` hard-blocks Telegram hard-down and route-class `FAIL`.
- `tools/v7-users-autoswitch:1618-1621` applies improvement thresholds only after an eligible candidate exists.

Admin/config locations mirror the same defaults:

- `admin/v7-admin-api:458-464`
- `admin/v7-admin-api:15659-15663`

Important semantic drift:

- Runtime autoswitch treats `SUSPECT` as a hard gate.
- Admin route scoring penalizes non-OK/WARN severity instead of hard-blocking it (`admin/v7-admin-api:15905-15913`).

## Product Intent Reconstructed

The intended product model is:

1. Never move users to broken, service-failing, reserved, manual-only, or governance-blocked channels.
2. Require meaningful improvement for planned movement.
3. Keep every movement under approval, restore barrier, audit, runtime recheck, and rollback controls.
4. Treat capacity as a forward admission gate, requalifiable only through evidence.
5. Fail closed when runtime truth is unknown.

The intent is not "pick the fastest raw channel." The intent also does not appear to be "permanently hide a channel when a protocol-specific checker cannot produce a WireGuard-style handshake signal." Prior reports show capacity and readiness can be requalified when evidence proves the previous metadata did not represent physical truth.

## Gate-By-Gate Starvation Map

Canonical A.2 planner summary:

- `users_total=18`
- `egress_total=7`
- `healthy_egress_total=0`
- `candidate_moves=0`
- `selected_moves=0`

| Candidate | First canonical blocker | Final blockers | A.3 conclusion |
|---|---|---|---|
| `1` | `avg_mbps_below_floor` | quality floors, `health_code_000`, route class fail, service critical fail, `severity_FAIL`, Telegram down | genuinely unsafe |
| `openvpn-1779388847-d2ad7c` | `avg_mbps_below_floor` | quality floors, `health_code_000`, route class fail, service critical fail, `severity_FAIL`, Telegram down | genuinely unsafe |
| `awg0` | `avg_mbps_below_floor` | avg/min floors | genuinely too weak; raw probe also failed |
| `awg3` | `avg_mbps_below_floor` | avg/min floors | genuinely too weak; raw probe also failed |
| `amneziawg-exec-20260528-10-8-1-14` | `avg_mbps_below_floor` | quality floors, `manual_only`, `reserve_only`, `canary_reserved` | intentionally not production-assignable |
| `wireguard-1779454504-c43409` | `avg_mbps_below_floor` | quality floors, `canary_reserved` | strong raw probe, but reservation blocks production assignment correctly |
| `vless` | `min_mbps_below_floor` | `min_mbps_below_floor`, `severity_SUSPECT`, `stability_below_floor` | policy semantics blocker; not proven unsafe |

## Theory Matrix

| Theory | Verdict |
|---|---|
| Current policy is correct and channels are genuinely unusable | Partially true; several channels are genuinely unusable, but `vless` is not proven unusable |
| Quality floors are used as eligibility floors when they should be migration thresholds | Proven true for current runtime implementation |
| Min/avg/stability floors are too aggressive | Partially true; true for `vless` semantics, false for weak AWG channels |
| Severity model is too aggressive | Proven true for protocol-specific VLESS `SUSPECT` |
| Canary reservation blocks the only viable candidate | False; it blocks WireGuard, but `vless` becomes viable under recommended policy |
| Multiple gates combine into candidate starvation | Proven true |
| Planner correct but policy wrong | Planner behavior correct; policy semantics need redesign |
| Policy correct but measurements misleading | Partially true; measurement interpretation is misleading for `vless` only |
| Admin/runtime severity semantics drift | True; admin scoring soft-penalizes where runtime hard-blocks |

## Shadow Models

All models are offline replay only. No runtime selected moves were generated.

| Model | Description | Eligible candidates | Shadow selected moves | Safety impact |
|---|---|---:|---:|---|
| A | Current policy | none | 0 | Lowest false-positive risk, guaranteed starvation |
| B | Hard floor plus relative improvement, severity still hard | none | 0 | Still starves because `vless` remains `SUSPECT` |
| C | Soft quality scoring, hard reservation/service gates | `vless`, `awg0`, `awg3` | 1 | Too permissive; admits weak AWG channels |
| D | Conservative hybrid | `vless` | 1 | Good safety balance; typed VLESS exception plus raw/1h evidence |
| E | Best-fit product intent | `vless` | 1 | Recommended; hard governance/safety plus evidence-certified quality semantics |

Shadow replay source: `program_a3_evidence/shadow_replay.json`.

Important: the shadow selected move is an offline one-user feasibility result. It is not an approval packet, not a canonical planner output, and not an execution instruction.

## First Safe Executable Candidate Analysis

The first safe candidate appears under Models D and E:

- Candidate: `vless`
- Current canonical avg: `38.7373 Mbps`
- Current canonical min: `6.82 Mbps`
- One-hour avg: `37.242 Mbps`
- One-hour min: `16.25 Mbps`
- Raw targeted benchmark: `99.86 Mbps`, ok run
- Telegram: OK
- Service matrix: WARN, not FAIL
- Reservation: not reserved
- Manual-only: no
- Reserve-only: no
- Health code: `200`
- Severity: `SUSPECT`
- Diagnose reason: `handshake_unsupported_for_protocol_vless`

Why this is not a bypass:

- It does not use the reserved WireGuard candidate.
- It does not ignore governance.
- It does not override planner output by hand.
- It does not fake measurements.
- It does not move users.
- It proposes that planner policy should learn typed severity and evidence-backed quality semantics before any future execution.

## Safety Analysis

Model A is safe but operationally starves the pool.

Model B is safer than C but still does not solve the real blocker because it leaves all `SUSPECT` diagnostics as fatal.

Model C is too broad. It allows `awg0` and `awg3`, even though A.2 raw probes show `1.53 Mbps` and `0.73 Mbps` failing runs. This model has unacceptable bad migration risk.

Model D is acceptable as a conservative design: keep hard health, service, reservation, manual, and governance blocks; allow only typed diagnostic exceptions with fresh raw proof and one-hour quality support.

Model E is the recommended product policy: preserve all hard safety/governance gates, split diagnostic severity into typed categories, and allow quality floor exceptions only when canonical long-window and fresh raw evidence both prove the instant floor failure is not representative.

## Recommended Policy

Do not implement in A.3.

Recommended policy semantics:

1. Keep hard blocks for `health_code != 200`, `severity_FAIL`, Telegram hard-down, route-class `FAIL`, service multiple critical failure, `manual_only`, `reserve_only`, `execution_reserved`, `canary_reserved`, and explicit production assignment denial.
2. Split `SUSPECT` into typed categories:
   - fatal suspect: hard block;
   - protocol-diagnostic-limited suspect: conditional warning when the protocol cannot supply the checker signal.
3. Treat quality floors as hard gates only when the measurement window is representative.
4. Add an evidence-backed exception for protocol-diagnostic-limited candidates:
   - fresh raw benchmark pass;
   - one-hour average above floor;
   - one-hour minimum above or near safety floor;
   - no Telegram hard-down;
   - no route/service `FAIL`;
   - no reservation/manual/governance block.
5. Keep migration thresholds separate from eligibility:
   - after eligibility, planned movement still requires score improvement and selected-move governance.
6. Emit explicit candidate reasons:
   - `typed_suspect_protocol_limited_warning`
   - `quality_floor_overridden_by_fresh_raw_and_1h_evidence`
   - `quality_floor_hard_block_representative_failure`

## Program A Readiness

Would Program A succeed under current policy?

No. Current policy produces:

- `candidate_moves=0`
- `selected_moves=0`
- `healthy_egress_total=0`

Would Program A succeed under recommended policy?

Likely yes for planning, because `vless` becomes the first non-reserved safe candidate in shadow replay. Real execution would still require:

- policy change implementation;
- tests;
- deployment through convergence gate;
- fresh runtime read-only recheck;
- fresh canonical planner run;
- fresh approval packet;
- fresh restore barrier;
- execution-time recheck;
- rollback plan and audit path verification.

## Final Verdicts

policy_semantics_understood=true

product_intent_understood=true

candidate_starvation_explained=true

all_theories_tested=true

shadow_models_tested=true

safe_candidate_exists_under_current_policy=false

safe_candidate_exists_under_recommended_policy=true

current_policy_matches_product_intent=false

recommended_policy_defined=true

safe_to_prepare_policy_change=true

## Non-Goals Confirmed

No production change was made.

No planner change was made.

No policy change was made.

No governance change was made.

No service restart, deploy, autoswitch apply, cleanup, deletion, routing mutation, or user movement was performed.

