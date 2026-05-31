# BLOCK P1.3 Implementation Roadmap And Build Sequence Report

p1_3_completed=true

runtime_mutation_performed=false

implementation_roadmap_defined=true
implementation_inventory_loaded=true
dependency_graph_defined=true
implementation_waves_defined=true
operator_value_defined=true
admin_evolution_defined=true
build_sequence_defined=true
implementation_ready=true
phase1_completion_defined=true
reality_first_rule_satisfied=true

## Summary

P1.3 defines the Phase 1 implementation roadmap and build sequence.

The goal is no longer architecture. The goal is deciding what to build first while maximizing visible operator value and minimizing complexity, risk and dependencies.

## Core Decision

FIRST_IMPLEMENTATION_WAVE=Wave 1 Evidence Foundation Visible In Admin

READY_TO_START_REAL_IMPLEMENTATION=true

## Dependency Graph

Evidence is the root dependency:

```text
Evidence Store
-> Evidence API
-> Evidence UI
```

Proposal depends on Evidence:

```text
Evidence Store
-> Proposal Store
-> Proposal API
-> Proposal UI
```

Runtime and Release Trust depend on Evidence links:

```text
Evidence Store
-> Runtime Convergence Store
-> Runtime Trust API/UI
```

```text
Evidence Store
-> Release Trust Store
-> Release Trust API/UI
```

## Implementation Waves

### Wave 1 — Evidence Foundation Visible In Admin

Scope:

- Evidence Store;
- Evidence APIs;
- EvidenceChip;
- EvidenceDrawer;
- EvidenceTimeline;
- initial seeded/read-only evidence from checks/logs/overview.

Visible admin value:

- proof opens from `Проверки`, `Логи`, `Главная`.

### Wave 2 — Proposal Visibility

Scope:

- Proposal Store;
- Proposal APIs;
- ProposalCard;
- ProposalStatus;
- ProposalDrawer;
- evidence linkage requirement.

Visible admin value:

- recommendations appear in `Главная`, `Пользователи`, `Каналы`, `Маршруты`.

### Wave 3 — Runtime And Release Trust Status

Scope:

- Runtime Convergence Store/API/UI;
- Release Trust Store/API/UI;
- RuntimeTrustStatus;
- ReleaseTrustStatus;
- RuntimeTrustDrawer;
- ReleaseDrawer;
- RollbackAvailability.

Visible admin value:

- operator can inspect runtime and release trust in `Главная`, `Проверки`, `Безопасность`.

### Wave 4 — Production Hardening

Scope:

- search/filter;
- retention and expiration;
- role-gated advanced details;
- proposal expiration/supersession;
- trust freshness/TTL;
- closure records.

Visible admin value:

- Phase 1 becomes sustainable for daily operations and audit.

## Build Sequence

1. Storage adapter.
2. Evidence Store.
3. Evidence APIs.
4. Evidence UI.
5. Proposal Store.
6. Proposal APIs.
7. Proposal UI.
8. Runtime Trust Store/API/UI.
9. Release Trust Store/API/UI.
10. Cross-links and blockers.
11. Tests and hardening.

## Phase 1 Completion

Partially complete after Wave 1:

- proof is visible.

Usable after Wave 3:

- operator can inspect problem, evidence, proposal, runtime trust and release trust.

Production-ready after Wave 4:

- retention, search, closure, role-gating and freshness rules are implemented.

## Remaining Blockers

remaining_blockers=none

Implementation choices needed at build start:

- SQLite vs JSONL adapter;
- state directory/file naming;
- id format;
- first evidence writer;
- advanced details role.

These are implementation choices, not roadmap blockers.

## Evidence Files

- `docs/track7/productization/p1_3-evidence/implementation-inventory.md`
- `docs/track7/productization/p1_3-evidence/dependency-graph.md`
- `docs/track7/productization/p1_3-evidence/wave-design.md`
- `docs/track7/productization/p1_3-evidence/operator-value-review.md`
- `docs/track7/productization/p1_3-evidence/admin-surface-evolution.md`
- `docs/track7/productization/p1_3-evidence/build-sequence.md`
- `docs/track7/productization/p1_3-evidence/implementation-readiness.md`
- `docs/track7/productization/p1_3-evidence/phase1-completion-review.md`
- `docs/track7/productization/p1_3-evidence/tests.md`

## Recommended Next Step

recommended_next_step=START_WAVE_1_EVIDENCE_FOUNDATION_VISIBLE_IN_ADMIN

READY_TO_START_REAL_IMPLEMENTATION=true

FIRST_IMPLEMENTATION_WAVE=Wave 1 Evidence Foundation Visible In Admin

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
