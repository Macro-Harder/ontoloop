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


if __name__ == "__main__":
    unittest.main()
