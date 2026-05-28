# E13 Operator Screens

## Design Baseline

The operator experience uses the existing V7 admin language: dark-first,
minimal, data-oriented, restrained accents, compact typography, low border
weight, progressive disclosure, and serious bounded actions. It must not look
like a generic VPN dashboard or a network engineer debug screen.

Canonical visual tokens:

- background: near-black application surface;
- panels: quiet elevated surfaces;
- text: high-contrast primary, muted secondary;
- accents: restrained blue for action, green for clean, amber for caution, red
  only for blocked/unsafe;
- borders: subtle separators only where grouping would otherwise be unclear;
- cards: used for repeated objects and approvals, not nested layout frames.

## 1. Runtime Overview

Purpose:

- show the current operational truth and whether any governed action is allowed.

Visible information:

- global status band;
- execution allowed now;
- planner/apply timer states;
- selected moves;
- current movement budget;
- generation token state;
- restore barrier state;
- delayed monitor state;
- runtime checkers;
- target readiness summary;
- newest authoritative block/report.

Progressive disclosure:

- checker detail drawer;
- timer journal drawer;
- evidence freshness drawer.

Primary actions:

- refresh read-only snapshot;
- open Approval Center;
- open Restore Lifecycle;
- open Evidence Viewer.

Dangerous actions:

- none directly on the overview.

Approval requirements:

- overview can route to approvals but cannot execute movement or timer changes.

Mobile behavior:

- status band, blockers, and next safe action appear first;
- target summary collapses into horizontal status rows;
- deep evidence opens full-screen.

Empty state:

- "No active governed operation" with planner/apply state and last verified
  clean snapshot.

Warning state:

- stale evidence, hidden mover detected, selected moves nonzero, generation
  mismatch, or apply active without approved lifecycle.

## 2. Target Pool

Purpose:

- show target readiness, reservation, capacity, and eligibility without exposing
  protocol internals by default.

Visible information:

- target grouped by `reserved`, `production`, `maintenance`, `blocked`;
- users count;
- soft/hard limit;
- readiness;
- reservation metadata;
- route class eligibility;
- quality summary;
- rollback suitability.

Progressive disclosure:

- service-signal details;
- diagnose evidence;
- per-target users;
- route-class support;
- raw egress registry row.

Primary actions:

- open target details;
- open readiness evidence;
- open reservation policy.

Dangerous actions:

- reservation mutation, target enable/disable, and drain are not one-click.

Approval requirements:

- target mutation requires separate governance packet, rollback material, and
  second confirmation.

Mobile behavior:

- targets become compact rows with health, users, cap, reservation, and blocker.

Empty state:

- no eligible test target, with exact blocker list.

Warning state:

- target over soft limit, near hard limit, stale readiness, reserved target
  occupied, or production target accidentally selected.

## 3. Pending Movement Preview

Purpose:

- show exactly what a bounded movement would do before approval.

Visible information:

- operation id;
- generated-at and expires-at;
- source registry hash;
- selected-move fingerprint;
- selected users;
- from/to targets;
- route delta;
- target capacity delta;
- rollback target per user;
- movement budget;
- blocked candidates;
- required gates.

Progressive disclosure:

- per-user route diff;
- candidate scoring;
- raw selected_moves payload;
- planner reason trace;
- copied-state vs live-state label.

Primary actions:

- regenerate preview;
- compare with previous preview;
- create approval contract.

Dangerous actions:

- approve movement;
- clear generation barrier;
- restore apply timer.

Approval requirements:

- approval requires fresh evidence, matching registry hash, generation token,
  selected-move fingerprint, rollback contract, and explicit blast-radius
  acknowledgement.

Mobile behavior:

- first screen shows affected users, target delta, rollback status, and expiry;
- per-user details are accordions.

Empty state:

- selected moves zero and no approval needed.

Warning state:

- preview stale, candidate count exceeds budget, target cap would be exceeded,
  generation mismatch, or rollback target unhealthy.

## 4. Approval Center

Purpose:

