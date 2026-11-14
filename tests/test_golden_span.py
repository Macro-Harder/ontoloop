"""Slice GOLDEN-SPAN, list section 2.8, plan section 6.5.

Failure and boundary perspective: these tests prize exact re reading
under the current schema version, the no merge boundary across a
signature version change, and the rule that automatic regeneration
is never evidence for a golden record.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.golden_span, with function names taken from the behaviour
wording of each row. Fields a row does not state are not invented.
GOLDEN-T04 states stage record evidence as its evidence home, so its
tests stand stage carried with that reason, never skipped and never
passed at this step.
"""

import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.golden_span"

STAGE_REASON_T04 = (
    "GOLDEN-T04 evidence home is stage record evidence: the suite "
    "standing as a runnable artifact before DATASET grouping work "
    "opens is a stage act, read from the stage record."
)


class TestGoldenT01(unittest.TestCase):
    """GOLDEN-T01: one real shaped record per type per version."""

    def test_one_record_per_type_per_schema_version_exists(self):
        module = require(MODULE)
        golden = module.golden_record_sets()
        for record_type in golden["record_types"]:
            for version in golden["schema_versions"]:
                self.assertIn((record_type, version), golden["records"])

    def test_each_record_re_reads_under_the_current_schema_version(self):
        module = require(MODULE)
        golden = module.golden_record_sets()
        for key, record in golden["records"].items():
            reread = module.re_read(record)
            self.assertTrue(reread["read"])
            self.assertEqual(reread["record"], record)


class TestGoldenT02(unittest.TestCase):
    """GOLDEN-T02: the spanning group regression suite."""

    def test_suite_runs_in_the_ordinary_test_run(self):
        module = require(MODULE)
        result = module.run_spanning_suite()
        self.assertTrue(result["ran_in_ordinary_run"])

    def test_external_task_identity_groups_across_version_change(self):
        module = require(MODULE)
        result = module.run_spanning_suite()
        shape = result["shapes"]["external task identity grouping"]
        self.assertTrue(shape["grouped_across_signature_version_change"])

    def test_no_merge_of_signature_based_groups_across_the_change(self):
        module = require(MODULE)
        result = module.run_spanning_suite()
        shape = result["shapes"]["signature based groups"]
        self.assertFalse(shape["merged_across_signature_version_change"])

    def test_pool_stamp_consequences_are_checked(self):
        module = require(MODULE)
        result = module.run_spanning_suite()
        self.assertTrue(result["pool_stamp_consequences_checked"])
        for row in result["rows"]:
            self.assertIn("pool_stamp", row)
            self.assertIn("outcome", row)

    def test_counted_evidence_home_is_the_suite_result_record(self):
        module = require(MODULE)
        result = module.run_spanning_suite()
        home = result["evidence_home"]
        self.assertEqual(home["counted_record"], "suite result record")
        self.assertTrue(home["stands_under_one_counted_row"])

    def test_migration_record_is_cited_by_pointer_at_each_run(self):
        module = require(MODULE)
        result = module.run_spanning_suite()
        self.assertTrue(result["migration_runs"])
        for run in result["migration_runs"]:
            self.assertEqual(
                run["migration_occasion_record_citation"], "by pointer"
            )

    def test_pointer_citation_of_migration_record_demotes_nothing(self):
        module = require(MODULE)
        result = module.run_spanning_suite()
        home = result["evidence_home"]
        self.assertFalse(home["citation_demotes_migration_record"])

    def test_migration_record_remains_a_home_in_its_own_right(self):
        module = require(MODULE)
        result = module.run_spanning_suite()
        home = result["evidence_home"]
        self.assertTrue(
            home["migration_occasion_record_remains_evidence_home"]
        )


class TestGoldenT03(unittest.TestCase):
    """GOLDEN-T03: blessing is a named act, never automatic."""

    def test_re_blessed_record_is_recorded_as_re_blessed_by_that_act(self):
        module = require(MODULE)
        record = module.re_bless(module.golden_record())
        self.assertEqual(record["blessing"]["act"], "re blessed")
        self.assertTrue(record["blessing"]["named_act"])

    def test_automatic_regeneration_is_never_evidence(self):
        module = require(MODULE)
        regenerated = module.regenerate(module.golden_record())
        self.assertFalse(regenerated["counts_as_evidence"])


class TestGoldenCombinedIdentityVersionFixR2(unittest.TestCase):
    """Fix round 2, R2-REPORT-GOLDEN-N1: combined field values.

    Each field name carrying both identity and version carries
    an identity formed from the record type and the version, in
    the identity limb form, at each schema version, beside a
    pure version field of the same record still carrying the
    schema version itself.
    """

    COMBINED = (
        ("Dataset", "Dataset identity and version",
         "Curation input versions"),
        ("Evaluation", "Scorer identity and version",
         "Cost table version"),
        ("Run", "Workflow identity and definition version",
         "Signature version"),
    )

    def test_combined_fields_carry_identity_form_at_each_version(self):
        module = require(MODULE)
        golden = module.golden_record_sets()
        for record_type, field, pure_version_field in self.COMBINED:
            slug = field.lower().replace(" ", "-")
            for version in golden["schema_versions"]:
                record = golden["records"][(record_type, version)]
                self.assertEqual(
                    record["payload"][field],
                    "golden-" + record_type.lower() + "-"
                    + str(version) + "-" + slug,
                    (record_type, field, version),
                )
                self.assertEqual(
                    record["payload"][pure_version_field], version,
                    (record_type, pure_version_field, version),
                )


