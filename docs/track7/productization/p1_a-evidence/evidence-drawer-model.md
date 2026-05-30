# P1.A Evidence Drawer Model

evidence_drawer_defined=true

## Drawer Purpose

Evidence Drawer is the shared admin component for inspecting proof without leaving the current workflow.

## Drawer Sections

### Summary

Shows:

- title;
- status pill;
- severity;
- primary object;
- operator meaning;
- current diagnosis.

### Timeline

Shows ordered evidence events:

- detected;
- checked;
- diagnosed;
- action recommended;
- action executed if applicable;
- verified;
- closed.

### Evidence Items

Shows proof cards or compact rows:

- item source;
- captured time;
- status;
- summary;
- redaction state;
- link to advanced details.

### Recommended Action

Shows:

- next safe action;
- action type: view, preview, guarded apply, rollback, containment;
- blockers;
- blast radius if relevant;
- required confirmation if relevant.

### Verification

Shows:

- required checks;
- completed checks;
- failed checks;
- missing evidence;
- final verification state.

### Closure

Shows:

- closure status;
- closure reason;
- actor/source;
- timestamp;
- residual risk.

### Advanced Details

Shows role-gated raw or semi-raw details:

- command output summaries;
- JSON payload previews;
- hashes;
- source paths;
- audit refs.

Secrets must remain redacted.

## Drawer Verdict

Evidence Drawer is the UI component that makes architecture evidence operational in the current V7 Admin without adding navigation.

