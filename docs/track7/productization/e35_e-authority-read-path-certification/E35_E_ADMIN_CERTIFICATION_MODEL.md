# E35.E Admin Certification Model

## Authority Explanation Contract

Operator must always understand:

- who owns routing;
- why user is here;
- why movement is allowed;
- why movement is denied;
- why review is required;
- why emergency exists.

## Required Admin Fields

Users:

- routing mode;
- owner;
- current channel;
- preferred/pinned/manual target;
- status;
- conflict/review/emergency flags;
- source freshness.

Channels:

- pinned users;
- authority conflicts;
- emergency usage;
- boundary violations.

Checks:

- authority read-path health;
- drift count;
- stale read models;
- API consistency state.

Logs:

- authority events;
- conflicts;
- reviews;
- emergency state changes.

Home:

- summary only.

## Certification Rule

Admin may summarize but must provide drill-down to source-linked explanation.

## Verdict

```text
admin_certification_defined=true
```
