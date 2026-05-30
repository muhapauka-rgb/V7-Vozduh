# E34.D Final Installer Decision

installer_architecture_defined=true

## Decision Summary

E34.D defines Installer & Deployability Architecture.

The future installer is a guided certified deployment process using:

```text
NEXT -> CHECK -> NEXT -> CHECK -> READY
```

## Certified Model Markers

```text
installer_model_defined=true
deployment_profile_model_defined=true
preflight_check_model_defined=true
installation_stages_defined=true
health_check_model_defined=true
installation_failure_model_defined=true
repeatable_deployment_defined=true
operator_experience_defined=true
commercial_compatible=true
installer_architecture_defined=true
```

## Core Rules

- Installer architecture work is read-only.
- Future installer execution is controlled deployment mutation, not user movement.
- READY requires passing checks and certification.
- PRODUCTION requires certified release and backup readiness.
- Preflight failures block installation when severity is BLOCKING.
- Health checks cover runtime, governance, routing intelligence, network, release, and backup.
- Repeatability requires same release, manifest, profile, approved config, and certified outcome.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- installer_packaging_strategy
- supported_os_matrix
- minimum_hardware_profile
- network_port_requirements
- dependency_install_policy
- secrets_input_flow
- installer_ui_surface
- installer_log_storage
- production_certification_authority
```

## Remaining Open Questions

- Which OS versions are commercially supported?
- Does installer ship as CLI, TUI, web UI, or all three?
- Which dependencies may installer install automatically?
- How should secrets be entered and stored?
- Who can certify PRODUCTION_READY?

recommended_next_block=E34.E_OPERATOR_INDEPENDENCE_ARCHITECTURE
