# WG.CANARY.1 - WireGuard Canary Dereservation Governance Review

## 1. Reservation Origin

Verdict: reservation was intentional and useful in the E10/E11 phase.

The channel `wireguard-1779454504-c43409` was reserved by governance as a clean second canary target:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Evidence:

- `BLOCK_E11_3_BOUNDED_WIREGUARD_RESERVATION_METADATA_MUTATION_REPORT.md`
- `BLOCK_E11_8_TARGET_RESERVATION_ENFORCEMENT_ROOT_CAUSE_AND_FIX_REPORT.md`
- `BLOCK_E11_11_POST_CLOSEOUT_GOVERNANCE_REVIEW_AND_PRODUCTION_HARDENING_REPORT.md`
- `BLOCK_E11_18_TWO_USER_MINI_COHORT_PROMOTION_CLEAN_GOVERNANCE_APPROVAL_REPORT.md`
- `WG_CANARY_ROOT_CAUSE_REPORT.md`

Original purpose:

- keep WireGuard empty and clean for controlled canary testing;
- prevent normal planner production assignment;
- avoid accidental timer/apply movement into a channel still under canary governance;
- force explicit governance before any production use.

That problem was real at the time. E11.8 proved the reservation flag existed but was not originally enforced by autoswitch. The enforcement fix made `canary_reserved=true` a real production assignment blocker.

Current assessment:

The old reason still exists historically, but the project phase has changed. V7 has since certified governed execution, batch execution, feedback, learning loop, operator-approved autonomy, and one/two-user autonomy. The channel is no longer needed only as an untouched canary target. The current operational problem is different: the production pool is too narrow while AWG0/AWG3 are unstable.

## 2. Current Channel Health

Current production-state capture was read-only. No runtime state was changed.

Evidence:

- `WG_CANARY_EVIDENCE/raw_capture/production_state/`
- `WG_CANARY_EVIDENCE/analysis/baseline_planner.json`
- `WG_CANARY_EVIDENCE/analysis/planner_impact_summary.json`

Current WireGuard facts from planner evidence:

| Field | Value |
| --- | --- |
| channel | `wireguard-1779454504-c43409` |
| protocol | `wireguard` |
| role | `GLOBAL_FAST` |
| production eligible now | false |
| blocker | `canary_reserved_production_assignment_blocked` |
| service aggregate | `100.0` |
| Telegram | `OK` |
| avg Mbps | `55.03` |
| min Mbps | `51.35` |
| current stability | `0.933` |
| 1h stability | `0.9366` |
| 1h samples | `6196` |
| required service missing | none |
| required service low | none |

Answer: the channel is production-capable by health and service evidence today. It is excluded by governance reservation, not by quality.

## 3. Risk Audit

If the reservation is removed without limits, the main risk is not channel health. The main risk is blast radius.

Observed counterfactual:

```text
healthy_egress_total: 1 -> 2
candidate_moves_total: 3 -> 26
selected_moves: 1 -> 1
```

Evidence:

- `WG_CANARY_EVIDENCE/counterfactual_state/egress.registry`
- `WG_CANARY_EVIDENCE/analysis/counterfactual_dereserved_planner.json`
- `WG_CANARY_EVIDENCE/analysis/planner_impact_summary.json`

Risk classification:

| Risk | Level | Reason |
| --- | --- | --- |
| routing risk | MEDIUM | planner immediately ranks WireGuard as best available pool member |
| capacity risk | MEDIUM | historical governance cap says `soft_limit=1 hard_limit=2`, while copied planner projection reports `30/38` |
| blast radius risk | HIGH if full promotion | counterfactual expands candidate moves from 3 to 26 |
| governance risk | MEDIUM | direct flag removal would bypass the original canary owner intent |
| stability risk | LOW today | current and historical stability are strong |
| service risk | LOW today | Telegram and required services are OK |

Important capacity note:

E11.11 and E11.18 recorded `soft_limit=1 hard_limit=2` as the safe WireGuard cap. The current copied-state planner projection reports `soft_limit=30 hard_limit=38`. That does not invalidate the health evidence, but it means real promotion must revalidate the canonical capacity owner before unreserved production use.

## 4. Capacity Audit

Historical governance capacity:

