# CT-M0F: topology provision consumed; controlled-source health boundary

**Date:** 2026-08-12  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Parent Mission:** `CT-M0F`

## Result

`APPROVED_TOPOLOGY_PROVISION_CONSUMED; EXTERNAL_INFRASTRUCTURE_OR_ACCESS_REQUIRED_FOR_CONTROLLED_SOURCE_HEALTH`.

The existing Authority decision was consumed exactly once by the existing
reservation owner.  It reserved the already materialized, empty production
source and published an append-only receipt.  No route was mutated and no user
was moved.

## Delivered owner chain

`Authority audit decision -> Matrix consumer -> users-autoswitch provision
consumer -> v7-egress-set-state reservation owner -> append-only receipt`.

- Authority request: `cstopauth_r1_6b395c70d2db7a54d8a0425e`
- Decision: `cstopdec_3cc01259228243303ae71c26`
- Draft: `1-1779291887-55965c`
- Existing source: `1`
- Reservation: `ctres_08031f22a01aaf4563b5a99d`
- Receipt hash: `56ca0950e8dbebb90aa9ba6dd91d614254737810259808c50b532c5bf946b712`
- Expiry: `2026-08-12T09:53:43.101757+00:00`

The deployed generic repair also prevents a source with an expired reservation
or a non-one-user certification cohort from being classified as a CT-M0F
``empty`` source.  This closes the source-selection defect without a
VLESS-specific exception.

## Verification

- Focused owner tests passed before deploy.
- Safe deploy `deploy-z8-14-Updatesystem-b41b038-20260812T122159` passed its
  manifest with only `tools/v7-users-autoswitch` changed.
- Earlier bridge deploy `deploy-z8-14-Updatesystem-99039e7-20260812T121454`
  passed with only `admin_core/operator_execution.py`,
  `tools/v7-users-autoswitch`, and `tools/v7-service-matrix-refresh-all`.
- The production caller returned `CONTROLLED_SOURCE_TOPOLOGY_PROVISIONED`.
- Effects: `registry_write=true`; `routing_mutation=false`; `users_moved=0`;
  Candidate, Packet, lease, controlled failure, rollback and Natural L8 credit
  are all absent.
- The ordinary Matrix service completed successfully and independently
  consumed its existing safe successors; it did not create an action.

## Exact terminal and re-entry

The exact source-health owner reports:

`STOP_SAFE_BASELINE_UNHEALTHY`

- source: `1` / interface `v7e356a192b79`
- services reachable: `0/14`
- diagnostic: `curl_failed_and_handshake_stale`
- handshake age: `999999` seconds
- classification: `EXTERNAL_INFRASTRUCTURE_OR_ACCESS_REQUIRED`
- missing producer-consumer link:
  `EXTERNAL_AMNEZIAWG_PEER_RESPONSE_OR_MATCHING_PROFILE -> LOCAL_HANDSHAKE -> MATRIX_BASELINE`

V7 must not assign the certification identity, create a Candidate/Packet/lease,
inject a controlled failure or move any route while this predicate fails.

**Re-entry condition:** the external AmneziaWG peer/profile owner restores a
reachable matching peer for the exact approved source; the next ordinary Matrix
observation must prove at least one reachable service and zero hard failures.
The existing CT-M0F source-selection and controlled-condition consumers then
continue automatically under the active one-user standing policy.
