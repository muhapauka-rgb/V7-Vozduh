# P1.D/E Admin Surface

release_trust_admin_surface_defined=true

## Placement Rule

Release Trust integrates into current V7 Admin. No new top-level navigation item is introduced.

It appears in:

- `Главная`;
- `Проверки`;
- `Безопасность`.

## Existing Navigation Mapping

| Admin section | Operator meaning | Visible surface | Drawer entry |
| --- | --- | --- | --- |
| `Главная` | Is the current release trusted and matching runtime? | Release trust pill, runtime/release match summary, attention banner. | Open Release Drawer from release status. |
| `Проверки` | What release verification passed or failed? | Release verification check rows, runtime/release match checks. | Open drawer from check result. |
| `Безопасность` | Is rollback/recovery available for current release? | Security overview, rollback availability, backup/restore context. | Open drawer from release/rollback panel. |

## What Operator Sees

The operator sees:

- current release label;
- release status;
- certification status;
- rollback availability;
- runtime match;
- verification freshness;
- next safe action.

## What Stays Hidden By Default

The first view hides:

- commit hashes;
- signature internals;
- manifest internals;
- lineage internals;
- raw provenance payloads.

Advanced details can show redacted technical references for expert roles.

## Drawer Behavior

Release Drawer opens from existing status cards, checks and security surfaces.

It includes:

- current release;
- status;
- certification;
- rollback availability;
- verification history;
- recommended action;
- advanced details.

## Admin Surface Verdict

Release Trust is a safety/status surface in existing admin workflows, not a new admin section.
