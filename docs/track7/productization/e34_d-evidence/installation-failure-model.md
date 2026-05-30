# E34.D Installation Failure Model

installation_failure_model_defined=true

## Failures

| Failure | Diagnosis | Operator Message | Recovery Path |
| --- | --- | --- | --- |
| DISK_INSUFFICIENT | disk preflight below profile floor. | Disk space is insufficient for selected profile. | Free disk, attach volume, or select lower profile. |
| NETWORK_FAILURE | required connectivity check fails. | Network checks failed; deployment cannot continue. | Fix routing/firewall/DNS and rerun CHECK. |
| TUN_UNAVAILABLE | TUN/TAP device or kernel support missing. | VPN tunnel support is unavailable. | Enable kernel/module/container permission and rerun CHECK. |
| SERVICE_FAILURE | installed service does not start or health fails. | Service did not reach healthy state. | Inspect logs, fix dependency/config, rerun HEALTH_CHECK. |
| CONFIG_INVALID | config schema/fingerprint invalid. | Configuration is invalid or does not match release profile. | Correct config from manifest and rerun CONFIGURATION. |
| RELEASE_MISSING | release object/artifacts unavailable. | Certified release cannot be found or verified. | Provide release object or stop. |
| BACKUP_MISSING | backup/rollback readiness absent. | Backup readiness is missing for selected profile. | Create/verify backup plan before production. |
| CERTIFICATION_FAILED | final checks or provenance fail. | Installation cannot be certified. | Review failed checks and remediate; READY denied. |

## Failure Output

```text
failure_id
stage
severity
diagnosis
operator_message
recovery_path
can_retry
requires_human_review
```

installation_failure_model_defined=true
