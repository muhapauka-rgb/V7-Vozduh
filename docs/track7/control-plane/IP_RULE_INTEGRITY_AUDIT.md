# IP Rule Integrity Audit

This audit is read-only. No `ip rule` was added, deleted, replaced, or repaired.

## Expected Rules

For every enabled user:

```text
from <user-ip> lookup <user-table>
```

## Actual Rules

Stable pre-check and post-check samples contained all expected enabled-user rules:

```text
100:  from 10.0.0.2 lookup 100
101:  from 10.0.0.3 lookup 101
104:  from 10.0.0.6 lookup 104
1000: from 10.7.0.2 lookup 1000
1001: from 10.7.0.3 lookup 1001
1002: from 10.7.0.4 lookup 1002
1003: from 10.7.0.5 lookup 1003
1004: from 10.7.0.6 lookup 1004
1006: from 10.7.0.8 lookup 1006
1007: from 10.7.0.9 lookup 1007
1008: from 10.7.0.10 lookup 1008
1009: from 10.7.0.11 lookup 1009
1010: from 10.7.0.12 lookup 1010
1011: from 10.7.0.13 lookup 1011
1012: from 10.7.0.14 lookup 1012
1013: from 10.7.0.15 lookup 1013
```

## Special Rules

```text
50: from all fwmark 0x77 lookup 70
55: from <server-public-ip> lookup main
60: from all uidrange 995-995 lookup 100
```

The uidrange rule sharing table `100` is a non-user special rule. It should be kept visible in future governance, but it was not identified as a direct conflict with user source-IP rules in this audit.

## Missing / Duplicate / Stale Rules

- Missing rules in stable `ip rule show`: none for enabled users.
- Duplicate user source rules: none observed.
- Stale disabled-user rule for table `1005`: none observed.
- Unexpected priorities: special rules exist but user rules match table numbers.

## Reconcile Mismatch

`v7-reconcile-check` reported missing rules while stable pre/post `ip rule show` showed those rules present. A targeted read-only shell grep for one reported missing rule returned `grep_rc=0`.

## Operational Risk

Current operational routing risk from IP rules appears low at the snapshot. The governance risk remains high because the checker can report FAIL under active control-plane conditions, making canary attribution unsafe.

```text
ip_rule_integrity=OK_AT_STABLE_SNAPSHOT
reconcile_rule_fail=intermittent_or_false_positive
leak_risk_from_missing_rules=not_proven
canary_status=NO-GO
```
