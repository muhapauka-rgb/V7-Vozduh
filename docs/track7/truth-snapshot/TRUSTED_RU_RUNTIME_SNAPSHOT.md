# Direct/RU / Trusted RU Snapshot

Evidence source:

```text
docs/track7/truth-snapshot/evidence/section-trusted-ru-direct-policy.txt
docs/track7/truth-snapshot/evidence/section-trusted-ru-direct-policy-details.txt
```

## State Files

```text
/opt/v7/egress/state/trusted-ru-diagnostic.state mtime=2026-05-22T23:36:30+03:00 approx
/opt/v7/egress/state/trusted-ru-decision.state mtime=2026-05-07T20:18:38+03:00 approx
/opt/v7/egress/state/route-classes.state mtime=2026-05-07T15:12:17+03:00 approx
/opt/v7/egress/state/direct-ru-autosync.state updated=2026-05-25T14:06:04+03:00
```

## Trusted RU

Decision state reports:

```text
route_class=TRUSTED_RU_SENSITIVE
route_class_status=NEEDS_TRUSTED_PATH
current_candidate=vless
candidate_result=VLESS_PARTIAL
blocked=2
missing=0
candidate_vless_failed=2
```

This remains Gosuslugi-sensitive. It is stale enough that canary cannot rely on it without separate governance.

## Direct/RU

Direct/RU autosync state reports:

```text
status=OK
changed=0
checked_count=8
ok_count=8
stale_count=0
failed_count=0
render=SKIPPED
dnsmasq=active
```

## Verdict

Direct/RU status looks currently OK. Trusted RU/Gosuslugi decision state is sensitive and not safe to treat as solved. Do not run refresh, policy apply, route-class mutation, or Direct/RU mutation without separate approval.
