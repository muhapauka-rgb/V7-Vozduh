# P1.2 Trust Chain Integration

trust_chain_defined=true

## Chain

```text
Problem
-> Evidence
-> Proposal
-> Runtime Trust
-> Release Trust
```

## Integration Rules

### Problem -> Evidence

Problem surfaces must link to Evidence Bundle when proof exists.

### Evidence -> Proposal

Proposal requires `evidence_bundle_id`.

No proposal without evidence.

### Proposal -> Runtime Trust

Proposal UI and future governance submission must show runtime trust state.

If runtime is:

- `RUNTIME_UNKNOWN`;
- `RUNTIME_DRIFT`;
- `RUNTIME_BLOCKING`;

then forward action must be blocked or require trust refresh before governance.

### Runtime Trust -> Release Trust

Runtime trust depends on expected release identity.

Release trust confirms:

- release is known;
- release is certified;
- rollback is available;
- runtime match is meaningful.

### Release Trust -> Operator Decision

If release status is:

- `RELEASE_UNKNOWN`;
- `RELEASE_DRIFT`;
- `RELEASE_BLOCKING`;

then forward action fails closed until verified or remediated.

## Admin Integration

The trust chain appears through existing surfaces:

- `Главная`: high-level trust summary;
- `Проверки`: verification details;
- `Безопасность`: rollback/release safety.

## Implementation Verdict

Trust chain is defined and compatible with P1.A, P1.B, P1.C and P1.D/E.
