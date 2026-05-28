# Multi-Operator Approval Audit Model

## Status

multi_operator_audit_model_defined=true
execution_allowed_now=false
implementation_mode=read_only_placeholder

## Model

The Stage 2 operator system now exposes a read-only model for future dual-operator approvals. It does not authenticate new actors, store approvals, or execute runtime actions.

Required future fields:

- approval_id
- operation_id
- approval_author
- approval_reviewer
- author_timestamp
- reviewer_timestamp
- approval_expiry_seconds
- approval_status
- generation_id
- selected_move_fingerprint
- selected_move_count
- runtime_snapshot_hash
- rollback_manifest_hash
- evidence_packet_hash

## Required Semantics

- Two independent acknowledgements are required before mutating execution can be designed.
- Approval expires automatically after a short window; Stage 2 default model is 900 seconds.
- Generation ID and selected-move fingerprint must match the read-only preview at execution time.
- Approval replay must be rejected after generation change, selected-move change, stale runtime truth, or rollback manifest change.
- Operator identity must come from the authenticated admin session, not from editable request body fields.

## Stage 2 Boundary

No approval execution exists in Stage 2. The model is rendered only inside the audit export/runbook preview so operators can see the future contract shape without gaining mutation controls.
