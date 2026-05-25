# V7 Phase 5 Organization Isolation

## Purpose

Organization isolation prevents accidental access mixing between companies.

## Isolation Dimensions

Organizations must be isolated across:

- identity visibility;
- allowed user list;
- device lifecycle;
- route eligibility;
- egress eligibility;
- diagnostics visibility;
- commercial/accounting hooks.

## Current Foundation

The current platform already has:

- `organizations`;
- `groups`;
- `allowed_users`;
- `identity_users.organization_id`;
- `identity_users.group_id`;
- `/etc/v7/org-egress-policy.json`;
- audited organization and allowed-phone updates.

## Required Contract

Organization-scoped actions must always know:

- acting admin;
- target organization;
- affected users/devices;
- before/after state;
- reason or workflow context.

## Egress Eligibility

An organization may use only egress resources allowed by policy.

If policy is missing or ambiguous, the safe behavior is:

- no silent privilege expansion;
- operator-visible warning;
- no automatic migration across isolation boundaries.

## Diagnostics Visibility

Operator views should first show:

- affected organizations;
- affected user count;
- affected route classes;
- affected egress.

Raw per-user details belong in drill-down views.

## Forbidden Behavior

V7 must not:

- silently assign users to another organization's egress;
- show unrelated organization details in scoped views;
- let autoswitch bypass organization policy;
- reuse stale delivery links across organizations;
- treat phone number alone as commercial tenant proof when organization policy disagrees.

