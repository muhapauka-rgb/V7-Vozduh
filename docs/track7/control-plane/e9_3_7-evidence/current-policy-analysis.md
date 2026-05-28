# E9.3.7 Current Autoswitch Policy Analysis

Mode: read-only source analysis.
Runtime mutation: no.
Autoswitch apply restore: no.
Canary: no.

## Source Scope

Primary source inspected:

- `tools/v7-users-autoswitch`

Relevant logic:

- `SwitchPlanner._decision_for_user`
- `SwitchPlanner._candidate`
- `SwitchPlanner._gate_service`
- `SwitchPlanner._telegram_candidate_state`
- `SwitchPlanner._select_moves`
- `SwitchPlanner._pick_projected_moves`
- `SwitchPlanner.apply`

## Current Eligibility Flow

For each enabled user, `SwitchPlanner._decision_for_user` builds candidate egress rows for the user's important services and route class. The current egress is evaluated with the same candidate rules as alternatives.

If current egress is missing or not eligible:

```text
if not current or not current.eligible:
    failover_candidates = [...]
    best_failover = next eligible candidate
    if best_failover and best_failover.egress.id != user.current and cooldown_ok:
        action = switch
        move_type = failover
        recommended = best_failover.egress.id
        reason.append("current_egress_not_eligible")
```

This means any hard eligibility block on the current egress can turn every user on that egress into a failover candidate.

## Service Hard Gates

`_gate_service` handles service matrix checks.

Telegram is special:

```text
if telegram.hard_blocked:
    block candidate
elif telegram.degraded:
    append degraded reason only
elif telegram.ok:
    append service_telegram_ok
```

Non-Telegram services are hard gates:

```text
row = matrix_services.get(service)
if row and row.get("ok") is False:
    block(candidate, f"service_{service}_failed")
```

Therefore a single measured `instagram ok=false` row is enough to make the egress globally ineligible for users whose important service set includes Instagram.

## E9.3.5 Failure Class

The E9.3.5 final planner sample saw:

```text
selected_moves=3
candidate_moves_total=15
target=vless
reason=current_egress_not_eligible
```

E9.3.6 classified the concrete egress `1` blocker as:

```text
service_instagram_failed
telegram.status=DEGRADED
telegram.hard_blocked=false
```

The hard blocker was Instagram, not Telegram. Telegram degraded contributed signal/penalty semantics, but did not itself make egress `1` ineligible.

## Persistence And Confidence

Current source does not show a persistence threshold for non-Telegram service hard gates inside `_gate_service`.

The planner does expose confidence in explanations:

```text
elif score_gap >= 250 or move_type == "failover":
    confidence = "high"
```

But this confidence is assigned after the decision path and does not prevent single-sample service failure from creating failover candidates.

The policy has cooldown/anti-flap protections, but those apply mainly to user movement cadence and repeated switching. They do not distinguish:

- single-service failure vs transport failure
- app-specific route problem vs whole-egress datapath failure
- one bad sample vs persistent failure
- restore-stage observation vs normal autonomous failover

## Failover Selection And Limits

`_select_moves` groups decisions by `move_type`.

Failover moves are capped by:

```text
autoswitch_max_failover_per_run
```

E9.3.5 selected three moves because the active policy limit was three. The broader candidate set still contained 15 users.

The cap limits per-run blast radius, but it does not suppress broad candidate generation. If the same signal persists across timer runs, multiple batches can move over time.

## Why Vless Was Selected

When egress `1` became ineligible, the failover path ranked eligible alternatives. E9.3.6 evidence showed `vless` was the best eligible failover target at that moment.

This is expected under current logic, not evidence that the operator manually selected `vless`.

## Policy Problem

Current policy treats a non-Telegram service failure as a hard eligibility blocker immediately. This is too strong for transient service signals during staged restore because it can convert a one-service observation into a broad egress-level failover plan.

The problem is not proven broken routing. Runtime checkers stayed OK:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Verdict

Current policy is safe enough to explain the E9.3.5 abort, but not safe enough to restore apply authority blindly while transient service signals can produce broad failover candidates.

Apply should remain held until either:

1. A fresh planner-only sample shows `selected_moves=0`, or
2. Operator explicitly approves exact bounded movement, or
3. Autoswitch policy is refined so single/transient service failures do not cause global ineligibility.

