"""Slice SURFACES tests, list section 2.15.

Rows transcribed from design/steps/step-09-merged-test-list.md section 2.15.
Perspective: whole path behaviour, evidence homes, records, and cross slice
effects. Every SURFACES row carries the agent surface protocol revision as
a registered instrument: the revision the first version implements stands
recorded in the SURFACES test record at its first run, and a move on that
axis breaks these rows and they are re performed against the new revision.
"""

import unittest

from tests import harness


def check_protocol_revision_recorded(test, mod):
    record = mod.surfaces_test_record()
    test.assertTrue(record["protocol_revision_recorded_at_first_run"])
    test.assertTrue(record["protocol_revision"])
    test.assertEqual(record["revision_home"], "SURFACES test record")


SURFACES_ROW_IDENTIFIERS = (
    "SURFACES-T01", "SURFACES-T02", "SURFACES-T03",
    "SURFACES-T04", "SURFACES-T05", "SURFACES-T06",
)


def check_revision_move_consequences(test, mod):
    moved = mod.move_protocol_revision()
    test.assertEqual(sorted(moved["broken_rows"]), sorted(SURFACES_ROW_IDENTIFIERS))
    test.assertTrue(moved["new_revision"])
    test.assertNotEqual(moved["new_revision"], moved["old_revision"])
    beside = mod.read_results_beside_each_other(
        old_revision=moved["old_revision"], new_revision=moved["new_revision"])
    test.assertFalse(beside["results_read_beside_each_other"])
    test.assertTrue(beside["reperformance_required_before_any_side_by_side_reading"])
    reperformed = mod.reperform_surfaces_rows(new_revision=moved["new_revision"])
    test.assertEqual(sorted(reperformed["rows_reperformed"]),
                     sorted(SURFACES_ROW_IDENTIFIERS))
    beside_after = mod.read_results_beside_each_other(
        old_revision=moved["old_revision"], new_revision=moved["new_revision"])
    test.assertTrue(beside_after["results_read_beside_each_other"])
    unrecorded = mod.surfaces_result_cited_before_first_run_records_a_revision()
    test.assertTrue(unrecorded["host_revision_named_in_citation"])
    test.assertFalse(unrecorded["cited_without_the_host_revision_it_ran_under"])


class SurfacesT01Tests(unittest.TestCase):
    """SURFACES-T01: the negative list test, by absence, criterion 19 in part."""

    def test_result_recorded_for_every_agent_surface_tool(self):
        mod = harness.require("service_layer")
        results = mod.negative_list_results()
        self.assertEqual(sorted(results), sorted(mod.agent_surface_tools()))
        for tool, entry in results.items():
            self.assertEqual(entry["result_recorded_in"], ["suite", "build stage ship record"], tool)

    def test_promotion_adjacent_powers_absent_not_permission_checked(self):
        mod = harness.require("service_layer")
        for tool in mod.agent_surface_tools():
            entry = mod.negative_list_results()[tool]
            for power in mod.promotion_adjacent_powers():
                self.assertEqual(entry["powers"][power], "absent", (tool, power))
                self.assertNotEqual(entry["powers"][power], "permission denied", (tool, power))

    def test_protocol_revision_recorded(self):
        mod = harness.require("service_layer")
        check_protocol_revision_recorded(self, mod)

    def test_revision_move_breaks_rows_until_they_are_reperformed(self):
        mod = harness.require("service_layer")
        check_revision_move_consequences(self, mod)


class SurfacesT02Tests(unittest.TestCase):
    """SURFACES-T02: no stamping rule is applied by a surface of its own."""

    def test_stamps_arrive_from_the_service_layer_only(self):
        mod = harness.require("service_layer")
        for surface in ("operator surface", "agent surface"):
            result = mod.submit_through(surface, material="same material")
            self.assertEqual(result["stamp_source"], "service layer", surface)
            self.assertFalse(result["surface_applied_own_stamp"], surface)

    def test_same_material_gets_the_same_stamps_across_both_surfaces(self):
        mod = harness.require("service_layer")
        first = mod.submit_through("operator surface", material="same material")
        second = mod.submit_through("agent surface", material="same material")
        self.assertEqual(first["stamps"], second["stamps"])

    def test_protocol_revision_recorded(self):
        mod = harness.require("service_layer")
        check_protocol_revision_recorded(self, mod)

    def test_revision_move_breaks_rows_until_they_are_reperformed(self):
        mod = harness.require("service_layer")
        check_revision_move_consequences(self, mod)


