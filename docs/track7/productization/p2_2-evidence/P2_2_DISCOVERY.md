# P2.2 Discovery

## Scope

P2.2 creates the first execution rehearsal layer.

It answers, in preview-only form:

- What would V7 try to execute?
- Why?
- What would be validated?
- How would success be verified?
- How would rollback be represented?

No runtime mutation, routing apply, autoswitch apply, policy apply, user movement, execution engine, or runtime hook was added.

## Reuse

Reused:

- Proposal Store and generated proposals.
- Evidence references attached to proposals.
- Runtime Trust read model.
- Release Trust read model.
- P2.1 Execution Contract Store/Event Store read patterns.
- Existing V7 Admin drawer-first UI.
- Existing auth and GET endpoint patterns.

## Extend

Extended:

- Existing `/api/execution/*` read surface with draft and preview endpoints.
- Existing Execution drawer with draft contracts and validation preview.
- Existing Users, Channels, Routes, Checks, Logs entry points via execution preview chips/cards.

## Refactor

No refactor required.

## Replace

Nothing replaced.

## Do Not Touch

Not touched:

- runtime execution
- user switching
- routing sync
- autoswitch apply
- policy apply
- killswitch mutation
- users.registry
- egress.registry
- runtime hooks

## Verdict

discovery_completed=true
implementation_safe=true
runtime_mutation_performed=false
