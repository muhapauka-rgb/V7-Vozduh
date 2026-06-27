# A4 Stale Approval Stop

Status: STOPPED_SAFE
Date: 2026-06-27

## Summary

Operator approved the prior A4 packet:

`pkt_preview_c72b642b2b6cd55532979944`

Before creating lease, restore-barrier clearance, or apply, V7 performed a fresh production recheck.

The fresh packet changed to:

`pkt_preview_2cb1fe3b8ce1551c75ccff11`

V7 stopped safely.

## Action Performed

Read-only production governed dry-run was executed before apply.

No execution lease was created for the stale packet.

No restore barrier was written.

No apply was executed.

No rollback was needed.

No user was moved.

## Objective Observations

Fresh packet:

- packet: `pkt_preview_2cb1fe3b8ce1551c75ccff11`
- decision: `decision_commit_66953558b80b8f5fdfc93807`
- operation: `govdry_67a8120c92718b98e6b38f4f`
- selected move hash: `7ba975860c901f49a5194cb84791c394cfdb737654864b49e4e75e416096585f`
- user: `10.7.0.18`
- move: `vless -> awg3`
- rollback manifest: `rb_preview_5e7201af4a2afb2ad89736b4`

Prior approved packet:

- packet: `pkt_preview_c72b642b2b6cd55532979944`
- user: `10.7.0.5`
- move: `awg0 -> wireguard-1779454504-c43409`

## Engineering Conclusions

The approved packet became stale before execution.

Existing safety behaved correctly:

- stale approval did not bind to the new packet;
- different user/target/hash were not silently accepted;
- execution stopped before mutation.

## Impact

A4 remains blocked by `OPERATIONAL_AUTHORITY`.

The current exact packet requires fresh operator approval before restore-barrier write or apply.

## Capability Progress

Movement Protection: unchanged.

Authority Evolution: unchanged.

Learning: unchanged.

Production Autonomy: unchanged.

## Backlog Progress

A4 remains `TODO`.

No representative production outcome was recorded.

## Production Maturity

Production Maturity unchanged: `24.0%`.

## Canonical Knowledge

No new canonical knowledge.

This confirms the existing rule:

stale exact packet approvals must fail closed before mutation.

## Evidence

Fresh production dry-run returned a different packet identity before apply.

Observed stop:

`A4_EXECUTION_STOPPED`

Reason:

`approved_packet_not_current`

## Next Step

Operator must approve or reject the current exact packet:

`pkt_preview_2cb1fe3b8ce1551c75ccff11`

## Re-audit Rule

Do not re-audit stale approval handling unless stale approval is accepted, mutation occurs after packet mismatch, or operator explicitly requests it.
