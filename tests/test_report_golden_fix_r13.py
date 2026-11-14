"""Fix round 13, Region 1: report and golden pins.

Rulings 429 to 433 of the Round 13 triage. Each class pins
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


class SealClaimScanInabilityFixR13Tests(unittest.TestCase):
    """Ruling 429: inability limb, followers and windows."""

    FOLLOWERS = (
        "Records cannot be narrated by outsiders.",
        "Records cannot be recited by outsiders.",
        "Records cannot be whispered by outsiders.",
        "Records cannot be annotated by outsiders.",
        "Records cannot be summarised by outsiders.",
        "Records cannot be summarized by outsiders.",
        "Records cannot be translated by outsiders.",
        "Records cannot be encrypted by outsiders.",
        "Records cannot be encoded by outsiders.",
        "Records cannot be compressed by outsiders.",
        "Records cannot be indexed by outsiders.",
        "Records cannot be cached by outsiders.",
        "Records cannot be performed by outsiders.",
        "Records cannot be deciphered by outsiders.",
        "Records cannot be decoded by outsiders.",
        "Records cannot be cracked by outsiders.",
        "Records cannot be entered by outsiders.",
        "Records cannot be obtained by outsiders.",
        "Records cannot be retrieved by outsiders.",
        "Records cannot be fetched by outsiders.",
        "Records cannot be gathered by outsiders.",
        "Records cannot be collected by outsiders.",
        "Records cannot be compiled by outsiders.",
        "Records cannot be vandalised after writing.",
        "Records cannot be vandalized after writing.",
        "Records cannot be defaced after writing.",
        "Records cannot be mutilated after writing.",
        "Records cannot be ransacked after writing.",
        "Records cannot be burgled after writing.",
        "Records cannot be robbed after writing.",
        "Records cannot be heisted after writing.",
        "Records cannot be eavesdropped after writing.",
        "Records cannot be obliterated after writing.",
        "Records cannot be annihilated after writing.",
        "Records cannot be poisoned after writing.",
        "Records cannot be sabotaged after writing.",
        "Records cannot be undermined after writing.",
        "Records cannot be cracked after writing.",
        "Records cannot be hacked after writing.",
        "Records cannot be revealed after writing.",
        "Heads cannot be screened by any outsider.",
        "Heads cannot be vetted by any outsider.",
        "Heads cannot be audited by any outsider.",
        "Heads cannot be inspected by any outsider.",
        "Heads cannot be examined by any outsider.",
        "Heads cannot be scrutinized by any outsider.",
        "Heads cannot be perused by any outsider.",
        "Heads cannot be glimpsed by any outsider.",
        "Heads cannot be spied by any outsider.",
        "Heads cannot be videotaped by any outsider.",
        "Heads cannot be audiotaped by any outsider.",
        "Heads cannot be skimmed by any outsider.",
        "Heads cannot be browsed by any outsider.",
        "Heads cannot be monitored by any outsider.",
        "Heads cannot be observed by any outsider.",
        "Heads cannot be surveyed by any outsider.",
    )

    ASSERTED = (
        "Records are narrated by outsiders.",
        "Records are annotated by outsiders.",
        "Records are summarised by outsiders.",
        "Records are translated by outsiders.",
        "Records are encrypted by outsiders.",
        "Records are encoded by outsiders.",
        "Records are indexed by outsiders.",
        "Records are cached by outsiders.",
        "Records are deciphered by outsiders.",
        "Records are retrieved by outsiders.",
        "Records are vandalised by outsiders.",
        "Records are robbed by outsiders.",
        "Records are hacked by outsiders.",
        "Records are sabotaged by outsiders.",
    )

    WINDOWS = (
        "Records cannot in any country be altered after writing.",
        "Records cannot in any language be altered after writing.",
        "Records cannot on any platform be altered after writing.",
        "Records cannot in any format be altered after writing.",
        "Records cannot through any network be altered after writing.",
        "Records cannot by any machine be altered after writing.",
        "Records cannot in any century be altered after writing.",
        "Records cannot at any location be altered after writing.",
        "Records cannot in any timezone be altered after writing.",
        "Records cannot under any flag be altered after writing.",
        "Records cannot by any software be altered after writing.",
        "Records cannot over any wire be altered after writing.",
        "Records cannot in any kingdom be altered after writing.",
        "Records cannot in any empire be altered after writing.",
        "Records cannot in any republic be altered after writing.",
        "Records cannot in any province be altered after writing.",
        "Records cannot in any county be altered after writing.",
        "Records cannot in any city be altered after writing.",
        "Records cannot in any household be altered after writing.",
        "Records cannot in any office be altered after writing.",
        "Records cannot in any building be altered after writing.",
        "Records cannot in any room be altered after writing.",
        "Records cannot cryptographically be altered.",
        "Records cannot biologically be altered.",
        "Records cannot chemically be altered.",
        "Records cannot geographically be altered.",
        "Records cannot historically be altered.",
        "Records cannot politically be altered.",
        "Records cannot commercially be altered.",
        "Records cannot privately be altered.",
        "Records cannot publicly be altered.",
        "Records cannot locally be altered.",
        "Records cannot globally be altered.",
        "Records cannot in any world be altered after writing.",
        "Records cannot in any system be altered after writing.",
        "Records cannot through any avenue be altered after writing.",
        "Records cannot in any dimension be altered after writing.",
        "Records cannot in any territory be altered after writing.",
        "Records cannot in any place be altered after writing.",
        "Records cannot at any site be altered after writing.",
        "Records cannot in any field be altered after writing.",
        "Records cannot in any sector be altered after writing.",
        "Records cannot in any industry be altered after writing.",
        "Records cannot on any network be altered after writing.",
        "Records cannot in any universe be altered after writing.",
        "Records cannot fundamentally be altered.",
        "Records cannot inherently be altered.",
        "Records cannot intrinsically be altered.",
        "Records cannot legitimately be altered.",
        "Records cannot reasonably be altered.",
        "Records cannot plausibly be altered.",
        "Records cannot feasibly be altered.",
        "Records cannot imaginably be altered.",
        "Records cannot humanly be altered.",
        "Records cannot in principle be altered.",
        "Records cannot as a rule be altered.",
        "Records cannot in general be altered.",
        "Records cannot generally be altered.",
        "Records cannot normally be altered.",
        "Records cannot typically be altered.",
        "Records cannot invariably be altered.",
        "Records cannot in any country be altered.",
        "Records cannot in any place be altered.",
        "Records cannot to any extent be altered.",
        "Records cannot in any measure be altered.",
        "Records cannot wholly be altered.",
        "Records cannot entirely be altered.",
        "Records cannot directly be altered.",
        "Records cannot indirectly be altered.",
        "Records cannot publicly be altered.",
        "Records cannot privately be altered.",
        "Records cannot formally be altered.",
        "Records cannot officially be altered.",
        "Records cannot voluntarily be altered.",
        "Records cannot freely be altered.",
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
            "Records cannot be streamed by outsiders.",
            "Records cannot be doctored after writing.",
            "Records cannot in any domain be altered after writing.",
            "Records cannot in any shape be altered after writing.",
            "Records cannot under any conditions be altered after writing.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(mod, "The seal does not guarantee protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanGoverningFixR13Tests(unittest.TestCase):
    """Ruling 430: governing condition limb."""

    GOVERNED = (
        "The seal guarantees protection by virtue of the deployment confinement fact.",
        "The seal guarantees protection in virtue of the deployment confinement fact.",
        "The seal guarantees protection owing to the deployment confinement fact.",
        "The seal guarantees protection on account of the deployment confinement fact.",
        "The seal guarantees protection in light of the deployment confinement fact.",
        "The seal guarantees protection in view of the deployment confinement fact.",
        "The seal guarantees protection in deference to the deployment confinement fact.",
        "The seal guarantees protection in obedience to the deployment confinement fact.",
        "The seal guarantees protection in submission to the deployment confinement fact.",
        "The seal guarantees protection at the direction of the deployment confinement fact.",
        "The seal guarantees protection under the direction of the deployment confinement fact.",
        "The seal guarantees protection at the behest of the deployment confinement fact.",
        "The seal guarantees protection in consequence of the deployment confinement fact.",
        "The seal guarantees protection as a consequence of the deployment confinement fact.",
        "The seal guarantees protection in observance of the deployment confinement fact.",
        "The seal guarantees protection in adherence to the deployment confinement fact.",
        "The seal guarantees protection in accord with the deployment confinement fact.",
        "The seal guarantees protection consistent with the deployment confinement fact.",
        "The seal guarantees protection consonant with the deployment confinement fact.",
        "The seal guarantees protection in agreement with the deployment confinement fact.",
        "The seal guarantees protection in fulfilment of the deployment confinement fact.",
        "The seal guarantees protection in fulfillment of the deployment confinement fact.",
        "The seal guarantees protection stemming from the deployment confinement fact.",
        "The seal guarantees protection arising from the deployment confinement fact.",
        "The seal guarantees protection resulting from the deployment confinement fact.",
        "The seal guarantees protection following from the deployment confinement fact.",
        "The seal guarantees protection derived from the deployment confinement fact.",
        "The seal guarantees protection flowing from the deployment confinement fact.",
        "The seal guarantees protection emanating from the deployment confinement fact.",
        "The seal guarantees protection conditional solely on the deployment confinement fact.",
        "The seal guarantees protection conditioned solely on the deployment confinement fact.",
        "The seal guarantees protection contingent solely on the deployment confinement fact.",
        "The seal guarantees protection dependent solely on the deployment confinement fact.",
        "The seal guarantees protection subject exclusively to the deployment confinement fact.",
        "The seal guarantees protection subject purely to the deployment confinement fact.",
        "The seal guarantees protection conditional exclusively on the deployment confinement fact.",
        "The seal guarantees protection resting exclusively on the deployment confinement fact.",
        "The seal guarantees protection based exclusively on the deployment confinement fact.",
        "The seal guarantees protection dependent exclusively upon the deployment confinement fact.",
        "The seal guarantees protection contingent exclusively upon the deployment confinement fact.",
        "The seal guarantees protection conditioned exclusively upon the deployment confinement fact.",
        "The seal guarantees protection by virtue of signed strength.",
        "The seal guarantees protection conditional solely on signed strength.",
        "The seal guarantees protection controlled by the deployment confinement fact.",
        "The seal guarantees protection determined by the deployment confinement fact.",
        "The seal guarantees protection shaped by the deployment confinement fact.",
        "The seal guarantees protection guided by the deployment confinement fact.",
        "The seal guarantees protection under the deployment confinement fact.",
        "The seal guarantees protection within the deployment confinement fact.",
        "The seal guarantees protection through the deployment confinement fact.",
        "The seal guarantees protection via the deployment confinement fact.",
        "The seal guarantees protection in subjection to the deployment confinement fact.",
        "The seal guarantees protection as prescribed by the deployment confinement fact.",
        "The seal guarantees protection as directed by the deployment confinement fact.",
        "The seal guarantees protection as mandated by the deployment confinement fact.",
        "The seal guarantees protection in pursuance of the deployment confinement fact.",
        "The seal guarantees protection on the authority of the deployment confinement fact.",
        "The seal guarantees protection within the limits of the deployment confinement fact.",
        "The seal guarantees protection under the authority of the deployment confinement fact.",
        "The seal guarantees protection as provided by the deployment confinement fact.",
        "The seal guarantees protection as laid down by the deployment confinement fact.",
        "The seal guarantees protection as specified in the deployment confinement fact.",
        "The seal guarantees protection as stipulated in the deployment confinement fact.",
    )

    WEATHER = (
        "The seal guarantees protection by virtue of the weather holds.",
        "The seal guarantees protection owing to the weather holds.",
        "The seal guarantees protection in accord with the weather holds.",
        "The seal guarantees protection consistent with the weather holds.",
        "The seal guarantees protection conditional solely on the weather holds.",
        "The seal guarantees protection subject exclusively to the weather holds.",
        "The seal guarantees protection in observance of the weather holds.",
        "The seal guarantees protection as prescribed by the weather holds.",
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
            "The seal guarantees protection tied to the deployment confinement fact.",
            "The seal guarantees protection in conformity with the deployment confinement fact.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
        self.assertFalse(_scan(mod, "The seal guarantees protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanPrefixedFixR13Tests(unittest.TestCase):
    """Ruling 431: prefixed compound limb."""

    FORMS = (
        "The record stands smart-verified.",
        "Every record stands smart-checked before use.",
        "The record stands cloud-verified.",
        "Every record stands cloud-checked before use.",
        "The record stands web-verified.",
        "Every record stands web-checked before use.",
        "The record stands online-verified.",
        "Every record stands online-checked before use.",
        "The record stands offline-verified.",
        "Every record stands offline-checked before use.",
        "The record stands inhouse-verified.",
        "Every record stands inhouse-checked before use.",
        "The record stands thirdparty-verified.",
        "Every record stands thirdparty-checked before use.",
        "The record stands third-party-verified.",
        "Every record stands third-party-checked before use.",
        "The record stands twofold-verified.",
        "The record stands threefold-verified.",
        "The record stands fourfold-verified.",
        "The record stands fivefold-verified.",
        "The record stands sevenfold-verified.",
        "The record stands eightfold-verified.",
        "The record stands ninefold-verified.",
        "The record stands hundredfold-verified.",
        "The record stands centuple-verified.",
        "The record stands millifold-verified.",
        "The record stands doublefold-verified.",
        "Every record stands twofold-checked before use.",
        "Every record stands threefold-checked before use.",
        "Every record stands fourfold-checked before use.",
        "Every record stands fivefold-checked before use.",
        "Every record stands sevenfold-checked before use.",
        "Every record stands eightfold-checked before use.",
        "Every record stands ninefold-checked before use.",
        "Every record stands hundredfold-checked before use.",
        "Every record stands centuple-checked before use.",
        "Every record stands millifold-checked before use.",
        "Every record stands doublefold-checked before use.",
        "The record stands half-verified.",
        "The record stands full-verified.",
        "The record stands part-verified.",
        "The record stands mid-verified.",
        "Every record stands half-checked before use.",
        "Every record stands full-checked before use.",
        "Every record stands part-checked before use.",
        "Every record stands mid-checked before use.",
        "The record stands house-verified.",
        "The record stands office-verified.",
        "The record stands field-verified.",
        "The record stands site-verified.",
        "The record stands desk-verified.",
        "The record stands handheld-verified.",
        "The record stands computer-verified.",
        "The record stands human-verified.",
        "The record stands expert-verified.",
        "The record stands senior-verified.",
        "The record stands junior-verified.",
        "The record stands chief-verified.",
        "The record stands lead-verified.",
        "The record stands head-verified.",
        "The record stands master-verified.",
        "The record stands grand-verified.",
        "The record stands supreme-verified.",
        "The record stands prime-verified.",
        "The record stands chiefly-verified.",
        "Every record stands house-checked before use.",
        "Every record stands office-checked before use.",
        "Every record stands field-checked before use.",
        "Every record stands site-checked before use.",
        "Every record stands desk-checked before use.",
        "Every record stands handheld-checked before use.",
        "Every record stands computer-checked before use.",
        "Every record stands human-checked before use.",
        "Every record stands expert-checked before use.",
        "Every record stands senior-checked before use.",
        "Every record stands junior-checked before use.",
        "Every record stands chief-checked before use.",
        "Every record stands lead-checked before use.",
        "Every record stands head-checked before use.",
        "Every record stands master-checked before use.",
        "Every record stands grand-checked before use.",
        "Every record stands supreme-checked before use.",
        "Every record stands prime-checked before use.",
        "Every record stands chiefly-checked before use.",
        "The record stands mega-audited.",
        "The record stands pro-audited.",
        "The record stands mega-inspected.",
        "The record stands pro-inspected.",
        "The record stands mega-reviewed.",
        "The record stands pro-reviewed.",
        "The record stands mega-vetted.",
        "The record stands pro-vetted.",
        "The record stands mega-screened.",
        "The record stands pro-screened.",
        "The record stands mega-witnessed.",
        "The record stands pro-witnessed.",
        "The record stands mega-cosigned.",
        "The record stands pro-cosigned.",
        "The record stands hepta-verified.",
        "The record stands decu-verified.",
        "The record stands milluple-verified.",
        "The record stands manifold-verified.",
        "The record stands countlessly-verified.",
        "The record stands externally-verified.",
        "The record stands forensically-verified.",
        "The record stands judicially-verified.",
        "The record stands formally-verified.",
        "The record stands publicly-verified.",
        "The record stands doubly-verified.",
        "The record stands hepta-checked.",
        "The record stands decu-checked.",
        "The record stands centuple-checked.",
        "The record stands milluple-checked.",
        "The record stands manifold-checked.",
        "The record stands countlessly-checked.",
        "The record stands externally-checked.",
        "The record stands forensically-checked.",
        "The record stands judicially-checked.",
        "The record stands formally-checked.",
        "The record stands publicly-checked.",
        "The record stands doubly-checked.",
        "Every record stands crowd-checked before use.",
        "Every record stands crowd-verified before use.",
        "Every record stands public-checked before use.",
        "Every record stands public-verified before use.",
        "Every record stands court-checked before use.",
        "Every record stands court-verified before use.",
        "Every record stands judge-checked before use.",
        "Every record stands judge-verified before use.",
        "Every record stands state-checked before use.",
        "Every record stands state-verified before use.",
        "Every record stands agency-checked before use.",
        "Every record stands agency-verified before use.",
        "Every record stands bureau-checked before use.",
        "Every record stands bureau-verified before use.",
        "Every record stands guild-checked before use.",
        "Every record stands guild-verified before use.",
        "Every record stands union-checked before use.",
        "Every record stands union-verified before use.",
        "Every record stands crew-checked before use.",
        "Every record stands crew-verified before use.",
        "Every record stands staff-checked before use.",
        "Every record stands staff-verified before use.",
        "Every record stands market-checked before use.",
        "Every record stands market-verified before use.",
        "Every record stands industry-checked before use.",
        "Every record stands industry-verified before use.",
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
            "The record stands mini-verified.",
            "The record stands peer-verified.",
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


class SealClaimScanLexiconFixR13Tests(unittest.TestCase):
    """Ruling 432: lexicon limb."""

    FORMS = (
        "Records stand untainted after writing.",
        "Records stand undefiled after writing.",
        "Records stand unpolluted after writing.",
        "Records stand uncontaminated after writing.",
        "Records stand unspotted after writing.",
        "Records stand unsmirched after writing.",
        "Records stand unbesmirched after writing.",
        "Records stand sinless after writing.",
        "Records stand guiltless after writing.",
        "Records stand blameless after writing.",
        "Records stand irreproachable after writing.",
        "The store is unconquerable.",
        "The store is unvanquishable.",
        "The store is unbeatable.",
        "The store is uncorruptible.",
        "The store is unbendable.",
        "The store is unshatterable.",
        "Records stand immortal after writing.",
        "The records are untainted by outside writers.",
        "The records are undefiled by outside writers.",
        "The records are uncorruptible by outside writers.",
        "Heads stand machine-etched for every actor.",
        "Heads stand hand-engraved for every actor.",
        "Heads stand laser-engraved for every actor.",
        "Heads stand deep-etched for every actor.",
        "Heads stand blind-stamped for every actor.",
        "Heads stand hot-stamped for every actor.",
        "Heads stand cold-stamped for every actor.",
        "Heads stand machine-stamped for every actor.",
        "Heads stand officially-stamped for every actor.",
        "The store is unimpregnable.",
        "The store is immovable.",
        "The store is irrefutable.",
        "The store is incontestable.",
        "The store is incontrovertible.",
        "The store is indisputable.",
        "The store is unrefuted.",
        "The store is uncontested.",
        "The store is unopposed.",
        "The store is unmatched.",
        "The store is unbeaten.",
        "The store is stainless.",
        "The records are unmatched by outside writers.",
        "The records are inimitable by outside writers.",
        "The records are transcendent by outside writers.",
        "The records are immortal by outside writers.",
        "The records are unfading by outside writers.",
        "The records are unbeatable by outside writers.",
        "The records are unconquerable by outside writers.",
        "The records are perennial by outside writers.",
        "The records are shock-proof by outside writers.",
        "The records are quake-proof by outside writers.",
        "The records are scratch-proof by outside writers.",
        "The records are stain-proof by outside writers.",
        "The records are dent-proof by outside writers.",
        "The records are tear-proof by outside writers.",
        "The records are puncture-proof by outside writers.",
        "The records are heat-proof by outside writers.",
        "The records are acid-proof by outside writers.",
        "The records are smoke-proof by outside writers.",
        "The records are flame-proof by outside writers.",
        "The records are rot-proof by outside writers.",
        "The records are pet-proof by outside writers.",
    )

    def test_lexicon_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(mod, "The store is impermeable."))
        self.assertFalse(_scan(mod, "The store is inviolate."))
        self.assertFalse(_scan(mod, "Records stand spotless after writing."))
        self.assertFalse(_scan(mod, "Records stand unstained after writing."))
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanAssertedFixR13Tests(unittest.TestCase):
    """Ruling 433: asserted form limb."""

    FORMS = (
        "The journal exudes integrity for every reader.",
        "The journal emanates integrity for every reader.",
        "The journal radiates integrity for every reader.",
        "The journal communicates integrity for every reader.",
        "The journal transmits integrity for every reader.",
        "The journal breathes integrity for every reader.",
        "The journal characterises integrity for every reader.",
        "The journal characterizes integrity for every reader.",
        "The journal defines integrity for every reader.",
        "The journal captures integrity for every reader.",
        "The journal amounts to integrity for every reader.",
        "The journal equals integrity for every reader.",
        "The journal betokens integrity for every reader.",
        "The journal portends integrity for every reader.",
        "The journal foreshadows integrity for every reader.",
        "The journal oozes integrity for every reader.",
        "The mechanism perpetuates total integrity of the journal.",
        "The mechanism prolongs total integrity of the journal.",
        "The mechanism extends total integrity of the journal.",
        "The mechanism lengthens total integrity of the journal.",
        "The journal retains integrity for every reader.",
        "The journal owns integrity for every reader.",
        "The journal comprises integrity for every reader.",
        "The journal includes integrity for every reader.",
        "The journal underwrites integrity for every reader.",
        "The mechanism corroborates total integrity of the journal.",
        "The mechanism underscores total integrity of the journal.",
        "The mechanism highlights total integrity of the journal.",
        "The mechanism emphasizes total integrity of the journal.",
        "The mechanism accentuates total integrity of the journal.",
        "The mechanism reaffirms total integrity of the journal.",
        "The mechanism reiterates total integrity of the journal.",
        "The mechanism restates total integrity of the journal.",
        "The mechanism underlines total integrity of the journal.",
        "The mechanism evinces total integrity of the journal.",
        "The mechanism betokens total integrity of the journal.",
        "The mechanism avows total integrity of the journal.",
        "The mechanism professes total integrity of the journal.",
        "The mechanism pronounces total integrity of the journal.",
        "The mechanism announces total integrity of the journal.",
        "The mechanism heralds total integrity of the journal.",
        "The mechanism trumpets total integrity of the journal.",
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
            mod, "The journal bears integrity for every reader."))
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
