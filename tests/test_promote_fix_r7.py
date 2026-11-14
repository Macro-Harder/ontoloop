"""Fix round 7 pins for the PROMOTE scope, Region 5.

Written test first for triage rulings 165, 166, 167, and 168 at
design/steps/step-15-r7-triage.md, beside the standing pins of
tests.test_promote. The ruling 167 pins in this home stand beside
the confined ruling 167 pins in tests.test_unrowed_c, which travel
in the latest push of that file under the act level splitting
discipline stated at ruling 190.
"""

import array
import collections
import unittest

from tests import harness


def _provisional_kwargs(**override):
    kwargs = {
        "provisional_outcomes": ["pass", "fail"],
        "displaced_outcomes": ["pass"],
        "provisional_corrections": ["open"],
        "displaced_corrections": ["corrected"],
    }
    kwargs.update(override)
    return kwargs


class ProvisionalArrayUserStringTests(unittest.TestCase):
    """Ruling 165, R7-PRO-1: array and UserString at the four sites."""

    def _assert_refused(self, mod, **override):
        with self.assertRaises(ValueError) as caught:
            mod.provisional_record(**_provisional_kwargs(**override))
        self.assertEqual(
            str(caught.exception),
            "provisional values must stand as a list of values")

    def test_array_refused_at_provisional_outcomes(self):
        mod = harness.require("ontoloop.promote")
        for value in (array.array("b", b"pass"),
                      array.array("H", [112, 97, 115, 115])):
            self._assert_refused(mod, provisional_outcomes=value)

    def test_array_refused_at_displaced_outcomes(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(
            mod, displaced_outcomes=array.array("b", b"pass"))

    def test_array_refused_at_provisional_corrections(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(
            mod, provisional_corrections=array.array("b", b"corrected"))

    def test_array_refused_at_displaced_corrections(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(
            mod, displaced_corrections=array.array("b", b"corrected"))

    def test_userstring_refused_at_provisional_outcomes(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(
            mod, provisional_outcomes=collections.UserString("pass"))

    def test_userstring_refused_at_displaced_outcomes(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(
            mod, displaced_outcomes=collections.UserString("pass"))

    def test_userstring_refused_at_provisional_corrections(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(
            mod,
            provisional_corrections=collections.UserString("corrected"))

    def test_userstring_refused_at_displaced_corrections(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(
            mod,
            displaced_corrections=collections.UserString("corrected"))

    def test_charged_forms_still_refused_and_list_forms_compute(self):
        mod = harness.require("ontoloop.promote")
        for value in ("pass", b"pass", bytearray(b"pass"),
                      memoryview(b"pass"), {"pass": 2, "fail": 1}):
            self._assert_refused(mod, provisional_outcomes=value)
        record = mod.provisional_record(**_provisional_kwargs())
        self.assertEqual(
            record["comparison"]["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})
        tuple_record = mod.provisional_record(**_provisional_kwargs(
            provisional_outcomes=("pass", "fail")))
        self.assertEqual(
            tuple_record["comparison"]["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})
        set_record = mod.provisional_record(**_provisional_kwargs(
            provisional_outcomes={"pass"}))
        self.assertEqual(
            set_record["comparison"]["provisional_period"]["outcome_mix"],
            {"pass": 1})


class RetainContentlessContainerTests(unittest.TestCase):
    """Ruling 166, R7-PRO-2 with Lead Engineer line E-11.

    The retain limb refuses a reason carrying no content in
    substance in whatever form the reason stands.
    """

    def _assert_refused(self, mod, reason):
        with self.assertRaises(ValueError) as caught:
            mod.dispose_demotion_flag("retain", reason=reason)
        self.assertEqual(str(caught.exception), "retain requires a reason")

    def test_deque_holding_no_content_refused(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, collections.deque([""]))
        self._assert_refused(mod, collections.deque([" "]))

    def test_generator_holding_no_content_refused(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, (item for item in ()))
        self._assert_refused(mod, (item for item in ("",)))

    def test_iterator_holding_no_content_refused(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, iter([]))
        self._assert_refused(mod, iter([""]))

    def test_userlist_holding_no_content_refused(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, collections.UserList([""]))
        self._assert_refused(mod, collections.UserList([" "]))

    def test_userstring_holding_no_content_refused(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, collections.UserString(" "))
        self._assert_refused(mod, collections.UserString(""))

    def test_range_of_zero_alone_refused(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, range(1))

    def test_array_holding_no_content_refused(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, array.array("b", b" "))
        self._assert_refused(mod, array.array("b", b""))

    def test_charged_contentless_forms_still_refused(self):
        mod = harness.require("ontoloop.promote")
        for reason in ("", " ", [], [""], {"detail": ""}, 0, None):
            self._assert_refused(mod, reason)
        with self.assertRaises(ValueError) as caught:
            mod.dispose_demotion_flag("retain")
        self.assertEqual(str(caught.exception), "retain requires a reason")

    def test_reasons_carrying_content_still_close(self):
        mod = harness.require("ontoloop.promote")
        for reason in ("evidence reviewed",
                       collections.deque(["evidence reviewed"]),
                       collections.UserList(["evidence reviewed"]),
                       collections.UserString("evidence reviewed"),
                       (item for item in ("evidence reviewed",)),
                       ["", "evidence reviewed"]):
            result = mod.dispose_demotion_flag("retain", reason=reason)
            self.assertEqual(result["record_form"], "retain")
            self.assertTrue(result["reason_recorded"])
            self.assertTrue(result["flag_closed"])
            self.assertTrue(result["age_stopped"])


class ConfirmFigureSubstanceTests(unittest.TestCase):
    """Ruling 167, the family 5 merged defect.

    Counted source names: R7-PRO-3, UC-R7-2, and Lead Engineer
    line E-9. confirm_provisional bars a comparison whose period
    figure positions carry no figure substance.
    """

    def _full_periods(self):
        provisional = {
            "outcome_mix": {"pass": 1},
            "correction_position": {"open": 1},
        }
        displaced = {
            "outcome_mix": {"pass": 1},
            "correction_position": {"open": 1},
            "standing": "last comparable period of the displaced bundle",
        }
        return provisional, displaced

    def _period_with_figures(self, outcome_mix, correction_position):
        return {
            "outcome_mix": outcome_mix,
            "correction_position": correction_position,
        }

    def _assert_barred(self, mod, comparison):
        result = mod.confirm_provisional({"comparison": comparison})
        self.assertEqual(result["outcome"], "barred", repr(comparison))
        self.assertEqual(
            result["bar_reason"],
            "no comparison in the provisional record")

    def test_figures_standing_as_none_barred(self):
        mod = harness.require("ontoloop.promote")
        period = self._period_with_figures(None, None)
        self._assert_barred(mod, {
            "provisional_period": period,
            "displaced_period": dict(period),
        })

    def test_figures_standing_as_empty_strings_barred(self):
        mod = harness.require("ontoloop.promote")
        period = self._period_with_figures("", "")
        self._assert_barred(mod, {
            "provisional_period": period,
            "displaced_period": dict(period),
        })

    def test_figures_standing_as_text_strings_barred(self):
        mod = harness.require("ontoloop.promote")
        period = self._period_with_figures("pass", "corrected")
        self._assert_barred(mod, {
            "provisional_period": period,
            "displaced_period": dict(period),
        })

    def test_figures_standing_as_integer_zero_barred(self):
        mod = harness.require("ontoloop.promote")
        period = self._period_with_figures(0, 0)
        self._assert_barred(mod, {
            "provisional_period": period,
            "displaced_period": dict(period),
        })

    def test_figures_standing_in_no_mapping_form_barred(self):
        mod = harness.require("ontoloop.promote")
        for figure in ([], False, True):
            period = self._period_with_figures(figure, figure)
            self._assert_barred(mod, {
                "provisional_period": period,
                "displaced_period": dict(period),
            })

    def test_one_figure_without_substance_beside_full_figures_barred(self):
        mod = harness.require("ontoloop.promote")
        provisional, displaced = self._full_periods()
        for comparison in (
            {"provisional_period": self._period_with_figures(
                None, {"open": 1}),
             "displaced_period": displaced},
            {"provisional_period": provisional,
             "displaced_period": self._period_with_figures(
                 {"pass": 1}, "")},
            {"provisional_period": self._period_with_figures(
                 {"pass": 1}, 0),
             "displaced_period": displaced},
            {"provisional_period": provisional,
             "displaced_period": self._period_with_figures(
                 None, None)},
        ):
            self._assert_barred(mod, comparison)

    def test_full_comparison_and_empty_mixes_still_confirm(self):
        mod = harness.require("ontoloop.promote")
        self.assertEqual(
            mod.confirm_provisional(mod.provisional_record())["outcome"],
            "confirmed")
        empty_mixes = mod.provisional_record(
            provisional_outcomes=[],
            displaced_outcomes=[],
            provisional_corrections=[],
            displaced_corrections=[])
        self.assertEqual(
            mod.confirm_provisional(empty_mixes)["outcome"], "confirmed")
        provisional, displaced = self._full_periods()
        ordered = {
            "provisional_period": collections.OrderedDict(provisional),
            "displaced_period": collections.OrderedDict(displaced),
        }
        self.assertEqual(
            mod.confirm_provisional({"comparison": ordered})["outcome"],
            "confirmed")

    def test_charged_no_period_forms_still_barred(self):
        mod = harness.require("ontoloop.promote")
        provisional, displaced = self._full_periods()
        for comparison in (
            {"provisional_period": None, "displaced_period": None},
            {"provisional_period": {}, "displaced_period": {}},
            {"provisional_period": None, "displaced_period": displaced},
            {"provisional_period": provisional, "displaced_period": {}},
        ):
            self._assert_barred(mod, comparison)


class ProvisionalUngovernedValueTests(unittest.TestCase):
    """Ruling 168, Lead Engineer line E-10.

    The four provisional sites meet a value in no iterable form
    and an unhashable value inside a list in the governed
    ValueError form.
    """

    def _assert_refused(self, mod, **override):
        with self.assertRaises(ValueError) as caught:
            mod.provisional_record(**_provisional_kwargs(**override))
        self.assertEqual(
            str(caught.exception),
            "provisional values must stand as a list of values")

    def test_integer_value_refused_at_each_site(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, provisional_outcomes=5)
        self._assert_refused(mod, displaced_outcomes=5)
        self._assert_refused(mod, provisional_corrections=5)
        self._assert_refused(mod, displaced_corrections=5)

    def test_list_holding_one_list_refused_at_each_site(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, provisional_outcomes=[["pass"]])
        self._assert_refused(mod, displaced_outcomes=[["pass"]])
        self._assert_refused(mod, provisional_corrections=[["open"]])
        self._assert_refused(mod, displaced_corrections=[["open"]])

    def test_charged_forms_still_refused_and_list_forms_compute(self):
        mod = harness.require("ontoloop.promote")
        for value in ("pass", b"pass", memoryview(b"pass"),
                      {"pass": 2, "fail": 1}):
            self._assert_refused(mod, provisional_outcomes=value)
        record = mod.provisional_record(**_provisional_kwargs())
        self.assertEqual(
            record["comparison"]["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})


if __name__ == "__main__":
    unittest.main()
