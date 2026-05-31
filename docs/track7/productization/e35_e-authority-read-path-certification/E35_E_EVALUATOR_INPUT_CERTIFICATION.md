# E35.E Evaluator Input Certification

## Goal

Before future execution, evaluator must receive correct authority state.

## Input Validation

Required:

- user exists;
- current route known;
- authority state resolved;
- source hash present;
- generated_at present;
- freshness within policy;
- required links available or marked unavailable.

## Input Completeness

Evaluator input must include:

- routing mode;
- authority owner;
- group boundary;
- trust state;
- selected moves state;
- hidden movers state;
- conflict/review/emergency context.

## Drift Detection

Evaluator context must be compared against API/read model source hash.

Mismatch:

```text
REVIEW_REQUIRED
```

or hard `DENY` for movement.

## Auditability

Verdict event records:

- input hash;
- source version;
- generated_at;
- missing fields.

## Verdict

```text
evaluator_certified=true
```
