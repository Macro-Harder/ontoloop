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
        mod = harness.require("ontoloop.promote")
        rules = mod.state_table_rules()
        generated = mod.generated_state_tests()
        self.assertEqual([g["rule"] for g in generated], list(rules))
        self.assertTrue(mod.interaction_set_name())
        for entry in generated:
            self.assertEqual(entry["generated_from"], "governing state table")

    def test_rule_by_rule_review_accounts_each_rule_exactly_once(self):
        mod = harness.require("ontoloop.promote")
        review = mod.review_slice_output(reviewer="named reviewer")
        rules = list(mod.state_table_rules())
        self.assertEqual(sorted(review["accounted_rules"]), sorted(rules))
        self.assertEqual(len(review["accounted_rules"]), len(set(review["accounted_rules"])))
        for rule in rules:
            self.assertIn(rule, review["implementation_home"])
        self.assertEqual(review["second_statement_findings"], [])

    def test_review_records_a_second_statement_as_a_finding(self):
        mod = harness.require("ontoloop.promote")
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
        mod = harness.require("ontoloop.promote")
        review = mod.review_slice_output(reviewer="named reviewer")
        self.assertEqual(review["record_home"], "PROMOTE slice exit record")
        self.assertTrue(review["filed"])
        self.assertFalse(review["rests_on_search_result"])

    def test_kill_before_the_append(self):
        mod = harness.require("ontoloop.promote")
        result = mod.interrupt_before_append()
        self.assertEqual(result["verify"], "agreement")
        self.assertEqual(result["history_after"], result["history_before"])
        self.assertFalse(result["append_completed"])

    def test_kill_inside_the_rollback_append(self):
        mod = harness.require("ontoloop.promote")
        result = mod.interrupt_inside_rollback_append()
        self.assertEqual(result["verify"], "agreement")
        self.assertEqual(result["pre_append_history_after"], result["pre_append_history_before"])
        self.assertFalse(result["currency_moved"])
        completed = mod.complete_append(result["attempt"])
        self.assertTrue(completed["currency_moved_at_completed_append"])


class PromoteT02Tests(unittest.TestCase):
    """PROMOTE-T02: gate pass and deployment land as one act."""

    def test_no_observable_moment_between_gate_pass_and_deployment(self):
        mod = harness.require("ontoloop.promote")
        observed = mod.promote_with_observer()
        self.assertNotIn("gate_passed_not_deployed", observed["observable_states"])
        self.assertEqual(observed["final_state"], "deployed")

    def test_journal_order_audit_before_acknowledgement(self):
        mod = harness.require("ontoloop.promote")
        result = mod.promote()
        kinds = [entry["kind"] for entry in result["journal"]]
        self.assertLess(kinds.index("audit"), kinds.index("acknowledgement"))
        self.assertLess(kinds.index("acknowledgement"), kinds.index("deployment"))


class PromoteT03Tests(unittest.TestCase):
    """PROMOTE-T03: the gate sequence runs in program order."""

    def test_gate_sequence_order(self):
        mod = harness.require("ontoloop.promote")
        order = mod.gate_sequence_order()
        self.assertEqual(
            order,
            ["cross_split_audit", "margin_recomputation",
             "stamp_acknowledgement", "deployment"],
        )

    def test_cross_split_audit_is_the_third_call_point(self):
        mod = harness.require("ontoloop.promote")
        first_step = mod.gate_sequence()[0]
        self.assertEqual(first_step["act"], "cross_split_audit")
        self.assertEqual(first_step["central_row"], "DATASET-T05")
        self.assertEqual(first_step["call_point"], 3)


class PromoteT04Tests(unittest.TestCase):
    """PROMOTE-T04: acknowledgement substance."""

    def test_proceed_is_the_only_satisfying_choice(self):
        mod = harness.require("ontoloop.promote")
        result = mod.acknowledge("proceed")
        self.assertEqual(result["position"], "acknowledged")
        self.assertTrue(result["satisfies_gate"])

    def test_any_other_acknowledgement_leaves_gate_pass_held(self):
        mod = harness.require("ontoloop.promote")
        for choice in ("noted", "seen", "visibility only"):
            result = mod.acknowledge(choice)
            self.assertEqual(result["position"], "gate pass held")
            self.assertFalse(result["satisfies_gate"])


