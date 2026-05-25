import unittest
from pathlib import Path

from admin_core.events import extract_user_ip, infer_event_severity, parse_jsonl_lines


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "events"


def fixture_lines(name):
    return (FIXTURE_DIR / name).read_text(encoding="utf-8").splitlines()


class EventsHelperTest(unittest.TestCase):
    def test_parse_jsonl_lines_parses_valid_rows(self):
        rows = parse_jsonl_lines(fixture_lines("simple_events.jsonl"))
        self.assertEqual(rows[0]["action"], "admin_login")
        self.assertEqual(rows[1]["message"], "verify ok")

    def test_parse_jsonl_lines_preserves_malformed_rows_as_raw(self):
        rows = parse_jsonl_lines(fixture_lines("malformed_events.jsonl"))
        self.assertEqual(rows[0]["action"], "ok")
        self.assertEqual(rows[1], {"raw": "not json at all"})
        self.assertEqual(rows[2], {"raw": '{"action":"truncated",'})
        self.assertEqual(rows[3], {"raw": ""})
        self.assertEqual(rows[4]["action"], "after")

    def test_parse_jsonl_lines_accepts_redactor_callback(self):
        rows = parse_jsonl_lines(['{"token":"secret","safe":"ok"}'], redact_value=lambda value: {"redacted": value})
        self.assertEqual(rows, [{"redacted": {"token": "secret", "safe": "ok"}}])

    def test_tail_behavior_is_preserved_by_calling_code_slicing(self):
        lines = fixture_lines("large_tail.jsonl")
        rows = parse_jsonl_lines(lines[-3:])
        self.assertEqual([row["idx"] for row in rows], [8, 9, 10])

    def test_infer_event_severity_preserves_current_priority(self):
        rows = parse_jsonl_lines(fixture_lines("mixed_severity.jsonl"))
        self.assertEqual([infer_event_severity(row) for row in rows], ["error", "warning", "info", "warning", "info"])

    def test_missing_fields_default_to_info_or_keyword_based_severity(self):
        rows = parse_jsonl_lines(fixture_lines("missing_fields.jsonl"))
        self.assertEqual([infer_event_severity(row) for row in rows], ["info", "error", "warning"])

    def test_unicode_and_user_ip_extraction(self):
        rows = parse_jsonl_lines(fixture_lines("unicode_events.jsonl"))
        self.assertEqual(rows[0]["message"], "проверка прошла ok")
        self.assertEqual(extract_user_ip(rows[0]["message"]), "")
        self.assertEqual(extract_user_ip(rows[1]["message"]), "10.0.0.7")

    def test_extract_user_ip_uses_current_vpn_subnet_pattern_only(self):
        self.assertEqual(extract_user_ip("client 10.0.0.255 failed"), "10.0.0.255")
        self.assertEqual(extract_user_ip("client 10.7.0.2 failed"), "")
        self.assertEqual(extract_user_ip(None), "")


if __name__ == "__main__":
    unittest.main()
