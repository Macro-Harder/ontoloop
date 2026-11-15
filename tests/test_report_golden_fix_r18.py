"""Fix round 18, Region 1: report and golden pins.

Rulings 657 to 661 of the Round 18 triage. Each class pins
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


class SealClaimScanInabilityFixR18Tests(unittest.TestCase):
    """Ruling 657: inability limb, followers and windows."""

    MODAL = (
        'Records cannot be beheld by outsiders.',
        'Records cannot be sighted by outsiders.',
        'Records cannot be studied by outsiders.',
        'Records cannot be scrutinised by outsiders.',
        'Records cannot be retained by outsiders.',
        'Records cannot be absorbed by outsiders.',
        'Records cannot be mastered by outsiders.',
        'Records cannot be interpreted by outsiders.',
        'Records cannot be explained by outsiders.',
        'Records cannot be confirmed by outsiders.',
        'Records cannot be buried by outsiders.',
        'Records cannot be ratified by outsiders.',
        'Records cannot be accredited by outsiders.',
        'Records cannot be notarized by outsiders.',
        'Records cannot be notarised by outsiders.',
        'Records cannot be felt by outsiders.',
        'Records cannot be tasted by outsiders.',
        'Records cannot be smelt by outsiders.',
        'Records cannot be parsed by outsiders.',
        'Records cannot be construed by outsiders.',
        'Records cannot be assessed by outsiders.',
        'Records cannot be evaluated by outsiders.',
        'Records cannot be judged by outsiders.',
        'Records cannot be discovered by outsiders.',
        'Records cannot be uncovered by outsiders.',
        'Records cannot be unveiled by outsiders.',
        'Records cannot be exhibited by outsiders.',
        'Records cannot be demonstrated by outsiders.',
        'Records cannot be illustrated by outsiders.',
        'Records cannot be depicted by outsiders.',
        'Records cannot be portrayed by outsiders.',
        'Records cannot be represented by outsiders.',
        'Records cannot be clarified by outsiders.',
        'Records cannot be unravelled by outsiders.',
        'Records cannot be unraveled by outsiders.',
        'Records cannot be solved by outsiders.',
        'Records cannot be resolved by outsiders.',
        'Records cannot be settled by outsiders.',
        'Records cannot be decided by outsiders.',
        'Records cannot be determined by outsiders.',
        'Records cannot be concluded by outsiders.',
        'Records cannot be derived by outsiders.',
        'Records cannot be computed by outsiders.',
        'Records cannot be calculated by outsiders.',
        'Records cannot be reckoned by outsiders.',
        'Records cannot be estimated by outsiders.',
        'Records cannot be gauged by outsiders.',
        'Records cannot be transported by outsiders.',
        'Records cannot be handed by outsiders.',
        'Records cannot be passed by outsiders.',
        'Records cannot be routed by outsiders.',
        'Records cannot be redirected by outsiders.',
    )

    ASSERTED = (
        'Records are beheld by outsiders.',
        'Records are glimpsed by outsiders.',
        'Records are studied by outsiders.',
        'Records are perused by outsiders.',
        'Records are felt by outsiders.',
        'Records are tasted by outsiders.',
        'Records are smelt by outsiders.',
        'Records are interpreted by outsiders.',
        'Records are parsed by outsiders.',
        'Records are construed by outsiders.',
        'Records are skimmed by outsiders.',
        'Records are browsed by outsiders.',
        'Records are handled by outsiders.',
    )

    WINDOWS = (
        'Records cannot in any windmill be altered after writing.',
        'Records cannot in any waterfall be altered after writing.',
        'Records cannot in any canyon be altered after writing.',
        'Records cannot in any university be altered after writing.',
        'Records cannot in any conservatory be altered after writing.',
        'Records cannot in any winery be altered after writing.',
        'Records cannot in any tannery be altered after writing.',
        'Records cannot in any granary be altered after writing.',
        'Records cannot in any apiary be altered after writing.',
        'Records cannot in any aviary be altered after writing.',
        'Records cannot in any gallery be altered after writing.',
        'Records cannot in any seaport be altered after writing.',
        'Records cannot in any plaza be altered after writing.',
        'Records cannot in any cavern be altered after writing.',
        'Records cannot in any grotto be altered after writing.',
        'Records cannot in any crypt be altered after writing.',
        'Records cannot in any tomb be altered after writing.',
        'Records cannot in any gazebo be altered after writing.',
        'Records cannot in any terrace be altered after writing.',
        'Records cannot in any balcony be altered after writing.',
        'Records cannot in any courtyard be altered after writing.',
        'Records cannot in any cloister be altered after writing.',
        'Records cannot in any refectory be altered after writing.',
        'Records cannot in any sacristy be altered after writing.',
        'Records cannot in any vestry be altered after writing.',
        'Records cannot in any narthex be altered after writing.',
        'Records cannot in any chancel be altered after writing.',
        'Records cannot in any nave be altered after writing.',
        'Records cannot in any transept be altered after writing.',
        'Records cannot in any presbytery be altered after writing.',
        'Records cannot in any rectory be altered after writing.',
        'Records cannot in any vicarage be altered after writing.',
        'Records cannot in any manse be altered after writing.',
        'Records cannot in any mission be altered after writing.',
        'Records cannot in any hermitage be altered after writing.',
        'Records cannot in any retreat be altered after writing.',
        'Records cannot in any sanatorium be altered after writing.',
        'Records cannot in any hospice be altered after writing.',
        'Records cannot in any infirmary be altered after writing.',
        'Records cannot in any dispensary be altered after writing.',
        'Records cannot in any workhouse be altered after writing.',
        'Records cannot in any poorhouse be altered after writing.',
        'Records cannot in any almshouse be altered after writing.',
        'Records cannot in any belfry be altered after writing.',
        'Records cannot in any minaret be altered after writing.',
        'Records cannot in any dome be altered after writing.',
        'Records cannot in any rotunda be altered after writing.',
        'Records cannot in any atrium be altered after writing.',
        'Records cannot in any arcade be altered after writing.',
        'Records cannot in any colonnade be altered after writing.',
        'Records cannot in any portico be altered after writing.',
        'Records cannot in any peristyle be altered after writing.',
        'Records cannot in any emporium be altered after writing.',
        'Records cannot in any oratory be altered after writing.',
        'Records cannot in any crematorium be altered after writing.',
        'Records cannot in any mortuary be altered after writing.',
        'Records cannot in any consulate be altered after writing.',
        'Records cannot in any chancery be altered after writing.',
        'Records cannot in any nunnery be altered after writing.',
        'Records cannot in any priory be altered after writing.',
        'Records cannot in any outpost be altered after writing.',
        'Records cannot in any garrison be altered after writing.',
        'Records cannot in any fort be altered after writing.',
        'Records cannot in any blockhouse be altered after writing.',
        'Records cannot in any catacomb be altered after writing.',
        'Records cannot in any mausoleum be altered after writing.',
        'Records cannot in any colosseum be altered after writing.',
        'Records cannot in any amphitheater be altered after writing.',
        'Records cannot at any spring be altered after writing.',
        'Records cannot at any summer be altered after writing.',
        'Records cannot at any autumn be altered after writing.',
        'Records cannot at any winter be altered after writing.',
        'Records cannot at any twilight be altered after writing.',
        'Records cannot at any sunrise be altered after writing.',
        'Records cannot at any sunset be altered after writing.',
        'Records cannot at any midday be altered after writing.',
        'Records cannot at any size be altered after writing.',
        'Records cannot at any level be altered after writing.',
        'Records cannot at any amount be altered after writing.',
        'Records cannot at any quantity be altered after writing.',
        'Records cannot at any strength be altered after writing.',
        'Records cannot at any power be altered after writing.',
        'Records cannot at any latitude be altered after writing.',
        'Records cannot at any longitude be altered after writing.',
        'Records cannot at any breadth be altered after writing.',
        'Records cannot at any thickness be altered after writing.',
        'Records cannot at any mass be altered after writing.',
        'Records cannot at any intensity be altered after writing.',
        'Records cannot at any magnitude be altered after writing.',
        'Records cannot at any amplitude be altered after writing.',
        'Records cannot at any wavelength be altered after writing.',
        'Records cannot at any resistance be altered after writing.',
        'Records cannot at any capacitance be altered after writing.',
        'Records cannot at any inductance be altered after writing.',
        'Records cannot at any conductance be altered after writing.',
        'Records cannot at any viscosity be altered after writing.',
        'Records cannot at any elasticity be altered after writing.',
        'Records cannot at any porosity be altered after writing.',
        'Records cannot at any salinity be altered after writing.',
        'Records cannot at any acidity be altered after writing.',
        'Records cannot at any alkalinity be altered after writing.',
        'Records cannot at any turbidity be altered after writing.',
        'Records cannot at any luminosity be altered after writing.',
        'Records cannot at any brightness be altered after writing.',
        'Records cannot at any loudness be altered after writing.',
        'Records cannot at any pitch be altered after writing.',
        'Records cannot at any tempo be altered after writing.',
        'Records cannot at any rhythm be altered after writing.',
        'Records cannot at any acceleration be altered after writing.',
        'Records cannot at any momentum be altered after writing.',
        'Records cannot at any torque be altered after writing.',
        'Records cannot at any tension be altered after writing.',
        'Records cannot at any shear be altered after writing.',
        'Records cannot at any friction be altered after writing.',
        'Records cannot at any gravity be altered after writing.',
        'Records cannot on any afternoon be altered after writing.',
        'Records cannot on any weekday be altered after writing.',
        'Records cannot on any holiday be altered after writing.',
        'Records cannot in any sense be altered after writing.',
        'Records cannot in any regard be altered after writing.',
    )

    WINDOW_WORDS = (
        'Records cannot loudly be altered after writing.',
        'Records cannot carefully be altered after writing.',
        'Records cannot carelessly be altered after writing.',
        'Records cannot recklessly be altered after writing.',
        'Records cannot intentionally be altered after writing.',
        'Records cannot improperly be altered after writing.',
        'Records cannot wrongly be altered after writing.',
        'Records cannot unfairly be altered after writing.',
        'Records cannot anonymously be altered after writing.',
        'Records cannot swiftly be altered after writing.',
        'Records cannot gradually be altered after writing.',
        'Records cannot roughly be altered after writing.',
        'Records cannot forcefully be altered after writing.',
        'Records cannot abruptly be altered after writing.',
        'Records cannot eventually be altered after writing.',
        'Records cannot repeatedly be altered after writing.',
        'Records cannot wilfully be altered after writing.',
        'Records cannot willfully be altered after writing.',
        'Records cannot unwittingly be altered after writing.',
        'Records cannot stealthily be altered after writing.',
        'Records cannot unobtrusively be altered after writing.',
        'Records cannot inconspicuously be altered after writing.',
        'Records cannot slyly be altered after writing.',
        'Records cannot cunningly be altered after writing.',
        'Records cannot craftily be altered after writing.',
        'Records cannot shrewdly be altered after writing.',
        'Records cannot astutely be altered after writing.',
        'Records cannot wilily be altered after writing.',
        'Records cannot artfully be altered after writing.',
        'Records cannot deviously be altered after writing.',
        'Records cannot underhandedly be altered after writing.',
        'Records cannot treacherously be altered after writing.',
        'Records cannot perfidiously be altered after writing.',
        'Records cannot faithlessly be altered after writing.',
        'Records cannot dishonorably be altered after writing.',
        'Records cannot ignobly be altered after writing.',
        'Records cannot basely be altered after writing.',
        'Records cannot vilely be altered after writing.',
        'Records cannot wickedly be altered after writing.',
        'Records cannot sinfully be altered after writing.',
        'Records cannot falsely be altered after writing.',
        'Records cannot untruthfully be altered after writing.',
        'Records cannot mendaciously be altered after writing.',
    )

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOWS + self.WINDOW_WORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be known by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanGoverningFixR18Tests(unittest.TestCase):
    """Ruling 658: governing condition limb."""

    PHRASES = (
        'The seal guarantees protection with authority of the deployment confinement fact.',
        'The seal guarantees protection by the order of the deployment confinement fact.',
        'The seal guarantees protection at the order of the deployment confinement fact.',
        'The seal guarantees protection upon the basis of the deployment confinement fact.',
        'The seal guarantees protection by force of the deployment confinement fact.',
        'The seal guarantees protection in satisfaction of the deployment confinement fact.',
        'The seal guarantees protection in performance of the deployment confinement fact.',
        'The seal guarantees protection for reasons of the deployment confinement fact.',
        'The seal guarantees protection on the ground of the deployment confinement fact.',
        'The seal guarantees protection under the provision of the deployment confinement fact.',
        'The seal guarantees protection as commanded by the deployment confinement fact.',
        'The seal guarantees protection with the sanction of the deployment confinement fact.',
        'The seal guarantees protection by sanction of the deployment confinement fact.',
        'The seal guarantees protection with approval of the deployment confinement fact.',
        'The seal guarantees protection by approval of the deployment confinement fact.',
        'The seal guarantees protection under the auspices of the deployment confinement fact.',
        'The seal guarantees protection at the direction given by the deployment confinement fact.',
        'The seal guarantees protection by the direction of the deployment confinement fact.',
        'The seal guarantees protection on the direction of the deployment confinement fact.',
        'The seal guarantees protection under the permission of the deployment confinement fact.',
        'The seal guarantees protection on the permission of the deployment confinement fact.',
        'The seal guarantees protection at the permission of the deployment confinement fact.',
        'The seal guarantees protection by leave of the deployment confinement fact.',
        'The seal guarantees protection with leave of the deployment confinement fact.',
        'The seal guarantees protection under licence from the deployment confinement fact.',
        'The seal guarantees protection under license from the deployment confinement fact.',
        'The seal guarantees protection by licence of the deployment confinement fact.',
        'The seal guarantees protection within the provisions of the deployment confinement fact.',
        'The seal guarantees protection under provision of the deployment confinement fact.',
        'The seal guarantees protection in pursuit of the deployment confinement fact.',
        'The seal guarantees protection in face of the deployment confinement fact.',
        'The seal guarantees protection consequent on the deployment confinement fact.',
        'The seal guarantees protection consequent upon the deployment confinement fact.',
        'The seal guarantees protection arising out of the deployment confinement fact.',
        'The seal guarantees protection originating in the deployment confinement fact.',
        'The seal guarantees protection rooted in the deployment confinement fact.',
    )

    WEATHER = (
        'The seal guarantees protection with authority of the weather holds.',
        'The seal guarantees protection by the order of the weather holds.',
        'The seal guarantees protection at the order of the weather holds.',
        'The seal guarantees protection upon the basis of the weather holds.',
        'The seal guarantees protection by force of the weather holds.',
        'The seal guarantees protection in satisfaction of the weather holds.',
        'The seal guarantees protection in performance of the weather holds.',
        'The seal guarantees protection for reasons of the weather holds.',
        'The seal guarantees protection on the ground of the weather holds.',
        'The seal guarantees protection under the provision of the weather holds.',
        'The seal guarantees protection as commanded by the weather holds.',
        'The seal guarantees protection with the sanction of the weather holds.',
        'The seal guarantees protection by sanction of the weather holds.',
        'The seal guarantees protection with approval of the weather holds.',
        'The seal guarantees protection by approval of the weather holds.',
        'The seal guarantees protection under the auspices of the weather holds.',
        'The seal guarantees protection at the direction given by the weather holds.',
        'The seal guarantees protection by the direction of the weather holds.',
        'The seal guarantees protection on the direction of the weather holds.',
        'The seal guarantees protection under the permission of the weather holds.',
        'The seal guarantees protection on the permission of the weather holds.',
        'The seal guarantees protection at the permission of the weather holds.',
        'The seal guarantees protection by leave of the weather holds.',
        'The seal guarantees protection with leave of the weather holds.',
        'The seal guarantees protection under licence from the weather holds.',
        'The seal guarantees protection under license from the weather holds.',
        'The seal guarantees protection by licence of the weather holds.',
        'The seal guarantees protection within the provisions of the weather holds.',
        'The seal guarantees protection under provision of the weather holds.',
        'The seal guarantees protection in pursuit of the weather holds.',
        'The seal guarantees protection in face of the weather holds.',
        'The seal guarantees protection consequent on the weather holds.',
        'The seal guarantees protection consequent upon the weather holds.',
        'The seal guarantees protection arising out of the weather holds.',
        'The seal guarantees protection originating in the weather holds.',
        'The seal guarantees protection rooted in the weather holds.',
    )

    THAT_PHRASES = (
        'The seal guarantees protection on the understanding that the deployment confinement fact holds.',
        'The seal guarantees protection on the assumption that the deployment confinement fact holds.',
        'The seal guarantees protection in the event that the deployment confinement fact holds.',
        'The seal guarantees protection on the premise that the deployment confinement fact holds.',
        'The seal guarantees protection with the understanding that the deployment confinement fact holds.',
        'The seal guarantees protection providing that the deployment confinement fact holds.',
        'The seal guarantees protection for as long as the deployment confinement fact holds.',
        'The seal guarantees protection so long as the deployment confinement fact holds.',
    )

    THAT_WEATHER = (
        'The seal guarantees protection on the understanding that the weather holds.',
        'The seal guarantees protection on the assumption that the weather holds.',
        'The seal guarantees protection in the event that the weather holds.',
        'The seal guarantees protection on the premise that the weather holds.',
        'The seal guarantees protection with the understanding that the weather holds.',
        'The seal guarantees protection providing that the weather holds.',
        'The seal guarantees protection for as long as the weather holds.',
        'The seal guarantees protection so long as the weather holds.',
    )

    def test_governed_phrasings_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PHRASES + self.THAT_PHRASES:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_in_same_phrasings_fails(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER + self.THAT_WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection with the "
            "authority of the deployment confinement fact."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanPrefixedFixR18Tests(unittest.TestCase):
    """Ruling 659: prefixed compound limb."""

    VERIFIED = (
        'Every record stands acoustic-verified before use.',
        'Every record stands agi-verified before use.',
        'Every record stands atomic-verified before use.',
        'Every record stands barcode-verified before use.',
        'Every record stands bone-verified before use.',
        'Every record stands bot-verified before use.',
        'Every record stands brain-verified before use.',
        'Every record stands breath-verified before use.',
        'Every record stands browser-verified before use.',
        'Every record stands cell-verified before use.',
        'Every record stands central-verified before use.',
        'Every record stands chip-verified before use.',
        'Every record stands cookie-verified before use.',
        'Every record stands cosmic-verified before use.',
        'Every record stands dental-verified before use.',
        'Every record stands ear-verified before use.',
        'Every record stands facial-verified before use.',
        'Every record stands financial-verified before use.',
        'Every record stands gait-verified before use.',
        'Every record stands gene-verified before use.',
        'Every record stands genetic-verified before use.',
        'Every record stands genome-verified before use.',
        'Every record stands gpt-verified before use.',
        'Every record stands hair-verified before use.',
        'Every record stands handwriting-verified before use.',
        'Every record stands heart-verified before use.',
        'Every record stands infrared-verified before use.',
        'Every record stands keystroke-verified before use.',
        'Every record stands laser-verified before use.',
        'Every record stands lunar-verified before use.',
        'Every record stands magnetic-verified before use.',
        'Every record stands mental-verified before use.',
        'Every record stands nail-verified before use.',
        'Every record stands net-verified before use.',
        'Every record stands nose-verified before use.',
        'Every record stands optical-verified before use.',
        'Every record stands oral-verified before use.',
        'Every record stands passkey-verified before use.',
        'Every record stands passphrase-verified before use.',
        'Every record stands physical-verified before use.',
        'Every record stands pin-verified before use.',
        'Every record stands pulse-verified before use.',
        'Every record stands qr-verified before use.',
        'Every record stands radar-verified before use.',
        'Every record stands saliva-verified before use.',
        'Every record stands seismic-verified before use.',
        'Every record stands session-verified before use.',
        'Every record stands skin-verified before use.',
        'Every record stands social-verified before use.',
        'Every record stands solar-verified before use.',
        'Every record stands sonar-verified before use.',
        'Every record stands stellar-verified before use.',
        'Every record stands sweat-verified before use.',
        'Every record stands tear-verified before use.',
        'Every record stands thermal-verified before use.',
        'Every record stands thumb-verified before use.',
        'Every record stands tongue-verified before use.',
        'Every record stands tooth-verified before use.',
        'Every record stands urine-verified before use.',
        'Every record stands vein-verified before use.',
        'Every record stands verbal-verified before use.',
        'Every record stands visual-verified before use.',
        'Every record stands written-verified before use.',
    )

    CHECKED = (
        'Every record stands agi-checked before use.',
        'Every record stands atomic-checked before use.',
        'Every record stands barcode-checked before use.',
        'Every record stands bone-checked before use.',
        'Every record stands bot-checked before use.',
        'Every record stands brain-checked before use.',
        'Every record stands breath-checked before use.',
        'Every record stands cell-checked before use.',
        'Every record stands chip-checked before use.',
        'Every record stands cosmic-checked before use.',
        'Every record stands ear-checked before use.',
        'Every record stands facial-checked before use.',
        'Every record stands gait-checked before use.',
        'Every record stands gene-checked before use.',
        'Every record stands gpt-checked before use.',
        'Every record stands hair-checked before use.',
        'Every record stands heart-checked before use.',
        'Every record stands lunar-checked before use.',
        'Every record stands nail-checked before use.',
        'Every record stands net-checked before use.',
        'Every record stands nose-checked before use.',
        'Every record stands passkey-checked before use.',
        'Every record stands pulse-checked before use.',
        'Every record stands qr-checked before use.',
        'Every record stands saliva-checked before use.',
        'Every record stands skin-checked before use.',
        'Every record stands solar-checked before use.',
        'Every record stands stellar-checked before use.',
        'Every record stands sweat-checked before use.',
        'Every record stands tear-checked before use.',
        'Every record stands thermal-checked before use.',
        'Every record stands thumb-checked before use.',
        'Every record stands tongue-checked before use.',
        'Every record stands tooth-checked before use.',
        'Every record stands urine-checked before use.',
        'Every record stands vein-checked before use.',
        'Every record stands visual-checked before use.',
    )

    def test_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERIFIED + self.CHECKED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Every record stands data-checked before use."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR18Tests(unittest.TestCase):
    """Ruling 660: lexicon limb."""

    PROOF = (
        'The records are virusproof by outside writers.',
        'The records are mouldproof by outside writers.',
        'The records are moldproof by outside writers.',
        'The records are insectproof by outside writers.',
        'The records are ratproof by outside writers.',
        'The records are mouseproof by outside writers.',
        'The records are dogproof by outside writers.',
        'The records are catproof by outside writers.',
        'The records are babyproof by outside writers.',
        'The records are studentproof by outside writers.',
        'The records are teacherproof by outside writers.',
        'The records are futureproof by outside writers.',
        'The records are recessionproof by outside writers.',
        'The records are inflationproof by outside writers.',
        'The records are crisisproof by outside writers.',
        'The records are tsunamiproof by outside writers.',
        'The records are blizzardproof by outside writers.',
        'The records are hailproof by outside writers.',
        'The records are avalancheproof by outside writers.',
        'The records are sandproof by outside writers.',
        'The records are mudproof by outside writers.',
        'The records are iceproof by outside writers.',
        'The records are sleetproof by outside writers.',
        'The records are greaseproof by outside writers.',
        'The records are oilproof by outside writers.',
        'The records are solventproof by outside writers.',
        'The records are diamondproof by outside writers.',
        'The records are titaniumproof by outside writers.',
        'The records are steelproof by outside writers.',
        'The records are ironproof by outside writers.',
        'The records are stoneproof by outside writers.',
        'The records are rockproof by outside writers.',
        'The records are glassproof by outside writers.',
        'The records are plasticproof by outside writers.',
        'The records are woodproof by outside writers.',
        'The records are leatherproof by outside writers.',
        'The records are rubberproof by outside writers.',
        'The records are ceramicproof by outside writers.',
        'The records are kevlarproof by outside writers.',
        'The records are carbonproof by outside writers.',
        'The records are leadproof by outside writers.',
        'The records are copperproof by outside writers.',
        'The records are bronzeproof by outside writers.',
        'The records are silverproof by outside writers.',
        'The records are goldproof by outside writers.',
        'The records are platinumproof by outside writers.',
        'The records are chromeproof by outside writers.',
        'The records are nickelproof by outside writers.',
        'The records are zincproof by outside writers.',
        'The records are tinproof by outside writers.',
        'The records are brassproof by outside writers.',
    )

    UNWORDS = (
        'The records are unviolated by outside writers.',
        'The records are unseen by outside writers.',
        'The records are unknown by outside writers.',
        'The records are undefaced by outside writers.',
        'The records are unvandalised by outside writers.',
        'The records are unvandalized by outside writers.',
        'The records are untampered by outside writers.',
        'The records are unfalsified by outside writers.',
        'The records are uncounterfeited by outside writers.',
        'The records are ungarbled by outside writers.',
        'The records are unscrambled by outside writers.',
        'The records are unencrypted by outside writers.',
        'The records are undecayed by outside writers.',
        'The records are undecomposed by outside writers.',
        'The records are unrotted by outside writers.',
    )

    def test_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROOF + self.UNWORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)
        self.assertFalse(_scan(mod, "The store is unstoppable."))
        self.assertFalse(_scan(mod, "The store is tsunamiproof."))

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are fireproof by outside writers."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanAssertedFixR18Tests(unittest.TestCase):
    """Ruling 661: asserted form limb."""

    JOURNAL = (
        'The journal sings integrity for every reader.',
        'The journal hymns integrity for every reader.',
        'The journal glorifies integrity for every reader.',
        'The journal magnifies integrity for every reader.',
        'The journal reveres integrity for every reader.',
        'The journal worships integrity for every reader.',
        'The journal idolises integrity for every reader.',
        'The journal idolizes integrity for every reader.',
        'The journal deifies integrity for every reader.',
        'The journal lionises integrity for every reader.',
        'The journal lionizes integrity for every reader.',
        'The journal eulogises integrity for every reader.',
        'The journal eulogizes integrity for every reader.',
        'The journal rhapsodises integrity for every reader.',
        'The journal blazons integrity for every reader.',
        'The journal emblazons integrity for every reader.',
        'The journal promulgates integrity for every reader.',
        'The journal disseminates integrity for every reader.',
        'The journal circulates integrity for every reader.',
        'The journal peddles integrity for every reader.',
        'The journal markets integrity for every reader.',
        'The journal advertises integrity for every reader.',
        'The journal publicises integrity for every reader.',
        'The journal publicizes integrity for every reader.',
        'The journal spotlights integrity for every reader.',
        'The journal emphasises integrity for every reader.',
        'The journal stresses integrity for every reader.',
        'The journal authenticates integrity for every reader.',
        'The journal ratifies integrity for every reader.',
        'The journal accredits integrity for every reader.',
        'The journal notarizes integrity for every reader.',
        'The journal notarises integrity for every reader.',
        'The journal countersigns integrity for every reader.',
        'The journal illuminates integrity for every reader.',
        'The journal clarifies integrity for every reader.',
        'The journal elucidates integrity for every reader.',
        'The journal explains integrity for every reader.',
        'The journal describes integrity for every reader.',
    )

    MECHANISM = (
        'The mechanism sings total integrity of the journal.',
        'The mechanism glorifies total integrity of the journal.',
        'The mechanism reveres total integrity of the journal.',
        'The mechanism worships total integrity of the journal.',
        'The mechanism deifies total integrity of the journal.',
        'The mechanism lionizes total integrity of the journal.',
        'The mechanism eulogizes total integrity of the journal.',
        'The mechanism promulgates total integrity of the journal.',
        'The mechanism disseminates total integrity of the journal.',
        'The mechanism peddles total integrity of the journal.',
        'The mechanism advertises total integrity of the journal.',
        'The mechanism publicizes total integrity of the journal.',
        'The mechanism spotlights total integrity of the journal.',
        'The mechanism emphasises total integrity of the journal.',
        'The mechanism stresses total integrity of the journal.',
        'The mechanism avers total integrity of the journal.',
        'The mechanism submits total integrity of the journal.',
        'The mechanism posits total integrity of the journal.',
        'The mechanism postulates total integrity of the journal.',
        'The mechanism chronicles total integrity of the journal.',
        'The mechanism narrates total integrity of the journal.',
        'The mechanism recounts total integrity of the journal.',
        'The mechanism relates total integrity of the journal.',
        'The mechanism describes total integrity of the journal.',
        'The mechanism explains total integrity of the journal.',
        'The mechanism expounds total integrity of the journal.',
        'The mechanism elucidates total integrity of the journal.',
    )

    def test_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL + self.MECHANISM:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)
        self.assertFalse(_scan(
            mod, "The mechanism goes into total integrity "
            "of the journal."))
        self.assertFalse(_scan(
            mod, "The mechanism deals in total integrity "
            "of the journal."))

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal advocates integrity for every reader."))
        self.assertTrue(
            _scan(mod, "Integrity label for the journal schedule."))


if __name__ == "__main__":
    unittest.main()