class PromoteT05Tests(unittest.TestCase):
    """PROMOTE-T05: confirmation record completeness, criteria 16 and 17 parts."""

    def test_missing_weight_position_field_is_refused(self):
        mod = harness.require("ontoloop.promote")
        record = mod.complete_confirmation_record()
        del record["production_evidence_weight_position"]
        result = mod.submit_confirmation(record)
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["reason"], "confirmation record incomplete")

    def test_label_and_weight_position_fields_carry_allowed_values_exactly(self):
        mod = harness.require("ontoloop.promote")
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
        mod = harness.require("ontoloop.promote")
        result = mod.race_two_promotions()
        self.assertEqual(result["winner"], result["journal_first"])
        self.assertEqual(result["loser_outcome"], "refused by journal order")
        self.assertEqual(len(result["deployments"]), 1)

    def test_interruption_leaves_no_half_promotion(self):
        mod = harness.require("ontoloop.promote")
        result = mod.interrupt_promotion()
        self.assertIn(result["state"], ("not promoted", "deployed"))
        self.assertEqual(result["verify"], "agreement")


class PromoteT07Tests(unittest.TestCase):
    """PROMOTE-T07: bundle bound at D-10 checked twice, no silent trimming."""

    def test_bound_checked_at_candidate_construction(self):
        mod = harness.require("ontoloop.promote")
        result = mod.construct_candidate(bundle_size="over D-10 bound")
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["check_point"], "candidate construction")

    def test_bound_checked_again_at_bundle_writing(self):
        mod = harness.require("ontoloop.promote")
        result = mod.write_bundle(bundle_size="over D-10 bound")
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["check_point"], "bundle writing")

    def test_no_silent_trimming_on_refusal(self):
        mod = harness.require("ontoloop.promote")
        candidate = mod.candidate_over_bound()
        result = mod.write_bundle(candidate)
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["bundle_size_after"], candidate["size"])
        self.assertFalse(result["trimmed"])


class PromoteT08Tests(unittest.TestCase):
    """PROMOTE-T08: demotion flag record and its three disposition forms."""

    def test_flag_record_carries_identity_evidence_and_age_as_one_record(self):
        mod = harness.require("ontoloop.promote")
        flag = mod.raise_demotion_flag(mod.confirmed_bundle())
        self.assertTrue(flag["bundle_identity"])
        self.assertTrue(flag["evidence"])
        self.assertIn("age", flag)
        self.assertEqual(flag["record_count"], 1)

    def test_disposition_demote(self):
        mod = harness.require("ontoloop.promote")
        result = mod.dispose_demotion_flag("demote")
        self.assertEqual(result["record_form"], "demote")
        self.assertEqual(result["bundle_position"], "demoted")

    def test_disposition_retain_closes_flag_and_stops_its_age(self):
        mod = harness.require("ontoloop.promote")
        result = mod.dispose_demotion_flag("retain", reason="evidence reviewed")
        self.assertEqual(result["record_form"], "retain")
        self.assertTrue(result["reason_recorded"])
        self.assertTrue(result["flag_closed"])
        self.assertTrue(result["age_stopped"])

    def test_disposition_defer_names_the_review_point(self):
        mod = harness.require("ontoloop.promote")
        result = mod.dispose_demotion_flag("defer")
        self.assertEqual(result["record_form"], "defer")
        self.assertTrue(result["review_point_named"])


class PromoteT09Tests(unittest.TestCase):
    """PROMOTE-T09: fixed text travel lint over bundle writing."""

    def test_lint_passes_over_bundle_writing(self):
        mod = harness.require("ontoloop.promote")
        result = mod.fixed_text_travel_lint(assembly="bundle writing")
        self.assertTrue(result["passed"])
        self.assertEqual(result["texts_checked"], 3)

    def test_paraphrase_of_any_verbatim_text_fails_the_lint(self):
        mod = harness.require("ontoloop.promote")
        for text_name in ("seal sentence", "verify sentence", "grader awareness label"):
            result = mod.fixed_text_travel_lint(
                assembly="bundle writing", paraphrase_of=text_name)
            self.assertFalse(result["passed"], text_name)
            self.assertEqual(result["failed_text"], text_name)


