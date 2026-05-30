# E32.3.A Policy Lifecycle

policy_lifecycle_defined=true

## Lifecycle States

```text
DRAFT
REVIEW
ACTIVE
DEPRECATED
EXPIRED
REVOKED
SUPERSEDED
```

## State Semantics

### DRAFT

Meaning:

Policy is being authored.

Allowed use:

- static review;
- dry-run tests.

Forbidden use:

- admission decisions.

### REVIEW

Meaning:

Policy is awaiting governance review.

Allowed use:

- simulation;
- conflict testing.

Forbidden use:

- production admission.

### ACTIVE

Meaning:

Policy is effective for admission decisions.

Allowed use:

- admission evaluation;
- denial;
- review requirements;
- gate requirements.

Forbidden use:

- mutation by itself.

### DEPRECATED

Meaning:

Policy remains visible but should not authorize new actions unless explicitly grandfathered.

Allowed use:

- audit;
- migration warning.

Forbidden use:

- new forward allow decisions by default.

### EXPIRED

Meaning:

Policy has passed expiration.

Allowed use:

- audit only.

Forbidden use:

- allow decisions.

### REVOKED

Meaning:

Policy was invalidated due to incident, contradiction, or governance decision.

Allowed use:

- audit and incident review.

Forbidden use:

- all admission allows.

### SUPERSEDED

Meaning:

Policy was replaced by newer version.

Allowed use:

- audit and lineage.

Forbidden use:

- new admission unless explicit migration rule exists.

## Transition Rules

Allowed:

```text
DRAFT -> REVIEW
REVIEW -> ACTIVE
ACTIVE -> DEPRECATED
ACTIVE -> EXPIRED
ACTIVE -> REVOKED
ACTIVE -> SUPERSEDED
DEPRECATED -> EXPIRED
DEPRECATED -> REVOKED
```

Disallowed:

```text
EXPIRED -> ACTIVE
REVOKED -> ACTIVE
SUPERSEDED -> ACTIVE
```

Reactivation requires new version and new review.

## Audit Requirements

Every transition must record:

- policy id;
- old status;
- new status;
- actor or authority;
- reason;
- timestamp;
- audit lineage id.

## Lifecycle Verdict

Policy lifecycle is defined and fail-closed.