- concentrate serious operator decisions into one controlled workflow.

Visible information:

- pending approvals;
- approval type;
- blast radius;
- token/fingerprint status;
- required confirmations;
- expiry;
- rollback status;
- evidence completeness.

Progressive disclosure:

- contract JSON;
- evidence bundle;
- exact commands that would be run by automation;
- rejection reason trace.

Primary actions:

- approve read-only evidence archive;
- approve bounded movement;
- approve apply timer restore;
- approve barrier clearance;
- reject approval;
- expire approval.

Dangerous actions:

- any nonzero movement budget;
- apply timer restore;
- generation clearance;
- target mutation.

Approval requirements:

- dual-confirmation for nonzero movement budget, apply timer restore, barrier
  clearance, and any rollback-impacting action.

Mobile behavior:

- one approval per screen;
- no multi-select dangerous approvals;
- confirmation text is short and specific.

Empty state:

- no pending approvals, with latest governance state.

Warning state:

- stale approval, replay attempt, mismatched fingerprint, expired token, or
  missing rollback evidence.

## 5. Restore Lifecycle

Purpose:

- make planner restore, restore-settle, apply restore, barrier, clearance, and
  delayed monitoring visible as one lifecycle.

Visible information:

- phase rail: hold, forward movement, observation, rollback/keep, planner
  restore, restore-settle, apply restore, delayed monitor, closeout;
- current phase;
- required evidence per phase;
- timer states;
- barrier state;
- generation clearance state;
- delayed monitor samples.

Progressive disclosure:

- phase evidence;
- journals;
- switch-history deltas;
- registry hash sequence.

Primary actions:

- open phase evidence;
- generate restore status;
- create apply-restore approval.

Dangerous actions:

- apply timer restore;
- barrier clearance;
- manual repair.

Approval requirements:

- apply restore requires restore-settle GO, generation contract, selected-move
  budget, rollback state, and delayed monitoring plan.

Mobile behavior:

- phase rail becomes a vertical checklist with current blocker pinned.

Empty state:

- no active restore lifecycle.

Warning state:

- restore-settle stale, timer overlap, delayed monitor incomplete, or barrier
  expired without clearance.

## 6. Generation Governance

Purpose:

- show generation-token ownership and replay resistance in operator language.

Visible information:

- current planner generation;
- apply generation;
- restore generation;
- token id;
- token scope;
- selected-move hash;
- maximum selected moves;
- expiry;
- clearance state;
- mismatch reason if blocked.

Progressive disclosure:

- token contract JSON;
- generation lineage;
- replay rejection evidence;
- selected-move canonicalization.

Primary actions:

- inspect token;
- invalidate approval;
- create clearance approval from an active preview.

Dangerous actions:

- issue nonzero clearance token;
- clear expired barrier.

Approval requirements:

- token issuance requires matching preview hash, current registry hash, max move
  budget, rollback contract, and explicit expiry.

Mobile behavior:

- one compact token status panel and mismatch reasons first.

Empty state:

- no active token; fail-closed state visible.

Warning state:

- stale token, mismatch, expired token, budget exceeded, or replay attempt.

## 7. Operations History

Purpose:

- give a readable timeline of governed operations, not a raw log stream.

Visible information:

- operation id;
- type;
- status;
- actor;
- started/closed time;
- affected users;
- target;
- movement count;
- rollback result;
- report link.

Progressive disclosure:

- phase timeline;
- evidence bundle;
- switch-history slice;
- mutation statement.

Primary actions:

- open operation;
- compare operations;
- export evidence bundle.

Dangerous actions:

- none.

Approval requirements:

- history is read-only.

Mobile behavior:

- timeline rows stack with status, affected users, and verdict.

Empty state:

- no operations in selected filter.

Warning state:

- operation closed with unresolved delayed monitor or missing evidence.

## 8. Evidence Viewer

Purpose:

- make reports and raw evidence searchable while preserving current/historical
  distinction.

Visible information:

- report title;
- block id;
- verdict;
- supersedes/superseded-by;
- evidence freshness;
- mutation statement;
- key hashes;
- linked files.

