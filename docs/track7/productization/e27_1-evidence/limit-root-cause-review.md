# E27.1 Limit Root-Cause Review

`capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_WITH_METADATA_DRIFT`

## Finding

The execution target carried `soft_limit=1 hard_limit=1` in `egress.registry`, inherited from the first one-user governed movement target setup.

Runtime load and quality sources did not agree with this one-user limit:

```text
egress-load.state:
amneziawg-exec-20260528-10-8-1-14_users=0
amneziawg-exec-20260528-10-8-1-14_soft_limit=1
amneziawg-exec-20260528-10-8-1-14_hard_limit=2
amneziawg-exec-20260528-10-8-1-14_load_status=OK
```

Fresh quality state also showed headroom:

```text
stability.state:
avg_mbps=65.7833
min_mbps=55.30
stability=0.840639
samples=30
```

Readiness helper explicit target mode returned GO before requalification.

## Classification

The limit was not classified as a throughput, stability, or diagnose failure.

```text
GOVERNANCE_LIMIT_ONLY_WITH_METADATA_DRIFT
```

## Consequence

Target metadata could be safely requalified from `hard_limit=1` to `hard_limit=2` only after target-local two-probe validation confirmed quality above floor and all runtime checkers stayed OK.