class TestGoldenT04(unittest.TestCase):
    """GOLDEN-T04: the suite stands before DATASET grouping opens."""

    def test_suite_exists_as_a_runnable_artifact(self):
        stage_carried(STAGE_REASON_T04)

    def test_suite_stands_before_dataset_grouping_work_opens(self):
        stage_carried(STAGE_REASON_T04)


class TestGoldenReReadWindowTypeFixR3(unittest.TestCase):
    """Fix round 3, S15-R3-011: the reader window type limb.

    The window limb refuses a schema version that does not
    stand as an integer of the window, in the same refusal
    case the limb already returns, beside the standing
    integer cases. This entry stands beside S15-R1-065 and
    does not reopen it.
    """

    def _sound_record(self):
        module = require(MODULE)
        golden = module.golden_record_sets()
        for record in golden["records"].values():
            if record["schema_version"] == 1:
                return record
        return next(iter(golden["records"].values()))

    def test_boolean_and_float_versions_stand_refused(self):
        module = require(MODULE)
        sound = self._sound_record()
        for wrong_type in (True, 1.0):
            record = dict(sound)
            record["schema_version"] = wrong_type
            reread = module.re_read(record)
            self.assertFalse(reread["read"], wrong_type)
            self.assertEqual(
                reread["refusal"]["case"],
                "schema version outside the reader window",
                wrong_type,
            )

    def test_standing_integer_cases_stand_as_they_stood(self):
        module = require(MODULE)
        sound = self._sound_record()
        reread = module.re_read(dict(sound))
        self.assertTrue(reread["read"])
        outside = dict(sound)
        outside["schema_version"] = 999
        refused = module.re_read(outside)
        self.assertFalse(refused["read"])
        self.assertEqual(
            refused["refusal"]["case"],
            "schema version outside the reader window",
        )


class TestGoldenSealClaimScanFixR4(unittest.TestCase):
    """Fix round 4, Region 2: the seal claim scan substance acts.

    The golden home pins the scan through the report travel
    lint beside the standing verify sentence form: an
    unconditional signed statement fails, and the governed
    verify sentence, whose heads stand signed at signed
    strength only, passes whole. The GOLDEN-T04 segment
    above stands untouched in its exact form.
    """

    def test_unconditional_signed_statement_fails_travel_lint(self):
        report = require("ontoloop.report")
        result = report.fixed_text_travel_lint(
            assembly="export",
            content="The bundle stands signed for every actor.")
        self.assertFalse(result["passed"])

    def test_governed_verify_sentence_passes_the_scan(self):
        from ontoloop import sealing

        report = require("ontoloop.report")
        self.assertTrue(report._seal_claim_scan(sealing.VERIFY_SENTENCE))
        result = report.fixed_text_travel_lint(
            assembly="export", content=sealing.VERIFY_SENTENCE)
        self.assertTrue(result["passed"])


class TestGoldenDischargeCollectionsFixR5(unittest.TestCase):
    """Fix round 5, N-46, ruling 83: the discharge collections.

    discharge_state checks its collections as the collections
    they stand stated to be, a list of class names, a list of
    checks run, and a mapping of results: string forms no
    longer discharge, class coverage standing as whole class
    name membership only and no character count standing as a
    check count, beside the same entry in list forms still
    discharging and the part class name list form still
    returning discharged False. The GOLDEN-T04 segment above
    stands untouched in its exact form.
    """

    def _entry(self, **overrides):
        module = require(MODULE)
        entry = dict(module.latest_meaning_change_entry())
        entry.update(overrides)
        return module, entry

    def test_single_class_string_form_does_not_discharge(self):
        module, entry = self._entry()
        first_class = entry["affected_classes"][0]
        string_entry = {
            "affected_classes": first_class,
            "checks_run": "x",
            "result_of_each_check": {
                "x": "meaning check result recorded"},
        }
        state = module.discharge_state(
            entry=string_entry, affected_classes=[first_class])
        self.assertFalse(state["discharged"])
        self.assertTrue(state["bar_stands"])
        self.assertFalse(state["change_passed_as_no_change"])

    def test_joined_classes_string_form_does_not_discharge(self):
        module, entry = self._entry()
        checks = list(entry["checks_run"])
        string_entry = {
            "affected_classes": " ".join(entry["affected_classes"]),
            "checks_run": "x" * len(checks),
            "result_of_each_check": {
                check: "meaning check result recorded"
                for check in checks},
        }
        state = module.discharge_state(entry=string_entry)
        self.assertFalse(state["discharged"])
        self.assertTrue(state["bar_stands"])

    def test_string_checks_and_string_results_do_not_discharge(self):
        module, entry = self._entry()
        checks = list(entry["checks_run"])
        checks_string_entry = dict(entry)
        checks_string_entry["checks_run"] = "x" * len(checks)
        state = module.discharge_state(entry=checks_string_entry)
        self.assertFalse(state["discharged"])
        results_string_entry = dict(entry)
        results_string_entry["result_of_each_check"] = (
            "y" * len(checks))
        state = module.discharge_state(entry=results_string_entry)
        self.assertFalse(state["discharged"])

    def test_list_forms_still_discharge_and_part_name_still_fails(self):
        module, entry = self._entry()
        state = module.discharge_state(entry=entry)
        self.assertTrue(state["discharged"])
        self.assertFalse(state["bar_stands"])
        first_class = entry["affected_classes"][0]
        part_entry = dict(entry)
        part_entry["affected_classes"] = [first_class[:4]]
        state = module.discharge_state(
            entry=part_entry, affected_classes=[first_class])
        self.assertFalse(state["discharged"])
        self.assertTrue(state["bar_stands"])


if __name__ == "__main__":
    unittest.main()
