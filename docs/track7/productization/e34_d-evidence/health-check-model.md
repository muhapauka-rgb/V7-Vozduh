# E34.D Health Check Model

health_check_model_defined=true

## Post-Install Validation

| Check Family | Required Checks |
| --- | --- |
| runtime checks | service process state, version endpoint, runtime fingerprint, runtime checkers. |
| governance checks | capacity/batch/policy/concurrency/scheduling schemas and read-only checker health. |
| routing intelligence checks | required_services catalog, service health probe availability, proposal engine read-only sanity. |
| network checks | public/private connectivity, DNS, TUN, WG/AWG/Reality dependency checks. |
| release checks | release fingerprint, manifest match, deployment lineage, config fingerprint. |
| backup checks | backup readiness, rollback target, backup verification status. |

## Health Result

```text
health_check_id
profile
release_id
runtime_status
governance_status
routing_intelligence_status
network_status
release_status
backup_status
overall_status=PASS|WARN|FAIL
blocked_reasons
```

## READY Rule

READY requires overall_status=PASS for PRODUCTION. TEST may allow WARN with explicit certification note. LAB may allow WARN if no production capability is claimed.

health_check_model_defined=true
