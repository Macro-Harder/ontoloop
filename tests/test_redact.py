"""Slice REDACT, list section 2.9, plan section 6.5 and section 13.2.

Failure and boundary perspective: these tests prize the refusal and
boundary outcomes the rows state: no unredacted journal record at any
moment, the depth 3 boundary at layer 4 with its two distinguished
outcomes, the queue defect firing boundaries of Example C, whole
assembly refusal at the exit scan, and the posture flag behaviour of
REDACT-T08 in its subsection 16.59 amended form.

Standing rule for REDACT-T08: its tests are written on its flag
behaviour only, in the amended two flag form: the store level
posture state and the per build flag. No test in this file is
written on the weakened ingest quantity figure limb of that row,
which stands marked not stated in the plan and mapped in form only.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.redact, with function names taken from the behaviour
wording of each row. The DATASET and REPORT call points of
REDACT-T08 are exercised through the flag values the redact module
supplies to those build points, as the amended row states the
derivation. Fields a row does not state are not invented.
"""

import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.redact"

SIX_LAYERS = (1, 2, 3, 4, 5, 6)
FOUR_ASSEMBLIES = (
    "export",
    "bundle writing",
    "dataset construction",
    "report construction",
)


class TestRedactT01(unittest.TestCase):
    """REDACT-T01: no journal record in unredacted form, ever."""

    def test_journal_bytes_hold_no_unredacted_definite_hit(self):
        module = require(MODULE)
        journal = module.journal_after_definite_hit_appends()
        for shape in module.secret_bearing_shapes():
            self.assertNotIn(shape["raw_bytes"], journal["bytes"])

    def test_scan_runs_after_the_appends_themselves(self):
        module = require(MODULE)
        journal = module.journal_after_definite_hit_appends()
        self.assertEqual(journal["scan_point"], "after appends")


class TestRedactT02(unittest.TestCase):
    """REDACT-T02: one shared classification rule per layer."""

    def test_classification_follows_the_one_shared_rule_per_layer(self):
        module = require(MODULE)
        result = module.classify_corpus_shapes()
        for layer in SIX_LAYERS:
            self.assertEqual(
                result["layers"][layer]["rule"],
                module.shared_rule(layer),
            )

    def test_per_layer_firing_records_for_all_six_layers_one_engine(self):
        module = require(MODULE)
        result = module.classify_corpus_shapes()
        self.assertEqual(result["engine_count"], 1)
        for layer in SIX_LAYERS:
            self.assertIn(layer, result["firing_records"])


class TestRedactT03(unittest.TestCase):
    """REDACT-T03: placeholders typed, stable, run scoped."""

    def test_placeholders_are_typed(self):
        module = require(MODULE)
        run = module.run_with_definite_hit("run one")
        for placeholder in run["placeholders"]:
            self.assertTrue(placeholder["type"])

    def test_placeholders_are_stable_within_a_run(self):
        module = require(MODULE)
        run = module.run_with_definite_hit("run one")
        first = run["placeholder_for_hit"]
        again = module.placeholder_for_same_hit(run)
        self.assertEqual(first, again)

    def test_placeholders_are_never_reused_across_runs(self):
        module = require(MODULE)
        one = module.run_with_definite_hit("run one")
        two = module.run_with_definite_hit("run two")
        self.assertNotEqual(
            one["placeholder_for_hit"], two["placeholder_for_hit"]
        )
        self.assertEqual(one["scope"], "run one")
        self.assertEqual(two["scope"], "run two")


class TestRedactT04(unittest.TestCase):
    """REDACT-T04: layer 4 decoding to depth 3, two outcomes split."""

    def test_decoding_runs_to_depth_3(self):
        module = require(MODULE)
        candidate = module.decoded_candidate("raised at depth 3")
        self.assertEqual(candidate["decoding_depth_reached"], 3)
        self.assertTrue(candidate["decoding_round_fields"])

    def test_depth_out_on_a_raised_candidate_is_an_uncertain_hit(self):
        module = require(MODULE)
        candidate = module.decoded_candidate("depth runs out raised")
        self.assertEqual(candidate["outcome"], "uncertain hit")

    def test_depth_limited_pass_where_no_layer_raised_the_value(self):
        module = require(MODULE)
        candidate = module.decoded_candidate("depth runs out unraised")
        self.assertEqual(candidate["outcome"], "depth limited pass")
        self.assertNotEqual(candidate["outcome"], "uncertain hit")


