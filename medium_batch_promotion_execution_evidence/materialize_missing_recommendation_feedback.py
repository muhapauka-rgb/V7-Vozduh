#!/usr/bin/env python3
import json
from pathlib import Path


path = Path("/opt/v7/egress/state/proposals.jsonl")
path.parent.mkdir(parents=True, exist_ok=True)
existing = path.read_text(encoding="utf-8", errors="replace").splitlines() if path.exists() else []
existing_ids = set()
for line in existing:
    try:
        row = json.loads(line)
    except json.JSONDecodeError:
        continue
    feedback_id = str(row.get("feedback_id") or "")
    schema = str(row.get("schema_version") or "")
    if feedback_id and schema == "v7.execution-recommendation-feedback.v1":
        existing_ids.add(feedback_id)

records = [
    {
        "schema_version": "v7.execution-recommendation-feedback.v1",
        "feedback_id": "execfb_dfac3391a383f3f76793fea0",
        "user": "10.0.0.3",
        "source_channel": "awg3",
        "target_channel": "vless",
        "outcome_status": "success",
        "audit_reference": "runtime_autoswitch_b5063a475a06312ff23c90a7",
        "closure_reference": "VERIFIED_READY",
        "created_at": "2026-06-06T08:47:20.062944+00:00",
        "recommendation_hash": "fcbbb6b0bb355003c3cf794875a78d68ce4a52d05c0c1ecfa94c761b7ef35438",
        "delta": 1.0,
        "outcome": "success",
        "repair_reason": "missing_recommendation_feedback_record_for_medium_batch_authority_promotion",
        "repair_program": "PROGRAM_MEDIUM_BATCH_PROMOTION_IMPLEMENTATION_AND_REAL_5_USER_EXECUTION",
        "runtime_mutation_performed": False,
        "users_moved": 0,
    },
    {
        "schema_version": "v7.execution-recommendation-feedback.v1",
        "feedback_id": "execfb_e42729ab1d2fe5ffad827c56",
        "user": "10.0.0.6",
        "source_channel": "awg3",
        "target_channel": "vless",
        "outcome_status": "success",
        "audit_reference": "runtime_autoswitch_b5063a475a06312ff23c90a7",
        "closure_reference": "VERIFIED_READY",
        "created_at": "2026-06-06T08:47:41.232753+00:00",
        "recommendation_hash": "fcbbb6b0bb355003c3cf794875a78d68ce4a52d05c0c1ecfa94c761b7ef35438",
        "delta": 1.0,
        "outcome": "success",
        "repair_reason": "missing_recommendation_feedback_record_for_medium_batch_authority_promotion",
        "repair_program": "PROGRAM_MEDIUM_BATCH_PROMOTION_IMPLEMENTATION_AND_REAL_5_USER_EXECUTION",
        "runtime_mutation_performed": False,
        "users_moved": 0,
    },
]

added = []
with path.open("a", encoding="utf-8") as fh:
    for record in records:
        if record["feedback_id"] in existing_ids:
            continue
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        added.append(record["feedback_id"])

print(json.dumps({
    "schema_version": "v7.recommendation-feedback-repair.v1",
    "path": str(path),
    "requested_feedback_ids": [record["feedback_id"] for record in records],
    "added_feedback_ids": added,
    "already_present_ids": sorted(existing_ids.intersection(record["feedback_id"] for record in records)),
    "runtime_mutation_performed": False,
    "users_moved": 0,
}, ensure_ascii=False, indent=2))
