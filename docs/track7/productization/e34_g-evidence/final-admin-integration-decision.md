# E34.G Final Admin Integration Decision

admin_integration_architecture_defined=true

## Decision

E32-E34 architecture integrates into the existing V7 Admin without a new dashboard product and without new top-level sections.

The current admin navigation remains sufficient.

## Certified Integration Markers

```text
current_admin_loaded=true
architecture_surface_map_defined=true
operator_surface_levels_defined=true
proposal_ux_defined=true
recovery_surface_defined=true
installer_surface_defined=true
navigation_integration_defined=true
progressive_disclosure_defined=true
complexity_hidden_by_default=true
```

## Operator Experience Rule

The operator sees tasks and decisions:

- what happened;
- who is affected;
- what should I do;
- what is safe;
- what evidence supports it.

The operator does not navigate backend architecture nouns.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- exact proposal card component shape
- expert diagnostics access role
- installer first-run entrypoint
- release/provenance drawer placement
- evidence bundle visual component
```

recommended_next_program=E34.H_ARCHITECTURE_TO_IMPLEMENTATION_MAPPING