Progressive disclosure:

- raw text;
- JSON;
- command output;
- diff against previous report.

Primary actions:

- search evidence;
- copy evidence reference;
- open raw file;
- compare historical/current state.

Dangerous actions:

- none.

Approval requirements:

- evidence viewer is read-only.

Mobile behavior:

- summary first; raw evidence opens in a dedicated view.

Empty state:

- no evidence for filter.

Warning state:

- evidence is historical, copied-state only, stale, or not authoritative.

## 9. Runtime Warnings

Purpose:

- concentrate actionable warnings without creating a warning wall.

Visible information:

- severity;
- impacted lifecycle;
- exact blocker;
- safe next action;
- evidence source;
- staleness.

Progressive disclosure:

- impacted objects;
- raw checker output;
- related operation.

Primary actions:

- inspect;
- refresh safe diagnostics;
- open relevant workflow.

Dangerous actions:

- none directly.

Approval requirements:

- warning cannot execute a mutation directly.

Mobile behavior:

- most severe warning pinned; lower-priority warnings grouped.

Empty state:

- no active warnings.

Warning state:

- blocked, stale, hidden movement, selected moves nonzero, generation mismatch.

## 10. Cohort Governance

Purpose:

- manage cohort readiness and approval shape without executing a cohort by
  default.

Visible information:

- allowed cohort size;
- selected candidates;
- target;
- rollback targets;
- hard capacity;
- current approval status;
- blockers;
- required evidence.

Progressive disclosure:

- candidate selection reasoning;
- rejected candidates;
- route diffs;
- capacity analysis;
- lifecycle plan.

Primary actions:

- generate approval packet;
- compare candidate sets;
- open movement preview.

Dangerous actions:

- cohort execution and rollback.

Approval requirements:

- execution requires separate approved movement contract and should not be
  launched from the read-only approval packet view.

Mobile behavior:

- candidate list summarizes into count, target, cap, and blockers.

Empty state:

- no approved cohort; show current maximum safe shape.

Warning state:

- cohort exceeds hard limit, target not clean, rollback not feasible, or larger
  cohort remains NO-GO.

## 11. Reservation Management

Purpose:

- show target reservation policy and protect reserved targets from accidental
  production assignment.

Visible information:

- reserved targets;
- reservation reason;
- allowed use;
- enforcement status;
- current users;
- recent blocked assignments;
- policy source.

Progressive disclosure:

- enforcement matrix;
- planner/apply/rebalance/fallback coverage;
- raw egress metadata.

Primary actions:

- inspect reservation;
- open reservation policy;
- generate mutation packet.

Dangerous actions:

- reserve/unreserve target;
- assign production user to reserved target.

Approval requirements:

- reservation mutation requires separate governance report and rollback plan.

Mobile behavior:

- reserved status and current users remain visible in every target row.

Empty state:

- no reserved test target, with blocker.

Warning state:

- reserved target occupied, enforcement incomplete, or policy stale.

## 12. Delayed Movement Monitor

Purpose:

- prove that nothing moved after restore/apply/clearance beyond the approved
  lifecycle.

Visible information:

- monitored operation;
- timer intervals observed;
- registry hash sequence;
- switch-history count sequence;
- selected_moves sequence;
- hidden mover scan;
- runtime checker sequence;
- verdict.

Progressive disclosure:

- sample evidence;
- journal snippets;
- switch-history diff;
- target readiness samples.

Primary actions:

- refresh sample;
- close monitor when required samples are clean;
- open evidence bundle.

Dangerous actions:

- emergency containment if unexpected movement appears.

Approval requirements:

- containment requires an explicit safety path, but it is available only for
  preventing additional movement, not repairing state silently.

Mobile behavior:

- sample timeline with clean/blocked states; raw hashes hidden.

Empty state:

- no active delayed monitoring.

Warning state:

- registry drift, switch-history delta, selected_moves nonzero, hidden mover,
  checker fail, or missing sample.

