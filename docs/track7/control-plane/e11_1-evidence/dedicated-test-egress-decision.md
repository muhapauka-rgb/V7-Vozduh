# E11.1 Dedicated Test Egress Decision

Mode: read-only strategy decision.

## Options Compared

| Option | Strength | Weakness | Recommendation |
|---|---|---|---|
| Use WireGuard with reservation + stale-handshake waiver | Fastest path, zero-user, quality OK, exclusions present | Diagnose still `SUSPECT`; reservation enforcement must be proven | Primary short-term path |
| Fix diagnose semantics, then reserve WireGuard | Converts conditional target into clean target | Requires code/policy work before second canary | Best quality short-term path if time permits |
| Dedicated new test egress | Best long-term isolation and attribution | Requires provisioning and governance mutation blocks | Recommended durable path, not required before next packet |
| Occupied target `1` | Production-realistic | Not clean isolated target | Avoid for second canary |
| awg0/awg3 | Existing pool | Quality/readiness blockers | Not current path |
| OpenVPN | Existing zero-user target | SUSPECT and weaker/noisier status than WireGuard | Fallback only |

## Decision

```text
dedicated_test_egress_needed=false_for_next_packet
dedicated_test_egress_recommended=true_for_long_term
best_strategy=WIREGUARD_RESERVE_THEN_DIAGNOSE_FIX_OR_STALE_HANDSHAKE_WAIVER
recommended_next_block=E11.2_WIREGUARD_RESERVATION_AND_DIAGNOSE_SEMANTICS_APPROVAL_PACKET
```

WireGuard is enough to proceed to an approval packet. A dedicated test egress remains the cleanest durable strategy, but it is not required before preparing the next bounded approval block.
