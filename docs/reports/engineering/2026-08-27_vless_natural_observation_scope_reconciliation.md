Mission ID: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
Run Nonce: `V7_VLESS_NATURAL_OBSERVATION_20260827_01`

# VLESS natural observation and scope reconciliation

## Observation

At `2026-08-27T14:28:21Z` the existing Matrix owner ran a fresh full probe for
`vless` (`tun0`).  Telegram passed; the remaining service probes mostly failed
with TLS connection resets or EOF.  Matrix returned `WARN` and wrote the
observation through its existing lock.  No route or user mutation was allowed
by this operation.

The immediately preceding read-only Telegram-only probe also passed at
`2026-08-27T14:27:15Z`.  Therefore the current evidence is a partial
service-plane degradation, not a proven total channel outage.

## Current scope and safety

- `egress.registry` identifies `vless` as a certification-controlled source;
  its reservation is still owned by `operator_execution_governance`.
- Current `users.registry` has one `vless` row, `10.7.0.7`, and it is
  disabled (`enabled=0`).  Active ordinary affected scope is therefore zero.
- Fresh Matrix events classify the observed VLESS scope as `EMPTY` with
  `affected_scope_count=0`; the latest fresh failure event is
  `sfe_1e0021387fa48b6f265f6a688ae08426` (Instagram).
- No Candidate, Packet, Lease, Apply or recovery action was created.  No
  ordinary client moved and no route changed.

## Decision

The event is now observable through the canonical Matrix path, but it cannot
provide production failover evidence because there is no active ordinary
VLESS scope.  The current Program remains at
`WAIT_FOR_REPRESENTATIVE_REAL_LEARNING_OUTCOMES`; no synthetic cohort or
manual client movement is lawful.  A future fresh event with a non-empty
active ordinary scope is the exact re-entry condition.

## Evidence

- Runtime/Matrix owner: `v7-health.service` active.
- Matrix canonical write: `service-matrix.json`, no alternate writer.
- Matrix probe mode: existing `tools/v7-service-matrix-test`; no new owner,
  timer, queue, registry or truth source.
- The final all-scope truth check before this observation was `PASS`; this
  observation does not change the engineering terminal or Authority state.

## Next step

Keep the current passive capture ready.  Re-enter the V7 program only when
Matrix records a fresh owner-backed VLESS incident with a non-empty active
ordinary scope, or when another qualifying natural outcome arrives.
