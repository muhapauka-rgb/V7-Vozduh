# Engineering Report: A3 Stale Approval Preflight Stop

Status: HISTORICAL_EVIDENCE
Date: 2026-06-26T15:26:56+0700
Backlog item: A3

## Summary

The operator approved the previous A3 packet, but production reality changed before execution. V7 rejected the stale approval before creating a new lease, writing restore-barrier clearance, applying movement, or moving any user.

## Action Performed

- Treated the operator message `Approve` as approval for the current known packet `pkt_preview_4eb137c926917c2761faadb4`.
- Ran production preflight through the existing governed canary dry-run owner.
- Compared current packet identity against the approved packet identity.
- Stopped before all mutation-capable steps when the packet identity changed.
- Ran truth and convergence after the safe stop.

## Objective Observations

- Approved packet: `pkt_preview_4eb137c926917c2761faadb4`.
- Approved user: `10.7.0.17`.
- Approved move: `vless -> awg0`.
- Approved selected move hash: `e1e09d2c95fc6c9b0b77e9ecaaf0def20e9759150eb35db8d70f95e107eb52cd`.
- Current packet: `pkt_preview_c72b642b2b6cd55532979944`.
- Current user: `10.7.0.5`.
- Current move: `awg0 -> wireguard-1779454504-c43409`.
- Current selected move hash: `2d0af437b5fa7131596633a669014e24b5cdb55a943d4ee30b64956d990d968c`.
- Restore-barrier written: `false`.
- Apply executed: `false`.
- Users moved: `0`.
- Rollback executed: `false`.
- Authority expanded: `false`.
- Truth: `PASS`.
- Convergence: `PASS`.

## Engineering Conclusions

The stale approval protection worked correctly. The approved packet was no longer the current packet, so the system refused to bind the old approval to a new production action.

This is an operational authority stop, not an unsafe implementation defect.

## Impact

- No production mutation occurred.
- A3 remains `IN_PROGRESS`.
- The current stop remains `OPERATIONAL_AUTHORITY`, now for packet `pkt_preview_c72b642b2b6cd55532979944`.
- Production Maturity remains unchanged.

## Capability Progress

Movement Protection and Authority Evolution gained fail-safe evidence for stale approval rejection. A3 certification did not progress because no real movement outcome occurred.

## Backlog Progress

A3 remains the highest priority backlog item.

## Production Maturity

Production Maturity remains `21.5%`.

## Canonical Knowledge

No new canonical knowledge was discovered. This event confirms the existing packet identity and operational authority rules.

## Evidence

- Preflight blocker: packet identity mismatch.
- Current packet preview id: `pkt_preview_c72b642b2b6cd55532979944`.
- Current operation id: `govdry_3252ccec7fc7335c069d5a84`.
- Current rollback manifest id: `rb_preview_25caf0af554686e597a37116`.
- Truth result: `PASS`.
- Convergence result: `PASS`.

## Next Step

Approve or reject exact packet `pkt_preview_c72b642b2b6cd55532979944`.

## Re-audit Rule

Do not re-audit stale approval behavior unless packet identity validation, execution lease binding, or operational authority semantics materially change.
