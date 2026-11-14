"""Fix round 3 region 5 pinning tests: consume and ops surfaces.

Written test first for triage rulings 3, 6, and 7 at
design/steps/step-15-r3-triage.md. Ruling 3 pins the shown
flag standing True itself in purge_without_preview. Rulings
6 and 7 pin the two docstrings against the returns they
describe, reading the return and the description together.
"""

import hashlib
import unittest

from tests import harness


class OpsPurgeShownFlagStrictTrueTests(unittest.TestCase):
    """Ruling 3, S15-R3-003: the flag stands True itself only."""

    def assert_failed(self, outcome):
        self.assertTrue(outcome["failed"])
        self.assertFalse(outcome["purge_proceeded"])
        self.assertEqual(
            outcome["reason"], "no preview shown for that act"
        )

    def assert_proceeded(self, outcome):
        self.assertFalse(outcome["failed"])
        self.assertTrue(outcome["purge_proceeded"])

    def test_string_flag_values_fail(self):
        module = harness.require("ontoloop.ops")
        for flag in ("no preview shown", "False", "True", "yes"):
            outcome = module.purge_without_preview(preview_shown=flag)
            self.assert_failed(outcome)

    def test_integer_flag_values_fail(self):
        module = harness.require("ontoloop.ops")
        for flag in (1, 42, -1):
            outcome = module.purge_without_preview(preview_shown=flag)
            self.assert_failed(outcome)

    def test_list_flag_values_fail(self):
        module = harness.require("ontoloop.ops")
        for flag in (["preview shown"], [True], ["x", "y"]):
            outcome = module.purge_without_preview(preview_shown=flag)
            self.assert_failed(outcome)

    def test_other_truthy_flag_values_fail(self):
        module = harness.require("ontoloop.ops")
        for flag in ({"shown": True}, (True,), 1.0):
            outcome = module.purge_without_preview(preview_shown=flag)
            self.assert_failed(outcome)

    def test_governed_true_flag_proceeds(self):
        module = harness.require("ontoloop.ops")
        self.assert_proceeded(
            module.purge_without_preview(preview_shown=True)
        )
        self.assert_proceeded(
            module.purge_without_preview(preview=False, preview_shown=True)
        )

    def test_standing_preview_forms_proceed(self):
        module = harness.require("ontoloop.ops")
        preview = module.purge_preview()
        self.assert_proceeded(module.purge_without_preview(preview=preview))
        minimal = {
            "record_home": "operator surface record for the purge occasion",
            "identities_affected": ["identity a"],
        }
        self.assert_proceeded(module.purge_without_preview(preview=minimal))

    def test_preview_form_proceeds_beside_a_junk_flag(self):
        module = harness.require("ontoloop.ops")
        minimal = {
            "record_home": "operator surface record for the purge occasion",
            "identities_affected": ["identity a"],
        }
        self.assert_proceeded(
            module.purge_without_preview(
                preview=minimal, preview_shown="no preview shown"
            )
        )

    def test_no_preview_and_no_flag_still_fails(self):
        module = harness.require("ontoloop.ops")
        self.assert_failed(module.purge_without_preview())
        self.assert_failed(
            module.purge_without_preview(preview_shown=False)
        )


class ConsumeInventoryDocstringTests(unittest.TestCase):
    """Ruling 6, S15-R3-006: the inventory docstring as built."""

    def test_return_form_and_description_agree(self):
        mod = harness.require("ontoloop.consumption")
        inventory = mod.holdout_content_access_inventory()
        doc = mod.holdout_content_access_inventory.__doc__ or ""
        self.assertEqual(
            set(inventory),
            {
                "listed_components",
                "entries",
                "inventory_version",
                "heading_block",
            },
        )
        self.assertEqual(len(inventory), 4)
        self.assertTrue(inventory["inventory_version"])
        cross = inventory["entries"]["cross split audit"]
        self.assertEqual(
            set(cross),
            {
                "sealed_holdout_content_held",
                "component",
                "runs_through",
                "read_position",
            },
        )
        for name in (
            "rescoring through the override",
            "verifier content exceptions through the override",
            "candidate construction",
        ):
            self.assertEqual(
                set(inventory["entries"][name]),
                {"sealed_holdout_content_held"},
                name,
            )
        self.assertIn("four keys", doc)
        self.assertIn("inventory_version", doc)
        self.assertIn("component", doc)
        self.assertIn("runs_through", doc)
        self.assertIn("read_position", doc)
        self.assertNotIn("exactly three keys", doc)


class ServiceLayerStampDocstringTests(unittest.TestCase):
    """Ruling 7, S15-R3-007: the stamp docstring as built."""

    def test_stamp_form_and_description_agree(self):
        mod = harness.require("ontoloop.service_layer")
        first = mod.submit_through("operator surface", material="one material")
        second = mod.submit_through(
            "operator surface", material="other material"
        )
        doc = mod.submit_through.__doc__ or ""
        self.assertEqual(
            set(first),
            {"stamp_source", "surface_applied_own_stamp", "stamps"},
        )
        self.assertEqual(
            set(first["stamps"]),
            {"written_by", "stamp_kind", "channel", "material_hash"},
        )
        self.assertEqual(len(first["stamps"]), 4)
        self.assertNotEqual(
            first["stamps"]["material_hash"],
            second["stamps"]["material_hash"],
        )
        self.assertEqual(
            first["stamps"]["material_hash"],
            hashlib.sha256(b"one material").hexdigest(),
        )
        for key in ("written_by", "stamp_kind", "channel"):
            self.assertEqual(first["stamps"][key], second["stamps"][key])
        self.assertIn("four keys", doc)
        self.assertIn("material_hash", doc)
        self.assertNotIn("exactly two keys", doc)
        self.assertNotIn("alters no value", doc)


if __name__ == "__main__":
    unittest.main()
