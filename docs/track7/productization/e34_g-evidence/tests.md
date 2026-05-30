# E34.G Tests

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

## Results

| Check | Command | Result | Notes |
| --- | --- | --- | --- |
| Marker scan | `rg -n "admin_integration_architecture_defined=true\|current_admin_loaded=true\|architecture_surface_map_defined=true\|proposal_ux_defined=true\|navigation_integration_defined=true\|progressive_disclosure_defined=true\|complexity_hidden_by_default=true" BLOCK_E34_G_ADMIN_INTEGRATION_ARCHITECTURE_REPORT.md docs/track7/productization/e34_g-evidence` | PASS | Required markers present. |
| Navigation consistency scan | `rg -n "No new top-level sections\|Главная\|Пользователи\|Каналы\|Маршруты\|Проверки\|Безопасность\|Настройки\|Логи\|What happened\\?\|Who is affected\\?\|What should I do\\?" BLOCK_E34_G_ADMIN_INTEGRATION_ARCHITECTURE_REPORT.md docs/track7/productization/e34_g-evidence` | PASS | Current navigation preserved and operator questions present. |
| Operator overload scan | `rg -n "Operators should not need to think\|backend architecture terms\|complexity_hidden_by_default=true\|Hide:" docs/track7/productization/e34_g-evidence` | PASS | Architecture internals are hidden by default. |
| Progressive disclosure scan | `rg -n "Summary\|Explanation\|Operational detail\|Expert diagnostics\|Hidden By Default\|Shown By Default" docs/track7/productization/e34_g-evidence/progressive-disclosure-model.md docs/track7/productization/e34_g-evidence/operator-surface-levels.md` | PASS | Four surface levels and hide/show rules defined. |
| No runtime/user/routing mutation scan | `rg -n "runtime_mutation_performed=true\|user_movement_performed=true\|routing_mutation_performed=true\|Autoswitch apply performed manually: YES\|Canary performed: YES\|Cohort performed: YES" BLOCK_E34_G_ADMIN_INTEGRATION_ARCHITECTURE_REPORT.md docs/track7/productization/e34_g-evidence` | PASS | No unsafe mutation markers found. |
| Git diff whitespace check | `git diff --check` | PASS | No whitespace errors. |

## Warnings

- This block defines architecture-to-admin integration only. It does not implement UI components.
- Proposal card shape, expert diagnostics role, installer entrypoint, release/provenance drawer placement and evidence bundle component remain implementation decisions.
