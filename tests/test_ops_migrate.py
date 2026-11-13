"""Slice OPS-MIGRATE tests, list section 2.17.

Rows transcribed from design/steps/step-09-merged-test-list.md section 2.17.
The slice name lowercased in python module form is ops_migrate.
Perspective: whole path behaviour, evidence homes, records, and cross slice
effects. Each test body begins by requiring its product surface through the
shared harness, then states the real assertions from its row.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness


class OpsT01Tests(unittest.TestCase):
    """OPS-T01: from the tombstone append onward the material reads as absent."""

    def test_every_read_path_treats_named_material_as_absent(self):
        mod = harness.require("ops_migrate")
        mod.append_tombstone("material x")
        for path in mod.read_paths():
            result = mod.read(path, "material x")
            self.assertEqual(result["treatment"], "absent", path)

    def test_treatment_holds_inside_the_interim_as_at_its_close(self):
        mod = harness.require("ops_migrate")
        mod.append_tombstone("material x")
        interim = mod.read_all_paths("material x", when="interim")
        close = mod.read_all_paths("material x", when="close")
        self.assertEqual(interim, close)
        self.assertTrue(all(r["treatment"] == "absent" for r in interim.values()))


class OpsT02Tests(unittest.TestCase):
    """OPS-T02: the rebuilt journal check and the purge checkpoint."""

    def test_exact_omission_of_tombstoned_identities(self):
        mod = harness.require("ops_migrate")
        check = mod.rebuild_journal_check()
        self.assertEqual(sorted(check["omitted_identities"]), sorted(check["tombstoned_identities"]))
        self.assertFalse(check["extra_omissions"])

    def test_retention_of_all_other_records(self):
        mod = harness.require("ops_migrate")
        check = mod.rebuild_journal_check()
        self.assertEqual(sorted(check["retained_identities"]), sorted(check["non_tombstoned_identities"]))

    def test_purge_checkpoint_stands_as_founding_object_of_the_rebuilt_journal(self):
        mod = harness.require("ops_migrate")
        rebuilt = mod.rebuilt_journal()
        self.assertEqual(rebuilt["founding_object"], "purge checkpoint record")
        self.assertTrue(rebuilt["founding_object_precedes_all_records"])


class OpsT03Tests(unittest.TestCase):
    """OPS-T03: purge stopped export and tombstoned assemblies are refused."""

    def test_purge_stopped_export_is_refused(self):
        mod = harness.require("ops_migrate")
        result = mod.export(purge_stopped=True)
        self.assertEqual(result["outcome"], "refused")
        self.assertFalse(result["export_written"])

    def test_any_assembly_containing_tombstoned_material_is_refused(self):
        mod = harness.require("ops_migrate")
        assembly = mod.assembly_including("material x")
        mod.append_tombstone("material x")
        result = mod.release_assembly(assembly)
        self.assertEqual(result["outcome"], "refused")
        self.assertFalse(result["assembly_written"])


class OpsT04Tests(unittest.TestCase):
    """OPS-T04: the migration command, its check, and the spanning suite run."""

    def test_compatibility_is_classified_transitively(self):
        mod = harness.require("ops_migrate")
        result = mod.classify_compatibility(path=["v1", "v2", "v3"])
        self.assertTrue(result["transitive"])
        self.assertEqual(result["classification_basis"], "composed path")

    def test_spanning_suite_runs_on_every_migration_command(self):
        mod = harness.require("ops_migrate")
        for command in ("migrate", "check", "classify"):
            result = mod.run_migration_command(command)
            self.assertTrue(result["spanning_suite_run"], command)
            self.assertTrue(result["spanning_suite_result_recorded"], command)

    def test_composed_path_that_fails_its_check_is_refused_with_the_named_error(self):
        mod = harness.require("ops_migrate")
        result = mod.run_migration_command("migrate", composed_path_fails=True)
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["error"], mod.named_error("migration composed path refused"))
        self.assertFalse(result["migration_ran"])

    def test_golden_records_re_read_under_the_migrated_version(self):
        mod = harness.require("ops_migrate")
        result = mod.run_migration_command("migrate")
        self.assertTrue(result["golden_records_re_read"])
        self.assertEqual(result["golden_records_read_under"], result["migrated_version"])

    def test_evidence_home_rule_for_the_spanning_suite(self):
        mod = harness.require("ops_migrate")
        result = mod.run_migration_command("migrate")
        self.assertEqual(result["counted_evidence_home"], "suite result record")
        citation = result["suite_result_record"]["migration_occasion_citation"]
        self.assertEqual(citation["form"], "pointer")
        self.assertTrue(result["migration_occasion_record_is_evidence_home_in_own_right"])


class OpsT05Tests(unittest.TestCase):
    """OPS-T05: import verifies whole and moves no pointer."""

    def test_import_verifies_whole(self):
        mod = harness.require("ops_migrate")
        result = mod.import_bundle(mod.whole_bundle())
        self.assertTrue(result["verified_whole"])
        self.assertTrue(result["imported"])

    def test_import_moves_no_pointer(self):
        mod = harness.require("ops_migrate")
        before = mod.current_pointer()
        mod.import_bundle(mod.whole_bundle())
        self.assertEqual(mod.current_pointer(), before)

    def test_a_bundle_that_fails_whole_verification_is_not_imported(self):
        mod = harness.require("ops_migrate")
        before = mod.current_pointer()
        result = mod.import_bundle(mod.bundle_with_one_bad_part())
        self.assertFalse(result["verified_whole"])
        self.assertFalse(result["imported"])
        self.assertEqual(mod.current_pointer(), before)


class OpsT06Tests(unittest.TestCase):
    """OPS-T06: withdrawal, one order check for the act in this slice."""

    def test_withdrawal_order_check(self):
        mod = harness.require("ops_migrate")
        result = mod.withdrawal_order_check()
        self.assertTrue(result["order_matches_governing_home"])
        self.assertFalse(result["order_restated_in_this_slice"])
        self.assertEqual(result["checks_in_this_slice"], 1)


class OpsT07Tests(unittest.TestCase):
    """OPS-T07: residual category records, fixture terminal position cases."""

    def test_each_record_is_produced_by_its_act(self):
        mod = harness.require("ops_migrate")
        for case in mod.terminal_position_cases():
            record = mod.residual_record_for(case)
            self.assertEqual(record["produced_by"], case["act"], case["name"])
            self.assertTrue(record["exists"], case["name"])

    def test_each_record_reads_in_its_simple_form_wording(self):
        mod = harness.require("ops_migrate")
        for case in mod.terminal_position_cases():
            record = mod.residual_record_for(case)
            self.assertEqual(record["reading_form"], "Simple", case["name"])
            self.assertTrue(record["simple_wording_present"], case["name"])


class OpsT08Tests(unittest.TestCase):
    """OPS-T08: the owing row for the residual entries, section 13.3."""

    def test_simple_owed_including_its_limits_passage(self):
        mod = harness.require("ops_migrate")
        entry = mod.build_residual_entry()
        self.assertTrue(entry["simple_form_present"])
        self.assertTrue(entry["limits_passage_in_simple_form"])
        self.assertFalse(entry["agentic_form_present"])
        self.assertFalse(entry["agentic_owed"])

    def test_advanced_owed_wherever_the_limits_passage_states_a_figure_or_bound(self):
        mod = harness.require("ops_migrate")
        entry = mod.build_residual_entry(limits_states_bound=True)
        self.assertTrue(entry["advanced_form_present"])
        self.assertEqual(entry["advanced_bound"], entry["simple_bound"])

    def test_bound_with_no_advanced_counterpart_is_a_defect_in_the_record_itself(self):
        mod = harness.require("ops_migrate")
        entry = mod.build_residual_entry(limits_states_bound=True, omit="advanced form")
        self.assertEqual(entry["defect_home"], "the residual record itself")

    def test_value_equality_condition_from_subsection_18_55(self):
        mod = harness.require("ops_migrate")
        entry = mod.build_residual_entry(limits_states_bound=True, advanced_bound_differs=True)
        self.assertTrue(entry["row_failed"])
        self.assertEqual(entry["defect_home"], "the residual record itself")

    def test_printed_claim_is_governed_by_the_owing_row_of_the_printing_artifact(self):
        mod = harness.require("ops_migrate")
        printed = mod.print_claim_inside_artifact(
            artifact="loop report", claim="residual limit")
        self.assertEqual(printed["printing_artifact"], "loop report")
        self.assertEqual(printed["governing_owing_row"], "REPORT-T04")
        self.assertEqual(printed["governing_owing_row"],
                         printed["owing_row_of_the_printing_artifact"])
        printed = mod.print_claim_inside_artifact(
            artifact="residual record", claim="error wording")
        self.assertEqual(printed["printing_artifact"], "residual record")
        self.assertEqual(printed["governing_owing_row"], "OPS-T08")
        self.assertEqual(printed["governing_owing_row"],
                         printed["owing_row_of_the_printing_artifact"])

    def test_this_row_is_no_substitute_for_owing_rows_1_to_5(self):
        mod = harness.require("ops_migrate")
        self.assertFalse(mod.residual_owing_row_substitutes_for_owing_rows_1_to_5())


class OpsT09Tests(unittest.TestCase):
    """OPS-T09: withdrawal fault injection, subsection 16.29 item three."""

    def test_kill_after_the_withdrawal_record_append(self):
        mod = harness.require("ops_migrate")
        result = mod.withdrawal_kill_at_halfway_point()
        self.assertEqual(
            result["harness_entry"],
            "kill after the withdrawal record append and before any later withdrawal act",
        )
        self.assertTrue(result["withdrawal_record_appended"])

    def test_reads_from_that_append_treat_the_position_as_withdrawn(self):
        mod = harness.require("ops_migrate")
        result = mod.withdrawal_kill_at_halfway_point()
        for path in mod.read_paths():
            self.assertEqual(mod.read(path, result["material"])["treatment"], "withdrawn", path)

    def test_file_copies_outside_the_product_are_unaffected_and_stated_as_such(self):
        mod = harness.require("ops_migrate")
        result = mod.withdrawal_kill_at_halfway_point()
        self.assertFalse(result["outside_copies_affected"])
        self.assertTrue(result["outside_copies_stated_as_unaffected"])

    def test_verify_returns_agreement_with_the_withdrawal_record(self):
        mod = harness.require("ops_migrate")
        mod.withdrawal_kill_at_halfway_point()
        self.assertEqual(mod.verify()["output"], "agreement")
        self.assertEqual(mod.verify()["durable_state"], "withdrawal record")

    def test_no_recovery_act_and_the_operator_is_informed_by_the_record(self):
        mod = harness.require("ops_migrate")
        result = mod.withdrawal_kill_at_halfway_point()
        self.assertIsNone(result["recovery_act"])
        self.assertFalse(result["withdrawal_reversed"])
        self.assertTrue(result["operator_informed_by_withdrawal_record"])


class OpsT10Tests(unittest.TestCase):
    """OPS-T10: interrupted migration, confined form at subsection 20.8."""

    def test_empty_store_completed_forward_or_founded_again_at_old_shape(self):
        mod = harness.require("ops_migrate")
        result = mod.interrupt_migration(store="no populated material, no bundle consumed")
        self.assertIn(result["outcome"], ("completed forward from the migration record",
                                          "founded again at the old shape"))
        self.assertIn(result["final_shape"], (result["old_shape"], result["new_shape"]))

    def test_populated_or_consumed_store_founding_again_stands_barred(self):
        mod = harness.require("ops_migrate")
        for store in ("populated material", "reached POPULATED", "bundle consumed"):
            result = mod.interrupt_migration(store=store)
            self.assertFalse(result["founded_again"], store)
            self.assertIn(result["final_shape_kind"],
                          ("old shape", "completed new shape", "named intermediate shape"), store)

    def test_no_reversal_of_a_change_that_was_never_made(self):
        mod = harness.require("ops_migrate")
        result = mod.interrupt_migration(store="populated material")
        self.assertFalse(result["reversal_of_unmade_change_attempted"])
        self.assertTrue(result["recorded_as_migration_position"])

    def test_migration_record_names_the_shape_at_each_statement_boundary(self):
        mod = harness.require("ops_migrate")
        result = mod.interrupt_migration(store="populated material")
        for boundary in result["statement_boundaries"]:
            self.assertTrue(boundary["shape_named_in_migration_record"], boundary["name"])
            self.assertTrue(boundary["recovery_act_recorded_as_performed"], boundary["name"])
            self.assertEqual(boundary["recovery_act_performed_from_shape"],
                             boundary["shape_named_in_migration_record"], boundary["name"])
        self.assertTrue(result["migration_verify_result_on_record"] or result["named_migration_error"])

    def test_kill_at_each_statement_boundary_with_composed_check_at_each_restart(self):
        mod = harness.require("ops_migrate")
        result = mod.interrupt_migration(store="populated material")
        self.assertEqual(
            result["harness_entry"],
            "kill inside the migration at each statement boundary",
        )
        sequence = result["driven_sequence"]
        boundary_names = [b["name"] for b in result["statement_boundaries"]]
        kills = [e for e in sequence if e["act"] == "kill inside the migration"]
        self.assertEqual([k["at_statement_boundary"] for k in kills], boundary_names)
        restarts = [e for e in sequence if e["act"] == "restart"]
        self.assertEqual(len(restarts), len(kills))
        for restart in restarts:
            self.assertTrue(restart["composed_check_run_again"], restart["at_statement_boundary"])

    def test_unnamed_shape_case_needs_the_operator_led_rebuild_act(self):
        mod = harness.require("ops_migrate")
        result = mod.interrupt_migration(store="populated material", lands_at="unnamed shape")
        self.assertFalse(result["counted_as_recovered"])
        entry = result["recovery_entry"]
        self.assertEqual(entry["act"], "operator led shape determination and rebuild")
        self.assertEqual(len(entry["parts"]), 3)
        completed = mod.complete_operator_led_rebuild(entry)
        self.assertTrue(completed["counted_as_recovered"])

    def test_failure_counterpart_unnamed_shape_or_reversal_fails_the_row(self):
        mod = harness.require("ops_migrate")
        for defect in ("shape not named in the migration record",
                       "recovery recorded as reversal of an unmade change",
                       "founded again a populated store"):
            result = mod.interrupt_migration_with_defect(defect)
            self.assertTrue(result["row_failed"], defect)
            self.assertTrue(result["failure_recorded_in_suite_result"], defect)


if __name__ == "__main__":
    unittest.main()
