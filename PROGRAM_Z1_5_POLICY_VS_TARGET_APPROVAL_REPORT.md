# Program Z1.5 Policy Vs Target Approval Report

Date: 2026-06-01
Project: V7 Vozduh
Mode: Analysis only

## 1. Reality Audit

No movement, rollback execution, apply, deploy, systemd change, or runtime mutation was performed.

Recent evidence shows repeated target drift:

- F2: `10.7.0.16`, target changed from `awg3` to `awg0`
- Z1: candidate changed to `10.7.0.10`, target `awg3`

Current runtime remains:

- execution target: `10`
- `awg0`: `3`
- `awg3`: `3`
- `vless`: `2`

## 2. Conflict Audit

No equivalent policy-based movement approval contract exists. Existing planner, proposal cap, safety review, movement preview, and zero-movement audit patterns should be reused.

## 3. Truth Source Audit

Fresh planner truth must override stale approval truth. Approval can authorize a target or policy class, but runtime recheck decides whether execution is still allowed.

## 4. Runtime Audit

Safety status is `ok`, but observability still reports capacity `warm`, channels `unstable`, routing `degraded`, services `blocked`, and trusted/direct routing `unknown`.

## 5. Target Approval Analysis

Target approval is concrete, clear, and safest. It fails closed on drift, but repeated stale denial makes it impractical for bounded autonomy during volatile health periods.

## 6. Policy Approval Analysis

Policy approval can authorize `user=X`, `target_class=BEST_HEALTHY`, `budget=1`, `route_class=GLOBAL_STABLE`. It reduces harmless target drift but requires strict target substitution and fingerprints.

## 7. Drift Model

Critical drift:

- candidate change
- budget change
- route/trust/policy class change
- rollback change
- safety critical
- target ineligible
- policy hash change

Non-critical drift under policy approval:

- target egress changes within same approved class and remains healthy, eligible, and capacity-safe.

## 8. Fingerprint Model

Approval, runtime, and proposal fingerprints must bind:

- user or candidate class
- budget
- route class
- target class
- rollback
- policy hashes
- registry hashes
- safety status
- selected move fingerprint
- TTL

## 9. Target Substitution Rules

Automatic target substitution is allowed only under policy approval and only if route class, trust class, policy class, service scope, capacity class, and rollback remain compatible.

## 10. Autonomy Impact

Target approval maximizes operator clarity but blocks autonomy through stale denials. Policy approval improves autonomy but needs strong guardrails. Hybrid gives the best balance.

## 11. Safety Review

Hybrid is safer than pure policy approval and more practical than pure target approval.

## 12. Decision Tree

Target approval path:

- exact target must match or deny.

Policy approval path:

- target may change only inside approved class.

Hybrid path:

- target approval for high-risk actions
- policy approval for one-user bounded autonomy

## 13. Governance Decision

Recommended model: HYBRID

## 14. Recommended Next Program

Program Z2 should implement and test the hybrid policy approval contract as read-only first:

- movement packet schema
- policy approval fingerprint
- target substitution validator
- runtime recheck validator
- replay/expiry/stale-hash tests
- admin preview copy explaining substitutions

## Required Verdicts

- target_approval_understood=true
- policy_approval_understood=true
- drift_model_defined=true
- fingerprint_model_defined=true
- target_substitution_defined=true
- autonomy_impact_understood=true
- governance_model_selected=true
- recommended_model=HYBRID
- safe_to_continue=true

## Safety Verdict

- users_moved=false
- rollback_executed=false
- autoswitch_apply_run=false
- routing_changed=false
- deploy_performed=false

