# Reconcile False-Positive Analysis

## Current Finding

`v7-reconcile-check` can report missing ip rules even when stable `ip -4 rule show` snapshots contain the expected rules. A targeted grep for a reported missing rule also succeeded.

This makes the current FAIL partially false-positive or race-sensitive.

## E8.5 Quiet-Window Finding

Block E8.5 created a verified post-split quiet window:

```text
autoswitch_planner_held=true
autoswitch_apply_held=true
v7-health_stayed_active=true
users.registry stable=true
egress.registry stable=true
switch-history stable=true
ip rules stable=true
route tables stable=true
user-route-check=OK
killswitch-check=OK
provisioning-reconcile-check=OK
```

During that quiet window:

```text
sample_A V7_RECONCILE_RESULT=FAIL rc=1
sample_B V7_RECONCILE_RESULT=FAIL rc=1
sample_C V7_RECONCILE_RESULT=FAIL rc=1
```

Updated classification:

```text
reconcile_under_quiet=STABLE_FAIL
```

This rules out "active autoswitch race" as the only explanation. The remaining likely explanations are:

- stable checker semantic mismatch;
- parser/output mismatch;
- expected rule model differs from the actual but operationally working datapath;
- stable real mismatch that does not currently trip `v7-user-route-check`, `v7-killswitch-check`, or provisioning reconcile.

It is not clean enough for automatic canary GO.

## E8.6 Classification

Block E8.6 confirmed the cause of the stable reconcile failure:

```text
classification=CONFIRMED_FALSE_POSITIVE
false_positive_class=pipefail_grep_q_sigpipe
affected_check=missing ip rule lookup table
real_runtime_mismatch_candidates=none for this failure class
```

The source has global `set -euo pipefail` and checks rules with:

```bash
ip -4 rule show 2>/dev/null | grep -q "from $ip lookup $table"
```

Read-only probe showed:

```text
pipefail_rc=141
no_pipefail_rc=0
```

for existing rules. This means `grep -q` can find a rule, exit early, cause the
upstream `ip` process to receive SIGPIPE, and make the pipeline fail under
`pipefail`.

## Conditions Where FAIL May Be Operationally Safe

FAIL may be safe enough for one-user canary consideration only when all are true:

- stable pre/post `ip -4 rule show` contains the candidate rule;
- candidate route table default points to expected egress;
- `ip route get` from candidate IP uses expected egress;
- `v7-user-route-check` is OK;
- `v7-killswitch-check` is OK;
- `v7-provisioning-reconcile-check` is OK;
- autoswitch authority is held so the state is not moving during audit;
- failure is limited to checker semantics and not actual missing runtime state.

## Conditions Where FAIL Is Definitely Dangerous

FAIL is dangerous when:

- stable `ip -4 rule show` lacks the candidate source rule;
- candidate table lacks default route;
- route-get uses public interface or wrong egress;
- kill switch check fails;
- provisioning reconcile fails;
- registry and assignment files disagree;
- autoswitch/routing-sync is concurrently mutating users;
- the candidate is not isolated to one table/user.

## Checker Semantics

Current checker behavior is conservative but can overstate operational risk. It has only OK/FAIL, so it cannot distinguish:

- rule absent in stable runtime;
- transient rule rewrite/race;
- parser/color/output mismatch;
- route reality OK but strict rule text check failed.

Recommended future semantics:

```text
OK: stable rules/tables/routes all match
WARN/DEGRADED: rule text check failed but route reality and pre/post stable snapshots pass
FAIL: stable runtime state missing required rule/table/route or leak risk detected
```

## Current Verdict

The current reconcile FAIL is not proven dangerous, and E8.5 shows it is stable under a verified quiet window while datapath checks remain OK.

Canary status may move from `NO-GO` to `CONDITIONAL`, but execution remains blocked until one of these happens:

```text
1. reconcile checker semantics are fixed or upgraded to OK/WARN/FAIL;
2. the stable mismatch is proven real and repair-planned outside canary;
3. an explicit one-user, time-bounded false-positive waiver is approved.
```

After E8.6, option 2 is not supported for the current missing-rule failure class.
The remaining paths are checker fix or explicit bounded waiver.

## E8.7 Checker Fix

Block E8.7 patched and deployed `v7-reconcile-check` for the confirmed
`pipefail_grep_q_sigpipe` false-positive class.

Patched pattern:

```text
capture `ip -4 rule show` once into `ip_rules`
check with `grep -Fq ... <<< "$ip_rules"`
```

The same snapshot approach is used for WireGuard allowed IP checks, and route
device matching now uses a here-string instead of a pipeline.

Post-fix runtime result:

```text
V7_RECONCILE_RESULT=OK
reconcile_rc=0
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Updated verdict:

```text
false-positive class fixed=true
runtime repair needed=false
checker hard-gate usable again=true, subject to fresh pre-canary checks
```
