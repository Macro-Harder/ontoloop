"""Slice DATASET, list section 2.11, plan section 6.5 plus rows
supplied at subsections 16.3, 16.19, and 19.64, and the Amendment 1
owing row at section 13.3.

Failure and boundary perspective: these tests prize the refusal and
shortfall outcomes the rows state: no dataset below the D-14 gate,
the span condition failing in its own form at group sizes 5 and 8,
eligibility drops under their own reasons, the sealed whole or not
at all write under interruption, and the paraphrase negative fixture
for the cross split audit.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.dataset, with function names taken from the behaviour
wording of each row. Fields a row does not state are not invented.
DATASET-T11 is the F-C1 pointer row for the REDACT-T08 call point at
DATASET: its class states no second wording of the behaviour and
exercises the pass condition of the central row REDACT-T08 at its
DATASET call point only.
"""

import unittest

try:
    from tests.harness import require, stage_carried
except ImportError:
    from harness import require, stage_carried

MODULE = "ontoloop.dataset"

THREE_RELATIONS = ("group", "signature", "near verbatim cluster")


class TestDatasetT01(unittest.TestCase):
    """DATASET-T01: below the D-14 gate nothing is written."""

    def test_below_the_gate_the_build_writes_no_dataset(self):
        module = require(MODULE)
        build = module.build_example_b(runs=30)
        self.assertFalse(build["dataset_written"])

    def test_workflow_recorded_not_yet_buildable_with_its_counts(self):
        module = require(MODULE)
        build = module.build_example_b(runs=30)
        self.assertEqual(build["workflow_state"], "not yet buildable")
        self.assertEqual(build["counts"]["runs"], 30)


class TestDatasetT02(unittest.TestCase):
    """DATASET-T02: the span condition fails at both group sizes."""

    def test_span_condition_fails_at_group_size_5(self):
        module = require(MODULE)
        build = module.build_example_b(group_size=5)
        self.assertEqual(build["span_condition"], "failed")

    def test_span_condition_fails_at_group_size_8(self):
        module = require(MODULE)
        build = module.build_example_b(group_size=8)
        self.assertEqual(build["span_condition"], "failed")

    def test_the_record_states_the_failure_in_its_own_form(self):
        module = require(MODULE)
        for size in (5, 8):
            build = module.build_example_b(group_size=size)
            self.assertEqual(
                build["span_failure_form"], "span condition failure"
            )


class TestDatasetT03(unittest.TestCase):
    """DATASET-T03: one consistent pool snapshot per build."""

    def test_build_order_runs_in_the_brief_order(self):
        module = require(MODULE)
        build = module.build_with_mid_build_append()
        self.assertEqual(build["order"], list(module.build_order()))

    def test_build_runs_over_one_consistent_pool_snapshot(self):
        module = require(MODULE)
        build = module.build_with_mid_build_append()
        self.assertEqual(build["snapshots_used"], 1)

    def test_mid_build_append_takes_effect_only_for_the_next_build(self):
        module = require(MODULE)
        build = module.build_with_mid_build_append()
        self.assertNotIn(
            build["appended_run"], build["pool_run_ids"]
        )
        following = module.next_build(build)
        self.assertIn(build["appended_run"], following["pool_run_ids"])


class TestDatasetT04(unittest.TestCase):
    """DATASET-T04: dedup, eligibility, selection, quotas."""

    def test_exact_dedup_keeps_outcome_bearing_fields_in_comparison(self):
        module = require(MODULE)
        result = module.dedup_grouped_fixture()
        self.assertIn(
            "outcome bearing fields", result["comparison_fields"]
        )
        self.assertFalse(result["merged_outcome_distinct_pair"])

    def test_eligibility_excludes_synthetic_and_canary_by_drop_reason(self):
        module = require(MODULE)
        result = module.eligibility_grouped_fixture()
        for kind in ("synthetic", "canary"):
            self.assertIn(kind, result["excluded"])
            self.assertTrue(result["excluded"][kind]["drop_reason"])

    def test_selection_order_outcome_mapping_and_quota_match_brief(self):
        module = require(MODULE)
        result = module.selection_grouped_fixture()
        self.assertEqual(result["order"], list(module.brief_order()))
        self.assertEqual(
            result["outcome_mapping"], module.brief_outcome_mapping()
        )
        self.assertEqual(result["quota"], module.brief_quota())


