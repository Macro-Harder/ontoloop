"""Slice PROMOTE tests, list section 2.13.

Rows transcribed from design/steps/step-09-merged-test-list.md section 2.13.
Perspective: whole path behaviour, evidence homes, records, and cross slice
effects. Each test body begins by requiring its product surface through the
shared harness, then states the real assertions from its row.
"""

import unittest

from tests import harness


class PromoteT01Tests(unittest.TestCase):
    """PROMOTE-T01, in its restated second statement check form.

    The governing state table is implemented as one unit, state tests are
    generated from the table rows with the interaction set named, RC SC-5
    adopted in that form, and no second statement of any state rule exists
    in the slice output, checked by a rule by rule review of the whole
    slice output against the governing table. Search is retained as an aid
    and is not the check itself.
    """

    def test_state_tests_generated_from_table_rows(self):
        mod = harness.require("promotion")
        rules = mod.state_table_rules()
        generated = mod.generated_state_tests()
        self.assertEqual([g["rule"] for g in generated], list(rules))
        self.assertTrue(mod.interaction_set_name())
        for entry in generated:
            self.assertEqual(entry["generated_from"], "governing state table")

    def test_rule_by_rule_review_accounts_each_rule_exactly_once(self):
        mod = harness.require("promotion")
        review = mod.review_slice_output(reviewer="named reviewer")
        rules = list(mod.state_table_rules())
        self.assertEqual(sorted(review["accounted_rules"]), sorted(rules))
        self.assertEqual(len(review["accounted_rules"]), len(set(review["accounted_rules"])))
        for rule in rules:
            self.assertIn(rule, review["implementation_home"])
        self.assertEqual(review["second_statement_findings"], [])

    def test_review_records_a_second_statement_as_a_finding(self):
        mod = harness.require("promotion")
        output = mod.slice_output_with_a_second_statement()
        review = mod.review_slice_output(
            reviewer="named reviewer", slice_output=output)
        rules = list(mod.state_table_rules())
        findings = review["second_statement_findings"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"], output["second_statement_rule"])
        self.assertEqual(findings[0]["passage"], output["second_statement_passage"])
        self.assertEqual(sorted(review["accounted_rules"]), sorted(rules))
        self.assertEqual(len(review["accounted_rules"]), len(set(review["accounted_rules"])))

    def test_review_record_is_the_evidence_home(self):
        mod = harness.require("promotion")
        review = mod.review_slice_output(reviewer="named reviewer")
        self.assertEqual(review["record_home"], "PROMOTE slice exit record")
        self.assertTrue(review["filed"])
        self.assertFalse(review["rests_on_search_result"])

    def test_kill_before_the_append(self):
        mod = harness.require("promotion")
        result = mod.interrupt_before_append()
        self.assertEqual(result["verify"], "agreement")
        self.assertEqual(result["history_after"], result["history_before"])
        self.assertFalse(result["append_completed"])

    def test_kill_inside_the_rollback_append(self):
        mod = harness.require("promotion")
        result = mod.interrupt_inside_rollback_append()
        self.assertEqual(result["verify"], "agreement")
        self.assertEqual(result["pre_append_history_after"], result["pre_append_history_before"])
        self.assertFalse(result["currency_moved"])
        completed = mod.complete_append(result["attempt"])
        self.assertTrue(completed["currency_moved_at_completed_append"])


class PromoteT02Tests(unittest.TestCase):
    """PROMOTE-T02: gate pass and deployment land as one act."""

    def test_no_observable_moment_between_gate_pass_and_deployment(self):
        mod = harness.require("promotion")
        observed = mod.promote_with_observer()
        self.assertNotIn("gate_passed_not_deployed", observed["observable_states"])
        self.assertEqual(observed["final_state"], "deployed")

    def test_journal_order_audit_before_acknowledgement(self):
        mod = harness.require("promotion")
        result = mod.promote()
        kinds = [entry["kind"] for entry in result["journal"]]
        self.assertLess(kinds.index("audit"), kinds.index("acknowledgement"))
        self.assertLess(kinds.index("acknowledgement"), kinds.index("deployment"))


class PromoteT03Tests(unittest.TestCase):
    """PROMOTE-T03: the gate sequence runs in program order."""

    def test_gate_sequence_order(self):
        mod = harness.require("promotion")
        order = mod.gate_sequence_order()
        self.assertEqual(
            order,
            ["cross_split_audit", "margin_recomputation",
             "stamp_acknowledgement", "deployment"],
        )

    def test_cross_split_audit_is_the_third_call_point(self):
        mod = harness.require("promotion")
        first_step = mod.gate_sequence()[0]
        self.assertEqual(first_step["act"], "cross_split_audit")
        self.assertEqual(first_step["central_row"], "DATASET-T05")
        self.assertEqual(first_step["call_point"], 3)


class PromoteT04Tests(unittest.TestCase):
    """PROMOTE-T04: acknowledgement substance."""

    def test_proceed_is_the_only_satisfying_choice(self):
        mod = harness.require("promotion")
        result = mod.acknowledge("proceed")
        self.assertEqual(result["position"], "acknowledged")
        self.assertTrue(result["satisfies_gate"])

    def test_any_other_acknowledgement_leaves_gate_pass_held(self):
        mod = harness.require("promotion")
        for choice in ("noted", "seen", "visibility only"):
            result = mod.acknowledge(choice)
            self.assertEqual(result["position"], "gate pass held")
            self.assertFalse(result["satisfies_gate"])


class PromoteT05Tests(unittest.TestCase):
    """PROMOTE-T05: confirmation record completeness, criteria 16 and 17 parts."""

    def test_missing_weight_position_field_is_refused(self):
        mod = harness.require("promotion")
        record = mod.complete_confirmation_record()
        del record["production_evidence_weight_position"]
        result = mod.submit_confirmation(record)
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["reason"], "confirmation record incomplete")

    def test_label_and_weight_position_fields_carry_allowed_values_exactly(self):
        mod = harness.require("promotion")
        allowed_label = mod.allowed_values("production_evidence_label_position")
        allowed_weight = mod.allowed_values("production_evidence_weight_position")
        record = mod.complete_confirmation_record()
        self.assertIn(record["production_evidence_label_position"], allowed_label)
        self.assertIn(record["production_evidence_weight_position"], allowed_weight)
        bad = dict(record)
        bad["production_evidence_weight_position"] = "outside the allowed values"
        self.assertEqual(mod.submit_confirmation(bad)["outcome"], "refused")


