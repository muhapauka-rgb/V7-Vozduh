# Block E8.7 - v7-reconcile-check Pipefail False-Positive Fix Report

Date: 2026-05-25.

Mode: bounded checker fix.

Runtime mutation scope: `/usr/local/bin/v7-reconcile-check` only.

## Executive Verdict

```text
checker_patched_repo_side=true
checker_deployed_runtime=true
runtime_files_changed=/usr/local/bin/v7-reconcile-check
backup_path=/root/v7-reconcile-check.backup.E87.20260525T134737Z
v7-reconcile-check_result_after_fix=OK
remaining_reconcile_errors=0
user_route_check_OK=true
kill_switch_OK=true
provisioning_reconcile_OK=true
users.registry_changed=false during deploy and post-check packet
egress.registry_changed=false during deploy and post-check packet
user_movement_observed=false during deploy and post-check packet
routing_drift_observed=false during post-check packet
canary_status=CONDITIONAL
execution_allowed_now=false
```

E8.7 fixed the confirmed E8.6 false-positive class in `v7-reconcile-check`.

This was not a routing repair. It did not change routes, ip rules, nftables,
registries, autoswitch services, policy, Direct/RU, Trusted RU, proxy runtime,
or kill switch state.

## Ownership

Repo path:

```text
tools/runtime-support/v7-reconcile-check
```

Runtime path:

```text
/usr/local/bin/v7-reconcile-check
```

Lineage:

```text
docs/track7/lineage/provisioning-support-tools.json
lineage_status=lineage_resolved_in_repo
```

Ownership evidence:

```text
docs/track7/control-plane/e8_7-evidence/checker-ownership.txt
```

## Patch

Previous false-positive-prone checks:

```bash
ip -4 rule show 2>/dev/null | grep -q "from $ip lookup $table"
wg show "$WG_IF" allowed-ips 2>/dev/null | awk '{print $2}' | grep -qx "$ip/32"
printf '%s\n' "$route" | grep -q " dev $dev "
```

Patched semantics:

```bash
ip_rules="$(ip -4 rule show 2>/dev/null || true)"
wg_allowed_ips="$(wg show "$WG_IF" allowed-ips 2>/dev/null | awk '{print $2}' || true)"

grep -Fq "from $ip lookup $table" <<< "$ip_rules"
grep -Fxq "$ip/32" <<< "$wg_allowed_ips"
grep -Fq " dev $dev " <<< "$route"
```

This preserves missing-rule detection while removing the `pipefail` plus
`grep -q` SIGPIPE false-positive.

## Tests

Added:

```text
tests/unit/test_v7_reconcile_check.py
```

Test coverage:

```text
existing rule is detected as present even if fake ip rule show exits 141
missing rule is still detected as missing
disabled users remain skipped
```

Local test result before deploy:

```text
python3 -m unittest tests.unit.test_v7_reconcile_check -v: OK
tools/v7-run-tests: OK
bash -n tools/runtime-support/v7-reconcile-check: OK
```

## Runtime Deploy

Backup:

```text
/root/v7-reconcile-check.backup.E87.20260525T134737Z
```

Before:

```text
sha256_before=a60b47ea064aa0113015bdaa401b324ba8182f3a75c92bbbab601382058f4c87
mode_before=755
owner_before=root:root
size_before=2940
```

After:

```text
sha256_after=f8218d42abb8b71d878790a59919d880e3da510ddc615d9f8b6a78da130c0e7b
mode_after=755
owner_after=root:root
size_after=3015
bash_n_rc=0
```

Deploy evidence:

```text
docs/track7/control-plane/e8_7-evidence/deploy-output.txt
```

## Post-Fix Runtime Verification

Post-fix read-only checks:

```text
V7_RECONCILE_RESULT=OK
reconcile_rc=0
V7_USER_ROUTE_CHECK=OK
user_route_rc=0
V7_KILLSWITCH_CHECK=OK
killswitch_rc=0
V7_PROVISIONING_RECONCILE_CHECK=OK
provisioning_rc=0
```

Registry hashes remained stable during deploy and post-check packet:

```text
users.registry=4b8ac23f01f8a6f5857500115bac6b401b824502648272ccaae234f76bd37908
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

Post-fix verification evidence:

```text
docs/track7/control-plane/e8_7-evidence/post-fix-verification.txt
```

## Canary Implication

The reconcile false-positive blocker is fixed.

Canary still does not become GO automatically because:

- autoswitch planner/apply timers are active outside a bounded hold window;
- one-user canary approval has not been granted;
- candidate user and target egress readiness must be refreshed;
- rollback command must be confirmed immediately before canary;
- Trusted RU relevance must be checked for the candidate path;
- the canary must be run only inside a verified post-split quiet window.

Updated status:

```text
canary_status=CONDITIONAL
execution_allowed_now=false
```

## Exact Next Recommended Step

Prepare a separate E8.8 one-user canary approval packet, not execution, using:

```text
1. verified post-split quiet-window hold model;
2. fixed v7-reconcile-check as a hard pre-check;
3. fresh candidate/target egress readiness;
4. explicit rollback command;
5. no autoswitch planner/apply authority during the proposed canary window.
```

## Final Answers

```text
checker patched repo-side=true
checker deployed runtime=true
runtime files changed=/usr/local/bin/v7-reconcile-check
backup path=/root/v7-reconcile-check.backup.E87.20260525T134737Z
v7-reconcile-check result after fix=OK
any remaining reconcile errors=none observed
user route check OK=true
kill switch OK=true
provisioning reconcile OK=true
users.registry changed=false during deploy/check packet
egress.registry changed=false during deploy/check packet
user movement observed=false during deploy/check packet
routing drift observed=false during post-check packet
canary_status after fix=CONDITIONAL
execution_allowed_now=false
```

## Mutation Statement

```text
Runtime mutation performed: YES - limited to checker file only: /usr/local/bin/v7-reconcile-check
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
