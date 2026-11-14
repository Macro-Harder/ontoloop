"""Fix round 1 PRO pinning tests.

Written test first for behaviours the standing suite does not pin
by name, in particular the refusal with no period open act at
plan section 4.4 (register S15-R1-047, PR-F6), and for the real
computation limbs of the consume and surfaces cures.
"""

import unittest

from tests import harness


class RefusalWithNoPeriodOpenTests(unittest.TestCase):
    """PR-F6: refusal recorded with no period open is refused."""

    def test_refusal_with_no_period_open_is_refused_and_spends_nothing(self):
        mod = harness.require("ontoloop.promote")
        result = mod.record_refusal(period_open=False)
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["error"], "refusal with no period open")
        self.assertFalse(result["recorded"])
        self.assertTrue(result["spends_nothing"])

    def test_refusal_with_a_period_open_is_recorded(self):
        mod = harness.require("ontoloop.promote")
        result = mod.record_refusal(period_open=True)
        self.assertEqual(result["outcome"], "recorded")
        self.assertTrue(result["recorded"])


class ConsumeRealActTests(unittest.TestCase):
    def test_discovery_returns_current_bundle_after_a_promotion(self):
        mod = harness.require("ontoloop.consumption")
        mod.record_promotion("pro workflow", bundle="bundle version 9")
        result = mod.discover(workflow="pro workflow")
        self.assertNotEqual(result["answer"], "no promotion")
        self.assertEqual(result["bundle"], "bundle version 9")
        other = mod.discover(workflow="unrelated workflow")
        self.assertEqual(other["answer"], "no promotion")

    def test_hash_check_varies_with_material(self):
        mod = harness.require("ontoloop.consumption")
        first = mod.load_with_hash_mismatch(material="alpha content")
        second = mod.load_with_hash_mismatch(material="beta content")
        self.assertNotEqual(first["presented_hash"], second["presented_hash"])
        self.assertEqual(first["position"], "unloadable")
        self.assertIn("load_refusal_record", first)

    def test_matching_hash_loads(self):
        mod = harness.require("ontoloop.consumption")
        import hashlib
        digest = hashlib.sha256(b"known material").hexdigest()
        result = mod.load_with_hash_check("known material", expected_hash=digest)
        self.assertTrue(result["loaded"])

    def test_attributed_version_matches_load_version(self):
        mod = harness.require("ontoloop.consumption")
        run = mod.run_once()
        self.assertEqual(run["attribution"]["bundle_version"],
                         mod.current_bundle("any workflow"))
        self.assertTrue(mod.run_records())


class SurfacesRealActTests(unittest.TestCase):
    def test_negative_list_covers_seven_abilities(self):
        mod = harness.require("ontoloop.service_layer")
        results = mod.negative_list_results()
        self.assertGreaterEqual(len(results), 7)

    def test_stamps_vary_with_material_and_carry_channel(self):
        mod = harness.require("ontoloop.service_layer")
        first = mod.submit_through("agent surface", material="one material")
        second = mod.submit_through("agent surface", material="other material")
        self.assertNotEqual(first["stamps"], second["stamps"])
        self.assertIn("channel", first["stamps"])
        same = mod.submit_through("operator surface", material="one material")
        self.assertEqual(first["stamps"], same["stamps"])


class InventoryRebuildTests(unittest.TestCase):
    def test_inventory_names_expected_readers_and_version(self):
        mod = harness.require("ontoloop.consumption")
        inventory = mod.holdout_content_access_inventory()
        self.assertIn("cross split audit", inventory["listed_components"])
        self.assertTrue(inventory["inventory_version"])
        entry = inventory["entries"]["cross split audit"]
        self.assertIn("read_position", entry)


if __name__ == "__main__":
    unittest.main()
