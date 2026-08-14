# PROGRAM A.3 Duplication Audit

Scope: local repository search over `tools`, `admin`, `systemd`, `docs`, and top-level reports.

## Findings

### Quality Floors

Definitions found:

- `tools/v7-users-autoswitch` default runtime policy.
- `admin/v7-admin-api` admin default policy and clamp/normalization layer.
- Historical reports documenting the same values.

Verdict:

- Duplicate definitions exist between runtime planner and admin defaults.
- They are value-aligned at `15.0/10.0/0.45`.
- Runtime planner is the authoritative execution implementation.
- Admin API is a configuration/read surface, not the execution owner.

Risk:

- Medium. Values are currently aligned, but semantics are not centrally documented as "hard eligibility" versus "migration threshold."

### Eligibility Logic

Definitions found:

- Runtime autoswitch candidate gates in `tools/v7-users-autoswitch`.
- Admin route candidate scoring in `admin/v7-admin-api`.

Verdict:

- The admin route scorer is not a duplicate runtime planner, but it uses related health/service concepts with different semantics.
- Runtime planner hard-blocks non-OK/WARN severity.
- Admin route scorer penalizes non-OK/WARN severity.

Risk:

- Medium. Operator-facing admin scoring can suggest a channel is degraded-but-rankable while runtime planner makes it completely ineligible.

### Migration Thresholds

Definitions found:

- Runtime `DEFAULT_SWITCH_POLICY` and `_beats_current`.
- Admin policy defaults and clamps.

Verdict:

- Values are aligned.
- No separate execution path was found.

Risk:

- Low.

### Reservation Logic

Definitions found:

- Runtime parser and planner gates.
- Historical E11 reports defining canary reservation enforcement.
- Admin metadata surfaces.

Verdict:

- Runtime planner is authoritative.
- Reservation behavior matches documented intent.

Risk:

- Low. WireGuard remains correctly blocked unless reservation is cleared by governance.

### Route-Class And Service Fitness

Definitions found:

- Runtime planner service gates.
- Admin API service matrix and route candidate scoring.
- Historical routing/control model docs.

Verdict:

- Admin is a preview/observability/control surface.
- Runtime autoswitch remains authoritative for movement.

Risk:

- Medium. The planner and admin scorer share concepts but not identical hard/soft boundaries.

## Single Authoritative Implementation

For Program A runtime movement:

- Authoritative policy executor: `tools/v7-users-autoswitch`
- Authoritative selected moves source: planner output from `tools/v7-users-autoswitch`
- Authoritative governance barrier: restore barrier fields in planner safety output
- Non-authoritative evidence source: targeted raw benchmark probe
- Non-authoritative UI/read source: `admin/v7-admin-api`

## Duplicate Truth Risk

The main risk is not a duplicate execution path. It is semantic drift between:

- runtime hard eligibility gates,
- admin/operator scoring semantics,
- documentation that sometimes says "quality floor" without specifying whether it is an absolute eligibility floor or migration threshold,
- raw benchmark evidence that is not consumed by canonical eligibility.

