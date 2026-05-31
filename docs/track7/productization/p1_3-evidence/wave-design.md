# P1.3 Wave Design

implementation_waves_defined=true

## Wave 1 — Evidence Foundation Visible In Admin

### Scope

- Evidence Store adapter.
- Evidence read APIs.
- EvidenceChip.
- EvidenceDrawer.
- EvidenceTimeline.
- Initial seeded/read-only evidence from existing checks/logs/overview.

### Dependencies

- Current `admin/v7-admin-api`.
- Existing `/admin-v2` drawer and pill patterns.

### Operator Value

Operator can open proof from existing admin surfaces instead of reading raw logs.

### Admin Changes

- `Проверки`: check results open Evidence Drawer.
- `Логи`: log event drawer links evidence bundles.
- `Главная`: alert/status rows show EvidenceChip.

### Expected Outcome

Evidence becomes visible and inspectable. No proposal or trust logic required yet.

## Wave 2 — Proposal Visibility

### Scope

- Proposal Store adapter.
- Proposal read APIs.
- ProposalCard.
- ProposalStatus.
- ProposalDrawer.
- Evidence linkage requirement.

### Dependencies

- Wave 1 Evidence Store/API/UI.

### Operator Value

Operator can see what V7 recommends, why, and which evidence supports it.

### Admin Changes

- `Главная`: proposal cards in attention/next-action area.
- `Пользователи`: user rows and drawers show proposal status.
- `Каналы`: channel drawers show suitability/avoidance proposals.
- `Маршруты`: route preview/checks show proposal cards.

### Expected Outcome

Evidence-backed recommendations are visible, but still cannot execute.

## Wave 3 — Runtime And Release Trust Status

### Scope

- Runtime Convergence Store.
- Release Trust Store.
- Runtime/release read APIs.
- RuntimeTrustStatus.
- ReleaseTrustStatus.
- RuntimeTrustDrawer.
- ReleaseDrawer.
- RollbackAvailability.

### Dependencies

- Wave 1 Evidence links.
- Wave 2 optional for showing proposal blockers.

### Operator Value

Operator can answer whether the running system and release can be trusted before acting.

### Admin Changes

- `Главная`: runtime/release trust status strip.
- `Проверки`: runtime/release verification rows.
- `Безопасность`: release/rollback trust panel.

### Expected Outcome

Phase 1 becomes usable as a read-only operator trust layer.

## Wave 4 — Production Hardening

### Scope

- Search/filter for evidence and proposals.
- Retention and expiration jobs.
- Role-gated advanced details.
- Proposal expiration/supersession.
- Trust freshness/TTL enforcement.
- Closure records.

### Dependencies

- Waves 1-3.

### Operator Value

The system becomes maintainable for daily operations and audit, not just visible.

### Admin Changes

- Search/filter controls.
- Closure/expired states.
- Advanced details sections.
- Better blocker indicators.

### Expected Outcome

Phase 1 becomes production-ready.

## Wave Verdict

Wave 1 is the correct first build because it unlocks visible proof and supports every later wave.
