# V7 Chuck2: live target-admission repair

## Scope

Live ordinary user `10.7.0.127` (Chuck2) was placed by the operator on
`vless`.  His required profile is `google`, `google_auth`, `instagram`, and
`telegram`.  VLESS then produced fresh required-service failures.  This report
records only the generic repair; Codex did not select a target, create an
incident, or move the user.

## Evidence before repair

- The existing health/Matrix path detected `OTHER_PROFILE_REQUIRED_SERVICE_FAILURE`
  for Chuck2 and invoked its normal consumer.
- The consumer stopped safely with `NO_COMPATIBLE_PREPARED_CLASS` /
  `NO_3S_TARGET_CAPACITY`, not with a route-writer or verification failure.
- `wireguard-1779454504-c43409` had fresh healthy evidence for all four
  required services and was the existing Planner's best service-compatible
  candidate.
- It was nevertheless classified `FAILOVER_FULL`: 44 ordinary assignments
  were present while the registry still carried `soft_limit=1 hard_limit=2`
  from an old certification overlay.  That row had no reservation owner, no
  reservation id, no expiry, and no production-assignment block, so it was not
  an active controlled-capacity contract.

## Repair

`tools/v7-users-autoswitch` now distinguishes an active exact
controlled-certification capacity overlay from a stale marker on an egress
already carrying ordinary production traffic.

Only the latter's tiny overlay is excluded from the existing dynamic capacity
calculation.  The repair does not edit registries or assignments.  Active
controlled reservations still require all of: exact reservation id, existing
reservation owner, future expiry, execution/canary reservation marker, and
production-assignment block; their explicit limits remain authoritative.

## Verification

Focused tests passed: 45 tests across service-aware admission, prepared-target
projection, and egress lifecycle safety.  New cases prove that a stale
certification overlay cannot strand an ordinary recovery, while a live exact
reservation remains hard-limited.

## Deployment and next observation

After safe deployment, the existing health caller must observe a fresh VLESS
required-service failure and autonomously carry the normal chain:

`health -> Matrix -> affected scope -> Authority -> Planner -> governed
execution -> S11`.

No result is credited until the Runtime itself performs that chain and records
the assignment and required-service verification.  The target remains chosen
only by the existing Planner.
