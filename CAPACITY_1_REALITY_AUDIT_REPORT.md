# CAPACITY.1 Reality Audit Report

Project: V7 VOZDUH
Program: CAPACITY.1_REALITY_AUDIT
Date: 2026-06-19
Code commit audited: `2fb9d205`
Mode: reality audit only

No UI, planner, governance, routing, execution, score, database, or runtime changes were made.

## 1. Capacity Source Map

| Source | Reality |
| --- | --- |
| Planner load policy | `tools/v7-users-autoswitch` defines dynamic/static load policy, reserve ratio, soft/hard/failover multipliers, min/max limits, and rebalance policy. |
| Per-channel limits | `_load_limits_for_egress` starts from policy limits and caps soft/hard/failover limits with explicit egress `capacity_users`, `soft_limit`, and `hard_limit` where present. |
| Healthy working pool | `_healthy_for_load` excludes disabled, maintenance, quarantine, manual, canary, bad quality, and hard-blocked channels. Reserve-only channels can be evaluated but are removed from the normal working pool. |
| Capacity status | `_capacity_status` returns `ok`, `warm`, `high`, `full`, or `overloaded` from per-egress soft/hard/failover status and healthy pool size. |
| Assignment gate | `_gate_load` blocks planned/failover candidates when hard/failover limits are reached, unless explicitly bypassed for current retention. |
| Capacity decision | `_capacity_decision` produces score/reason/headroom and states such as `capacity_available`, `soft_capacity_full`, `hard_capacity_full`, and `empty_capacity_available`. |
| Admin signal | `admin/v7-admin-api` renders capacity/load in score breakdown, channel signals, tooltips, overview load posture, and channel table/drawer. |
| Global capacity plan | `capacity_plan` in overview is IP/pool/readiness capacity, not the same as per-channel assignment load. |

## 2. Overloaded Reality Audit

Canonical finding: `Overloaded` is not a general statement that internet, CPU, traffic, or speed is overloaded.

`Overloaded` is the strongest assignment/load state and appears when a per-egress channel reaches failover-hard capacity. It is stronger than `Hard Full`.

| State | Meaning |
| --- | --- |
| OK | Within assignment policy limits. |
| SOFT_FULL / high | At or above soft limit; check before adding users. |
| HARD_FULL / full | At or above hard limit; planned new assignments are restricted. Existing users are not automatically failing. |
| FAILOVER_FULL / overloaded | At or above failover-hard limit; emergency load state. |

Production evidence captured in `docs/capacity_1/evidence/production_capacity_summary.json` showed hard-full channels, not proof of physical saturation.

## 3. Limit Reality Report

| Limit | Source | Effect |
| --- | --- | --- |
| `soft_limit` | Policy or per-egress registry | Triggers warning/high state and capacity score reduction. |
| `hard_limit` | Policy or per-egress registry | Blocks planned new assignment through load gate. |
| `failover_hard_limit` | Policy or computed from explicit capacity | Blocks failover assignment and maps to overloaded. |
| `capacity_users` | Per-egress registry when present | Caps soft/hard and influences failover capacity limit. |
| Dynamic pool limits | Load policy plus healthy working pool | Changes soft/hard baseline based on current users and available healthy channels. |

Live production policy evidence:

- mode: `dynamic`
- reserve_ratio: `0.15`
- soft_multiplier: `1.15`
- hard_multiplier: `1.45`
- failover_hard_multiplier: `2.0`
- failover_capacity_multiplier: `1.25`
- min_soft_limit: `5`
- min_hard_limit: `10`
- max_hard_limit: `80`

Per-egress registry evidence showed explicit `soft_limit: 1` and `hard_limit: 2` on some newer/test channels, while older channels such as `vless`, `awg0`, and `awg3` relied on policy/default-derived limits.

## 4. Use Semantics Report

Canonical definition:

`Use` means V7 can use the channel under current planner/assignment evidence. It does not mean:

- fastest channel;
- best channel;
- no warnings;
- no capacity pressure;
- unlimited new users;
- superior to every other channel in every test.

`Use` must be read with blocker/load details. A channel can remain usable for current or selected planner context while broad new assignment is limited by capacity.

## 5. Healthy Reality Audit

There are three distinct health meanings:

