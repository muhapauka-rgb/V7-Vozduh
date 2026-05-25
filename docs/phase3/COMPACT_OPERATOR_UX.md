# V7 Phase 3 - Compact Operator UX

## Purpose

Observability must make the operator calmer and more effective.

The main page must not become a dashboard wall.

## Main Page Summary

Show only:

- system healthy/degraded;
- affected users;
- degraded channels;
- incidents requiring attention;
- autoswitch state;
- trusted RU status.

## Progressive Disclosure

All complex data is hidden by default and grouped logically.

Example:

- `2 degraded channels`
- click/drill-down
- service failures, route evidence, suggested action.

## Diagnostic Groups

Groups:

- Routing;
- Channels;
- Services;
- Users;
- Trusted RU;
- Autoswitch;
- Provisioning;
- Security;
- Direct routing.

## Decision Support

Each group should answer:

- what is wrong;
- who is affected;
- why likely;
- how severe;
- what safe action is next;
- rollback implications.

## Forbidden UX

Do not create:

- giant dashboards;
- metric walls;
- topology spaghetti;
- alert spam;
- raw command-first screens;
- unexplained red status.
