# E35.0 Required Services Audit

## Scope

Audit question: do admin-selected required services match current routing/proposal logic, and do they guarantee access to those services.

## Storage

required_services_storage_exists=true

Current storage is `SERVICE_PREFS_FILE` read by `service_preferences_state()`.

Shape:

- `enabled`
- `users`
- per-user row:
  - `schema_version`
  - `services`
  - `updated`
  - `updated_by`

Updates are handled by `/api/actions/service-preferences-update`.

## Admin Surface

required_services_admin_surface_exists=true

In `Пользователи`, the table has a `Приоритеты` cell. Opening it shows drawer title `Приоритеты` with section `Обязательные сервисы`.

Known service groups include service names such as Telegram, Google/Auth, YouTube, Instagram, ChatGPT/Claude, WhatsApp, depending on configured catalog groups.

## Evaluation

required_services_evaluated=true

`service_recommendations(active_users, matrix, prefs)` evaluates each user's required services against `service-matrix.json`.

It computes:

- current channel OK/missing/failed
- candidate channels that satisfy all required services
- `KEEP_CURRENT`
- `SWITCH_AVAILABLE`
- `NO_EGRESS_MATCHES_REQUIRED_SERVICES`

Generated proposals use those recommendations:

- `SWITCH_AVAILABLE` can produce `MOVEMENT_PROPOSAL`
- no matching channel can produce `OBSERVATION`

## Runtime Guarantee

required_services_guarantee_access=false
required_services_create_auto_movement=false

Selecting required services in admin does not itself guarantee access and does not automatically move a user.

What it currently guarantees:

- the preference is stored
- the service matrix/recommendation layer can evaluate it
- proposals can surface mismatch or better channel
- service-aware previews/guarded actions can use it when explicitly invoked

What it does not yet guarantee:

- that the current channel is changed immediately
- that all movement APIs are hard-blocked if required services are unavailable
- that every runtime routing path enforces user-required services as an authority

## Audit Verdict

required_services_audit_complete=true
storage=true
admin_ui=true
proposal_integration=true
hard_runtime_enforcement=PARTIAL
operator_expectation_gap=true

## E35 Implication

Admin wording should avoid implying "guaranteed access" until E35 adds hard suitability gates. The accurate current wording is:

"Обязательные сервисы используются для оценки канала и предложений. Перенос выполняется только через отдельное подтвержденное governance-действие."
