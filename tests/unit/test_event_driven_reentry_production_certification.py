from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools/v7_sync_lib.py"
CPS = ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
OMP = ROOT / "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_reentry_production", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class EventDrivenReentryProductionCertificationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        cls.omp = OMP.read_text(encoding="utf-8")

    def evidence(self, **overrides):
        evidence = {
            "production_deploy_completed": True,
            "external_platform_turn_occurred": True,
            "standard_continue_omp_invoked": True,
            "real_consumer_invoked": True,
            "duplicate_suppression_passed": True,
            "watchdog_recovery_passed": True,
            "truth_passed": True,
            "convergence_passed": True,
            "snapshot_equality_passed": True,
            "production_hashes_match": True,
            "forbidden_effects_absent": True,
            "pending_wake_id": "NONE",
            "active_lease": "NONE",
            "overlap_count": "0",
        }
        evidence.update(overrides)
        return evidence

    def status(self, **overrides):
        return self.lib.event_driven_external_reentry_completion_projection(
            self.evidence(**overrides)
        )["status"]

    def test_01_pending_before_deploy(self):
        self.assertEqual(
            self.status(production_deploy_completed=False),
            self.lib.EVENT_DRIVEN_REENTRY_DEPLOY_PENDING,
        )

    def test_02_complete_evidence_is_production_certified(self):
        self.assertEqual(
            self.status(),
            self.lib.EVENT_DRIVEN_REENTRY_PRODUCTION_CERTIFIED,
        )

    def test_03_missing_truth_blocks_terminal(self):
        self.assertEqual(
            self.status(truth_passed=False),
            self.lib.EVENT_DRIVEN_REENTRY_DEPLOY_PENDING,
        )

    def test_04_missing_convergence_blocks_terminal(self):
        self.assertEqual(
            self.status(convergence_passed=False),
            self.lib.EVENT_DRIVEN_REENTRY_DEPLOY_PENDING,
        )

    def test_05_snapshot_mismatch_blocks_terminal(self):
        self.assertEqual(
            self.status(snapshot_equality_passed=False),
            self.lib.EVENT_DRIVEN_REENTRY_DEPLOY_PENDING,
        )

    def test_06_pending_wake_or_active_lease_blocks_terminal(self):
        self.assertEqual(
            self.status(pending_wake_id="wake-1"),
            self.lib.EVENT_DRIVEN_REENTRY_DEPLOY_PENDING,
        )
        self.assertEqual(
            self.status(active_lease="lease-1"),
            self.lib.EVENT_DRIVEN_REENTRY_DEPLOY_PENDING,
        )

    def test_07_missing_real_consumer_blocks_terminal(self):
        self.assertEqual(
            self.status(real_consumer_invoked=False),
            self.lib.EVENT_DRIVEN_REENTRY_DEPLOY_PENDING,
        )

    def test_08_normalized_owner_and_current_cps_agree(self):
        evidence = self.lib._event_driven_external_reentry_completion_evidence(
            self.cps, root=ROOT
        )
        normalized = self.lib.normalized_cps_live_state(
            completion_evidence=evidence
        )
        self.assertEqual(
            normalized["event_driven_external_reentry_status"],
            self.lib.EVENT_DRIVEN_REENTRY_PRODUCTION_CERTIFIED,
        )
        result = self.lib.cps_live_state_consistency(
            self.cps, root=ROOT, omp_text=self.omp
        )
        self.assertEqual(result["final_verdict"], "PASS", result["errors"])

    def test_09_documentation_only_override_without_evidence_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.lib.cps_live_state_consistency(
                self.cps, root=Path(tmp), omp_text=self.omp
            )
        self.assertIn(
            "cps_normalized_field_divergence:EVENT_DRIVEN_EXTERNAL_REENTRY_STATUS",
            result["errors"],
        )

    def test_10_historical_report_does_not_override_current_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            historical = root / "docs/reports/engineering/historical.md"
            historical.parent.mkdir(parents=True)
            historical.write_text(
                "- Final verdict: `EVENT_DRIVEN_EXTERNAL_REENTRY_PRODUCTION_CERTIFIED`\n"
                "- Production truth: `FULLY_ALIGNED / PASS`.\n",
                encoding="utf-8",
            )
            evidence = self.lib._event_driven_external_reentry_completion_evidence(
                self.cps, root=root
            )
        self.assertEqual(
            self.lib.event_driven_external_reentry_completion_projection(evidence)["status"],
            self.lib.EVENT_DRIVEN_REENTRY_DEPLOY_PENDING,
        )


if __name__ == "__main__":
    unittest.main()
