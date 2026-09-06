# EXTERNAL_ISOLATED_SOURCE_REQUIRED — Polygon E2E evidence packet

## Verdict

`EXTERNAL_ISOLATED_SOURCE_REQUIRED`

Fresh read-only discovery through the existing
`v7-users-autoswitch --controlled-source-topology-diagnostic` owner returned:

`CONTROLLED_TOPOLOGY_FULL_PATH_EXTERNAL_RESOURCE_REQUIRED`

This is a resource/topology verdict, not a policy-only inference.  No source
reservation, registry write, user move, route mutation, fault injection,
packet, lease, or Production action occurred.

## Immutable observation identity

- Capability-map fingerprint:
  `d79038a589ac453913dc5b3e8a868ff481cf9f0fc3960484cc07e8fce37071bd`.
- Controlled-certification identity-set fingerprint:
  `d97ab1d596570d45d0fab25c78f954fd6153ecbd4e3ab5838e6a991633cf0916`.
- Current campaign source: empty.
- Authority lifecycle: `SUPERSEDED_STALE_PREFLIGHT`.
- Current selected topology: source empty, target set empty.
- Current source/target roles exact: false.
- All current planner targets: `HARD_INELIGIBLE` for execution.

The existing owner explicitly records:

`OWNER_VERIFIED_ISOLATED_CONTROLLED_TARGET_OR_CORRELATION_DISTINCT_TARGET_SET_WITH_USABLE_CAPACITY_AT_LEAST_48`

as its full-campaign external successor.  For the requested five-user Polygon
baseline, the narrower non-negotiable condition is still the same: one healthy
isolated controlled source, distinct from a healthy controlled target, with no
ordinary users in the source fault domain.  The current system has neither a
lawful source nor a lawful distinct target pair.

## Why current resources cannot be repurposed

The only identified healthy execution-only target is empty and reserved, but
does not pass current execution admission.  Existing certification users are
distributed across non-isolated or unavailable sources.  Reclassifying a
shared egress would make a whole-interface physical fault affect ordinary
scope; the topology owner rejects that as a source slice.  Reusing the target
as both source and destination would violate the existing source-target
collision law.

## Exact external input and lawful re-entry

An external egress/profile provider must make available a healthy,
owner-verifiable, isolated controlled source and a distinct healthy controlled
target (or a correlation-distinct target set), each with current Matrix,
quality, capacity, verification and restore evidence.  The existing admin
egress-draft lifecycle then becomes the only lawful producer.  Its successor
chain is:

`external resource owner → existing draft lifecycle → Matrix/quality/capacity
diagnostic → exact POLYGON_ONLY Authority admission → reuse-only five-user
substrate → one physical-fault E2E ledger`.

No user identity may be created or reclassified, and no ordinary source,
routing or failover action may be used to satisfy this packet.
