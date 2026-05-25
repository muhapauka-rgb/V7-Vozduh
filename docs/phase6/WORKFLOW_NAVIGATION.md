# V7 Phase 6 Workflow-Based Navigation

## Purpose

Navigation should follow operator jobs, not raw runtime objects.

## Primary Workflows

- Overview;
- Users;
- Channels;
- Routing;
- Diagnostics;
- Incidents;
- Security;
- Maintenance;
- Settings.

## Current Navigation Mapping

Current `admin-v2` tabs:

- Главная -> Overview;
- Пользователи -> Users;
- Каналы -> Channels;
- Маршруты -> Routing;
- Проверки -> Diagnostics;
- Безопасность -> Security/Maintenance;
- Настройки -> Settings/Policy;
- Логи -> Incidents/Logs.

Identity exists as a page section but is not in the visible primary tab list. Future navigation should expose identity through Users/Access workflows rather than raw database tables.

## Navigation Rule

Every navigation item must answer an operator question:

- Who is affected?
- Which channel is unhealthy?
- Is routing safe?
- What incident needs action?
- Which maintenance action is safe?

