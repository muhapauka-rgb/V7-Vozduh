import unittest
from pathlib import Path

from admin_core.registry_readers import parse_kv_line, parse_registry_lines


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "registry"


def fixture_lines(name):
    return (FIXTURE_DIR / name).read_text(encoding="utf-8").splitlines()


class RegistryReaderTest(unittest.TestCase):
    def test_parse_kv_line_preserves_current_whitespace_split_contract(self):
        self.assertEqual(
            parse_kv_line("id=u1 broken current=awg3 value=a=b"),
            {"id": "u1", "current": "awg3", "value": "a=b"},
        )

    def test_simple_registry(self):
        self.assertEqual(
            parse_registry_lines(fixture_lines("simple.registry")),
            [
                {"id": "u1", "ip": "10.7.0.2", "current": "awg3", "enabled": "1"},
                {"id": "u2", "ip": "10.7.0.3", "current": "vless", "enabled": "0"},
            ],
        )

    def test_comments_and_empty_lines_are_skipped_after_strip(self):
        self.assertEqual(
            parse_registry_lines(fixture_lines("comments_empty.registry")),
            [{"id": "u1", "current": "awg3"}],
        )

    def test_malformed_parts_are_ignored_but_malformed_rows_are_preserved(self):
        self.assertEqual(
            parse_registry_lines(fixture_lines("malformed_lines.registry")),
            [
                {},
                {"id": "u1", "current": "awg3"},
                {"id": "u2", "key": "value", "shadow": "kept"},
            ],
        )

    def test_duplicate_keys_keep_last_value(self):
        self.assertEqual(
            parse_registry_lines(fixture_lines("duplicate_keys.registry")),
            [
                {"id": "u1", "current": "awg3"},
                {"id": "u2", "tag": "second"},
            ],
        )

    def test_quoted_values_are_not_shell_parsed(self):
        self.assertEqual(
            parse_registry_lines(fixture_lines("quoted_values.registry")),
            [
                {"id": "u1", "name": '"Alice', "note": "value=with=equals"},
                {"id": "u2", "name": "'Single", "label": "plain"},
            ],
        )

    def test_whitespace_and_unicode_values(self):
        self.assertEqual(
            parse_registry_lines(fixture_lines("whitespace.registry")),
            [
                {"id": "u1", "current": "awg3", "enabled": "1"},
                {"id": "u2", "current": "vless"},
                {"id": "u3", "value": "unicode-значение"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
