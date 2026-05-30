# E34.G Installer UX Model

installer_surface_defined=true

## Installer Principle

Installer UX should follow the current admin philosophy:

```text
NEXT -> CHECK -> NEXT -> CHECK -> READY
```

It must feel like a guided operational checklist, not a separate product or wizard island.

## Recommended Surface

Installer appears in:

- setup / first-run mode before production readiness;
- `Безопасность` for deployability, backups, release and recovery readiness;
- `Проверки` for preflight and health check results;
- `Логи` for installer audit/provenance.

No new top-level `Installer` section is required for normal operation.

## Installer Steps

| Step | Operator sees | Hidden by default |
| --- | --- | --- |
| Discovery | Host, OS, network, permissions, dependencies. | Raw package checks. |
| Preflight | Pass/fail checklist with blockers. | Shell command output. |
| Release selection | Certified release identity and rollback release. | Manifest internals. |
| Configuration | Required inputs and validation. | Raw config templates. |
| Health check | Services, routes, backup readiness, runtime convergence. | Deep logs. |
| Certification | READY or blocked with next safe action. | Internal certification record fields. |

## Ready State

Installer may show `READY` only when:

- preflight passed;
- release provenance valid;
- backup readiness valid;
- health checks pass;
- runtime/repo convergence known;
- operator has next safe action.
