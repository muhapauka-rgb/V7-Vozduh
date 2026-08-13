# RESET-M6 Core Production Cutover

Status: `RESET_M6_COMPLETE`

## Conclusion

Certification identity `10.7.0.114` moved from `awg0` to `awg3` by the pure Routing Core decision and the existing single route writer. The exact one-use Reset Authority contract was consumed once. Registry assignment, policy rule, table default, effective route and target-bound TLS payload passed verification. Rollback remained available and was not triggered.

## Evidence basis

- deployed commit `48efc49e732272854ec30e1efc9ec94b70183cc9`; safe deploy, GitHub and Runtime alignment `PASS`;
- request `accauth_r1_5014e001543ac7c77d02a9e9`; contract `acc_68100fd931e738bd28ef3bb8`; consumption `accuse_e431e8ca95b48d903c04bb78`;
- operation `resetm6_0bcbd645b1aa28bf50134f2d`; Core decision fingerprint `542c64a44499436b9bfd9c7fdae558fb4a5132bc69bd3f920127f598163a264a`;
- existing `v7-user-switch` wrote table `1112` to `awg3`; scoped registry/rule/table/route-get verification returned `PASS`;
- payload receipt `cttarget_a34510bf2d9a006e76608cc0` proved interface binding, fresh DNS/socket, TLS/HTTP payload and expected public egress identity;
- bounded path: Core `0.234 ms`; decision-to-scoped-route verification `657.141 ms`; target payload `301.1 ms`; all below the `3 s` gate and `5 s` hard ceiling;
- complexity: one member row, one existing writer process, no legacy Planner initialization and no global planning scan.

## Owner and disposition

Decision owner: `admin_core/routing_core.py`. Authority/one-use owner: `admin_core/operator_execution.py`. Effect owner: existing `tools/runtime-support/v7-user-switch`. Verification owners: existing scoped verifier and `tools/v7-client-speed-api`. Legacy remains fallback; no owner boundary changed.

Disposition: certification-user production correctness, initial latency and bounded-complexity proof are `PASS`. A pre-consumption helper-signature failure changed no route; the contract remained unconsumed until the corrected deployed consumer succeeded.

## Residual and successor

Residual: prove at least 10k users and 50 egresses through semantic classes/buckets, generation binding and bounded commit, with prepared compatible warm-path `p95 < 1 s` and no hidden O(N) work.

Exact successor: `EXECUTE_RESET_M7_BOUNDED_COHORT_CONSTANT_TIME_AND_WARM_PATH_PROOF`.

Runtime effects: one certification identity moved `awg0 -> awg3`.

Production effects: bounded certification-only route and assignment update; verified.

Authority effects: exact one-use CANARY contract consumed; no Authority expansion.
