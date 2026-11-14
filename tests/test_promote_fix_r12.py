"""Fix round 12 pins for the PROMOTE scope, Region 4.

Written test first for triage rulings 396, 397, 398, and 399 at
design/steps/step-15-r12-triage.md. Ruling 396 counts R12-PRO-1.
Ruling 397 counts R12-PRO-2. Ruling 398 counts R12-PRO-3. Ruling
399 counts R12-PRO-4. Each ruling stands counted in its own act
here and nowhere else in this region. No pin of this file stands
in tests/test_unrowed_b.py: the domain pins of ruling 412 stand
in Region 7 alone.
"""

import unittest
from collections import ChainMap, OrderedDict, UserDict, UserString
from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction
from types import MappingProxyType

from tests import harness


class _CustomMapping(Mapping):
    """A Mapping subclass standing as no dict instance."""

    def __init__(self, values):
        self._values = dict(values)

    def __getitem__(self, key):
        return self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)


def _mapping_forms(values):
    return (
        UserDict(values),
        MappingProxyType(dict(values)),
        ChainMap(dict(values)),
        _CustomMapping(values),
    )


_MARKER = "over D-10 bound"
_MARKER_BYTES = b"over D-10 bound"


def _byte_forms(value):
    raw = value.encode("utf-8") if isinstance(value, str) else bytes(value)
    return (
        bytes(raw),
        bytearray(raw),
        memoryview(raw),
    )


class ConstructCandidateByteFormTests(unittest.TestCase):
    """Ruling 396: construct_candidate reads a size in byte form."""

    def test_over_bound_marker_in_each_byte_form_refused(self):
        mod = harness.require("ontoloop.promote")
        for form in _byte_forms(_MARKER):
            result = mod.construct_candidate(bundle_size=form)
            self.assertEqual(result["outcome"], "refused", type(form).__name__)
            self.assertEqual(
                result["check_point"], "candidate construction",
                type(form).__name__)

    def test_size_under_bound_in_byte_form_still_constructs(self):
        mod = harness.require("ontoloop.promote")
        for form in _byte_forms("within bound"):
            result = mod.construct_candidate(bundle_size=form)
            self.assertEqual(
                result["outcome"], "constructed", type(form).__name__)
            self.assertEqual(result["check_point"], "candidate construction")

    def test_standing_marker_forms_still_refuse(self):
        mod = harness.require("ontoloop.promote")
        for size in (_MARKER, UserString(_MARKER)):
            result = mod.construct_candidate(bundle_size=size)
            self.assertEqual(result["outcome"], "refused", repr(size))
            self.assertEqual(result["check_point"], "candidate construction")
        result = mod.construct_candidate(bundle_size="within bound")
        self.assertEqual(result["outcome"], "constructed")


class WriteBundleByteFormTests(unittest.TestCase):
    """Ruling 397: write_bundle reads a size in byte form, both forms."""

    def test_marker_in_each_byte_form_refused_at_keyword_form(self):
        mod = harness.require("ontoloop.promote")
        for form in _byte_forms(_MARKER):
            result = mod.write_bundle(bundle_size=form)
            self.assertEqual(result["outcome"], "refused", type(form).__name__)
            self.assertEqual(result["check_point"], "bundle writing")
            self.assertEqual(result["bundle_size_after"], form)
            self.assertFalse(result["trimmed"])

    def test_marker_in_each_byte_form_refused_at_candidate_form(self):
        mod = harness.require("ontoloop.promote")
        for form in _byte_forms(_MARKER):
            candidate = {"size": form}
            for presented in (dict(candidate),) + _mapping_forms(candidate):
                result = mod.write_bundle(presented)
                self.assertEqual(
                    result["outcome"], "refused", type(presented).__name__)
                self.assertEqual(result["check_point"], "bundle writing")
                self.assertEqual(result["bundle_size_after"], form)
                self.assertFalse(result["trimmed"])

    def test_size_under_bound_in_byte_form_still_writes(self):
        mod = harness.require("ontoloop.promote")
        for form in _byte_forms("within bound"):
            result = mod.write_bundle(bundle_size=form)
            self.assertEqual(result["outcome"], "written", type(form).__name__)
            self.assertEqual(result["bundle_size_after"], form)
            self.assertFalse(result["trimmed"])
            result = mod.write_bundle({"size": form})
            self.assertEqual(result["outcome"], "written", type(form).__name__)
            self.assertEqual(result["bundle_size_after"], form)
            self.assertFalse(result["trimmed"])

    def test_standing_marker_forms_still_refuse_at_both_forms(self):
        mod = harness.require("ontoloop.promote")
        result = mod.write_bundle(bundle_size=_MARKER)
        self.assertEqual(result["outcome"], "refused")
        result = mod.write_bundle({"size": UserString(_MARKER)})
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["bundle_size_after"], UserString(_MARKER))
        candidate = mod.candidate_over_bound()
        result = mod.write_bundle(candidate)
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["bundle_size_after"], candidate["size"])


