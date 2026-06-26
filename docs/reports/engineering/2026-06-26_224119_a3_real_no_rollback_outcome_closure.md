# Engineering Report: A3 real no-rollback outcome closure

Status: CLOSED
Date: 2026-06-26T22:41:19+0700
Language: Russian

## Summary

A3 закрыт реальным production outcome. Одобренный пакет `pkt_preview_5c4bcfaa59d769ced6d6e5dc` был выполнен через существующих owners, один пользователь `10.7.0.17` был перемещен `vless -> awg3`, проверка прошла успешно, rollback не потребовался.

## Action Performed

- Создан execution lease для уже одобренного пакета.
- Записана restore-barrier clearance только для этого пакета.
- Выполнен guarded apply через существующий autoswitch owner.
- Выполнена немедленная verification.
- Outcome закрыт через существующий feedback/learning owner.
- Intelligence snapshots обновлены.
- Truth и convergence выполнены после closure.
- A3 отмечен как `DONE`; следующий backlog item: `A4`.

## Objective Observations

- Packet id: `pkt_preview_5c4bcfaa59d769ced6d6e5dc`.
- Preview operation id: `govdry_27823dc8d8acf421271345f5`.
- Runtime operation id: `runtime_autoswitch_c06b1bc2a4ed6b53706de763`.
- Decision id: `decision_preview_89f97b0be8b2ad54543542fd`.
- Selected move hash: `56fa62f34a169276aa56bcedbb7ad17a3d6731c92313a8833be3fad153dc6159`.
- User: `10.7.0.17`.
- Move: `vless -> awg3`.
- Apply result: `APPLIED`.
- Verification result: `PASS`; `verify_rc=0`.
- Rollback result: `NOT_ATTEMPTED`; rollback was not required.
- Outcome closure: `execfb_55e330784ad36b513d23e12a`.
- Learning record: `learn_0c3b5cdd250c64ac7d9b97e7`.
- Synthetic evidence: `false`.
- Runtime automation enabled: `false`.
- Authority expanded: `false`.

## Engineering Conclusions

A3 produced the required class-level no-rollback evidence for a governed candidate movement. The previously fixed approved-plan-lock and snapshot-gate path preserved the selected move into apply time. The outcome is real production evidence, not simulated evidence.

The next highest implementation leverage item is A4: representative outcome evidence for the first action class. A4 must use only real comparable outcomes. If the existing evidence is not representative enough, OMP must stop at `REAL_WORLD_LIMIT`.

## Why The System Made This Decision

The system considered the movement because the governed canary dry-run produced an exact packet with one bounded selected move. The operator approved that exact packet. Runtime then consumed the approved packet identity, preserved the selected move hash, wrote restore clearance, and applied only the approved movement.

## Why The Decision Was Safe

The action was bounded to one user, one source, one target, one selected move hash, one restore-barrier clearance, and one execution lease. Verification ran immediately. Rollback was available through the rollback manifest, but verification passed, so rollback was not executed.

## Why The Decision Was Useful

The outcome closes A3 with real no-rollback evidence. This advances rollback/no-rollback certification, learning, authority evolution evidence, and the first action-class promotion path without enabling runtime automation.

## Why Alternatives Were Not Chosen

No alternative target or user was selected because the approved packet bound the action to `10.7.0.17 vless -> awg3`. Runtime was not allowed to rerun planner, change target, change selected move hash, or execute any other packet.

## Impact

- Capability affected: Movement Protection, Rollback, Learning, Authority Evolution.
- Backlog affected: `A3` is `DONE`; `A4` is next.
- Product impact: one more real production outcome reduces reliance on packet-level theory and supports future action-class evidence.
- User impact: one user moved to `awg3`; verification passed.

## Capability Progress

Movement Protection remains `IN_PROGRESS`. A3 completion advances rollback/no-rollback evidence, but Movement Protection is not complete until the remaining criteria in OMP are satisfied.

## Backlog Progress

- Tier A: `3 / 6`.
- Overall actionable: `3 / 34`.
- Current highest priority: `A4`.

## Production Maturity

Production Maturity updated to `24.0%`.

## Canonical Knowledge

No new owner and no new truth source were created. Durable knowledge is captured in OMP, Current Program State, Production Maturity Model, and Implementation Backlog.

## Evidence

- Apply: `runtime_autoswitch_c06b1bc2a4ed6b53706de763`.
- Feedback store: `execfb_55e330784ad36b513d23e12a`.
- Learning store: `learn_0c3b5cdd250c64ac7d9b97e7`.
- Snapshot refresh: `PASS`; `snapshot_count=11`; `runtime_behavior_changed=false`; `users_moved=false` during refresh.
- Truth: `PASS`.
- Convergence: `PASS`; local/GitHub/production aligned on `86547ff1739d842cd6a75f24024a7fc2f75061cf`.

## Next Step

Continue OMP with `A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS`.

## Re-audit Rule

Do not re-audit A3 unless production evidence contradicts the closed no-rollback outcome, the apply/verification owners materially change, or the operator explicitly requests it.
