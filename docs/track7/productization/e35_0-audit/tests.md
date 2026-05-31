# E35.0 Tests / Static Checks

## Code Inspection

code_inspection_performed=true

Inspected:

- identity schema and upsert functions in `admin/v7-admin-api`
- service preferences storage/update functions
- service matrix normalization and route fitness
- proposal generation from service recommendations
- egress policy and suitability scoring
- admin Users/Channels/Routes/Settings surfaces
- autoswitch policy tests

## Admin Inspection

admin_inspection_performed=true

Performed by static inspection of current admin JS/HTML in `admin/v7-admin-api`.

Confirmed visible surfaces:

- `Пользователи` / `Организации`
- `Пользователи` / `Приоритеты`
- `Каналы` / `Сервисная матрица`
- `Маршруты` / route classes and modes
- `Настройки` / policy and route modes

## API Inspection

api_inspection_performed=true

Confirmed APIs/actions by code inspection:

- `/api/overview`
- `/api/policy`
- `/api/org-egress-policy`
- `/api/actions/org-egress-policy-update`
- `/api/actions/service-preferences-update`
- `/api/actions/service-aware-route-dry-run`
- `/api/actions/service-aware-apply-preview`
- `/api/actions/service-aware-live-rollout-preview`
- `/api/actions/service-aware-apply-guarded`

No API actions were executed for this audit.

## Consistency Review

consistency_review_performed=true

Main consistency finding:

- Admin required services are real and connected to service matrix/proposals.
- They are not yet a hard runtime access guarantee.

## No Mutation Verification

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false
autoswitch_apply_performed=false

Only read commands and documentation file writes were performed.

## git diff --check

git_diff_check_passed=true

Command:

`git diff --check`

Result:

No whitespace errors reported.

## Marker Scan

marker_scan_performed=true

Checked E35.0 audit artifacts for mutation markers and forbidden execution commands. Only descriptive mention of `v7-user-switch` appears in the pinning audit to explain existing current-assignment semantics; no command was executed or prescribed for this audit block.
