"""Fix round 4 Region 5 pinning tests for defect N-04.

Ruling 22 of the Round 4 triage: provisional_record must
distinguish no value from an empty value on each of its four
value parameters. An explicitly passed empty list yields empty
mixes for its period, with the mix counts computed from the
empty lists, while a parameter not passed keeps the fixture
default the module docstring states. Written test first.
"""

import unittest

from tests import harness


class ProvisionalEmptyListTests(unittest.TestCase):
    """N-04: an explicit empty list is a value, not an absence."""

    def test_provisional_outcomes_empty_alone(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(
            provisional_outcomes=[],
            displaced_outcomes=["pass", "fail"],
            provisional_corrections=["open"],
            displaced_corrections=["corrected", "corrected"])
        comparison = record["comparison"]
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"], {})
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})
        self.assertEqual(
            comparison["provisional_period"]["correction_position"],
            {"open": 1})
        self.assertEqual(
            comparison["displaced_period"]["correction_position"],
            {"corrected": 2})

    def test_displaced_outcomes_empty_alone(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(
            provisional_outcomes=["pass", "fail"],
            displaced_outcomes=[],
            provisional_corrections=["open"],
            displaced_corrections=["corrected", "corrected"])
        comparison = record["comparison"]
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"], {})
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})
        self.assertEqual(
            comparison["provisional_period"]["correction_position"],
            {"open": 1})
        self.assertEqual(
            comparison["displaced_period"]["correction_position"],
            {"corrected": 2})

    def test_provisional_corrections_empty_alone(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(
            provisional_outcomes=["pass", "fail"],
            displaced_outcomes=["pass"],
            provisional_corrections=[],
            displaced_corrections=["corrected", "corrected"])
        comparison = record["comparison"]
        self.assertEqual(
            comparison["provisional_period"]["correction_position"], {})
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"], {"pass": 1})
        self.assertEqual(
            comparison["displaced_period"]["correction_position"],
            {"corrected": 2})

    def test_displaced_corrections_empty_alone(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(
            provisional_outcomes=["pass", "fail"],
            displaced_outcomes=["pass"],
            provisional_corrections=["open"],
            displaced_corrections=[])
        comparison = record["comparison"]
        self.assertEqual(
            comparison["displaced_period"]["correction_position"], {})
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"], {"pass": 1})
        self.assertEqual(
            comparison["provisional_period"]["correction_position"],
            {"open": 1})

    def test_all_four_empty(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(
            provisional_outcomes=[],
            displaced_outcomes=[],
            provisional_corrections=[],
            displaced_corrections=[])
        comparison = record["comparison"]
        self.assertIsNotNone(comparison)
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"], {})
        self.assertEqual(
            comparison["provisional_period"]["correction_position"], {})
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"], {})
        self.assertEqual(
            comparison["displaced_period"]["correction_position"], {})

    def test_confirm_provisional_consequence_on_all_empty(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(
            provisional_outcomes=[],
            displaced_outcomes=[],
            provisional_corrections=[],
            displaced_corrections=[])
        comparison = record["comparison"]
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"], {})
        self.assertEqual(
            comparison["provisional_period"]["correction_position"], {})
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"], {})
        self.assertEqual(
            comparison["displaced_period"]["correction_position"], {})
        result = mod.confirm_provisional(record)
        self.assertEqual(result["outcome"], "confirmed")
        self.assertNotIn("bar_reason", result)

    def test_no_value_keeps_fixture_defaults(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record()
        comparison = record["comparison"]
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"],
            {"pass": 2, "fail": 1})
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"],
            {"pass": 1, "fail": 2})
        self.assertEqual(
            comparison["provisional_period"]["correction_position"],
            {"corrected": 1, "open": 1})
        self.assertEqual(
            comparison["displaced_period"]["correction_position"],
            {"corrected": 1, "open": 1})

    def test_explicit_none_keeps_fixture_defaults(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(
            provisional_outcomes=None,
            displaced_outcomes=None,
            provisional_corrections=None,
            displaced_corrections=None)
        comparison = record["comparison"]
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"],
            {"pass": 2, "fail": 1})
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"],
            {"pass": 1, "fail": 2})
        self.assertEqual(
            comparison["provisional_period"]["correction_position"],
            {"corrected": 1, "open": 1})
        self.assertEqual(
            comparison["displaced_period"]["correction_position"],
            {"corrected": 1, "open": 1})


if __name__ == "__main__":
    unittest.main()
