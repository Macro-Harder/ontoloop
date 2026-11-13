"""Slice CONSUME tests, list section 2.14.

Rows transcribed from design/steps/step-09-merged-test-list.md section 2.14.
Perspective: whole path behaviour, evidence homes, records, and cross slice
effects. Each product touching test body begins by requiring its product
surface through the shared harness, then states the real assertions from
its row. Stage carried rows call harness.stage_carried with their reason.
"""

import unittest

from tests import harness


class ConsumeT01Tests(unittest.TestCase):
    """CONSUME-T01: discovery returns an explicit no promotion state."""

    def test_no_current_bundle_is_a_normal_answer(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.discover(workflow="review")
        self.assertEqual(result["answer"], "no promotion")
        self.assertFalse(result["is_error"])
        self.assertIsNone(result["bundle"])


class ConsumeT02Tests(unittest.TestCase):
    """CONSUME-T02: a run never observes two bundle versions inside itself."""

    def test_pinning_holds_for_the_run(self):
        mod = harness.require("ontoloop.consumption")
        run = mod.run_with_mid_run_promotion()
        self.assertEqual(len(set(run["observed_bundle_versions"])), 1)
        self.assertEqual(run["observed_bundle_versions"][0], run["pinned_version"])

    def test_attribution_names_the_bundle_version_in_use(self):
        mod = harness.require("ontoloop.consumption")
        run = mod.run_once()
        self.assertEqual(run["attribution"]["bundle_version"], run["pinned_version"])
        self.assertTrue(run["attribution"]["recorded_on_run_record"])


class ConsumeT03Tests(unittest.TestCase):
    """CONSUME-T03: hash mismatch places the bundle in the unloadable position."""

    def test_mismatch_places_bundle_unloadable(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.load_with_hash_mismatch()
        self.assertEqual(result["position"], "unloadable")
        self.assertFalse(result["content_presented"])

    def test_error_names_each_side_and_the_hash_each_side_carried(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.load_with_hash_mismatch()
        error = result["error"]
        self.assertTrue(error["checked_side"])
        self.assertTrue(error["checked_against_side"])
        self.assertNotEqual(error["checked_side_hash"], error["against_side_hash"])
        self.assertEqual(error["checked_side_hash"], result["tool_side_hash"])
        self.assertEqual(error["against_side_hash"], result["presented_hash"])


class ConsumeT04Tests(unittest.TestCase):
    """CONSUME-T04: the mixed fleet window at item S5-O-66."""

    def test_window_behaves_as_the_brief_states_on_a_schema_version_move(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.mixed_fleet_window(bundle_schema_move=True)
        self.assertEqual(result["old_fleet_loads"], result["window_old_fleet_loads"])
        self.assertEqual(result["new_fleet_loads"], result["window_new_fleet_loads"])
        self.assertTrue(result["window_recorded"])

    def test_outside_the_window_the_old_fleet_does_not_load_the_moved_bundle(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.mixed_fleet_window(bundle_schema_move=True, after_window=True)
        self.assertFalse(result["old_fleet_loads"])
        self.assertEqual(result["old_fleet_position"], "unloadable")


class ConsumeT05Tests(unittest.TestCase):
    """CONSUME-T05: holdout content access inventory construction test."""

    def test_inventory_lists_every_component_that_can_read_sealed_holdout(self):
        mod = harness.require("ontoloop.consumption")
        inventory = mod.holdout_content_access_inventory()
        readers = mod.components_that_can_read_sealed_holdout()
        self.assertEqual(sorted(inventory["listed_components"]), sorted(readers))

    def test_candidate_construction_is_named_as_holding_none(self):
        mod = harness.require("ontoloop.consumption")
        inventory = mod.holdout_content_access_inventory()
        entry = inventory["entries"]["candidate construction"]
        self.assertEqual(entry["sealed_holdout_content_held"], "none")

    def test_listed_paths_are_checked_by_construction(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.check_inventory_paths_by_construction()
        self.assertTrue(result["all_listed_paths_checked"])
        self.assertFalse(result["rests_on_behaviour_sampling"])

    def test_completeness_limit_stands_in_the_heading_block(self):
        mod = harness.require("ontoloop.consumption")
        inventory = mod.holdout_content_access_inventory()
        self.assertTrue(inventory["heading_block"]["completeness_limit_stated"])
        self.assertEqual(
            inventory["heading_block"]["completeness_limit"],
            "this inventory can be incomplete, a test of it proves only "
            "the paths tested, and it is not a confinement proof and "
            "proves no Section 7.1 claim",
        )


class ConsumeT06Tests(unittest.TestCase):
    """CONSUME-T06: file presentation standing, fact condition on BQ-41."""

    def test_file_loads_carry_only_the_three_named_standings(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.load_file_presentation()
        self.assertEqual(
            sorted(result["standings_carried"]),
            ["backup", "inspection", "portability"],
        )

    def test_file_copy_is_treated_as_a_cache_that_outlives_withdrawal(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.withdraw_then_read_file_copy()
        self.assertEqual(result["copy_position"], "cache outliving withdrawal")
        self.assertTrue(result["assertions_treat_copy_as_cache"])
        self.assertFalse(result["copy_treated_as_withdrawn"])


class ConsumeT07Tests(unittest.TestCase):
    """CONSUME-T07: provisional loadability opt out, Position 2 at section 13.2."""

    def test_opt_out_places_bundle_current_and_not_loadable_by_opt_out(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.opt_out("workflow a")
        self.assertEqual(result["position"], "current and not loadable by opt out")
        self.assertTrue(result["bundle_stays_current"])
        self.assertFalse(result["pointer_moved"])
        self.assertFalse(result["withdrawal_act_ran"])

    def test_load_attempt_is_refused_in_that_position_and_no_other_wording(self):
        mod = harness.require("ontoloop.consumption")
        mod.opt_out("workflow a")
        result = mod.load("workflow a")
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["refusal_wording"], "current and not loadable by opt out")

    def test_other_workflow_loads_as_before(self):
        mod = harness.require("ontoloop.consumption")
        mod.opt_out("workflow a")
        result = mod.load("workflow b")
        self.assertTrue(result["loaded"])
        self.assertEqual(result["bundle_version"], mod.current_bundle("workflow b"))

    def test_bound_keeps_running_and_no_run_is_attributed_while_opted_out(self):
        mod = harness.require("ontoloop.consumption")
        mod.opt_out("workflow a")
        first = mod.bound_position("workflow a")
        second = mod.bound_position("workflow a", later=True)
        self.assertGreater(second["bound_elapsed"], first["bound_elapsed"])
        self.assertEqual(mod.attributed_runs("workflow a", since="opt out"), [])

    def test_opt_back_in_takes_effect_at_the_next_run_boundary(self):
        mod = harness.require("ontoloop.consumption")
        mod.opt_out("workflow a")
        run = mod.begin_run("workflow a")
        mod.opt_out_off("workflow a")
        self.assertFalse(run["loads_under_opt_back_in"])
        first_after = mod.begin_run("workflow a")
        self.assertTrue(first_after["loaded"])

    def test_bound_after_opt_back_in_is_continuous_with_no_restart(self):
        mod = harness.require("ontoloop.consumption")
        before = mod.bound_position("workflow a")
        mod.opt_out("workflow a")
        mod.opt_out_off("workflow a")
        after = mod.bound_position("workflow a")
        self.assertFalse(after["restart_recorded"])
        self.assertGreaterEqual(after["bound_elapsed"], before["bound_elapsed"])

    def test_refusal_use_position_after_opt_back_in_equals_position_before(self):
        mod = harness.require("ontoloop.consumption")
        for case in ("spent", "unspent"):
            before = mod.refusal_use_position("workflow a", case=case)
            mod.opt_out("workflow a")
            mod.opt_out_off("workflow a")
            after = mod.refusal_use_position("workflow a", case=case)
            self.assertEqual(after, before, case)
        self.assertEqual(mod.refresh_records(at=("opt out", "opt back in")), [])

    def test_failure_counterpart_opt_out_side_effects_fail_the_row(self):
        mod = harness.require("ontoloop.consumption")
        for defect in ("moves the pointer", "affects a second workflow",
                       "stops the bound", "restarts the bound",
                       "takes effect inside a running run"):
            result = mod.opt_out_with_defect(defect)
            self.assertTrue(result["row_failed"], defect)


class ConsumeT08Tests(unittest.TestCase):
    """CONSUME-T08: owing row 5, Agentic artifacts, section 13.3."""

    FIXTURE = "attributed run records with one load refusal case and one qualified load case"

    def test_agentic_owed_in_full_for_each_artifact(self):
        mod = harness.require("ontoloop.consumption")
        for artifact in ("bundle presentation", "tool answers", "load refusal diagnostics"):
            built = mod.build_agentic_artifact(artifact, fixture=self.FIXTURE)
            self.assertTrue(built["agentic_form_present"], artifact)
            self.assertFalse(built["defect"], artifact)

    def test_missing_agentic_form_is_a_defect_in_the_artifact_itself(self):
        mod = harness.require("ontoloop.consumption")
        built = mod.build_agentic_artifact("tool answers", omit="agentic form")
        self.assertEqual(built["defect_home"], "the artifact itself")

    def test_simple_owed_in_reverse_for_a_refusal_or_qualification(self):
        mod = harness.require("ontoloop.consumption")
        for case in ("load refusal", "qualified load"):
            built = mod.build_agentic_artifact("load refusal diagnostics", case=case)
            self.assertTrue(built["simple_wording_for_same_act_present"], case)
            self.assertTrue(built["simple_wording_where_operator_reads_the_act"], case)
            missing = mod.build_agentic_artifact(
                "load refusal diagnostics", case=case, omit="simple wording")
            self.assertEqual(missing["defect_home"], "the artifact itself")

    def test_advanced_counterpart_named_for_an_agentic_figure_or_bound(self):
        mod = harness.require("ontoloop.consumption")
        built = mod.build_agentic_artifact("bundle presentation", with_figure=True)
        self.assertTrue(built["advanced_counterpart_named"])
        self.assertEqual(built["advanced_figure"], built["agentic_figure"])
        missing = mod.build_agentic_artifact(
            "bundle presentation", with_figure=True, omit="advanced counterpart")
        self.assertTrue(missing["row_failed"])

    def test_value_equality_condition_from_subsection_18_55(self):
        mod = harness.require("ontoloop.consumption")
        built = mod.build_agentic_artifact(
            "bundle presentation", with_figure=True, advanced_figure_differs=True)
        self.assertTrue(built["row_failed"])
        self.assertEqual(built["defect_home"], "the artifact itself")


class ConsumeT09Tests(unittest.TestCase):
    """CONSUME-T09: a tool presentation load appends its access event."""

    def test_access_event_stands_on_the_journal_after_the_load(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.tool_presentation_load()
        self.assertTrue(result["loaded"])
        journal = mod.journal_after(result)
        self.assertEqual(journal[-1]["kind"], "access event")
        self.assertEqual(journal[-1]["load"], result["load_identity"])

    def test_load_whose_access_event_append_fails_does_not_proceed(self):
        mod = harness.require("ontoloop.consumption")
        result = mod.tool_presentation_load(access_event_append_fails=True)
        self.assertFalse(result["loaded"])
        self.assertFalse(result["content_presented"])
        self.assertTrue(result["outcome_recorded"])
        self.assertFalse(result["passed_over_in_silence"])
        self.assertEqual(result["outcome_form"], "non silent load outcome")


class ConsumeT10Tests(unittest.TestCase):
    """CONSUME-T10: adversarial audit of the holdout content access inventory.

    Stage carried in the form plan section 6.3 uses: its target is the
    inventory and the access paths of the populated store at the owning
    stages, the Step 15 audit and the Step 19 finished product audit, and
    no fixture result closes it.
    """

    def test_adversarial_inventory_audit_paths_and_payloads(self):
        harness.stage_carried(
            "CONSUME-T10 is stage carried: real target only, the inventory "
            "and access paths of the populated store, owned by the Step 15 "
            "audit and the Step 19 finished product audit; no fixture "
            "result closes it. The row passes for an occasion only where "
            "the audit record at the inventory record names every route "
            "class the search covered, being routes that run through "
            "activities, tuning, calibration, debugging notes, and "
            "derived artifacts, and states for each class either that no "
            "unlisted path was found or the unlisted path found, entered "
            "as a finding against the inventory with the component it "
            "runs through named. For the payload member, the search "
            "covers every legitimately accessed content item in the "
            "inventory version searched, and the record states either "
            "that no payload instruction was found in any item searched "
            "or one finding for each payload instruction found, naming "
            "the item that carried it and the direction it gave; an "
            "audit that searches paths alone stands incomplete."
        )

    def test_two_entry_evidence_home_at_each_occasion(self):
        harness.stage_carried(
            "CONSUME-T10 evidence stands in two entries owed at each "
            "occasion, the inventory search entry in the audit record of "
            "the owning stage and the audit entry at the inventory record; "
            "both are stage records of stages that have not run. Where "
            "the two entries disagree on the inventory version searched, "
            "on a route class covered, or on a path or payload found, "
            "neither entry discharges the act and the audit at that "
            "occasion stands incomplete."
        )

    def test_uncoverable_route_class_leaves_the_row_not_passed(self):
        harness.stage_carried(
            "CONSUME-T10 failure counterpart is stage carried with the "
            "row: where the search cannot cover a route class the row "
            "names, that limit stands recorded in the same audit record "
            "with its reason, the row stands not passed for that "
            "occasion, and no listed paths only check passes the row at "
            "any occasion."
        )


if __name__ == "__main__":
    unittest.main()
