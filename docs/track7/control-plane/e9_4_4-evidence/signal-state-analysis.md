# E9.4.4 Signal / Service State Analysis

## Signal Transition

The observed signal sequence was:

```text
07:20:02Z:
  egress_1_eligible=true
  telegram.status=DOWN_GRACE
  telegram.hard_blocked=false
  selected_moves=0
  apply_result=no_selected_moves

07:29:03Z:
  egress_1_eligible=false
  blocker=telegram_required_telegram_down_14s
  telegram.status=TELEGRAM_DOWN_14S
  telegram.hard_blocked=true
  candidate_moves_total=16
  selected_moves=3

07:29:23Z and later:
  selected_moves=0
  apply_result=no_selected_moves
  moved users are frozen/cooldown-protected
  egress_1 returns to eligible/degraded, not hard-blocked
```

## Source Logic

`tools/v7-users-autoswitch` treats Telegram hard statuses as hard global blockers for a candidate egress:

```text
TELEGRAM_HARD_STATUSES = {"NOT_STARTED", "DOWN"}
telegram_status_is_hard(status) => true when status starts with TELEGRAM_DOWN_
telegram hard_blocked => block candidate as telegram_required_<status>
```

The transient service-signal policy fix from E9.3.8/E9.3.9 applies to non-Telegram transient failures and soft Telegram degradation. It correctly does not suppress a Telegram hard-block.

## What Changed After Clean Restore

The clean gate sampled `DOWN_GRACE`, which is degraded but not hard-blocking. A later timer cycle sampled `TELEGRAM_DOWN_14S`, which the policy classifies as a hard-block. That hard-block made egress `1` globally ineligible for Telegram-required users and produced broad failover candidates from `1` to `vless`.

## Classification Candidates

| Candidate | Applies? | Reason |
|---|---:|---|
| Telegram hard-block recurrence | Yes | Direct evidence: `telegram_required_telegram_down_14s`, `TELEGRAM_DOWN_14S`, `hard_blocked=true` |
| Persistent service failure threshold | No primary evidence | The blocker was Telegram hard status, not non-Telegram persistence |
| Multiple critical services | No primary evidence | The decisive blocker was Telegram |
| Stale safety state | No | Safety state updated exactly at movement time and later samples were coherent |
| Planner/apply timing race | Partial | The race is governance-level: signal changed after a single clean gate |
| Expected periodic autoswitch recovery | Yes mechanically | The timer applied normal failover under hard-block conditions |

## Verdict

Root cause is a Telegram hard-block recurrence after the clean restore gate. The autoswitch behavior was mechanically expected, but the restore governance did not require a long enough clean window to catch this recurrence before apply authority was considered safe.