class ReuseWarningGovernedFormTests(unittest.TestCase):
    """Ruling 398: reuse_warning_at_count reads bound and count in
    governed form outside the plain int form, with its threshold
    computed without a float conversion that rounds it."""

    def test_non_numeric_bound_forms_raise_governed_refusal(self):
        mod = harness.require("ontoloop.promote")
        for bound in ("3", None, [3], {"bound": 3}, {3}, object()):
            with self.assertRaises(ValueError) as caught:
                mod.reuse_warning_at_count(2, bound=bound)
            self.assertEqual(
                str(caught.exception),
                "unknown reuse warning bound: %r" % (bound,),
                repr(bound))

    def test_non_finite_bound_forms_raise_governed_refusal(self):
        mod = harness.require("ontoloop.promote")
        for bound in (float("inf"), float("-inf"), float("nan"),
                      Decimal("Infinity"), Decimal("NaN")):
            with self.assertRaises(ValueError) as caught:
                mod.reuse_warning_at_count(2, bound=bound)
            self.assertEqual(
                str(caught.exception),
                "unknown reuse warning bound: %r" % (bound,),
                repr(bound))

    def test_decimal_and_fraction_bounds_read_for_their_value(self):
        mod = harness.require("ontoloop.promote")
        outcome = mod.reuse_warning_at_count(1, bound=Decimal("2.5"))
        self.assertEqual(outcome["firing_point_count"], 1)
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["bound_after"], Decimal("2.5"))
        self.assertFalse(outcome["act_blocked"])
        outcome = mod.reuse_warning_at_count(2, bound=Fraction(7, 2))
        self.assertEqual(outcome["firing_point_count"], 2)
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["bound_after"], Fraction(7, 2))
        outcome = mod.reuse_warning_at_count(1, bound=Fraction(7, 2))
        self.assertFalse(outcome["fired"])
        with self.assertRaises(ValueError) as caught:
            mod.reuse_warning_at_count(0, bound=Decimal("0.5"))
        self.assertEqual(
            str(caught.exception),
            "unknown reuse warning bound: Decimal('0.5')")
        with self.assertRaises(ValueError) as caught:
            mod.reuse_warning_at_count(0, bound=Fraction(1, 2))
        self.assertEqual(
            str(caught.exception),
            "unknown reuse warning bound: Fraction(1, 2)")

    def test_float_bound_read_for_its_value(self):
        mod = harness.require("ontoloop.promote")
        outcome = mod.reuse_warning_at_count(2, bound=3.0)
        self.assertEqual(outcome["firing_point_count"], 2)
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["bound_after"], 3.0)

    def test_huge_bound_threshold_computed_exactly(self):
        mod = harness.require("ontoloop.promote")
        bound = 10 ** 100
        expected = 75 * 10 ** 98
        under = mod.reuse_warning_at_count(expected - 1, bound=bound)
        self.assertEqual(under["firing_point_count"], expected)
        self.assertFalse(under["fired"])
        self.assertEqual(under["bound_after"], bound)
        at = mod.reuse_warning_at_count(expected, bound=bound)
        self.assertEqual(at["firing_point_count"], expected)
        self.assertTrue(at["fired"])

    def test_bound_beyond_float_range_still_decides(self):
        mod = harness.require("ontoloop.promote")
        bound = 10 ** 400
        expected = 3 * 10 ** 400 // 4
        outcome = mod.reuse_warning_at_count(expected, bound=bound)
        self.assertEqual(outcome["firing_point_count"], expected)
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["bound_after"], bound)

    def test_non_numeric_count_raises_governed_refusal(self):
        mod = harness.require("ontoloop.promote")
        for count in ("2", None, [2], {"count": 2}):
            with self.assertRaises(ValueError) as caught:
                mod.reuse_warning_at_count(count, bound=3)
            self.assertEqual(
                str(caught.exception),
                "unknown reuse warning count: %r" % (count,),
                repr(count))

    def test_numeric_count_forms_read_for_their_value(self):
        mod = harness.require("ontoloop.promote")
        self.assertTrue(
            mod.reuse_warning_at_count(Decimal("2"), bound=3)["fired"])
        self.assertFalse(
            mod.reuse_warning_at_count(Fraction(3, 2), bound=3)["fired"])
        self.assertTrue(
            mod.reuse_warning_at_count(2.0, bound=3)["fired"])
        self.assertFalse(
            mod.reuse_warning_at_count(float("nan"), bound=3)["fired"])
        self.assertTrue(
            mod.reuse_warning_at_count(float("inf"), bound=3)["fired"])

    def test_standing_reuse_pins_still_pass(self):
        mod = harness.require("ontoloop.promote")
        with self.assertRaises(ValueError) as caught:
            mod.reuse_warning_at_count(0, bound=0)
        self.assertEqual(str(caught.exception),
                         "unknown reuse warning bound: 0")
        outcome = mod.reuse_warning_at_count(2, bound=3)
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["firing_point_count"], 2)
        self.assertEqual(outcome["bound_after"], 3)
        outcome = mod.reuse_warning_at_count(74, bound=100)
        self.assertFalse(outcome["fired"])
        self.assertEqual(outcome["firing_point_count"], 75)
        outcome = mod.reuse_warning_at_count(75, bound=100)
        self.assertTrue(outcome["fired"])


