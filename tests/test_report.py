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
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        self.assertTrue(report["journal_state_named"])
        self.assertEqual(report["construction_acts"], 1)
        self.assertEqual(report["counting_paths"], 1)
        for figure in report["figures"].values():
            self.assertEqual(figure["source"], report["journal_state"])

    def test_varied_journal_fixture_changes_the_figures(self):
        mod = harness.require("ontoloop.report")
        base = mod.build_loop_report()
        varied = mod.build_loop_report(journal="varied journal fixture")
        self.assertNotEqual(varied["figures"], base["figures"])
        self.assertEqual(varied["journal_state"], "varied journal fixture")


class ReportT02Tests(unittest.TestCase):
    """REPORT-T02: a reconstruction failure prints as a named defect."""

    def test_failure_prints_named_defect_in_the_same_view(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report(reconstruction_fails=True)
        self.assertTrue(report["defect_printed"])
        self.assertTrue(report["defect_name"])
        self.assertEqual(report["defect_view"], report["view"])

    def test_failure_is_never_a_blank_or_a_zero(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report(reconstruction_fails=True)
        self.assertNotEqual(report["printed_value"], "")
        self.assertNotEqual(report["printed_value"], 0)
        self.assertIsNotNone(report["printed_value"])


class ReportT03Tests(unittest.TestCase):
    """REPORT-T03: the report carries its full named contents in one view."""

    def test_scores_carry_their_holdout_named(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        for score in report["scores"]:
            self.assertTrue(score["holdout_named"])

    def test_stamps_claim_labels_and_ledger_counts_present(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        self.assertTrue(report["stamps"])
        self.assertTrue(report["claim_labels"])
        self.assertTrue(report["ledger_counts"])

    def test_leakage_limit_sentence_in_the_same_view_as_any_audit_result(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        self.assertIn("leakage limit sentence", report["view_contents"])
        if report["audit_results"]:
            self.assertEqual(report["leakage_limit_sentence_view"], report["view"])

    def test_override_and_disclosure_account_recomputed_from_the_journal(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        account = report["override_and_disclosure_account"]
        self.assertEqual(account["source"], "recomputed from the journal")
        self.assertFalse(account["carried_forward"])

    def test_precursor_line_for_the_current_dataset_version_only(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        lines = report["precursor_lines"]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["dataset_version"], report["current_dataset_version"])


class ReportT04Tests(unittest.TestCase):
    """REPORT-T04: the owing rule over the Simple, Advanced, and Agentic forms."""

    def test_missing_owed_form_is_a_defect_in_the_reporting_artifact_itself(self):
        mod = harness.require("ontoloop.report")
        for form in ("Simple", "Advanced", "Agentic"):
            built = mod.build_report_artifact(omit=form)
            self.assertTrue(built["form_owed"], form)
            self.assertTrue(built["defect"], form)
            self.assertEqual(built["defect_home"], "the reporting artifact itself", form)

    def test_all_owed_forms_present_passes(self):
        mod = harness.require("ontoloop.report")
        built = mod.build_report_artifact()
        self.assertFalse(built["defect"])
        self.assertEqual(sorted(built["forms_present"]), sorted(built["forms_owed"]))

    def test_value_equality_condition_from_subsection_18_55(self):
        mod = harness.require("ontoloop.report")
        built = mod.build_report_artifact(owed_form_value_differs=True)
        self.assertTrue(built["row_failed"])
        self.assertEqual(built["defect_home"], "the reporting artifact itself")


class ReportT05Tests(unittest.TestCase):
    """REPORT-T05: a refusal is readable from the loop report alone."""

    def test_simple_form_names_the_failed_condition_and_its_figures(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report(with_refusal=True)
        refusal = report["refusal"]
        self.assertEqual(refusal["form"], "Simple")
        self.assertTrue(refusal["failed_condition_named"])
        self.assertTrue(refusal["figures_present"])
        self.assertTrue(refusal["readable_from_report_alone"])


class ReportT06Tests(unittest.TestCase):
    """REPORT-T06: seal claim lint and fixed text travel lint over construction."""

    def test_both_lints_pass_over_report_construction(self):
        mod = harness.require("ontoloop.report")
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        self.assertEqual(result["assembly"], "report construction")


class ReportT07Tests(unittest.TestCase):
    """REPORT-T07: attention figures quoted with their cadences, both guessed."""

    def test_each_cadence_figure_is_quoted_with_its_cadence(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        quotes = report["attention_figures"]
        self.assertIn({"seconds_per_review": 35.6, "reviews_per_version": 100}, quotes)
        self.assertIn({"seconds_per_review": 72.0, "reviews_per_version": 30}, quotes)
        for quote in quotes:
            self.assertEqual(quote["source_class"], "guessed")

    def test_the_two_readings_and_their_totals_stand_distinct(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        readings = report["attention_readings"]
        self.assertEqual(readings["recorded"]["total_seconds_per_dataset_version"], 3560)
        self.assertEqual(readings["recorded"]["seconds_per_review"], 35.6)
        self.assertEqual(readings["sensitivity"]["total_seconds_per_dataset_version"], 2160)
        self.assertEqual(readings["sensitivity"]["seconds_per_review"], 72.0)

    def test_no_report_row_describes_the_attention_budget_as_satisfied(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report()
        self.assertNotIn("attention budget satisfied", report["all_wording"])
        for row in report["rows"]:
            self.assertFalse(row.get("describes_attention_budget_as_satisfied"))


class ReportT08Tests(unittest.TestCase):
    """REPORT-T08: fixed text travel lint over export, subsection 16.19."""

    def test_lint_passes_over_export(self):
        mod = harness.require("ontoloop.report")
        result = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(result["passed"])
        self.assertEqual(result["texts_checked"], 3)

    def test_paraphrase_of_any_verbatim_text_fails_the_lint(self):
        mod = harness.require("ontoloop.report")
        for text_name in ("seal sentence", "verify sentence", "grader awareness label"):
            result = mod.fixed_text_travel_lint(assembly="export", paraphrase_of=text_name)
            self.assertFalse(result["passed"], text_name)


class ReportT09Tests(unittest.TestCase):
    """REPORT-T09: every figure named at subsection 16.62 stands in its place."""

    def test_rate_figures_in_their_place(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report(journal="journal state exercising each named case")
        self.assertIn("cannot judge rate", report["figures_in_place"])
        self.assertIn("not scored by cause rate", report["figures_in_place"])

    def test_spend_drop_and_queue_figures_in_their_place(self):
        mod = harness.require("ontoloop.report")
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
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report(journal="journal state exercising each named case")
        self.assertIn("futility statement", report["figures_in_place"])
        exhausted = [v for v in report["views"] if v["budget_exhausted"] and not v["promotion"]]
        for view in exhausted:
            self.assertTrue(view["futility_statement_printed"])

    def test_promotion_side_counts_beside_a_successful_promotion_score(self):
        mod = harness.require("ontoloop.report")
        report = mod.build_loop_report(journal="journal state exercising each named case")
        promoted = [v for v in report["views"] if v["promotion_succeeded"]]
        self.assertTrue(promoted)
        for view in promoted:
            self.assertIn("does not beat baseline verdict count", view["figures_beside_score"])
            self.assertIn("attempts charged as completed evaluations count", view["figures_beside_score"])

    def test_omitting_any_named_figure_fails_the_row(self):
        mod = harness.require("ontoloop.report")
        for name in FIGURES_16_62:
            report = mod.build_loop_report(
                journal="journal state exercising each named case", omit_figure=name)
            self.assertTrue(report["row_failed"], name)


class ReportT10Tests(unittest.TestCase):
    """REPORT-T10: pointer row for the REDACT-T08 call point at REPORT."""

    def test_pointer_names_the_central_row_and_states_no_second_wording(self):
        mod = harness.require("ontoloop.report")
        pointer = mod.redact_t08_call_point("REPORT")
        self.assertEqual(pointer["central_row"], "REDACT-T08")
        self.assertEqual(pointer["pass_condition_home"], "REDACT-T08")
        self.assertFalse(pointer["states_second_wording_of_behaviour"])

    def test_report_for_weakened_material_carries_the_per_build_flag(self):
        mod = harness.require("ontoloop.report")
        build = mod.dataset_build_including_weakened_ingest()
        report = mod.build_loop_report(for_build=build)
        self.assertTrue(report["per_build_flag"])
        self.assertEqual(report["flag_view"], report["build_view"])

    def test_report_with_no_weakened_material_carries_no_flag(self):
        mod = harness.require("ontoloop.report")
        build = mod.dataset_build_without_weakened_ingest()
        report = mod.build_loop_report(for_build=build)
        self.assertFalse(report["per_build_flag"])


class ReportLintScanDepthFixR2Tests(unittest.TestCase):
    """Fix round 2, CL-16: whole form travel and seal claim judgement.

    The three tests stand in the exact three part form triage
    ruling 3 states: the paraphrased surface, an unconditional
    seal claim in wording outside the three listed phrases, and
    the standing clean assemblies beside a listed phrase.
    """

    def test_paraphrased_surface_fails_the_travel_lint(self):
        import json

        from ontoloop import sealing

        mod = harness.require("ontoloop.report")
        surface = sealing.paraphrased_surface()
        sealing_result = sealing.travel_lint(surface)
        self.assertFalse(sealing_result["passed"])
        result = mod.fixed_text_travel_lint(
            assembly="export", content=json.dumps(surface))
        self.assertFalse(result["passed"])

    def test_unconditional_seal_claim_outside_listed_phrases_fails(self):
        mod = harness.require("ontoloop.report")
        original = mod.build_loop_report

        def carrying_claim(**kwargs):
            built = original(**kwargs)
            built["all_wording"] = (
                "the seal binds all actors unconditionally "
                "and the confinement of every surface stands "
                "assured in every case"
            )
            return built

        mod.build_loop_report = carrying_claim
        try:
            result = mod.lint_report_construction()
            travel = mod.fixed_text_travel_lint(assembly="export")
        finally:
            mod.build_loop_report = original
        self.assertFalse(result["seal_claim_lint_passed"])
        self.assertFalse(result["fixed_text_travel_lint_passed"])
        self.assertFalse(travel["passed"])

    def test_clean_assemblies_pass_and_listed_phrase_still_fails(self):
        mod = harness.require("ontoloop.report")
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])
        original = mod.build_loop_report

        def carrying_phrase(**kwargs):
            built = original(**kwargs)
            built["all_wording"] = "seal verified"
            return built

        mod.build_loop_report = carrying_phrase
        try:
            listed = mod.lint_report_construction()
        finally:
            mod.build_loop_report = original
        self.assertFalse(listed["seal_claim_lint_passed"])


class ProductionReportFormFixR2Tests(unittest.TestCase):
    """Fix round 2, triage ruling 6: the production report form.

    This class is the form test charged as the first act of the
    report region in Fix round 2. It discharges the P-20 test
    position at cluster CL-R2-3 only: no criterion 6 position,
    no F6 reservation, and no part of S15-R1-093 stands
    discharged by it, and no populated store position stands
    claimed by it. It pins the form on material passed directly
    to the surface.
    """

    def test_form_stands_labelled_beside_the_commitment(self):
        mod = harness.require("ontoloop.report")
        form = mod.production_report_form()
        self.assertEqual(form["form"], "production")
        self.assertEqual(form["label"], "production report form")
        self.assertTrue(form["beside_specification_commitment"])
        self.assertFalse(form["merged_into_specification_commitment"])
        commitment = form["specification_commitment"]
        self.assertEqual(commitment["form"], "minimum")
        self.assertEqual(commitment["count"], 30)
        self.assertNotEqual(commitment["evidence"], form["evidence"])

    def test_counts_computed_from_the_material_passed(self):
        mod = harness.require("ontoloop.report")
        pairs = {"kind a": [1, 2, 3], "kind b": [1]}
        records = [
            {"shape": "shape one", "family": "family one"},
            {"shape": "shape one", "family": "family two"},
            {"shape": "shape two", "family": "family one"},
        ]
        form = mod.production_report_form(
            produced_pairs=pairs, produced_records=records)
        counts = form["production_counts"]
        self.assertEqual(counts["per_kind"], {"kind a": 3, "kind b": 1})
        self.assertEqual(
            counts["per_shape"], {"shape one": 2, "shape two": 1})
        self.assertEqual(
            counts["per_family"], {"family one": 2, "family two": 1})
        self.assertTrue(form["counts_present"])

    def test_counts_vary_with_differing_material_passed(self):
        mod = harness.require("ontoloop.report")
        first = mod.production_report_form(
            produced_pairs={"kind a": [1]},
            produced_records=[{"shape": "s1", "family": "f1"}])
        second = mod.production_report_form(
            produced_pairs={"kind a": [1, 2], "kind c": [1, 2, 3, 4]},
            produced_records=[
                {"shape": "s2", "family": "f1"},
                {"shape": "s2", "family": "f3"},
            ])
        self.assertNotEqual(
            first["production_counts"], second["production_counts"])
        self.assertEqual(
            second["production_counts"]["per_kind"],
            {"kind a": 2, "kind c": 4})
        self.assertEqual(
            second["production_counts"]["per_shape"], {"s2": 2})
        self.assertEqual(
            second["production_counts"]["per_family"],
            {"f1": 1, "f3": 1})

    def test_no_material_passed_claims_no_production_count(self):
        mod = harness.require("ontoloop.report")
        form = mod.production_report_form()
        counts = form["production_counts"]
        self.assertEqual(counts["per_kind"], {})
        self.assertEqual(counts["per_shape"], {})
        self.assertEqual(counts["per_family"], {})
        self.assertFalse(form["counts_present"])


class SealClaimScanSubstanceFixR3Tests(unittest.TestCase):
    """Fix round 3, S15-R3-018: the seal claim judgement in substance.

    A statement counts as a claim statement where it states a
    seal, verify, or confinement claim in substance, beyond the
    listed subject words. A conditional or negated marker
    excuses a claim only where it governs that claim, so a
    compound statement joining an unconditional claim clause
    to an unrelated conditional or negated clause fails on the
    claim clause, as the same clause standing alone fails.
    """

    OUTSIDE_WORDING = (
        "Agents are confined.",
        "Exposure is controlled at all times.",
        "Record integrity stands guaranteed for every store.",
        "Each envelope is tamper proof.",
        "Every record stands attested before use.",
        "Authenticity of each entry stands certified.",
    )

    def test_claims_outside_the_subject_list_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.OUTSIDE_WORDING:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_compound_statement_fails_as_the_claim_clause_alone_fails(self):
        mod = harness.require("ontoloop.report")
        control = "The seal guarantees protection."
        compounds = (
            "The seal guarantees protection and does not expire.",
            "The seal guarantees protection and the schedule "
            "is conditional on the weather.",
        )
        self.assertFalse(mod._seal_claim_scan(control))
        for statement in compounds:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_governed_forms_and_clean_assemblies_still_pass(self):
        mod = harness.require("ontoloop.report")
        governed = (
            "The seal stands conditional on signing "
            "at signed strength only.",
            "The seal guarantees protection conditional on "
            "the deployment confinement fact.",
            "Records stand attested conditional on "
            "the deployment confinement fact.",
            "Record integrity stands guaranteed conditional on "
            "the deployment confinement fact.",
            "The seal does not guarantee protection.",
        )
        for statement in governed:
            self.assertTrue(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertTrue(result["passed"], statement)
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanSigningAnchoringFixR4Tests(unittest.TestCase):
    """Fix round 4, N-01, ruling 19: signing and anchoring claims.

    The claim judgement reaches signing and anchoring claim
    clauses in substance, so an unconditional statement that a
    bundle or a head stands signed or anchored fails the scan,
    in the same clause governing form as the standing families:
    a conditional or negated marker excuses such a clause only
    where it governs that clause. The governed signed strength
    forms and the standing clean assemblies still pass.
    """

    UNCONDITIONAL = (
        "The bundle stands signed for every actor.",
        "Every bundle is anchored unconditionally.",
        "The bundle was signed and anchored in all cases.",
        "The journal head stands signed under the signing key "
        "at all times.",
        "Signing is guaranteed for every bundle.",
    )

    def test_unconditional_signed_and_anchored_statements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.UNCONDITIONAL:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_governed_signed_forms_and_clean_assemblies_pass(self):
        mod = harness.require("ontoloop.report")
        governed = (
            "Heads are signed at signed strength only.",
            "The bundle stands signed conditional on "
            "the deployment confinement fact.",
            "The bundle does not stand signed.",
        )
        for statement in governed:
            self.assertTrue(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertTrue(result["passed"], statement)
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanSubordinateFixR4Tests(unittest.TestCase):
    """Fix round 4, N-02, ruling 20: the marker governing test.

    A conditional or negated marker excuses a claim clause
    only where it governs that claim clause itself. A marker
    standing inside a subordinate clause, a parenthetical, or
    a colon joined clause, speaking of expiry or of the
    weather, excuses nothing, and a fragment clause that
    conditions nothing, the Lead Engineer B-1 noun phrase
    fragment form, counted in this act and nowhere else,
    excuses nothing. A fragment that genuinely conditions
    the claim, and the standing governed forms, still pass.
    """

    DEFEATED = (
        "The seal guarantees protection that does not expire.",
        "The seal guarantees protection while the policy "
        "does not expire.",
        "The seal guarantees protection that is conditional "
        "on the weather.",
        "The seal guarantees protection when the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection (the schedule is "
        "conditional on the weather).",
        "The seal guarantees protection: the schedule is "
        "conditional on the weather.",
        "The seal guarantees protection, the conditional on "
        "the deployment confinement fact poster on the wall.",
    )

    def test_subordinate_parenthetical_colon_and_fragment_fail(self):
        mod = harness.require("ontoloop.report")
        control = "The seal guarantees protection."
        self.assertFalse(mod._seal_claim_scan(control))
        for statement in self.DEFEATED:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_genuine_fragment_and_governed_forms_still_pass(self):
        mod = harness.require("ontoloop.report")
        governed = (
            "The seal guarantees protection, conditional on "
            "the deployment confinement fact.",
            "The seal guarantees protection conditional on "
            "the deployment confinement fact.",
            "The seal stands conditional on signing "
            "at signed strength only.",
            "The seal does not guarantee protection.",
        )
        for statement in governed:
            self.assertTrue(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertTrue(result["passed"], statement)
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanLexiconFixR4Tests(unittest.TestCase):
    """Fix round 4, N-05, ruling 23: the claim lexicon reach.

    The claim judgement reaches claim statements in the
    alteration, shielding, unalterable, impenetrable, and
    watertight wordings, as claim statements in substance
    in the charged families. The standing seal sentence
    and the governed verify sentence, whose alteration
    wording stands under its governing exception and its
    signed strength condition, still pass, as do the
    governed conditional and negated claims and the
    standing clean assemblies.
    """

    OUTSIDE_WORDING = (
        "Records cannot be altered after writing.",
        "Every record is shielded from alteration.",
        "Journal entries are unalterable.",
        "The journal is impenetrable to outside writers.",
        "The store is watertight against outside writers.",
        "The store is impregnable.",
    )

    def test_alteration_family_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.OUTSIDE_WORDING:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_governed_forms_and_clean_assemblies_still_pass(self):
        from ontoloop import sealing

        mod = harness.require("ontoloop.report")
        governed = (
            "Records stand attested conditional on "
            "the deployment confinement fact.",
            "The seal does not guarantee protection.",
            "The seal stands conditional on signing "
            "at signed strength only.",
        )
        for statement in governed:
            self.assertTrue(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertTrue(result["passed"], statement)
        self.assertTrue(mod._seal_claim_scan(sealing.VERIFY_SENTENCE))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanGoverningReachFixR5Tests(unittest.TestCase):
    """Fix round 5, N-03, ruling 40: the marker governing reach.

    A conditional or negated marker excuses a claim clause only
    where it governs that claim clause, in whatever clause form
    the marker stands in. Markers standing in subordinate clauses
    opened by the probed introducers outside the standing list,
    and in clauses the standing splitting never separates, excuse
    nothing, and a fragment conditioning the claim on an unrelated
    subject, the weather and the postman forms of Lead Engineer
    lines C-1 and C-2, counted in this act and nowhere else,
    beside confinement Findings 1 and 2, counted in this act and
    nowhere else, excuses nothing. The claim clause standing
    alone fails, and every governed, conditional, negated, and
    genuine fragment form that stands passing still passes.
    """

    INTRODUCER_FORMS = (
        "The seal guarantees protection if the policy "
        "does not expire.",
        "The seal guarantees protection if the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection unless the policy "
        "does not expire.",
        "The seal guarantees protection until the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection after the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection once the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection provided the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection whether the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection as the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection before the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection whenever the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection wherever the policy "
        "does not expire.",
        "The seal guarantees protection in case the schedule "
        "is conditional on the weather.",
        "Records stand signed if the schedule is conditional "
        "on the weather.",
    )

    SEPARATOR_FORMS = (
        "The seal guarantees protection or the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection alongside a schedule "
        "conditional on the weather.",
        "The seal guarantees protection [the schedule is "
        "conditional on the weather].",
        "The seal guarantees protection - the schedule is "
        "conditional on the weather.",
        "The seal guarantees protection! The schedule is "
        "conditional on the weather.",
        "The seal guarantees protection? The schedule is "
        "conditional on the weather.",
        "The seal guarantees protection or does not expire.",
        "The seal guarantees protection nor the schedule "
        "is conditional on the weather.",
        "The seal guarantees protection / the schedule is "
        "conditional on the weather.",
    )

    FRAGMENT_FORMS = (
        "The seal guarantees protection, conditional on "
        "the weather.",
        "The seal guarantees protection, conditional on "
        "the postman arriving.",
    )

    def test_introducer_forms_fail(self):
        mod = harness.require("ontoloop.report")
        control = "The seal guarantees protection."
        self.assertFalse(mod._seal_claim_scan(control))
        for statement in self.INTRODUCER_FORMS:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_separator_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.SEPARATOR_FORMS:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_unrelated_fragment_conditions_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FRAGMENT_FORMS:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_governed_forms_and_clean_assemblies_still_pass(self):
        from ontoloop import sealing

        mod = harness.require("ontoloop.report")
        governed = (
            "The seal guarantees protection, conditional on "
            "the deployment confinement fact.",
            "The seal guarantees protection conditional on "
            "the deployment confinement fact.",
            "The seal stands conditional on signing "
            "at signed strength only.",
            "The seal does not guarantee protection.",
            "Heads are signed at signed strength only.",
            "The bundle stands signed conditional on "
            "the deployment confinement fact.",
            "The bundle does not stand signed.",
        )
        for statement in governed:
            self.assertTrue(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertTrue(result["passed"], statement)
        self.assertTrue(mod._seal_claim_scan(sealing.VERIFY_SENTENCE))
        texts = sealing.verbatim_texts()
        self.assertTrue(mod._seal_claim_scan(texts["seal sentence"]))
        self.assertTrue(
            mod._seal_claim_scan(texts["grader awareness label"]))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanInabilityFixR5Tests(unittest.TestCase):
    """Fix round 5, N-26, ruling 63: the inability reading.

    The inability reading covers a cannot claim in substance:
    a statement that a governed thing cannot be acted on in a
    claim family, and not only the two followers the landed
    limb names. The tampered and broken followers, and the
    ever and never forms of confinement Finding 4, counted in
    this act and nowhere else, stand judged as claims beside
    the charged altered form, while the standing negated
    claims still pass.
    """

    INABILITY_FORMS = (
        "Records cannot be tampered with after writing.",
        "Entries cannot be tampered with by anyone.",
        "The seal cannot be broken by outside writers.",
        "Records cannot ever be altered after writing.",
        "Records can never be altered after writing.",
        "Records cannot be altered after writing.",
    )

    def test_inability_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.INABILITY_FORMS:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_negated_claims_and_clean_assemblies_still_pass(self):
        from ontoloop import sealing

        mod = harness.require("ontoloop.report")
        governed = (
            "The seal does not guarantee protection.",
            "The bundle does not stand signed.",
            "The seal stands conditional on signing "
            "at signed strength only.",
        )
        for statement in governed:
            self.assertTrue(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertTrue(result["passed"], statement)
        texts = sealing.verbatim_texts()
        self.assertTrue(
            mod._seal_claim_scan(texts["grader awareness label"]))
        self.assertTrue(mod._seal_claim_scan(sealing.VERIFY_SENTENCE))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanLexiconReachFixR5Tests(unittest.TestCase):
    """Fix round 5, N-27, ruling 64: the claim lexicon reach.

    The claim judgement reaches the probed lexicon wordings
    of the entering papers, across the alteration, sealing
    and confinement, and verification and signing families,
    with confinement Finding 3 and the sealing, confinement,
    and signing wordings of Lead Engineer line C-3 counted in
    this act and nowhere else. Each wording stands judged as
    a claim in claim form, beside the protect and authentic
    controls and every standing governed form unchanged.
    """

    PROBED_WORDINGS = (
        "Records cannot be changed after writing.",
        "Records cannot be modified after writing.",
        "Records cannot be rewritten after writing.",
        "Journal entries are unchangeable.",
        "Journal entries are immutable.",
        "The journal is change proof against outside writers.",
        "The journal is secure against outside writers.",
        "The system keeps everything locked down forever.",
        "Access is impossible for outsiders.",
        "The store is airtight against outside writers.",
        "The store is hermetic against outside writers.",
        "The store is water-tight against outside writers.",
        "No data leaves the store.",
        "Nothing escapes the store.",
        "Outgoing traffic is blocked at all times.",
        "Every record stands confirmed before use.",
        "Every record stands checked before use.",
        "The bundle stands countersigned for every actor.",
        "The bundle stands resealed for every actor.",
        "Heads are endorsed for every actor.",
        "The journal is immutable.",
        "Records stand immutable after writing.",
        "The journal is inviolable.",
        "The store resists penetration by outside writers.",
        "Records are immune to outside writers.",
        "Records are unbreachable.",
        "The journal head stands notarised for every bundle.",
    )

    CONTROLS_ALREADY_FAILING = (
        "Every record is protected from change.",
        "Authenticity of each entry stands proven.",
    )

    def test_probed_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED_WORDINGS:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_controls_and_governed_forms_unchanged(self):
        from ontoloop import sealing

        mod = harness.require("ontoloop.report")
        for statement in self.CONTROLS_ALREADY_FAILING:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
        governed = (
            "Records stand attested conditional on "
            "the deployment confinement fact.",
            "The seal does not guarantee protection.",
            "The seal stands conditional on signing "
            "at signed strength only.",
            "The bundle does not stand signed.",
        )
        for statement in governed:
            self.assertTrue(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertTrue(result["passed"], statement)
        self.assertTrue(mod._seal_claim_scan(sealing.VERIFY_SENTENCE))
        texts = sealing.verbatim_texts()
        self.assertTrue(mod._seal_claim_scan(texts["seal sentence"]))
        self.assertTrue(
            mod._seal_claim_scan(texts["grader awareness label"]))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanAssertedVerbsFixR5Tests(unittest.TestCase):
    """Fix round 5, N-28, ruling 65: the asserted form reach.

    The asserted form reading reaches the probed verb forms:
    a judged concept with one of those verbs states a claim
    and is judged, beside the holds control. The standing
    fragment boundary the module states still holds: a
    fragment carrying a concept word in a label or a name,
    with no asserted form of any kind, states no claim.
    """

    PROBED_VERBS = (
        "The journal offers integrity to every reader.",
        "The archive affords integrity to every reader.",
        "The journal grants integrity to every reader.",
    )

    def test_probed_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        control = "The journal holds integrity for every reader."
        self.assertFalse(mod._seal_claim_scan(control))
        for statement in self.PROBED_VERBS:
            self.assertFalse(mod._seal_claim_scan(statement), statement)
            result = mod.fixed_text_travel_lint(
                assembly="export", content=statement)
            self.assertFalse(result["passed"], statement)

    def test_fragment_boundary_and_clean_assemblies_hold(self):
        mod = harness.require("ontoloop.report")
        fragment = "Integrity label for the journal schedule."
        self.assertTrue(mod._seal_claim_scan(fragment))
        result = mod.fixed_text_travel_lint(
            assembly="export", content=fragment)
        self.assertTrue(result["passed"])
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class ProductionReportFormPairsFixR5Tests(unittest.TestCase):
    """Fix round 5, N-45, ruling 82: the pairs value form.

    production_report_form checks its pairs value as a list
    of pairs: a string value no longer counts by characters
    and counts_present no longer stands True on it, and the
    integer and float forms beside it return the governed
    form of the surface for a malformed pairs value, no
    count stated for pairs never presented and no exception,
    beside the genuine pair list still counting as pinned.
    """

    def test_string_pairs_value_states_no_count(self):
        mod = harness.require("ontoloop.report")
        form = mod.production_report_form(
            produced_pairs={"kind a": "abcd"})
        self.assertEqual(form["production_counts"]["per_kind"], {})
        self.assertFalse(form["counts_present"])

    def test_integer_and_float_pairs_values_state_no_count(self):
        mod = harness.require("ontoloop.report")
        for value in (5, 1.5):
            form = mod.production_report_form(
                produced_pairs={"kind a": value})
            self.assertEqual(
                form["production_counts"]["per_kind"], {}, value)
            self.assertFalse(form["counts_present"], value)

    def test_genuine_pair_list_still_counts_beside_a_malformed_kind(self):
        mod = harness.require("ontoloop.report")
        form = mod.production_report_form(
            produced_pairs={
                "kind a": "abcd",
                "kind b": [[1, 2], [3, 4]],
            })
        self.assertEqual(
            form["production_counts"]["per_kind"], {"kind b": 2})
        self.assertTrue(form["counts_present"])
        standing = mod.production_report_form(
            produced_pairs={"kind a": [1, 2, 3], "kind b": [1]})
        self.assertEqual(
            standing["production_counts"]["per_kind"],
            {"kind a": 3, "kind b": 1})
        self.assertTrue(standing["counts_present"])


if __name__ == "__main__":
    unittest.main()
