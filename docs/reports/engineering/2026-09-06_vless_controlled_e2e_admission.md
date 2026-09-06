# VLESS controlled E2E admission — 2026-09-06

## Decision

`STOP_SAFE_SHARED_VLESS_NO_ISOLATION`

This is the result of fresh read-only discovery through the existing
`v7-users-autoswitch` topology owner, existing `v7-egress-guard`, and the
canonical Matrix state.  No fault, source reservation, user switch, route
change, policy write, Authority decision, or Runtime write was performed.

## VLESS state

- Egress: `vless`; protocol `vless`; interface `tun0`; enabled.
- The current egress guard returns
  `controlled_certification_source_not_marked`.
- Topology owner sees zero ordinary identities and one certification identity
  on VLESS.  It does not reveal raw user identities.
- The VLESS source is not an independently controllable controlled-failure
  boundary, is not empty-reservation eligible, and has no active controlled
  reservation.
- Its compact topology fingerprint is
  `c7b6c635b7c7c7f5635736e27cbcf1f2ce2fd1f537c8f05227f09f3b694fb39b`.

Therefore a whole-VLESS physical failure would currently affect the one
certification identity, but no owner proves that the channel may carry the
required five-user certification-only cohort or that its fault is governed as
a controlled experiment.  `ordinary_identities = 0` is a current inventory
fact, not permission to reassign users or inject a fault.

## Health and route admission

The canonical Matrix VLESS row is stale (`2026-09-05T07:02:22Z`) and is not a
healthy baseline: status `WARN`, one of fourteen services OK, `VIDEO_OPTIMIZED`
is `FAIL`, and both `GLOBAL_*` and `LOW_LATENCY` are `WARN`.  VLESS uses `tun0`;
the currently reported channel-level route state does not establish a healthy
required-service baseline.  A fault must never be injected into an already
unhealthy source.

A fresh, non-writing required-service S11 observation was nevertheless run
through the existing Matrix owner: Telegram passed all 5 required endpoints on
`tun0`.  This proves only that one S11 probe is currently reachable.  It does
not repair or replace the stale full Matrix baseline, source reservation, or
five-user source admission.

## Target discovery

The topology owner sees a currently healthy shared WireGuard destination with
capacity for the five-user stage, but it has 49 ordinary identities.  It may
never be faulted.  Its use as destination requires the existing exact shared
target action-class contract and fresh Planner revalidation; that contract is
not active.  Thus there is no present lawful target for this VLESS experiment.

## Minimal lawful preparation

1. Existing VLESS/channel owner restores and proves a fresh healthy Matrix
   baseline on `tun0`.
2. Existing source reservation/classification owner marks and reserves VLESS
   as a certification-only controlled source with zero ordinary users.
3. Existing registry/Authority owner admits exactly five existing
   certification users, with zero new identities and preserved ordinary routes.
4. Existing target owner produces a fresh healthy target and the exact
   destination contract without a source-target collision.
5. Only after all four receipts are current may the controller authorize one
   physical VLESS failure and the owner chain execute it.

## Runtime truth gate

The final fresh Runtime truth check returned `RUNTIME_NO_GO`: Runtime remains
at `328b0185`, while the current source is `031b016f`.  The differing
deploy-required path is `tools/v7_sync_lib.py`, which contains the corrected
five-user Polygon baseline gate.  No experiment may run against the older
Runtime contract.  A future safe deployment and fresh Runtime convergence
check are necessary only after the VLESS/source and target admission receipts
above exist; deployment alone cannot satisfy those receipts.

## Material-block A terminal

`STOP_SAFE_VLESS_EXTERNAL_PEER_OR_CONFIG_RECOVERY_REQUIRED`

The canonical full baseline was refreshed at `2026-09-06T19:37:03Z` through
the existing Matrix writer. Its verdict remains `WARN`: Telegram is the only
healthy service; all other thirteen required HTTP services time out at roughly
ten seconds. Existing path evidence passes for interface, firewall, policy and
routing-table observations, so this is not a missing local route proof.

The existing `sing-box.service` is active, but its own current diagnostics
record `EOF` while opening connections through `outbound/vless[vless-out]` to
required endpoints. `v7-egress-set-state` can change registry state,
reservation or controlled-failure condition; it cannot repair the remote VLESS
peer or lawfully replace `/etc/sing-box` configuration. That is a new external
input. Steps B--H are not legally reachable until the VLESS owner provides a
healthy peer/configuration and the full Matrix baseline then passes.

### Read-only external-owner diagnostic

At `2026-09-06T19:42:58Z`, the existing owner command
`/usr/local/bin/v7-egress-diagnose --output -` returned
`vless_diagnose_reason=curl_failed_and_handshake_unsupported` and
`vless_diagnose_severity=FAIL`.  It made no configuration, Matrix, route,
user, Authority, or external-infrastructure change.

