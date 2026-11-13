"""Harness regression probe, scratch module, not collected by the suite.

Regression for BEH2-F1: a present module whose own import of a
missing submodule of itself fails must surface as an error, not as
the NOT BUILT marker. This module stands outside the test discovery
pattern on purpose, so the suite totals are unchanged by it. Run it
directly, for example with python3 -m unittest
tests.scratch_harness_regression from the system directory.
"""

import importlib
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from tests.harness import require
except ImportError:
    from harness import require

PACKAGE = "harness_regression_present_pkg"


class TestHarnessRegression(unittest.TestCase):
    """Harness regression: present but broken module is an error."""

    def test_present_module_importing_missing_submodule_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = Path(tmp) / PACKAGE
            package_dir.mkdir()
            (package_dir / "__init__.py").write_text(
                "import " + PACKAGE + ".missing_inner_xyz\n",
                encoding="utf-8",
            )
            sys.path.insert(0, tmp)
            importlib.invalidate_caches()
            try:
                with self.assertRaises(ModuleNotFoundError):
                    require(PACKAGE)
            finally:
                sys.path.remove(tmp)
                sys.modules.pop(PACKAGE, None)
                importlib.invalidate_caches()


if __name__ == "__main__":
    unittest.main()