class ReviewSliceOutputMappingFormTests(unittest.TestCase):
    """Ruling 399: review_slice_output reads its slice output through
    the abstract mapping discipline of its siblings."""

    def _assert_governed_record(self, review, mod):
        self.assertEqual(review["second_statement_findings"], [])
        self.assertEqual(
            sorted(review["accounted_rules"]),
            sorted(mod.state_table_rules()))
        self.assertEqual(review["record_home"], "PROMOTE slice exit record")
        self.assertTrue(review["filed"])
        self.assertFalse(review["rests_on_search_result"])

    def test_non_mapping_outputs_return_governed_record(self):
        mod = harness.require("ontoloop.promote")
        for output in ([], "abc", 123, 1.5, True, b"abc", {"a", "b"}):
            review = mod.review_slice_output(slice_output=output)
            self._assert_governed_record(review, mod)

    def test_incomplete_mappings_return_governed_record(self):
        mod = harness.require("ontoloop.promote")
        incomplete = (
            {},
            {"second_statement_rule": "state_rule_01"},
            {"second_statement_passage": "a passage"},
            OrderedDict(),
            UserDict({"second_statement_rule": "state_rule_01"}),
        )
        for output in incomplete:
            review = mod.review_slice_output(slice_output=output)
            self._assert_governed_record(review, mod)

    def test_complete_outputs_in_mapping_forms_still_return_finding(self):
        mod = harness.require("ontoloop.promote")
        output = mod.slice_output_with_a_second_statement()
        for form in (dict(output), OrderedDict(output)) + _mapping_forms(output):
            review = mod.review_slice_output(slice_output=form)
            findings = review["second_statement_findings"]
            self.assertEqual(len(findings), 1, type(form).__name__)
            self.assertEqual(
                findings[0]["rule"], output["second_statement_rule"])
            self.assertEqual(
                findings[0]["passage"], output["second_statement_passage"])

    def test_no_output_call_still_returns_standing_record(self):
        mod = harness.require("ontoloop.promote")
        review = mod.review_slice_output(reviewer="named reviewer")
        self._assert_governed_record(review, mod)
        review = mod.review_slice_output()
        self._assert_governed_record(review, mod)


if __name__ == "__main__":
    unittest.main()
