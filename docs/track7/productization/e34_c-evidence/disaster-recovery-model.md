# E34.C Disaster Recovery Model

disaster_recovery_defined=true

## Disaster Classes

| Disaster | Recovery Path | Recovery Priority | Recovery Authority |
| --- | --- | --- | --- |
| server_loss | Provision new host, restore release/config/audit from verified backup, verify convergence. | High | Operator plus release/backup evidence. |
| disk_loss | Restore from latest verified backup to replacement disk/host. | High | Operator plus backup verification. |
| configuration_loss | Restore config artifacts, verify config fingerprint, reload only through future deploy procedure. | Medium/High | Operator review required. |
| partial_corruption | Identify corrupt artifact, restore only affected scope if lineage remains valid. | Medium | Operator review, fail closed. |
| lineage_corruption | Reconstruct from backup/audit/release records; production denied until verified. | Critical | Human review and certification authority. |

## Recovery Priorities

1. Preserve audit and provenance evidence.
2. Restore release objects and rollback targets.
3. Restore governance and routing configuration.
4. Restore operator visibility.
5. Restore runtime services through release-aware deployment.
6. Verify convergence before production use.

## Fail-Closed Rules

- Disaster recovery starts in read-only/containment posture.
- No user movement is authorized by recovery itself.
- If lineage cannot be reconstructed, production status remains UNKNOWN/BLOCKING.
- Emergency rollback can be allowed for containment but must be marked degraded until provenance is restored.

disaster_recovery_defined=true
