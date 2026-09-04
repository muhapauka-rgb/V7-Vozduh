---
name: v7-code-optimization
description: Run the V7 governed Code Optimization campaign when the user says `CODE_OPTIMIZATION FULL_BASELINE`, `CODE_OPTIMIZATION CHANGED`, `CODE_OPTIMIZATION DOMAIN`, `CODE_OPTIMIZATION CONTINUE`, or `CODE_OPTIMIZATION STATUS`. Use only in this V7 repository; do not use for generic refactoring.
---

# V7 Code Optimization

## Trigger and boundary

On a compact `CODE_OPTIMIZATION` intent, read the current CPS, OMP protocol,
Operational Maturity Program and this skill. OMP remains the sole orchestration
owner, `CODE_OPTIMIZATION` the bounded profile, and
`mission_completion_evidence_gate` the completion consumer. Do not create a
V7 coordinator, Agent System, owner, queue, registry, planner, CPS frontier,
Runtime truth source or Authority. Keep the active Product frontier unchanged.

## Algorithm

1. Run the compact OMP command. It discovers owner-backed domains, derives
   bounded subgraphs and emits fresh immutable executor packets. A packet is
   never a semantic result.
2. Evidence Explorer: inspect packet-bounded source symbols and required
   callers/consumers. Record exact path, symbol, line, input/output,
   reads/writes, errors/STOP_SAFE, compatibility consumer, observability,
   terminal effect, canonical owner and removal/bypass consequence.
3. Semantic Analyst: answer `WHAT NEW REQUIRED PRODUCT, SAFETY, COMPATIBILITY
   OR OBSERVABILITY FACT DOES THIS ADD?` Classify each inspected mechanism as
   `ESSENTIAL`, `SAFETY_ESSENTIAL`, `OBSERVABILITY_ESSENTIAL`,
   `COMPATIBILITY_CURRENT`, `ACTIVE_BUT_REDUNDANT`, `SUPERSEDED`,
   `HISTORICAL_ONLY`, `INCOMPLETE_REQUIRED`, `INCOMPLETE_ORPHANED` or localized
   `UNKNOWN`.
4. Every UNKNOWN names missing fact, existing evidence owner, acquisition action
   and re-entry condition. Static reachability, LOC, tests, documentation or a
   missing static caller alone are not semantic proof.
5. Generate and rank evidence-backed hypotheses. Counterfactual Analyst compares
   CONTROL and COUNTERFACTUAL, including invariants, errors, compatibility,
   rollback and residue. A falsified candidate continues the same Mission.
6. Only `REDUNDANT_LINK_PROVEN` permits one bounded cleanup. Then prove
   before/after subgraph, callers/consumers, regression and residue. Otherwise
   record an evidence-backed honest zero.
7. Submit immutable results through the existing consumer. Use separate
   Architecture, Safety/Regression, Evidence, Quality/Complexity and Mission
   Integrity review contexts; reviewers cannot edit the result.
8. Consume `CONTINUE_SAME_MISSION` until completion. `STATUS` reports pending
   packets, coverage, hypotheses, attempts, cleanup, blockers and next action.
   Never ask the user to relay packets or paste a bootstrap prompt.

## Tool and truth boundary

Python packages, fingerprints, validates, tests and gates. It never decides
semantic truth or auto-generates classifications, candidates or PASS reviews.
No fresh executor result means exactly `SEMANTIC_EXECUTOR_REQUIRED` and
`CONTINUE_SAME_MISSION`. Reject stale, duplicate, unsupported and
blanket-UNKNOWN submissions. Distinguish `FULL_ACTIVE_COVERAGE` from
`PARTIAL_OWNER_BACKED_COVERAGE`; keep unadmitted surfaces as owner-backed local
blockers.

## Completion

Do not stop at packet-ready, tests-pass, report-created or candidate-ready. The
successful full-command terminal is
`CODE_OPTIMIZATION_REAL_SEMANTIC_EXECUTOR_ACTIVE_AND_COMPACT_COMMAND_ACCEPTED`.
Report in compact Russian: intent, coverage, inspected symbols, classes,
hypotheses/counterfactuals, cleanup, localized UNKNOWN, review separation,
terminal and next compact command. Use existing canonical V7 docs and one
Engineering Report; never a new Program or roadmap.
