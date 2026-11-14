"""Unrowed obligations discharged by this seat, F-C2 ruling at section 5
of design/steps/step-13-content-retrace.md.

Each obligation below is written as a suite test under a recorded
transcription decision homed at its plan subsection, counted in the suite
manifest under the subsection rather than a row identifier. No identifier
is invented for any of them, and the refreshed list is not edited to
carry them. A comment block at each class names the subsection, the
obligation as stated, and the transcription choice for that obligation.
"""

import ast
import inspect
import unittest

from tests import harness


# ---------------------------------------------------------------------
# Transcription decision, unrowed obligation at plan subsection 19.86.
# Subsection: 19.86, holdout content through instruction items.
# Obligation as stated in the F-C2 ruling: Step 13 rows this test as its
# own test rows, covering a verbatim case, a near verbatim case, and a
# clean instruction case, at both occasions, candidate construction and
# promotion: the verbatim and near verbatim content test over the
# instruction text field of every instruction item in a candidate bundle
# against the sealed holdout, refusal in the cross split audit refusal
# form where the test fires, and no clearance claim covering instruction
# items until a promotion record carries the test result.
# Transcription choice: seven suite tests, three cases at two occasions
# plus the clearance claim method
# test_no_clearance_claim_until_a_promotion_record_carries_the_result,
# in one case class in this module, manifest entry keyed "19.86"
# recording the same count of seven with the method names. The
# candidate construction occasion tests require the dataset surface that
# assembles the candidate bundle, the promotion occasion tests require
# the promotion surface, and each firing case asserts refusal in the
# cross split audit refusal form at that occasion.
# ---------------------------------------------------------------------


class Unrowed1986Tests(unittest.TestCase):
    """Subsection 19.86: instruction item content against the sealed holdout."""

    def assert_fired_item_recorded_in_the_audit_record(self, result):
        self.assertEqual(result["items_tested"], result["instruction_item_count"])
        self.assertGreater(result["instruction_item_count"], 0)
        self.assertEqual(result["field_scope"], "instruction text field")
        self.assertFalse(result["wider_material_compared"])
        record = result["audit_record"]
        self.assertEqual(record["home"], "cross split audit record for the candidate")
        self.assertTrue(record["fired_item"])
        self.assertEqual(record["fired_item"], result["fired_item"])
        self.assertTrue(record["test_result_recorded"])
        self.assertEqual(record["test_result"], result["test_result"])

    def test_verbatim_case_at_candidate_construction(self):
        mod = harness.require("ontoloop.dataset")
        bundle = mod.candidate_with_instruction_item(kind="verbatim holdout content")
        result = mod.test_instruction_items_against_holdout(bundle, occasion="candidate construction")
        self.assertTrue(result["fired"])
        self.assertEqual(result["refusal_form"], "cross split audit refusal")
        self.assertFalse(result["bundle_proceeds"])
        self.assert_fired_item_recorded_in_the_audit_record(result)

    def test_near_verbatim_case_at_candidate_construction(self):
        mod = harness.require("ontoloop.dataset")
        bundle = mod.candidate_with_instruction_item(kind="near verbatim holdout content")
        result = mod.test_instruction_items_against_holdout(bundle, occasion="candidate construction")
        self.assertTrue(result["fired"])
        self.assertEqual(result["refusal_form"], "cross split audit refusal")
        self.assertFalse(result["bundle_proceeds"])
        self.assert_fired_item_recorded_in_the_audit_record(result)

    def test_clean_case_at_candidate_construction(self):
        mod = harness.require("ontoloop.dataset")
        bundle = mod.candidate_with_instruction_item(kind="clean instruction")
        result = mod.test_instruction_items_against_holdout(bundle, occasion="candidate construction")
        self.assertFalse(result["fired"])
        self.assertEqual(result["items_tested"], result["instruction_item_count"])
        self.assertGreater(result["instruction_item_count"], 0)
        self.assertEqual(result["field_scope"], "instruction text field")
        self.assertFalse(result["wider_material_compared"])

    def test_verbatim_case_at_promotion(self):
        mod = harness.require("ontoloop.promote")
        bundle = mod.candidate_with_instruction_item(kind="verbatim holdout content")
        result = mod.test_instruction_items_against_holdout(bundle, occasion="promotion")
        self.assertTrue(result["fired"])
        self.assertEqual(result["refusal_form"], "cross split audit refusal")
        self.assertFalse(result["promotion_proceeds"])
        self.assert_fired_item_recorded_in_the_audit_record(result)
        partial = mod.test_instruction_items_against_holdout(
            bundle, occasion="promotion", after_partial_scoring=True)
        self.assertTrue(partial["fired"])
        self.assertEqual(partial["refusal_form"], "cross split audit refusal")
        self.assertFalse(partial["promotion_proceeds"])
        self.assertEqual(partial["charging_form"],
                         "standing charging form for a refusal after partial scoring")
        self.assertTrue(partial["charged_under_the_standing_charging_rules"])
        self.assert_fired_item_recorded_in_the_audit_record(partial)

    def test_near_verbatim_case_at_promotion(self):
        mod = harness.require("ontoloop.promote")
        bundle = mod.candidate_with_instruction_item(kind="near verbatim holdout content")
        result = mod.test_instruction_items_against_holdout(bundle, occasion="promotion")
        self.assertTrue(result["fired"])
        self.assertEqual(result["refusal_form"], "cross split audit refusal")
        self.assertFalse(result["promotion_proceeds"])
        self.assert_fired_item_recorded_in_the_audit_record(result)

    def test_clean_case_at_promotion(self):
        mod = harness.require("ontoloop.promote")
        bundle = mod.candidate_with_instruction_item(kind="clean instruction")
        result = mod.test_instruction_items_against_holdout(bundle, occasion="promotion")
        self.assertFalse(result["fired"])
        self.assertEqual(result["items_tested"], result["instruction_item_count"])
        self.assertGreater(result["instruction_item_count"], 0)
        self.assertEqual(result["field_scope"], "instruction text field")
        self.assertFalse(result["wider_material_compared"])
        self.assertTrue(result["test_result_carried_on_promotion_record"])

    def test_no_clearance_claim_until_a_promotion_record_carries_the_result(self):
        mod = harness.require("ontoloop.promote")
        claim = mod.clearance_claim_covering_instruction_items(promotion_record=None)
        self.assertFalse(claim["claim_stands"])
        # Fix round 3, S15-R3-013: the intermediate case stands
        # presented, a record standing as a promotion record without
        # the instruction test result carried on it, in both the form
        # carrying the position at False and the form carrying no such
        # position at all, and the claim does not stand on either.
        standing_without_result = {
            "record_home": "Promotion Record",
            "instruction_test_result_carried": False,
        }
        claim = mod.clearance_claim_covering_instruction_items(
            promotion_record=standing_without_result)
        self.assertFalse(claim["claim_stands"])
        standing_with_no_position = {"record_home": "Promotion Record"}
        claim = mod.clearance_claim_covering_instruction_items(
            promotion_record=standing_with_no_position)
        self.assertFalse(claim["claim_stands"])
        record = mod.promotion_record_carrying_instruction_test_result()
        claim = mod.clearance_claim_covering_instruction_items(promotion_record=record)
        self.assertTrue(claim["claim_stands"])


