# E16 E15 Integration Survey

## Purpose

E16 extends the E15 read-only operator surface with preview-only approval UX.
The survey confirms the safe integration path before implementation.

## E15 Integration Points

| Area | Finding | E16 decision |
|---|---|---|
| Read-only adapter | `admin_core/operator_observability.py` already builds the operator view model from files/evidence without shelling out or writing runtime state. | Extend this adapter with approval preview objects only. |
| Admin UI | `/admin-v2` is served from `admin/v7-admin-api`; the E15 `Оператор` tab already contains Runtime Overview, Target Pool, Operations History, Evidence Viewer, and Delayed Movement. | Add an Approval Center panel inside the existing tab. |
| API routing | Operator endpoints are authenticated `GET /api/operator/*` in `do_GET`; no operator POST namespace exists. | Add authenticated GET-only preview endpoints. |
| Styles | E15 uses existing dark tokens and compact cards. | Reuse the same operator card vocabulary and add compact disabled-action styling. |
| Tests | `tests/unit/test_operator_observability.py` covers conservative missing-data behavior and no POST operator routes. | Extend tests for preview-only contract shape, disabled actions, redaction, and UI markers. |
| Endpoint inventory | `tools/v7-admin-endpoint-inventory` freezes admin endpoint counts. | Regenerate after adding GET-only preview endpoints. |

## Files Touched

- `admin_core/operator_observability.py`
- `admin/v7-admin-api`
- `tests/unit/test_operator_observability.py`
- `tests/contracts/endpoint_inventory_test.py`
- `docs/track5/endpoint-inventory.json`
- `docs/track7/productization/e16-*`
- `BLOCK_E16_APPROVAL_CENTER_AND_SAFE_ACTION_UX_CONTRACT_IMPLEMENTATION_REPORT.md`

## Files Intentionally Not Touched

- runtime state under `/opt/v7`;
- users registry;
- egress registry;
- routing state;
- autoswitch runtime files;
- kill switch state;
- systemd units;
- Direct/RU or Trusted RU runtime state;
- proxy runtime state.

## Safe Integration Plan

1. Add `build_operator_approval_preview()` as a read-only view-model helper.
2. Include `approval_preview` in the existing operator overview payload.
3. Add GET-only endpoints:
   - `/api/operator/approval-preview`
   - `/api/operator/approval-contracts`
   - `/api/operator/rollback-preview`
4. Add Approval Center cards and disabled execution controls to the existing Operator tab.
5. Prove no POST or mutating operator namespace exists.

## Abort Criteria Review

- Admin structure identified: yes.
- Existing operator tab identified: yes.
- Safe read-only adapter path identified: yes.
- Runtime mutation required: no.
- POST endpoint required: no.
- Build/test commands inferred: yes.

## Integration Verdict

E16 can proceed as a preview-only productization extension. No runtime control
surface is required or allowed.