```text
soft_limit=1
hard_limit=2
```

Meaning in previous governance:

- one user was safe as canary;
- two users were promotion-clean only after additional governance;
- three or more users were explicitly not justified without separate capacity review.

Current planner copied-state capacity projection:

```text
soft_limit=30
hard_limit=38
users=0
status=OK
```

Capacity conclusion:

WireGuard can participate safely only under a limited production model until capacity ownership is reconciled. Treating it as a normal large-capacity target immediately would be unsafe because the old governance cap and current planner projection disagree.

## 5. Planner Impact

Baseline with `canary_reserved=true`:

```json
{
  "users_total": 26,
  "egress_total": 7,
  "healthy_egress_total": 1,
  "candidate_moves_total": 3,
  "selected_moves": 1
}
```

Counterfactual with only the local copied `canary_reserved` fields removed:

```json
{
  "users_total": 26,
  "egress_total": 7,
  "healthy_egress_total": 2,
  "candidate_moves_total": 26,
  "selected_moves": 1
}
```

The first selected counterfactual move becomes:

```text
10.0.0.2: awg3 -> wireguard-1779454504-c43409
```

Planner impact answer:

Removing the reservation would immediately make WireGuard eligible, place it into the best available pool, and increase planner candidate pressure sharply. That is useful for pool recovery, but too broad for full promotion without a bounded rollout.

## 6. Governance Review

Question: should the canary reservation remain?

Answer: not indefinitely.

The reservation solved a real earlier problem: protecting a clean second canary target from accidental production assignment. That phase is no longer the main platform bottleneck. Today the channel is healthy, while AWG0/AWG3 are temporarily unstable and the production pool has only one healthy eligible channel.

Question: should it be removed fully now?

Answer: no.

Full promotion would let planner treat WireGuard as a normal production target immediately. Counterfactual evidence shows it would become a strong target and expand candidates to the full visible user set. The channel health supports promotion, but the governance/capacity model supports only a gradual promotion.

Governance decision:

```text
LIMITED_PROMOTION
```

## 7. Promotion Plan

No implementation was performed in this program.

Recommended path:

1. Keep current production state unchanged until a separate approved promotion block.
2. Create a bounded `wireguard_limited_production` approval packet.
3. Revalidate truth/convergence and fresh planner state.
4. Reconcile canonical capacity owner:
   - if governance cap remains authoritative, enforce `max_users=2`;
   - if planner load cap is authoritative, document why E11 cap is superseded.
5. Remove `canary_reserved=true` only through the governance owner.
6. Keep effective production cap at two users for the first limited phase.
7. Run dry-run only and verify:
   - WireGuard eligible;
   - healthy pool becomes at least 2;
   - selected users do not exceed cap;
   - no target substitution;
   - no restore-barrier bypass.
8. Execute only in a later explicitly approved program if dry-run passes.
9. Observe service/stability/trust after limited production.
10. Consider full promotion only after limited production evidence is clean.

Suggested next program:

```text
WG_CANARY_LIMITED_PRODUCTION_PROMOTION_PREP_AND_DRY_RUN
```

## 8. Final Verdict

Final classification:

```text
LIMITED_PROMOTION
```

Final answers:

| Question | Answer |
| --- | --- |
| should WireGuard remain permanent canary? | no |
| should canary flag be removed immediately? | no |
| should it become part of production pool? | yes, gradually |
| should it be full production now? | no |
| is channel health blocker present? | no |
| is governance blocker present? | yes, promotion must go through owner |
| is capacity blocker present? | partial, cap ownership must be reconciled |
| does planner benefit if released? | yes |
| does BA.3 benefit if released? | likely yes, but only after bounded promotion |

Final verdict:

```text
wg_canary_origin_understood=true
current_channel_production_capable=true
risk_audit_complete=true
capacity_audit_complete=true
planner_impact_known=true
promotion_justified=true
full_promotion_safe=false
limited_promotion_safe_to_prepare=true
runtime_changed=false
policy_changed=false
users_moved=0
autoswitch_apply_run=false
FINAL_VERDICT=LIMITED_PROMOTION
SAFE_NEXT_STEP=WG_CANARY_LIMITED_PRODUCTION_PROMOTION_PREP_AND_DRY_RUN
```

