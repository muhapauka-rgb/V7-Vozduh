# E35.E Conflict Resolver Certification

## Goal

Conflict resolver must receive the same authority truth as evaluator.

## Input Validation

Required:

- same action id;
- same user id;
- same routing mode;
- same owner;
- same target;
- same source hash;
- same conflict candidate list.

## Freshness

Conflict input freshness must match evaluator input freshness.

## Drift Detection

If resolver input differs from evaluator input:

```text
REVIEW_REQUIRED
```

and `CONFLICT_INPUT_DRIFT`.

## Auditability

Conflict events include:

- evaluator verdict id;
- input hash;
- conflict type;
- outcome;
- winning domain.

## Verdict

```text
conflict_resolver_certified=true
```