class TestRedactT05(unittest.TestCase):
    """REDACT-T05: queue defect boundaries, Example C, guessed."""

    def test_30_over_120_fires(self):
        module = require(MODULE)
        result = module.queue_defect_check(30, 120)
        self.assertTrue(result["fires"])

    def test_20_over_120_does_not_fire(self):
        module = require(MODULE)
        result = module.queue_defect_check(20, 120)
        self.assertFalse(result["fires"])

    def test_30_over_10000_growth_test_is_the_operative_check(self):
        module = require(MODULE)
        result = module.queue_defect_check(30, 10000)
        self.assertEqual(result["operative_check"], "growth test")
        self.assertTrue(result["uses_cumulative_divisor"])

    def test_every_figure_is_labelled_guessed(self):
        module = require(MODULE)
        result = module.queue_defect_check(30, 120)
        self.assertEqual(result["source_class"], "guessed")


class TestRedactT06(unittest.TestCase):
    """REDACT-T06: exit scan refuses whole, and refuses no scan."""

    def test_each_governed_assembly_is_scanned(self):
        module = require(MODULE)
        result = module.exit_scan_over_assemblies()
        self.assertEqual(set(result["assemblies"]), set(FOUR_ASSEMBLIES))

    def test_assembly_with_an_uncleared_hit_is_refused_whole(self):
        module = require(MODULE)
        outcome = module.exit_scan(module.assembly_with_planted_hit())
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_a_scan_that_cannot_run_refuses_the_exit_in_form(self):
        module = require(MODULE)
        outcome = module.exit_scan(module.assembly_scan_cannot_run())
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")


class TestRedactT07(unittest.TestCase):
    """REDACT-T07: clearing routes, refusal state, BQ-43 adopted."""

    def test_clearing_by_rescan_lands_its_record(self):
        module = require(MODULE)
        outcome = module.clear_by_rescan(module.uncertain_hit_case())
        self.assertTrue(outcome["record_landed"])
        self.assertTrue(outcome["strength_condition_met"])

    def test_clearing_by_operator_decision_lands_its_record(self):
        module = require(MODULE)
        outcome = module.clear_by_operator_decision(
            module.uncertain_hit_case()
        )
        self.assertTrue(outcome["record_landed"])
        self.assertTrue(outcome["decision_recorded"])

    def test_refusal_state_reopening_and_bound_expiry_behave(self):
        module = require(MODULE)
        outcome = module.refusal_state_lifecycle()
        self.assertTrue(outcome["refusal_state_held"])
        self.assertTrue(outcome["reopening_behaves"])
        self.assertTrue(outcome["bound_expiry_behaves"])

    def test_bq43_marking_carried_at_all_three_named_places(self):
        module = require(MODULE)
        places = module.bq43_marking_places()
        self.assertEqual(
            set(places),
            {"act bar", "intake accounting use", "clearing bound"},
        )
        for marking in places.values():
            self.assertEqual(marking["form"], "adopted")
            self.assertEqual(
                marking["quarantine"], "build exclusion"
            )

    def test_no_redaction_parameter_below_the_floor(self):
        module = require(MODULE)
        floor = module.redaction_floor()
        for parameter in module.redaction_parameters():
            self.assertGreaterEqual(parameter["value"], floor)


