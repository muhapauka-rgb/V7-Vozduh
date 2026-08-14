# Block E8.6 - Reconcile Stable Fail Classification Report

Date: 2026-05-25.

Mode: read-only / diagnostic only.

Live mutation: forbidden.

## Executive Verdict

```text
reconcile_under_quiet_classification=CONFIRMED_FALSE_POSITIVE
false_positive_class=pipefail_grep_q_sigpipe
real_stable_runtime_mismatch_candidates=none for missing-ip-rule errors
canary_status=CONDITIONAL
execution_allowed_now=false
runtime_repair_needed_before_canary=false for this reconcile failure class
checker_fix_needed=true
bounded_waiver_acceptable_before_canary=true, if one-user scoped and all route/kill/provisioning checks pass
```

E8.6 classified the E8.5 `STABLE_FAIL` as a confirmed semantic false-positive in `v7-reconcile-check` for the specific error class:

```text
ERROR: user=<ip> missing ip rule lookup table <table>
```

The rules exist. Route tables exist. Route reality checks pass. Kill switch checks pass. Provisioning reconcile passes.

The false-positive is caused by `set -o pipefail` combined with `grep -q`:

```bash
if ! ip -4 rule show 2>/dev/null | grep -q "from $ip lookup $table"; then
  err "user=$ip missing ip rule lookup table $table"
fi
```

When `grep -q` finds a match and exits early, the upstream `ip` command can receive SIGPIPE. With `pipefail`, the pipeline can return `141`, so the checker reports a missing rule even though grep found the rule.

## Evidence

Evidence folder:

```text
docs/track7/control-plane/e8_6-evidence/
```

Files:

```text
reconcile-errors.txt
reconcile-source-analysis.txt
reconcile-expected-actual-matrix.md
checker-comparison.md
```

## Exact Failing Checks

E8.5 quiet-window samples:

```text
sample_A: errors=8, V7_RECONCILE_RESULT=FAIL
sample_B: errors=11, V7_RECONCILE_RESULT=FAIL
sample_C: errors=4, V7_RECONCILE_RESULT=FAIL
```

The exact complained users varied even though the quiet-window route/rule state stayed stable. This variation is consistent with the `pipefail`/SIGPIPE behavior and inconsistent with a stable set of missing rules.

Fresh E8.6 read-only run:

```text
primary errors=6
V7_RECONCILE_RESULT=FAIL
```

Fresh complained users:

```text
10.0.0.3 table 101
10.7.0.6 table 1004
10.7.0.11 table 1009
10.7.0.12 table 1010
10.7.0.13 table 1011
10.7.0.14 table 1012
```

In the same fresh run, `ip -4 rule show` contained all these rules.

## Pipefail Proof

Read-only probe:

```text
PATTERN=from 10.0.0.3 lookup 101
pipefail_rc_1=141
no_pipefail_rc_1=0
pipefail_rc_3=141
no_pipefail_rc_3=0
pipefail_rc_4=141
no_pipefail_rc_4=0
pipefail_rc_5=141
no_pipefail_rc_5=0
```

For the same existing rule, without `pipefail`, grep returns `0`. With
`pipefail`, the pipeline can return `141`. This confirms a checker semantic
false-positive.

## Affected Users / Tables

Observed false-positive candidates across E8.5/E8.6:

| User | Table | Actual ip rule | Route reality | Classification |
|---|---:|---|---|---|
| 10.0.0.2 | 100 | present | OK | false-positive candidate |
| 10.0.0.3 | 101 | present | OK | confirmed false-positive |
| 10.0.0.6 | 104 | present | OK | confirmed false-positive |
| 10.7.0.2 | 1000 | present | OK | false-positive candidate |
| 10.7.0.3 | 1001 | present | OK | false-positive candidate |
| 10.7.0.4 | 1002 | present | OK | false-positive candidate |
| 10.7.0.5 | 1003 | present | OK | false-positive candidate |
| 10.7.0.6 | 1004 | present | OK | confirmed false-positive |
| 10.7.0.8 | 1006 | present | OK | false-positive candidate |
| 10.7.0.9 | 1007 | present | OK | false-positive candidate |
| 10.7.0.10 | 1008 | present | OK | false-positive candidate |
| 10.7.0.11 | 1009 | present | OK | confirmed false-positive |
| 10.7.0.12 | 1010 | present | OK | confirmed false-positive |
| 10.7.0.13 | 1011 | present | OK | confirmed false-positive |
| 10.7.0.14 | 1012 | present | OK | confirmed false-positive |
| 10.7.0.15 | 1013 | present | OK | false-positive candidate |

