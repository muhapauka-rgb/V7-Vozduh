# Z9 Evidence 02 - Local Owner And Duplication Audit

## Canonical Runtime Owner

`tools/v7-users-autoswitch`

## Canonical Scheduler

`systemd/v7-users-autoswitch.service`

```text
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

`systemd/v7-users-autoswitch.timer`

```text
OnUnitActiveSec=20s
Unit=v7-users-autoswitch.service
```

## Canonical Audit Owner

`tools/runtime-support/v7-audit-log`

## Canonical Closure Owner

`admin/v7-admin-api`

Closure store:

```text
CLOSURE_STORE_FILE = STATE_DIR / "closure-records.jsonl"
```

Closure API:

```text
/api/actions/closure-set
```

## Existing Alternate Execution Paths Found

| Path | Type | Z9 classification |
| --- | --- | --- |
| `/api/actions/user-switch` -> `v7-user-switch` | Manual user movement | Bypass risk; do not use |
| egress delete/pause migration -> `v7-user-switch` | Egress lifecycle migration | Not Z9 runtime owner; do not use |
| `/api/actions/autoswitch-apply-guarded` -> `v7-users-autoswitch --mode guarded --apply --pretty` | Admin-triggered autoswitch apply | Existing path, but not verified live in Z9 |
| `systemd/drafts/v7-autoswitch-planner.service` -> `v7-users-autoswitch` | Planner refresh draft | Non-apply draft; not execution |
| direct `v7-user-switch` | Direct routing mutation | Forbidden by Z9 |

## Duplicate Path Verdict

Potential bypass paths exist in the codebase, but no duplicate Runtime Orchestrator was created by this block.

For Z9 execution, the only acceptable path remains the canonical runtime owner path after live verification. Because live verification did not pass, no path is safe to use.

