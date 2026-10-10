#!/usr/bin/env python3
"""Contrato: los validadores de fichero responden INVALID con código 2, nunca un traceback."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
VALIDATORS = ("validate_cache_report.py", "validate_evidence.py")


class UnreadableReportTest(unittest.TestCase):
    def _run(self, script: str, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPTS / script), "--file", str(target)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_missing_report_exits_2_with_invalid_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "cache-report.txt"
            for script in VALIDATORS:
                with self.subTest(script=script):
                    proc = self._run(script, missing)
                    self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                    self.assertNotIn("Traceback", proc.stderr, proc.stderr)
                    self.assertTrue(proc.stdout.startswith("INVALID:"), proc.stdout)

    def test_template_report_is_still_accepted(self) -> None:
        template = SKILL / "templates" / "cache-report.txt"
        proc = self._run("validate_cache_report.py", template)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.startswith("VALID:"), proc.stdout)


if __name__ == "__main__":
    unittest.main()