Disabled user:

```text
10.7.0.7 table=1005 enabled=0
```

The disabled user is correctly skipped by the checker.

## Real Mismatch Candidates

No real stable runtime mismatch candidate was found for the current reconcile
failure class.

Evidence:

```text
all enabled user ip rules present=true
all enabled route table defaults present=true
v7-user-route-check=OK
v7-killswitch-check=OK
v7-provisioning-reconcile-check=OK
```

This does not prove all future routing changes are safe. It only classifies this
specific reconcile `missing ip rule` failure as checker semantics, not runtime
truth.

## Checker Comparison

| Checker | Result | Meaning |
|---|---|---|
| `v7-reconcile-check` | FAIL | semantic false-positive in missing rule check |
| `v7-user-route-check` | OK | per-user route reality works |
| `v7-killswitch-check` | OK | leak guard and route safety assumptions hold |
| `v7-provisioning-reconcile-check` | OK | provisioning/runtime consistency holds |

## Canary Implication

Can one-user canary be considered with waiver?

```text
yes, conditionally
```

A bounded waiver is acceptable for this reconcile failure class only if:

- the waiver explicitly names `v7-reconcile-check` `missing ip rule` as a confirmed checker false-positive;
- the target candidate user has an actual `ip rule` entry;
- target candidate route table default exists and points to expected device;
- `ip route get 8.8.8.8 from <candidate> iif wg0` uses expected device;
- `v7-user-route-check` is OK immediately before canary;
- `v7-killswitch-check` is OK immediately before canary;
- `v7-provisioning-reconcile-check` is OK immediately before canary;
- post-split autoswitch planner/apply authority is held for the canary window;
- rollback command is explicit;
- operator approval is one-user scoped.

Canary does not become GO automatically because:

- autoswitch timers are active outside approved hold windows;
- candidate/target readiness must be refreshed;
- target egress quality may still block;
- Trusted RU relevance must be checked for the candidate path;
- canary approval has not been granted.

## Recommended Next Step

Do not repair runtime for this reconcile failure.

Preferred next step:

```text
Prepare a one-user canary approval packet with an explicit reconcile false-positive waiver, or first patch v7-reconcile-check in a separate repo/runtime block to avoid pipefail+grep -q false failures.
```

Safer engineering path:

```text
Fix checker semantics before using v7-reconcile-check as a hard gate.
```

Operationally faster path:

```text
Use a bounded one-user waiver only if immediate canary planning is needed and all route/kill/provisioning checks pass inside a verified quiet window.
```

## Final Answers

```text
reconcile_under_quiet classification=CONFIRMED_FALSE_POSITIVE
exact failing checks=missing ip rule lookup table checks in v7-reconcile-check
affected users/tables=10.0.0.2/100, 10.0.0.3/101, 10.0.0.6/104, 10.7.0.2/1000, 10.7.0.3/1001, 10.7.0.4/1002, 10.7.0.5/1003, 10.7.0.6/1004, 10.7.0.8/1006, 10.7.0.9/1007, 10.7.0.10/1008, 10.7.0.11/1009, 10.7.0.12/1010, 10.7.0.13/1011, 10.7.0.14/1012, 10.7.0.15/1013
false-positive candidates=all current missing-ip-rule complaints
real mismatch candidates=none for current missing-ip-rule class
canary_status after classification=CONDITIONAL
execution_allowed_now=false
repair needed before canary=no runtime repair for this failure class; checker fix recommended
bounded waiver acceptable before canary=yes, with strict one-user scope and pre-checks
```

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
