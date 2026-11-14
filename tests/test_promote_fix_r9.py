"""Fix round 9 pins for the PROMOTE scope, Region 4.

Written test first for triage rulings 256, 263, and 264 at
design/steps/step-15-r9-triage.md. Ruling 256 counts R9-PRO-1,
Chair Finding F-2, and the provisional limb of Lead Engineer
line E-6 in that act and nowhere else in this region.
Ruling 263 counts R9-PRO-2. Ruling 264 counts R9-PRO-3.
"""

import unittest
from array import array
from collections import UserString

from tests import harness


class ProvisionalWritableMemoryviewTests(unittest.TestCase):
    """Ruling 256: a writable memoryview item in a provisional value list."""

    def _assert_governed(self, mod, kwargs):
        with self.assertRaises(ValueError) as caught:
            mod.provisional_record(**kwargs)
        self.assertEqual(
            str(caught.exception),
            "provisional values must stand as a list of values")

    def test_writable_memoryview_item_at_each_of_the_four_sites(self):
        mod = harness.require("ontoloop.promote")
        for site in ("provisional_outcomes", "displaced_outcomes",
                     "provisional_corrections", "displaced_corrections"):
            item = memoryview(bytearray(b"pass"))
            self._assert_governed(mod, {site: [item]})

    def test_standing_unhashable_item_forms_still_governed(self):
        mod = harness.require("ontoloop.promote")
        for item in ([], {}, {"pass"}, bytearray(b"pass"), (["pass"],)):
            self._assert_governed(
                mod, {"provisional_outcomes": [item]})

    def test_standing_record_still_builds_and_confirms(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(
            provisional_outcomes=["pass", "fail"])
        self.assertIsNotNone(record["comparison"])
        result = mod.confirm_provisional(record)
        self.assertEqual(result["outcome"], "confirmed")


class AllowedValuesUnhashableFieldTests(unittest.TestCase):
    """Ruling 263: an unhashable field name in allowed_values."""

    def _assert_governed(self, mod, field):
        with self.assertRaises(ValueError) as caught:
            mod.allowed_values(field)
        self.assertEqual(
            str(caught.exception),
            "unknown confirmation field: %r" % (field,))

    def test_unhashable_field_forms_raise_governed_value_error(self):
        mod = harness.require("ontoloop.promote")
        pinned = b"production_evidence_label_position"
        forms = (
            bytearray(pinned),
            ["production_evidence_label_position"],
            {"production_evidence_label_position": 1},
            {"production_evidence_label_position"},
            array("b", b"x"),
            array("u", "x"),
            memoryview(bytearray(b"pass")),
        )
        for field in forms:
            self._assert_governed(mod, field)

    def test_pinned_names_and_standing_unknown_forms_preserved(self):
        mod = harness.require("ontoloop.promote")
        for field in ("production_evidence_label_position",
                      "production_evidence_weight_position",
                      UserString("production_evidence_label_position")):
            values = mod.allowed_values(field)
            self.assertEqual(values, ["at record head", "at record foot"])
        for field in (frozenset({"x"}), ("x",), range(1), None, "bogus"):
            self._assert_governed(mod, field)


class CandidateUnhashableKindTests(unittest.TestCase):
    """Ruling 264: an unhashable kind in candidate_with_instruction_item."""

    def _assert_governed(self, mod, kind):
        with self.assertRaises(ValueError) as caught:
            mod.candidate_with_instruction_item(kind=kind)
        self.assertEqual(
            str(caught.exception),
            "unknown instruction item kind: %r" % (kind,))

    def test_unhashable_kind_forms_raise_governed_value_error(self):
        mod = harness.require("ontoloop.promote")
        pinned = b"clean instruction"
        forms = (
            bytearray(pinned),
            ["clean instruction"],
            {"clean instruction": 1},
            {"clean instruction"},
            array("b", b"x"),
            array("u", "x"),
            memoryview(bytearray(b"pass")),
        )
        for kind in forms:
            self._assert_governed(mod, kind)

    def test_pinned_kinds_and_standing_unknown_forms_preserved(self):
        mod = harness.require("ontoloop.promote")
        for kind in ("verbatim holdout content",
                     "near verbatim holdout content",
                     "clean instruction"):
            bundle = mod.candidate_with_instruction_item(kind=kind)
            self.assertEqual(bundle["kind"], kind)
            self.assertEqual(bundle["instruction_item_count"], 1)
        for kind in (frozenset({"x"}), ("x",), range(1), None, "bogus"):
            self._assert_governed(mod, kind)


if __name__ == "__main__":
    unittest.main()
