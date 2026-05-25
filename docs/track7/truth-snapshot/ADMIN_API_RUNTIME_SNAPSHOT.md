# Admin / API Runtime Snapshot

Evidence source:

```text
docs/track7/truth-snapshot/evidence/section-proxy-telemetry-admin.txt
docs/track7/truth-snapshot/evidence/admin-endpoint-inventory.json
```

## Runtime Status

```text
v7-admin-api.service active/running
process=python3 /usr/local/bin/v7-admin-api
listener=127.0.0.1:7080
```

Admin API is local-bound. Public gateway is separately active on `0.0.0.0:80` and forwards selected public delivery paths.

## Static Endpoint Inventory

Static inventory summary:

```text
endpoint_count=192
GET=47
HEAD=8
POST=137
public=19
auth_required=173
critical_risk=13
high_risk=95
medium_risk=37
low_risk=47
csrf_required_count=132
safe_mode_blocked_count=86
```

## Dangerous Bindings

The admin surface contains many POST/action endpoints and high-risk bindings. This snapshot did not call any admin action and did not validate auth correctness live.

## Verdict

Admin API is operational and locally bound, but the endpoint inventory confirms high mutation potential. Admin action execution remains forbidden without explicit approval.