class PromoteT06Tests(unittest.TestCase):
    """PROMOTE-T06: race and interruption tests on journal order, FF2-19."""

    def test_concurrent_promotions_are_decided_by_journal_order(self):
        mod = harness.require("promotion")
        result = mod.race_two_promotions()
        self.assertEqual(result["winner"], result["journal_first"])
        self.assertEqual(result["loser_outcome"], "refused by journal order")
        self.assertEqual(len(result["deployments"]), 1)

    def test_interruption_leaves_no_half_promotion(self):
        mod = harness.require("promotion")
        result = mod.interrupt_promotion()
        self.assertIn(result["state"], ("not promoted", "deployed"))
        self.assertEqual(result["verify"], "agreement")


class PromoteT07Tests(unittest.TestCase):
    """PROMOTE-T07: bundle bound at D-10 checked twice, no silent trimming."""

    def test_bound_checked_at_candidate_construction(self):
        mod = harness.require("promotion")
        result = mod.construct_candidate(bundle_size="over D-10 bound")
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["check_point"], "candidate construction")

    def test_bound_checked_again_at_bundle_writing(self):
        mod = harness.require("promotion")
        result = mod.write_bundle(bundle_size="over D-10 bound")
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["check_point"], "bundle writing")

    def test_no_silent_trimming_on_refusal(self):
        mod = harness.require("promotion")
        candidate = mod.candidate_over_bound()
        result = mod.write_bundle(candidate)
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["bundle_size_after"], candidate["size"])
        self.assertFalse(result["trimmed"])


class PromoteT08Tests(unittest.TestCase):
    """PROMOTE-T08: demotion flag record and its three disposition forms."""

    def test_flag_record_carries_identity_evidence_and_age_as_one_record(self):
        mod = harness.require("promotion")
        flag = mod.raise_demotion_flag(mod.confirmed_bundle())
        self.assertTrue(flag["bundle_identity"])
        self.assertTrue(flag["evidence"])
        self.assertIn("age", flag)
        self.assertEqual(flag["record_count"], 1)

    def test_disposition_demote(self):
        mod = harness.require("promotion")
        result = mod.dispose_demotion_flag("demote")
        self.assertEqual(result["record_form"], "demote")
        self.assertEqual(result["bundle_position"], "demoted")

    def test_disposition_retain_closes_flag_and_stops_its_age(self):
        mod = harness.require("promotion")
        result = mod.dispose_demotion_flag("retain", reason="evidence reviewed")
        self.assertEqual(result["record_form"], "retain")
        self.assertTrue(result["reason_recorded"])
        self.assertTrue(result["flag_closed"])
        self.assertTrue(result["age_stopped"])

    def test_disposition_defer_names_the_review_point(self):
        mod = harness.require("promotion")
        result = mod.dispose_demotion_flag("defer")
        self.assertEqual(result["record_form"], "defer")
        self.assertTrue(result["review_point_named"])


class PromoteT09Tests(unittest.TestCase):
    """PROMOTE-T09: fixed text travel lint over bundle writing."""

    def test_lint_passes_over_bundle_writing(self):
        mod = harness.require("promotion")
        result = mod.fixed_text_travel_lint(assembly="bundle writing")
        self.assertTrue(result["passed"])
        self.assertEqual(result["texts_checked"], 3)

    def test_paraphrase_of_any_verbatim_text_fails_the_lint(self):
        mod = harness.require("promotion")
        for text_name in ("seal sentence", "verify sentence", "grader awareness label"):
            result = mod.fixed_text_travel_lint(
                assembly="bundle writing", paraphrase_of=text_name)
            self.assertFalse(result["passed"], text_name)
            self.assertEqual(result["failed_text"], text_name)


if __name__ == "__main__":
    unittest.main()
