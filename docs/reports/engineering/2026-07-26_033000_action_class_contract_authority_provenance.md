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

## Production caller repair

The first production read-only caller after deployment exposed an exact
producer defect: the freshly coherent planner legitimately had no
`operation.source_bundle_hash` while the Authority request required one. The
repair derives that identity from the same canonical Intelligence Snapshot
source hashes and binds the shadow move identity (user/source/target), not the
empty post-authority selected-move set. This preserves fail-closed behavior:
if those canonical identities are unavailable or change before consumption,
issuance or the one-use transition stops safely.
