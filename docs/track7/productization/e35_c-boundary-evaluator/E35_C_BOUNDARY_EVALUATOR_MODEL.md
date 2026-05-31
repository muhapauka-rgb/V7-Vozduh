# E35.C Boundary Evaluator Model

## Definition

Boundary Evaluator:

```text
Checks whether a proposed action is allowed.
```

Russian meaning:

```text
Проверка допустимости действия.
```

## Core Rule

The evaluator does not execute.

It does not move users.

It does not choose targets.

It only produces:

```text
ALLOW
DENY
REVIEW_REQUIRED
EMERGENCY_ONLY
```

## Product Meaning

V7 has a single consistent gate that answers:

```text
May this actor perform this action on this user/channel now?
```

## Operator Meaning

Admin can show:

- why movement is allowed;
- why movement is blocked;
- what needs review;
- whether only emergency action is allowed.

## Runtime Mapping

Called before:

- autoswitch apply;
- manual switch;
- governed execution;
- scheduler execution;
- containment action.

## Storage Impact

Stores verdict events, not movement state.

Primary future stores:

- authority state;
- verdict event log;
- conflict event log.

## API Impact

Read APIs expose verdicts, conflicts, reviews, emergency state and explanations.

No mutation API in E35.C.

## Admin Surface

Existing `/admin-v2` surfaces:

- Home summary;
- Users drawer;
- Channels drawer;
- Checks;
- Logs.

## Tests

- evaluator returns deterministic verdict;
- evaluator never calls movement commands;
- missing critical input fails closed;
- no score/speed-only action can override boundary.

## Verdict

```text
boundary_evaluator_defined=true
```
