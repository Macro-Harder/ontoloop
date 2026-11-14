"""Fix round 10, Region 1: report and golden pins.

Rulings 306 to 311 of the Round 10 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide.
"""

import unittest

from tests import harness


def _scan(mod, statement):
    return mod._seal_claim_scan(statement)


def _travel(mod, statement):
    result = mod.fixed_text_travel_lint(
        assembly="export", content=statement)
    return result["passed"]


class SealClaimScanJuxtaposedModalFixR10Tests(unittest.TestCase):
    """Ruling 306: juxtaposed negated clause on modal forms."""

    FORMS = (
        "The seal guarantees protection expiry shall never occur.",
        "The seal guarantees protection expiry must never occur.",
        "The seal guarantees protection expiry will never occur.",
        "The seal guarantees protection expiry can never occur.",
    )

    def test_juxtaposed_modal_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_charged_and_genuine_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "The seal guarantees protection expiry never occurs.",
            "The seal guarantees protection the schedule could not expire.",
            "The seal guarantees protection the schedule does not expire.",
            "The seal guarantees protection the schedule had never expired.",
            "The seal guarantees protection the schedule is occurring.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        for statement in (
            "The seal guarantees protection conditional on "
            "the deployment confinement fact.",
            "The seal guarantees protection conditional on "
            "signed strength.",
            "The seal does not guarantee protection.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanInabilityFixR10Tests(unittest.TestCase):
    """Ruling 307: the inability merged defect."""

    FOLLOWER_FORMS = (
        "Records cannot be mirrored by outsiders.",
        "Records cannot be cloned by outsiders.",
        "Records cannot be screenshotted by outsiders.",
        "Records cannot be emailed by outsiders.",
        "Records cannot be uploaded by outsiders.",
        "Records cannot be archived by outsiders.",
        "Records cannot be broadcast by outsiders.",
        "Records cannot be stolen by outsiders.",
        "Records cannot be wiped by outsiders.",
        "Records cannot be exfiltrated after writing.",
        "Records cannot be purged after writing.",
        "Records cannot be corrupted after writing.",
        "Heads cannot be exfiltrated by any outsider.",
        "Heads cannot be filmed by any outsider.",
        "Heads cannot be scanned by any outsider.",
        "Heads cannot be traced by any outsider.",
        "Heads cannot be mirrored by any outsider.",
        "Heads cannot be cloned by any outsider.",
        "Heads cannot be uploaded by any outsider.",
        "Heads cannot be emailed by any outsider.",
    )

    ASSERTED_FOLLOWER_FORMS = (
        "Records are mirrored by outsiders.",
        "Records are cloned by outsiders.",
        "Records are emailed by outsiders.",
        "Records are stolen by outsiders.",
        "Records are wiped by outsiders.",
        "Records are exfiltrated after writing.",
        "Records are uploaded by outsiders.",
        "Records are corrupted after writing.",
    )

    WINDOW_FORMS = (
        "Records cannot conceivably be altered after writing.",
        "Records cannot remotely be altered after writing.",
        "Records cannot in any event be altered after writing.",
        "Records cannot under any conditions be altered after writing.",
        "Records cannot regardless be altered.",
        "Records cannot somehow be altered.",
        "Records cannot anyhow be altered.",
        "Records cannot just be altered.",
        "Records cannot merely be altered.",
        "Records cannot truly be altered.",
        "Records cannot actually be altered.",
        "Records cannot even be altered.",
        "Records cannot still be altered.",
        "Records cannot in the least be altered.",
        "Records cannot by any stretch be altered.",
        "Records cannot under any pretext be altered.",
        "Records cannot on any account be altered.",
    )

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

    def test_window_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOW_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_deep_window_form_fails(self):
        mod = harness.require("ontoloop.report")
        deep = (
            "Records cannot " + "in any way " * 22 + "be altered.")
        self.assertFalse(_scan(mod, deep), deep)
        self.assertFalse(_travel(mod, deep), deep)
        inside = (
            "Records cannot " + "in any way " * 10 + "be altered.")
        self.assertFalse(_scan(mod, inside), inside)

    def test_charged_forms_and_negated_claims_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "Records cannot be altered after writing.",
            "Records cannot be duplicated after writing.",
            "Records cannot absolutely be altered.",
            "Records cannot in any manner be altered after writing.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(mod, "The seal does not guarantee protection."))


