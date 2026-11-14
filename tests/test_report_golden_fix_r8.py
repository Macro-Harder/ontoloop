"""Fix round 8, Region 1: report and golden pins.

Rulings 199 to 204 of the Round 8 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide.
"""

import unittest
from collections import UserDict
from types import MappingProxyType

from tests import harness


def _scan(mod, statement):
    return mod._seal_claim_scan(statement)


def _travel(mod, statement):
    result = mod.fixed_text_travel_lint(
        assembly="export", content=statement)
    return result["passed"]


class SealClaimScanGoverningPhraseFixR8Tests(unittest.TestCase):
    """Ruling 199: introducer and governing phrase limb, Medium."""

    MODAL_JUXTAPOSITION = (
        "The seal guarantees protection the schedule could not expire.",
        "The seal guarantees protection the schedule might not expire.",
        "The seal guarantees protection the schedule should not expire.",
        "The seal guarantees protection the schedule would not expire.",
        "The seal guarantees protection the schedule could never expire.",
        "The seal guarantees protection the schedule might never expire.",
        "The seal guarantees protection the schedule ought not expire.",
        "The seal guarantees protection this schedule could not expire.",
        "The seal guarantees protection a schedule could not expire.",
        "The seal guarantees protection schedules could not expire.",
    )

    COMBINED_FORMS = (
        "The seal guarantees protection % the schedule could not expire.",
        "The seal guarantees protection moreover the schedule "
        "could not expire.",
        "The seal guarantees protection therefore the schedule "
        "could not expire.",
        "The seal guarantees protection upon the schedule "
        "could not expire.",
        "The seal guarantees protection using the schedule "
        "could not expire.",
        "The seal guarantees protection believing the schedule "
        "could not expire.",
    )

    ONLY_FORMS = (
        "The seal guarantees protection only if the weather holds.",
        "The seal guarantees protection only when the weather holds.",
        "The seal guarantees protection only where the weather holds.",
        "The seal guarantees protection only if the weather at the "
        "deployment confinement fact office holds.",
    )

    NOUN_PHRASE_INTRODUCERS = (
        "The seal guarantees protection regarding expiry never occurs.",
        "The seal guarantees protection concerning expiry never occurs.",
        "The seal guarantees protection providing expiry never occurs.",
        "The seal guarantees protection imagining expiry never occurs.",
        "The seal guarantees protection presuming expiry never occurs.",
        "The seal guarantees protection stipulating expiry never occurs.",
        "The seal guarantees protection remembering expiry never occurs.",
        "The seal guarantees protection forgetting expiry never occurs.",
        "The seal guarantees protection witnessing expiry never occurs.",
        "The seal guarantees protection accepting expiry never occurs.",
    )

    ARTICLE_GOVERNED = (
        "The seal guarantees protection conditional on a signed strength.",
        "The seal guarantees protection conditional on an deployment "
        "confinement fact.",
        "The seal guarantees protection subject to a deployment "
        "confinement fact.",
        "The seal guarantees protection conditional on a deployment "
        "confinement fact.",
        "The seal guarantees protection only if the deployment "
        "confinement fact holds.",
        "The seal guarantees protection only when the signed strength "
        "stands.",
    )

    def test_modal_juxtaposition_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_JUXTAPOSITION:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_combined_marker_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMBINED_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_only_forms_on_ungoverned_subjects_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ONLY_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_noun_phrase_introducer_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NOUN_PHRASE_INTRODUCERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_article_governed_conditions_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ARTICLE_GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_genuine_forms_and_clean_assemblies_still_pass(self):
        mod = harness.require("ontoloop.report")
        governed = (
            "The seal guarantees protection conditional on "
            "the deployment confinement fact.",
            "The seal guarantees protection conditional on "
            "deployment confinement fact.",
            "The seal guarantees protection conditional on "
            "signed strength.",
            "The seal does not guarantee protection.",
        )
        for statement in governed:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])
        self.assertFalse(_scan(mod, "The seal guarantees protection."))


class SealClaimScanInabilityFixR8Tests(unittest.TestCase):
    """Ruling 200: the inability limb."""

    MODAL_AND_WINDOW_FORMS = (
        "Records should never be altered after writing.",
        "Records would never be altered after writing.",
        "Records should not be altered after writing.",
        "Records would not be altered after writing.",
        "Records ought never to be altered after writing.",
        "Records cannot by any means be altered after writing.",
        "Records cannot under all circumstances be altered after writing.",
        "Records cannot at all be altered after writing.",
        "Records cannot under any conceivable circumstances be "
        "altered after writing.",
        "Records can be never altered after writing.",
        "Records cannot under any condition be altered after writing.",
        "Records cannot in any case be altered after writing.",
        "Records cannot for any reason be altered after writing.",
        "Records cannot in any respect be altered after writing.",
        "Records cannot under any circumstance be altered after writing.",
        "Records cannot under any circumstances whatsoever be "
        "altered after writing.",
        "Heads cannot be verified by any outsider.",
    )

    FOLLOWER_FORMS = (
        "Store files cannot be read by outsiders.",
        "Store files cannot be copied by outsiders.",
        "Records cannot be accessed by outsiders.",
        "Store files cannot be viewed by outsiders.",
        "Store files cannot be opened by outsiders.",
        "Store files cannot be listed by outsiders.",
        "Records cannot be leaked after writing.",
        "Records cannot be disclosed after writing.",
        "Records cannot be exported by outsiders.",
        "Records cannot be edited after writing.",
        "Records cannot be overwritten after writing.",
        "Records cannot be updated after writing.",
        "Records cannot be replaced after writing.",
    )

    ASSERTED_FOLLOWER_FORMS = (
        "Store files are read by outsiders.",
        "Records are accessed by outsiders.",
        "Records are edited after writing.",
        "Records are overwritten after writing.",
    )

    def test_modal_and_window_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_AND_WINDOW_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_follower_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FOLLOWER_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_follower_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_FOLLOWER_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_negated_claims_still_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "The seal does not guarantee protection.",
        ):
            self.assertTrue(_scan(mod, statement), statement)


