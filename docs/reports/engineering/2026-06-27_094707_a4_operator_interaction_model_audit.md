# Engineering Report

## Summary

Да. Текущая модель, где человек утверждает exact packet, может делать A4 практически невыполнимой: approval и execution разделены временем, а packet является короткоживущим runtime artifact.

Существующая архитектура уже поддерживает выход: one-time governed execution authority для одного полного execution cycle, а не для одного packet id.

## Action Performed

Проверены существующие owners: Product Specification, Runtime Model, OMP, Current Program State, Implementation Backlog, Action-Class Authority ADR, Delegated Autonomy Policy ADR, recent A4/authority reports.

## Objective Observations

- Product Specification прямо говорит: packet approval временный fallback, не целевая product abstraction.
- Runtime Model разделяет authority object и execution object.
- ADR Action-Class Authority фиксирует: packet is fresh runtime execution artifact.
- ADR Delegated Autonomy Policy допускает governed learning mode внутри approved policy bounds.
- Последние A4 попытки показывают практическую проблему: packet меняется между approval и lease/apply.

## Engineering Conclusions

Exact packet approval is the immediate loop source.

One-time governed execution authority can fit existing architecture if it authorizes:

- one complete governed A4 cycle;
- one fresh READY packet generated inside that same cycle;
- one user maximum;
- current action class only;
- no daemon/timer;
- no runtime automation;
- no authority expansion;
- mandatory live validation, restore barrier, apply, verify, rollback/no-rollback closure, learning.

Runtime must still stop if fresh packet exits the approved envelope.

## Impact

No runtime behavior changed. No authority expanded. No users moved.

## Capability Progress

No percentage change.

## Backlog Progress

A4 remains current. A6 remains the existing owner for generalized runtime eligibility arbitration.

## Production Maturity

No maturity change.

## Canonical Knowledge

No canonical update required. Existing canonical owners already contain the model.

## Evidence

Recent A4 stale approval stops:

- `pkt_preview_c72b642b2b6cd55532979944` became stale before execution.
- `pkt_preview_2cb1fe3b8ce1551c75ccff11` became stale before execution.
- `pkt_preview_a69fe12e51c528c2a0402c0c` is the latest fresh packet.

## Next Step

Continue OMP with explicit one-time governed execution-cycle authority if operator approves that authority form.

## Re-audit Rule

Re-audit only if Runtime Model changes authority semantics, OMP removes Action-Class/Delegated Autonomy path, or production evidence shows execution-cycle authority weakens safety.
