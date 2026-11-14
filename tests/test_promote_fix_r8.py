"""Fix round 8 pins for the PROMOTE scope, Region 4.

Written test first for triage rulings 218 and 219 at
design/steps/step-15-r8-triage.md. Ruling 218 counts R8-PRO-1
and Lead Engineer line E-9 in that act and nowhere else.
Ruling 219 counts Lead Engineer line E-8 in that act.
"""

import unittest

from tests import harness


def _nested(value, depth):
    result = value
    for _ in range(depth):
        result = [result]
    return result


class RetainCyclicAndDeepReasonTests(unittest.TestCase):
    """Ruling 218: cyclic or deeply nested retain reasons."""

    def _assert_refused(self, mod, reason):
        with self.assertRaises(ValueError) as caught:
            mod.dispose_demotion_flag("retain", reason=reason)
        self.assertEqual(str(caught.exception), "retain requires a reason")

    def test_self_holding_list_refused_in_governed_form(self):
        mod = harness.require("ontoloop.promote")
        reason = []
        reason.append(reason)
        self._assert_refused(mod, reason)

    def test_self_holding_mapping_refused_in_governed_form(self):
        mod = harness.require("ontoloop.promote")
        reason = {}
        reason["detail"] = reason
        self._assert_refused(mod, reason)

    def test_list_holding_empty_string_beside_itself_refused(self):
        mod = harness.require("ontoloop.promote")
        reason = [""]
        reason.append(reason)
        self._assert_refused(mod, reason)

    def test_deeply_nested_space_only_reason_refused(self):
        mod = harness.require("ontoloop.promote")
        self._assert_refused(mod, _nested(" ", 500))

    def test_deeply_nested_stated_text_closes_without_recursion_error(self):
        mod = harness.require("ontoloop.promote")
        result = mod.dispose_demotion_flag(
            "retain", reason=_nested("evidence reviewed", 500))
        self.assertEqual(result["record_form"], "retain")
        self.assertTrue(result["reason_recorded"])
        self.assertTrue(result["flag_closed"])
        self.assertTrue(result["age_stopped"])

    def test_charged_contentless_and_closing_forms_still_decide(self):
        mod = harness.require("ontoloop.promote")
        for reason in ("", " ", [], [""], {"detail": ""}, 0, None):
            self._assert_refused(mod, reason)
        with self.assertRaises(ValueError) as caught:
            mod.dispose_demotion_flag("retain")
        self.assertEqual(str(caught.exception), "retain requires a reason")
        result = mod.dispose_demotion_flag(
            "retain", reason="evidence reviewed")
        self.assertEqual(result["record_form"], "retain")
        self.assertTrue(result["flag_closed"])


class ConfirmFigureCountSubstanceTests(unittest.TestCase):
    """Ruling 219: count substance inside a figure mapping."""

    def _period(self, figure):
        return {
            "outcome_mix": figure,
            "correction_position": figure,
        }

    def _record(self, provisional_figure, displaced_figure=None):
        if displaced_figure is None:
            displaced_figure = provisional_figure
        return {"comparison": {
            "provisional_period": self._period(provisional_figure),
            "displaced_period": self._period(displaced_figure),
        }}

    def _assert_barred(self, mod, record):
        result = mod.confirm_provisional(record)
        self.assertEqual(result["outcome"], "barred", repr(record))
        self.assertEqual(
            result["bar_reason"],
            "no comparison in the provisional record")

    def _assert_confirmed(self, mod, record):
        result = mod.confirm_provisional(record)
        self.assertEqual(result["outcome"], "confirmed", repr(record))
        self.assertNotIn("bar_reason", result)

    def test_figures_carrying_count_as_none_barred(self):
        mod = harness.require("ontoloop.promote")
        self._assert_barred(mod, self._record({"pass": None}))

    def test_figures_carrying_count_as_text_barred(self):
        mod = harness.require("ontoloop.promote")
        self._assert_barred(mod, self._record({"pass": "one"}))

    def test_figures_carrying_zero_counts_throughout_barred(self):
        mod = harness.require("ontoloop.promote")
        self._assert_barred(mod, self._record({"pass": 0}))
        self._assert_barred(mod, self._record({"pass": 0, "fail": 0}))

    def test_one_figure_without_count_substance_beside_full_barred(self):
        mod = harness.require("ontoloop.promote")
        full = {"pass": 1}
        record = {"comparison": {
            "provisional_period": self._period({"pass": None}),
            "displaced_period": self._period(full),
        }}
        self._assert_barred(mod, record)

    def test_full_and_empty_mixes_and_mixed_counts_still_confirm(self):
        mod = harness.require("ontoloop.promote")
        self._assert_confirmed(mod, self._record({"pass": 1}))
        self._assert_confirmed(
            mod, self._record({"pass": 1, "fail": 0}))
        self._assert_confirmed(
            mod, mod.provisional_record())
        empty_mixes = mod.provisional_record(
            provisional_outcomes=[],
            displaced_outcomes=[],
            provisional_corrections=[],
            displaced_corrections=[])
        self._assert_confirmed(mod, empty_mixes)

    def test_charged_no_figure_forms_still_barred(self):
        mod = harness.require("ontoloop.promote")
        for figure in (None, "", "pass", [], 0, False, True):
            self._assert_barred(mod, self._record(figure))


if __name__ == "__main__":
    unittest.main()
