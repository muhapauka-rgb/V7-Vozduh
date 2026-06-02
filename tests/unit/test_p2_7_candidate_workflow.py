import importlib.machinery
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


def load_admin_api():
    loader = importlib.machinery.SourceFileLoader("v7_admin_api_p2_7", str(ADMIN_API))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class CandidateWorkflowBridgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_admin_api()

    def setUp(self):
        self.candidate = {
            "candidate_id": "cand_p2_7",
            "contract_draft_id": "draft_p2_7",
            "lifecycle_state": "READY_FOR_CONTRACT",
            "risk_state": "LOW",
            "proposal_references": ["prop_p2_7"],
            "evidence_references": ["ev_p2_7"],
            "authority_references": {"authority_state": "PREVIEW_ONLY"},
            "affected_users": ["10.7.0.11"],
            "target": "wireguard-target",
            "validation_state": "PASS",
            "simulation_state": "SIMULATION_READY",
            "readiness_state": "READY",
            "source_of_truth": "proposal_store_plus_draft_preview",
            "lineage": {"proposal_id": "prop_p2_7", "draft_id": "draft_p2_7"},
        }
        self.approval = {
            "schema_version": "e16.approval-preview.v1",
            "approval_status": {"state": "PREVIEW_ONLY"},
            "contracts": {"MovementApprovalPreview": {}, "GenerationClearancePreview": {}},
            "movement_preview": {"candidate_users": [{"user": "10.7.0.11", "to": "wireguard-target"}]},
            "generation_guard": {},
            "rollback_manifest": {},
            "blast_radius": {},
            "evidence_freshness": {},
            "disabled_actions": [{"label": "Execute", "disabled": True}],
        }
        self.governance = {
            "schema_version": "e19.execution-governance-preview.v1",
            "contracts": {"ExecutionIntent": {}, "ExecutionApproval": {}},
            "safe_action_status": {"state": "DISABLED_CONTRACT_ONLY"},
            "execution_boundary": {"allowed_users": ["10.7.0.11"], "allowed_targets": ["wireguard-target"]},
            "dual_confirmation": {"both_operators_required": True},
            "replay_protection": {"reject_on_stale_evidence": True},
            "blast_radius_enforcement": {},
            "execution_denial": {"denial_reasons": ["PREVIEW_ONLY"]},
            "disabled_actions": [{"label": "Execute", "disabled": True}],
        }
        self.rehearsal = {
            "schema_version": "e20.execution-rehearsal.v1",
            "rehearsal_only": True,
            "runtime_recheck_model": {},
            "rehearsal_matrix": [
                {"actual_rehearsal_verdict": "EXECUTION_ALLOWED"},
                {"actual_rehearsal_verdict": "REPLAY_REJECTED"},
            ],
            "rehearsal_timeline": [],
            "immutable_execution_audit": {},
            "productization_maturity": {},
        }

    def test_candidate_approval_detail_reuses_approval_center(self):
        m = self.m
        detail = m.p2_7_candidate_approval_detail(self.candidate, approval_preview=self.approval)
        self.assertEqual(detail["approval_center"]["approval_status"]["state"], "PREVIEW_ONLY")
        self.assertIn("MovementApprovalPreview", detail["lineage"]["candidate_to_approval_center"]["contracts_reused"])
        self.assertTrue(detail["read_only"])
        self.assertFalse(detail["parallel_systems_created"])
        self.assertFalse(detail["execution_allowed_now"])

    def test_candidate_governance_detail_reuses_governance_preview(self):
        m = self.m
        detail = m.p2_7_candidate_governance_detail(self.candidate, governance_preview=self.governance)
        self.assertEqual(detail["governance_preview"]["schema_version"], "e19.execution-governance-preview.v1")
        self.assertTrue(detail["lineage"]["candidate_to_governance_preview"]["no_duplicate_governance_workflow"])
        self.assertEqual(detail["authority_readiness"], "READY")
        self.assertFalse(detail["runtime_mutation_performed"])

    def test_candidate_rehearsal_detail_reuses_rehearsal_preview(self):
        m = self.m
        detail = m.p2_7_candidate_rehearsal_detail(self.candidate, rehearsal_preview=self.rehearsal)
        self.assertEqual(detail["rehearsal_preview"]["schema_version"], "e20.execution-rehearsal.v1")
        self.assertEqual(detail["dry_run_preparation"]["rehearsal_cases"], 2)
        self.assertEqual(detail["dry_run_preparation"]["denial_cases"], 1)
        self.assertFalse(detail["execution_engine_implemented"])

    def test_workflow_consistency_fails_closed_without_proposal(self):
        m = self.m
        candidate = dict(self.candidate)
        candidate["proposal_references"] = []
        approval = m.p2_7_candidate_approval_detail(candidate, approval_preview=self.approval)
        governance = m.p2_7_candidate_governance_detail(candidate, governance_preview=self.governance)
        rehearsal = m.p2_7_candidate_rehearsal_detail(candidate, rehearsal_preview=self.rehearsal)
        consistency = m.p2_7_workflow_consistency(candidate, approval, governance, rehearsal)
        self.assertEqual(consistency["status"], "FAIL_CLOSED")
        self.assertTrue(consistency["fail_closed"])


if __name__ == "__main__":
    unittest.main()
