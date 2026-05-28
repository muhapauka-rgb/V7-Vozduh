# Egress `1` Eligibility Matrix After Policy Fix

Evidence sources:
- E9.4 final gate: `docs/track7/control-plane/e9_4-evidence/final-planner-only-gate.txt`
- E9.4.1 current snapshot: `docs/track7/control-plane/e9_4_1-evidence/current-post-policy-snapshot.txt`
- Source: `tools/v7-users-autoswitch`

## E9.4 abort sample

| Signal | Raw state | Policy interpretation | Hard or soft | Causes global ineligibility? | Evidence |
|---|---|---|---|---|---|
| registry enabled | enabled/current users on `1` | usable registry target | soft/normal | no | `users.registry`, `egress.registry` |
| interface | `v7e356a192b79` routes present for users on `1` | datapath present | soft/normal | no | route tables and `v7-user-route-check=OK` |
| load | `users=16`, `soft_limit=19`, `hard_limit=24`, `status=OK` | not full | soft/normal | no | final planner output |
| diagnose/severity | not the blocker for `1` in selected candidates | no diagnose hard fail observed for `1` | soft/normal | no | candidate object |
| speed | `avg_mbps=59.01`, `min_mbps=52.37` | above floor | soft/normal | no | candidate object |
| stability | `0.887` | above floor | soft/normal | no | candidate object |
| Instagram | one failed sample | `DEGRADED_SERVICE`, penalty-only | soft | no | `service_instagram_degraded`, `service_instagram_failed_samples_1`, `service_signal_DEGRADED_SERVICE` |
| Telegram | `TELEGRAM_DOWN_14S`, `hard_blocked=true`, `bad_now=true`, timeout on all listed endpoints | required service hard block | hard | yes | `blocked=["telegram_required_telegram_down_14s"]` |
| route class | `VIDEO_OPTIMIZED_warn` | warning, not route-class hard fail | soft | no | candidate reasons |
| maintenance/quarantine | no egress quarantine shown | no hard block | soft/normal | no | candidate safety |
| policy service persistence | Instagram count `1`, below persistence threshold | not persistent | soft | no | source thresholds |
| critical service count | single non-Telegram service failure plus Telegram hard block | Telegram drives hard state | hard due Telegram | yes | candidate object and source |

## E9.4.1 current snapshot

| Signal | Raw state | Policy interpretation | Hard or soft | Causes global ineligibility? | Evidence |
|---|---|---|---|---|---|
| selected moves | `[]` | no current planner-selected movement | normal | no | latest planner journal in snapshot |
| apply result | `applied=false`, `reason=dry_run` | planner-only state | normal | no | latest planner journal |
| egress `1` eligibility | `eligible=true`, `blocked=[]` | recovered/eligible | normal | no | latest planner journal |
| Telegram | degraded or OK, `hard_blocked=false` in latest candidate objects | penalty/sticky keep, not hard block | soft | no | latest planner journal |
| Instagram | OK or degraded depending sample, no hard block | expected post-policy semantics | soft | no | latest planner journal |
| runtime checks | reconcile/user-route/killswitch/provisioning OK | routing/control-plane checks clean | normal | no | snapshot checks |

## Source semantics relevant to this matrix

`tools/v7-users-autoswitch` treats Telegram differently from generic service signals:

- Telegram `hard_blocked=true` calls `_block(candidate, "telegram_required_<status>")`.
- Telegram degraded but not hard-blocked appends a reason and subtracts score, but does not hard-block.
- A single non-Telegram service failure produces `service_signal_DEGRADED_SERVICE`.
- The restore-stage suppression gate only applies to service-signal-only blockers.

Therefore the E9.4 selected moves were not evidence that the Instagram persistence fix failed. They were evidence that a Telegram hard block can still make egress `1` globally ineligible.

```text
post_policy_egress_1_root_cause=telegram_required_telegram_down_14s
root_cause_classification=TELEGRAM_HARD_BLOCK
confidence=high_for_E9_4_abort_sample
```
