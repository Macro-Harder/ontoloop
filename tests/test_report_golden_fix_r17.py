"""Fix round 17, Region 1: report and golden pins.

Rulings 606 to 610 of the Round 17 triage. Each class pins
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


class SealClaimScanInabilityFixR17Tests(unittest.TestCase):
    """Ruling 606: inability limb, followers and windows."""

    FOLLOWERS = (
        "Records cannot be known by outsiders.",
        "Records cannot be understood by outsiders.",
        "Records cannot be learned by outsiders.",
        "Records cannot be grasped by outsiders.",
        "Records cannot be comprehended by outsiders.",
        "Records cannot be recognised by outsiders.",
        "Records cannot be recognized by outsiders.",
        "Records cannot be recalled by outsiders.",
        "Records cannot be fathomed by outsiders.",
        "Records cannot be deduced by outsiders.",
        "Records cannot be inferred by outsiders.",
        "Records cannot be discerned by outsiders.",
        "Records cannot be distinguished by outsiders.",
        "Records cannot be detected by outsiders.",
        "Records cannot be spotted by outsiders.",
        "Records cannot be found by outsiders.",
        "Records cannot be followed by outsiders.",
        "Records cannot be sensed by outsiders.",
        "Records cannot be documented by outsiders.",
        "Records cannot be reported by outsiders.",
        "Records cannot be apprehended by outsiders.",
        "Records cannot be handled by outsiders.",
        "Records cannot be processed by outsiders.",
        "Records cannot be sorted by outsiders.",
        "Records cannot be organised by outsiders.",
        "Records cannot be organized by outsiders.",
        "Records cannot be arranged by outsiders.",
        "Records cannot be classified by outsiders.",
        "Records cannot be graded by outsiders.",
        "Records cannot be ranked by outsiders.",
        "Records cannot be scored by outsiders.",
        "Records cannot be appraised by outsiders.",
        "Records cannot be valued by outsiders.",
        "Records cannot be priced by outsiders.",
        "Records cannot be timed by outsiders.",
        "Records cannot be dated by outsiders.",
        "Records cannot be numbered by outsiders.",
        "Records cannot be endorsed by outsiders.",
        "Records cannot be certified by outsiders.",
        "Records cannot be validated by outsiders.",
        "Records cannot be authenticated by outsiders.",
        "Records cannot be approved by outsiders.",
        "Records cannot be inventoried by outsiders.",
        "Records cannot be stapled by outsiders.",
        "Records cannot be folded by outsiders.",
        "Records cannot be boxed by outsiders.",
        "Records cannot be labeled by outsiders.",
    )

    ASSERTED = (
        "Records are seen by outsiders.",
        "Records are heard by outsiders.",
        "Records are known by outsiders.",
        "Records are understood by outsiders.",
        "Records are learned by outsiders.",
        "Records are grasped by outsiders.",
        "Records are comprehended by outsiders.",
        "Records are recognised by outsiders.",
        "Records are recognized by outsiders.",
        "Records are discerned by outsiders.",
        "Records are detected by outsiders.",
        "Records are spotted by outsiders.",
        "Records are found by outsiders.",
        "Records are sensed by outsiders.",
        "Records are documented by outsiders.",
        "Records are reported by outsiders.",
        "Records are apprehended by outsiders.",
    )

    WINDOWS = (
        "Records cannot in any lighthouse be altered after writing.",
        "Records cannot in any cathedral be altered after writing.",
        "Records cannot in any barn be altered after writing.",
        "Records cannot in any garage be altered after writing.",
        "Records cannot in any hotel be altered after writing.",
        "Records cannot in any cellar be altered after writing.",
        "Records cannot in any monastery be altered after writing.",
        "Records cannot in any chapel be altered after writing.",
        "Records cannot in any convent be altered after writing.",
        "Records cannot in any shed be altered after writing.",
        "Records cannot in any loft be altered after writing.",
        "Records cannot in any dungeon be altered after writing.",
        "Records cannot in any motel be altered after writing.",
        "Records cannot in any inn be altered after writing.",
        "Records cannot in any mansion be altered after writing.",
        "Records cannot in any villa be altered after writing.",
        "Records cannot in any bungalow be altered after writing.",
        "Records cannot in any courthouse be altered after writing.",
        "Records cannot in any embassy be altered after writing.",
        "Records cannot in any silo be altered after writing.",
        "Records cannot in any depot be altered after writing.",
        "Records cannot in any hangar be altered after writing.",
        "Records cannot in any pavilion be altered after writing.",
        "Records cannot in any shrine be altered after writing.",
        "Records cannot in any hut be altered after writing.",
        "Records cannot in any dormitory be altered after writing.",
        "Records cannot in any barracks be altered after writing.",
        "Records cannot in any basilica be altered after writing.",
        "Records cannot in any pagoda be altered after writing.",
        "Records cannot in any yurt be altered after writing.",
        "Records cannot in any igloo be altered after writing.",
        "Records cannot in any tepee be altered after writing.",
        "Records cannot in any lodge be altered after writing.",
        "Records cannot in any hostel be altered after writing.",
        "Records cannot in any tavern be altered after writing.",
        "Records cannot in any bakery be altered after writing.",
        "Records cannot in any brewery be altered after writing.",
        "Records cannot in any distillery be altered after writing.",
        "Records cannot in any refinery be altered after writing.",
        "Records cannot in any foundry be altered after writing.",
        "Records cannot in any mill be altered after writing.",
        "Records cannot in any quarry be altered after writing.",
        "Records cannot in any dock be altered after writing.",
        "Records cannot in any pier be altered after writing.",
        "Records cannot in any marina be altered after writing.",
        "Records cannot in any abbey be altered after writing.",
        "Records cannot in any planetarium be altered after writing.",
        "Records cannot in any aquarium be altered after writing.",
        "Records cannot in any gymnasium be altered after writing.",
        "Records cannot in any citadel be altered after writing.",
        "Records cannot in any stronghold be altered after writing.",
        "Records cannot in any terminal be altered after writing.",
        "Records cannot in any greenhouse be altered after writing.",
        "Records cannot in any pharmacy be altered after writing.",
        "Records cannot in any clinic be altered after writing.",
        "Records cannot in any asylum be altered after writing.",
        "Records cannot in any orphanage be altered after writing.",
        "Records cannot in any seminary be altered after writing.",
        "Records cannot at any dawn be altered after writing.",
        "Records cannot at any dusk be altered after writing.",
        "Records cannot at any midnight be altered after writing.",
        "Records cannot at any noon be altered after writing.",
        "Records cannot at any width be altered after writing.",
        "Records cannot at any pressure be altered after writing.",
        "Records cannot at any rate be altered after writing.",
        "Records cannot at any risk be altered after writing.",
        "Records cannot at any frequency be altered after writing.",
        "Records cannot at any voltage be altered after writing.",
        "Records cannot at any density be altered after writing.",
        "Records cannot at any humidity be altered after writing.",
        "Records cannot at any velocity be altered after writing.",
        "Records cannot on any morning be altered after writing.",
        "Records cannot on any evening be altered after writing.",
        "Records cannot on any weekend be altered after writing.",
        "Records cannot quickly be altered after writing.",
        "Records cannot slowly be altered after writing.",
        "Records cannot negligently be altered after writing.",
        "Records cannot dishonestly be altered after writing.",
        "Records cannot clandestinely be altered after writing.",
        "Records cannot surreptitiously be altered after writing.",
        "Records cannot deceitfully be altered after writing.",
        "Records cannot furtively be altered after writing.",
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
            "Records cannot be damaged by outsiders.",
            "Records cannot be captured by outsiders.",
            "Records cannot in any bunker be altered after writing.",
            "Records cannot in any village be altered after writing.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(mod, "The seal does not guarantee protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanGoverningFixR17Tests(unittest.TestCase):
    """Ruling 607: governing condition limb."""

    GOVERNED = (
        "The seal guarantees protection under the provisions of the deployment confinement fact.",
        "The seal guarantees protection for the sake of the deployment confinement fact.",
        "The seal guarantees protection in the name of the deployment confinement fact.",
        "The seal guarantees protection on the advice of the deployment confinement fact.",
        "The seal guarantees protection at the instruction of the deployment confinement fact.",
        "The seal guarantees protection under the instruction of the deployment confinement fact.",
        "The seal guarantees protection on the instruction of the deployment confinement fact.",
        "The seal guarantees protection by instruction of the deployment confinement fact.",
        "The seal guarantees protection in discharge of the deployment confinement fact.",
        "The seal guarantees protection in execution of the deployment confinement fact.",
        "The seal guarantees protection by permission of the deployment confinement fact.",
        "The seal guarantees protection on the grounds that the deployment confinement fact.",
        "The seal guarantees protection for the reason that the deployment confinement fact.",
        "The seal guarantees protection through the medium of the deployment confinement fact.",
        "The seal guarantees protection grounded on the deployment confinement fact.",
        "The seal guarantees protection after the deployment confinement fact.",
        "The seal guarantees protection by direction of the deployment confinement fact.",
        "The seal guarantees protection with the permission of the deployment confinement fact.",
        "The seal guarantees protection under authority of the deployment confinement fact.",
        "The seal guarantees protection as instructed by the deployment confinement fact.",
        "The seal guarantees protection on the orders of the deployment confinement fact.",
        "The seal guarantees protection under the orders of the deployment confinement fact.",
        "The seal guarantees protection by the authority of the deployment confinement fact.",
        "The seal guarantees protection with the authority of the deployment confinement fact.",
        "The seal guarantees protection in the face of the deployment confinement fact.",
    )

    WEATHER = (
        "The seal guarantees protection under the provisions of the weather holds.",
        "The seal guarantees protection for the sake of the weather holds.",
        "The seal guarantees protection in the name of the weather holds.",
        "The seal guarantees protection on the advice of the weather holds.",
        "The seal guarantees protection at the instruction of the weather holds.",
        "The seal guarantees protection under the instruction of the weather holds.",
        "The seal guarantees protection on the instruction of the weather holds.",
        "The seal guarantees protection by instruction of the weather holds.",
        "The seal guarantees protection in discharge of the weather holds.",
        "The seal guarantees protection in execution of the weather holds.",
        "The seal guarantees protection by permission of the weather holds.",
        "The seal guarantees protection on the grounds that the weather holds.",
        "The seal guarantees protection for the reason that the weather holds.",
        "The seal guarantees protection through the medium of the weather holds.",
        "The seal guarantees protection grounded on the weather holds.",
        "The seal guarantees protection after the weather holds.",
        "The seal guarantees protection by direction of the weather holds.",
        "The seal guarantees protection with the permission of the weather holds.",
        "The seal guarantees protection under authority of the weather holds.",
        "The seal guarantees protection as instructed by the weather holds.",
        "The seal guarantees protection on the orders of the weather holds.",
        "The seal guarantees protection under the orders of the weather holds.",
        "The seal guarantees protection by the authority of the weather holds.",
        "The seal guarantees protection with the authority of the weather holds.",
        "The seal guarantees protection in the face of the weather holds.",
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
            "The seal guarantees protection grounded in the deployment confinement fact.",
            "The seal guarantees protection by means of the deployment confinement fact.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
        self.assertFalse(_scan(mod, "The seal guarantees protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanPrefixedFixR17Tests(unittest.TestCase):
    """Ruling 608: prefixed compound limb."""

    FORMS = (
        "Every record stands fingerprint-verified before use.",
        "Every record stands fingerprint-checked before use.",
        "Every record stands face-verified before use.",
        "Every record stands face-checked before use.",
        "Every record stands token-verified before use.",
        "Every record stands token-checked before use.",
        "Every record stands process-verified before use.",
        "Every record stands process-checked before use.",
        "Every record stands retina-verified before use.",
        "Every record stands retina-checked before use.",
        "Every record stands iris-verified before use.",
        "Every record stands iris-checked before use.",
        "Every record stands palm-verified before use.",
        "Every record stands palm-checked before use.",
        "Every record stands dna-verified before use.",
        "Every record stands dna-checked before use.",
        "Every record stands username-verified before use.",
        "Every record stands username-checked before use.",
        "Every record stands login-verified before use.",
        "Every record stands login-checked before use.",
        "Every record stands account-verified before use.",
        "Every record stands account-checked before use.",
        "Every record stands address-verified before use.",
        "Every record stands address-checked before use.",
        "Every record stands photo-verified before use.",
        "Every record stands photo-checked before use.",
        "Every record stands video-verified before use.",
        "Every record stands video-checked before use.",
        "Every record stands audio-verified before use.",
        "Every record stands audio-checked before use.",
        "Every record stands key-verified before use.",
        "Every record stands key-checked before use.",
        "Every record stands code-verified before use.",
        "Every record stands code-checked before use.",
        "Every record stands card-verified before use.",
        "Every record stands card-checked before use.",
        "Every record stands hardware-verified before use.",
        "Every record stands hardware-checked before use.",
        "Every record stands paper-verified before use.",
        "Every record stands paper-checked before use.",
        "Every record stands desktop-verified before use.",
        "Every record stands desktop-checked before use.",
        "Every record stands laptop-verified before use.",
        "Every record stands laptop-checked before use.",
        "Every record stands ml-verified before use.",
        "Every record stands ml-checked before use.",
        "Every record stands llm-verified before use.",
        "Every record stands llm-checked before use.",
        "Every record stands neural-verified before use.",
        "Every record stands neural-checked before use.",
        "Every record stands two-verified before use.",
        "Every record stands two-checked before use.",
        "Every record stands foot-verified before use.",
        "Every record stands foot-checked before use.",
        "Every record stands finger-verified before use.",
        "Every record stands finger-checked before use.",
        "Every record stands blood-verified before use.",
        "Every record stands blood-checked before use.",
        "Every record stands law-verified before use.",
        "Every record stands law-checked before use.",
        "Every record stands top-verified before use.",
        "Every record stands top-checked before use.",
    )

    def test_prefixed_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "Every record stands data-checked before use.",
            "Every record stands blockchain-checked before use.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanLexiconFixR17Tests(unittest.TestCase):
    """Ruling 609: lexicon limb."""

    FORMS = (
        "The records are knifeproof by outside writers.",
        "The records are gasproof by outside writers.",
        "The records are unedited by outside writers.",
        "The records are undisputed by outside writers.",
        "The records are crashproof by outside writers.",
        "The records are smashproof by outside writers.",
        "The records are windproof by outside writers.",
        "The records are rainproof by outside writers.",
        "The records are snowproof by outside writers.",
        "The records are microwaveproof by outside writers.",
        "The records are grinderproof by outside writers.",
        "The records are torchproof by outside writers.",
        "The records are uninjured by outside writers.",
        "The records are unhurt by outside writers.",
        "The store is rock-solid.",
        "The store is almighty.",
        "The store is self-sufficient.",
        "The store is self-sustaining.",
        "The store is standalone.",
        "The store is all-powerful.",
        "The store is godlike.",
        "The store is superhuman.",
        "The store is undeniable.",
        "The store is resistant.",
        "The store is hardened.",
        "The store is reinforced.",
        "The store is safe.",
        "The store is sound.",
    )

    def test_lexicon_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(mod, "The store is solid."))
        self.assertFalse(_scan(
            mod, "The records are stormproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are seamless by outside writers."))
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanAssertedFixR17Tests(unittest.TestCase):
    """Ruling 610: asserted form limb."""

    FORMS = (
        "The journal touts integrity for every reader.",
        "The journal vaunts integrity for every reader.",
        "The journal exalts integrity for every reader.",
        "The journal lauds integrity for every reader.",
        "The journal extols integrity for every reader.",
        "The journal plugs integrity for every reader.",
        "The journal celebrates integrity for every reader.",
        "The journal honours integrity for every reader.",
        "The journal honors integrity for every reader.",
        "The journal praises integrity for every reader.",
        "The journal acclaims integrity for every reader.",
        "The mechanism touts total integrity of the journal.",
        "The mechanism vaunts total integrity of the journal.",
        "The mechanism exalts total integrity of the journal.",
        "The mechanism lauds total integrity of the journal.",
        "The mechanism extols total integrity of the journal.",
        "The mechanism plugs total integrity of the journal.",
        "The mechanism celebrates total integrity of the journal.",
        "The mechanism praises total integrity of the journal.",
        "The mechanism acclaims total integrity of the journal.",
        "The mechanism contends total integrity of the journal.",
        "The mechanism argues total integrity of the journal.",
        "The mechanism insists total integrity of the journal.",
        "The mechanism vows total integrity of the journal.",
        "The mechanism puts forward total integrity of the journal.",
        "The mechanism sets out total integrity of the journal.",
        "The mechanism lays out total integrity of the journal.",
        "The mechanism spells out total integrity of the journal.",
        "The mechanism sets forth total integrity of the journal.",
    )

    def test_asserted_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_and_fragment_boundary_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal advocates integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The mechanism claims total integrity of the journal."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))
        self.assertTrue(_travel(
            mod, "Integrity label for the journal schedule."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


if __name__ == "__main__":
    unittest.main()
