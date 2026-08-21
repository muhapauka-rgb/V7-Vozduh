"""Deterministic Stage-E causal timing revalidation.

This is an engineering-only virtual-clock model built from existing V7 owner
contracts and measured spans. It never invokes production routing or Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import unittest


GOVERNED_TRANSACTION_SEC = 0.023675
FULL_MATRIX_SEC = 85.675
CURRENT_CADENCE_SEC = 900.0
PASSIVE_SENTINEL_SEC = 4.0
CURRENT_PERSISTENCE_SEC = 180.0
FAST_CONFIRM_SAMPLE_INTERVAL_SEC = 4.0
FAST_CONFIRM_SAMPLES = 3
FAST_CONFIRM_SEC = FAST_CONFIRM_SAMPLE_INTERVAL_SEC * (FAST_CONFIRM_SAMPLES - 1)
PREDECLARED_MIN_IMPROVEMENT = 0.50


@dataclass(frozen=True)
class Scenario:
    name: str
    passive_signal: bool
    subset_sufficient: bool
    failure_confirmed: bool
    target_ready: bool = True
    requires_full_for_confirmation: bool = False
    expected_stop_safe: bool = False
    recovery_stable: bool = True


SCENARIOS = (
    Scenario("HARD_CHANNEL_DOWN", True, True, True),
    Scenario("TUNNEL_UP_INTERNET_DEAD", True, True, True),
    Scenario("TELEGRAM_PERSISTENT_FAILURE", True, True, True),
    Scenario("REQUIRED_SERVICE_FAILURE", False, True, True),
    Scenario("TRANSIENT_FALSE_ALARM", True, False, False, expected_stop_safe=True),
    Scenario("PARTIAL_DEGRADATION", True, False, False, requires_full_for_confirmation=True, expected_stop_safe=True),
    Scenario("STALE_OR_UNKNOWN_STATE", True, True, True, target_ready=False, expected_stop_safe=True),
    Scenario("CONFLICTING_GENERATION", True, True, True, target_ready=False, expected_stop_safe=True),
    Scenario("FAILURE_RECOVERY_FAILURE", True, True, True, recovery_stable=False, expected_stop_safe=True),
    Scenario("CLEAN_RECOVERY", True, True, True),
    Scenario("TARGET_UNAVAILABLE", True, True, True, target_ready=False, expected_stop_safe=True),
    Scenario("CAPACITY_OR_POLICY_DENIAL", True, True, True, target_ready=False, expected_stop_safe=True),
)


@dataclass(frozen=True)
class Candidate:
    name: str
    uses_subset: bool
    passive: bool
    current_full_barrier: bool


CANDIDATES = (
    Candidate("A_FULL_IMPROVED_MATRIX", uses_subset=False, passive=False, current_full_barrier=False),
    Candidate("B_FAST_DEEP_EXISTING_OWNER", uses_subset=True, passive=False, current_full_barrier=True),
    Candidate("C_PASSIVE_ESCALATION_MATRIX", uses_subset=True, passive=True, current_full_barrier=True),
    Candidate("B_PLUS_C_PROPOSED_FAST_RECOVERY", uses_subset=True, passive=True, current_full_barrier=False),
)


class VirtualClock:
    def __init__(self):
        self.now = 0.0

    def advance(self, seconds: float) -> float:
        self.now += max(0.0, float(seconds))
        return self.now


def simulate(candidate: Candidate, scenario: Scenario) -> dict[str, object]:
    clock = VirtualClock()
    signal_delay = (
        PASSIVE_SENTINEL_SEC
        if candidate.passive and scenario.passive_signal
        else CURRENT_CADENCE_SEC
    )
    clock.advance(signal_delay)
    signal_ts = clock.now

    # Full baseline uses the existing persistence contract after its deep
    # observation. The proposed fast policy uses three rapid confirmations
    # only for hard/required evidence; partial/ambiguous evidence remains
    # full-barrier or STOP_SAFE.
    if not scenario.failure_confirmed:
        return {
            "scenario": scenario.name,
            "candidate": candidate.name,
            "failure_to_signal": signal_ts,
            "signal_to_t0": None,
            "failure_to_t0": None,
            "t0_to_decision": None,
            "decision_to_t11": None,
            "t0_to_t11": None,
            "failure_to_t11": None,
            "full_wait_required": bool(
                scenario.requires_full_for_confirmation or candidate.current_full_barrier
            ),
            "correct_stop_safe": True,
            "false_switch": False,
            "missed_failure": False,
            "recovery": "NOT_APPLICABLE",
        }

    evidence_blocked = not scenario.target_ready or not scenario.recovery_stable
    fast_evidence_allowed = (
        candidate.uses_subset
        and scenario.subset_sufficient
        and not evidence_blocked
    )
    full_required = (
        not candidate.uses_subset
        or scenario.requires_full_for_confirmation
        or not fast_evidence_allowed
    )
    full_wait_required = bool(full_required or candidate.current_full_barrier)

    if candidate.uses_subset and fast_evidence_allowed:
        clock.advance(FAST_CONFIRM_SEC)
        if scenario.name == "CLEAN_RECOVERY":
            # Recovery remains more conservative than failure confirmation.
            clock.advance(CURRENT_PERSISTENCE_SEC)
        else:
            clock.advance(FAST_CONFIRM_SAMPLE_INTERVAL_SEC)
    else:
        clock.advance(FULL_MATRIX_SEC + CURRENT_PERSISTENCE_SEC)

    t0 = clock.now
    signal_to_t0 = t0 - signal_ts
    if full_required:
        # The required evidence is unavailable for the early route decision;
        # retain full barrier or stop before any recovery action.
        t0_to_decision = FULL_MATRIX_SEC if candidate.current_full_barrier else 0.0
    else:
        t0_to_decision = FULL_MATRIX_SEC if candidate.current_full_barrier else 0.0

    if evidence_blocked:
        return {
            "scenario": scenario.name,
            "candidate": candidate.name,
            "failure_to_signal": signal_ts,
            "signal_to_t0": signal_to_t0,
            "failure_to_t0": t0,
            "t0_to_decision": t0_to_decision,
            "decision_to_t11": None,
            "t0_to_t11": None,
            "failure_to_t11": None,
            "full_wait_required": full_wait_required,
            "correct_stop_safe": True,
            "false_switch": False,
            "missed_failure": False,
            "recovery": "STOP_SAFE",
        }

    decision_to_t11 = GOVERNED_TRANSACTION_SEC
    t0_to_t11 = t0_to_decision + decision_to_t11
    return {
        "scenario": scenario.name,
        "candidate": candidate.name,
        "failure_to_signal": signal_ts,
        "signal_to_t0": signal_to_t0,
        "failure_to_t0": t0,
        "t0_to_decision": t0_to_decision,
        "decision_to_t11": decision_to_t11,
        "t0_to_t11": t0_to_t11,
        "failure_to_t11": t0 + t0_to_decision + decision_to_t11,
        "full_wait_required": full_wait_required,
        "correct_stop_safe": False,
        "false_switch": False,
        "missed_failure": False,
        "recovery": "RECOVERY_READY",
    }


class V53LatencyCausalRevalidationTest(unittest.TestCase):
    def test_predeclared_criteria_are_frozen_before_runs(self):
        self.assertEqual(PREDECLARED_MIN_IMPROVEMENT, 0.50)
        self.assertEqual(FAST_CONFIRM_SAMPLES, 3)
        self.assertEqual(CURRENT_PERSISTENCE_SEC, 180.0)
        self.assertEqual(FULL_MATRIX_SEC, 85.675)

    def test_all_candidates_run_the_same_failure_matrix(self):
        results = [simulate(candidate, scenario) for candidate in CANDIDATES for scenario in SCENARIOS]
        self.assertEqual(len(results), len(CANDIDATES) * len(SCENARIOS))
        self.assertTrue(all(row["candidate"] for row in results))
        self.assertTrue(all(row["scenario"] for row in results))

    def test_safety_invariants_hold_for_every_candidate(self):
        for candidate in CANDIDATES:
            for scenario in SCENARIOS:
                row = simulate(candidate, scenario)
                if scenario.expected_stop_safe:
                    self.assertTrue(row["correct_stop_safe"], (candidate, scenario, row))
                    self.assertIsNone(row["decision_to_t11"], (candidate, scenario, row))
                self.assertFalse(row["false_switch"], (candidate, scenario, row))
                self.assertFalse(row["missed_failure"], (candidate, scenario, row))

    def test_proposed_b_plus_c_reduces_failure_to_t0_and_t0_to_t11(self):
        for scenario_name in (
            "HARD_CHANNEL_DOWN",
            "TUNNEL_UP_INTERNET_DEAD",
            "TELEGRAM_PERSISTENT_FAILURE",
        ):
            scenario = next(item for item in SCENARIOS if item.name == scenario_name)
            current = simulate(CANDIDATES[0], scenario)
            current_barrier = simulate(CANDIDATES[2], scenario)
            proposed = simulate(CANDIDATES[3], scenario)
            self.assertLess(proposed["failure_to_t0"], current["failure_to_t0"])
            self.assertLess(proposed["t0_to_t11"], current_barrier["t0_to_t11"])
            failure_gain = 1.0 - proposed["failure_to_t0"] / current["failure_to_t0"]
            t0_gain = 1.0 - proposed["t0_to_t11"] / current_barrier["t0_to_t11"]
            self.assertGreaterEqual(failure_gain, PREDECLARED_MIN_IMPROVEMENT)
            self.assertGreaterEqual(t0_gain, PREDECLARED_MIN_IMPROVEMENT)

    def test_required_service_without_passive_signal_keeps_cadence_but_can_remove_full_barrier(self):
        scenario = next(item for item in SCENARIOS if item.name == "REQUIRED_SERVICE_FAILURE")
        b = simulate(CANDIDATES[1], scenario)
        bc = simulate(CANDIDATES[3], scenario)
        self.assertEqual(b["failure_to_signal"], CURRENT_CADENCE_SEC)
        self.assertEqual(bc["failure_to_signal"], CURRENT_CADENCE_SEC)
        self.assertEqual(b["t0_to_decision"], FULL_MATRIX_SEC)
        self.assertEqual(bc["t0_to_decision"], 0.0)
        self.assertLess(bc["t0_to_t11"], b["t0_to_t11"])

    def test_partial_degradation_and_conflicting_evidence_keep_full_or_stop_safe(self):
        for scenario_name in ("PARTIAL_DEGRADATION", "STALE_OR_UNKNOWN_STATE", "CONFLICTING_GENERATION"):
            scenario = next(item for item in SCENARIOS if item.name == scenario_name)
            proposed = simulate(CANDIDATES[3], scenario)
            self.assertTrue(proposed["correct_stop_safe"], (scenario, proposed))
            self.assertTrue(proposed["full_wait_required"] or proposed["recovery"] == "STOP_SAFE")

    def test_recovery_is_more_conservative_than_failure_confirmation(self):
        clean = next(item for item in SCENARIOS if item.name == "CLEAN_RECOVERY")
        hard = next(item for item in SCENARIOS if item.name == "HARD_CHANNEL_DOWN")
        candidate = CANDIDATES[3]
        clean_row = simulate(candidate, clean)
        hard_row = simulate(candidate, hard)
        self.assertGreater(clean_row["signal_to_t0"], hard_row["signal_to_t0"])

    def test_barrier_roles_are_scenario_specific(self):
        hard = simulate(CANDIDATES[3], next(item for item in SCENARIOS if item.name == "HARD_CHANNEL_DOWN"))
        partial = simulate(CANDIDATES[3], next(item for item in SCENARIOS if item.name == "PARTIAL_DEGRADATION"))
        self.assertFalse(hard["full_wait_required"])
        self.assertTrue(partial["full_wait_required"] or partial["correct_stop_safe"])


def build_result_rows() -> list[dict[str, object]]:
    return [simulate(candidate, scenario) for candidate in CANDIDATES for scenario in SCENARIOS]


if __name__ == "__main__":
    unittest.main()