class TestDatasetT05(unittest.TestCase):
    """DATASET-T05: cross split audit, three relations only."""

    def test_spanning_pairs_are_dropped_and_recorded(self):
        module = require(MODULE)
        audit = module.cross_split_audit_at_build()
        self.assertTrue(audit["spanning_pairs_dropped"])
        self.assertTrue(audit["spanning_pairs_recorded"])

    def test_the_audit_runs_over_the_three_relations_only(self):
        module = require(MODULE)
        audit = module.cross_split_audit_at_build()
        self.assertEqual(set(audit["relations"]), set(THREE_RELATIONS))

    def test_paraphrase_pair_is_a_negative_fixture(self):
        module = require(MODULE)
        audit = module.cross_split_audit_at_build()
        pair = audit["paraphrase_pair"]
        self.assertFalse(pair["flagged_on_paraphrase_grounds"])
        if pair["flagged"]:
            self.assertIn(pair["flag_relation"], THREE_RELATIONS)

    def test_the_audit_does_not_clear_paraphrase_leakage(self):
        module = require(MODULE)
        audit = module.cross_split_audit_at_build()
        self.assertFalse(audit["clears_paraphrase_leakage"])
        self.assertEqual(
            audit["residual_risk"], "paraphrase leakage across the split"
        )


class TestDatasetT06(unittest.TestCase):
    """DATASET-T06: pinned versions, attestation, shortfall state."""

    def test_curation_versions_are_pinned(self):
        module = require(MODULE)
        record = module.dataset_record()
        self.assertTrue(record["curation_versions_pinned"])

    def test_operator_attestation_field_is_present(self):
        module = require(MODULE)
        record = module.dataset_record()
        self.assertIn("operator_attestation", record["fields"])

    def test_post_audit_shortfall_lands_where_material_runs_out(self):
        module = require(MODULE)
        build = module.build_with_shortfall()
        self.assertEqual(build["state"], "post audit shortfall")

    def test_protocol_record_stands_in_its_conditional_form(self):
        module = require(MODULE)
        record = module.dataset_record()
        protocol = record["pre_scoring_protocol_record"]
        self.assertTrue(protocol["conditional_form"])


class TestDatasetT07(unittest.TestCase):
    """DATASET-T07: sealed whole or not written at all."""

    def test_interruption_leaves_no_dataset_and_no_dataset_record(self):
        module = require(MODULE)
        outcome = module.build_with_fault("kill inside dataset writing")
        self.assertFalse(outcome["dataset_stands"])
        self.assertFalse(outcome["dataset_record_stands"])

    def test_named_error_is_dataset_writing_interrupted(self):
        module = require(MODULE)
        outcome = module.build_with_fault("kill inside dataset writing")
        self.assertEqual(outcome["error"], "dataset writing interrupted")

    def test_intake_account_records_the_abort(self):
        module = require(MODULE)
        outcome = module.build_with_fault("kill inside dataset writing")
        self.assertTrue(outcome["intake_account_records_abort"])
        self.assertFalse(outcome["dataset_to_verify"])

    def test_recovery_is_a_whole_re_run_from_the_snapshot(self):
        module = require(MODULE)
        outcome = module.build_with_fault("kill inside dataset writing")
        self.assertEqual(
            outcome["recovery"], "build act re run whole from snapshot"
        )
        self.assertFalse(outcome["operator_attestation_taken"])

    def test_operator_is_informed_by_the_intake_account_entry(self):
        module = require(MODULE)
        outcome = module.build_with_fault("kill inside dataset writing")
        self.assertTrue(outcome["operator_informed"])
        self.assertEqual(
            outcome["operator_informed_by"], "intake account entry"
        )


