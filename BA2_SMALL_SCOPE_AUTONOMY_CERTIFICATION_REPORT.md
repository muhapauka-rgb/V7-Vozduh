# BA2 Small Scope Autonomy Certification Report

Проект: V7 Vozduh

Дата: 2026-06-12

Итоговый вердикт: `SMALL_SCOPE_AUTONOMY_BLOCKED`

Единственный blocker: `planned_autonomy_policy_limit_is_1`

## 1. Truth Gate

Canonical checks were rerun with network access:

| Check | Result |
|---|---|
| GitHub branch readable | `true` |
| local commit | `55ceb2d0a7de18f4a8036eca610fbcf847d07d24` |
| GitHub commit | `55ceb2d0a7de18f4a8036eca610fbcf847d07d24` |
| truth-check final verdict | `PASS` |
| convergence final verdict | `PASS` |
| runtime action safe | `true` |
| production runtime truth | `PASS` |

Production runtime root is not a git checkout. Runtime identity is copied binaries from deploy manifest.

Critical runtime hashes matched local tools:

| Tool | Local/Production |
|---|---|
| `v7-users-autoswitch` | `01cf8e67ddd60e42888f3bf58a3ef4e8e29662588fa4a1c45ef10b64aba1d229` |
| `v7-operator-execution-packet` | `9cf153a1869c4d3d72c418d74b49300995b3f5621c78cb523eef50ad39a301bf` |
| `v7-intelligence-snapshot-refresh` | `d9ff95a593450a02a33b27442dc0b0229bf7c7b0bf959b924ce6a249140c5312` |

Evidence:

- `BA2_EVIDENCE/phase1_truth_gate_escalated.json`
- `BA2_EVIDENCE/phase1_convergence_gate_escalated.json`

## 2. Two User Autonomy

Command used:

```bash
/usr/local/bin/v7-users-autoswitch \
  --pre-planner-refresh write \
  --pre-planner-refresh-command v7-intelligence-snapshot-refresh \
  --max-selected-moves 2 \
  --pretty
```

Result:

| Field | Value |
|---|---|
| snapshot gate stop required | `false` |
| source mismatch families | `[]` |
| pre-planner refresh | `REFRESH_SUCCESS` |
| authority class | `POOL` |
| authority allowed user budget | `25` |
| requested max selected moves | `2` |
| policy planned limit | `1` |
| selected after policy count | `1` |
| selected after authority budget count | `1` |
| effective blast radius | `1` |
| final selected moves | `0` |
| terminal state | `DRY_RUN` |
| terminal reason | `dry_run_restore_barrier_clearance_generation_expired` |

The planner found 25 candidate moves and the platform authority budget allows up to 25, but the current planned autonomy policy still caps planned moves to 1:

```json
"planned_limit": 1
```

`--max-selected-moves 2` does not raise policy. It only narrows selection when the policy already allows a larger number.

Evidence:

- `BA2_EVIDENCE/phase2_two_user_fresh_planner.json`
- `BA2_EVIDENCE/phase2_two_user_fresh_planner_summary.json`
- `BA2_EVIDENCE/phase2_two_user_blocker_analysis.json`

## 3. Two User Certification

Verdict: `BLOCKED`

Reason:

V7 is certified for one-user autonomy, but the active planned autonomy policy still permits only one planned user per run. Therefore BA2 cannot safely certify 2-user autonomy without an explicit governance/policy step that raises the planned per-run limit from `1` to `2`.

No 2-user packet was generated because the canonical planner did not produce an authorized 2-user selected move set.

No restore barrier was generated for 2 users.

No apply was executed.

Users moved in BA2: `0`

## 4. Five User Autonomy

Status: `NOT_STARTED`

Reason:

BA2 requires progression:

```text
2 users
↓
5 users
```

Since 2-user autonomy is blocked, 5-user autonomy was not attempted.

## 5. Blast Radius Review

| Check | Result |
|---|---|
| unexpected users moved | `false` |
| target replacement | `false` |
| planner bypass | `false` |
| governance bypass | `false` |
| rollback failure | `false` |
| apply executed | `false` |

BA2 stopped before runtime mutation.

## 6. Learning Loop Review

Not applicable for BA2 execution because no BA2 movement occurred.

The BA1 learning loop remains certified from `BA1_FINAL_AUTONOMY_CERTIFICATION_REPORT.md`.

## 7. Final Certification

| Verdict | Value |
|---|---|
| truth_gate_pass | `true` |
| convergence_pass | `true` |
| runtime_action_safe | `true` |
| two_user_autonomy_certified | `false` |
| five_user_autonomy_certified | `false` |
| users_moved | `0` |
| apply_executed | `false` |
| autonomy_scope_exceeded | `false` |
| final_verdict | `SMALL_SCOPE_AUTONOMY_BLOCKED` |
| single_blocker | `planned_autonomy_policy_limit_is_1` |
| SAFE_NEXT_STEP | `BA2_POLICY_GATE_RAISE_PLANNED_LIMIT_TO_2_THEN_RERUN_TWO_USER_AUTONOMY` |

## 8. What This Means

The system is behaving safely.

It did not blindly use POOL authority to move 2 users. It also respected the lower planned-autonomy policy cap of 1.

To continue BA2, the next program must explicitly decide whether to raise:

```text
autoswitch_max_planned_per_run: 1 -> 2
```

Only after that policy gate passes should BA2 rerun the 2-user stage. If 2-user autonomy is certified, a separate controlled step may raise the planned limit to 5 and run the 5-user stage.

