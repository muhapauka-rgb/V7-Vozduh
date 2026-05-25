# V7 Phase 5 Policy-Based Access

## Purpose

Access must be policy-driven and explainable.

Identity policy must not bypass datapath policy.

## Policy Inputs

Policy may come from:

- organization;
- group;
- allowed user;
- user;
- device;
- route class;
- org egress policy;
- maintenance state.

## Access Decisions

Policy must decide:

- whether user can onboard;
- whether device can be issued;
- which route mode/profile mode is allowed;
- which egress is eligible;
- whether trusted RU is allowed or required;
- whether direct routing is allowed;
- whether maintenance blocks new assignment.

## Current Foundation

Current code supports:

- group route policy through `groups.route_policy`;
- organization and allowed user linkage;
- org egress policy;
- device limit per user;
- safe-mode blocking for mutating identity actions;
- explicit confirm tokens for dangerous operations.

## Required Rule

Policy denial must be visible and explainable.

The system should say:

`organization policy does not allow this egress`

not:

`profile failed`

## Forbidden Behavior

V7 must not:

- silently issue profile outside org policy;
- silently fallback to unsafe route class;
- ignore suspended user state;
- issue device when device limit is exceeded;
- override maintenance restrictions.

