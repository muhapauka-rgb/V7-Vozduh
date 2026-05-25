# V7 Phase 6A Future Complexity Protection

## Purpose

The admin must not grow a new page or widget for every new platform capability.

## IA Review Gate

Every new UI feature must answer:

- which operator workflow owns it;
- which diagnostics group owns it;
- which information level it belongs to;
- what summary appears before detail;
- what gets hidden until drill-down;
- what dangerous action preview is required;
- how it scales to 50 channels and 500 users.

## Navigation Rule

Do not add a primary navigation item unless it represents a durable operator workflow.

Preferred workflow buckets:

- Users;
- Channels;
- Routing;
- Diagnostics;
- Incidents/Logs;
- Security;
- Maintenance/Settings.

## Anti-Sprawl Rule

New telemetry belongs in an existing diagnostics group unless it changes operator behavior.

## Feature Acceptance Rule

A feature that increases operator anxiety or cognitive load is not Phase 6A-compatible, even if the data is technically useful.

