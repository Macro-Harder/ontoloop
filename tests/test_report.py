"""Slice REPORT tests, list section 2.16.

Rows transcribed from design/steps/step-09-merged-test-list.md section 2.16.
Perspective: whole path behaviour, evidence homes, records, and cross slice
effects. Each test body begins by requiring its product surface through the
shared harness, then states the real assertions from its row.
"""

import unittest

from tests import harness

FIGURES_16_62 = (
    "cannot judge rate",
    "not scored by cause rate",
    "cumulative spend per dataset version",
    "cumulative spend per workflow",
    "drop counts beside the scores",
    "outstanding quarantined count",
    "queue defect test results",
    "futility statement",
    "does not beat baseline verdict count",
    "attempts charged as completed evaluations count",
)


class ReportT01Tests(unittest.TestCase):
    """REPORT-T01: every figure recomputed from the journal by one act."""

    def test_figures_come_from_one_named_journal_state_by_one_act(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        self.assertTrue(report["journal_state_named"])
        self.assertEqual(report["construction_acts"], 1)
        self.assertEqual(report["counting_paths"], 1)
        for figure in report["figures"].values():
            self.assertEqual(figure["source"], report["journal_state"])

    def test_varied_journal_fixture_changes_the_figures(self):
        mod = harness.require("reporting")
        base = mod.build_loop_report()
        varied = mod.build_loop_report(journal="varied journal fixture")
        self.assertNotEqual(varied["figures"], base["figures"])
        self.assertEqual(varied["journal_state"], "varied journal fixture")


class ReportT02Tests(unittest.TestCase):
    """REPORT-T02: a reconstruction failure prints as a named defect."""

    def test_failure_prints_named_defect_in_the_same_view(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report(reconstruction_fails=True)
        self.assertTrue(report["defect_printed"])
        self.assertTrue(report["defect_name"])
        self.assertEqual(report["defect_view"], report["view"])

    def test_failure_is_never_a_blank_or_a_zero(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report(reconstruction_fails=True)
        self.assertNotEqual(report["printed_value"], "")
        self.assertNotEqual(report["printed_value"], 0)
        self.assertIsNotNone(report["printed_value"])


class ReportT03Tests(unittest.TestCase):
    """REPORT-T03: the report carries its full named contents in one view."""

    def test_scores_carry_their_holdout_named(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        for score in report["scores"]:
            self.assertTrue(score["holdout_named"])

    def test_stamps_claim_labels_and_ledger_counts_present(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        self.assertTrue(report["stamps"])
        self.assertTrue(report["claim_labels"])
        self.assertTrue(report["ledger_counts"])

    def test_leakage_limit_sentence_in_the_same_view_as_any_audit_result(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        self.assertIn("leakage limit sentence", report["view_contents"])
        if report["audit_results"]:
            self.assertEqual(report["leakage_limit_sentence_view"], report["view"])

    def test_override_and_disclosure_account_recomputed_from_the_journal(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        account = report["override_and_disclosure_account"]
        self.assertEqual(account["source"], "recomputed from the journal")
        self.assertFalse(account["carried_forward"])

    def test_precursor_line_for_the_current_dataset_version_only(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        lines = report["precursor_lines"]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["dataset_version"], report["current_dataset_version"])


class ReportT04Tests(unittest.TestCase):
    """REPORT-T04: the owing rule over the Simple, Advanced, and Agentic forms."""

    def test_missing_owed_form_is_a_defect_in_the_reporting_artifact_itself(self):
        mod = harness.require("reporting")
        for form in ("Simple", "Advanced", "Agentic"):
            built = mod.build_report_artifact(omit=form)
            self.assertTrue(built["form_owed"], form)
            self.assertTrue(built["defect"], form)
            self.assertEqual(built["defect_home"], "the reporting artifact itself", form)

    def test_all_owed_forms_present_passes(self):
        mod = harness.require("reporting")
        built = mod.build_report_artifact()
        self.assertFalse(built["defect"])
        self.assertEqual(sorted(built["forms_present"]), sorted(built["forms_owed"]))

    def test_value_equality_condition_from_subsection_18_55(self):
        mod = harness.require("reporting")
        built = mod.build_report_artifact(owed_form_value_differs=True)
        self.assertTrue(built["row_failed"])
        self.assertEqual(built["defect_home"], "the reporting artifact itself")


class ReportT05Tests(unittest.TestCase):
    """REPORT-T05: a refusal is readable from the loop report alone."""

    def test_simple_form_names_the_failed_condition_and_its_figures(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report(with_refusal=True)
        refusal = report["refusal"]
        self.assertEqual(refusal["form"], "Simple")
        self.assertTrue(refusal["failed_condition_named"])
        self.assertTrue(refusal["figures_present"])
        self.assertTrue(refusal["readable_from_report_alone"])


class ReportT06Tests(unittest.TestCase):
    """REPORT-T06: seal claim lint and fixed text travel lint over construction."""

    def test_both_lints_pass_over_report_construction(self):
        mod = harness.require("reporting")
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        self.assertEqual(result["assembly"], "report construction")


class ReportT07Tests(unittest.TestCase):
    """REPORT-T07: attention figures quoted with their cadences, both guessed."""

    def test_each_cadence_figure_is_quoted_with_its_cadence(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        quotes = report["attention_figures"]
        self.assertIn({"seconds_per_review": 35.6, "reviews_per_version": 100}, quotes)
        self.assertIn({"seconds_per_review": 72.0, "reviews_per_version": 30}, quotes)
        for quote in quotes:
            self.assertEqual(quote["source_class"], "guessed")

    def test_the_two_readings_and_their_totals_stand_distinct(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        readings = report["attention_readings"]
        self.assertEqual(readings["recorded"]["total_seconds_per_dataset_version"], 3560)
        self.assertEqual(readings["recorded"]["seconds_per_review"], 35.6)
        self.assertEqual(readings["sensitivity"]["total_seconds_per_dataset_version"], 2160)
        self.assertEqual(readings["sensitivity"]["seconds_per_review"], 72.0)

    def test_no_report_row_describes_the_attention_budget_as_satisfied(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report()
        self.assertNotIn("attention budget satisfied", report["all_wording"])
        for row in report["rows"]:
            self.assertFalse(row.get("describes_attention_budget_as_satisfied"))


class ReportT08Tests(unittest.TestCase):
    """REPORT-T08: fixed text travel lint over export, subsection 16.19."""

    def test_lint_passes_over_export(self):
        mod = harness.require("reporting")
        result = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(result["passed"])
        self.assertEqual(result["texts_checked"], 3)

    def test_paraphrase_of_any_verbatim_text_fails_the_lint(self):
        mod = harness.require("reporting")
        for text_name in ("seal sentence", "verify sentence", "grader awareness label"):
            result = mod.fixed_text_travel_lint(assembly="export", paraphrase_of=text_name)
            self.assertFalse(result["passed"], text_name)


class ReportT09Tests(unittest.TestCase):
    """REPORT-T09: every figure named at subsection 16.62 stands in its place."""

    def test_rate_figures_in_their_place(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report(journal="journal state exercising each named case")
        self.assertIn("cannot judge rate", report["figures_in_place"])
        self.assertIn("not scored by cause rate", report["figures_in_place"])

    def test_spend_drop_and_queue_figures_in_their_place(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report(journal="journal state exercising each named case")
        for name in ("cumulative spend per dataset version",
                     "cumulative spend per workflow",
                     "drop counts beside the scores",
                     "outstanding quarantined count",
                     "queue defect test results"):
            self.assertIn(name, report["figures_in_place"], name)
        drops = report["figures"]["drop counts beside the scores"]
        self.assertEqual(drops["placed_beside"], "scores")

    def test_futility_statement_where_a_budget_is_exhausted_with_no_promotion(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report(journal="journal state exercising each named case")
        self.assertIn("futility statement", report["figures_in_place"])
        exhausted = [v for v in report["views"] if v["budget_exhausted"] and not v["promotion"]]
        for view in exhausted:
            self.assertTrue(view["futility_statement_printed"])

    def test_promotion_side_counts_beside_a_successful_promotion_score(self):
        mod = harness.require("reporting")
        report = mod.build_loop_report(journal="journal state exercising each named case")
        promoted = [v for v in report["views"] if v["promotion_succeeded"]]
        self.assertTrue(promoted)
        for view in promoted:
            self.assertIn("does not beat baseline verdict count", view["figures_beside_score"])
            self.assertIn("attempts charged as completed evaluations count", view["figures_beside_score"])

    def test_omitting_any_named_figure_fails_the_row(self):
        mod = harness.require("reporting")
        for name in FIGURES_16_62:
            report = mod.build_loop_report(
                journal="journal state exercising each named case", omit_figure=name)
            self.assertTrue(report["row_failed"], name)


class ReportT10Tests(unittest.TestCase):
    """REPORT-T10: pointer row for the REDACT-T08 call point at REPORT."""

    def test_pointer_names_the_central_row_and_states_no_second_wording(self):
        mod = harness.require("reporting")
        pointer = mod.redact_t08_call_point("REPORT")
        self.assertEqual(pointer["central_row"], "REDACT-T08")
        self.assertEqual(pointer["pass_condition_home"], "REDACT-T08")
        self.assertFalse(pointer["states_second_wording_of_behaviour"])

    def test_report_for_weakened_material_carries_the_per_build_flag(self):
        mod = harness.require("reporting")
        build = mod.dataset_build_including_weakened_ingest()
        report = mod.build_loop_report(for_build=build)
        self.assertTrue(report["per_build_flag"])
        self.assertEqual(report["flag_view"], report["build_view"])

    def test_report_with_no_weakened_material_carries_no_flag(self):
        mod = harness.require("reporting")
        build = mod.dataset_build_without_weakened_ingest()
        report = mod.build_loop_report(for_build=build)
        self.assertFalse(report["per_build_flag"])


if __name__ == "__main__":
    unittest.main()
