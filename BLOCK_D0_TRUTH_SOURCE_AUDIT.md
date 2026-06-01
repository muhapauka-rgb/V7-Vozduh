# Block D0 Truth Source Audit

Project: V7 Vozduh

Block: D0 - Execution Cohort Decision Program

Date: 2026-06-01

## Capacity

Canonical source:

- `/opt/v7/egress/state/egress.registry`

Derived source:

- Runtime counts from `/opt/v7/egress/state/users.registry`

Presentation source:

- Block D0 reports

## Target Readiness

Canonical source:

- Egress registry fields plus runtime checker outputs

Derived source:

- Readiness helpers and observability summaries

Presentation source:

- Runtime audit and decision matrix

## Trust

Canonical source:

- `/opt/v7/egress/state/trusted-ru-decision.state`
- `/opt/v7/egress/state/trusted-ru-diagnostic.state`

Observed trust status:

- `overall=NEEDS_ATTENTION`
- `route_class=TRUSTED_RU_SENSITIVE`
- `route_class_status=NEEDS_TRUSTED_PATH`

## Execution Cohort

Canonical source:

- `/opt/v7/egress/state/users.registry`

Derived source:

- Route tables and checker outputs

Presentation source:

- Cohort observation report

## Verdict

No truth source conflict was found. Admin API health is a presentation/control-plane availability risk, not the canonical movement truth source.

