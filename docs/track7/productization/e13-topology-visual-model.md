# E13 Topology Visual Model

## Purpose

V7 topology must explain governed movement, not display infrastructure trivia.
The visual model should be calm, scalable, and legible to an operator who needs
to answer: what is healthy, what is reserved, who can move, what is approved,
and how rollback is guaranteed.

## Topology Philosophy

Use a structured lane model instead of a graph.

Preferred abstraction:

```text
Users / Cohort -> Policy + Approval -> Target Pool -> Service Outcome
```

This keeps the topology governed. It avoids protocol-centered maps, animated
links, hop graphs, and visually noisy network diagrams.

## Target Display

Targets appear as compact columns or rows grouped by role:

- reserved test targets;
- production targets;
- maintenance targets;
- blocked targets.

Each target shows:

- target id/name;
- protocol family only as metadata;
- reservation badge;
- users count;
- soft/hard limit;
- readiness state;
- service signal summary;
- approval eligibility;
- current blocker if any.

WireGuard example:

```text
WireGuard reserved
0 / 2 users
readiness GO
approval only
```

## User Display

Users are not rendered as hundreds of nodes. They are grouped:

- selected users;
- affected users;
- rollback users;
- blocked candidates;
- all other users.

Only the approved movement set is expanded by default. The rest is count-first
with drill-down.

## Movement Display

Movement is a bounded approval lane:

```text
2 selected users
target 1 -> wireguard-1779454504-c43409
rollback: target 1
budget: 2
fingerprint: matched
```

Movement arrows are shown only for pending/approved operation scope. There is
no background animation for normal routing.

## Reserved Target Display

Reserved targets use a quiet accent badge and a capacity indicator. They must
not look like normal production capacity. A reserved target with users becomes
a warning state, not a decorative change.

## Unhealthy Target Display

Unhealthy or blocked targets show:

- concise blocker;
- affected route class;
- whether autoswitch can use it;
- whether rollback can use it;
- evidence freshness.

Deep diagnose details are hidden behind a drawer.

## Blast Radius Display

Blast radius is a first-class strip in every approval:

- users affected;
- target capacity delta;
- rollback target;
- route class delta;
- timer/barrier state;
- delayed-monitor requirement.

It should appear before any approve button.

## Delayed Movement Display

Delayed movement monitoring is displayed as a sample timeline:

```text
sample A clean -> sample B clean -> sample C clean -> closeout clean
```

Each sample carries:

- registry hash stable yes/no;
- switch-history delta yes/no;
- selected_moves;
- hidden mover scan;
- runtime checks.

## Generation State Display

Generation state appears as a small contract object, not raw JSON:

- planner generation;
- token id;
- selected-move fingerprint;
- budget;
- expiry;
- status: active, consumed, expired, mismatch, fail-closed.

Mismatch states explain the exact failure in operator language.

## Scaling Rules

- Up to 2 users: show exact users by default.
- 3-10 users: show exact users in a compact list with grouped route delta.
- More than 10 users: show summary first, require filter/search to expand.
- Targets: group by eligibility before protocol.
- Warnings: group by lifecycle impact before target.

## Forbidden Topology Patterns

- giant network graphs;
- animated topology;
- interface/hop maps on overview;
- protocol-first dashboard;
- decorative traffic streams;
- metric wall;
- node-link diagrams that imply autonomous movement.

## Visual Tone

The topology should feel like a governed ledger with live operational context:
precise, quiet, and serious. It should not feel like a packet tracer.

