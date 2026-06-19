# SIGNAL_HIERARCHY_MATRIX

Project: V7 VOZDUH
Program: UX.2_CHANNELS_OPERATOR_CLARITY_PASS
Date: 2026-06-20
Branch: Updatesystem

## Rule

Channel Decision V7 is stronger than signals.

Signals explain confidence and evidence. Signals do not create a second operator decision.

## Signal Hierarchy

| Signal | Confirms Decision | Warns Operator | Affects Decision | Operator Meaning |
| --- | --- | --- | --- | --- |
| Services | Green confirms service checks support the decision | Yellow means the latest service confirmation is stale or incomplete | Red can influence blocked/evacuate when primary services fail | Are user-facing services available enough for this channel decision? |
| Load | Green confirms assignment headroom supports the decision | Yellow means assignment headroom is limited | Red can restrict new assignments or contribute to evacuation/blocked states | Can this channel receive or keep users under assignment limits? |
| Readiness | Green confirms the current runtime/readiness snapshot supports the decision | Yellow means the latest readiness confirmation is stale or incomplete | Red can reduce confidence or block safe assignment when readiness is not proven | Is current channel readiness proven enough to trust the decision? |
| Stability | Green confirms stability supports the decision | Yellow means the latest stability check is stale or incomplete | Red can influence blocked/evacuate when stability is below floor | Is the channel steady enough for users? |

## Yellow Rule

Yellow means attention, freshness, or limited confidence.

Yellow does not mean:

- Do not use.
- Evacuate.
- Blocked.
- Planner override.

If V7 says `Использовать` and a signal is yellow, operator copy must say the channel can still be used unless the decision changes.

## Red Rule

Red means the signal can affect the decision.

Red signal detail must explain:

1. What happened.
2. Why it matters.
3. What the operator can do now.

## Final Classification

| Signal State | First-Screen Label | Relationship To Decision |
| --- | --- | --- |
| Green | OK | Confirms decision |
| Yellow | Проверка устарела / Запас ограничен | Attention only; does not override decision |
| Red | Влияет на решение | Participates in decision |

