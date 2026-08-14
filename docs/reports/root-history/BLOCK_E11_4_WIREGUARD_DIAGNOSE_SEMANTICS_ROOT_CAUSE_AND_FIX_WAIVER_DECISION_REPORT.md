# BLOCK E11.4 - WireGuard Diagnose Semantics Root-Cause And Fix/Waiver Decision Report

## Summary

```text
block=E11.4
mode=LARGE_READ_ONLY_DIAGNOSE_GOVERNANCE_DECISION
target=wireguard-1779454504-c43409
interface=v7e06a394c478
runtime_mutation_performed=false
canary_performed=false
execution_allowed_now=false
```

E11.4 found a concrete diagnose semantics bug: the runtime `v7-egress-diagnose` script computes handshake age through `awg show "$iface"` unconditionally. For the reserved WireGuard target, live handshake inspection should use `wg show "$iface"`. When the AWG command path yields no handshake line, diagnose falls back to `999999` seconds and persists `SUSPECT` / `curl_ok_but_handshake_stale`.

This explains why WireGuard is zero-user, reserved, quality-good, and route-capable, yet strict target readiness still reports `NO-GO`.

## Evidence

```text
current_runtime_truth=docs/track7/control-plane/e11_4-evidence/current-wireguard-runtime-truth.txt
target_readiness_pretty=docs/track7/control-plane/e11_4-evidence/current-target-readiness.txt
target_readiness_json=docs/track7/control-plane/e11_4-evidence/current-target-readiness.json
restore_settle_pretty=docs/track7/control-plane/e11_4-evidence/current-restore-settle.txt
restore_settle_json=docs/track7/control-plane/e11_4-evidence/current-restore-settle.json
source_analysis=docs/track7/control-plane/e11_4-evidence/diagnose-source-analysis.md
root_cause=docs/track7/control-plane/e11_4-evidence/stale-handshake-root-cause.md
impact=docs/track7/control-plane/e11_4-evidence/impact-analysis.md
fix_vs_waiver=docs/track7/control-plane/e11_4-evidence/fix-vs-waiver-decision.md
second_canary_simulation=docs/track7/control-plane/e11_4-evidence/second-canary-simulation.md
```

Current strict target readiness remains:

```text
selected_target=NONE
approval_status=NO-GO
second_canary_readiness=NO-GO
wireguard_zero_user=true
wireguard_diagnose=SUSPECT
wireguard_avg_mbps=51.648
wireguard_min_mbps=48.01
wireguard_stability=0.929562
wireguard_blocker=diagnose SUSPECT
```

Runtime planner evidence also rejects WireGuard through:

```text
blocked=["severity_SUSPECT"]
users=0
load.status=OK
quality_ok=true
```

Runtime checkers in the captured evidence remain OK:

```text
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
```

Note on restore-settle evidence: the local `tools/v7-restore-settle-gate`
default invocation still reads historical E9.4.4 sample files and therefore
reports historical `NO-GO`. That output was captured honestly in E11.4 evidence.
It does not change the WireGuard diagnose conclusion; E11.4's canary decision is
`NO-GO` because diagnose semantics require a fix or explicit waiver before
second-canary approval.

## Root Cause

```text
wireguard_root_cause_classification=DIAGNOSE_REFRESH_BUG
secondary_classification=ZERO_USER_IDLE_SEMANTICS_WRONG
confidence=HIGH
```

The stale-handshake signal is a diagnose producer issue, not a proven WireGuard datapath failure. The strict target readiness checker is behaving conservatively and correctly by rejecting persisted `SUSPECT`; the bug is upstream in how the persisted diagnose state is produced for WireGuard.

## Impact

```text
diagnose_affects_real_runtime=false
diagnose_affects_target_readiness_only=false
stale_handshake_operational_risk=LOW_DATAPATH_MEDIUM_GOVERNANCE_ATTRIBUTION
```

The diagnose bug does not directly mutate routes or users and does not prove the target is broken. It does affect control-plane decisions beyond readiness: autoswitch planner eligibility also treats `severity_SUSPECT` as a blocker. That makes this a control-plane eligibility problem, not merely a display/reporting issue.

## Fix Vs Waiver

Primary recommendation:

```text
best_strategy=FIX_FIRST_WITH_WAIVER_AS_FALLBACK
fix_required=true
waiver_acceptable=true
waiver_status=CONDITIONAL_FALLBACK_ONLY
```

The correct long-term fix is to make diagnose protocol-aware:

```text
wireguard -> wg show <iface>
amneziawg/awg -> awg show <iface>
```

An explicit stale-handshake waiver is acceptable only as a bounded fallback for one user, with fresh live `wg show`, route, zero-user, quality, restore-settle, and runtime-check evidence. It should not be used to call the target clean.

## Second Canary Simulation

```text
expected_second_canary_readiness=GO_AFTER_DIAGNOSE_FIX_AND_FRESH_GATES_OR_CONDITIONAL_WITH_EXPLICIT_STALE_HANDSHAKE_WAIVER
selected_target_after_fix=wireguard-1779454504-c43409
selected_target_with_waiver=wireguard-1779454504-c43409
blast_radius=one_user
restore_lifecycle=staged_planner_first_apply_after_settle_gate
execution_allowed_now=false
```

Direct second canary execution remains forbidden from this block.

## Final Answers

```text
wireguard_root_cause_classification=DIAGNOSE_REFRESH_BUG
diagnose_affects_real_runtime=false
diagnose_affects_target_readiness_only=false
stale_handshake_operational_risk=LOW_DATAPATH_MEDIUM_GOVERNANCE_ATTRIBUTION
fix_required=true
waiver_acceptable=true
best_strategy=FIX_FIRST_WITH_WAIVER_AS_FALLBACK
expected_second_canary_readiness=GO_AFTER_DIAGNOSE_FIX_AND_FRESH_GATES_OR_CONDITIONAL_WITH_EXPLICIT_STALE_HANDSHAKE_WAIVER
recommended_next_block=E11.5_BOUNDED_WIREGUARD_DIAGNOSE_SEMANTICS_FIX_PACKET
execution_allowed_now=false
```

## Verification

Mandatory verification was run after E11.4 report/governance updates:

```text
tools/v7-run-tests=PASS
targeted_autoswitch_policy_tests=PASS
restore_settle_gate_tests=PASS
target_readiness_tests=PASS
tools/v7-control-plane-governance-check --pretty=PASS
tools/v7-second-canary-target-readiness --pretty=PASS_READ_ONLY_NO-GO
tools/v7-second-canary-target-readiness --json=PASS_READ_ONLY_NO-GO
tools/v7-restore-settle-gate --pre-restore --pretty=PASS_READ_ONLY_HISTORICAL_NO-GO
tools/v7-restore-settle-gate --pre-restore --json=PASS_READ_ONLY_HISTORICAL_NO-GO
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty=PASS_WITH_WARNINGS
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty=PASS_WITH_WARNINGS
py_compile admin/tools/governance/autoswitch=PASS
git diff --check=PASS
```

Expected warnings / strict-tool outcomes:

- `v7-second-canary-target-readiness` remains strict `NO-GO` because WireGuard
  still has `diagnose=SUSPECT`.
- `v7-restore-settle-gate` default mode reads historical E9.4.4 evidence and
  reports historical `NO-GO`.
- runtime/repo diff and release lineage remain partial because runtime/archive
  manifests are not supplied locally and the worktree is dirty.

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
