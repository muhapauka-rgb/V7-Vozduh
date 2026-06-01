# Block D2 Truth Source Audit

Date: 2026-06-01

## Runtime Truth Sources

| Truth | Source | Owner |
| --- | --- | --- |
| Users and current egress | `/opt/v7/egress/state/users.registry` | Runtime registry |
| Egress inventory and enabled status | `/opt/v7/egress/state/egress.registry` | Runtime registry |
| Autoswitch safety memory | `/opt/v7/egress/state/autoswitch-safety.json` | Autoswitch safety layer |
| Restore barrier | `/opt/v7/egress/state/autoswitch-restore-barrier.json` | Governance barrier |
| Policy | `/etc/v7/policy.json` | Runtime policy |
| Org policy | `/etc/v7/org-egress-policy.json` | Runtime policy |
| Service state | `/opt/v7/egress/state/service-matrix.json`, `telegram-sentinel.json` | Service observability |

## Parser Certification

The previous safety-review defect was not truth-source ambiguity. It was a parser mismatch:

- Live registry format: `key=value`
- Old safety-review expectation: first token as name, second token as value
- Result before remediation: false `enabled_egress=0`

After remediation, safety-review reads `enabled`, `id`, and `ip` from KV rows while preserving legacy two-column support.

## Certified Counts

- Safety-review enabled egress: `7`
- Egress registry rows: `7`
- Active enabled users: `18`
- Safety-review status: `ok`
- Critical findings: `0`

## Verdict

truth_sources_clean=true

