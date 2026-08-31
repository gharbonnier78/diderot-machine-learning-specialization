from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HarnessBootstrapTest(unittest.TestCase):
    def test_agent_bootstraps_match_manifest_pin(self) -> None:
        manifest = (ROOT / "harness-adoption.yaml").read_text(encoding="utf-8")
        match = re.search(r'^\s*ref:\s*["\']?([0-9a-f]{40})["\']?\s*$', manifest, re.M)
        self.assertIsNotNone(match, "harness-adoption.yaml must pin an immutable 40-character commit SHA")
        harness_ref = match.group(1)

        for filename in ("AGENTS.md", "CLAUDE.md"):
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("harness-adoption.yaml", text)
                self.assertIn(harness_ref, text, f"{filename} must use the same harness ref as the manifest")
                self.assertIn("MATHEMATICAL_NOTATION_CAPITALIZATION.md", text)
                self.assertIn("mmals-ml-wiki", text, "canonical Diderot notation atlas must remain discoverable")

    def test_meta_documentation_records_current_pin(self) -> None:
        manifest = (ROOT / "harness-adoption.yaml").read_text(encoding="utf-8")
        harness_ref = re.search(r'^\s*ref:\s*["\']?([0-9a-f]{40})["\']?\s*$', manifest, re.M).group(1)
        meta = (ROOT / "docs" / "harness-meta.md").read_text(encoding="utf-8")
        self.assertIn(harness_ref, meta)


if __name__ == "__main__":
    unittest.main()
