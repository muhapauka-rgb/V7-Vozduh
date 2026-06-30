# Necessity Framework V2

Status: `COMPLETE`

Final verdict: `V7_NECESSITY_FRAMEWORK_V2_COMPLETE`

## Existing Sections Reused

Preserved and extended:

- Purpose;
- Scope;
- Non-Goals;
- Existing Philosophy Reused;
- Engineering Laws;
- Necessity Audit Model;
- Removal Test;
- Merge Test;
- Chain Completion Test;
- Production Value Test;
- Necessity Verdicts;
- Integration Contract;
- Framework Boundaries;
- Definition Of Done For Necessity.

No rewrite was performed.

## Lifecycle Added

Added `Necessity Lifecycle`:

```text
Idea
-> Need Identified
-> Creation Justified
-> Implemented
-> Integrated
-> Necessity Verified
-> Necessity Certified
-> Locked
-> Deprecated
-> Historical
-> Removed
```

## Trigger Model Added

Added `Necessity Trigger Model` for:

- new owner proposal;
- new capability proposal;
- new document proposal;
- new API / CLI / module / service proposal;
- capability completed;
- capability locked;
- architecture change;
- merge proposal;
- production incident;
- production maturity milestone;
- explicit operator request.

## Creation Test Added

Added symmetric Creation Test.

Creation now fails unless necessity is proven before creation.

## Necessity Certification Added

Added certification states:

- `NOT_REVIEWED`;
- `NECESSITY_VERIFIED`;
- `NECESSITY_CERTIFIED`;
- `INCOMPLETE`;
- `MERGE_REQUIRED`;
- `REMOVE_RECOMMENDED`;
- `HISTORICAL_ONLY`.

## Deferred By Reality Concept

Added `DEFERRED_BY_REALITY`.

Meaning:

```text
The component is genuinely necessary.
Current production reality does not justify implementation yet.
```

This distinguishes unnecessary from necessary but premature.

## Integration Impact

OMP integration remains documentation-only.

Future OMP shall execute Necessity Audit when component permanence, owner status, canonical status, lock status, merge, removal, or historical status is being decided.

No execution behavior changed.

## Canonical Owner Changes

Updated:

- `docs/reference/V7_NECESSITY_FRAMEWORK.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

## Need New Owner

`FALSE`

Existing owners remain sufficient.

## Need New Backlog

`FALSE`

No implementation task was created.

## Recommendation

Use V2 for future component creation, permanence, locking, deprecation, merge, removal, and historical classification decisions.

Do not create new V7 components without Creation Test.
Do not keep components permanently without Necessity Certification.
