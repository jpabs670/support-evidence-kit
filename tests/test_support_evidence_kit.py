from pathlib import Path
import tempfile
import unittest

from support_evidence_kit.bundle import build_bundle
from support_evidence_kit.classify import classify_text
from support_evidence_kit.redact import redact_text


class RedactionTests(unittest.TestCase):
    def test_redacts_common_sensitive_values(self) -> None:
        text = (
            "email admin@example.com host 192.0.2.10 "
            "token=abc123456789 Bearer test-token-12345"
        )
        redacted, counts = redact_text(text)
        self.assertNotIn("admin@example.com", redacted)
        self.assertNotIn("192.0.2.10", redacted)
        self.assertNotIn("abc123456789", redacted)
        self.assertEqual(counts["email"], 1)
        self.assertEqual(counts["ipv4"], 1)


class ClassificationTests(unittest.TestCase):
    def test_classifies_cross_layer_evidence(self) -> None:
        layers = classify_text("nginx returned HTTP 502 after a DNS timeout")
        self.assertEqual(layers, ["linux_service", "application_http", "network"])


class BundleTests(unittest.TestCase):
    def test_builds_manifest_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "incident"
            output = root / "build"
            source.mkdir()
            (source / "service.log").write_text(
                "systemctl: nginx active; curl HTTP 200; host 192.0.2.42\n",
                encoding="utf-8",
            )

            manifest = build_bundle(source, output)

            self.assertEqual(manifest["file_count"], 1)
            self.assertIn("linux_service", manifest["layers"])
            self.assertTrue((output / "evidence.json").exists())
            self.assertTrue((output / "escalation.md").exists())
            self.assertNotIn(
                "192.0.2.42",
                (output / "escalation.md").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()

