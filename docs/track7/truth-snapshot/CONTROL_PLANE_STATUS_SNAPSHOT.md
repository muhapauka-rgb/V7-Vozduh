# Control Plane Status Snapshot

Evidence source:

```text
tools/v7-control-plane-governance-check --pretty
docs/track7/control-plane/e8-evidence/*
docs/track7/truth-snapshot/evidence/section-processes.txt
```

## Current Status

```text
current_canary_status=NO-GO
current_canary_integrity_status=NO-GO
current_quiet_window_status=unstable
rehearsal_executed=True
rehearsal_aborted=True
autoswitch_restored=True
quiet_window_verified=False
reconcile_under_quiet=NOT_SAMPLED_ABORTED
current_operational_status=rehearsal_aborted_restored
execution_allowed_now=False
```

## Main Blocker

Autoswitch authority is not fully modeled. A non-systemd loop invokes `v7-users-autoswitch` every 30 seconds. That loop invalidates quiet-window attribution and blocks canary.

## Blast Radius

Biggest current blast radius:

- autoswitch user movement;
- routing-sync all-enabled-user route/rule mutation;
- policy/proxy/Direct/RU apply;
- kill switch rebuild/disable;
- broad rollback apply.

## Verdict

Control plane is governance-rich but execution-sensitive. It is not ready for canary or apply actions.