The exact secret-free owner identity available to V7 is
`REMOTE_VLESS_LISTENER_OR_PROFILE_CONFIGURATION_OWNER_FOR_EGRESS_vless`:
the active local profile terminates at `sing-box` outbound `vless-out`, while
the remote listener/TLS peer and matching profile material are outside the
local V7 ownership boundary.  No inventory provides a more specific external
owner identity; inventing one would be false attribution.  The lawful
re-entry is an owner-verified healthy peer/profile followed by a fresh full
VLESS Matrix baseline.

## VLESS_ROOT_CAUSE_DECISION

`LIKELY_EXTERNAL_VLESS_LISTENER_OR_PROFILE_REJECTION_OR_EXPIRY`
(`MEDIUM_HIGH`, bounded to the evidence below; this is not attribution to a named
third party).

| Decision element | Evidence | Conclusion |
| --- | --- | --- |
| Last owner-backed good | `docs/track7/control-plane/e9_3_3-evidence/pre-rehearsal.txt` records `2026-05-25T22:16:44+03:00`, `vless_diagnose_reason=OK`, `vless_diagnose_detail=proxy_test_ok`. | VLESS was demonstrably usable on or before 25 May. |
| Earliest available owner-backed bad | `docs/reports/engineering/2026-08-26_v5_3_telegram_post_fix_clean_evidence_and_pasha_reconciliation.md` records that `vless` failed its current Matrix baseline. The retained live `egress-history.jsonl` is empty, so it cannot tighten the transition time. | Proven regression window: after 25 May and no later than 26 August; no false exact outage time is claimed. |
| Current local profile provenance | Current `/etc/sing-box/config.json` fingerprint is `6c89a44f7a187389030733ec03657b6d3c60ee8da2cc84fad4876f39e2342e9f`; its mtime/ctime and `sing-box.service` start are all `2026-05-12 02:06:14 +0300`. The VLESS registry identity remains `id=vless`, `protocol=vless`, `type=proxy`, `interface=tun0`, enabled. | There is no evidence of local VLESS config drift, service restart, or post-good local deployment causing this regression. |
| Current failure locus | The existing read-only diagnose returned `curl_failed_and_handshake_unsupported` / `FAIL`; current summary is `vless_code=000`, speed `0`; retained `sing-box` logs contain 237 `outbound/vless ... EOF` records, beginning `2026-09-06T08:27:30+03:00`. Earlier path evidence passed for interface, firewall, policy and routing. | Local process/path presence is intact; the failure occurs after the local VLESS outbound attempts its remote peer/profile exchange. |

The evidence rules out a recent local configuration or service change with high
confidence. It does not prove whether the remote listener is down, rejects the
profile, or the profile has expired/changed; those alternatives share the same
external owner boundary. Local DNS/TLS/network causation is not independently
proven, but is less likely because local path evidence passes and the failure
is a peer-side `EOF` across the required services.

**Minimal repair owner/action:** external VLESS listener/profile-configuration
owner restores the listener or provides an owner-verified current matching
profile. This is an **external** action. After that input exists, the existing
local egress-draft/configuration lifecycle may validate and stage it; no local
repair or configuration mutation is proposed or authorized before a controller
approval. The sole re-entry proof remains one fresh read-only diagnosis without
`curl_failed_and_handshake_unsupported`, followed by the fresh full Matrix
baseline.

### Final local discriminator

One controller-authorized read-only discriminator completed at
`2026-09-06T23:29:00+03:00`, without a VLESS handshake retry or any mutation:

- `sing-box check -c /etc/sing-box/config.json`: `PASS`;
- system clock: NTP synchronized; system CA bundle present;
- the one configured VLESS endpoint is a literal-IP profile identity
  (`endpoint_fingerprint=062b035c35a7960a37f3a0d687ab85a2b6906a7cb3f9778e36291cf3d9626f57`),
  has TLS SNI configured, and accepted one basic TCP connection;
- `sing-box` retained 238 VLESS outbound `EOF` records from
  `2026-09-06T08:27:30+03:00` through `2026-09-06T23:28:56+03:00`.

`VLESS_ROOT_CAUSE_DECISION: EXTERNAL_PROFILE_OR_LISTENER_REPAIR_REQUIRED`
(`HIGH`). Local DNS does not participate in this literal-IP profile, and the
current config, local clock, CA store, process, basic TCP path and local route
evidence all pass. The remaining failure is after TCP establishment, in the
remote listener/TLS/VLESS-profile exchange, which is outside local V7 control.

**External handoff (non-secret):** repair or replace the remote listener and
provide an owner-verified profile matching local config fingerprint
`6c89a44f7a187389030733ec03657b6d3c60ee8da2cc84fad4876f39e2342e9f` and
endpoint fingerprint above; observed symptom is continuous local
`outbound/vless` `EOF` after TCP success. No local repair is justified. The
existing local egress-draft/configuration lifecycle may validate and stage an
owner-supplied profile only after controller approval.
