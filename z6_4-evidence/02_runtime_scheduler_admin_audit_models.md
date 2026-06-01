# Runtime, Scheduler, Admin, and Audit Models

## Runtime Owner Model

Primary runtime owner:

`tools/v7-users-autoswitch`

Responsibilities that belong to autoswitch and only autoswitch:

- live eligibility evaluation for movement;
- planner execution;
- canonical live selected-move generation;
- selected-move hash/generation validation;
- restore-barrier consumption and runtime validation;
- runtime recheck for movement execution;
- apply admission for selected moves;
- execution through the movement primitive;
- verification of movement result;
- movement rollback decision for the operation it executed;
- runtime outcome emission;
- runtime state writes already owned by autoswitch, including safety/reconnect/load state.

In scope:

- movement lifecycle runtime truth;
- selected-move truth;
- runtime barrier enforcement;
- per-run verification and movement rollback;
- final runtime outcome for Admin closure/audit surfaces.

Out of scope:

- systemd scheduling truth;
- policy authorship;
- signal production;
- operator approval UX;
- closure record authorship;
- audit sink ownership;
- broad file/config rollback ownership;
- historical report ownership.

## Scheduler Model

Scheduler owner:

`systemd/v7-users-autoswitch.timer/service`

Scheduler should own:

- timer cadence;
- process launch;
- environment/actor identity for scheduled autoswitch;
- service-level success/failure from the OS perspective.

Scheduler should never own:

- selected moves;
- planner authority;
- restore-barrier truth;
- execution outcome truth;
- rollback decisions;
- audit completion;
- closure state;
- policy/trust/capacity decisions.

Runtime truths that must remain outside scheduler ownership:

- all planner outputs;
- all movement decisions;
- all rollback decisions;
- all runtime final verdicts;
- all closure records.

## Admin Model

Admin components:

- `admin/v7-admin-api`
- `admin_core/operator_observability.py`

Admin should own:

- operator visibility;
- proposal and approval surface;
- dry-run display;
- execution contract preview/read model;
- closure records;
- audit search/export surface;
- controlled operator invocation surface;
- runtime verdict display;
- evidence lineage and operation timeline.

Admin should display:

- signals and freshness;
- policy/trust/capacity/eligibility evidence;
- autoswitch plan/dry-run;
- selected-move visibility;
- restore-barrier status;
- runtime outcome;
- rollback previews/results;
- audit and closure state.

Admin should approve:

- operator intent;
- closure transitions;
- governed manual actions;
- future runtime-owner-bound actions.

Admin should close:

- evidence objects;
- proposals;
- runtime/current objects;
- release/trust/drift objects;
- operation lifecycle records once runtime outcome and audit evidence exist.

Admin should never execute directly as lifecycle owner:

- direct user movement outside runtime ownership;
- independent selected-move execution;
- independent planner execution as truth;
- independent rollback as lifecycle truth;
- sentinel-triggered runtime actions;
- closure without runtime/audit backing.

Visibility-only:

- execution contracts until ownership-connected;
- operator rehearsal/governance previews;
- selected-move file adapters;
- historical operation timelines.

## Audit Model

Primary audit owner:

`tools/runtime-support/v7-audit-log`

Canonical audit truth:

- structured events written through `v7-audit-log`;
- Admin actions should continue to use `audit_admin` as wrapper into `v7-audit-log`;
- runtime owner outcomes should be represented as audit events when connected later.

Supplemental evidence:

- Admin action responses;
- operator observability timeline;
- service matrix event JSONL;
- Telegram sentinel event JSONL;
- autoswitch stdout/systemd journal;
- execution preview stores.

Historical evidence:

- markdown reports;
- historical approval packets;
- evidence bundles from prior blocks;
- raw fallback records.

Closure evidence:

- Admin closure records;
- final runtime outcome from autoswitch;
- audit event proving close/terminal state;
- operator export preview.

Audit relationship to runtime ownership:

- Runtime owner produces the facts of execution.
- Audit owner records canonical events.
- Closure owner interprets terminal state and records closure.
- No separate audit truth source should be created.