class SealClaimScanGoverningFixR10Tests(unittest.TestCase):
    """Ruling 308: the governing condition merged defect."""

    GOVERNED = (
        "The seal guarantees protection reliant on "
        "the deployment confinement fact.",
        "The seal guarantees protection dependent on "
        "the deployment confinement fact.",
        "The seal guarantees protection subject only to "
        "the deployment confinement fact.",
        "The seal guarantees protection only under "
        "the deployment confinement fact.",
        "The seal guarantees protection only with signed strength.",
        "The seal guarantees protection conditioned upon "
        "the deployment confinement fact.",
        "The seal guarantees protection premised on "
        "the deployment confinement fact.",
        "The seal guarantees protection predicated on "
        "the deployment confinement fact.",
        "The seal guarantees protection based on "
        "the deployment confinement fact.",
        "The seal guarantees protection resting on "
        "the deployment confinement fact.",
        "The seal guarantees protection assuming "
        "the deployment confinement fact.",
        "The seal guarantees protection granted "
        "the deployment confinement fact.",
        "The seal guarantees protection presuming "
        "the deployment confinement fact.",
        "The seal guarantees protection supposing "
        "the deployment confinement fact.",
    )

    WEATHER = (
        "The seal guarantees protection reliant on the weather.",
        "The seal guarantees protection conditioned on the weather.",
        "The seal guarantees protection based on the weather.",
        "The seal guarantees protection dependent on the weather.",
        "The seal guarantees protection assuming the weather holds.",
    )

    def test_governed_phrasings_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_phrasings_still_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_governed_forms_still_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "The seal guarantees protection conditional on "
            "the deployment confinement fact.",
            "The seal guarantees protection subject to "
            "the deployment confinement fact.",
            "The seal guarantees protection depending on "
            "the deployment confinement fact.",
            "The seal guarantees protection contingent on "
            "the deployment confinement fact.",
            "The seal guarantees protection conditional upon "
            "the deployment confinement fact.",
            "The seal guarantees protection conditioned on "
            "the deployment confinement fact.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
        self.assertFalse(_scan(mod, "The seal guarantees protection."))


class SealClaimScanPrefixedFixR10Tests(unittest.TestCase):
    """Ruling 309: the prefixed compound merged defect."""

    PREFIXES = (
        "mega", "giga", "nano", "pico", "hemi", "mono", "bi",
        "quad", "penta", "hexa", "octo", "deca", "kilo", "milli",
        "centi", "deci", "proto", "retro", "infra", "supra",
        "meta", "para", "hypo", "epi", "endo", "exo", "hetero",
        "homo", "iso", "tele", "pan", "uni",
        "triple", "hand", "machine", "deep",
    )

    def test_prefixed_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for prefix in self.PREFIXES:
            statement = "The record stands %s-verified." % prefix
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)
            checked = "Every record stands %s-checked before use." % prefix
            self.assertFalse(_scan(mod, checked), checked)

    def test_charged_compounds_still_fail_and_governed_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "Every record stands tri-checked before use.",
            "The record stands super-verified.",
            "The record stands x-verified.",
            "Every record stands inter-checked before use.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR10Tests(unittest.TestCase):
    """Ruling 310: the lexicon merged defect."""

    WORDINGS = (
        "The store is impermeable.",
        "The store is burglarproof.",
        "The store is vandalproof.",
        "Records stand ageless after writing.",
        "Records stand endless after writing.",
        "Records stand boundless after writing.",
        "Records stand perfect after writing.",
        "Records stand impeccable after writing.",
        "Records stand undying after writing.",
        "The store is infallible.",
        "Every record stands corroborated before use.",
        "The records are infallible by outside writers.",
        "The journal is failsafe.",
        "The journal is errorproof.",
        "The journal is peerless.",
        "The journal is matchless.",
        "The records are error-free by outside writers.",
        "The records are risk-free by outside writers.",
        "Heads stand rubber-stamped for every actor.",
        "Heads stand time-stamped for every actor.",
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


class SealClaimScanAssertedFixR10Tests(unittest.TestCase):
    """Ruling 311: the asserted form merged defect."""

    VERB_FORMS = (
        "The journal epitomizes integrity for every reader.",
        "The journal personifies integrity for every reader.",
        "The journal incarnates integrity for every reader.",
        "The journal shields integrity for every reader.",
        "The journal guards integrity for every reader.",
        "The mechanism attains total integrity of the journal.",
        "The mechanism reaches total integrity of the journal.",
        "The mechanism realises total integrity of the journal.",
        "The mechanism evidences total integrity of the journal.",
        "The mechanism documents total integrity of the journal.",
        "The mechanism records total integrity of the journal.",
    )

    def test_asserted_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_fragment_boundary_and_listed_verbs_stand(self):
        mod = harness.require("ontoloop.report")
        statement = "Integrity label for the journal schedule."
        self.assertTrue(_scan(mod, statement), statement)
        self.assertTrue(_travel(mod, statement), statement)
        for statement in (
            "The journal embodies integrity for every reader.",
            "The journal exemplifies integrity for every reader.",
            "The journal gives integrity for every reader.",
        ):
            self.assertFalse(_scan(mod, statement), statement)


if __name__ == "__main__":
    unittest.main()
