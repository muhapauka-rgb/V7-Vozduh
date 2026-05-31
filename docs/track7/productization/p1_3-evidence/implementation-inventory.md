# P1.3 Implementation Inventory

implementation_inventory_loaded=true

## Reviewed Inputs

Reviewed implementation plans:

- P1.1 Evidence + Proposal Implementation Planning;
- P1.2 Runtime Trust + Release Trust Implementation Planning.

## Stores

| Store | Purpose | Dependency |
| --- | --- | --- |
| Evidence Store | Bundle metadata, items, timeline, links, closure state. | Foundation for all proof surfaces. |
| Proposal Store | Evidence-backed recommendations, lifecycle, links, timeline. | Requires Evidence Store. |
| Runtime Convergence Store | Runtime trust snapshots, fingerprints, drift, verification history. | Links to Evidence Store and Release Trust. |
| Release Trust Store | Release summary, certification, lineage, rollback lineage, verification history. | Links to Evidence Store and Runtime Trust. |

## APIs

| API | Purpose |
| --- | --- |
| `GET /api/evidence` | List evidence bundles. |
| `GET /api/evidence/{id}` | Open full evidence drawer data. |
| `GET /api/evidence/by-object/{type}/{id}` | Show evidence in current object context. |
| `GET /api/proposals` | List proposals. |
| `GET /api/proposals/{id}` | Open full proposal drawer data. |
| `GET /api/proposals/by-object/{type}/{id}` | Show proposals in current object context. |
| `GET /api/runtime/convergence` | Current runtime trust summary. |
| `GET /api/runtime/fingerprint` | Runtime fingerprint summary. |
| `GET /api/runtime/drift` | Drift list/history. |
| `GET /api/release/current` | Current release trust summary. |
| `GET /api/release/history` | Release history/lineage list. |
| `GET /api/release/{id}` | Full release drawer data. |

## Drawers

- EvidenceDrawer;
- ProposalDrawer;
- RuntimeTrustDrawer;
- ReleaseDrawer.

## Components

- EvidenceChip;
- EvidenceSummary;
- EvidenceTimeline;
- ProposalCard;
- ProposalStatus;
- ProposalTimeline;
- RuntimeTrustStatus;
- DriftComponent;
- VerificationHistoryView;
- ReleaseTrustStatus;
- ReleaseHistory;
- RollbackAvailability.

## Admin Integrations

| Admin section | Planned visible additions |
| --- | --- |
| `Главная` | Evidence chips, proposal cards, runtime trust, release trust. |
| `Пользователи` | Evidence/proposal chips in user rows and drawer. |
| `Каналы` | Evidence/proposal chips in channel rows and drawer. |
| `Маршруты` | Proposal cards and evidence links in route checks/previews. |
| `Проверки` | Evidence drawer, runtime/release verification rows. |
| `Безопасность` | Runtime/release trust, rollback availability. |
| `Логи` | Evidence links from log event drawer. |

## Inventory Verdict

Inventory is loaded. The smallest useful build slice is Evidence Store/API/UI because every later surface needs evidence links.
