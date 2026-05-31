# P1.D/E Drawer Model

release_drawer_defined=true

## Drawer Purpose

Release Drawer explains the current release, certification, rollback availability and runtime match without requiring operator knowledge of internals.

## Required Sections

### Current Release

Shows:

- release label;
- release id;
- current/previous marker;
- deployment timestamp when known.

### Status

Shows:

- release status;
- certification;
- runtime match;
- rollback availability;
- verification age.

### Certification

Shows:

- certification state;
- required checks;
- passed/failed/missing checks;
- evidence bundle;
- certifying source.

### Rollback Availability

Shows:

- rollback target;
- rollback lineage status;
- backup/restore reference;
- blockers or unknowns.

### Verification History

Shows:

- release checks;
- runtime convergence checks;
- backup/restore checks;
- previous verification events.

### Recommended Action

Shows one safe next action:

- no action needed;
- refresh release verification;
- inspect runtime convergence;
- inspect backup/restore;
- open evidence bundle;
- start containment/recovery.

### Advanced Details

Shows role-gated:

- commit hash references;
- manifest references;
- signature/provenance references;
- lineage internals;
- raw but redacted payload refs.

## Drawer Verdict

Release Drawer makes release trust inspectable and safe without exposing internal provenance complexity by default.
