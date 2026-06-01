# Program F Reality Audit

Date: 2026-06-01
Branch: `v7-next`
Status: STOPPED_APPROVAL_PACKET_MISSING

## Repository

- Current branch: `v7-next`
- HEAD: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- `origin/v7-next`: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`

## Runtime Evidence

Fresh read-only evidence was collected into:

`/private/tmp/v7-program-f`

Files:

- `users.registry`
- `egress.registry`
- `runtime-guard.txt`
- `killswitch.txt`
- `user-route-check.txt`
- `runtime-contract.txt`
- `observability.txt`
- `safety-fixed.json`
- `shadow.json`
- `proposal-cap.json`
- `move-preview.json`
- `rollback-preview.json`

## Current Runtime Distribution

- registry rows: `19`
- enabled users: `18`
- `amneziawg-exec-20260528-10-8-1-14`: `10`
- `awg0`: `3`
- `awg3`: `3`
- `vless`: `2`

## Current Proposal

- user: `10.7.0.16`
- movement: `vless -> awg3`
- target interface: `awg3`
- rollback: `v7-user-switch 10.7.0.16 vless`
- budget: `1`

## Current Status

- proposal valid: true
- capacity valid: true
- target readiness valid: true
- rollback ready: true
- explicit approved packet present: false

## Reality Verdict

Program F cannot execute Stage 1 because the prompt says the explicit approval is pending and no approved packet was provided.