class PromoteFixR5Tests(unittest.TestCase):
    """Fix round 5 pins: rulings 57, 58, 59, and 74."""

    # Act 1, ruling 57, N-20: non list containers at the four sites.

    def _provisional_kwargs(self, **override):
        kwargs = {
            "provisional_outcomes": ["pass", "fail"],
            "displaced_outcomes": ["pass"],
            "provisional_corrections": ["open"],
            "displaced_corrections": ["corrected"],
        }
        kwargs.update(override)
        return kwargs

    def test_act1_provisional_outcomes_non_list_containers_refused(self):
        mod = harness.require("ontoloop.promote")
        for value in ("pass", b"pass", {"pass": 2, "fail": 1}):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    provisional_outcomes=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")

    def test_act1_displaced_outcomes_non_list_containers_refused(self):
        mod = harness.require("ontoloop.promote")
        for value in ("pass", b"pass", {"pass": 2, "fail": 1}):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    displaced_outcomes=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")

    def test_act1_provisional_corrections_non_list_containers_refused(self):
        mod = harness.require("ontoloop.promote")
        for value in ("corrected", b"corrected", {"corrected": 1}):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    provisional_corrections=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")

    def test_act1_displaced_corrections_non_list_containers_refused(self):
        mod = harness.require("ontoloop.promote")
        for value in ("corrected", b"corrected", {"corrected": 1}):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    displaced_corrections=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")

    def test_act1_standing_list_forms_still_compute(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(**self._provisional_kwargs())
        comparison = record["comparison"]
        self.assertEqual(
            comparison["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})
        self.assertEqual(
            comparison["displaced_period"]["outcome_mix"], {"pass": 1})
        self.assertEqual(
            comparison["provisional_period"]["correction_position"],
            {"open": 1})
        empty = mod.provisional_record(**self._provisional_kwargs(
            provisional_outcomes=[]))
        self.assertEqual(
            empty["comparison"]["provisional_period"]["outcome_mix"], {})

    # Act 2, ruling 58, N-21: a retain reason carrying no content.

    def test_act2_retain_empty_reason_forms_refused(self):
        mod = harness.require("ontoloop.promote")
        for reason in ("", [], 0):
            with self.assertRaises(ValueError) as caught:
                mod.dispose_demotion_flag("retain", reason=reason)
            self.assertEqual(str(caught.exception), "retain requires a reason")

    def test_act2_retain_no_reason_and_standing_reason_forms(self):
        mod = harness.require("ontoloop.promote")
        with self.assertRaises(ValueError) as caught:
            mod.dispose_demotion_flag("retain")
        self.assertEqual(str(caught.exception), "retain requires a reason")
        result = mod.dispose_demotion_flag(
            "retain", reason="evidence reviewed")
        self.assertTrue(result["reason_recorded"])
        self.assertTrue(result["flag_closed"])
        self.assertTrue(result["age_stopped"])

    # Act 3, ruling 59, N-22: a present falsy bundle identity.

    def test_act3_demotion_flag_falsy_identity_carried(self):
        mod = harness.require("ontoloop.promote")
        for identity in ("", 0, False):
            flag = mod.raise_demotion_flag({"bundle_identity": identity})
            self.assertEqual(flag["bundle_identity"], identity)
            self.assertEqual(
                type(flag["bundle_identity"]), type(identity))

    def test_act3_demotion_flag_missing_key_still_fixture(self):
        mod = harness.require("ontoloop.promote")
        flag = mod.raise_demotion_flag({})
        self.assertEqual(flag["bundle_identity"], "confirmed bundle 1")
        flag = mod.raise_demotion_flag("not a mapping")
        self.assertEqual(flag["bundle_identity"], "confirmed bundle 1")

    # Act 4, ruling 74, N-37: a comparison that is no comparison mapping.

    def test_act4_confirm_provisional_non_mapping_comparison_barred(self):
        mod = harness.require("ontoloop.promote")
        for value in ({}, False, 0, "", "plain text", []):
            result = mod.confirm_provisional({"comparison": value})
            self.assertEqual(result["outcome"], "barred", repr(value))
            self.assertEqual(
                result["bar_reason"],
                "no comparison in the provisional record")

    def test_act4_confirm_provisional_full_comparison_still_confirms(self):
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


class PromoteFixR6Tests(unittest.TestCase):
    """Fix round 6 pins: rulings 103, 104, and 127."""

    def _provisional_kwargs(self, **override):
        kwargs = {
            "provisional_outcomes": ["pass", "fail"],
            "displaced_outcomes": ["pass"],
            "provisional_corrections": ["open"],
            "displaced_corrections": ["corrected"],
        }
        kwargs.update(override)
        return kwargs

    # Act 1, ruling 103, R6-PRO-1: a memoryview at the four sites.

    def test_act1_provisional_outcomes_memoryview_refused(self):
        mod = harness.require("ontoloop.promote")
        for value in (memoryview(b"pass"), memoryview(bytearray(b"pass"))):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    provisional_outcomes=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")

    def test_act1_displaced_outcomes_memoryview_refused(self):
        mod = harness.require("ontoloop.promote")
        for value in (memoryview(b"pass"), memoryview(bytearray(b"pass"))):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    displaced_outcomes=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")

    def test_act1_provisional_corrections_memoryview_refused(self):
        mod = harness.require("ontoloop.promote")
        for value in (memoryview(b"corrected"),
                      memoryview(bytearray(b"corrected"))):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    provisional_corrections=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")

    def test_act1_displaced_corrections_memoryview_refused(self):
        mod = harness.require("ontoloop.promote")
        for value in (memoryview(b"corrected"),
                      memoryview(bytearray(b"corrected"))):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    displaced_corrections=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")

    def test_act1_charged_forms_and_standing_list_forms(self):
        mod = harness.require("ontoloop.promote")
        for value in ("pass", b"pass", bytearray(b"pass"),
                      {"pass": 2, "fail": 1}):
            with self.assertRaises(ValueError) as caught:
                mod.provisional_record(**self._provisional_kwargs(
                    provisional_outcomes=value))
            self.assertEqual(
                str(caught.exception),
                "provisional values must stand as a list of values")
        record = mod.provisional_record(**self._provisional_kwargs())
        self.assertEqual(
            record["comparison"]["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})
        tuple_record = mod.provisional_record(**self._provisional_kwargs(
            provisional_outcomes=("pass", "fail")))
        self.assertEqual(
            tuple_record["comparison"]["provisional_period"]["outcome_mix"],
            {"pass": 1, "fail": 1})

    # Act 2, ruling 104, R6-PRO-2 with Lead Engineer line D-9:
    # a retain reason carrying no content in substance.

    def test_act2_retain_whitespace_only_reason_refused(self):
        mod = harness.require("ontoloop.promote")
        for reason in (" ", "   ", "\t", "\n", " \t\n "):
            with self.assertRaises(ValueError) as caught:
                mod.dispose_demotion_flag("retain", reason=reason)
            self.assertEqual(str(caught.exception), "retain requires a reason")

    def test_act2_retain_contentless_container_reason_refused(self):
        mod = harness.require("ontoloop.promote")
        for reason in ([""], [" "], {"detail": ""}, {"detail": " "}):
            with self.assertRaises(ValueError) as caught:
                mod.dispose_demotion_flag("retain", reason=reason)
            self.assertEqual(str(caught.exception), "retain requires a reason")

    def test_act2_retain_charged_and_standing_reason_forms(self):
        mod = harness.require("ontoloop.promote")
        for reason in ("", [], 0, None):
            with self.assertRaises(ValueError) as caught:
                mod.dispose_demotion_flag("retain", reason=reason)
            self.assertEqual(str(caught.exception), "retain requires a reason")
        with self.assertRaises(ValueError) as caught:
            mod.dispose_demotion_flag("retain")
        self.assertEqual(str(caught.exception), "retain requires a reason")
        for reason in ("evidence reviewed", ["evidence reviewed"],
                       {"detail": "evidence reviewed"}):
            result = mod.dispose_demotion_flag("retain", reason=reason)
            self.assertTrue(result["reason_recorded"])
            self.assertTrue(result["flag_closed"])
            self.assertTrue(result["age_stopped"])

    # Act 3, ruling 127, UC-R6-2 with Lead Engineer line D-8:
    # a comparison whose periods carry no period substance.

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

    def _assert_barred(self, mod, comparison):
        result = mod.confirm_provisional({"comparison": comparison})
        self.assertEqual(result["outcome"], "barred", repr(comparison))
        self.assertEqual(
            result["bar_reason"],
            "no comparison in the provisional record")

    def test_act3_both_periods_none_barred(self):
        mod = harness.require("ontoloop.promote")
        self._assert_barred(mod, {
            "provisional_period": None,
            "displaced_period": None,
        })

    def test_act3_both_periods_empty_mappings_barred(self):
        mod = harness.require("ontoloop.promote")
        self._assert_barred(mod, {
            "provisional_period": {},
            "displaced_period": {},
        })

    def test_act3_one_period_no_value_beside_full_period_barred(self):
        mod = harness.require("ontoloop.promote")
        provisional, displaced = self._full_periods()
        for comparison in (
            {"provisional_period": None, "displaced_period": displaced},
            {"provisional_period": provisional, "displaced_period": None},
            {"provisional_period": {}, "displaced_period": displaced},
            {"provisional_period": provisional, "displaced_period": {}},
        ):
            self._assert_barred(mod, comparison)

    def test_act3_periods_in_no_period_form_barred(self):
        mod = harness.require("ontoloop.promote")
        for comparison in (
            {"provisional_period": "plain text",
             "displaced_period": "plain text"},
            {"provisional_period": ["pass"],
             "displaced_period": ["pass"]},
            {"provisional_period": {"outcome_mix": {"pass": 1}},
             "displaced_period": {"outcome_mix": {"pass": 1}}},
            {"provisional_period": {"correction_position": {"open": 1}},
             "displaced_period": {"correction_position": {"open": 1}}},
        ):
            self._assert_barred(mod, comparison)

    def test_act3_full_and_charged_forms_stand(self):
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
        self._assert_barred(mod, None)
        for value in ({}, False, 0, "", "plain text", []):
            self._assert_barred(mod, value)


if __name__ == "__main__":
    unittest.main()
