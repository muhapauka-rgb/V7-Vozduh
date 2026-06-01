# P4 Rollback Model

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Rollback Authority

P4 defines rollback planning only.

Rollback execution remains forbidden.

## Rollback Scope

Rollback scope must be no broader than the action scope and must name:

- affected users or objects
- previous target/state
- restoration target
- verification checks
- observation window
- operator decision point

## Rollback Triggers

- post-action health failure
- route verification failure
- capacity regression
- user impact beyond scope
- hidden movement detection
- rollback target drift
- failed observation checkpoint
- operator abort

## Rollback Verification

Rollback plan must include:

- pre-action rollback preview
- post-action rollback feasibility check
- route/runtime checker list
- audit/event proof requirements
- restore-settle or equivalent settle window when applicable

## P4 Boundary

P4 creates no rollback executor and runs no rollback.

## Verdict

`rollback_model_defined=true`

