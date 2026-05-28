# E13 Governance Information Hierarchy

## Purpose

The V7 operator UI must show governance truth before technical evidence. It
should feel like a calm control plane, not a routing console.

## Layer 1 - Global Operational Truth

This is always visible on the Runtime Overview and compactly visible on every
governance workflow.

Content:

- operational maturity state;
- execution allowed now: yes/no and why;
- planner timer state;
- apply timer state;
- active operation or idle state;
- selected moves count;
- movement budget;
- generation token state;
- restore barrier state;
- delayed monitor state;
- runtime checker summary;
- target readiness summary;
- evidence freshness.

Primary question answered:

```text
Is the system safe, what is blocked, and what is the next governed action?
```

What does not belong:

- raw journals;
- full route tables;
- raw registry rows;
- every egress metric;
- every historical report.

## Layer 2 - Movement And Governance State

This layer appears on movement previews, approvals, restore lifecycle, cohort
governance, and delayed monitoring.

Content:

- proposed movement set;
- selected-move fingerprint;
- affected users;
- source and destination targets;
- rollback targets;
- blast radius;
- capacity delta;
- generation token scope;
- approval expiry;
- barrier and clearance status;
- planner/apply generation match;
- required checks;
- abort conditions.

Primary question answered:

```text
What exactly is being approved, what can move, and how is it rolled back?
```

What is expandable:

- per-user route diff;
- candidate scoring;
- blocked candidates;
- raw selected_moves JSON;
- journal excerpts.

## Layer 3 - Target And Runtime Details

This layer supports target readiness, reservation, capacity, route quality, and
runtime state inspection.

Content:

- target rows grouped by eligibility;
- reserved targets;
- current user count;
- soft and hard limits;
- quality and service signals;
- route class support;
- rollback suitability;
- diagnose summary;
- production occupancy;
- target-specific blockers.

Primary question answered:

```text
Can this target safely participate in the approved bounded lifecycle?
```

What is hidden until detail:

- raw `wg show` / `awg show` output;
- probe details;
- full checker logs;
- Linux route internals.

## Layer 4 - Deep Evidence And Debug

This layer is explicitly opened from an evidence link, timeline event, or
diagnostic drawer.

Content:

- registry hashes;
- switch-history rows;
- journal slices;
- raw JSON evidence;
- report links;
- runtime/repo diff;
- release lineage;
- command output;
- copied-state vs live-state labels.

Primary question answered:

```text
What exact evidence supports the visible decision?
```

## Always Visible

- Current action eligibility.
- Active blockers.
- Timer states.
- Selected moves.
- Movement budget.
- Generation-token status.
- Barrier status.
- Evidence freshness.
- Rollback availability for any pending movement.

## Expandable Only

- Candidate lists beyond the approved movement set.
- Raw registry rows.
- Raw JSON contracts.
- Per-service diagnose internals.
- Long switch-history and journal sections.
- Historical superseded reports.

## Never On Homepage

- Full registry tables.
- Full Linux route tables.
- Raw nftables or interface internals.
- Animated topology.
- Metric walls.
- Unscoped warnings without safe next action.

## Visual Hierarchy

The UI should use full-width bands and compact grouped surfaces, not nested
cards. One status band leads, one active operation area follows, and target or
evidence details stay below the fold or behind drawers.