class SurfacesT03Tests(unittest.TestCase):
    """SURFACES-T03: channel stamp wording, fact condition marking."""

    def test_channel_stamps_are_reported_as_channel_records(self):
        mod = harness.require("service_layer")
        report = mod.channel_stamp_report()
        for stamp in report["stamps"]:
            self.assertEqual(stamp["reported_as"], "channel record")

    def test_self_reported_share_is_exposure_never_controlled_exposure(self):
        mod = harness.require("service_layer")
        report = mod.channel_stamp_report()
        self.assertEqual(report["self_reported_share_wording"], "exposure")
        self.assertNotIn("controlled exposure", report["all_wording"])

    def test_corroboration_is_never_worded_as_actor_independence(self):
        mod = harness.require("service_layer")
        report = mod.channel_stamp_report()
        self.assertNotIn("actor independence", report["all_wording"])
        for entry in report["corroboration_entries"]:
            self.assertNotEqual(entry["wording"], "actor independence")

    def test_protocol_revision_recorded(self):
        mod = harness.require("service_layer")
        check_protocol_revision_recorded(self, mod)

    def test_revision_move_breaks_rows_until_they_are_reperformed(self):
        mod = harness.require("service_layer")
        check_revision_move_consequences(self, mod)


class SurfacesT04Tests(unittest.TestCase):
    """SURFACES-T04: no output on either surface carries sealed content."""

    def test_each_output_path_carries_only_the_allowed_kinds(self):
        mod = harness.require("service_layer")
        allowed = {"identities", "counts", "hashes", "reason codes"}
        for surface in ("operator surface", "agent surface"):
            for path in ("error", "log", "progress", "support"):
                output = mod.surface_output(surface, path, sealed_stand_in=True)
                self.assertLessEqual(set(output["kinds_carried"]), allowed, (surface, path))
                self.assertFalse(output["carries_sealed_content"], (surface, path))

    def test_no_row_uses_real_sealed_content(self):
        mod = harness.require("service_layer")
        output = mod.surface_output("agent surface", "error", sealed_stand_in=True)
        self.assertEqual(output["sealed_material_kind"], "stand in material only")

    def test_protocol_revision_recorded(self):
        mod = harness.require("service_layer")
        check_protocol_revision_recorded(self, mod)

    def test_revision_move_breaks_rows_until_they_are_reperformed(self):
        mod = harness.require("service_layer")
        check_revision_move_consequences(self, mod)


class SurfacesT05Tests(unittest.TestCase):
    """SURFACES-T05: conditional treatment at claim 2 of brief Section 7.1."""

    def test_each_flow_carries_the_conditional_treatment(self):
        mod = harness.require("service_layer")
        for flow in ("grading", "ingest", "confirmation"):
            result = mod.flow_conditional_treatment(flow)
            self.assertEqual(result["treatment"], "conditional at claim 2", flow)
            self.assertFalse(result["stated_unconditionally"], flow)

    def test_treatment_applied_per_reach_kind_and_per_object_separately(self):
        mod = harness.require("service_layer")
        for flow in ("grading", "ingest", "confirmation"):
            result = mod.flow_conditional_treatment(flow)
            keys = {(entry["reach_kind"], entry["object"]) for entry in result["entries"]}
            self.assertEqual(len(keys), len(result["entries"]), flow)
            for entry in result["entries"]:
                self.assertTrue(entry["own_conditional_entry"], flow)

    def test_protocol_revision_recorded(self):
        mod = harness.require("service_layer")
        check_protocol_revision_recorded(self, mod)

    def test_revision_move_breaks_rows_until_they_are_reperformed(self):
        mod = harness.require("service_layer")
        check_revision_move_consequences(self, mod)


class SurfacesT06Tests(unittest.TestCase):
    """SURFACES-T06: the override fault injection test, subsection 16.29 item two."""

    def test_kill_between_access_record_append_and_content_return(self):
        mod = harness.require("service_layer")
        result = mod.override_kill_between_append_and_return()
        self.assertEqual(result["harness_entry"], "kill between access record append and any content return")
        self.assertFalse(result["content_returned"])

    def test_journal_shows_access_record_stands_and_spend_mark_matches(self):
        mod = harness.require("service_layer")
        result = mod.override_kill_between_append_and_return()
        journal = mod.verify_from_journal(result)
        self.assertTrue(journal["access_record_stands"])
        self.assertEqual(journal["spend_mark"], journal["access_record"]["spend_mark"])
        self.assertFalse(journal["content_returned"])

    def test_evidence_in_both_homes(self):
        mod = harness.require("service_layer")
        result = mod.override_kill_between_append_and_return()
        self.assertEqual(sorted(result["evidence_homes"]), ["build stage ship record", "suite result"])

    def test_protocol_revision_recorded(self):
        mod = harness.require("service_layer")
        check_protocol_revision_recorded(self, mod)

    def test_revision_move_breaks_rows_until_they_are_reperformed(self):
        mod = harness.require("service_layer")
        check_revision_move_consequences(self, mod)


if __name__ == "__main__":
    unittest.main()
