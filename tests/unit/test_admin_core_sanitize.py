import unittest

from admin_core.sanitize import redact


class SanitizeHelperTest(unittest.TestCase):
    def test_redacts_secret_keys_in_nested_data_without_mutating_input(self):
        original = {
            "public": "ok",
            "password": "secret",
            "nested": [{"token": "abc"}, {"value": "kept"}],
        }
        redacted = redact(original)
        self.assertEqual(original["password"], "secret")
        self.assertEqual(redacted["password"], "[REDACTED]")
        self.assertEqual(redacted["nested"][0]["token"], "[REDACTED]")
        self.assertEqual(redacted["nested"][1]["value"], "kept")

    def test_redacts_wireguard_and_json_style_strings(self):
        text = 'PrivateKey = abc123\n{"token": "secret", "safe": "value"}'
        redacted = redact(text)
        self.assertIn("PrivateKey=[REDACTED]", redacted)
        self.assertIn('"token": "[REDACTED]"', redacted)
        self.assertIn('"safe": "value"', redacted)

    def test_redacts_inline_blocks(self):
        text = "before\n<tls-crypt>\nsecret\nmaterial\n</tls-crypt>\nafter"
        self.assertEqual(redact(text), "before\n<tls-crypt>[REDACTED]</tls-crypt>\nafter")

    def test_preserves_non_secret_non_string_values(self):
        self.assertIsNone(redact(None))
        self.assertEqual(redact(42), 42)
        self.assertEqual(redact(["safe"]), ["safe"])


if __name__ == "__main__":
    unittest.main()

