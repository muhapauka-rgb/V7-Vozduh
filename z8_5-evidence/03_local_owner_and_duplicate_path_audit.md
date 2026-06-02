# Z8.5 Evidence 03 - Local Owner And Duplicate Path Audit

## Local Canonical Owners

| Capability | Local owner/path |
| --- | --- |
| Runtime owner | `tools/v7-users-autoswitch` |
| Scheduler service | `systemd/v7-users-autoswitch.service` |
| Scheduler timer | `systemd/v7-users-autoswitch.timer` |
| Audit owner | `tools/runtime-support/v7-audit-log` |
| Admin API | `admin/v7-admin-api` |
| Closure store default | `/opt/v7/egress/state/closure-records.jsonl` |
| Runtime state default | `/opt/v7/egress/state` |

## Local Service Definitions

`systemd/v7-users-autoswitch.service`:

```text
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

`systemd/v7-users-autoswitch.timer`:

```text
OnUnitActiveSec=20s
Unit=v7-users-autoswitch.service
```

## Duplicate / Alternate Execution Paths Found Locally

| Path | Behavior | Z8.5 classification |
| --- | --- | --- |
| `systemd/v7-users-autoswitch.service` | Canonical apply service definition | Candidate runtime owner, live not verified |
| `systemd/drafts/v7-autoswitch-planner.service` | Planner refresh only | Draft/non-active unless deployed |
| `admin/v7-admin-api` `/api/actions/autoswitch-apply-guarded` | Calls `v7-users-autoswitch --mode guarded --apply --pretty` | Existing admin apply surface, live not verified |
| `admin/v7-admin-api` `/api/actions/user-switch` | Calls `v7-user-switch` directly | Manual bypass risk for Z9; not canonical orchestrator path |
| egress pause/delete migration functions | Call `v7-user-switch` | Egress lifecycle path, not Z9 runtime owner |
| direct `v7-user-switch` | Direct routing mutation | Bypass risk; forbidden for Z9 |

## Duplicate Audit Verdict

Local duplicate/bypass-capable paths exist. Their production deployment and active/inactive status are UNKNOWN.
