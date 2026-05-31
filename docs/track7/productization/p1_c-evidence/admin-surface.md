# P1.C Admin Surface

runtime_convergence_admin_surface_defined=true

## Placement Rule

Runtime Convergence integrates into current V7 Admin. No new top-level navigation item is introduced.

It appears in:

- `Главная`;
- `Проверки`;
- `Безопасность`.

## Existing Navigation Mapping

| Admin section | Operator meaning | Visible surface | Drawer entry |
| --- | --- | --- | --- |
| `Главная` | Is the running system trustworthy right now? | Runtime trust pill, release match summary, drift alert. | Open Runtime Convergence Drawer from status card. |
| `Проверки` | What convergence checks passed or failed? | Check result row, readiness/check map, verification details. | Open drawer from convergence check result. |
| `Безопасность` | Can backup/restore/release safety be trusted? | Security overview, backup/restore validation, safe-mode context. | Open drawer from security trust indicator. |

## What Operator Sees

The operator sees:

- status: OK, warning, drift, unknown or blocking;
- short summary;
- release match label;
- drift category;
- verification age;
- action impact;
- next safe action.

## What Stays Hidden By Default

The first view hides:

- raw hashes;
- fingerprint internals;
- lineage internals;
- raw file lists;
- low-level runtime diff payloads.

These are available in advanced details only when role, redaction and relevance allow them.

## Drawer Behavior

Runtime Convergence Drawer opens from existing cards, checks and security panels.

It shows:

- trust status;
- summary;
- drift details;
- verification history;
- recommended action;
- advanced details.

## Admin Surface Verdict

Runtime trust is a system status and safety gate. It belongs in existing overview/check/security workflows, not as a new navigation destination.