# ---------------------------------------------------------------------
# Transcription decision, unrowed obligation at plan subsection 19.87.
# Subsection: 19.87, the provisional bundle comparison basis.
# Obligation as stated in the F-C2 ruling: Step 13 rows this rule: a
# provisional record with the comparison present, the outcome mix and
# the correction position for the provisional period set against the
# same figures for the displaced bundle over its last comparable
# period; a provisional record with no comparison and a confirmation
# barred in that state; and a record whose comparison basis is stated
# by name with the reason it was chosen, where no comparable displaced
# period stands.
# Transcription choice: three suite tests, one per case the subsection
# states, in one case class in this module, manifest entry keyed
# "19.87". Each test requires the promotion surface, which owns the
# provisional record and the confirmation bar.
# ---------------------------------------------------------------------


class Unrowed1987Tests(unittest.TestCase):
    """Subsection 19.87: the provisional bundle comparison basis."""

    def test_provisional_record_with_the_comparison_present(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(with_comparison=True)
        comparison = record["comparison"]
        provisional = comparison["provisional_period"]
        displaced = comparison["displaced_period"]
        for figure in ("outcome_mix", "correction_position"):
            self.assertIn(figure, provisional)
            self.assertIn(figure, displaced)
            self.assertTrue(provisional[figure], figure)
            self.assertTrue(displaced[figure], figure)
            self.assertEqual(sorted(provisional[figure]), sorted(displaced[figure]), figure)
        self.assertEqual(comparison["figures_set_against"],
                         ["outcome mix", "correction position"])
        self.assertEqual(displaced["standing"],
                         "last comparable period of the displaced bundle")
        self.assertTrue(record["comparison_in_same_view_as_run_count_and_coverage"])
        self.assertIn("attributed run count", record["comparison_view_contents"])
        self.assertIn("outcome and signal coverage figures",
                      record["comparison_view_contents"])
        self.assertIn("outcome mix", record["comparison_view_contents"])
        self.assertIn("correction position", record["comparison_view_contents"])
        # Fix round 3, S15-R3-012: the figure values themselves stand
        # pinned on material passed, and differing material returns
        # differing counts, so a stored figure returning the same
        # counts for every input cannot pass this test.
        counted = mod.provisional_record(
            with_comparison=True,
            provisional_outcomes=["pass", "pass", "pass", "fail"],
            displaced_outcomes=["pass", "fail", "fail"],
            provisional_corrections=["open", "open", "corrected"],
            displaced_corrections=["corrected", "corrected"])
        counted_comparison = counted["comparison"]
        counted_provisional = counted_comparison["provisional_period"]
        counted_displaced = counted_comparison["displaced_period"]
        self.assertEqual(counted_provisional["outcome_mix"],
                         {"pass": 3, "fail": 1})
        self.assertEqual(counted_displaced["outcome_mix"],
                         {"pass": 1, "fail": 2})
        self.assertEqual(counted_provisional["correction_position"],
                         {"open": 2, "corrected": 1})
        self.assertEqual(counted_displaced["correction_position"],
                         {"corrected": 2})
        differing = mod.provisional_record(
            with_comparison=True,
            provisional_outcomes=["fail", "fail"],
            displaced_outcomes=["pass"],
            provisional_corrections=["open"],
            displaced_corrections=["open", "open", "open", "corrected"])
        differing_comparison = differing["comparison"]
        differing_provisional = differing_comparison["provisional_period"]
        differing_displaced = differing_comparison["displaced_period"]
        self.assertEqual(differing_provisional["outcome_mix"], {"fail": 2})
        self.assertEqual(differing_displaced["outcome_mix"], {"pass": 1})
        self.assertEqual(differing_provisional["correction_position"],
                         {"open": 1})
        self.assertEqual(differing_displaced["correction_position"],
                         {"open": 3, "corrected": 1})
        self.assertNotEqual(differing_provisional["outcome_mix"],
                            counted_provisional["outcome_mix"])
        self.assertNotEqual(differing_displaced["outcome_mix"],
                            counted_displaced["outcome_mix"])
        self.assertNotEqual(differing_provisional["correction_position"],
                            counted_provisional["correction_position"])
        self.assertNotEqual(differing_displaced["correction_position"],
                            counted_displaced["correction_position"])

    def test_provisional_record_with_no_comparison_bars_confirmation(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(with_comparison=False)
        self.assertIsNone(record["comparison"])
        result = mod.confirm_provisional(record)
        self.assertEqual(result["outcome"], "barred")
        self.assertEqual(result["bar_reason"], "no comparison in the provisional record")

    # Fix round 3, S15-R3-014: the success side of the confirmation
    # bar stands pinned, on a record carrying a comparison, so an act
    # barring every record cannot pass this file.
    def test_confirm_provisional_on_a_record_carrying_a_comparison(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(with_comparison=True)
        self.assertIsNotNone(record["comparison"])
        result = mod.confirm_provisional(record)
        self.assertEqual(result["outcome"], "confirmed")
        self.assertNotIn("bar_reason", result)

    def test_comparison_basis_stated_by_name_with_its_reason(self):
        mod = harness.require("ontoloop.promote")
        record = mod.provisional_record(comparable_displaced_period=False)
        self.assertTrue(record["comparison_basis_named"])
        self.assertTrue(record["comparison_basis_reason_recorded"])
        self.assertNotEqual(record["comparison_basis"], "")


# ---------------------------------------------------------------------
# Transcription decision, unrowed obligation at plan subsection 20.18.
# Subsection: 20.18, the determinism check at subsection 18.7.
# Obligation as stated in the F-C2 ruling: one CORE test row added at
# section 6.5 under this subsection, carrying both limbs of the
# determinism check at subsection 18.7: the source limb, scanning the
# core source for use of the builtin hash function for grouping,
# ordering, or assignment, and for any construction whose output order
# is the iteration order of a set; and the run limb, running one core
# computation twice over the same inputs with the set valued inputs
# constructed in a different order on the second run and comparing the
# two outputs in full; the row failing on a build that performs either
# barred practice, a failure recorded with the limb and the computation
# that failed it, and the CORE exit not standing passed on an
# undisposed failure.
# Transcription choice: one case class in this module with one test per
# limb and one test for the failure recording and CORE exit limb,
# manifest entry keyed "20.18". The tests require the core surface,
# which is the surface the check scans and runs.
# ---------------------------------------------------------------------


class Unrowed2018Tests(unittest.TestCase):
    """Subsection 20.18: the determinism check, both limbs at subsection 18.7."""

    def test_source_limb_scans_for_barred_practices(self):
        mod = harness.require("ontoloop.core")
        scan = mod.determinism_source_scan()
        self.assertEqual(scan["limb"], "source")
        self.assertEqual(scan["builtin_hash_uses_for_grouping_ordering_assignment"], [])
        self.assertEqual(scan["set_iteration_order_constructions"], [])
        self.assertTrue(scan["whole_core_source_scanned"])

    def test_run_limb_compares_two_runs_in_full(self):
        mod = harness.require("ontoloop.core")
        result = mod.determinism_run_check()
        self.assertEqual(result["limb"], "run")
        self.assertNotEqual(result["first_input_order"], result["second_input_order"])
        self.assertEqual(result["first_output"], result["second_output"])
        self.assertTrue(result["compared_in_full"])

    def test_failure_is_recorded_with_limb_and_computation_and_blocks_core_exit(self):
        mod = harness.require("ontoloop.core")
        for limb in ("source", "run"):
            failure = mod.determinism_check_with_barred_practice(limb=limb)
            self.assertTrue(failure["row_failed"], limb)
            self.assertEqual(failure["recorded_limb"], limb)
            self.assertTrue(failure["recorded_computation"], limb)
            self.assertFalse(mod.core_exit_passes(undisposed_failure=failure), limb)
        disposed = mod.dispose_determinism_failure(failure)
        self.assertTrue(mod.core_exit_passes(undisposed_failure=None, disposed=[disposed]))

    # Fix round 2, R2-CORE-1: core_exit_passes checks every entry of
    # its disposed list, and an undisposed argument in a non mapping
    # form fails closed in form rather than by exception.
    def test_core_exit_passes_checks_every_disposed_entry(self):
        mod = harness.require("ontoloop.core")
        failure = mod.determinism_check_with_barred_practice(limb="run")
        self.assertFalse(failure["disposed"])
        self.assertFalse(
            mod.core_exit_passes(undisposed_failure=None, disposed=[failure]))
        self.assertFalse(
            mod.core_exit_passes(disposed=[{"disposed": False, "row_failed": True}]))
        disposed = mod.dispose_determinism_failure(failure)
        self.assertFalse(
            mod.core_exit_passes(
                undisposed_failure=None,
                disposed=[disposed, {"disposed": False, "row_failed": True}]))
        self.assertTrue(
            mod.core_exit_passes(undisposed_failure=None, disposed=[disposed]))
        self.assertTrue(
            mod.core_exit_passes(undisposed_failure=None, disposed=[]))

    def test_core_exit_passes_non_mapping_undisposed_argument_fails_closed(self):
        mod = harness.require("ontoloop.core")
        for argument in ("failure", 123, ["disposed"]):
            self.assertFalse(
                mod.core_exit_passes(undisposed_failure=argument), repr(argument))

    # Fix round 2, R2-CORE-2: the run limb seed input stands set
    # valued in form, so the order the seed emits is the set
    # iteration order itself, and the run limb still records its
    # failure under its standing computation name.
    def test_run_limb_seed_input_stands_set_valued_in_form(self):
        mod = harness.require("ontoloop.core")
        tree = ast.parse(inspect.getsource(
            mod.determinism_check_with_barred_practice))
        seed_calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "_seeded_set_order_computation"
        ]
        self.assertEqual(len(seed_calls), 2)
        for call in seed_calls:
            self.assertEqual(len(call.args), 1)
            argument = call.args[0]
            self.assertIsInstance(argument, ast.Call)
            self.assertIsInstance(argument.func, ast.Name)
            self.assertEqual(argument.func.id, "set")
        seed = getattr(mod, "_seeded_set_order_computation")
        first_values = set((0, 8, 16))
        second_values = set((16, 8, 0))
        self.assertEqual(seed(first_values), list(first_values))
        self.assertEqual(seed(second_values), list(second_values))
        self.assertNotEqual(seed(first_values), seed(second_values))
        self.assertEqual(sorted(seed(first_values)), [0, 8, 16])

    def test_run_limb_still_records_its_failure(self):
        mod = harness.require("ontoloop.core")
        failure = mod.determinism_check_with_barred_practice(limb="run")
        self.assertTrue(failure["row_failed"])
        self.assertEqual(failure["recorded_limb"], "run")
        self.assertEqual(
            failure["recorded_computation"],
            "seeded computation emitting set iteration order")
        self.assertFalse(failure["disposed"])


if __name__ == "__main__":
    unittest.main()