class TestDatasetT08(unittest.TestCase):
    """DATASET-T08, Amendment 1: forms owed in the intake account."""

    def test_acknowledgement_wording_stands_in_full_in_the_account(self):
        module = require(MODULE)
        record = module.dataset_record_example_b()
        account = record["intake_account"]
        self.assertEqual(
            account["acknowledgement_wording"],
            module.acknowledgement_wording(),
        )
        self.assertFalse(account["acknowledgement_in_summary_form"])
        self.assertFalse(account["acknowledgement_in_pointer_form"])

    def test_shortened_or_missing_wording_fails_the_row(self):
        module = require(MODULE)
        record = module.dataset_record_example_b()
        varied = dict(record)
        account = dict(record["intake_account"])
        account["acknowledgement_wording"] = "shortened wording"
        varied["intake_account"] = account
        defects = module.check_dataset_record(varied)
        self.assertTrue(defects)
        self.assertTrue(all(d["artifact"] == "Dataset record"
                            for d in defects))

    def test_each_simple_figure_has_an_advanced_counterpart(self):
        module = require(MODULE)
        record = module.dataset_record_example_b()
        self.assertEqual(module.check_dataset_record(record), [])
        for figure in record["intake_account"]["figures"]:
            self.assertIn(figure, record["advanced"]["figures"])
            self.assertTrue(
                record["advanced"]["figures"][figure]["derivation"]
            )

    def test_simple_figure_without_counterpart_fails_the_row(self):
        module = require(MODULE)
        record = module.dataset_record_example_b()
        varied = dict(record)
        varied["advanced"] = {"figures": {}}
        self.assertTrue(module.check_dataset_record(varied))

    def test_agentic_claim_is_not_owed_and_none_is_printed(self):
        module = require(MODULE)
        record = module.dataset_record_example_b()
        self.assertNotIn("agentic", record["intake_account"])

    def test_owed_form_with_a_different_value_fails_the_row(self):
        module = require(MODULE)
        record = module.dataset_record_example_b()
        varied = dict(record)
        advanced = dict(record["advanced"])
        figures = dict(advanced["figures"])
        first = sorted(figures)[0]
        entry = dict(figures[first])
        entry["value"] = "a different value"
        figures[first] = entry
        advanced["figures"] = figures
        varied["advanced"] = advanced
        self.assertTrue(module.check_dataset_record(varied))


class TestDatasetT09(unittest.TestCase):
    """DATASET-T09: fixed text travel lint over dataset build."""

    SEAL_SENTENCE = (
        "sealed binds candidate construction, all agent facing "
        "surfaces, and the operator as an actor through the tools, "
        "conditional on the deployment confinement fact at Section "
        "7.1 item 1; it does not bind the operator as a reader of "
        "her own files; holdout content through a tool surface "
        "requires an override on the operator door only, with a "
        "required reason, and the override writes a permanent "
        "access record before any content is shown; an override "
        "spends the disclosed group whole, by disclosure, and that "
        "group never judges a later promotion."
    )

    VERIFY_SENTENCE = (
        "Verify proved the journal chain and the manifest agree "
        "over every record checked, and that the journal head and "
        "the manifest head stand signed under the signing key, so "
        "no checked record was altered after it was written except "
        "under that key, at signed strength only."
    )

    VERIFY_HOLES = (
        "a rewrite signed with the genuine key is not detected",
        "the anchor covers the heads as they stood at the most "
        "recent completed backup archive",
        "whole home deletion is detected only where an anchor for "
        "the store stands in an archive that survives",
    )

    GRADER_AWARENESS_LABEL = (
        "No bundle name was hidden in this record. Each run is "
        "named with the bundle that produced it. The grades here "
        "are operator grades. They are not a blind check, and they "
        "are not separate from the bundle. Signal counts in this "
        "record are not grades, and they stand apart from the "
        "grades. These grades can support your decision. They "
        "cannot confirm the bundle on their own."
    )

    def test_three_verbatim_texts_stand_in_their_landed_forms(self):
        module = require(MODULE)
        texts = list(module.three_verbatim_texts())
        self.assertEqual(len(texts), 3)
        self.assertIn(self.SEAL_SENTENCE, texts)
        self.assertIn(self.GRADER_AWARENESS_LABEL, texts)
        verify_texts = [
            text for text in texts if self.VERIFY_SENTENCE in text
        ]
        self.assertEqual(len(verify_texts), 1)
        for hole in self.VERIFY_HOLES:
            self.assertIn(hole, verify_texts[0])
        self.assertEqual(verify_texts[0].count(self.VERIFY_SENTENCE), 1)
        for hole in self.VERIFY_HOLES:
            self.assertEqual(verify_texts[0].count(hole), 1)
        self.assertLess(
            verify_texts[0].index(self.VERIFY_SENTENCE),
            verify_texts[0].index(self.VERIFY_HOLES[0]),
        )
        self.assertLess(
            verify_texts[0].index(self.VERIFY_HOLES[0]),
            verify_texts[0].index(self.VERIFY_HOLES[1]),
        )
        self.assertLess(
            verify_texts[0].index(self.VERIFY_HOLES[1]),
            verify_texts[0].index(self.VERIFY_HOLES[2]),
        )
        superseded_sentence = (
            "Verify proved the journal chain and the manifest agree "
            "over every record checked, and that no checked record "
            "was altered after it was written, at local strength only."
        )
        for text in texts:
            self.assertNotIn(superseded_sentence, text)
            self.assertNotIn("at local strength only", text)

    def test_lint_passes_over_dataset_construction(self):
        module = require(MODULE)
        result = module.fixed_text_travel_lint("dataset construction")
        self.assertTrue(result["passes"])

    def test_paraphrase_of_any_verbatim_text_fails_the_lint(self):
        module = require(MODULE)
        for text in module.three_verbatim_texts():
            result = module.fixed_text_travel_lint(
                "dataset construction", paraphrase_of=text
            )
            self.assertFalse(result["passes"])


