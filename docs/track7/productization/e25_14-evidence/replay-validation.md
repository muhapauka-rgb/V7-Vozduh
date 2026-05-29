# E25.14 Replay Validation

## Result

`replay_rejection_verified=false`

`stale_packet_rejection_verified=true`

`runtime_mutation_performed=false`

## Explanation

The approved packet was never executed because final execution authorization failed before mutation.

Since no success record was written for the packet in E25.14, a true post-execution replay test could not be performed honestly.

However, the same packet is now denied before execution because its packet-bound `users.registry` hash no longer matches live runtime truth:

```text
packet_users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
current_users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
denial=users_registry_hash_mismatch
```

## Movement Safety

- no movement command executed;
- no routing mutation occurred;
- no denial runtime write was performed;
- denial is recorded in this evidence file and final report.

## Required Next Step

Regenerate the movement approval packet against the current registry hash, then repeat execution-time recheck. Only after a successful movement can a true replay rejection be verified against the used packet.