class SealClaimScanPrefixedCompoundsFixR8Tests(unittest.TestCase):
    """Ruling 201: the prefixed compound limb."""

    COMPOUNDS = (
        "Every record stands inter-checked before use.",
        "Every record stands post-verified before use.",
        "Every record stands multi-checked before use.",
        "Every record stands semi-verified before use.",
        "Every record stands non-verified before use.",
        "Every record stands un-verified before use.",
        "Every record stands hyper-verified before use.",
        "Every record stands micro-checked before use.",
        "Every record stands macro-verified before use.",
        "Every record stands pseudo-verified before use.",
        "Every record stands quasi-verified before use.",
        "The record stands ultra-verified.",
        "The record stands hyper-checked.",
    )

    def test_prefixed_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMPOUNDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_charged_compounds_still_fail_and_governed_pass(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Every record stands self-verified before use."))
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR8Tests(unittest.TestCase):
    """Ruling 202: the lexicon limb."""

    WORDINGS = (
        "Records stand impervious after writing.",
        "Records stand eternal after writing.",
        "Records stand perpetual after writing.",
        "Records stand indissoluble after writing.",
        "Records stand inalterable after writing.",
        "Records stand unchanging after writing.",
        "The store stands walled against outside writers.",
        "Every record stands proofread before use.",
        "Every record stands vetted before use.",
        "Every record stands screened before use.",
        "Every record stands reviewed before use.",
        "The store is unhackable.",
        "The store is crackproof.",
        "The journal is theftproof.",
        "The store is pickproof.",
        "The journal is incorruptible.",
        "The records are unerasable by outside writers.",
        "The records are undeletable by outside writers.",
        "The records are unmodifiable by outside writers.",
        "The store is unpenetrable by outside writers.",
        "The records are incorruptible by outside writers.",
        "Heads stand stamped for every actor.",
        "Heads stand enrolled for every actor.",
        "Heads stand registered for every actor.",
    )

    def test_lexicon_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WORDINGS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_governed_and_clean_forms_still_pass(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanAssertedVerbsFixR8Tests(unittest.TestCase):
    """Ruling 203: the asserted form limb."""

    VERB_FORMS = (
        "The journal gives integrity for every reader.",
        "The journal safeguards integrity for every reader.",
        "The journal defends integrity for every reader.",
        "The journal promotes integrity for every reader.",
        "The journal supports integrity for every reader.",
        "The journal fosters integrity for every reader.",
        "The journal bolsters integrity for every reader.",
        "The journal strengthens integrity for every reader.",
        "The journal fortifies integrity for every reader.",
        "The journal reinforces integrity for every reader.",
        "The journal underpins integrity for every reader.",
        "The mechanism vouches total integrity of the journal.",
        "The mechanism effects total integrity of the journal.",
        "The mechanism realizes total integrity of the journal.",
        "The mechanism represents total integrity of the journal.",
        "The mechanism brings total integrity of the journal.",
    )

    def test_asserted_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_fragment_boundary_still_holds(self):
        mod = harness.require("ontoloop.report")
        statement = "Integrity label for the journal schedule."
        self.assertTrue(_scan(mod, statement), statement)
        self.assertTrue(_travel(mod, statement), statement)
        self.assertFalse(
            _scan(mod, "The journal secures integrity for every reader."))


class ProductionReportFormMappingRecordsFixR8Tests(unittest.TestCase):
    """Ruling 204: produced records counting by mapping form."""

    ENTRIES = {"shape": "sealed shape", "family": "sealed family"}

    def test_mapping_proxy_record_counts(self):
        mod = harness.require("ontoloop.report")
        result = mod.production_report_form(
            produced_records=[MappingProxyType(dict(self.ENTRIES))])
        self.assertEqual(
            result["production_counts"]["per_shape"],
            {"sealed shape": 1})
        self.assertEqual(
            result["production_counts"]["per_family"],
            {"sealed family": 1})
        self.assertTrue(result["counts_present"])

    def test_userdict_record_counts(self):
        mod = harness.require("ontoloop.report")
        result = mod.production_report_form(
            produced_records=[UserDict(dict(self.ENTRIES))])
        self.assertEqual(
            result["production_counts"]["per_shape"],
            {"sealed shape": 1})
        self.assertEqual(
            result["production_counts"]["per_family"],
            {"sealed family": 1})
        self.assertTrue(result["counts_present"])

    def test_plain_mapping_control_still_counts(self):
        mod = harness.require("ontoloop.report")
        result = mod.production_report_form(
            produced_records=[dict(self.ENTRIES)])
        self.assertEqual(
            result["production_counts"]["per_shape"],
            {"sealed shape": 1})
        self.assertEqual(
            result["production_counts"]["per_family"],
            {"sealed family": 1})
        self.assertTrue(result["counts_present"])

    def test_unhashable_value_and_no_material_forms_stand(self):
        mod = harness.require("ontoloop.report")
        result = mod.production_report_form(
            produced_records=[{"shape": ["a", "b"], "family": "fam"}])
        self.assertEqual(result["production_counts"]["per_shape"], {})
        self.assertEqual(
            result["production_counts"]["per_family"], {"fam": 1})
        empty = mod.production_report_form()
        self.assertFalse(empty["counts_present"])


if __name__ == "__main__":
    unittest.main()