class TestRedactT08(unittest.TestCase):
    """REDACT-T08, Amendment 1, subsection 16.59 amended form.

    Flag behaviour only: the store level posture state and the per
    build flag. No test here touches the quantity figure limb.
    Fixture: the authored weaken, ingest, restore, build sequence.
    """

    def test_store_level_state_set_by_the_weakening_act_itself(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        at_weaken = module.posture_state_at(sequence, "after weaken")
        self.assertTrue(at_weaken["store_level_state_set"])

    def test_store_level_state_set_before_any_restore(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        at_weaken = module.posture_state_at(sequence, "after weaken")
        at_restore = module.posture_state_at(sequence, "after restore")
        self.assertTrue(at_weaken["store_level_state_set"])
        self.assertTrue(at_restore["store_level_state_set"])

    def test_restoring_the_layer_does_not_discharge_the_state(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        at_restore = module.posture_state_at(sequence, "after restore")
        self.assertTrue(at_restore["store_level_state_set"])
        self.assertFalse(at_restore["discharged"])

    def test_the_state_is_not_a_toggle_and_has_no_off_act(self):
        module = require(MODULE)
        state = module.store_level_posture_state()
        self.assertFalse(state["is_toggle"])
        self.assertIsNone(state["off_act"])

    def test_dataset_build_with_weakened_material_carries_the_flag(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        build = module.dataset_build_for_sequence(sequence)
        self.assertTrue(build["per_build_flag"])

    def test_loop_report_carries_the_flag_in_the_builds_view(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        build = module.dataset_build_for_sequence(sequence)
        report = module.loop_report_for_build(build)
        self.assertTrue(report["per_build_flag"])
        self.assertEqual(report["flag_view"], report["build_view"])

    def test_control_build_carries_no_flag_while_state_stands_on(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        control = module.control_build_in_same_store(sequence)
        self.assertFalse(control["per_build_flag"])
        self.assertTrue(control["store_level_state_may_stand"])

    def test_store_level_state_is_never_printed_on_an_artifact(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        build = module.dataset_build_for_sequence(sequence)
        report = module.loop_report_for_build(build)
        for artifact in (build, report):
            self.assertNotIn("store_level_state", artifact["printed"])

    def test_flag_is_derived_from_ingest_posture_stamps_alone(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        build = module.dataset_build_for_sequence(sequence)
        stamps = module.ingest_posture_stamps(build["material"])
        self.assertEqual(
            build["per_build_flag"],
            module.per_build_flag_from_stamps(stamps),
        )
        self.assertEqual(build["posture_computations"], 1)

    def test_state_stands_on_before_the_purge_completes(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        before = module.posture_state_at(sequence, "before purge")
        self.assertTrue(before["store_level_state_set"])
        self.assertFalse(before["discharged"])

    def test_discharge_after_every_weakened_record_is_purged(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        after = module.posture_after_tombstone_and_purge(sequence)
        self.assertTrue(after["discharge_recorded"])
        self.assertFalse(after["store_level_state_set"])

    def test_discharge_is_by_material_and_in_no_other_way(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        partial = module.posture_after_partial_purge(sequence)
        self.assertTrue(partial["store_level_state_set"])
        self.assertFalse(partial["discharged"])

    def test_omitted_flag_for_weakened_material_fails_the_row(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        build = module.dataset_build_for_sequence(sequence)
        stripped = dict(build)
        stripped["per_build_flag"] = False
        defects = module.check_posture_travel(build, stripped)
        self.assertTrue(defects)

    def test_weakening_act_without_the_state_set_fails_at_the_act(self):
        module = require(MODULE)
        act = module.weakening_act_record(without_state=True)
        defects = module.check_weakening_act(act)
        self.assertTrue(defects)
        self.assertEqual(defects[0]["point"], "the act")

    def test_restore_obligation_reads_the_store_level_state(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        obligation = module.restore_obligation_for_sequence(sequence)
        self.assertTrue(obligation["reads_store_level_posture_state"])
        self.assertEqual(
            obligation["state_read"], "store level posture state"
        )

    def test_discharge_recorded_in_posture_record_at_build_point(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        check = module.discharge_check_at(sequence, "dataset build point")
        self.assertTrue(check["check_ran"])
        self.assertEqual(check["record_home"], "store posture record")
        self.assertTrue(check["discharge_recorded_in_store_posture_record"])

    def test_discharge_recorded_in_posture_record_at_purge_end(self):
        module = require(MODULE)
        sequence = module.posture_fixture_sequence()
        check = module.discharge_check_at(sequence, "purge completion")
        self.assertTrue(check["check_ran"])
        self.assertEqual(check["record_home"], "store posture record")
        self.assertTrue(check["discharge_recorded_in_store_posture_record"])


class TestRedactFixR1(unittest.TestCase):
    """Fix round 1: content scanning, classification, decoding.

    Written test first for the COR cures of S15-R1-056,
    S15-R1-057, S15-R1-058, S15-R1-061, and S15-R1-063: the
    exit scan scans content and fails closed, the
    classification act classifies the material passed, the
    decoding act computes its depth over a real candidate,
    the redacting append path writes through the store
    append, and placeholders name the layer and class that
    fired.
    """

    def test_exit_scan_fails_closed_on_an_unknown_state(self):
        module = require(MODULE)
        outcome = module.exit_scan({"assembly_state": "some unknown state"})
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def test_exit_scan_fails_closed_on_an_empty_mapping_and_on_none(self):
        module = require(MODULE)
        for assembly in ({}, None):
            outcome = module.exit_scan(assembly)
            self.assertTrue(outcome["refused"])
            self.assertEqual(
                outcome["form"], "no exit scan result, no exit"
            )

    def test_exit_scan_refuses_an_assembly_carrying_definite_hit_bytes(self):
        module = require(MODULE)
        shape = module.secret_bearing_shapes()[0]
        outcome = module.exit_scan({"content": shape["raw_bytes"]})
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])
        outcome = module.exit_scan(shape["raw_bytes"])
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")

    def test_exit_scan_releases_scannable_clean_content(self):
        module = require(MODULE)
        outcome = module.exit_scan({"content": "an ordinary record line"})
        self.assertFalse(outcome["refused"])

    def test_classification_act_classifies_the_material_passed(self):
        module = require(MODULE)
        hit = module.classify_material("password = SyntheticValue123")
        fired = [
            record
            for records in hit["firing_records"].values()
            for record in records
        ]
        self.assertTrue(
            any(record["outcome"] == "definite" for record in fired)
        )
        plain = module.classify_material("a routine note about lunch")
        plain_fired = [
            record
            for records in plain["firing_records"].values()
            for record in records
        ]
        self.assertFalse(
            any(record["outcome"] == "definite" for record in plain_fired)
        )
        self.assertNotEqual(hit["firing_records"], plain["firing_records"])
        self.assertEqual(hit["engine_count"], 1)
        for layer in SIX_LAYERS:
            self.assertEqual(
                hit["layers"][layer]["rule"], module.shared_rule(layer)
            )

    def test_classify_corpus_shapes_records_per_layer_firings(self):
        module = require(MODULE)
        result = module.classify_corpus_shapes()
        self.assertEqual(result["engine_count"], 1)
        for layer in SIX_LAYERS:
            self.assertIn(layer, result["firing_records"])
            self.assertIsInstance(result["firing_records"][layer], list)
            for record in result["firing_records"][layer]:
                self.assertIn(record["outcome"], ("definite", "uncertain"))
                self.assertEqual(record["layer"], layer)

    def test_decoding_computes_depth_over_a_real_candidate(self):
        import base64
        import urllib.parse

        module = require(MODULE)
        hit = "password = SyntheticValue123"
        layer_one = urllib.parse.quote(hit, safe="")
        layer_two = layer_one.encode("utf-8").hex()
        candidate = base64.b64encode(
            layer_two.encode("utf-8")
        ).decode("ascii")
        result = module.decoded_candidate(candidate)
        self.assertEqual(result["decoding_depth_reached"], 3)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(len(result["decoding_round_fields"]), 3)
        plain = module.decoded_candidate("a routine note")
        self.assertEqual(plain["decoding_depth_reached"], 0)
        self.assertEqual(plain["outcome"], "depth limited pass")

    def test_redacting_append_path_writes_through_the_store_append(self):
        module = require(MODULE)
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        before = len(store["records"])
        outcome = module.append_redacted(
            store, "password = SyntheticValue123", scope="run one"
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(len(store["records"]), before + 1)
        journal = b"\n".join(
            record["canonical_bytes"] for record in store["records"]
        )
        self.assertNotIn(b"SyntheticValue123", journal)
        self.assertTrue(outcome["placeholders"])
        for placeholder in outcome["placeholders"]:
            self.assertIn("layer", placeholder)

    def test_journal_after_appends_comes_from_a_real_store_journal(self):
        module = require(MODULE)
        journal = module.journal_after_definite_hit_appends()
        self.assertEqual(journal["scan_point"], "after appends")
        self.assertIn(b"redacted placeholder", journal["bytes"])
        for shape in module.secret_bearing_shapes():
            self.assertNotIn(shape["raw_bytes"], journal["bytes"])

    def test_placeholders_name_the_layer_and_class_that_fired(self):
        module = require(MODULE)
        run = module.run_with_definite_hit("run one")
        for placeholder in run["placeholders"]:
            self.assertIn("layer 2", placeholder["type"])
            self.assertIn("private_key_block_headers", placeholder["type"])
        self.assertIn(
            "private_key_block_headers", run["placeholder_for_hit"]
        )


class TestRedactFixR2(unittest.TestCase):
    """Fix round 2: exit scan content, zero byte content, append spans.

    Written test first for the three charges of region 4 in
    the Round 2 triage: ruling 5, Chair F-1, the exit scan
    label branch removed and the planted hit fixture case
    re-founded on scannable content as a recorded test act;
    R2-CR-1, the redacting append path acting on every
    definite firing record, not on layer 2 pattern spans
    alone; and R2-CR-2, content at zero bytes in total
    standing in the no scannable content position.
    """

    def test_planted_hit_fixture_carries_scannable_definite_hit_content(self):
        module = require(MODULE)
        fixture = module.assembly_with_planted_hit()
        content = [
            value
            for key, value in fixture.items()
            if key != "assembly_state"
        ]
        self.assertTrue(content)
        result = module.classify_material(content)
        fired = [
            record
            for records in result["firing_records"].values()
            for record in records
        ]
        self.assertTrue(
            any(record["outcome"] == "definite" for record in fired)
        )
        outcome = module.exit_scan(fixture)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_exit_scan_old_label_beside_clean_content_decides_on_content(self):
        module = require(MODULE)
        outcome = module.exit_scan(
            {
                "assembly_state": "planted uncleared hit",
                "content": "an ordinary record line",
            }
        )
        self.assertFalse(outcome["refused"])

    def test_exit_scan_old_label_beside_hit_content_refuses_whole(self):
        module = require(MODULE)
        shape = module.secret_bearing_shapes()[0]
        outcome = module.exit_scan(
            {
                "assembly_state": "planted uncleared hit",
                "content": shape["raw_bytes"],
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_exit_scan_old_label_alone_fails_closed(self):
        module = require(MODULE)
        outcome = module.exit_scan(
            {"assembly_state": "planted uncleared hit"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def test_exit_scan_zero_byte_content_fails_closed(self):
        module = require(MODULE)
        for assembly in (
            {"content": ""},
            {"content": b""},
            [""],
        ):
            outcome = module.exit_scan(assembly)
            self.assertTrue(outcome["refused"])
            self.assertEqual(
                outcome["form"], "no exit scan result, no exit"
            )

    def test_exit_scan_clean_non_empty_content_still_releases(self):
        module = require(MODULE)
        outcome = module.exit_scan({"content": "an ordinary record line"})
        self.assertFalse(outcome["refused"])

    def test_append_redacts_layer_5_declaration_form_material(self):
        module = require(MODULE)
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        before = len(store["records"])
        material = "credential type: plain words only"
        outcome = module.append_redacted(store, material, scope="run one")
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome.get("refused", False))
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertEqual(len(store["records"]), before + 1)
        self.assertNotIn(material, outcome["redacted_material"])
        self.assertNotIn("plain words only", outcome["redacted_material"])
        self.assertTrue(
            any(
                "layer 5" in placeholder
                and "credential type field" in placeholder
                for placeholder in outcome["placeholders"]
            )
        )
        journal = b"\n".join(
            record["canonical_bytes"] for record in store["records"]
        )
        self.assertNotIn(material.encode("utf-8"), journal)

    def test_append_redacts_each_governed_definite_hit_shape_once(self):
        module = require(MODULE)
        store_module = require("ontoloop.store")
        for shape in module.secret_bearing_shapes():
            store = store_module.golden_record_store()
            material = shape["raw_bytes"].decode("utf-8")
            outcome = module.append_redacted(
                store, material, scope="run one"
            )
            self.assertTrue(outcome["appended"])
            self.assertEqual(outcome["hits_redacted"], 1)
            self.assertNotIn(material, outcome["redacted_material"])
            journal = b"\n".join(
                record["canonical_bytes"] for record in store["records"]
            )
            self.assertNotIn(shape["raw_bytes"], journal)

    def test_append_clean_material_unchanged(self):
        module = require(MODULE)
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        material = "a routine note about lunch"
        outcome = module.append_redacted(store, material, scope="run one")
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["placeholders"], [])
        self.assertEqual(outcome["redacted_material"], material)

    def test_append_refused_where_a_definite_record_has_no_span(self):
        module = require(MODULE)
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        before = len(store["records"])
        outcome = module.append_redacted(
            store, {"password": "x"}, scope="run one"
        )
        self.assertFalse(outcome["appended"])
        self.assertFalse(outcome["reported_appended"])
        self.assertTrue(outcome.get("refused"))
        self.assertEqual(len(store["records"]), before)


class TestRedactFixR3Cycle(unittest.TestCase):
    """Fix round 3, ruling 8: cyclic gathering fails closed.

    Written test first for S15-R3-008. The recursive content
    gathering through exit_scan and through classify_material
    detects a cycle on its path and the surfaces return the
    REDACT-T06 fail closed form, refused True with form
    standing at no exit scan result, no exit, on cyclic
    input, beside the standing acyclic cases and the deep
    finite nesting cases.
    """

    def test_exit_scan_self_referential_list_fails_closed(self):
        module = require(MODULE)
        material = []
        material.append(material)
        outcome = module.exit_scan(material)
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_exit_scan_self_referential_mapping_fails_closed(self):
        module = require(MODULE)
        material = {}
        material["self"] = material
        outcome = module.exit_scan(material)
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_classify_material_self_referential_list_fails_closed(self):
        module = require(MODULE)
        material = []
        material.append(material)
        outcome = module.classify_material(material)
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_exit_scan_mutually_referential_material_fails_closed(self):
        module = require(MODULE)
        first = []
        second = {"inner": first}
        first.append(second)
        outcome = module.exit_scan(first)
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_exit_scan_deep_finite_nesting_still_decides_clean(self):
        module = require(MODULE)
        for depth in (100, 300, 500):
            material = "a routine clean note"
            for _ in range(depth):
                material = [material]
            outcome = module.exit_scan(material)
            self.assertFalse(outcome["refused"])

    def test_exit_scan_shared_acyclic_content_still_decides_clean(self):
        module = require(MODULE)
        shared = ["a routine clean note"]
        outcome = module.exit_scan([shared, shared, {"again": shared}])
        self.assertFalse(outcome["refused"])


class TestRedactFixR3State(unittest.TestCase):
    """Fix round 3, ruling 18: state key gathering and state gate.

    Written test first for S15-R3-017. The gathering act
    skips only the state label value at the top level
    position the stated form names, and gathers content
    standing under any other key at any depth, including
    a repeated assembly_state key below the top level.
    An assembly whose state the act does not know stands
    decided by its content where scannable content
    stands, and returns the fail closed form only where
    no scannable content stands.
    """

    def test_hit_under_nested_assembly_state_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "content": "a routine clean note",
                "nested": {"assembly_state": hit},
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_under_ordinary_key_control_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "content": "a routine clean note",
                "nested": {"ordinary": hit},
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_under_deeply_nested_assembly_state_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "content": "a routine clean note",
                "outer": [{"inner": {"assembly_state": hit}}],
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")

    def test_clean_content_under_nested_assembly_state_releases(self):
        module = require(MODULE)
        outcome = module.exit_scan(
            {
                "content": "a routine clean note",
                "nested": {"assembly_state": "a routine clean note"},
            }
        )
        self.assertFalse(outcome["refused"])

    def test_top_level_state_label_value_alone_does_not_decide(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {"assembly_state": hit, "content": "a routine clean note"}
        )
        self.assertFalse(outcome["refused"])

    def test_unknown_state_with_clean_content_decides_clean(self):
        module = require(MODULE)
        outcome = module.exit_scan(
            {
                "assembly_state": "ready",
                "content": "a routine clean note",
            }
        )
        self.assertFalse(outcome["refused"])

    def test_unknown_state_with_hit_content_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {"assembly_state": "ready", "content": hit}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_unknown_state_with_no_scannable_content_fails_closed(self):
        module = require(MODULE)
        for assembly in (
            {"assembly_state": "ready"},
            {"assembly_state": "ready", "content": ""},
            {"assembly_state": "a state nobody named"},
        ):
            outcome = module.exit_scan(assembly)
            self.assertTrue(outcome["refused"])
            self.assertEqual(
                outcome["form"], "no exit scan result, no exit"
            )

    def test_standing_governed_forms_still_hold(self):
        module = require(MODULE)
        cannot = module.exit_scan(module.assembly_scan_cannot_run())
        self.assertTrue(cannot["refused"])
        self.assertEqual(
            cannot["form"], "no exit scan result, no exit"
        )
        planted = module.exit_scan(module.assembly_with_planted_hit())
        self.assertTrue(planted["refused"])
        self.assertEqual(planted["refused_scope"], "whole")
        clean = module.exit_scan({"content": "a routine clean note"})
        self.assertFalse(clean["refused"])


class TestRedactFixR4Keys(unittest.TestCase):
    """Fix round 4, ruling 33: mapping keys gathered as content.

    Written test first for S15-R4-017. The gathering act in
    redact.py gathers mapping keys as content beside mapping
    values, so hit bytes standing as a mapping key, top level
    and nested, refuse whole exactly as the same bytes
    standing as a value do, and ordinary assemblies stand
    unchanged.
    """

    def test_hit_bytes_as_top_level_key_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {hit: "a routine clean note", "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_text_as_top_level_key_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                hit.decode("utf-8"): "a routine clean note",
                "content": "a routine clean note",
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_bytes_as_nested_key_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "content": "a routine clean note",
                "nested": {hit: "a routine clean note"},
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_bytes_as_key_nested_through_a_list_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "content": "a routine clean note",
                "outer": [{"inner": {hit: "a routine clean note"}}],
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_bytes_inside_a_tuple_key_refuse_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                (hit, "a routine clean note"): "a routine clean note",
                "content": "a routine clean note",
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_same_hit_as_a_value_control_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {"a routine clean note": hit, "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_clean_key_carrying_a_hit_value_still_refuses_whole(self):
        module = require(MODULE)
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan({"note": hit})
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_ordinary_assemblies_unchanged(self):
        module = require(MODULE)
        clean = module.exit_scan(
            {"note": "a routine clean note", "other": "another clean note"}
        )
        self.assertFalse(clean["refused"])
        numeric_key = module.exit_scan({1: "a routine clean note"})
        self.assertFalse(numeric_key["refused"])
        state_only = module.exit_scan({"assembly_state": "ready"})
        self.assertTrue(state_only["refused"])
        self.assertEqual(
            state_only["form"], "no exit scan result, no exit"
        )
        zero_byte = module.exit_scan({"content": ""})
        self.assertTrue(zero_byte["refused"])
        self.assertEqual(
            zero_byte["form"], "no exit scan result, no exit"
        )


class TestRedactFixR4DeepNesting(unittest.TestCase):
    """Fix round 4, ruling 25: deep nesting fails closed.

    Written test first for N-07. The gathering surfaces
    return the fail closed form where the gathering
    raises RecursionError, in the same catch position
    that catches the cycle signal, beside the standing
    deep nesting cases still deciding on their content
    and the standing cycle forms unchanged.
    """

    def _nested_list(self, depth):
        material = "a routine clean note"
        for _ in range(depth):
            material = [material]
        return material

    def _nested_mapping(self, depth):
        material = "a routine clean note"
        for _ in range(depth):
            material = {"inner": material}
        return material

    def test_exit_scan_deep_list_nesting_fails_closed(self):
        module = require(MODULE)
        outcome = module.exit_scan(self._nested_list(1500))
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_exit_scan_deep_mapping_nesting_fails_closed(self):
        module = require(MODULE)
        outcome = module.exit_scan(self._nested_mapping(1500))
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_classify_material_deep_list_nesting_fails_closed(self):
        module = require(MODULE)
        outcome = module.classify_material(self._nested_list(1500))
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_classify_material_deep_mapping_nesting_still_classifies(self):
        # Protecting pin, stated on first hand evidence: in
        # _material_items a mapping stands as a leaf, its
        # values standing in string form, so deep mapping
        # nesting raises nothing on this surface and the
        # classification returns its governed form.
        module = require(MODULE)
        outcome = module.classify_material(self._nested_mapping(1500))
        self.assertIn("firing_records", outcome)
        self.assertIn("layers", outcome)

    def test_append_redacted_deep_list_nesting_refuses(self):
        module = require(MODULE)
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        before = len(store["records"])
        outcome = module.append_redacted(store, self._nested_list(1500))
        self.assertFalse(outcome["appended"])
        self.assertFalse(outcome["reported_appended"])
        self.assertTrue(outcome["refused"])
        self.assertIsNone(outcome["redacted_material"])
        self.assertEqual(outcome["placeholders"], [])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(len(store["records"]), before)

    def test_append_redacted_deep_mapping_nesting_still_appends(self):
        # Protecting pin on the same evidence as the
        # classification pin above: mapping material gathers
        # in string form, raises nothing, and clean material
        # in that form appends in the standing form.
        module = require(MODULE)
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        before = len(store["records"])
        outcome = module.append_redacted(
            store, self._nested_mapping(1500)
        )
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(len(store["records"]), before + 1)

    def test_standing_deep_nesting_still_decides_on_content(self):
        module = require(MODULE)
        for depth in (100, 300, 500):
            scanned = module.exit_scan(self._nested_list(depth))
            self.assertFalse(scanned["refused"])
            classified = module.classify_material(
                self._nested_list(depth)
            )
            self.assertIn("firing_records", classified)
            self.assertIn("layers", classified)

    def test_cycle_forms_unchanged_beside_the_depth_form(self):
        module = require(MODULE)
        cyclic = []
        cyclic.append(cyclic)
        scanned = module.exit_scan(cyclic)
        self.assertTrue(scanned["refused"])
        self.assertEqual(
            scanned["form"], "no exit scan result, no exit"
        )
        classified = module.classify_material(cyclic)
        self.assertTrue(classified["refused"])
        self.assertEqual(
            classified["form"], "no exit scan result, no exit"
        )
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        before = len(store["records"])
        appended = module.append_redacted(store, cyclic)
        self.assertFalse(appended["appended"])
        self.assertTrue(appended["refused"])
        self.assertEqual(len(store["records"]), before)


if __name__ == "__main__":
    unittest.main()
