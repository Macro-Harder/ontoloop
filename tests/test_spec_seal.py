"""Slice SPEC-SEAL, list section 2.3, plan section 6.5.

Data structures perspective: these tests pin byte identity across
two implementations, field presence per package form, the exact
seven field manifest list, and the verbatim forms of the three
fixed texts.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.sealing. The unnumbered failure pair stated in the
SPEC-SEAL slice paragraph (a manifest field list missing one of
its seven registered fields fails the completeness check) is
written as a method of the SPEC-SEAL-T04 case, the last row of
the slice, and invents no identifier for it.
"""

import unittest

try:
    from tests.harness import require, stage_carried
except ImportError:
    from harness import require, stage_carried

MODULE = "ontoloop.sealing"

PACKAGE_FORMS = ("journal", "manifest", "bundle")


class TestSpecSealT01(unittest.TestCase):
    """SPEC-SEAL-T01: second implementer, byte identical output."""

    def _assert_second_implementation_matches(self, form):
        module = require(MODULE)
        store = module.worked_example_store()
        first = module.package_form(store, form, reader="first")
        second = module.package_form_from_specifications(
            store, form, specifications=("SPEC-CANON", "SPEC-SEAL")
        )
        self.assertIsInstance(second, bytes)
        self.assertEqual(second, first)

    def test_journal_line_byte_identical(self):
        self._assert_second_implementation_matches("journal")

    def test_manifest_byte_identical(self):
        self._assert_second_implementation_matches("manifest")

    def test_bundle_byte_identical(self):
        self._assert_second_implementation_matches("bundle")


class TestSpecSealT02(unittest.TestCase):
    """SPEC-SEAL-T02: field presence stated and checked per form."""

    def _assert_presence_checked(self, form):
        module = require(MODULE)
        stated = module.specification_package_form_rows(form)
        self.assertTrue(stated)
        product_rows = module.package_form_rows(form)
        self.assertEqual(set(product_rows), set(stated))
        checked = module.check_field_presence(form)
        self.assertEqual(set(checked.keys()), set(stated))
        self.assertEqual(set(checked.values()), {True})

    def test_journal_field_presence(self):
        self._assert_presence_checked("journal")

    def test_manifest_field_presence(self):
        self._assert_presence_checked("manifest")

    def test_bundle_field_presence(self):
        self._assert_presence_checked("bundle")


class TestSpecSealT03(unittest.TestCase):
    """SPEC-SEAL-T03: fixed text travel lint over three texts."""

    def test_lint_passes_the_three_verbatim_texts(self):
        module = require(MODULE)
        texts = module.verbatim_texts()
        self.assertEqual(
            set(texts.keys()),
            {"seal sentence", "verify sentence", "grader awareness label"},
        )
        self.assertEqual(texts["verify sentence"].count("{}"), 2)
        surfaces = module.specification_surfaces()
        self.assertTrue(surfaces)
        for surface in surfaces:
            result = module.travel_lint(surface)
            self.assertIs(result["passed"], True)
            self.assertEqual(result["paraphrases"], [])
            carried = module.surface_texts(surface)
            self.assertEqual(
                carried["seal sentence"], texts["seal sentence"]
            )
            self.assertEqual(
                carried["grader awareness label"],
                texts["grader awareness label"],
            )

    def test_a_paraphrase_fails_the_lint(self):
        module = require(MODULE)
        surface = module.paraphrased_surface()
        result = module.travel_lint(surface)
        self.assertIs(result["passed"], False)
        self.assertTrue(result["paraphrases"])


class TestSpecSealT04(unittest.TestCase):
    """SPEC-SEAL-T04: verify computation over the example store."""

    def test_verify_returns_agreement_on_the_example_store(self):
        module = require(MODULE)
        store_bytes = module.example_store_bytes()
        result = module.verify(store_bytes)
        self.assertEqual(result["output"], "agreement")
        self.assertIn(
            result["output"],
            {"agreement", "disagreement", "unverifiable"},
        )

    def test_failure_pair_manifest_missing_one_of_seven_fields(self):
        module = require(MODULE)
        registered = module.manifest_registered_fields()
        self.assertEqual(len(registered), 7)
        self.assertEqual(len(set(registered)), 7)
        incomplete = tuple(registered[:-1])
        result = module.specification_completeness_check(incomplete)
        self.assertIs(result["complete"], False)
        self.assertEqual(result["missing"], [registered[-1]])


if __name__ == "__main__":
    unittest.main()
