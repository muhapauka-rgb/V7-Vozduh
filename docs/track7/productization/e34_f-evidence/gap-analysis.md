# E34.F Gap Analysis

## Remaining Gaps

The commercial hardening architecture is certified, but implementation still requires product and engineering decisions.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- fingerprint_hash_algorithm
- release_object_storage_backend
- deployment_lineage_backend
- runtime_inventory_collector
- release_signing_policy
- backup_storage_backend
- backup_encryption_policy
- backup_retention_policy
- restore_rehearsal_cadence
- installer_packaging_strategy
- supported_os_matrix
- dependency_install_policy
- secrets_input_flow
- installer_ui_surface
- operator_ui_surface
- runbook_storage_format
- evidence_bundle_storage_backend
- evidence_redaction_policy
- emergency_operator_authority
- closure_record_backend
```

## Remaining Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Storage backend not chosen | MEDIUM | Decide release, backup, lineage, evidence, and closure storage. |
| Signing policy undefined | MEDIUM | Choose release signing and verification mechanism. |
| Operator UI not implemented | MEDIUM | Design CLI/TUI/web operator surface. |
| Secrets flow undefined | HIGH | Define secret input, storage, redaction, and backup strategy before commercial release. |
| Restore rehearsal cadence undefined | MEDIUM | Define recurring restore test policy. |
| Emergency authority undefined | MEDIUM | Define emergency roles and dual confirmation requirements. |

## Certification Impact

None of these gaps invalidate architecture certification. They are implementation and product decisions required before commercial launch.
