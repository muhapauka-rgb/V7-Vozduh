# CTR.I1 Truth Source And Duplication Audit

Canonical CTR truth source:

- `trust-evolution-summaries.channel_trust_recovery`

Reused readers:

- `tools/v7-users-autoswitch` reads existing runtime snapshot family `trust-evolution-summaries`.
- `admin_core/operator_decision_surface.py` reads existing `trust-evolution-summaries.channel_trust_recovery`.
- `admin_core/operator_execution_pipeline.py` receives CTR evidence from the existing operator decision row.

No new systems created:

- new planner: false
- new governance path: false
- new runtime authority: false
- new snapshot family: false
- new truth source: false
- new routing system: false

Implementation boundary:

- CTR soft influence is computed as advisory fields:
  - `soft_adjustment`
  - `advisory_score`
  - `recommended_action`
  - `blocked_actions`
- CTR soft influence is not applied to runtime score.
- CTR hard gate is not applied.
- CTR target suppression is not applied.
