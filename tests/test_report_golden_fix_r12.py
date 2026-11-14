"""Fix round 12, Region 1: report and golden pins.

Rulings 383 to 387 of the Round 12 triage. Each class pins
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


class SealClaimScanInabilityFixR12Tests(unittest.TestCase):
    """Ruling 383: inability limb, followers and windows."""

    FOLLOWERS = (
        "Records cannot be streamed by outsiders.",
        "Records cannot be distributed by outsiders.",
        "Records cannot be transferred by outsiders.",
        "Records cannot be circulated by outsiders.",
        "Records cannot be disseminated by outsiders.",
        "Records cannot be conveyed by outsiders.",
        "Records cannot be dispatched by outsiders.",
        "Records cannot be aired by outsiders.",
        "Records cannot be televised by outsiders.",
        "Records cannot be projected by outsiders.",
        "Records cannot be displayed by outsiders.",
        "Records cannot be beamed by outsiders.",
        "Records cannot be overheard by outsiders.",
        "Records cannot be quoted by outsiders.",
        "Records cannot be paraphrased by outsiders.",
        "Records cannot be plagiarized by outsiders.",
        "Records cannot be exposed by outsiders.",
        "Records cannot be unlocked by outsiders.",
        "Records cannot be decrypted by outsiders.",
        "Records cannot be doctored after writing.",
        "Records cannot be manipulated after writing.",
        "Records cannot be pilfered after writing.",
        "Records cannot be looted after writing.",
        "Records cannot be snatched after writing.",
        "Records cannot be swiped after writing.",
        "Records cannot be pinched after writing.",
        "Records cannot be memorised after writing.",
        "Heads cannot be recorded by any outsider.",
        "Heads cannot be taped by any outsider.",
        "Heads cannot be bugged by any outsider.",
        "Heads cannot be wiretapped by any outsider.",
        "Heads cannot be embezzled by any outsider.",
        "Heads cannot be diverted by any outsider.",
        "Heads cannot be xeroxed by any outsider.",
        "Heads cannot be retyped by any outsider.",
        "Heads cannot be resealed by any outsider.",
        "Heads cannot be seen by any outsider.",
        "Heads cannot be heard by any outsider.",
        "Heads cannot be witnessed by any outsider.",
        "Heads cannot be noted by any outsider.",
        "Heads cannot be logged by any outsider.",
        "Heads cannot be catalogued by any outsider.",
        "Heads cannot be memorialized by any outsider.",
        "Heads cannot be chronicled by any outsider.",
    )

    ASSERTED = (
        "Records are streamed by outsiders.",
        "Records are distributed by outsiders.",
        "Records are transferred by outsiders.",
        "Records are doctored by outsiders.",
        "Records are pilfered by outsiders.",
        "Records are memorised by outsiders.",
    )

    WINDOWS = (
        "Records cannot under any statute be altered after writing.",
        "Records cannot in any jurisdiction be altered after writing.",
        "Records cannot by any device be altered after writing.",
        "Records cannot through any channel be altered after writing.",
        "Records cannot via any channel be altered after writing.",
        "Records cannot in any domain be altered after writing.",
        "Records cannot in any realm be altered after writing.",
        "Records cannot in any sphere be altered after writing.",
        "Records cannot in any setting be altered after writing.",
        "Records cannot in any environment be altered after writing.",
        "Records cannot through any medium be altered after writing.",
        "Records cannot in any venue be altered after writing.",
        "Records cannot in any arena be altered after writing.",
        "Records cannot under any regime be altered after writing.",
        "Records cannot by any channel be altered after writing.",
        "Records cannot in any framework be altered after writing.",
        "Records cannot realistically be altered.",
        "Records cannot effectively be altered.",
        "Records cannot virtually be altered.",
        "Records cannot technically be altered.",
        "Records cannot mechanically be altered.",
        "Records cannot digitally be altered.",
        "Records cannot electronically be altered.",
        "Records cannot manually be altered.",
        "Records cannot automatically be altered.",
        "Records cannot in reality be altered.",
        "Records cannot in effect be altered.",
        "Records cannot in essence be altered.",
        "Records cannot by any outsider be altered.",
        "Records cannot by any stranger be altered.",
        "Records cannot on any grounds be altered.",
        "Records cannot in any forum be altered.",
        "Records cannot to any degree be altered.",
        "Records cannot by any agency be altered.",
    )

    def test_follower_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FOLLOWERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_follower_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_window_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOWS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "Records cannot be memorized by outsiders.",
            "Records cannot in any shape be altered after writing.",
            "Records cannot under any conditions be altered after writing.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(mod, "The seal does not guarantee protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanGoverningFixR12Tests(unittest.TestCase):
    """Ruling 384: governing condition limb."""

    GOVERNED = (
        "The seal guarantees protection in conformity with the deployment confinement fact.",
        "The seal guarantees protection in compliance with the deployment confinement fact.",
        "The seal guarantees protection in reliance upon the deployment confinement fact.",
        "The seal guarantees protection founded upon the deployment confinement fact.",
        "The seal guarantees protection built on the deployment confinement fact.",
        "The seal guarantees protection built upon the deployment confinement fact.",
        "The seal guarantees protection hinging upon the deployment confinement fact.",
        "The seal guarantees protection based solely on the deployment confinement fact.",
        "The seal guarantees protection resting solely on the deployment confinement fact.",
        "The seal guarantees protection dependent solely upon the deployment confinement fact.",
        "The seal guarantees protection dependent solely upon signed strength.",
        "The seal guarantees protection contingent solely upon the deployment confinement fact.",
        "The seal guarantees protection conditioned solely upon the deployment confinement fact.",
        "The seal guarantees protection tied to the deployment confinement fact.",
        "The seal guarantees protection relying on the deployment confinement fact.",
        "The seal guarantees protection conditioned by the deployment confinement fact.",
        "The seal guarantees protection on the basis of the deployment confinement fact.",
        "The seal guarantees protection anchored in the deployment confinement fact.",
        "The seal guarantees protection linked to the deployment confinement fact.",
        "The seal guarantees protection bound by the deployment confinement fact.",
        "The seal guarantees protection in dependence on the deployment confinement fact.",
        "The seal guarantees protection in keeping with the deployment confinement fact.",
        "The seal guarantees protection in line with the deployment confinement fact.",
        "The seal guarantees protection as required by the deployment confinement fact.",
        "The seal guarantees protection under the terms of the deployment confinement fact.",
        "The seal guarantees protection within the bounds of the deployment confinement fact.",
        "The seal guarantees protection bounded by the deployment confinement fact.",
        "The seal guarantees protection limited by the deployment confinement fact.",
        "The seal guarantees protection constrained by the deployment confinement fact.",
    )

    WEATHER = (
        "The seal guarantees protection in conformity with the weather holds.",
        "The seal guarantees protection in compliance with the weather holds.",
        "The seal guarantees protection bounded by the weather holds.",
        "The seal guarantees protection tied to the weather holds.",
        "The seal guarantees protection based solely on the weather holds.",
    )

    def test_governed_phrasings_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_and_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
        for statement in (
            "The seal guarantees protection conditional on the deployment confinement fact.",
            "The seal guarantees protection contingent on the deployment confinement fact.",
            "The seal guarantees protection contingent upon the deployment confinement fact.",
            "The seal guarantees protection hinging on the deployment confinement fact.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
        self.assertFalse(_scan(mod, "The seal guarantees protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanPrefixedFixR12Tests(unittest.TestCase):
    """Ruling 385: prefixed compound limb."""

    FORMS = (
        "The record stands mini-verified.",
        "The record stands maxi-verified.",
        "The record stands cyber-verified.",
        "Every record stands remotely-checked before use.",
        "Every record stands locally-checked before use.",
        "Every record stands virtually-checked before use.",
        "Every record stands physically-checked before use.",
        "Every record stands audibly-checked before use.",
        "Every record stands sixfold-checked before use.",
        "Every record stands tenfold-checked before use.",
        "Every record stands once-checked before use.",
        "Every record stands single-checked before use.",
        "The record stands mega-attested.",
        "The record stands pro-attested.",
        "The record stands mega-endorsed.",
        "The record stands mega-notarized.",
        "The record stands mega-countersigned.",
        "The record stands sextuple-verified.",
        "The record stands septuple-verified.",
        "The record stands octuple-verified.",
        "The record stands nonuple-verified.",
        "The record stands hecto-verified.",
        "The record stands acoustically-verified.",
        "The record stands remotely-verified.",
        "The record stands blindly-verified.",
        "The record stands sextuple-checked.",
        "The record stands hecto-checked.",
        "The record stands acoustically-checked.",
        "The record stands remotely-checked.",
        "The record stands blindly-checked.",
        "Every record stands peer-checked before use.",
        "Every record stands peer-verified before use.",
        "Every record stands owner-checked before use.",
        "Every record stands owner-verified before use.",
        "Every record stands author-checked before use.",
        "Every record stands author-verified before use.",
        "Every record stands clerk-checked before use.",
        "Every record stands clerk-verified before use.",
        "Every record stands team-checked before use.",
        "Every record stands team-verified before use.",
        "Every record stands group-checked before use.",
        "Every record stands group-verified before use.",
        "Every record stands board-checked before use.",
        "Every record stands board-verified before use.",
        "Every record stands panel-checked before use.",
        "Every record stands panel-verified before use.",
        "Every record stands joint-checked before use.",
        "Every record stands joint-verified before use.",
    )

    def test_prefixed_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "The record stands mega-verified.",
            "The record stands pro-verified.",
            "The record stands sealed.",
            "The record stands attested.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanLexiconFixR12Tests(unittest.TestCase):
    """Ruling 386: lexicon limb."""

    FORMS = (
        "Records stand unstained after writing.",
        "Records stand untarnished after writing.",
        "Records stand unsullied after writing.",
        "Records stand unsoiled after writing.",
        "Records stand unequalled after writing.",
        "Records stand unparalleled after writing.",
        "Records stand unrivalled after writing.",
        "Records stand unsurpassed after writing.",
        "Records stand incomparable after writing.",
        "The store is unreachable.",
        "The store is unapproachable.",
        "The store is ungettable.",
        "The records are unstained by outside writers.",
        "The records are unreachable by outside writers.",
        "Heads stand foil-stamped for every actor.",
        "Heads stand ink-stamped for every actor.",
        "Heads stand laser-etched for every actor.",
        "The store is inviolate.",
        "The store is unflawed.",
        "The store is unmarred.",
        "The store is unimpaired.",
        "The store is entryproof.",
        "Every record stands unchallenged before use.",
        "The records are imperishable by outside writers.",
        "The records are unrivalled by outside writers.",
        "The records are incomparable by outside writers.",
        "The records are fraud-proof by outside writers.",
        "The records are drill-proof by outside writers.",
        "The records are dust-proof by outside writers.",
        "The records are smudge-proof by outside writers.",
    )

    def test_lexicon_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(mod, "The store is impermeable."))
        self.assertFalse(_scan(mod, "Records stand spotless after writing."))
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanAssertedFixR12Tests(unittest.TestCase):
    """Ruling 387: asserted form limb."""

    FORMS = (
        "The journal mirrors integrity for every reader.",
        "The journal reflects integrity for every reader.",
        "The journal signals integrity for every reader.",
        "The journal implies integrity for every reader.",
        "The journal suggests integrity for every reader.",
        "The journal indicates integrity for every reader.",
        "The journal testifies to integrity for every reader.",
        "The journal echoes integrity for every reader.",
        "The journal speaks for integrity for every reader.",
        "The journal bears integrity for every reader.",
        "The journal wields integrity for every reader.",
        "The journal harbours integrity for every reader.",
        "The journal harbors integrity for every reader.",
        "The journal carries integrity for every reader.",
        "The mechanism illustrates total integrity of the journal.",
        "The mechanism crystallizes total integrity of the journal.",
        "The mechanism encapsulates total integrity of the journal.",
        "The mechanism actualizes total integrity of the journal.",
        "The mechanism substantiates total integrity of the journal.",
    )

    def test_asserted_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_and_fragment_boundary_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal embodies integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal symbolizes integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))
        self.assertTrue(_travel(
            mod, "Integrity label for the journal schedule."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


if __name__ == "__main__":
    unittest.main()