class TestDatasetT10(unittest.TestCase):
    """DATASET-T10: BQ-43 marking in its adopted form, subsection
    20.82 point four."""

    def test_intake_account_carries_the_marking_in_adopted_form(self):
        module = require(MODULE)
        record = module.dataset_record_first_build_gate()
        marking = record["intake_account"]["bq43_marking"]
        self.assertEqual(marking["form"], "adopted")
        self.assertEqual(
            marking["quarantine"], "build exclusion"
        )

    def test_marking_absent_at_intake_accounting_use_fails_the_row(self):
        module = require(MODULE)
        record = module.dataset_record_first_build_gate()
        varied = dict(record)
        account = dict(record["intake_account"])
        account["bq43_marking"] = None
        varied["intake_account"] = account
        self.assertTrue(module.check_dataset_record(varied))

    def test_marking_in_adoption_condition_form_fails_the_row(self):
        module = require(MODULE)
        record = module.dataset_record_first_build_gate()
        varied = dict(record)
        account = dict(record["intake_account"])
        marking = dict(account["bq43_marking"])
        marking["form"] = "adoption condition"
        account["bq43_marking"] = marking
        varied["intake_account"] = account
        self.assertTrue(module.check_dataset_record(varied))

    def test_marking_carries_its_discharge_event_from_the_ruling(self):
        module = require(MODULE)
        record = module.dataset_record_first_build_gate()
        marking = record["intake_account"]["bq43_marking"]
        self.assertEqual(marking["discharge_event"], "ruling at BQ-43")
        self.assertEqual(
            marking["discharge_effected_by"], "subsection 20.82"
        )


class TestDatasetT11(unittest.TestCase):
    """DATASET-T11: pointer row, F-C1 cure, subsection 19.64.

    This row names REDACT-T08 as its central row and states no
    second wording of the behaviour. The tests below exercise the
    pass condition of REDACT-T08 at its DATASET call point only.
    """

    def test_central_row_is_redact_t08(self):
        module = require(MODULE)
        build = module.dataset_build_for_posture_sequence()
        self.assertEqual(build["central_row"], "REDACT-T08")

    def test_dataset_call_point_build_carries_the_per_build_flag(self):
        module = require(MODULE)
        build = module.dataset_build_for_posture_sequence()
        self.assertTrue(build["per_build_flag"])

    def test_dataset_call_point_control_build_carries_no_flag(self):
        module = require(MODULE)
        build = module.dataset_build_for_posture_sequence()
        control = module.control_build_in_same_store(build)
        self.assertFalse(control["per_build_flag"])


if __name__ == "__main__":
    unittest.main()
