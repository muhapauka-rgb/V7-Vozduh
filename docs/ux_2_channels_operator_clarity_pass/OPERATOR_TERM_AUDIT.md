# OPERATOR_TERM_AUDIT

Project: V7 VOZDUH
Program: UX.2_CHANNELS_OPERATOR_CLARITY_PASS
Date: 2026-06-20
Branch: Updatesystem

## Operator Term Rule

The first channel drawer screen must be understandable without V7 internals.

Developer terms stay in Engineering Diagnostics.

## Term Audit

| Term | Decision | Operator Replacement | Reason |
| --- | --- | --- | --- |
| Runtime | Rename on operator surface | Готовность | Operator cares whether V7 has current readiness proof, not runtime internals |
| Confidence | Hide / replace | Уверенность only in deeper diagnostics, otherwise "проверка устарела" | Confidence reads like a model score and competes with the decision |
| Evidence | Hide to engineering layer | Данные / источник only when needed | Evidence is a technical proof object, not a first-screen action |
| Snapshot | Hide to engineering layer | Проверка / текущие данные | Snapshot is internal implementation language |
| Eligibility | Hide to engineering layer | Можно использовать / нельзя назначать | Eligibility is planner vocabulary |
| Trust score | Hide to engineering layer | Technical diagnostics only | Trust math must not compete with Channel Decision V7 |
| Health score | Hide to engineering layer | Technical diagnostics only | Score explains diagnostics, not assignment truth |
| Planner internals | Hide to engineering layer | Решение V7 / причина | Operator needs the answer, not candidate/gate internals |
| Уточнить | Rename | Проверка устарела / Открыть источник | Too vague; does not say what is true |
| Частичная уверенность | Rename | Последняя проверка не свежая | Operator needs current reality, not abstract confidence |
| Нет свежих данных | Narrow usage | Проверка устарела / Нет свежего подтверждения | Allowed only when it does not conflict with the decision |

## Implemented Surface Terms

| Surface | Before | After |
| --- | --- | --- |
| Channel signal label | Runtime | Готовность |
| Yellow service/runtime/stability signal | Нет свежих данных | Проверка устарела |
| Yellow load signal | Нет свежих данных | Запас ограничен |
| Red signal | Проблема | Влияет на решение |
| Signal detail fields | Состояние / Причина / Решение | Что произошло / Почему / Что делать |
| Problem detail fields | Проблема / Причина / Решение | Что произошло / Почему это важно / Что можно сделать сейчас |

## Remaining Allowed Technical Terms

Technical words may still appear inside Engineering Diagnostics, logs, setup/provisioning workflows, or raw API/debug surfaces. Those areas are not the first-screen operator answer.

