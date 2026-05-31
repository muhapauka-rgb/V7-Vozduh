# P1.3 Build Sequence

build_sequence_defined=true

## Exact Build Order

### 1. Storage Adapter

- Choose backend: SQLite preferred, JSONL acceptable with adapter.
- Create shared store helper pattern for P1 stores.
- Implement Evidence Store first.

### 2. Evidence APIs

- `GET /api/evidence`
- `GET /api/evidence/{id}`
- `GET /api/evidence/by-object/{type}/{id}`

### 3. Evidence UI

- EvidenceChip.
- EvidenceDrawer.
- EvidenceTimeline.
- Integrate into `Проверки`, `Логи`, `Главная`.

### 4. Proposal Store

- Create Proposal Store.
- Enforce `evidence_bundle_id` requirement.
- Persist lifecycle and timeline.

### 5. Proposal APIs

- `GET /api/proposals`
- `GET /api/proposals/{id}`
- `GET /api/proposals/by-object/{type}/{id}`

### 6. Proposal UI

- ProposalCard.
- ProposalStatus.
- ProposalDrawer.
- Integrate into `Главная`, `Пользователи`, `Каналы`, `Маршруты`.

### 7. Runtime Trust Store/API/UI

- Runtime Convergence Store.
- Runtime APIs.
- RuntimeTrustStatus.
- RuntimeTrustDrawer.
- DriftComponent.

### 8. Release Trust Store/API/UI

- Release Trust Store.
- Release APIs.
- ReleaseTrustStatus.
- ReleaseDrawer.
- RollbackAvailability.

### 9. Integration

- Wire evidence links across proposal/runtime/release.
- Show proposal blockers from runtime/release trust.
- Link release drawer to runtime drawer and evidence drawer.

### 10. Tests

- API contract tests.
- Store adapter tests.
- UI render smoke tests.
- No-mutation guard tests.
- Redaction tests.
- `git diff --check`.

## Build Sequence Verdict

Build begins with Evidence Foundation. Phase 1 is usable after Wave 3 and production-ready after Wave 4.
