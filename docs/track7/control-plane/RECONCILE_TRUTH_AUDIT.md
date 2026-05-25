# Reconcile Truth Audit

Evidence was collected read-only on 2026-05-25 around 00:09-00:10 MSK. No `v7-routing-sync`, `v7-user-switch`, autoswitch apply, reconcile repair, route mutation, ip rule mutation, nft mutation, service restart, chmod/chown, cleanup, deploy, or canary was executed by this block.

## Evidence Files

```text
/private/tmp/v7-e4-live-audit-nontty.txt
/private/tmp/v7-e4-reconcile-resample.txt
/private/tmp/v7-e4-grep-debug.txt
```

## Current Reconcile Result

`v7-reconcile-check` still reports FAIL:

```text
V7_RECONCILE_RESULT=FAIL
```

The non-TTY full audit reported 6 missing-rule errors. A short immediate resample reported 10 missing-rule errors.

## Expected User Tables

Registry at audit time had all enabled users on `vless`, with tables:

```text
100, 101, 104, 1000, 1001, 1002, 1003, 1004, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013
```

Disabled user `10.7.0.7` uses table `1005` and is intentionally out of the enabled routing set.

## Actual IP Rules

`ip -4 rule show` before and after reconcile contained the expected enabled-user rules, for example:

```text
100:  from 10.0.0.2 lookup 100
104:  from 10.0.0.6 lookup 104
1000: from 10.7.0.2 lookup 1000
1011: from 10.7.0.13 lookup 1011
1013: from 10.7.0.15 lookup 1013
```

Targeted grep for a reconcile-reported failing user also succeeded:

```text
pattern=<from 10.0.0.6 lookup 104>
grep_rc=0
```

## Actual Route Tables

Every enabled-user table had:

```text
default dev tun0 table <table> scope link
```

This matches the registry state because all enabled users were assigned to `vless`, whose egress interface is `tun0`.

## Reality Checks

```text
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Each of those checks reported 16 enabled-user routes OK.

## Truth Classification

The current FAIL is not supported by stable pre/post `ip rule show` snapshots. The strongest explanation is an intermittent reconcile/checker false-positive or moving-target race while active control-plane authority is present.

Classification:

```text
stable_rules_present=true
route_tables_present=true
datapath_checks_ok=true
reconcile_check_fail=true
dangerous_missing_rules_proven=false
checker_or_race_false_positive_likely=true
canary_status=NO-GO
```

## Why Canary Still Blocks

Even if the current FAIL is partially false-positive, the control plane is not quiet: autoswitch authority is active and registry state changed since Block E2. A one-user canary needs a stable observation window. Until reconcile can run cleanly or the false-positive condition is documented under a quiet autoswitch hold, canary remains NO-GO.
