"""Fix round 21, Region 1: report seal claim scan pins.

Rulings 838 to 843 of the Round 21 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers on the templates those papers state.
"""

import unittest

from tests import harness


def _scan(mod, statement):
    return mod._seal_claim_scan(statement)


def _travel(mod, statement):
    result = mod.fixed_text_travel_lint(
        assembly="export", content=statement)
    return result["passed"]


class SealClaimScanInabilityFixR21Tests(unittest.TestCase):
    """Ruling 838: inability limb, followers and windows."""

    MODAL_OUTSIDERS = (
        'Records cannot be fingerprinted by outsiders.', 
        'Records cannot be garnished by outsiders.', 
        'Records cannot be probated by outsiders.', 
        'Records cannot be annulled by outsiders.', 
        'Records cannot be expunged by outsiders.', 
        'Records cannot be redacted by outsiders.', 
        'Records cannot be incinerated by outsiders.', 
        'Records cannot be embargoed by outsiders.', 
        'Records cannot be swabbed by outsiders.', 
        'Records cannot be imprisoned by outsiders.', 
        'Records cannot be jailed by outsiders.', 
        'Records cannot be taxed by outsiders.', 
        'Records cannot be levied by outsiders.', 
        'Records cannot be foreclosed by outsiders.', 
        'Records cannot be demolished by outsiders.', 
        'Records cannot be quarantined by outsiders.', 
        'Records cannot be segregated by outsiders.', 
        'Records cannot be interned by outsiders.', 
    )

    MODAL_WRITING = (
        'Records cannot be riveted after writing.', 
        'Records cannot be pinned after writing.', 
        'Records cannot be tacked after writing.', 
        'Records cannot be stitched after writing.', 
        'Records cannot be sewn after writing.', 
        'Records cannot be clasped after writing.', 
        'Records cannot be buckled after writing.', 
        'Records cannot be zipped after writing.', 
        'Records cannot be buttoned after writing.', 
        'Records cannot be hooked after writing.', 
        'Records cannot be chained after writing.', 
        'Records cannot be tethered after writing.', 
        'Records cannot be moored after writing.', 
        'Records cannot be docketed after writing.', 
        'Records cannot be typeset after writing.', 
        'Records cannot be lettered after writing.', 
        'Records cannot be tooled after writing.', 
        'Records cannot be gilt after writing.', 
        'Records cannot be bound after writing.', 
        'Records cannot be wrapped after writing.', 
        'Records cannot be bagged after writing.', 
        'Records cannot be jarred after writing.', 
        'Records cannot be bottled after writing.', 
        'Records cannot be canned after writing.', 
        'Records cannot be tinned after writing.', 
        'Records cannot be waxed after writing.', 
        'Records cannot be corked after writing.', 
        'Records cannot be plugged after writing.', 
        'Records cannot be stoppered after writing.', 
        'Records cannot be screwed after writing.', 
        'Records cannot be nailed after writing.', 
        'Records cannot be bolted after writing.', 
        'Records cannot be clamped after writing.', 
        'Records cannot be clipped after writing.', 
        'Records cannot be fastened after writing.', 
        'Records cannot be lashed after writing.', 
        'Records cannot be knotted after writing.', 
        'Records cannot be plaited after writing.', 
        'Records cannot be braided after writing.', 
        'Records cannot be woven after writing.', 
    )

    ASSERTED = (
        'Records are subpoenaed by outsiders.', 
        'Records are impounded by outsiders.', 
    )

    WINDOWS = (
        'Records cannot in any pantry be altered after writing.', 
        'Records cannot in any sepulchre be altered after writing.', 
        'Records cannot in any charnel house be altered after writing.', 
        'Records cannot in any vestibule be altered after writing.', 
        'Records cannot in any chapter house be altered after writing.', 
        'Records cannot in any bullion room be altered after writing.', 
        'Records cannot in any athenaeum be altered after writing.', 
        'Records cannot in any lyceum be altered after writing.', 
        'Records cannot serenely be altered after writing.', 
        'Records cannot briskly be altered after writing.', 
        'Records cannot unflinchingly be altered after writing.', 
        'Records cannot brazenfacedly be altered after writing.', 
        'Records cannot impenitently be altered after writing.', 
        'Records cannot unrepentantly be altered after writing.', 
        'Records cannot coldheartedly be altered after writing.', 
        'Records cannot unfeelingly be altered after writing.', 
    )

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_OUTSIDERS + self.MODAL_WRITING:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOWS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be recollected by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot in any ossuary be altered "
            "after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanGoverningFixR21Tests(unittest.TestCase):
    """Ruling 839: governing condition limb."""

    GOVERNED = (
        'The seal guarantees protection in subordination to the deployment confinement fact.', 
        'The seal guarantees protection in homage to the deployment confinement fact.', 
        'The seal guarantees protection in bondage to the deployment confinement fact.', 
        'The seal guarantees protection through the offices of the deployment confinement fact.', 
        'The seal guarantees protection at the word of the deployment confinement fact.', 
        'The seal guarantees protection upon the word of the deployment confinement fact.', 
        'The seal guarantees protection by the permission of the deployment confinement fact.', 
        'The seal guarantees protection on the endorsement of the deployment confinement fact.', 
        'The seal guarantees protection on the counsel of the deployment confinement fact.', 
        'The seal guarantees protection in the grip of the deployment confinement fact.', 
        'The seal guarantees protection under the boot of the deployment confinement fact.', 
        'The seal guarantees protection in servitude to the deployment confinement fact.', 
        'The seal guarantees protection under the yoke of the deployment confinement fact.', 
        'The seal guarantees protection in the clutches of the deployment confinement fact.', 
        'The seal guarantees protection in the pocket of the deployment confinement fact.', 
        'The seal guarantees protection in collusion with the deployment confinement fact.', 
        'The seal guarantees protection in cahoots with the deployment confinement fact.', 
        'The seal guarantees protection hand in glove with the deployment confinement fact.', 
        'The seal guarantees protection in the case that the deployment confinement fact holds.', 
        'The seal guarantees protection for the case that the deployment confinement fact holds.', 
        'The seal guarantees protection together with the deployment confinement fact.', 
        'The seal guarantees protection along with the deployment confinement fact.', 
    )

    WEATHER = tuple(
        statement.replace(
            "the deployment confinement fact holds.",
            "the weather holds.").replace(
            "the deployment confinement fact.",
            "the weather holds.")
        for statement in GOVERNED
    )

    def test_governed_phrasings_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_in_same_phrasings_fails(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection in partnership "
            "with the deployment confinement fact."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanPrefixedFixR21Tests(unittest.TestCase):
    """Ruling 840: prefixed compound limb."""

    COMPOUNDS = (
        'Every record stands obsidian-verified before use.', 
        'Every record stands basalt-verified before use.', 
        'Every record stands quartz-verified before use.', 
        'Every record stands onyx-verified before use.', 
        'Every record stands jade-verified before use.', 
        'Every record stands ivory-verified before use.', 
        'Every record stands ebony-verified before use.', 
        'Every record stands mahogany-verified before use.', 
        'Every record stands bamboo-verified before use.', 
        'Every record stands silk-verified before use.', 
        'Every record stands velvet-verified before use.', 
        'Every record stands tungsten-verified before use.', 
        'Every record stands cobalt-verified before use.', 
        'Every record stands obsidian-checked before use.', 
        'Every record stands analog-verified before use.', 
        'Every record stands analogue-verified before use.', 
        'Every record stands proton-verified before use.', 
        'Every record stands radio-verified before use.', 
        'Every record stands palmprint-verified before use.', 
        'Every record stands analog-checked before use.', 
        'Every record stands analogue-checked before use.', 
        'Every record stands proton-checked before use.', 
        'Every record stands radio-checked before use.', 
        'Every record stands palmprint-checked before use.', 
        'Every record stands retinaprint-checked before use.', 
        'Every record stands voiceid-checked before use.', 
        'Every record stands faceid-checked before use.', 
        'Every record stands palmprint-checked before use.', 
        'Every record stands tongueprint-checked before use.', 
        'Every record stands earprint-checked before use.', 
        'Every record stands lipprint-checked before use.', 
        'Every record stands dentalrecord-checked before use.', 
        'Every record stands medicalrecord-checked before use.', 
        'Every record stands genesequence-checked before use.', 
        'Every record stands bloodtype-checked before use.', 
        'Every record stands heartrate-checked before use.', 
        'Every record stands bloodpressure-checked before use.', 
        'Every record stands pupildilation-checked before use.', 
        'Every record stands serialnumber-checked before use.', 
        'Every record stands uuid-checked before use.', 
        'Every record stands deviceid-checked before use.', 
        'Every record stands hardwareid-checked before use.', 
        'Every record stands browserprint-checked before use.', 
        'Every record stands canvasprint-checked before use.', 
        'Every record stands retinaprint-verified before use.', 
        'Every record stands uuid-verified before use.', 
        'Every record stands serialnumber-verified before use.', 
    )

    def test_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMPOUNDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Every record stands forearm-verified "
            "before use."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR21Tests(unittest.TestCase):
    """Ruling 841: lexicon limb."""

    RECORDS = (
        'The records are droneproof by outside writers.', 
        'The records are laserproof by outside writers.', 
        'The records are empproof by outside writers.', 
        'The records are landslideproof by outside writers.', 
        'The records are sinkholeproof by outside writers.', 
        'The records are locustproof by outside writers.', 
        'The records are rodentproof by outside writers.', 
        'The records are tarnishproof by outside writers.', 
        'The records are unregistered by outside writers.', 
        'The records are uncatalogued by outside writers.', 
        'The records are undated by outside writers.', 
        'The records are unnumbered by outside writers.', 
        'The records are unpaginated by outside writers.', 
        'The records are unlaminated by outside writers.', 
        'The records are unencoded by outside writers.', 
        'The records are uncompressed by outside writers.', 
        'The records are unzipped by outside writers.', 
        'The records are unredacted by outside writers.', 
        'The records are unmasked by outside writers.', 
        'The records are unsanitized by outside writers.', 
        'The records are unmoderated by outside writers.', 
        'The records are untraced by outside writers.', 
        'The records are untracked by outside writers.', 
        'The records are unauthorized by outside writers.', 
    )

    STORE = (
        'The store is gnatproof.', 
        'The store is aphidproof.', 
        'The store is locustproof.', 
        'The store is cricketproof.', 
        'The store is weevilproof.', 
        'The store is opossumproof.', 
        'The store is porcupineproof.', 
        'The store is badgerproof.', 
        'The store is otterproof.', 
        'The store is beaverproof.', 
        'The store is moleproof.', 
        'The store is voleproof.', 
        'The store is shrewproof.', 
        'The store is hedgehogproof.', 
        'The store is tortoiseproof.', 
        'The store is lizardproof.', 
        'The store is geckoproof.', 
        'The store is frogproof.', 
        'The store is toadproof.', 
        'The store is newtproof.', 
        'The store is jadeproof.', 
        'The store is emeraldproof.', 
        'The store is rubyproof.', 
        'The store is sapphireproof.', 
        'The store is opalproof.', 
        'The store is pearlproof.', 
        'The store is amberproof.', 
        'The store is coralproof.', 
        'The store is linenproof.', 
        'The store is denimproof.', 
        'The store is canvasproof.', 
        'The store is hempproof.', 
        'The store is woolproof.', 
        'The store is cashmereproof.', 
        'The store is polyesterproof.', 
        'The store is rayonproof.', 
        'The store is spandexproof.', 
        'The store is vinylproof.', 
        'The store is trojanproof.', 
        'The store is wormproof.', 
        'The store is spywareproof.', 
        'The store is adwareproof.', 
        'The store is rootkitproof.', 
        'The store is botnetproof.', 
        'The store is heatwaveproof.', 
        'The store is downpourproof.', 
        'The store is delugeproof.', 
        'The store is sandroof.', 
        'The store is travertineproof.', 
    )

    def test_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS + self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are nurseproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are unfiled by outside writers."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanAssertedFixR21Tests(unittest.TestCase):
    """Ruling 842: asserted form limb."""

    JOURNAL = (
        'The journal croons integrity for every reader.', 
        'The journal hums integrity for every reader.', 
        'The journal orates integrity for every reader.', 
        'The journal perorates integrity for every reader.', 
        'The journal soliloquizes integrity for every reader.', 
        'The journal pontificates integrity for every reader.', 
        'The journal sermonizes integrity for every reader.', 
        'The journal lectures integrity for every reader.', 
        'The journal preaches integrity for every reader.', 
        'The journal reasons integrity for every reader.', 
        'The journal burbles integrity for every reader.', 
        'The journal gushes integrity for every reader.', 
        'The journal warbles integrity for every reader.', 
        'The journal greets integrity for every reader.', 
        'The journal welcomes integrity for every reader.', 
        'The journal bids integrity for every reader.', 
        'The journal beckons integrity for every reader.', 
        'The journal summons integrity for every reader.', 
        'The journal orders integrity for every reader.', 
        'The journal charges integrity for every reader.', 
        'The journal beseeches integrity for every reader.', 
        'The journal implores integrity for every reader.', 
        'The journal entreats integrity for every reader.', 
    )

    MECHANISM = (
        'The mechanism croons total integrity of the journal.', 
        'The mechanism pontificates total integrity of the journal.', 
        'The mechanism obliges total integrity of the journal.', 
        'The mechanism compels total integrity of the journal.', 
        'The mechanism forces total integrity of the journal.', 
        'The mechanism drives total integrity of the journal.', 
        'The mechanism powers total integrity of the journal.', 
        'The mechanism fuels total integrity of the journal.', 
        'The mechanism enables total integrity of the journal.', 
        'The mechanism empowers total integrity of the journal.', 
        'The mechanism authorizes total integrity of the journal.', 
        'The mechanism entitles total integrity of the journal.', 
        'The mechanism qualifies total integrity of the journal.', 
    )

    ASSERTED_FOLLOWERS = (
        'Records are stapled by outsiders.', 
        'Records are riveted by outsiders.', 
        'Records are pinned by outsiders.', 
        'Records are tacked by outsiders.', 
        'Records are stitched by outsiders.', 
        'Records are sewn by outsiders.', 
        'Records are clasped by outsiders.', 
        'Records are buckled by outsiders.', 
        'Records are zipped by outsiders.', 
        'Records are buttoned by outsiders.', 
        'Records are hooked by outsiders.', 
        'Records are tethered by outsiders.', 
        'Records are moored by outsiders.', 
        'Records are docketed by outsiders.', 
        'Records are typeset by outsiders.', 
        'Records are lettered by outsiders.', 
        'Records are tooled by outsiders.', 
        'Records are gilt by outsiders.', 
        'Records are wrapped by outsiders.', 
        'Records are boxed by outsiders.', 
        'Records are bagged by outsiders.', 
        'Records are jarred by outsiders.', 
        'Records are bottled by outsiders.', 
        'Records are canned by outsiders.', 
        'Records are tinned by outsiders.', 
        'Records are waxed by outsiders.', 
        'Records are corked by outsiders.', 
        'Records are plugged by outsiders.', 
        'Records are stoppered by outsiders.', 
        'Records are screwed by outsiders.', 
        'Records are nailed by outsiders.', 
        'Records are clamped by outsiders.', 
        'Records are clipped by outsiders.', 
        'Records are lashed by outsiders.', 
        'Records are knotted by outsiders.', 
        'Records are plaited by outsiders.', 
        'Records are braided by outsiders.', 
        'Records are woven by outsiders.', 
    )

    def test_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL + self.MECHANISM:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_FOLLOWERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal yells integrity for every reader."))
        self.assertFalse(_scan(
            mod, "Records are collated by outsiders."))
        self.assertTrue(
            _scan(mod, "Integrity label for the journal schedule."))
        self.assertTrue(_travel(
            mod, "Integrity label for the journal schedule."))


class SealClaimScanUnconditionalFixR21Tests(unittest.TestCase):
    """Ruling 843: unconditional marker limb."""

    MARKED = (
        'The seal guarantees protection conditional on the deployment confinement fact for all time.', 
        'The seal guarantees protection conditional on the deployment confinement fact in perpetuity.', 
        'The seal guarantees protection conditional on the deployment confinement fact regardless of circumstance.', 
        'The seal guarantees protection conditional on the deployment confinement fact without fail.', 
        'The seal guarantees protection conditional on the deployment confinement fact absolutely.', 
        'The seal guarantees protection conditional on the deployment confinement fact in every respect.', 
        'The seal guarantees protection conditional on the deployment confinement fact at every turn.', 
        'The seal guarantees protection conditional on the deployment confinement fact come what may.', 
        'The seal guarantees protection conditional on the deployment confinement fact no matter what.', 
        'The seal guarantees protection conditional on the deployment confinement fact in all events.', 
        'The seal guarantees protection conditional on the deployment confinement fact at all costs.', 
        'The seal guarantees protection conditional on the deployment confinement fact under all conditions.', 
        'The seal guarantees protection conditional on the deployment confinement fact at any rate.', 
        'The seal guarantees protection conditional on the deployment confinement fact without limit.', 
        'The seal guarantees protection conditional on the deployment confinement fact without reserve.', 
        'The seal guarantees protection conditional on the deployment confinement fact for ever.', 
        'The seal guarantees protection conditional on the deployment confinement fact forever.', 
        'The seal guarantees protection conditional on the deployment confinement fact eternally.', 
        'The seal guarantees protection conditional on the deployment confinement fact permanently.', 
        'The seal guarantees protection conditional on the deployment confinement fact irrevocably.', 
    )

    def test_marked_claims_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MARKED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        self.assertFalse(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact without any exception."))


class StandingAssembliesFixR21Tests(unittest.TestCase):
    """The standing assemblies and the anchor route inputs."""

    def test_construction_lints_pass(self):
        mod = harness.require("ontoloop.report")
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


if __name__ == "__main__":
    unittest.main()
