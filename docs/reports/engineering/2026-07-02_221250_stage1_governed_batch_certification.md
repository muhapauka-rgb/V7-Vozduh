# Stage 1 Governed Batch Certification

Timestamp: 2026-07-02 22:12:50 Asia/Bangkok

Verdict: STAGE_1_FAILED

Failure phase: PRECHECK

## Mission

Certify Stage 1 governed batch evacuation for active failed-source incident:

```text
incident_source = openvpn-1779388847-d2ad7c
requested max_users = 5
```

## Result

Stage 1 certification was not executed.

Reason:

```text
production_canonical_ladder_mismatch
```

Production currently runs runtime commit:

```text
e390d924987f3283b2424deb133a4bbf963c2b7a
```

Production `/usr/local/bin/v7-users-autoswitch` still contains the pre-correction ladder:

```text
CANARY      = 1
SMALL_BATCH = 2
MEDIUM_BATCH = 5
LARGE_BATCH = 10
POOL        = 25
```

Production binary does not contain:

```text
XLARGE_BATCH
FULL_INCIDENT
```

Local canonical branch contains the corrected ladder, but it was not deployed in this task.

## Required Precheck

Expected canonical ladder:

```text
CANARY        = 1
SMALL_BATCH   = 5
MEDIUM_BATCH  = 10
LARGE_BATCH   = 25
XLARGE_BATCH  = 50
FULL_INCIDENT = remaining affected users on the same active failed-source incident
```

Precheck status:

```text
FAILED
```

## Authority Budget

Production `/etc/v7/policy.json` authority budget:

```json
{
  "authority_class": "POOL",
  "certified_authority_class": "POOL",
  "authority_lifecycle_state": "PROMOTED",
  "current_allowed_user_budget": 25,
  "next_allowed_user_budget": 25
}
```

This is not CANARY=1. However, because production still uses the accidental pre-canonical ladder, the Stage 1 certification was stopped before movement.

## Production Entrypoint

Production systemd governed heartbeat remains one-user bounded:

```text
ExecStart=/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

No timer was changed.

No production behavior was changed.

## Remaining Affected Users

Read-only evidence from exact files:

```text
/opt/v7/egress/state/user-10.7.0.*.assign
```

Users still assigned to `openvpn-1779388847-d2ad7c`:

```text
10.7.0.10
10.7.0.11
10.7.0.12
10.7.0.13
10.7.0.15
10.7.0.2
10.7.0.6
10.7.0.8
10.7.0.9
```

Remaining count:

```text
9
```

## Certification Fields

Selected users:

```text
[]
```

Moved users:

```text
[]
```

Moved user count:

```text
0
```

Verification result:

```text
NOT_RUN
```

Rollback result:

```text
NOT_RUN
```

Approved Plan Lock:

```text
NOT_RUN
```

Restore Barrier:

```text
NOT_RUN
```

Runtime Apply:

```text
NOT_RUN
```

## Production Impact

Deploy performed:

```text
NO
```

Production movement performed:

```text
NO
```

Users moved:

```text
0
```

Certification state changed:

```text
NO
```

Broad automation enabled:

```text
NO
```

Stage 2 enabled:

```text
NO
```

## Next Stage Recommendation

Do not run Stage 1 movement until production runtime is aligned with the canonical ladder correction.

Required next action:

```text
safe deploy canonical ladder correction, then rerun Stage 1 certification precheck
```

## Final Verdict

STAGE_1_FAILED
