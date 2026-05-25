# V7 Phase 0 UI Philosophy

Purpose: preserve calm operator UX while future observability and diagnostics grow.

## Core Principle

V7 UI is for calm operation, not spectacle and not telemetry dumping.

The operator should understand:

- current state;
- user impact;
- likely cause;
- recommended bounded action;
- whether the system is safe.

## Information Hierarchy

The UI should show information in this order:

1. Overall state.
2. Impact on users/channels/services.
3. Active incidents or warnings.
4. Grouped diagnostics.
5. Drill-down technical details.
6. Raw telemetry only when explicitly opened.

## Overview-First UX

The first screen should answer:

- Is the platform safe?
- Are users affected?
- Are route classes healthy?
- Is autoswitch stable?
- Is the kill switch OK?
- Are there actions that need operator attention?

It should not start with:

- giant tables;
- raw logs;
- topology diagrams;
- every metric at once.

## Grouped Visibility

Diagnostics should be grouped by operator question:

- Users: who is impacted?
- Channels: which egress is degraded?
- Routing: is datapath policy correct?
- Safety: is kill switch/reconciliation OK?
- Provisioning: are drafts/quarantine/rollbacks clean?
- Events: what changed recently?

## Progressive Disclosure

Every complex object should have:

- summary;
- reason;
- suggested action;
- drill-down.

Raw command output belongs behind drill-down, not in the primary view.

## Minimal Visual Noise

Avoid:

- blinking statuses;
- large metric walls;
- topology spaghetti;
- Grafana-style dense dashboards;
- duplicate warnings in multiple panels;
- ungrouped logs.

Prefer:

- small status summaries;
- stable severity language;
- grouped cards or sections;
- short explanations;
- details drawers.

## Operator Workflows

The UI should support workflows:

- diagnose a user;
- assess a degraded channel;
- quarantine or drain egress;
- verify direct/RU behavior;
- review autoswitch plan;
- create or revoke profile;
- inspect audit trail.

It should not force the operator to infer workflows from raw metrics.

## UI Governance

Any new UI feature must answer:

- What operator question does this solve?
- Is it summary-first?
- Can details be hidden until needed?
- Does it reduce firefighting?
- Does it preserve calm UX?

