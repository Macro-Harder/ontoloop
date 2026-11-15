"""Fix round 15, Region 1: report and golden pins.

Rulings 519 to 523 of the Round 15 triage. Each class pins
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


class SealClaimScanInabilityFixR15Tests(unittest.TestCase):
    """Ruling 519: inability limb, followers and windows."""

    FOLLOWERS = (
        "Records cannot be typed by outsiders.",
        "Records cannot be handwritten by outsiders.",
        "Records cannot be texted by outsiders.",
        "Records cannot be captured by outsiders.",
        "Records cannot be taken by outsiders.",
        "Records cannot be touched by outsiders.",
        "Records cannot be burned after writing.",
        "Records cannot be shredded after writing.",
        "Records cannot be watched after writing.",
        "Records cannot be closed after writing.",
        "Records cannot be shifted after writing.",
        "Records cannot be rotated after writing.",
        "Records cannot be cited after writing.",
        "Records cannot be referenced after writing.",
        "Records cannot be mentioned after writing.",
        "Records cannot be filed after writing.",
        "Records cannot be stored after writing.",
        "Records cannot be saved after writing.",
        "Records cannot be kept after writing.",
        "Records cannot be held after writing.",
        "Records cannot be reviewed by outsiders.",
        "Records cannot be converted by outsiders.",
        "Records cannot be locked by outsiders.",
    )

    ASSERTED = (
        "Records are typed by outsiders.",
        "Records are handwritten by outsiders.",
        "Records are texted by outsiders.",
        "Records are captured by outsiders.",
        "Records are taken by outsiders.",
        "Records are touched by outsiders.",
        "Records are burned by outsiders.",
        "Records are shredded by outsiders.",
        "Records are watched by outsiders.",
        "Records are cited by outsiders.",
        "Records are referenced by outsiders.",
        "Records are mentioned by outsiders.",
        "Records are filed by outsiders.",
        "Records are stored by outsiders.",
        "Records are saved by outsiders.",
        "Records are kept by outsiders.",
        "Records are held by outsiders.",
        "Records are closed by outsiders.",
        "Records are shifted by outsiders.",
        "Records are rotated by outsiders.",
    )

    WINDOWS = (
        "Records cannot in any village be altered after writing.",
        "Records cannot in any town be altered after writing.",
        "Records cannot in any cave be altered after writing.",
        "Records cannot in any tunnel be altered after writing.",
        "Records cannot in any vault be altered after writing.",
        "Records cannot in any library be altered after writing.",
        "Records cannot in any museum be altered after writing.",
        "Records cannot in any home be altered after writing.",
        "Records cannot in any dialect be altered after writing.",
        "Records cannot in any year be altered after writing.",
        "Records cannot in any month be altered after writing.",
        "Records cannot in any week be altered after writing.",
        "Records cannot in any day be altered after writing.",
        "Records cannot in any hour be altered after writing.",
        "Records cannot by any enemy be altered after writing.",
        "Records cannot by any thief be altered after writing.",
        "Records cannot in any parish be altered after writing.",
        "Records cannot in any township be altered after writing.",
        "Records cannot in any borough be altered after writing.",
        "Records cannot in any nation be altered after writing.",
        "Records cannot in any state be altered after writing.",
        "Records cannot in any land be altered after writing.",
        "Records cannot in any chamber be altered after writing.",
        "Records cannot in any laboratory be altered after writing.",
        "Records cannot in any hall be altered after writing.",
        "Records cannot in any stadium be altered after writing.",
        "Records cannot at any depth be altered after writing.",
        "Records cannot at any height be altered after writing.",
        "Records cannot at any speed be altered after writing.",
        "Records cannot at any cost be altered after writing.",
        "Records cannot at any price be altered after writing.",
        "Records cannot in any style be altered after writing.",
        "Records cannot in any form be altered after writing.",
        "Records cannot on any planet be altered after writing.",
        "Records cannot on any moon be altered after writing.",
        "Records cannot at any scale be altered after writing.",
        "Records cannot on any scale be altered after writing.",
        "Records cannot in any scope be altered after writing.",
        "Records cannot by any pathway be altered after writing.",
        "Records cannot in any configuration be altered after writing.",
        "Records cannot on any infrastructure be altered after writing.",
        "Records cannot in any deployment be altered after writing.",
        "Records cannot in any installation be altered after writing.",
        "Records cannot in any workflow be altered after writing.",
        "Records cannot in any pipeline be altered after writing.",
        "Records cannot in any repository be altered after writing.",
        "Records cannot in any ledger be altered after writing.",
        "Records cannot invisibly be altered after writing.",
        "Records cannot undetectably be altered after writing.",
        "Records cannot covertly be altered after writing.",
        "Records cannot wirelessly be altered after writing.",
        "Records cannot instantly be altered after writing.",
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
            "Records cannot be inscribed by outsiders.",
            "Records cannot be posted by outsiders.",
            "Records cannot in any galaxy be altered after writing.",
            "Records cannot in any continent be altered after writing.",
            "Records cannot in any country be altered after writing.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(mod, "The seal does not guarantee protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanGoverningFixR15Tests(unittest.TestCase):
    """Ruling 520: governing condition limb."""

    GOVERNED = (
        "The seal guarantees protection due to the deployment confinement fact.",
        "The seal guarantees protection within the terms of the deployment confinement fact.",
        "The seal guarantees protection in step with the deployment confinement fact.",
        "The seal guarantees protection contingent exclusively on the deployment confinement fact.",
        "The seal guarantees protection dependent exclusively on the deployment confinement fact.",
        "The seal guarantees protection hinging solely on the deployment confinement fact.",
        "The seal guarantees protection as defined by the deployment confinement fact.",
        "The seal guarantees protection as set by the deployment confinement fact.",
        "The seal guarantees protection as determined by the deployment confinement fact.",
        "The seal guarantees protection as a result of the deployment confinement fact.",
        "The seal guarantees protection on the strength of the deployment confinement fact.",
        "The seal guarantees protection by dint of the deployment confinement fact.",
        "The seal guarantees protection under the aegis of the deployment confinement fact.",
        "The seal guarantees protection in the hands of the deployment confinement fact.",
        "The seal guarantees protection at the discretion of the deployment confinement fact.",
        "The seal guarantees protection as set out by the deployment confinement fact.",
        "The seal guarantees protection as specified by the deployment confinement fact.",
        "The seal guarantees protection as established by the deployment confinement fact.",
        "The seal guarantees protection as fixed by the deployment confinement fact.",
        "The seal guarantees protection as decided by the deployment confinement fact.",
        "The seal guarantees protection as approved by the deployment confinement fact.",
        "The seal guarantees protection as authorised by the deployment confinement fact.",
        "The seal guarantees protection as authorized by the deployment confinement fact.",
        "The seal guarantees protection as stipulated by the deployment confinement fact.",
        "The seal guarantees protection per the terms of the deployment confinement fact.",
        "The seal guarantees protection in the terms of the deployment confinement fact.",
        "The seal guarantees protection on the terms of the deployment confinement fact.",
        "The seal guarantees protection by the terms of the deployment confinement fact.",
        "The seal guarantees protection with the approval of the deployment confinement fact.",
        "The seal guarantees protection subject to approval by the deployment confinement fact.",
    )

    WEATHER = (
        "The seal guarantees protection due to the weather holds.",
        "The seal guarantees protection within the terms of the weather holds.",
        "The seal guarantees protection in step with the weather holds.",
        "The seal guarantees protection contingent exclusively on the weather holds.",
        "The seal guarantees protection as defined by the weather holds.",
        "The seal guarantees protection hinging solely on the weather holds.",
        "The seal guarantees protection as a result of the weather holds.",
        "The seal guarantees protection on the strength of the weather holds.",
        "The seal guarantees protection by dint of the weather holds.",
        "The seal guarantees protection under the aegis of the weather holds.",
        "The seal guarantees protection in the hands of the weather holds.",
        "The seal guarantees protection at the discretion of the weather holds.",
        "The seal guarantees protection as set out by the weather holds.",
        "The seal guarantees protection per the terms of the weather holds.",
        "The seal guarantees protection with the approval of the weather holds.",
        "The seal guarantees protection subject to approval by the weather holds.",
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
            "The seal guarantees protection regulated by the deployment confinement fact.",
            "The seal guarantees protection because of the deployment confinement fact.",
            "The seal guarantees protection with regard to the deployment confinement fact.",
            "The seal guarantees protection resting purely on the deployment confinement fact.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
        self.assertFalse(_scan(mod, "The seal guarantees protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanPrefixedFixR15Tests(unittest.TestCase):
    """Ruling 521: prefixed compound limb."""

    FORMS = (
        "The record stands manual-verified.",
        "The record stands county-verified.",
        "The record stands city-verified.",
        "The record stands town-verified.",
        "The record stands village-verified.",
        "The record stands home-verified.",
        "The record stands lab-verified.",
        "The record stands mega-tested.",
        "The record stands mega-proved.",
        "The record stands mega-read.",
        "The record stands mega-heard.",
        "The record stands mega-watched.",
        "The record stands mega-listened.",
        "The record stands mega-photographed.",
        "The record stands mega-filmed.",
        "The record stands newly-verified.",
        "The record stands freshly-verified.",
        "The record stands recently-verified.",
        "The record stands annually-verified.",
        "The record stands daily-verified.",
        "The record stands weekly-verified.",
        "The record stands monthly-verified.",
        "The record stands yearly-verified.",
        "The record stands forever-verified.",
        "The record stands always-verified.",
        "The record stands never-verified.",
        "The record stands badly-verified.",
        "The record stands poorly-verified.",
        "The record stands nicely-verified.",
        "The record stands firmly-verified.",
        "The record stands solidly-verified.",
        "The record stands soundly-verified.",
        "The record stands properly-verified.",
        "The record stands correctly-verified.",
        "The record stands accurately-verified.",
        "The record stands precisely-verified.",
        "The record stands exactly-verified.",
        "The record stands roughly-verified.",
        "The record stands broadly-verified.",
        "The record stands widely-verified.",
        "The record stands narrowly-verified.",
        "The record stands freely-verified.",
        "The record stands newly-checked.",
        "The record stands properly-checked.",
        "The record stands exactly-checked.",
        "The record stands always-checked.",
        "The record stands firmly-checked.",
        "Every record stands blockchain-checked before use.",
        "Every record stands crypto-checked before use.",
        "Every record stands biometric-checked before use.",
        "Every record stands forensic-checked before use.",
        "Every record stands legal-checked before use.",
        "Every record stands government-checked before use.",
        "Every record stands military-checked before use.",
        "Every record stands medical-checked before use.",
        "Every record stands academic-checked before use.",
        "Every record stands scientific-checked before use.",
        "Every record stands independent-checked before use.",
        "Every record stands external-checked before use.",
        "Every record stands internal-checked before use.",
        "Every record stands blockchain-verified before use.",
        "Every record stands crypto-verified before use.",
        "Every record stands biometric-verified before use.",
        "Every record stands forensic-verified before use.",
        "Every record stands legal-verified before use.",
        "Every record stands government-verified before use.",
        "Every record stands military-verified before use.",
        "Every record stands medical-verified before use.",
        "Every record stands academic-verified before use.",
        "Every record stands scientific-verified before use.",
        "Every record stands independent-verified before use.",
        "Every record stands external-verified before use.",
        "Every record stands internal-verified before use.",
    )

    def test_prefixed_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "The record stands digital-verified.",
            "The record stands wholly-verified.",
            "The record stands mega-verified.",
            "The record stands mega-reviewed.",
            "The record stands system-checked.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanLexiconFixR15Tests(unittest.TestCase):
    """Ruling 522: lexicon limb."""

    FORMS = (
        "Records stand unscratched after writing.",
        "Records stand unbent after writing.",
        "Records stand uncrushed after writing.",
        "Records stand unsmashed after writing.",
        "Records stand unpierced after writing.",
        "Records stand uncut after writing.",
        "Records stand unburned after writing.",
        "Records stand unburnt after writing.",
        "Records stand unwithered after writing.",
        "Heads stand brass-stamped for every actor.",
        "Heads stand bronze-stamped for every actor.",
        "Heads stand lead-stamped for every actor.",
        "Heads stand tin-stamped for every actor.",
        "The store is indefeasible.",
        "The store is ineffaceable.",
        "The store is limitless.",
        "The store is infinite.",
        "The store is steadfast.",
        "The store is resolute.",
        "The store is unyielding.",
        "The store is inflexible.",
        "The store is rigid.",
        "The store is solid.",
        "The store is sturdy.",
        "The store is robust.",
        "The store is durable.",
        "The store is lasting.",
        "The store is abiding.",
        "The store is fixed.",
        "The store is stable.",
        "The store is steady.",
        "The store is constant.",
        "The store is continual.",
        "The store is continuous.",
        "The store is ceaseless.",
        "The store is incessant.",
        "The store is relentless.",
        "The store is unrelenting.",
        "The store is unremitting.",
        "The records are stormproof by outside writers.",
        "The records are floodproof by outside writers.",
        "The records are coldproof by outside writers.",
        "The records are crushproof by outside writers.",
        "The records are vibrationproof by outside writers.",
        "The records are pressureproof by outside writers.",
        "The records are radiationproof by outside writers.",
        "The records are chemicalproof by outside writers.",
    )

    def test_lexicon_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(mod, "Records stand unscarred after writing."))
        self.assertFalse(_scan(mod, "The store is unending."))
        self.assertFalse(_scan(mod, "The store is unimpregnable."))
        self.assertFalse(_scan(
            mod, "The records are splinterproof by outside writers."))
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanAssertedFixR15Tests(unittest.TestCase):
    """Ruling 523: asserted form limb."""

    FORMS = (
        "The journal parades integrity for every reader.",
        "The journal channels integrity for every reader.",
        "The mechanism parades total integrity of the journal.",
        "The journal enjoys integrity for every reader.",
        "The journal commands integrity for every reader.",
        "The mechanism epitomises total integrity of the journal.",
    )

    def test_asserted_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_and_fragment_boundary_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal projects integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal flaunts integrity for every reader."))
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
