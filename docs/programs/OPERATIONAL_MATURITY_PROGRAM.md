# V7 Operational Maturity Program

Status: `ACTIVE`
Program: `Operational Maturity`
Created: 2026-06-25
Current reference commit: `e975461860bb23178a7d0f2885ad7e9990edb6fc`
Runtime architecture certification commit: `39c46ed379ff4a2ccadb84a49a0dd9dcd2de579b`

This document is the primary program source for future V7 implementation work. It replaces roadmap-driven development with evidence-driven operational maturity.

Roadmaps, reports, ADRs, and reference files remain evidence and context. This program decides the current phase, next phase, stop conditions, and whether Codex may continue automatically.

## 1. Project Vision

V7 is an event-driven autonomous routing control plane that protects user connectivity by observing production reality, selecting safe routes through existing owners, acting only under certified authority, verifying outcomes, and learning from real evidence.

This vision is immutable unless a future ADR explicitly supersedes it.

## 2. Program Principles

1. Reality First.
2. Discover -> Reuse -> Extend -> Implement.
3. No duplicate owners.
4. No duplicate planners.
5. No duplicate governance.
6. No synthetic evidence.
7. Tests before certification.
8. Certification before next phase.
9. Documentation after implementation.
10. Continue automatically when possible.

Operational meaning:

- Reports preserve evidence.
- Canonical reference preserves current truth.
- ADRs preserve decisions.
- This program preserves what V7 does next.

## 3. Program States

| State | Meaning |
| --- | --- |
| `NOT_STARTED` | Phase is known but no implementation or verification has begun. |
| `ACTIVE` | Phase is the current work item and may proceed under the stop conditions below. |
| `BLOCKED` | Phase hit an allowed stop condition. |
| `CERTIFIED` | Phase passed tests, truth, convergence, and evidence review. |
| `COMPLETED` | Phase is certified and its results are absorbed into reference/program state. |

## 4. Current Program

`Operational Maturity`

Purpose:

Move V7 from architecture-complete / authority-bound autonomy to production maturity through the shortest safe sequence of real outcomes, verification, learning, and certification.

## 5. Current Phase

`GOVERNED_CANDIDATE_OUTCOME_EXECUTION_AND_CLOSURE`

Source:

- `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`
- `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`
- `docs/reference/SYSTEM_MAP.md`

Reason:

The final architecture certification says V7 has no fundamental architecture gap. The governed dry-run reaches `AUTHORITY_BOUNDARY` with packet preview, restore/rollback preview, verification plan, outcome closure plan, and learning path connected. The next maturity gain requires real governed candidate outcome evidence.

## 6. Current Objective

Use existing owners to create and close one real governed candidate outcome only after explicit operator authority.

The phase must:

1. reuse the existing planner;
2. reuse the existing governed packet owner;
3. reuse the existing restore barrier;
4. reuse the existing rollback preview;
5. reuse the existing verification plan;
6. reuse the existing feedback/outcome closure owner;
7. reuse the existing learning refresh owner;
8. re-evaluate confidence, trust, prediction, and suitability after outcome closure.

No autonomous apply is approved by this program state.

## 7. Success Criteria

| Criterion | Required State |
| --- | --- |
| Exact packet authority | Explicit operator approval exists for the exact packet before any restore-barrier write or apply. |
| Runtime safety | No movement occurs before authority; no hidden daemon or timer apply is enabled. |
| Existing owners | Planner, packet, restore barrier, rollback, feedback, learning, and truth/convergence owners are reused. |
| Real outcome | The candidate outcome is observed after a real governed/manual action, not synthesized. |
| Closure | Outcome, verification, rollback/no-rollback decision, feedback, and learning are recorded through existing paths. |
| Certification | Tests, `tools/v7-truth-check --all --json`, and `tools/v7-convergence-status --json` pass after the phase. |
| Documentation | Canonical reference, system map, ADRs, and this program are updated when meaning changes. |

## 8. Stop Conditions

Only these stop conditions are allowed:

1. `AUTHORITY_BOUNDARY`
2. `REAL_WORLD_LIMIT`
3. `UNSAFE_IMPLEMENTATION`
4. `FUNDAMENTAL_ARCHITECTURE_GAP`

Current blocker:

`AUTHORITY_BOUNDARY`

Details:

- production governed dry-run stops before restore-barrier write or apply;
- explicit operator approval is required for the exact packet;
- confidence, trust, prediction confidence, and suitability are still below autonomous maturity needs;
- candidate outcome gap remains real-world evidence, not missing architecture.

## 9. Automatic Continuation Rule

After every completed phase Codex must:

1. read this file;
2. read `docs/reference/V7_CANONICAL_REFERENCE.md`;
3. read `docs/reference/SYSTEM_MAP.md`;
4. read relevant ADRs and latest certified reports;
5. determine the next phase from certified state;
6. continue automatically when the next action is read-only, documentation-only, verification-only, or an implementation through existing owners with no runtime apply risk;
7. stop only when one of the four allowed stop conditions is reached.

If `AUTHORITY_BOUNDARY` is reached, Codex may continue all safe preparation, validation, documentation, and read-only verification. Codex must not cross the authority boundary into restore-barrier write, apply, or user movement without explicit operator approval for that exact action.

