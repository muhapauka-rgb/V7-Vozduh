# ADR-V7-KNOWLEDGE-QUALITY-MODEL

Status: Accepted
Date: 2026-06-24
Commit: base `f46a28639e839cb585e29289a9f5e044eecb963b`; introduced by this ADR commit.

## Context

V7 now has a canonical ideal autonomous routing model for `10,000+` users and `100+` channels.

The next question is not whether V7 has collected rows or reports. The question is whether current evidence has become routing knowledge that is fresh, covered, correct, consistent, diverse, attributable, relevant to users and services, and actionable.

Certified current facts:

- prediction rows are matched (`21/21`) but source confidence is low;
- candidate outcomes are incomplete (`84/156`) with `72` missing outcomes;
- blast confidence is `100`;
- rollback confidence is `100`;
- capture loss is `0`;
- visibility loss is `0`;
- aggregation loss is `0`;
- production autonomy remains blocked by knowledge quality, not by missing planner/execution architecture.

## Decision

V7 will treat routing knowledge quality as a first-class canonical concept.

Knowledge quality is evaluated on nine dimensions:

1. Freshness;
2. Coverage;
3. Correctness;
4. Consistency;
5. Diversity;
6. Source Confidence;
7. User Impact Relevance;
8. Service Relevance;
9. Actionability.

Every knowledge object can be classified into one of five maturity stages:

```text
RAW_OBSERVATION
  -> STABLE_SIGNAL
  -> CONFIRMED_KNOWLEDGE
  -> ACTIONABLE_KNOWLEDGE
  -> AUTONOMY_GRADE_KNOWLEDGE
```

Only autonomy-grade knowledge may support operator-free autonomous action, and only inside an explicitly certified authority tier.

## Alternatives Considered

| Alternative | Rejected Because |
| --- | --- |
| Count rows as confidence | Row count does not prove freshness, correctness, attribution, service relevance, or actionability. |
| Create another trust/confidence audit | Trust and evidence saturation are already documented; the missing piece is knowledge quality. |
| Change floors or formulas | This would hide the quality problem instead of improving knowledge. |
| Create a new planner or truth source | V7 already has canonical owners; new owners would fragment truth. |
| Treat operator comparison as primary knowledge | Operator context is secondary supervised evidence only. |

## Consequences

1. Future autonomy phases must identify which knowledge object is weak and which quality dimension blocks it.
2. Reports must stop saying only "more evidence needed"; they must name freshness, coverage, correctness, consistency, diversity, source confidence, user impact relevance, service relevance, or actionability.
3. Planner and autonomy gates remain unchanged until a later implementation phase explicitly changes behavior.
4. The next safe implementation phase is a read-only quality/maturity read model through existing owners.
5. Service/user/SLA fit, recovery admission, suitability outcome closure, freshness/actionability, anti-flap knowledge, and autonomous rollback certification are P0 knowledge gaps.

## Affected Modules

Documentation only in this phase:

- `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`
- `docs/reports/V7_KNOWLEDGE_QUALITY_MODEL_REPORT.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`

Future read-only implementation should reuse existing owners:

- `admin_core/autonomy_trust_acceleration.py`
- `admin_core/intelligence_platform.py`
- `admin_core/intelligence_workers.py`
- `admin_core/operator_execution_pipeline.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `tools/v7-intelligence-snapshot-refresh`

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`
- `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`

## Related Reports

- `docs/reports/V7_IDEAL_AUTONOMOUS_ROUTING_SYSTEM_MODEL_REPORT.md`
- `docs/reports/V7_KNOWLEDGE_QUALITY_MODEL_REPORT.md`
- `docs/reports/AUTONOMY_EVIDENCE_SATURATION_MODEL_REPORT.md`
- `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`
