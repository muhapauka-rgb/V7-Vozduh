# Duplication Audit Report

## Duplicate Candidate Findings

| Candidate | Severity | Evidence | Verdict |
|---|---|---|---|
| New RI service history store | HIGH if created | Existing `ServiceHistoryStore` already derives from service matrix + quality summary | DO_NOT_CREATE |
| New service scoring model | HIGH if created | Existing `ServiceIntelligenceEngine`, `RoutingBrain`, native service suitability and snapshot workers | EXTEND existing only |
| New snapshot root/envelope | CRITICAL if created | Existing canonical root and envelope in `intelligence_snapshots.py`; production CONV.2 confirms root/files | DO_NOT_CREATE |
| New planner | CRITICAL if created | `tools/v7-users-autoswitch` owns runtime planner and selected moves | DO_NOT_CREATE |
| New governance authority | CRITICAL if created | Governance/approval packet ownership already exists outside RI | DO_NOT_CREATE |
| New trust model | MEDIUM/HIGH if created | `ExecutionTrustModel` and `trust-summaries` exist | EXTEND existing |
| New risk model | MEDIUM/HIGH if created | risk worker and `risk-summaries` exist | EXTEND existing |
| New channel quality history | HIGH if created | `v7-egress-quality-compact` owns summary/ring history | REUSE existing |
| New capacity forecast producer | LOW/MEDIUM if implementing existing contract | contract exists but current producer not production-confirmed | NEW_IMPLEMENTATION_ALLOWED only inside existing snapshot contract |
| New prediction producer | LOW/MEDIUM if implementing existing contract | contract exists; prediction foundation disabled | NEW_IMPLEMENTATION_ALLOWED only as advisory-only snapshot |
| New user-service snapshot producer | LOW/MEDIUM if implementing existing contract | `UserServiceWeights` and snapshot family exist | EXTEND existing contract |

## Duplicate Ownership Risk

Current duplicate creation risk for RI.4:

```text
MEDIUM
```

Reason:

Many building blocks already exist. The main risk is accidentally rebuilding service history, scoring, trust, risk, or planner logic instead of extending them.

## Hard Rule

RI.4 implementation must be an extension of existing owners:

- `admin_core.routing_intelligence`
- `admin_core.routing_brain`
- `admin_core.intelligence_workers`
- `admin_core.intelligence_snapshots`
- `tools/v7-users-autoswitch`

