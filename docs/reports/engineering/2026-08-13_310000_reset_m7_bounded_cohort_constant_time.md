# RESET-M7 Bounded Cohort and Warm Path

Status: `RESET_M7_COMPLETE`

Conclusion: the existing Routing Core now prepares generation-bound semantic classes outside the hot path and validates one bounded class-to-target-bucket commit without loading members or requesting per-user writes.

Evidence basis:

- scale corpus: 10k, 20k and 50k users, 50 egress semantic classes;
- pure Core hot commit p95: `0.005458`, `0.005208`, `0.005083 ms`; observed max `0.020166 ms`; measured N-independence `PASS`;
- production-kernel non-hooked Polygon: 10,000 membership map entries, 50 class-to-mark buckets, 200 atomic one-class nft transactions; p95 `18.81383805 ms`, max `105.217022 ms`, hard ceiling `250 ms`;
- each kernel commit changed one class element in one atomic nft transaction; member scan, per-user serialization, audit expansion and registry rewrite were absent from the measured hot path;
- generation, projection fingerprint, membership fingerprint, target generation and capacity are exact fail-closed bindings;
- temporary Polygon table cleanup `PASS`; no traffic hook, Runtime route, assignment, user or Authority effect occurred;
- deployed Core commit `2d39a0ac81c83ec215684c69946f521ece520c9c`; safe deploy and convergence `PASS`.

Owner: existing `admin_core/routing_core.py` decision owner plus existing Linux nftables dataplane primitive. No new Runtime owner, Planner, registry or truth source was created.

Disposition: bounded cohort architecture, declared constant-time commit and prepared compatible warm path `p95 < 1 s` are `PASS`. Asynchronous O(N) preparation is explicit Engineering Plane work; it is not hidden in recovery.

Residual: promote the Core to primary production decision authority through M8 gates while retaining explicit legacy fallback and proving restart/crash, duplicate suppression, blast radius, capacity, observability and fallback restoration.

Exact successor: `EXECUTE_RESET_M8_CORE_PRIMARY_PRODUCTION_PROMOTION_WITH_SAFE_FALLBACK`.

Runtime effects: `NONE`. Production traffic effects: `NONE`. Authority effects: `NONE`.
