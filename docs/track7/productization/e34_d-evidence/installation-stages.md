# E34.D Installation Stages

installation_stages_defined=true

## Guided Flow

```text
DISCOVERY -> VALIDATION -> INSTALLATION -> CONFIGURATION -> HEALTH_CHECK -> CERTIFICATION -> READY
```

## Stage Model

| Stage | Inputs | Outputs | Failure Modes | Recovery Path |
| --- | --- | --- | --- | --- |
| DISCOVERY | host info, profile request, operator identity | host inventory, profile candidate | missing host facts, unsupported OS | collect facts, change profile, stop. |
| VALIDATION | discovery output, release object, backup plan | preflight_result | disk/memory/network/time/dependency failure | guided remediation then recheck. |
| INSTALLATION | certified release, package/artifact manifest | installed artifacts | package failure, permission failure, missing dependency | rollback partial install or retry. |
| CONFIGURATION | config manifest, secrets references, profile settings | config fingerprint | invalid config, missing secret, schema mismatch | fix config, rerun validation. |
| HEALTH_CHECK | installed runtime, config, release | health_check_result | service failure, network failure, checker failure | diagnose, remediate, rerun check. |
| CERTIFICATION | health checks, fingerprints, lineage, backup readiness | installation certification | provenance mismatch, backup missing, drift | fail closed, repair evidence. |
| READY | certification result | READY report | none; terminal success | monitor. |

## NEXT / CHECK Contract

- NEXT advances to the next stage only after previous stage outputs exist.
- CHECK verifies the current stage.
- READY is impossible without all CHECK gates passing.

installation_stages_defined=true
