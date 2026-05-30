# E34.E Operator Responsibility Model

operator_responsibility_defined=true

## Purpose

Operator Independence means a non-author operator can run V7 safely without Codex, the original developer, or historical memory.

The operator is responsible for driving operational problems through a bounded workflow:

```text
Problem -> Evidence -> Diagnosis -> Action -> Verification -> Closure
```

The operator is not responsible for inventing hidden system behavior, bypassing governance, or guessing remediation.

## Responsibility Domains

| Domain | Operator responsibility | Required guardrail |
| --- | --- | --- |
| Monitoring | Notice degraded, stale, failed, blocked, or drifted state. | Dashboard must expose current status and blocker reason. |
| Diagnosis | Collect evidence, compare plausible causes, and identify root cause. | Runbook must require evidence before action. |
| Recovery | Execute guided recovery only after gates pass. | Recovery action must be scoped and reversible. |
| Rollback | Use certified rollback paths for release, config, routing, or governance. | Rollback must include verification and closure. |
| Release handling | Verify release identity, provenance, certification, and rollback release. | Unknown release lineage is blocking. |
| Backup handling | Confirm backup freshness, completeness, encryption, and restore readiness. | Unverified backup cannot certify restore safety. |
| Escalation | Escalate when authority, evidence, or safe action is missing. | Escalation is a safe terminal outcome, not failure. |

## Non-Responsibilities

Operators must not:

- move users outside an approval packet;
- execute autoswitch apply manually;
- alter kill-switch state as a routine recovery shortcut;
- deploy unknown releases;
- restore from uncertified backups;
- ignore runtime/repo drift;
- lower capacity, policy, or readiness gates to make an operation pass.

## Authority Boundaries

Operator authority is procedural, not absolute.

An operator may:

- gather evidence;
- trigger read-only diagnostics;
- follow approved recovery or rollback runbooks;
- request certification or escalation.

An operator may not:

- override fail-closed gates without a separately certified emergency policy;
- mutate runtime from an architecture-only workflow;
- convert a diagnostic hypothesis directly into action.

## Closure Requirement

Every operational problem must end with one of:

- `CLOSED_FIXED`
- `CLOSED_NO_ACTION_NEEDED`
- `CLOSED_ESCALATED`
- `CLOSED_FAIL_CLOSED`
- `CLOSED_REQUIRES_ARCHITECTURE_DECISION`

Open-ended “probably fixed” outcomes are not allowed.
