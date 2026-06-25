# V7 Do Not Repeat

This file lists certified areas that should not be re-audited unless one of the Reference First conditions is true:

1. The canonical reference has no answer.
2. The canonical reference marks the area UNKNOWN.
3. System behavior changed after the last verified commit.
4. New evidence contradicts the canonical reference or ADR.

## Certified Conclusions

| Area | Certified conclusion | Evidence |
| --- | --- | --- |
| Reference First | Canonical reference, ADRs, and system map must be checked before any new audit. | `docs/decisions/ADR-005-reference-first-rule.md` |
| OMP | OMP is the execution authority; work is optimization-first, not roadmap-first. | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Event-driven autonomy | Production autonomy must be event-driven, not "move every N minutes". | `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md` |
| Architecture completeness | Architecture owners exist; blockers are evidence, authority, and real outcomes. | `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md` |
| Ideal routing model | Correct model is event-driven routing control plane with tiered authority. | `docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md`, `docs/decisions/ADR-V7-IDEAL-AUTONOMOUS-ROUTING-MODEL.md` |
| Knowledge quality model | Safety knowledge is autonomy-grade; suitability/service/route/recovery/freshness are lower maturity and gate autonomy. | `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`, `docs/decisions/ADR-V7-KNOWLEDGE-QUALITY-MODEL.md` |
| Trust source hierarchy | Observed network outcome is primary; operator comparison is secondary supervised evidence only. | `docs/decisions/ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.md` |
| Trust sufficiency | 70/70/70 is a TIER_2+ autonomy floor, not a TIER_1 review requirement. | `docs/decisions/ADR-AUTONOMY-TRUST-SUFFICIENCY-TIER-AWARE.md` |
| Evidence saturation | More rows alone do not unlock autonomy; missing real outcome quality remains the gap. | `docs/decisions/ADR-AUTONOMY-EVIDENCE-SATURATION.md` |
| Risk-tier floors | Floors are tier-aware; do not flatten TIER_1/TIER_2/TIER_3 requirements. | `docs/decisions/ADR-AUTONOMY-RISK-TIERED-FLOORS.md` |
| Knowledge to decision | Existing knowledge gates are connected to decision surface. | `docs/reports/V7_KNOWLEDGE_TO_DECISION_INTEGRATION_REPORT.md` |
| Decision to outcome to learning | Decision, outcome closure, and learning path are connected. | `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md` |
| Governed dry-run cycle | Current cycle reaches authority boundary without apply or user movement. | `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md` |
| Maximum reality extraction | Current passive/runtime evidence has been extracted; more gain requires real outcomes. | `docs/reports/V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md` |
| Suitability bottleneck | Suitability is current highest bottleneck. | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `docs/handoff/V7_CURRENT_STATE_SNAPSHOT.md` |

## Do Not Recreate

Do not recreate:

- Planner
- Governance
- Execution path
- Restore barrier
- Rollback path
- Truth source
- Knowledge model
- OMP
- Event-driven autonomy model
- Trust model
- Evidence saturation model
- Risk-tier floor model
- Canary authority model

## Do Not Re-Audit By Default

Do not repeat broad audits for:

- Route
- Capacity
- Channel Score
- Health
- Planner
- Assignment
- Service Matrix
- Trust
- Recovery
- Autonomy
- Knowledge Quality
- Suitability
- Evidence Saturation
- Event-driven autonomy

Use the reference and ADRs first. Re-audit only if the Reference First rule permits it.

## Do Not Claim

Do not claim:

- that the system can move users autonomously today;
- that TIER_2 is reached;
- that 70/70/70 was skipped;
- that operator comparison replaces observed outcomes;
- that synthetic evidence is allowed;
- that a timer-only daemon is the production model;
- that the current packet can be applied without explicit approval.
