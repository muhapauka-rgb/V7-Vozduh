# BLOCK E34.G Admin Integration Architecture Report

e34_g_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

admin_integration_architecture_defined=true

current_admin_loaded=true
architecture_surface_map_defined=true
operator_surface_levels_defined=true
proposal_ux_defined=true
recovery_surface_defined=true
installer_surface_defined=true
navigation_integration_defined=true
progressive_disclosure_defined=true
complexity_hidden_by_default=true

## Summary

E34.G defines how E32-E34 architecture appears inside the current V7 Admin.

The result is integration, not redesign. Capacity, Policy, Scheduler, Concurrency, Routing Intelligence, Backup, Release, Installer and Recovery appear inside existing operator workflows as status, blockers, proposals, evidence, previews, guided actions and verification.

## Navigation Decision

No new top-level sections are required.

Current navigation remains:

```text
Главная
Пользователи
Каналы
Маршруты
Проверки
Безопасность
Настройки
Логи
```

## Operator Surface

The admin should keep answering:

```text
What happened?
Who is affected?
What should I do?
```

It should not ask operators to navigate backend nouns such as Capacity, Scheduler, Policy, or Concurrency.

## Proposal UX

Proposal surfaces are defined for:

- `MOVEMENT_PROPOSAL`
- `EVACUATION_PROPOSAL`
- `REBALANCE_PROPOSAL`
- `OBSERVATION`

Each proposal must show impact, confidence, reason, affected users, next action, and safety boundary.

## Recovery and Installer UX

Recovery is integrated into `Безопасность`, `Главная`, `Проверки`, `Логи`, and object drawers.

Installer is integrated as a guided setup/deployability flow:

```text
NEXT -> CHECK -> NEXT -> CHECK -> READY
```

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- exact proposal card component shape
- expert diagnostics access role
- installer first-run entrypoint
- release/provenance drawer placement
- evidence bundle visual component
```

## Remaining Open Questions

- Should expert diagnostics require `admin` or `owner` role?
- Should release/provenance live primarily under `Безопасность` or inside a deployment drawer launched from `Проверки`?
- Should installer appear only in setup mode or remain available as a maintenance/deployability panel?
- What is the standard visual component for an evidence bundle?

recommended_next_program=E34.H_ARCHITECTURE_TO_IMPLEMENTATION_MAPPING

## Evidence Files

- `docs/track7/productization/e34_g-evidence/current-admin-intake.md`
- `docs/track7/productization/e34_g-evidence/architecture-surface-map.md`
- `docs/track7/productization/e34_g-evidence/operator-surface-levels.md`
- `docs/track7/productization/e34_g-evidence/proposal-ux-model.md`
- `docs/track7/productization/e34_g-evidence/recovery-ux-model.md`
- `docs/track7/productization/e34_g-evidence/installer-ux-model.md`
- `docs/track7/productization/e34_g-evidence/navigation-integration.md`
- `docs/track7/productization/e34_g-evidence/progressive-disclosure-model.md`
- `docs/track7/productization/e34_g-evidence/final-admin-integration-decision.md`
- `docs/track7/productization/e34_g-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