| Term | Meaning | Can disagree with assignment? |
| --- | --- | --- |
| Technical Health | Diagnostic score/evidence health. | Yes. |
| Healthy for load pool | `_healthy_for_load` eligibility before reserve-only removal. | Yes. |
| Table Healthy | Operator table filter: assignment key is `use` or `keep` and no red first-level signal. | Narrowest; should not be used as generic technical health. |

Important conclusion: `Emergency Only` can be technically healthy. That does not make it safe for normal production assignment.

## 6. Semantic Contradiction Report

| Apparent contradiction | Canonical answer |
| --- | --- |
| Good score but `Emergency Only` | Valid. Role/policy can restrict assignment even when diagnostics are good. |
| Good speed/stability but load warning | Valid. Load is user-assignment pressure, not speed. |
| `Use` but capacity warning | Valid when planner context allows use but broad/additional assignment needs caution. |
| `Healthy` but not assignable | Valid only for technical health. Invalid if claiming table/operator Healthy. |
| `Overloaded` but users still online | Valid. Capacity state restricts movement/additions; it is not automatic current-user failure. |
| Route score low because capacity is full | Existing route component can be reduced by topology/capacity context. It should not be presented as pure route failure. |

## 7. Runtime Evidence

Evidence captured from production read-only endpoints and reduced into committed summaries:

- `docs/capacity_1/evidence/production_capacity_summary.json`
- `docs/capacity_1/evidence/production_decision_summary.json`

Full raw endpoint dumps were used only during the audit session and were not committed, to avoid storing unnecessary production detail in the reference commit.

Key production facts:

| Fact | Value |
| --- | --- |
| Active users | 26 |
| Egress channels | 7 |
| Egress healthy count | 5 |
| Global capacity plan | `FAIL` readiness warning, despite `1248` free IP capacity in pool summary |
| `vless` | 11 users, trusted/currently safe in decision surface, load hard-full in overview evidence |
| `awg3` | 8 users, trusted/currently safe in decision surface, load hard-full in overview evidence |
| `awg0` | 0 users, trusted/currently safe in decision surface, load OK evidence |
| execution-only channel | technically trusted with manual/reserve/canary flags, therefore emergency-only in operator semantics |

This evidence confirms that capacity/load and quality/assignment are separate concepts.

## 8. Operator Semantics

| Operator word | Canonical meaning |
| --- | --- |
| Capacity | Whether current/projected users fit assignment policy limits. |
| Load | Current assigned-user pressure against soft/hard/failover limits. |
| Healthy | Use only with qualifier: technical health, load-pool health, or table/operator Healthy. |
| Use | V7 can use the channel in current planner context. |
| Emergency Only | Role/policy restricted; not normal production assignment. |
| On limit / Hard Full | Do not broadly add users; current users are not automatically failing. |
| Overloaded | Failover-hard assignment limit reached. |
| Score | Mixed diagnostics/condition score, not assignment truth. |

## 9. Canonical Definitions

1. Capacity is an assignment/load concept, not a bandwidth, CPU, or speed concept.
2. Load is assigned-user pressure against configured limits.
3. Hard-full means new planned assignment is restricted; it does not prove current users must leave.
4. Overloaded means failover-hard limit was reached.
5. Use means assignment is allowed in current planner context, not that the channel is objectively best.
6. Emergency means policy/role restriction, not brokenness.
7. Technical health can disagree with assignment decision.
8. Table/operator Healthy is narrower than technical health.
9. Global IP capacity readiness is separate from per-channel assignment load.
10. Operator surfaces must avoid implying capacity warnings are speed failures.

## 10. Documentation Update Plan

Completed in this task:

| Document | Update |
| --- | --- |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Updated Channel Decision V7, Channel Score, Technical Health, Capacity, and Channel Operator Signal Model semantics. |
| `docs/reference/SYSTEM_MAP.md` | Updated Capacity/Load and Planner rows with CAPACITY.1/ADR-009 evidence. |
| `docs/decisions/ADR-009-capacity-and-health-semantics.md` | Created accepted ADR for Capacity/Health/Use/Emergency semantics. |

## 11. Final Verdict

Verdict: `CAPACITY_TRUTH_ESTABLISHED`

Capacity truth is now canonical:

- Capacity/Load is assignment pressure.
- Use is planner-context usability, not best-channel status.
- Emergency is role/policy restriction, not brokenness.
- Healthy must always be qualified as technical, load-pool, or table/operator.
- Overloaded is failover-hard assignment load, not physical traffic saturation.

No runtime changes were made.
