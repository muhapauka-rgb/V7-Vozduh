# API.1 Decomposition Risk Matrix

## Highest-Risk Refactors

| Refactor | Risk | Failure mode | Mitigation |
|---|---|---|---|
| Extract `Handler.do_POST` | CRITICAL | CSRF, auth, role, safe-mode, confirm, command invocation, or response behavior changes | Freeze all action contracts first; extract metadata before code |
| Move `run_action` | CRITICAL | Runtime mutation behavior changes or unlogged commands | Keep in monolith until execution block certification |
| Move user switch/autoswitch apply | CRITICAL | User movement or planner/apply drift | Do not touch in API.2 |
| Move rollback apply | CRITICAL | Recovery path broken | Preview-only extraction first |
| Move policy/direct/trusted RU apply | HIGH/CRITICAL | Routing behavior changes | Read-only summaries only |
| Move `audit_admin` | HIGH | Missing/incorrect audit records | Extract readers only |
| Move closure writer | HIGH | Broken operator closure accountability | Extract readers only |
| Split auth/session/RBAC | HIGH | privilege or login behavior drift | Dedicated security contract block |
| Split `html_page_v2` first | HIGH | UI/action contract drift and broken operator workflows | Freeze APIs first |
| Move identity/profile issuance | HIGH | access/profile delivery breakage | Read-only identity views first |

## Highest-Risk Truth Sources

| Truth source | Risk | Reason |
|---|---|---|
| `/opt/v7/egress/state/users.registry` | CRITICAL | User routing and movement authority |
| `/opt/v7/egress/state/egress.registry` | CRITICAL | Channel lifecycle and routing authority |
| `/etc/v7/policy.json` | HIGH | Route/policy behavior |
| `/etc/v7/org-egress-policy.json` | HIGH | Organization/group routing behavior |
| `/etc/v7/direct/domains.conf` | HIGH | Direct routing behavior |
| `/opt/v7/admin/v7-identity.db` | HIGH | Identity/access lifecycle |
| `/opt/v7/audit/audit.jsonl` | HIGH | Audit/accountability |
| closure store | HIGH | Operator closure/audit linkage |
| `/etc/v7/admin/auth.json` | HIGH | Admin access/security |
| `/etc/v7/admin/safe-mode.json` | HIGH | Safety gating |

## Endpoint Group Risk

| Endpoint group | Risk | API.2 decision |
|---|---|---|
| public pages and profile delivery | MEDIUM/HIGH | Do not extract first |
| `/api/overview` | MEDIUM/HIGH | Extract sub-builders only after schema snapshots |
| operator read-only endpoints | LOW/MEDIUM | Good extraction area |
| audit/evidence read endpoints | LOW/MEDIUM | Good extraction area |
| egress preview endpoints | MEDIUM | Pure parsers only |
| egress apply/provision endpoints | HIGH/CRITICAL | Do not extract first |
| user movement endpoints | CRITICAL | Do not extract first |
| autoswitch apply endpoints | CRITICAL | Do not extract first |
| governance preview endpoints | MEDIUM | Read-only extraction only |
| governance/action endpoints | HIGH | Do not extract first |
| rollback endpoints | HIGH/CRITICAL | Preview-only first; apply stays |
| Trusted RU/direct policy endpoints | HIGH | Read-only summaries first |

## Ownership Overlap Risk

| Overlap | Risk | Resolution |
|---|---|---|
| admin audit writer vs runtime audit writer | MEDIUM | Keep separate writers; share read-only views only |
| admin closure writer vs planner closure target metadata | MEDIUM | Keep admin closure owner; planner only emits target metadata |
| admin registry wrapper vs tool-local registry parsers | MEDIUM | Reuse `admin_core.registry_readers` for admin only first |
| admin service summaries vs service matrix tools | MEDIUM | Separate cache producer from view reader |
| admin RI display vs RI planner authority | MEDIUM | Admin displays RI; does not decide |
| admin rollback wrapper vs runtime rollback tools | HIGH | Runtime tools remain authority |

## Certification Risk Verdict

The risk profile supports API.2 only as a read-only extraction. Any mutation-bearing decomposition requires separate certification blocks and stronger contract coverage.