## 10. Phase History

| Phase | Certified Result | State | Evidence |
| --- | --- | --- | --- |
| Canonical Reference Base | Reference and ADR system created | `COMPLETED` | `docs/reference/V7_CANONICAL_REFERENCE.md`, `docs/reference/SYSTEM_MAP.md` |
| Reference First Rule | Future audits must read reference before re-auditing | `COMPLETED` | `docs/decisions/ADR-005-reference-first-rule.md` |
| Event-Driven Autonomy Contract | Timer-only movement rejected; event-driven model accepted | `COMPLETED` | `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md` |
| Knowledge Quality Model | Data/signal/knowledge/action authority separated | `COMPLETED` | `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md` |
| Autonomous Routing Foundation | Fit, outcome, recovery, anti-flap, freshness models exposed read-only | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_ROUTING_FIT_OUTCOME_RECOVERY_FOUNDATION_REPORT.md` |
| Knowledge To Decision Integration | Routing knowledge can influence read-only decisions without apply | `COMPLETED` | `docs/reports/V7_KNOWLEDGE_TO_DECISION_INTEGRATION_REPORT.md` |
| Decision To Outcome To Learning Integration | Outcome quality and learning path connected | `COMPLETED` | `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md` |
| Highest Leverage Outcome Growth | Verdict `MIXED_PATH`; suitability needs real candidate outcomes | `COMPLETED` | `docs/reports/V7_HIGHEST_LEVERAGE_OUTCOME_GROWTH_REPORT.md` |
| Autonomy-Grade Suitability Program | Suitability growth requires real candidate outcome closure | `COMPLETED` | `docs/reports/V7_AUTONOMY_GRADE_SUITABILITY_PROGRAM_REPORT.md` |
| Autonomous Knowledge Growth Program | 12 cycles verified; maturity score `84.167`; boundary remains authority | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_KNOWLEDGE_GROWTH_PROGRAM_REPORT.md` |
| Autonomous Routing Evolution Program | TIER_2 remains blocked by confidence/trust/prediction/suitability and real outcomes | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_ROUTING_EVOLUTION_PROGRAM_REPORT.md` |
| Maximum Reality Knowledge Extraction | `72` candidate outcomes are not hidden; they require governed/manual action | `COMPLETED` | `docs/reports/V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md` |
| Final Autonomous Routing Architecture Certification | Verdict `ARCHITECTURE_COMPLETE_WITH_FUTURE_OPTIONAL_EXTENSIONS` | `CERTIFIED` | `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md` |
| Governed Canary Knowledge-Gated Dry-Run Cycle | Production reaches `AUTHORITY_BOUNDARY`; no apply, no movement | `CERTIFIED` | `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md` |

## 11. Next Phase

`TIER1_EXPLICIT_OPERATOR_APPROVAL_FOR_EXACT_PACKET`

Program interpretation:

This is not a new discovery phase. It is the authority decision required before `GOVERNED_CANDIDATE_OUTCOME_EXECUTION_AND_CLOSURE` can cross from safe preparation into a real governed/manual action.

If approval is granted, the next implementation step is:

```text
exact packet approval
  -> restore-barrier write through existing owner
  -> bounded governed/manual apply through existing owner
  -> verification
  -> rollback/no-rollback decision
  -> outcome closure
  -> feedback
  -> learning refresh
  -> confidence/trust/prediction/suitability re-evaluation
  -> certification
```

If approval is not granted, the program remains blocked at `AUTHORITY_BOUNDARY` and may continue only read-only verification, documentation, and evidence freshness checks.

## 12. Next Phase Entry Criteria

| Entry Criterion | Required |
| --- | --- |
| Exact packet | Fresh exact packet from existing governed dry-run cycle. |
| Operator authority | Explicit approval or rejection for that exact packet. |
| Restore readiness | Existing restore/rollback preview passes before action. |
| Scope | One governed candidate outcome unless a future certified phase narrows or expands the scope. |
| Apply path | Existing guarded/manual owner only. |
| Evidence | Outcome closure and learning paths available before apply. |
| Safety | No daemon enablement, no timer-only movement, no duplicate planner/governance/execution. |

## 13. Program Certification

| Field | Current Value |
| --- | --- |
| Completed phases | Canonical reference, reference-first rule, event-driven contract, knowledge quality, routing foundation, knowledge-to-decision, decision-to-outcome-to-learning, outcome leverage, suitability program, knowledge growth, routing evolution, maximum reality extraction. |
| Certified phases | Final autonomous routing architecture certification; governed knowledge-gated dry-run cycle. |
| Current blockers | `AUTHORITY_BOUNDARY`; confidence/trust/prediction confidence below autonomous floor; suitability/candidate outcome gap; explicit apply authority not granted. |
| Current maturity | Architecture complete with future optional extensions; autonomy cycles mature to authority boundary; real-world outcome evidence remains the maturity bottleneck. |
| Current runtime posture | No autonomous apply, no user movement, no daemon enablement. |
| Current next action | Obtain explicit operator decision for the exact packet, or stay in safe read-only preparation. |

## Program Rule For Future Work

Before starting any future implementation phase, Codex must treat this file as the first program source. If a prompt conflicts with this program, the program wins unless the user explicitly changes the program through a new ADR/reference update.
