# E34.G Proposal UX Model

proposal_ux_defined=true

## Proposal Principle

Proposals appear as operator tasks, not backend objects.

The operator sees:

- impact;
- confidence;
- reason;
- affected users;
- target/channel;
- rollback path;
- next safe action.

The operator does not see backend internals first.

## Proposal Types

| Proposal | Where it appears | Operator wording | Required visible fields | Hidden by default |
| --- | --- | --- | --- | --- |
| `MOVEMENT_PROPOSAL` | `Главная`, `Пользователи`, `Каналы`, `Маршруты`, `Проверки` | “Move these users to this safer/better channel.” | affected users, current channel, target channel, services satisfied, confidence, preview, rollback. | batch packet internals, score math, lock IDs. |
| `EVACUATION_PROPOSAL` | `Главная` alert, `Каналы` degraded drawer, `Безопасность` containment | “This channel is unsafe/degraded; evacuate affected users.” | degraded channel, affected users, safe target(s), urgency, rollback/containment. | scheduler queue internals. |
| `REBALANCE_PROPOSAL` | `Настройки` autoswitch, `Каналы` load, `Проверки` readiness | “Capacity/load suggests rebalancing.” | source/target channels, user count, load before/after, policy cap, dry-run. | capacity class transition internals. |
| `OBSERVATION` | `Главная`, `Проверки`, `Логи` | “No action yet; observe or collect evidence.” | reason, evidence missing/stale, next check, safe state. | internal checker raw output. |

## Proposal Card/Drawer Layout

Recommended layout:

```text
Title: What is proposed?
Status: ALLOW / DENY / REVIEW / OBSERVE
Impact: users, channels, services
Why: plain-language reasons
Evidence: summary first, detail drawer second
Safety: preview, rollback, audit
Action: open preview / run check / guarded apply
```

## Denied Proposal UX

A denied proposal must still be useful.

It should show:

- denial reason;
- which gate blocked it;
- what evidence is missing;
- what operator can safely do next.
