# V7 Phase 5 Commercial And Enterprise Foundation

## Purpose

Phase 5 prepares commercial readiness without implementing billing.

## Future Hooks

The architecture should leave room for:

- subscriptions;
- quotas;
- usage summaries;
- org limits;
- device limits;
- billing integration;
- SSO;
- delegated admins;
- managed deployments.

## Current Foundation

Current platform already has:

- organizations;
- groups;
- max devices;
- allowed users;
- access password;
- identity audit events;
- traffic database references;
- admin RBAC for identity actions.

## Non-Goals

Phase 5 must not add:

- billing engine;
- enterprise SSO implementation;
- delegated admin hierarchy;
- complex CRM workflows;
- noisy account dashboards.

## Design Rule

Commercial features must be policy hooks first.

They should not push complexity onto users or weaken routing safety.

