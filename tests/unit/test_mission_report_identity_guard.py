import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from admin_core import operator_execution


class MissionReportIdentityGuardTest(unittest.TestCase):
    def test_exact_new_identity_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            mission = "MISSION_NEW"
            nonce = "NONCE_NEW"
            start = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
            report.write_text(f"Mission ID: `{mission}`\nRun Nonce: `{nonce}`\n", encoding="utf-8")
            result = operator_execution.mission_report_identity_guard(
                requested_mission_id=mission,
                requested_run_nonce=nonce,
                mission_start_timestamp=start,
                report_path=report,
                cps_text=f"CURRENT_MISSION_ID={mission}\nCURRENT_RUN_NONCE={nonce}",
            )
        self.assertTrue(result["ok"])

    def test_old_report_identity_nonce_and_cps_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            report.write_text("Mission ID: `MISSION_OLD`\nRun Nonce: `NONCE_OLD`\n", encoding="utf-8")
            start = datetime.now(timezone.utc).isoformat()
            old = datetime.now(timezone.utc).timestamp() - 60
            os.utime(report, (old, old))
            result = operator_execution.mission_report_identity_guard(
                requested_mission_id="MISSION_NEW",
                requested_run_nonce="NONCE_NEW",
                mission_start_timestamp=start,
                report_path=report,
                cps_text="CURRENT_MISSION_ID=MISSION_OLD\nCURRENT_RUN_NONCE=NONCE_OLD",
            )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "MISSION_CONTEXT_MISMATCH_STOP_SAFE")
        self.assertIn("report_mission_id_mismatch", result["errors"])
        self.assertIn("report_run_nonce_mismatch", result["errors"])
        self.assertIn("cps_mission_id_mismatch", result["errors"])

    def test_filename_similarity_cannot_override_header_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "MISSION_NEW_report.md"
            report.write_text("Mission ID: `MISSION_OLD`\nRun Nonce: `NONCE_NEW`\n", encoding="utf-8")
            result = operator_execution.mission_report_identity_guard(
                requested_mission_id="MISSION_NEW",
                requested_run_nonce="NONCE_NEW",
                mission_start_timestamp=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
                report_path=report,
                cps_text="MISSION_NEW NONCE_NEW",
            )
        self.assertFalse(result["ok"])
        self.assertIn("report_mission_id_mismatch", result["errors"])


if __name__ == "__main__":
    unittest.main()
