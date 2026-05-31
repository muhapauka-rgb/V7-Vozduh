# E35.C Review Required Model

## Definition

`REVIEW_REQUIRED` means:

```text
Machine cannot safely allow movement without human/governance decision.
```

## Review Triggers

- group conflict;
- authority conflict;
- stale runtime trust;
- stale release trust;
- unknown suitability;
- expired authority;
- policy ambiguity;
- operator override request;
- missing evidence;
- unknown conflict type.

## Who Reviews?

| Review Type | Reviewer |
|---|---|
| group conflict | operator/admin |
| protected user override | operator + governance if movement follows |
| stale trust | operator after checks |
| policy ambiguity | operator/product owner |
| emergency conversion to permanent | operator/governance |

## Data Shown

Admin review item must show:

- proposed action;
- user;
- current/target channel;
- authority mode/owner;
- conflict type;
- blocking domain;
- evidence/proposal links;
- runtime trust;
- service/capacity/suitability summary;
- next safe actions.

## Audit Created

Events:

- `REVIEW_CREATED`;
- `REVIEW_CLOSED`;
- final verdict reference.

## Runtime Meaning

Forward movement is denied until review closes with a new valid authority/governance state.

## Verdict

```text
review_model_defined=true
```
