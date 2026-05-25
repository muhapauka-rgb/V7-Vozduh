# V7 Phase 5 Onboarding And Recovery UX

## Purpose

Onboarding must feel like "internet simply works".

Users should not understand:

- route classes;
- egress;
- transports;
- DNS path;
- kill switch;
- autoswitch.

## User Flow

The user flow should stay minimal:

1. Identify with organization, phone, name, and connection password.
2. Receive or import the prepared profile.
3. Connect.
4. Reconnect or restore access if needed.

## Recovery UX

Recovery actions should be simple:

- resend profile link;
- rotate profile;
- reconnect;
- revoke stale device;
- issue additional device.

The user should not be asked to diagnose networking.

## Operator Flow

Operator sees:

- onboarding status;
- pending confirmations;
- failed attempts;
- profile delivery state;
- device readiness;
- route/readiness blockers.

Operator should not see a noisy identity dashboard by default.

## Current Useful Foundation

Current admin already exposes:

- connect sessions;
- onboarding attempts;
- pending profiles;
- user readiness;
- onboarding stage;
- profile delivery summaries.

## UX Rule

Identity UX should be grouped around workflows:

- invite;
- issue;
- reconnect;
- revoke;
- recover.

Not around raw database tables.

