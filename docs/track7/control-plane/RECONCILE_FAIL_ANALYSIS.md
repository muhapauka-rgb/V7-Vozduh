# Reconcile FAIL Analysis

This analysis uses Block E2 read-only output and repo-side source inspection only. No reconcile repair, routing sync, ip rule change, route change, or runtime mutation was performed.

## Observed Failure

`v7-reconcile-check` returned:

```text
V7_RECONCILE_RESULT=FAIL
errors=11
```

The errors were missing exact per-user rules:

```text
user=10.0.0.3 missing ip rule lookup table 101
user=10.0.0.6 missing ip rule lookup table 104
user=10.7.0.2 missing ip rule lookup table 1000
user=10.7.0.4 missing ip rule lookup table 1002
user=10.7.0.5 missing ip rule lookup table 1003
user=10.7.0.8 missing ip rule lookup table 1006
user=10.7.0.10 missing ip rule lookup table 1008
user=10.7.0.11 missing ip rule lookup table 1009
user=10.7.0.12 missing ip rule lookup table 1010
user=10.7.0.14 missing ip rule lookup table 1012
user=10.7.0.15 missing ip rule lookup table 1013
```

Candidate `10.7.0.13 table=1011` was not listed among these errors.

## What The Checker Requires

Repo-side lineage copy of `v7-reconcile-check` requires exact output from:

```text
ip -4 rule show | grep "from <user-ip> lookup <table>"
```

It also checks assignment file presence, live WireGuard allowed IPs, and route-get device match.

## Conflicting Read-Only Evidence

Other checks were OK at the same sample:

```text
V7_KILLSWITCH_CHECK=OK
V7_USER_ROUTE_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Those checks showed route-get and table defaults matching expected egress devices for enabled users, including the candidate.

## Root Cause Assessment

The most likely root cause is a strict-contract mismatch around exact per-user `ip rule` presence. It is not yet proven to be a datapath outage, because route-get/table/default checks passed. It is also not safe to dismiss as harmless, because `v7-reconcile-check` and `v7-reconcile-repair-preview` both treat missing rules as repair-worthy.

Classification:

```text
real_status=unresolved
datapath_outage_proven=false
strict_reconcile_contract_failed=true
canary_blocker=true
```

## Why This Blocks Canary

A one-user canary relies on knowing whether the live routing model is consistent before movement. If one checker says policy rules are missing for many users, the operator cannot prove that post-canary route behavior is attributable only to the canary.

## Required Future Read-Only Confirmation

Before canary, collect:

- full `ip -4 rule show`;
- full `ip -4 route show table <candidate_table>`;
- exact route-get for candidate before canary;
- exact output from `v7-reconcile-check`;
- exact output from `v7-user-route-check`;
- decision whether the reconcile rule check is stale/too strict or whether rules must be repaired under separate approval.

## Forbidden In This Block

- no `v7-reconcile-repair-preview` against live runtime if it could imply repair execution;
- no `v7-user-reconcile-apply`;
- no `v7-routing-sync`;
- no ip rule or route mutation.

## Verdict

`v7-reconcile-check=FAIL` remains a hard NO-GO blocker until explained or repaired through a separate approved flow.
