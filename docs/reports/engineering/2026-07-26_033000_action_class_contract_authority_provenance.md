# Engineering Report — provenance-bound Action Class Contract

Date: 2026-07-26

## Цель

Исключить путь, при котором `current_action_class_contract` в
`/etc/v7/policy.json` выглядит как техническая JSON-запись, а не как точное
независимое решение существующего Authority owner.

## Реализация

Расширен существующий owner `admin_core/operator_execution.py`; новый owner,
watcher, registry, queue, planner или Authority system не созданы.

- read-only reconciliation в `tools/v7-users-autoswitch` теперь формирует
  неперсистентный request `v7.current-action-class-contract-authority-request.v1`;
- request хешируется и содержит active Program, exact user, source/target,
  source generation (planner/source/snapshot/selected-move identities),
  incident generation, `max_users=1`, `max_concurrent_transactions=1`,
  verification, rollback/containment, cooldown, anti-flap и one-use law;
- только explicit existing-owner surface accepts exact
  `APPROVE_ONCE_AS_SCOPED` plus expected request id/hash and writes v2 contract;
- v2 contract carries `issuing_owner`, immutable Authority decision provenance,
  `issued_at`, short `expires_at`, contract hash, all bounded scope fields and
  `one_use_consumption=ISSUED`;
- the separate read-only reconciliation request expires after five minutes, so
  an Authority decision cannot issue a contract from an old snapshot;
- autoswitch validates that provenance before any Candidate/Packet/apply path;
  it additionally filters selection to the one exact user/source/target;
- immediately before a sole forward mutation, autoswitch calls the same
  existing owner to atomically record `ISSUED -> CONSUMED`. A later failure is
  not retried under the old decision.

## Safety boundary

This change does not issue a production contract, edit production policy,
create Candidate/Packet/lease, apply routing, move a user, change Authority,
or change Production Maturity. A future production issuance still requires a
fresh owner-backed reconciliation result and a separately exact Authority
decision for its emitted request id/hash.

## Verification

Focused unit coverage verifies successful exact issuance, issuer/provenance,
one-user/one-transaction scope, atomic one-use consumption and rejection of a
second consumption. Full local test, deployment, production caller and truth /
convergence results are recorded only after their respective commands finish.

## Reliability hardening — 2026-07-26

The same existing Authority owner was extended, without a new registry or
execution path:

- a v2 contract is rejected at consumption when its `expires_at` has passed;
- an advisory sidecar file lock serializes policy read -> validation -> atomic
  write, so concurrent autoswitch processes have exactly one successful
  `ISSUED -> CONSUMED` transition;
- the established append-only
  `/opt/v7/audit/operator-execution-audit.jsonl` now records exactly one
  `APPROVE_ONCE_AS_SCOPED` or `DECLINE` with request/hash, actor provenance,
  incident/source identities and pre-decision policy generation; consumption
  is recorded by the same owner;
- issuance rejects changed policy generation, incomplete incident identity,
  an Authority class above its policy ceiling, incomplete stop conditions, and
  incomplete verification/rollback/anti-flap contracts;
- the request binds the policy generation and Authority ceiling in addition to
  the prior source/snapshot/selected-move generation.

New focused tests prove expired-contract rejection, malformed incident and
Authority-ceiling rejection, one-and-only-one APPROVE/DECLINE audit record,
and two concurrent consumers producing exactly one `PASS` and one
`STOP_SAFE`. These are engineering safety properties only: they do not issue a
production contract or create L7/L8 evidence.

## Production caller repair

The first production read-only caller after deployment exposed an exact
producer defect: the freshly coherent planner legitimately had no
`operation.source_bundle_hash` while the Authority request required one. The
repair derives that identity from the same canonical Intelligence Snapshot
source hashes and binds the shadow move identity (user/source/target), not the
empty post-authority selected-move set. This preserves fail-closed behavior:
if those canonical identities are unavailable or change before consumption,
issuance or the one-use transition stops safely.

## Final production verification

The repaired production non-test caller returned
`ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY` with a fresh exact request:

- authority request: `accauth_r1_ede0f1fd7546a91c901a6615`;
- issuing owner: `admin_core/operator_execution.py`;
- exact scope: user `10.0.0.2`, `vless -> wireguard-1779454504-c43409`;
- source generation is fully populated and `issue_preflight.ready=true`;
- budget is exactly one user and one concurrent transaction;
- one-use owner is `tools/v7-users-autoswitch`.

The caller remained `POLICY_READ_ONLY_HANDOFF_WITH_EXISTING_SNAPSHOT_REFRESH`:
policy write, Authority grant, Candidate/Packet/lease, runtime apply, routing
mutation, rollback apply and user movement all remained absent. No production
contract was issued. The remaining legal terminal is the intended independent
Authority decision for this fresh request; it is not an engineering defect.

After deploy `e3393e872eaf58fa659b947b6448c1eb07af26a1`, full truth returned
`PASS/FULLY_ALIGNED`; convergence returned `PASS/ALIGNED` with local, GitHub and
production at that same commit.
