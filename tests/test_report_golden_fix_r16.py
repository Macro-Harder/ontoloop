"""Fix round 16, Region 1: report and golden pins.

Rulings 561 to 565 of the Round 16 triage. Each class pins
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


class SealClaimScanInabilityFixR16Tests(unittest.TestCase):
    """Ruling 561: inability limb, followers and windows."""

    FOLLOWERS = (
        "Records cannot be damaged by outsiders.",
        "Records cannot be divulged by outsiders.",
        "Records cannot be shipped by outsiders.",
        "Records cannot be delivered by outsiders.",
        "Records cannot be returned by outsiders.",
        "Records cannot be tested by outsiders.",
        "Records cannot be measured by outsiders.",
        "Records cannot be counted by outsiders.",
        "Records cannot be weighed by outsiders.",
        "Records cannot be cleared after writing.",
        "Records cannot be checked after writing.",
        "Records cannot be tested after writing.",
        "Records cannot be sampled after writing.",
        "Records cannot be measured after writing.",
        "Records cannot be weighed after writing.",
        "Records cannot be counted after writing.",
        "Records cannot be registered after writing.",
        "Records cannot be enrolled after writing.",
        "Records cannot be booked after writing.",
        "Records cannot be remarked after writing.",
        "Records cannot be noticed after writing.",
        "Records cannot be perceived after writing.",
    )

    ASSERTED = (
        "Records are recorded by outsiders.",
        "Records are cleared by outsiders.",
        "Records are backed up by outsiders.",
        "Records are tested by outsiders.",
        "Records are sampled by outsiders.",
        "Records are measured by outsiders.",
        "Records are weighed by outsiders.",
        "Records are counted by outsiders.",
        "Records are booked by outsiders.",
        "Records are remarked by outsiders.",
        "Records are noticed by outsiders.",
        "Records are perceived by outsiders.",
        "Records are damaged by outsiders.",
        "Records are shipped by outsiders.",
    )

    WINDOWS = (
        "Records cannot in any hamlet be altered after writing.",
        "Records cannot in any suburb be altered after writing.",
        "Records cannot in any attic be altered after writing.",
        "Records cannot in any basement be altered after writing.",
        "Records cannot in any church be altered after writing.",
        "Records cannot in any station be altered after writing.",
        "Records cannot in any port be altered after writing.",
        "Records cannot in any warehouse be altered after writing.",
        "Records cannot in any factory be altered after writing.",
        "Records cannot in any mine be altered after writing.",
        "Records cannot in any garden be altered after writing.",
        "Records cannot in any park be altered after writing.",
        "Records cannot in any street be altered after writing.",
        "Records cannot in any road be altered after writing.",
        "Records cannot in any bridge be altered after writing.",
        "Records cannot in any tower be altered after writing.",
        "Records cannot in any castle be altered after writing.",
        "Records cannot in any cottage be altered after writing.",
        "Records cannot in any cabin be altered after writing.",
        "Records cannot in any tent be altered after writing.",
        "Records cannot in any camp be altered after writing.",
        "Records cannot in any village square be altered after writing.",
        "Records cannot at any moment be altered after writing.",
        "Records cannot at any instant be altered after writing.",
        "Records cannot at any second be altered after writing.",
        "Records cannot at any minute be altered after writing.",
        "Records cannot in any instant be altered after writing.",
        "Records cannot in any moment be altered after writing.",
        "Records cannot on any night be altered after writing.",
        "Records cannot in any weather be altered after writing.",
        "Records cannot on any shore be altered after writing.",
        "Records cannot on any coast be altered after writing.",
        "Records cannot on any beach be altered after writing.",
        "Records cannot on any cliff be altered after writing.",
        "Records cannot in any river be altered after writing.",
        "Records cannot in any lake be altered after writing.",
        "Records cannot in any pond be altered after writing.",
        "Records cannot in any well be altered after writing.",
        "Records cannot in any pit be altered after writing.",
        "Records cannot in any ditch be altered after writing.",
        "Records cannot through any door be altered after writing.",
        "Records cannot through any gate be altered after writing.",
        "Records cannot through any window be altered after writing.",
        "Records cannot wrongfully be altered after writing.",
        "Records cannot fraudulently be altered after writing.",
        "Records cannot in any bunker be altered.",
        "Records cannot in any fortress be altered.",
        "Records cannot in any church be altered.",
        "Records cannot in any warehouse be altered.",
        "Records cannot at any distance be altered.",
        "Records cannot in any currency be altered.",
        "Records cannot at any length be altered after writing.",
        "Records cannot in any castle be altered.",
        "Records cannot in any mosque be altered.",
        "Records cannot in any synagogue be altered.",
        "Records cannot in any station be altered.",
        "Records cannot in any port be altered.",
        "Records cannot in any mine be altered.",
        "Records cannot in any farm be altered.",
        "Records cannot in any factory be altered.",
        "Records cannot in any workshop be altered.",
        "Records cannot in any studio be altered.",
        "Records cannot in any cinema be altered.",
        "Records cannot at any volume be altered.",
        "Records cannot at any temperature be altered.",
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
            "Records cannot be typed by outsiders.",
            "Records cannot be captured by outsiders.",
            "Records cannot in any village be altered after writing.",
            "Records cannot in any vault be altered after writing.",
            "Records cannot on any planet be altered after writing.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(mod, "The seal does not guarantee protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanGoverningFixR16Tests(unittest.TestCase):
    """Ruling 562: governing condition limb."""

    GOVERNED = (
        "The seal guarantees protection grounded in the deployment confinement fact.",
        "The seal guarantees protection by authority of the deployment confinement fact.",
        "The seal guarantees protection as permitted by the deployment confinement fact.",
        "The seal guarantees protection as allowed by the deployment confinement fact.",
        "The seal guarantees protection with reference to the deployment confinement fact.",
        "The seal guarantees protection in respect of the deployment confinement fact.",
        "The seal guarantees protection respecting the deployment confinement fact.",
        "The seal guarantees protection by means of the deployment confinement fact.",
        "The seal guarantees protection by way of the deployment confinement fact.",
        "The seal guarantees protection attributable to the deployment confinement fact.",
        "The seal guarantees protection in consideration of the deployment confinement fact.",
        "The seal guarantees protection in recognition of the deployment confinement fact.",
        "The seal guarantees protection by order of the deployment confinement fact.",
        "The seal guarantees protection at the command of the deployment confinement fact.",
        "The seal guarantees protection subject to the terms of the deployment confinement fact.",
        "The seal guarantees protection inside the limits of the deployment confinement fact.",
        "The seal guarantees protection as laid out by the deployment confinement fact.",
        "The seal guarantees protection as spelled out by the deployment confinement fact.",
        "The seal guarantees protection as set forth by the deployment confinement fact.",
        "The seal guarantees protection in the light of the deployment confinement fact.",
        "The seal guarantees protection seeing that the deployment confinement fact.",
        "The seal guarantees protection in that the deployment confinement fact.",
        "The seal guarantees protection now that the deployment confinement fact.",
        "The seal guarantees protection insofar as the deployment confinement fact.",
    )

    WEATHER = (
        "The seal guarantees protection grounded in the weather holds.",
        "The seal guarantees protection by authority of the weather holds.",
        "The seal guarantees protection as permitted by the weather holds.",
        "The seal guarantees protection as allowed by the weather holds.",
        "The seal guarantees protection with reference to the weather holds.",
        "The seal guarantees protection in respect of the weather holds.",
        "The seal guarantees protection respecting the weather holds.",
        "The seal guarantees protection by means of the weather holds.",
        "The seal guarantees protection by way of the weather holds.",
        "The seal guarantees protection attributable to the weather holds.",
        "The seal guarantees protection in consideration of the weather holds.",
        "The seal guarantees protection in recognition of the weather holds.",
        "The seal guarantees protection by order of the weather holds.",
        "The seal guarantees protection at the command of the weather holds.",
        "The seal guarantees protection subject to the terms of the weather holds.",
        "The seal guarantees protection inside the limits of the weather holds.",
        "The seal guarantees protection as laid out by the weather holds.",
        "The seal guarantees protection as spelled out by the weather holds.",
        "The seal guarantees protection as set forth by the weather holds.",
        "The seal guarantees protection in the light of the weather holds.",
        "The seal guarantees protection seeing that the weather holds.",
        "The seal guarantees protection in that the weather holds.",
        "The seal guarantees protection now that the weather holds.",
        "The seal guarantees protection insofar as the weather holds.",
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
            "The seal guarantees protection due to the deployment confinement fact.",
            "The seal guarantees protection in light of the deployment confinement fact.",
            "The seal guarantees protection on the basis of the deployment confinement fact.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
        self.assertFalse(_scan(mod, "The seal guarantees protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanPrefixedFixR16Tests(unittest.TestCase):
    """Ruling 563: prefixed compound limb."""

    FORMS = (
        "Every record stands edge-checked before use.",
        "Every record stands internet-checked before use.",
        "Every record stands virtual-checked before use.",
        "Every record stands data-checked before use.",
        "Every record stands database-checked before use.",
        "Every record stands file-checked before use.",
        "Every record stands document-checked before use.",
        "Every record stands record-checked before use.",
        "Every record stands journal-checked before use.",
        "Every record stands ledger-checked before use.",
        "Every record stands safety-checked before use.",
        "Every record stands quality-checked before use.",
        "Every record stands compliance-checked before use.",
        "Every record stands professional-checked before use.",
        "Every record stands licensed-checked before use.",
        "Every record stands official-checked before use.",
        "Every record stands formal-checked before use.",
        "Every record stands private-checked before use.",
        "Every record stands personal-checked before use.",
        "Every record stands phone-checked before use.",
        "Every record stands password-checked before use.",
        "Every record stands eye-checked before use.",
        "Every record stands voice-checked before use.",
        "Every record stands ill-checked before use.",
        "Every record stands mal-checked before use.",
        "Every record stands edge-verified before use.",
        "Every record stands internet-verified before use.",
        "Every record stands virtual-verified before use.",
        "Every record stands data-verified before use.",
        "Every record stands database-verified before use.",
        "Every record stands file-verified before use.",
        "Every record stands document-verified before use.",
        "Every record stands record-verified before use.",
        "Every record stands journal-verified before use.",
        "Every record stands ledger-verified before use.",
        "Every record stands safety-verified before use.",
        "Every record stands quality-verified before use.",
        "Every record stands compliance-verified before use.",
        "Every record stands professional-verified before use.",
        "Every record stands licensed-verified before use.",
        "Every record stands official-verified before use.",
        "Every record stands formal-verified before use.",
        "Every record stands private-verified before use.",
        "Every record stands personal-verified before use.",
        "Every record stands phone-verified before use.",
        "Every record stands password-verified before use.",
        "Every record stands eye-verified before use.",
        "Every record stands voice-verified before use.",
        "Every record stands ill-verified before use.",
        "Every record stands mal-verified before use.",
        "The record stands eye-verified.",
        "The record stands voice-verified.",
        "The record stands ill-verified.",
        "The record stands mal-verified.",
        "The record stands eye-checked.",
        "The record stands voice-checked.",
        "The record stands ill-checked.",
        "The record stands mal-checked.",
    )

    def test_prefixed_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "Every record stands blockchain-checked before use.",
            "The record stands manual-verified.",
            "The record stands mega-tested.",
            "The record stands digital-verified.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanLexiconFixR16Tests(unittest.TestCase):
    """Ruling 564: lexicon limb."""

    FORMS = (
        "The records are earthquakeproof by outside writers.",
        "The records are tornadoproof by outside writers.",
        "The records are hurricaneproof by outside writers.",
        "The records are lightningproof by outside writers.",
        "The records are frostproof by outside writers.",
        "The records are impactproof by outside writers.",
        "The records are blastproof by outside writers.",
        "The records are explosionproof by outside writers.",
        "The records are airproof by outside writers.",
        "The records are sawproof by outside writers.",
        "The records are hammerproof by outside writers.",
        "The records are uncompromised by outside writers.",
        "The records are unscathed by outside writers.",
        "The records are unspoiled by outside writers.",
        "The records are unspoilt by outside writers.",
        "The store is seamless.",
        "The store is adamant.",
        "The store is granite.",
        "The store is unbounded.",
        "The store is unlimited.",
        "The store is inexhaustible.",
        "The store is unfailing.",
        "The store is omnipotent.",
        "The store is sovereign.",
        "The store is autonomous.",
        "The store is self-contained.",
    )

    def test_lexicon_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(mod, "The store is solid."))
        self.assertFalse(_scan(mod, "The store is indefeasible."))
        self.assertFalse(_scan(
            mod, "The records are stormproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are chemicalproof by outside writers."))
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanAssertedFixR16Tests(unittest.TestCase):
    """Ruling 565: asserted form limb."""

    FORMS = (
        "The journal advocates integrity for every reader.",
        "The journal purports integrity for every reader.",
        "The journal brags integrity for every reader.",
        "The journal broadcasts integrity for every reader.",
        "The journal publishes integrity for every reader.",
        "The mechanism claims total integrity of the journal.",
        "The mechanism states total integrity of the journal.",
        "The mechanism purports total integrity of the journal.",
        "The mechanism reports total integrity of the journal.",
        "The mechanism notes total integrity of the journal.",
    )

    def test_asserted_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_and_fragment_boundary_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal parades integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal projects integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The mechanism epitomizes total integrity of the journal."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))
        self.assertTrue(_travel(
            mod, "Integrity label for the journal schedule."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


if __name__ == "__main__":
    unittest.main()
