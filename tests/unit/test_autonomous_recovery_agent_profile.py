from __future__ import annotations

import copy
import contextlib
import io
import importlib.util
import importlib.machinery
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location(
        "v7_sync_lib_autonomous_recovery", ROOT / "tools/v7_sync_lib.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_script(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AutonomousRecoveryAgentProfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def test_compact_command_prepares_same_mission_native_handoff(self):
        packet = self.lib.autonomous_recovery_full_campaign_packet(root=ROOT)
        self.assertEqual(packet["final_verdict"], "CONTINUE_SAME_MISSION")
        self.assertEqual(packet["terminal"], "AUTONOMOUS_RECOVERY_NATIVE_ANALYST_REQUIRED")
        self.assertEqual(packet["command"], "AUTONOMOUS_RECOVERY FULL_CAMPAIGN")
        self.assertEqual(packet["execution_profile"]["final_verdict"], "PASS")
        self.assertEqual(packet["execution_profile"]["profile_type"], "AUTONOMOUS_RECOVERY")
        self.assertEqual(packet["role_order"], [
            "ANALYST", "CODEX_CRITICAL_EXECUTOR", "INDEPENDENT_REVIEWER",
        ])
        self.assertFalse(packet["repair_return_contract"]["user_relay_required"])
        self.assertTrue(packet["repair_return_contract"]["automatic_continuation_required"])

    def test_compact_bundle_enters_material_change_only_through_continue_omp(self):
        source = (ROOT / "tools/v7-autonomous-recovery-bundle").read_text(encoding="utf-8")
        self.assertIn("continue_omp_engineering_control_loop", source)
        self.assertNotIn("autonomous_recovery_qualifying_material_change_continuation(", source)

    def test_compact_campaign_exit_and_truth_check_consumption_are_terminal_only(self):
        bundle = load_script("v7_autonomous_recovery_bundle_exit_test", ROOT / "tools/v7-autonomous-recovery-bundle")
        self.assertEqual(bundle.full_campaign_exit_code({"final_verdict": "PASS"}), 0)
        self.assertEqual(bundle.full_campaign_exit_code({"final_verdict": "CONTINUE_SAME_MISSION"}), 2)
        self.assertEqual(bundle.full_campaign_exit_code({"final_verdict": "STOP_SAFE"}), 2)

        truth = load_script("v7_truth_check_autonomous_exit_test", ROOT / "tools/v7-truth-check")
        original_run = truth.subprocess.run
        try:
            truth.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
                returncode=0, stdout=json.dumps({"final_verdict": "PASS", "terminal": "SECTION8"}), stderr="",
            )
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(truth.main(["--json", "AUTONOMOUS_RECOVERY", "FULL_CAMPAIGN"]), 0)
            self.assertEqual(json.loads(stream.getvalue())["final_verdict"], "PASS")

            truth.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
                returncode=2, stdout=json.dumps({"final_verdict": "CONTINUE_SAME_MISSION"}), stderr="",
            )
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(truth.main(["--json", "AUTONOMOUS_RECOVERY", "FULL_CAMPAIGN"]), 2)
            self.assertEqual(json.loads(stream.getvalue())["final_verdict"], "STOP_SAFE")
        finally:
            truth.subprocess.run = original_run

    def test_native_context_envelope_is_complete_for_access_failure_and_strict_smoke_success(self):
        bundle = load_script("v7_autonomous_recovery_bundle_envelope_test", ROOT / "tools/v7-autonomous-recovery-bundle")
        original_run = bundle.subprocess.run
        packet = {"packet_fingerprint": "immutable-smoke-packet", "mission_id": "M", "authority": "READ_ONLY"}
        try:
            bundle.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
                returncode=7, stdout="", stderr="permission denied: configured runtime",
            )
            with self.assertRaises(bundle.NativeContextFailure) as failed:
                bundle.native_context("smoke_analyst", packet, 1, runner=bundle.subprocess.run)
            self.assertEqual(failed.exception.terminal, "STOP_SAFE_NATIVE_RUNTIME_ACCESS")
            envelope = failed.exception.envelope
            self.assertEqual(envelope["exit_code"], 7)
            self.assertFalse(envelope["timed_out"])
            self.assertTrue(envelope["stderr_fingerprint"])
            self.assertEqual(envelope["project_authority"], "READ_ONLY")

            def successful_run(command, **kwargs):
                output_path = Path(command[command.index("--output-last-message") + 1])
                message = json.dumps({
                    "verdict": "SMOKE_PASS", "scope": "READ_ONLY", "mutations": "NONE",
                    "packet_fingerprint": "immutable-smoke-packet",
                })
                output_path.write_text(message, encoding="utf-8")
                return SimpleNamespace(
                    returncode=0,
                    stdout="\n".join((
                        json.dumps({"type": "thread.started", "thread_id": "fresh-native-thread"}),
                        json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": message}}),
                    )), stderr="",
                )
            bundle.subprocess.run = successful_run
            context_id, result, envelope = bundle.native_context("smoke_analyst", packet, 1, runner=bundle.subprocess.run)
            self.assertEqual(context_id, "fresh-native-thread")
            self.assertEqual(result["verdict"], "SMOKE_PASS")
            self.assertTrue(envelope["thread_started"])
            self.assertTrue(envelope["final_agent_message_observed"])
            self.assertEqual(envelope["final_verdict"], "PASS")
            self.assertTrue(envelope["attempt_fingerprint"])
        finally:
            bundle.subprocess.run = original_run

    def test_outer_compact_truth_check_retains_bundle_attempt_and_budget_exceeds_composed_phases(self):
        bundle = load_script("v7_autonomous_recovery_bundle_budget_test", ROOT / "tools/v7-autonomous-recovery-bundle")
        truth = load_script("v7_truth_check_autonomous_envelope_test", ROOT / "tools/v7-truth-check")
        self.assertEqual(
            bundle.FULL_CAMPAIGN_TIMEOUT_SECONDS,
            bundle.ANALYST_TIMEOUT_SECONDS + bundle.EXECUTOR_TIMEOUT_SECONDS + bundle.REVIEWER_TIMEOUT_SECONDS
            + bundle.DOCKER_PHASE_TIMEOUT_SECONDS + bundle.OUTER_TIMEOUT_MARGIN_SECONDS,
        )
        self.assertGreater(truth.AUTONOMOUS_NATIVE_FULL_TIMEOUT_SECONDS, bundle.FULL_CAMPAIGN_TIMEOUT_SECONDS)
        original_run = truth.subprocess.run
        try:
            truth.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
                returncode=2,
                stdout=json.dumps({"final_verdict": "STOP_SAFE", "terminal": "STOP_SAFE_NATIVE_DISPATCH_TIMEOUT", "native_attempts": [{"role": "analyst"}]}),
                stderr="native analyst timeout",
            )
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(truth.main(["--json", "AUTONOMOUS_RECOVERY", "NATIVE_SMOKE"]), 2)
            result = json.loads(stream.getvalue())
            self.assertEqual(result["terminal"], "STOP_SAFE_NATIVE_DISPATCH_TIMEOUT")
            self.assertEqual(result["native_attempts"], [{"role": "analyst"}])
            self.assertEqual(result["native_bundle_attempt"]["exit_code"], 2)
            self.assertTrue(result["native_bundle_attempt"]["stderr_fingerprint"])
        finally:
            truth.subprocess.run = original_run

    def test_all_native_negative_event_streams_retain_inner_and_outer_envelopes(self):
        """Exercise adapter -> bundle JSON -> compact truth-check without live Codex."""
        bundle = load_script("v7_autonomous_recovery_bundle_negative_stream_test", ROOT / "tools/v7-autonomous-recovery-bundle")
        truth = load_script("v7_truth_check_autonomous_negative_stream_test", ROOT / "tools/v7-truth-check")
        lib = load_lib()
        terminals = {
            "access": "STOP_SAFE_NATIVE_RUNTIME_ACCESS",
            "timeout": "STOP_SAFE_NATIVE_DISPATCH_TIMEOUT",
            "no_thread": "STOP_SAFE_NATIVE_THREAD_START_MISSING",
            "no_message": "STOP_SAFE_NATIVE_FINAL_MESSAGE_MISSING",
            "malformed": "STOP_SAFE_NATIVE_OUTPUT_INVALID",
            "output_mismatch": "STOP_SAFE_NATIVE_OUTPUT_MISMATCH",
            "packet_mismatch": "STOP_SAFE_NATIVE_PACKET_FINGERPRINT_MISMATCH",
            "schema": "STOP_SAFE_NATIVE_OUTPUT_SCHEMA",
        }

        def native_runner(case):
            def run(command, **kwargs):
                output_path = Path(command[command.index("--output-last-message") + 1])
                schema_path = Path(command[command.index("--output-schema") + 1])
                expected_fingerprint = json.loads(schema_path.read_text(encoding="utf-8"))["properties"]["packet_fingerprint"]["const"]
                message = json.dumps({
                    "verdict": "SMOKE_PASS", "scope": "READ_ONLY", "mutations": "NONE",
                    "packet_fingerprint": expected_fingerprint,
                })
                if case == "timeout":
                    raise subprocess.TimeoutExpired(command, 1, output="partial-native-output", stderr="native deadline")
                if case == "access":
                    return SimpleNamespace(returncode=7, stdout="", stderr="permission denied")
                if case == "malformed":
                    message = "{"
                elif case == "packet_mismatch":
                    message = json.dumps({"verdict": "SMOKE_PASS", "scope": "READ_ONLY", "mutations": "NONE", "packet_fingerprint": "wrong"})
                elif case == "schema":
                    message = json.dumps({"verdict": "SMOKE_PASS", "scope": "READ_ONLY", "packet_fingerprint": expected_fingerprint})
                if case != "no_message":
                    output_path.write_text("different" if case == "output_mismatch" else message, encoding="utf-8")
                events = []
                if case != "no_thread":
                    events.append(json.dumps({"type": "thread.started", "thread_id": "controlled-thread"}))
                if case != "no_message":
                    events.append(json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": message}}))
                return SimpleNamespace(returncode=0, stdout="\n".join(events), stderr="")
            return run

        for case, terminal in terminals.items():
            inner = bundle.run_native_smoke(lib, runner=native_runner(case))
            self.assertEqual(inner["final_verdict"], "STOP_SAFE", case)
            self.assertEqual(inner["terminal"], terminal, case)
            inner_attempt = inner["native_attempts"][0]
            self.assertIn("stdout_fingerprint", inner_attempt, case)
            self.assertIn("stderr_fingerprint", inner_attempt, case)
            self.assertIn("exit_code", inner_attempt, case)
            self.assertIn("timed_out", inner_attempt, case)
            self.assertIn("thread_started", inner_attempt, case)
            self.assertIn("final_agent_message_observed", inner_attempt, case)

            def bundle_runner(command, **kwargs):
                return SimpleNamespace(
                    returncode=bundle.full_campaign_exit_code(inner),
                    stdout=json.dumps(inner), stderr="",
                )
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(
                    truth.main(["--json", "AUTONOMOUS_RECOVERY", "NATIVE_SMOKE"], native_bundle_runner=bundle_runner),
                    2, case,
                )
            outer = json.loads(stream.getvalue())
            self.assertEqual(outer["final_verdict"], "STOP_SAFE", case)
            self.assertEqual(outer["terminal"], terminal, case)
            self.assertEqual(outer["native_attempts"][0]["role"], "smoke_analyst", case)
            self.assertIn("native_bundle_attempt", outer, case)
            self.assertEqual(outer["native_bundle_attempt"]["exit_code"], 2, case)
            self.assertNotIn("section8_completion", outer, case)

    def test_profile_rejects_missing_independent_review(self):
        packet = self.lib.autonomous_recovery_full_campaign_packet(root=ROOT)
        profile = dict(packet["execution_profile"])
        profile.pop("profile_fingerprint", None)
        profile["required_reviews"] = ["ARCHITECTURE_REVIEW"]
        admitted = self.lib.admit_execution_profile_contract(
            profile, mission_id=profile["mission_id"],
        )
        self.assertEqual(admitted["final_verdict"], "STOP_SAFE")
        self.assertIn(
            "autonomous_recovery_requires_exact_independent_reviews",
            admitted["errors"],
        )

    def test_packet_is_read_only_and_keeps_product_frontier_unchanged(self):
        packet = self.lib.autonomous_recovery_full_campaign_packet(root=ROOT)
        self.assertEqual(packet["execution_profile"]["mutation_class"], "READ_ONLY")
        self.assertEqual(packet["runtime_impact"], "NONE")
        self.assertEqual(packet["production_impact"], "NONE")
        self.assertEqual(packet["authority_impact"], "NONE")
        required = packet["mission_intent"]["required_outcomes"]
        self.assertEqual(set(required), set(self.lib.AUTONOMOUS_RECOVERY_SECTION8_OUTCOMES))
        self.assertEqual(
            packet["execution_profile"]["mission_id"],
            packet["active_omp_mission_id"],
        )

    def _native_submission(self):
        packet = self.lib.autonomous_recovery_full_campaign_packet(root=ROOT)
        profile = packet["execution_profile"]
        manifest = {
            "schema": "v7.codex-native-context-manifest.v1",
            "roles": [
                {"role": "ANALYST", "native_agent_id": "ar-analyst-v1"},
                {"role": "CODEX_CRITICAL_EXECUTOR", "native_agent_id": "ar-codex-v1"},
            ],
        }
        output = {
            "mission_reference": profile["mission_id"],
            "profile_reference": profile["profile_fingerprint"],
            "input_fingerprint": profile["input_fingerprint"],
            "current_cps_frontier": packet["active_omp_mission_id"],
            "selected_obligation": "READ_ONLY_PROFILE_BINDING",
            "physical_onset_contract": "POLYGON_ONLY_PENDING_EXISTING_OWNER",
            "affected_scope_contract": "EXISTING_MATRIX_OWNER",
            "polygon_campaign_plan": "PENDING_EXISTING_OMP_OWNER",
            "causal_hypotheses": ["native artifact receipt must bind exact live Mission"],
            "recommended_existing_owner_change": "NONE_READ_ONLY_PROFILE_CONSUMPTION",
            "codex_critical_assessment": "replace competing Mission identity with the CPS Mission identity",
            "adaptation_required": True,
            "repair_return_packet": {},
            "remaining_outcomes": ["ACTIVE_RECOVERY_FRONTIER_REMAINS_EXISTING_OWNER_BOUND"],
            "owner_decision_required": False,
            "unproven_claims": ["repair/replay not yet consumed"],
            "seeded_defect_diagnosis": "existing equivalence consumer rejects the immutable member-binding mismatch before BDP/OMP repair and exact replay",
            "terminal_verdict": "CONTINUE_SAME_MISSION",
        }
        provisional = self.lib.gpt_decision_review_result_contract(
            profile, output, executor_context_id="ar-analyst-v1",
            native_context_manifest=manifest,
        )
        reviews = []
        for review_type in profile["required_reviews"]:
            reviews.append(self.lib.execution_profile_review_record(
                profile, provisional, review_type=review_type, review_verdict="PASS",
                review_context_id="ar-reviewer-v1",
                native_context_proof={
                    "role": "INDEPENDENT_REVIEWER", "native_agent_id": "ar-reviewer-v1",
                    "fork_turns": "none", "platform_dispatch": "spawn_agent",
                },
            ))
        adaptation = self.lib.autonomous_recovery_codex_adaptation(
            packet["mission_intent"], codex_executor_context_id="ar-codex-v1",
            discovered_fact="the initial packet attempted to create a competing Mission identity",
            original_proposed_method="bind a new autonomous Mission",
            adapted_method="bind the read-only profile to the exact current CPS Mission",
            continuation_action="EXISTING_OMP_OWNER_SELECTS_NEXT_LAWFUL_RECOVERY_OBLIGATION",
            evidence_references=["docs/programs/V7_CURRENT_PROGRAM_STATE.md"],
        )
        return packet, output, reviews, manifest, adaptation

    def _section8_fixture(self):
        packet = self.lib.autonomous_recovery_full_campaign_packet(root=ROOT)
        members = lambda scale: [{"member_identity": f"member-{scale}-{index}"} for index in range(scale)]
        physical = []
        for scale in (1_000, 10_000):
            onset = 1_000_000_000
            physical.append({
                "scale": scale, "receipt_identity": f"physical-{scale}",
                "physical_onset_phase": "PRE_MUTATION_DISPATCH", "fault_command_succeeded": True,
                "t_physical_failure_ns": onset, "last_required_service_s11_ns": onset + 2_000_000_000,
                "requested_members": scale, "completed_members": scale, "member_receipts": members(scale),
            })
        catalog = {
            "final_verdict": "PASS", "coverage": {"all": True},
            "equivalence_certification": {"final_verdict": "PASS", "engineering_certified_scopes": [1_000, 10_000]},
        }
        output = {
            "repair_return_packet": {
                "schema": "v7.autonomous-recovery-docker-repair-replay-cycle.v2",
                "final_verdict": "PASS",
                "origin": {"final_verdict": "STOP_SAFE"},
                "bdp_handoff": {"admission_decision": "MISSION_ACCEPTED"},
                "repair": {"final_verdict": "PASS", "isolated_recovery_receipts": physical},
                "replay": {"final_verdict": "PASS"},
                "repair_fault_catalog": catalog,
                "checks": {
                    "cleanup_and_replay_proven": True,
                    "origin_stopped_safe": True,
                    "omp_mission_executed": True,
                },
            },
            "material_change_continuation": {
                "final_verdict": "PASS", "no_user_relay": True, "receipt_fingerprint": "material-receipt",
            },
            "material_change_omp_consumption": {
                "trigger": "Continue OMP qualifying Autonomous Recovery material change",
                "real_caller": "continue_omp_engineering_control_loop", "transitions": [{"terminal": "PASS"}],
            },
            "distinct_member_seeded_repair": {
                "final_verdict": "PASS", "mission_executed": True,
                "seeded": {"final_verdict": "STOP_SAFE"}, "seed_cleanup": {"seeded_copy_discarded": True},
                "replay": {"final_verdict": "PASS"},
            },
                "seeded_defect_diagnosis": "native analyst diagnosed immutable distinct-member binding mismatch through existing BDP/OMP repair/replay",
        }
        output["engineering_evidence_contract"] = self.lib.autonomous_recovery_engineering_evidence_contract(
            packet, output, root=ROOT,
        )
        reviews = [
            {
                "review_verdict": "PASS", "review_context_id": "independent-review",
                "review_output_fingerprint": f"review-{index}",
                "engineering_evidence_fingerprint": output["engineering_evidence_contract"]["evidence_fingerprint"],
                "engineering_scope": "ISOLATED_POLYGON_ENGINEERING_ONLY",
            }
            for index in range(len(packet["execution_profile"]["required_reviews"]))
        ]
        adaptation = self.lib.autonomous_recovery_codex_adaptation(
            packet["mission_intent"], codex_executor_context_id="critical-executor",
            discovered_fact="existing OMP controls the continuation",
            original_proposed_method="direct helper", adapted_method="Continue OMP selected bounded runner",
            continuation_action="EXISTING_OMP_LAWFUL_TERMINAL_OR_SUCCESSOR_ALREADY_CONSUMED",
            evidence_references=["tools/v7_sync_lib.py"],
        )
        return packet, output, reviews, adaptation

    def test_reviewer_requires_current_owner_caller_consumer_evidence_and_scope_binding(self):
        packet, output, reviews, adaptation = self._section8_fixture()
        contract = self.lib.autonomous_recovery_engineering_evidence_contract(packet, output, root=ROOT)
        self.assertEqual(contract["final_verdict"], "PASS")
        self.assertEqual(contract["scope"], "ISOLATED_POLYGON_ENGINEERING_ONLY")
        self.assertEqual(contract["forbidden_claims"], [
            "RUNTIME_EFFECT", "PRODUCTION_EFFECT", "USER_EFFECT", "SECTION8_CLOSURE",
        ])

        missing_consumer = copy.deepcopy(output)
        missing_consumer["material_change_omp_consumption"]["real_caller"] = "DOCUMENTED_ONLY_NO_CURRENT_CONSUMER"
        rejected = self.lib.autonomous_recovery_engineering_evidence_contract(packet, missing_consumer, root=ROOT)
        self.assertEqual(rejected["final_verdict"], "STOP_SAFE")

        wrong_evidence_reviews = copy.deepcopy(reviews)
        wrong_evidence_reviews[0]["engineering_evidence_fingerprint"] = "tampered"
        bound = self.lib.autonomous_recovery_section8_completion_binding(
            packet=packet, output=output, reviews=wrong_evidence_reviews,
            codex_adaptation=adaptation, root=ROOT,
        )
        self.assertEqual(bound["final_verdict"], "STOP_SAFE")
        self.assertIn("NATIVE_ANALYST_CRITICAL_EXECUTOR_AND_INDEPENDENT_REVIEW_CONSUMED", bound["errors"])

        wrong_scope_reviews = copy.deepcopy(reviews)
        wrong_scope_reviews[0]["engineering_scope"] = "RUNTIME_EFFECT"
        bound = self.lib.autonomous_recovery_section8_completion_binding(
            packet=packet, output=output, reviews=wrong_scope_reviews,
            codex_adaptation=adaptation, root=ROOT,
        )
        self.assertEqual(bound["final_verdict"], "STOP_SAFE")
        self.assertIn("NATIVE_ANALYST_CRITICAL_EXECUTOR_AND_INDEPENDENT_REVIEW_CONSUMED", bound["errors"])

    def test_campaign_evidence_is_bounded_redacted_and_idempotent(self):
        packet, output, reviews, adaptation = self._section8_fixture()
        section8 = self.lib.autonomous_recovery_section8_completion_binding(
            packet=packet, output=output, reviews=reviews, codex_adaptation=adaptation, root=ROOT,
        )
        result = {
            "final_verdict": "STOP_SAFE", "terminal": "STOP_SAFE_AUTONOMOUS_RECOVERY_ARTIFACT_CONSUMPTION",
            "errors": ["previous_reviewer_lacked_current_owner_consumer_evidence"],
            "section8_completion": section8,
            "provenance_level": "ORCHESTRATOR_OBSERVED_NOT_CRYPTOGRAPHIC",
        }
        attempts = [{
            "role": "reviewer", "thread_id": "controlled-reviewer", "thread_started": True,
            "final_agent_message_observed": True, "stdout_excerpt": "must-not-persist",
            "stderr_excerpt": "must-not-persist", "stdout_fingerprint": "stdout-fp",
            "stderr_fingerprint": "stderr-fp", "attempt_fingerprint": "attempt-fp",
        }]
        with tempfile.TemporaryDirectory() as temporary:
            first = self.lib.persist_autonomous_recovery_campaign_evidence(
                packet=packet, output=output, result=result, native_attempts=attempts,
                reviews=reviews, root=Path(temporary),
            )
            self.assertEqual(first["final_verdict"], "PASS")
            artifact = Path(first["artifact_path"])
            content = artifact.read_text(encoding="utf-8")
            self.assertNotIn("must-not-persist", content)
            self.assertIn("ISOLATED_POLYGON_ENGINEERING_ONLY", content)
            second = self.lib.persist_autonomous_recovery_campaign_evidence(
                packet=packet, output=output, result=result, native_attempts=attempts,
                reviews=reviews, root=Path(temporary),
            )
            self.assertEqual(second["final_verdict"], "PASS")
            self.assertEqual(second["artifact_fingerprint"], first["artifact_fingerprint"])

    def test_section8_binding_requires_every_outcome_and_rejects_each_tamper(self):
        packet, output, reviews, adaptation = self._section8_fixture()
        baseline = self.lib.autonomous_recovery_section8_completion_binding(
            packet=packet, output=output, reviews=reviews, codex_adaptation=adaptation, root=ROOT,
        )
        self.assertEqual(baseline["final_verdict"], "PASS", baseline["errors"])
        tamper = {
            "PERSISTENT_COMPACT_CONTRACT_LOADED": lambda p, o, r: p.update({"command": "wrong"}),
            "EXACT_LAWFUL_OBLIGATION_SELECTED": lambda p, o, r: p["execution_profile"].update({"mission_id": "wrong"}),
            "MULTI_FAULT_ISOLATED_POLYGON_CAMPAIGN_CONSUMED": lambda p, o, r: o["repair_return_packet"].update({"final_verdict": "STOP_SAFE"}),
            "NATIVE_ANALYST_CRITICAL_EXECUTOR_AND_INDEPENDENT_REVIEW_CONSUMED": lambda p, o, r: r[0].update({"review_verdict": "FAIL_WITH_EXACT_INVARIANT"}),
            "NONTRIVIAL_SEEDED_DEFECT_REPAIRED_BY_EXISTING_OWNER": lambda p, o, r: o["distinct_member_seeded_repair"].update({"final_verdict": "STOP_SAFE"}),
            "ORIGIN_EXPERIMENT_AUTOMATIC_REPLAY_PASSED": lambda p, o, r: o["distinct_member_seeded_repair"]["replay"].update({"final_verdict": "STOP_SAFE"}),
            "PHYSICAL_ONSET_TO_LAST_REQUIRED_S11_WITHIN_SEVEN_SECONDS": lambda p, o, r: o["repair_return_packet"]["repair"]["isolated_recovery_receipts"][0].update({"completed_members": 999}),
            "SCALE_AND_CAPACITY_LAW_OWNER_CONSUMED": lambda p, o, r: o["repair_return_packet"]["repair_fault_catalog"]["equivalence_certification"].update({"engineering_certified_scopes": [1_000]}),
            "NO_UNEXPLAINED_MANUAL_RELAY": lambda p, o, r: o["material_change_continuation"].update({"no_user_relay": False}),
            "OWNER_CONSUMED_PROJECTION_OR_LAWFUL_TERMINAL_WITH_SUCCESSOR": lambda p, o, r: o["material_change_omp_consumption"].update({"transitions": []}),
        }
        for outcome, alter in tamper.items():
            candidate_packet, candidate_output, candidate_reviews = copy.deepcopy((packet, output, reviews))
            alter(candidate_packet, candidate_output, candidate_reviews)
            checked = self.lib.autonomous_recovery_section8_completion_binding(
                packet=candidate_packet, output=candidate_output, reviews=candidate_reviews,
                codex_adaptation=adaptation, root=ROOT,
            )
            self.assertEqual(checked["final_verdict"], "STOP_SAFE", outcome)
            self.assertIn(outcome, checked["errors"])

    def test_native_artifact_chain_is_interim_not_section8_completion(self):
        packet, output, reviews, manifest, adaptation = self._native_submission()
        result = self.lib.submit_autonomous_recovery_result(
            packet=packet, output=output, reviews=reviews,
            native_context_manifest=manifest, codex_adaptation=adaptation, root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertTrue(result["native_context_separation_proven"])
        self.assertEqual(
            result["interim_completion"]["mission_integrity_binding"]["terminal_class"],
            "CONTINUE_SAME_MISSION",
        )
        profile_errors = result["interim_completion"]["execution_profile_binding"]["errors"]
        self.assertIn("autonomous_recovery_engineering_evidence_missing_or_invalid", profile_errors)
        self.assertIn(
            "NATIVE_ANALYST_CRITICAL_EXECUTOR_AND_INDEPENDENT_REVIEW_CONSUMED",
            result["section8_completion"]["errors"],
        )
        self.assertIn(
            "PHYSICAL_ONSET_TO_LAST_REQUIRED_S11_WITHIN_SEVEN_SECONDS",
            result["section8_completion"]["errors"],
        )

    def test_reviewer_schema_requires_bound_evidence_fingerprint_and_engineering_scope(self):
        bundle = load_script("v7_autonomous_recovery_reviewer_schema_test", ROOT / "tools/v7-autonomous-recovery-bundle")
        schema, required = bundle.schema_for("reviewer", "evidence-contract-fingerprint")
        self.assertEqual(schema["properties"]["scope_verdict"]["enum"], [
            "ISOLATED_POLYGON_ENGINEERING_ONLY", "FAIL_WITH_EXACT_INVARIANT",
        ])
        valid = {
            "verdict": "PASS",
            "sections": {key: "PASS" for key in (
                "ARCHITECTURE_REVIEW", "SAFETY_REGRESSION_REVIEW",
                "EVIDENCE_REVIEW", "MISSION_INTEGRITY_REVIEW",
            )},
            "rejected_candidate_ids": [], "rejection_reasons": [],
            "evidence_fingerprint": "evidence-contract-fingerprint",
            "scope_verdict": "ISOLATED_POLYGON_ENGINEERING_ONLY",
        }
        self.assertEqual(bundle.validate_native_result("reviewer", valid, "packet-fingerprint", required), "")
        missing = dict(valid); missing.pop("evidence_fingerprint")
        self.assertEqual(
            bundle.validate_native_result("reviewer", missing, "packet-fingerprint", required),
            "STOP_SAFE_NATIVE_OUTPUT_SCHEMA",
        )
        wrong_scope = dict(valid); wrong_scope["scope_verdict"] = "RUNTIME_EFFECT"
        self.assertEqual(
            bundle.validate_native_result("reviewer", wrong_scope, "packet-fingerprint", required),
            "STOP_SAFE_NATIVE_OUTPUT_SCHEMA",
        )

    def test_native_artifact_chain_rejects_colliding_reviewer_context(self):
        packet, output, reviews, manifest, adaptation = self._native_submission()
        for review in reviews:
            review["review_context_id"] = "ar-analyst-v1"
            review["native_context_proof"]["native_agent_id"] = "ar-analyst-v1"
            review["review_output_fingerprint"] = self.lib._execution_contract_fingerprint({
                key: value for key, value in review.items()
                if key != "review_output_fingerprint"
            })
        result = self.lib.submit_autonomous_recovery_result(
            packet=packet, output=output, reviews=reviews,
            native_context_manifest=manifest, codex_adaptation=adaptation, root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        errors = result["interim_completion"]["execution_profile_binding"]["errors"]
        self.assertIn("execution_profile_review_context_not_separate:ARCHITECTURE_REVIEW", errors)

    def test_repair_ready_artifact_requires_validated_existing_owner_receipts(self):
        packet, output, reviews, manifest, adaptation = self._native_submission()
        output["terminal_verdict"] = "PASS_EXPERIMENT_REPLAY_READY"
        output["repair_return_packet"] = self.lib.certify_permanent_polygon_repair_return_cycle(root=ROOT)
        provisional = self.lib.gpt_decision_review_result_contract(
            packet["execution_profile"], output, executor_context_id="ar-analyst-v1",
            native_context_manifest=manifest,
        )
        for review in reviews:
            review["submitted_output_fingerprint"] = provisional["output_fingerprint"]
            review["review_output_fingerprint"] = self.lib._execution_contract_fingerprint({
                key: value for key, value in review.items()
                if key != "review_output_fingerprint"
            })
        result = self.lib.submit_autonomous_recovery_result(
            packet=packet, output=output, reviews=reviews,
            native_context_manifest=manifest, codex_adaptation=adaptation, root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertTrue(result["native_context_separation_proven"])


if __name__ == "__main__":
    unittest.main()
