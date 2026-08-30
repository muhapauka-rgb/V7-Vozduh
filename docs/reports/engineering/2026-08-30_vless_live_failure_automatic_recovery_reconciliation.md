# VLESS: live failure and automatic recovery reconciliation

Date: 2026-08-30

## Current factual state

The current Matrix classifies `vless` as `WARN`, not healthy. Fresh probes on
the live source recorded failures for Google (TLS EOF), Google Auth, Instagram
and YouTube (timeout). Telegram alone remained reachable; it does not make the
channel suitable for profiles requiring the failed services.

## Work completed

1. Reconciled the prior ordinary recovery lease that had reached a terminal
   no-apply result but remained active. The existing Matrix owner now closes
   only an exact finished, unapplied lease after it verifies that no governed
   route worker is running and every bound user is still on the source.
   Commit: `1b2e46bc`.
2. Bound the existing Core-primary cohort owner to the already-issued standing
   emergency-failover contract and its exact operation-scoped execution window;
   the old Reset-only contract remains required for Reset paths. No new owner,
   policy source or route writer was added. Commit: `5911b44b`.
3. Reconciled the ordinary production scope name used by the Matrix producer
   with the existing direct handoff consumer. Commit: `a1f26ca3`.

## Verification

- Focused and related unit suites: 372 passing tests.
- Safe deployment, GitHub, local tree and deployed runtime are aligned at
  `a1f26ca3764945be4595f6ec62717c1986460144`.
- `v7-health.service` is active.
- No client was moved by engineering commands.

## Live automatic evidence

After the handoff correction, V7 itself created a new bounded transaction for
two ordinary users on `vless`, created Candidate/Packet/Lease and selected an
existing healthy target. The transaction then stopped before route mutation at
`approved_plan_lock_selected_moves_missing`.

This is an unresolved generic Packet/Barrier handoff defect. It is not a
health verdict that makes VLESS acceptable, and it is not valid recovery
evidence. The next task is to retain the exact current Packet lock through
the existing automatic apply consumer, then allow the live V7 caller—not
engineering—to complete and verify the recovery.
