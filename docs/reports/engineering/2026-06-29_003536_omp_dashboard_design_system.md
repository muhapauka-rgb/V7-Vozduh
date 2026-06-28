# OMP Dashboard Design System

Date: 2026-06-29 00:35:36

Task: OMP Dashboard Design System.

## UI Research

| Reference | Reused | Avoided |
| --- | --- | --- |
| Linear | Calm focused workspace, low noise, high polish. | Beauty without evidence trace. |
| GitHub Projects | Multiple synchronized views over one data model. | View config as second roadmap. |
| Stripe Dashboard | Clear home, navigation, search, operational hierarchy. | Business cards that imply authority. |
| Datadog | Dashboard grouping, widgets, operational drill-down. | Metric overload and duplicated dashboards. |
| Grafana | Panel discipline, dashboard reuse, drill-down. | Chart-first UI before certified chart read models. |
| Apple HIG / macOS / iOS | Clarity, hierarchy, legibility, spacing, accessible targets. | Decorative motion, weak contrast, tiny controls. |

Sources reviewed:

- https://linear.app/method
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/changing-the-layout-of-a-view
- https://docs.stripe.com/dashboard/basics
- https://docs.datadoghq.com/dashboards/
- https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/
- https://developer.apple.com/design/human-interface-guidelines

## Design Principles

Minimal, elegant, calm, fast, low-noise, source-owned, progressively disclosed, modern dark/light mode, and read-only.

## Dashboard Philosophy

Dashboard answers: where are we, why are we here, what is blocked, what was produced, what comes next, why, what changed today, and current maturity.

## Operator Mockup

Operator Home Screen:

`Header -> Status Strip -> Progress Row -> Current Stage -> Capability -> Stop Gates -> Recommendation/Risks -> Expandable Details`.

Current basis: B1 produced Liveness Evidence Aggregation, B2 is current, Production Maturity is `37.9 / 100`, RT2 is complete, EI is canonical, runtime apply/automation/authority/user movement remain blocked.

## Engineering Mockup

Engineering View:

`Capability Production Graph -> Producer/Consumer Matrix -> Transition Contract -> RT2/EI/Maturity Panels -> Evidence -> Owners -> Blockers -> Expandable Technical Details`.

## Interaction Model

Default view is `OPERATOR_VIEW`.

`ENGINEERING_VIEW` is a synchronized mode over the same canonical data.

Cards expand to owner/evidence. Graph nodes highlight producer, produced capability, owner, consumers, unlocked stage, and blocked stages. Search spans step, capability, owner, evidence, gate, report, and canonical reference. Filters are Engineering-only by default.

## Canonical Deliverables

| Concept | Owner | Document updated | Report-only |
| --- | --- | --- | --- |
| Dashboard Design Principles | OMP | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | `FORBIDDEN` |
| Dashboard UX principles | Canonical Reference | `docs/reference/V7_CANONICAL_REFERENCE.md` | `FORBIDDEN` |
| Dashboard ownership | SYSTEM_MAP | `docs/reference/SYSTEM_MAP.md` | `FORBIDDEN` |
| Dashboard entry point | Current Program State | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | `FORBIDDEN` |

## Knowledge Preservation

Deleting this report does not remove dashboard philosophy, hierarchy, UX principles, navigation, or visual language.

Permanent knowledge lives in OMP, Canonical Reference, SYSTEM_MAP, and Current Program State.

## Files Changed

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reports/engineering/2026-06-29_003536_omp_dashboard_design_system.md`

## Files Intentionally Unchanged

- Runtime code.
- React/HTML/admin UI implementation.
- OMP data model.
- Dashboard read models.
- A5/B16 implementation.

## Final Verdict

OMP_DASHBOARD_DESIGN_SYSTEM_COMPLETE
