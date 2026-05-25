# V7 Phase 8 Controlled Experimentation Framework

## Purpose

Experiments must be isolated, opt-in, measurable, and reversible.

## Experiment Requirements

- explicit operator opt-in;
- isolated users, orgs, channels, or route classes;
- quarantine-first for new egress;
- no production-wide default;
- measurable success criteria;
- rollback plan;
- audit entry;
- expiration window.

## Experiment States

- proposed;
- approved;
- isolated;
- running;
- paused;
- completed;
- rolled_back;
- rejected.

## Forbidden Experiments

- silent production-wide routing experiments;
- hidden protocol changes;
- unbounded stealth escalation;
- experiments on trusted RU without safety gates;
- experiments that bypass kill switch or policy.

