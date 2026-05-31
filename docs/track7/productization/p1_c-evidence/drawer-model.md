# P1.C Drawer Model

runtime_convergence_drawer_defined=true

## Drawer Purpose

Runtime Convergence Drawer explains whether the running system matches release expectations and what to do if it does not.

## Required Sections

### Status

Shows:

- runtime status;
- release match;
- blocking flag;
- verification freshness;
- evidence bundle link.

### Summary

Shows operator-safe language:

- "System matches release";
- "System drift detected";
- "Runtime trust unknown";
- "Runtime blocked".

### Drift

Shows:

- drift type;
- severity;
- affected area;
- detected time;
- impact;
- whether forward governance is blocked.

### Verification History

Shows:

- latest convergence check;
- previous checks;
- check source;
- release reference;
- evidence bundle;
- result.

### Recommended Action

Shows one safe next action:

- refresh verification;
- inspect release provenance;
- inspect backup/restore;
- open evidence bundle;
- start containment/recovery;
- no action needed.

### Advanced Details

Shows role-gated:

- fingerprint summary;
- hash refs;
- lineage refs;
- raw but redacted diff references;
- source checker output summary.

## Drawer Verdict

Runtime Convergence Drawer makes runtime trust understandable without requiring operators to read fingerprint internals.
