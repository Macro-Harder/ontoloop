"""Fix round 20, Region 1: report seal claim scan pins.

Rulings 773 to 778 of the Round 20 triage. Each class pins
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



class SealClaimScanInabilityFixR20Tests(unittest.TestCase):
    """Ruling 773: inability limb, followers and windows."""

    MODAL_OUTSIDERS = (
        "Records cannot be arraigned by outsiders.", 
        "Records cannot be extradited by outsiders.", 
        "Records cannot be deposed by outsiders.", 
        "Records cannot be sequestered by outsiders.", 
        "Records cannot be impeached by outsiders.", 
        "Records cannot be concocted by outsiders.", 
        "Records cannot be simulated by outsiders.", 
        "Records cannot be pirated by outsiders.", 
        "Records cannot be repossessed by outsiders.", 
        "Records cannot be commandeered by outsiders.", 
        "Records cannot be litigated by outsiders.", 
        "Records cannot be adjudicated by outsiders.", 
        "Records cannot be acquitted by outsiders.", 
        "Records cannot be convicted by outsiders.", 
        "Records cannot be pardoned by outsiders.", 
        "Records cannot be gazed by outsiders.", 
        "Records cannot be peered by outsiders.", 
        "Records cannot be glanced by outsiders.", 
        "Records cannot be stared by outsiders.", 
        "Records cannot be copyrighted by outsiders.", 
        "Records cannot be trademarked by outsiders.", 
        "Records cannot be patented by outsiders.", 
        "Records cannot be misappropriated by outsiders.", 
        "Records cannot be appropriated by outsiders.", 
        "Records cannot be adjudicated by outsiders.", 
        "Records cannot be litigated by outsiders.", 
        "Records cannot be arraigned by outsiders.", 
        "Records cannot be extradited by outsiders.", 
        "Records cannot be deported by outsiders.", 
        "Records cannot be exiled by outsiders.", 
        "Records cannot be ostracized by outsiders.", 
        "Records cannot be ostracised by outsiders.", 
        "Records cannot be boycotted by outsiders.", 
        "Records cannot be blackballed by outsiders.", 
        "Records cannot be debarred by outsiders.", 
        "Records cannot be disbarred by outsiders.", 
        "Records cannot be defrocked by outsiders.", 
        "Records cannot be unfrocked by outsiders.", 
        "Records cannot be excommunicated by outsiders.", 
        "Records cannot be anathematized by outsiders.", 
        "Records cannot be anathematised by outsiders.", 
        "Records cannot be censured by outsiders.", 
        "Records cannot be reprimanded by outsiders.", 
        "Records cannot be rebuked by outsiders.", 
        "Records cannot be reproached by outsiders.", 
        "Records cannot be admonished by outsiders.", 
        "Records cannot be chastised by outsiders.", 
        "Records cannot be castigated by outsiders.", 
        "Records cannot be berated by outsiders.", 
        "Records cannot be scolded by outsiders.", 
        "Records cannot be upbraided by outsiders.", 
        "Records cannot be reviled by outsiders.", 
        "Records cannot be vilified by outsiders.", 
        "Records cannot be traduced by outsiders.", 
        "Records cannot be defamed by outsiders.", 
        "Records cannot be libeled by outsiders.", 
        "Records cannot be libelled by outsiders.", 
        "Records cannot be slandered by outsiders.", 
        "Records cannot be calumniated by outsiders.", 
        "Records cannot be impugned by outsiders.", 
        "Records cannot be disparaged by outsiders.", 
        "Records cannot be denigrated by outsiders.", 
        "Records cannot be belittled by outsiders.", 
        "Records cannot be deprecated by outsiders.", 
        "Records cannot be decried by outsiders.", 
        "Records cannot be derided by outsiders.", 
        "Records cannot be mocked by outsiders.", 
        "Records cannot be ridiculed by outsiders.", 
        "Records cannot be lampooned by outsiders.", 
        "Records cannot be satirized by outsiders.", 
        "Records cannot be satirised by outsiders.", 
        "Records cannot be parodied by outsiders.", 
        "Records cannot be burlesqued by outsiders.", 
        "Records cannot be caricatured by outsiders.", 
        "Records cannot be imitated by outsiders.", 
        "Records cannot be mimicked by outsiders.", 
        "Records cannot be aped by outsiders.", 
        "Records cannot be echoed by outsiders.", 
        "Records cannot be emulated by outsiders.", 
    )
    MODAL_WRITING = (
        "Records cannot be collated after writing.", 
        "Records cannot be alphabetized after writing.", 
        "Records cannot be alphabetised after writing.", 
        "Records cannot be categorized after writing.", 
        "Records cannot be categorised after writing.", 
        "Records cannot be microfiched after writing.", 
        "Records cannot be embossed after writing.", 
        "Records cannot be imprinted after writing.", 
        "Records cannot be branded after writing.", 
        "Records cannot be hallmarked after writing.", 
        "Records cannot be watermarked after writing.", 
        "Records cannot be padlocked after writing.", 
        "Records cannot be latched after writing.", 
        "Records cannot be glued after writing.", 
        "Records cannot be pasted after writing.", 
        "Records cannot be varnished after writing.", 
        "Records cannot be lacquered after writing.", 
        "Records cannot be gilded after writing.", 
        "Records cannot be framed after writing.", 
        "Records cannot be shelved after writing.", 
        "Records cannot be enveloped after writing.", 
        "Records cannot be crated after writing.", 
    )
    ASSERTED = (
        "Records are blueprinted by outsiders.", 
        "Records are devised by outsiders.", 
        "Records are pictured by outsiders.", 
        "Records are outlined by outsiders.", 
        "Records are envisioned by outsiders.", 
        "Records are transformed by outsiders.", 
        "Records are reworded by outsiders.", 
        "Records are confiscated by outsiders.", 
        "Records are collated by outsiders.", 
        "Records are alphabetized by outsiders.", 
        "Records are alphabetised by outsiders.", 
        "Records are categorized by outsiders.", 
        "Records are categorised by outsiders.", 
        "Records are microfiched by outsiders.", 
        "Records are padlocked by outsiders.", 
        "Records are latched by outsiders.", 
        "Records are glued by outsiders.", 
        "Records are pasted by outsiders.", 
        "Records are varnished by outsiders.", 
        "Records are lacquered by outsiders.", 
        "Records are gilded by outsiders.", 
        "Records are framed by outsiders.", 
        "Records are shelved by outsiders.", 
        "Records are enveloped by outsiders.", 
        "Records are crated by outsiders.", 
    )
    WINDOWS = (
        "Records cannot calmly be altered after writing.", 
        "Records cannot eagerly be altered after writing.", 
        "Records cannot fiercely be altered after writing.", 
        "Records cannot tenderly be altered after writing.", 
        "Records cannot timidly be altered after writing.", 
        "Records cannot anxiously be altered after writing.", 
        "Records cannot ostensibly be altered after writing.", 
        "Records cannot purportedly be altered after writing.", 
        "Records cannot allegedly be altered after writing.", 
        "Records cannot supposedly be altered after writing.", 
        "Records cannot apparently be altered after writing.", 
        "Records cannot presumably be altered after writing.", 
        "Records cannot evidently be altered after writing.", 
        "Records cannot happily be altered after writing.", 
        "Records cannot angrily be altered after writing.", 
        "Records cannot nervously be altered after writing.", 
        "Records cannot in any courtroom be altered after writing.", 
        "Records cannot in any classroom be altered after writing.", 
        "Records cannot in any boardroom be altered after writing.", 
        "Records cannot in any newsroom be altered after writing.", 
        "Records cannot in any ballroom be altered after writing.", 
        "Records cannot in any storeroom be altered after writing.", 
        "Records cannot in any washroom be altered after writing.", 
        "Records cannot in any ossuary be altered after writing.", 
        "Records cannot in any baptistery be altered after writing.", 
        "Records cannot in any reliquary be altered after writing.", 
        "Records cannot at any eclipse be altered after writing.", 
        "Records cannot on any eclipse be altered after writing.", 
        "Records cannot candidly be altered after writing.", 
        "Records cannot forthrightly be altered after writing.", 
        "Records cannot unabashedly be altered after writing.", 
        "Records cannot unapologetically be altered after writing.", 
        "Records cannot unreservedly be altered after writing.", 
        "Records cannot wholeheartedly be altered after writing.", 
        "Records cannot defiantly be altered after writing.", 
        "Records cannot rebelliously be altered after writing.", 
        "Records cannot insolently be altered after writing.", 
        "Records cannot contemptuously be altered after writing.", 
        "Records cannot scornfully be altered after writing.", 
        "Records cannot disdainfully be altered after writing.", 
        "Records cannot gleefully be altered after writing.", 
        "Records cannot cheerfully be altered after writing.", 
        "Records cannot enthusiastically be altered after writing.", 
        "Records cannot in any strongroom be altered.", 
        "Records cannot in any keep be altered.", 
        "Records cannot in any donjon be altered.", 
        "Records cannot in any acropolis be altered.", 
        "Records cannot in any panopticon be altered.", 
        "Records cannot in any belvedere be altered.", 
        "Records cannot in any pergola be altered.", 
        "Records cannot in any parsonage be altered.", 
        "Records cannot in any deanery be altered.", 
        "Records cannot in any coliseum be altered.", 
        "Records cannot in any hothouse be altered.", 
        "Records cannot in any orangery be altered.", 
        "Records cannot in any dolphinarium be altered.", 
        "Records cannot in any oceanarium be altered.", 
        "Records cannot in any serpentarium be altered.", 
        "Records cannot in any insectarium be altered.", 
        "Records cannot in any herbarium be altered.", 
        "Records cannot in any arboretum be altered.", 
        "Records cannot in any pinery be altered.", 
        "Records cannot in any vinery be altered.", 
        "Records cannot in any gristmill be altered.", 
        "Records cannot in any papermill be altered.", 
        "Records cannot in any steelworks be altered.", 
        "Records cannot in any ironworks be altered.", 
        "Records cannot in any mint be altered.", 
        "Records cannot in any dockyard be altered.", 
        "Records cannot in any boatyard be altered.", 
        "Records cannot in any lumberyard be altered.", 
        "Records cannot in any stockyard be altered.", 
        "Records cannot in any barnyard be altered.", 
        "Records cannot in any farmyard be altered.", 
        "Records cannot in any graveyard be altered.", 
        "Records cannot in any junkyard be altered.", 
        "Records cannot in any salvageyard be altered.", 
        "Records cannot in any switchyard be altered.", 
        "Records cannot in any railyard be altered.", 
        "Records cannot at any expansivity be altered.", 
        "Records cannot at any emissivity be altered.", 
        "Records cannot at any absorptivity be altered.", 
        "Records cannot at any diffusivity be altered.", 
        "Records cannot at any luminance be altered.", 
        "Records cannot at any chromaticity be altered.", 
        "Records cannot at any refractivity be altered.", 
        "Records cannot at any susceptibility be altered.", 
        "Records cannot at any magnetization be altered.", 
        "Records cannot at any hygroscopicity be altered.", 
        "Records cannot at any plasticity be altered.", 
        "Records cannot at any permeance be altered.", 
        "Records cannot at any reluctivity be altered.", 
        "Records cannot at any specificity be altered.", 
        "Records cannot at any selectivity be altered.", 
        "Records cannot at any sensitivity be altered.", 
        "Records cannot at any linearity be altered.", 
        "Records cannot at any hysteresis be altered.", 
        "Records cannot at any coercivity be altered.", 
        "Records cannot at any remanence be altered.", 
        "Records cannot at any saturation be altered.", 
        "Records cannot audaciously be altered.", 
        "Records cannot impudently be altered.", 
        "Records cannot unashamedly be altered.", 
        "Records cannot defiantly be altered.", 
        "Records cannot ostentatiously be altered.", 
        "Records cannot unabashedly be altered.", 
        "Records cannot unapologetically be altered.", 
        "Records cannot heedlessly be altered.", 
        "Records cannot rashly be altered.", 
        "Records cannot foolhardily be altered.", 
        "Records cannot courageously be altered.", 
        "Records cannot fearlessly be altered.", 
        "Records cannot dauntlessly be altered.", 
        "Records cannot intrepidly be altered.", 
        "Records cannot heroically be altered.", 
        "Records cannot valiantly be altered.", 
        "Records cannot gallantly be altered.", 
        "Records cannot nobly be altered.", 
        "Records cannot honorably be altered.", 
        "Records cannot mercilessly be altered.", 
        "Records cannot pitilessly be altered.", 
        "Records cannot remorselessly be altered.", 
        "Records cannot callously be altered.", 
        "Records cannot coldly be altered.", 
        "Records cannot brutally be altered.", 
        "Records cannot savagely be altered.", 
        "Records cannot ferociously be altered.", 
        "Records cannot viciously be altered.", 
        "Records cannot vengefully be altered.", 
        "Records cannot rancorously be altered.", 
        "Records cannot malevolently be altered.", 
        "Records cannot malignantly be altered.", 
        "Records cannot sinisterly be altered.", 
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
            mod, "Records cannot in any sea be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot gently be altered after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))



class SealClaimScanGoverningFixR20Tests(unittest.TestCase):
    """Ruling 774: governing condition limb."""

    GOVERNED = (
        "The seal guarantees protection in partnership with the deployment confinement fact.", 
        "The seal guarantees protection in collaboration with the deployment confinement fact.", 
        "The seal guarantees protection in association with the deployment confinement fact.", 
        "The seal guarantees protection in alliance with the deployment confinement fact.", 
        "The seal guarantees protection in cooperation with the deployment confinement fact.", 
        "The seal guarantees protection in coordination with the deployment confinement fact.", 
        "The seal guarantees protection in union with the deployment confinement fact.", 
        "The seal guarantees protection in combination with the deployment confinement fact.", 
        "The seal guarantees protection on the guidance given by the deployment confinement fact.", 
        "The seal guarantees protection under the guidance given by the deployment confinement fact.", 
        "The seal guarantees protection by the guidance given by the deployment confinement fact.", 
        "The seal guarantees protection at the behest given by the deployment confinement fact.", 
        "The seal guarantees protection by the behest given by the deployment confinement fact.", 
        "The seal guarantees protection under the permission given by the deployment confinement fact.", 
        "The seal guarantees protection by the permission given by the deployment confinement fact.", 
        "The seal guarantees protection on the permission given by the deployment confinement fact.", 
        "The seal guarantees protection with the authority given by the deployment confinement fact.", 
        "The seal guarantees protection under the consent given by the deployment confinement fact.", 
        "The seal guarantees protection by the consent given by the deployment confinement fact.", 
        "The seal guarantees protection under the command given by the deployment confinement fact.", 
        "The seal guarantees protection on the command given by the deployment confinement fact.", 
        "The seal guarantees protection at the command given by the deployment confinement fact.", 
        "The seal guarantees protection by the request given by the deployment confinement fact.", 
        "The seal guarantees protection on the request given by the deployment confinement fact.", 
        "The seal guarantees protection at the request given by the deployment confinement fact.", 
        "The seal guarantees protection on the sanction given by the deployment confinement fact.", 
        "The seal guarantees protection by the sanction given by the deployment confinement fact.", 
        "The seal guarantees protection under the sanction given by the deployment confinement fact.", 
        "The seal guarantees protection on the approval given by the deployment confinement fact.", 
        "The seal guarantees protection by the approval given by the deployment confinement fact.", 
        "The seal guarantees protection under the approval given by the deployment confinement fact.", 
        "The seal guarantees protection on the endorsement given by the deployment confinement fact.", 
        "The seal guarantees protection by the endorsement given by the deployment confinement fact.", 
        "The seal guarantees protection on the blessing given by the deployment confinement fact.", 
        "The seal guarantees protection by the blessing given by the deployment confinement fact.", 
        "The seal guarantees protection on the urging given by the deployment confinement fact.", 
        "The seal guarantees protection by the urging given by the deployment confinement fact.", 
        "The seal guarantees protection by virtue of the terms of the deployment confinement fact.", 
        "The seal guarantees protection under the sanction of the deployment confinement fact.", 
        "The seal guarantees protection at the sanction of the deployment confinement fact.", 
        "The seal guarantees protection on the sanction of the deployment confinement fact.", 
        "The seal guarantees protection under the approval of the deployment confinement fact.", 
        "The seal guarantees protection at the approval of the deployment confinement fact.", 
        "The seal guarantees protection on the approval of the deployment confinement fact.", 
        "The seal guarantees protection under the consent of the deployment confinement fact.", 
        "The seal guarantees protection at the consent of the deployment confinement fact.", 
        "The seal guarantees protection on the consent of the deployment confinement fact.", 
        "The seal guarantees protection under the request of the deployment confinement fact.", 
        "The seal guarantees protection on the recommendation of the deployment confinement fact.", 
        "The seal guarantees protection at the suggestion of the deployment confinement fact.", 
        "The seal guarantees protection on the proposal of the deployment confinement fact.", 
        "The seal guarantees protection at the invitation of the deployment confinement fact.", 
        "The seal guarantees protection in consultation with the deployment confinement fact.", 
        "The seal guarantees protection in collaboration with the deployment confinement fact.", 
        "The seal guarantees protection in partnership with the deployment confinement fact.", 
        "The seal guarantees protection in association with the deployment confinement fact.", 
        "The seal guarantees protection in alliance with the deployment confinement fact.", 
        "The seal guarantees protection in coordination with the deployment confinement fact.", 
        "The seal guarantees protection in cooperation with the deployment confinement fact.", 
        "The seal guarantees protection in harmony with the deployment confinement fact.", 
        "The seal guarantees protection in unison with the deployment confinement fact.", 
        "The seal guarantees protection in sync with the deployment confinement fact.", 
        "The seal guarantees protection under the sponsorship of the deployment confinement fact.", 
        "The seal guarantees protection under the tutelage of the deployment confinement fact.", 
        "The seal guarantees protection at the pleasure of the deployment confinement fact.", 
        "The seal guarantees protection by the will of the deployment confinement fact.", 
        "The seal guarantees protection on the motion of the deployment confinement fact.", 
        "The seal guarantees protection on the word of the deployment confinement fact.", 
        "The seal guarantees protection on the testimony of the deployment confinement fact.", 
        "The seal guarantees protection on the evidence of the deployment confinement fact.", 
        "The seal guarantees protection on the assurance of the deployment confinement fact.", 
        "The seal guarantees protection at the say of the deployment confinement fact.", 
        "The seal guarantees protection on the word of the deployment confinement fact.", 
        "The seal guarantees protection by the word of the deployment confinement fact.", 
        "The seal guarantees protection under the thumb of the deployment confinement fact.", 
        "The seal guarantees protection at the whim of the deployment confinement fact.", 
        "The seal guarantees protection on the whim of the deployment confinement fact.", 
        "The seal guarantees protection at the pleasure of the deployment confinement fact.", 
        "The seal guarantees protection by the will of the deployment confinement fact.", 
        "The seal guarantees protection under the will of the deployment confinement fact.", 
        "The seal guarantees protection in subservience to the deployment confinement fact.", 
        "The seal guarantees protection by fiat of the deployment confinement fact.", 
        "The seal guarantees protection by edict of the deployment confinement fact.", 
        "The seal guarantees protection under edict of the deployment confinement fact.", 
        "The seal guarantees protection on pain of the deployment confinement fact.", 
        "The seal guarantees protection under penalty of the deployment confinement fact.", 
        "The seal guarantees protection in the gift of the deployment confinement fact.", 
        "The seal guarantees protection within the gift of the deployment confinement fact.", 
        "The seal guarantees protection at the gift of the deployment confinement fact.", 
        "The seal guarantees protection in the power of the deployment confinement fact.", 
        "The seal guarantees protection within the power of the deployment confinement fact.", 
        "The seal guarantees protection under the power of the deployment confinement fact.", 
        "The seal guarantees protection in the shadow of the deployment confinement fact.", 
        "The seal guarantees protection under the shadow of the deployment confinement fact.", 
        "The seal guarantees protection in the wake of the deployment confinement fact.", 
        "The seal guarantees protection on the heels of the deployment confinement fact.", 
        "The seal guarantees protection in the aftermath of the deployment confinement fact.", 
        "The seal guarantees protection at the feet of the deployment confinement fact.", 
        "The seal guarantees protection in the pay of the deployment confinement fact.", 
        "The seal guarantees protection under the heel of the deployment confinement fact.", 
        "The seal guarantees protection at the beck of the deployment confinement fact.", 
        "The seal guarantees protection at the call of the deployment confinement fact.", 
        "The seal guarantees protection on the call of the deployment confinement fact.", 
        "The seal guarantees protection by the hand of the deployment confinement fact.", 
        "The seal guarantees protection through the hand of the deployment confinement fact.", 
        "The seal guarantees protection in the sight of the deployment confinement fact.", 
        "The seal guarantees protection under the eye of the deployment confinement fact.", 
        "The seal guarantees protection beneath the eye of the deployment confinement fact.", 
        "The seal guarantees protection under the watch of the deployment confinement fact.", 
        "The seal guarantees protection in the keeping of the deployment confinement fact.", 
        "The seal guarantees protection in the care of the deployment confinement fact.", 
        "The seal guarantees protection under the care of the deployment confinement fact.", 
        "The seal guarantees protection in the charge of the deployment confinement fact.", 
        "The seal guarantees protection under the charge of the deployment confinement fact.", 
        "The seal guarantees protection in the custody of the deployment confinement fact.", 
        "The seal guarantees protection under the custody of the deployment confinement fact.", 
        "The seal guarantees protection in the possession of the deployment confinement fact.", 
        "The seal guarantees protection by the leave of the deployment confinement fact.", 
        "The seal guarantees protection with the leave of the deployment confinement fact.", 
        "The seal guarantees protection at the leave of the deployment confinement fact.", 
        "The seal guarantees protection at the say so of the deployment confinement fact.", 
        "The seal guarantees protection on the basis that the deployment confinement fact holds.", 
        "The seal guarantees protection on the ground that the deployment confinement fact holds.", 
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
            mod, "The seal guarantees protection through the "
            "agency of the deployment confinement fact."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))



class SealClaimScanPrefixedFixR20Tests(unittest.TestCase):
    """Ruling 775: prefixed compound limb."""

    COMPOUNDS = (
        "Every record stands forearm-verified before use.", 
        "Every record stands forearm-checked before use.", 
        "Every record stands thumbprint-verified before use.", 
        "Every record stands thumbprint-checked before use.", 
        "Every record stands eyebrow-verified before use.", 
        "Every record stands eyebrow-checked before use.", 
        "Every record stands eyelash-verified before use.", 
        "Every record stands eyelash-checked before use.", 
        "Every record stands fingernail-verified before use.", 
        "Every record stands fingernail-checked before use.", 
        "Every record stands toenail-verified before use.", 
        "Every record stands toenail-checked before use.", 
        "Every record stands titanium-verified before use.", 
        "Every record stands titanium-checked before use.", 
        "Every record stands aluminium-verified before use.", 
        "Every record stands aluminium-checked before use.", 
        "Every record stands aluminum-verified before use.", 
        "Every record stands aluminum-checked before use.", 
        "Every record stands copper-verified before use.", 
        "Every record stands copper-checked before use.", 
        "Every record stands bronze-verified before use.", 
        "Every record stands bronze-checked before use.", 
        "Every record stands silver-verified before use.", 
        "Every record stands silver-checked before use.", 
        "Every record stands platinum-verified before use.", 
        "Every record stands platinum-checked before use.", 
        "Every record stands marble-verified before use.", 
        "Every record stands marble-checked before use.", 
        "Every record stands ceramic-verified before use.", 
        "Every record stands ceramic-checked before use.", 
        "Every record stands plastic-verified before use.", 
        "Every record stands plastic-checked before use.", 
        "Every record stands rubber-verified before use.", 
        "Every record stands rubber-checked before use.", 
        "Every record stands leather-verified before use.", 
        "Every record stands leather-checked before use.", 
        "Every record stands kevlar-verified before use.", 
        "Every record stands kevlar-checked before use.", 
        "Every record stands carbon-verified before use.", 
        "Every record stands carbon-checked before use.", 
        "Every record stands telescope-verified before use.", 
        "Every record stands telescope-checked before use.", 
        "Every record stands microscope-verified before use.", 
        "Every record stands microscope-checked before use.", 
        "Every record stands stethoscope-verified before use.", 
        "Every record stands stethoscope-checked before use.", 
        "Every record stands thermometer-verified before use.", 
        "Every record stands thermometer-checked before use.", 
        "Every record stands passcode-verified before use.", 
        "Every record stands passcode-checked before use.", 
        "Every record stands keyfob-verified before use.", 
        "Every record stands keyfob-checked before use.", 
        "Every record stands qrcode-verified before use.", 
        "Every record stands qrcode-checked before use.", 
        "Every record stands qrcode-verified before use.", 
        "Every record stands qrcode-checked before use.", 
        "Every record stands magstripe-verified before use.", 
        "Every record stands magstripe-checked before use.", 
        "Every record stands wearable-verified before use.", 
        "Every record stands wearable-checked before use.", 
        "Every record stands implant-verified before use.", 
        "Every record stands implant-checked before use.", 
        "Every record stands microchip-verified before use.", 
        "Every record stands microchip-checked before use.", 
        "Every record stands heartbeat-verified before use.", 
        "Every record stands heartbeat-checked before use.", 
        "Every record stands brainwave-verified before use.", 
        "Every record stands brainwave-checked before use.", 
        "Every record stands skeleton-verified before use.", 
        "Every record stands skeleton-checked before use.", 
        "Every record stands otp-verified before use.", 
        "Every record stands otp-checked before use.", 
        "Every record stands totp-verified before use.", 
        "Every record stands totp-checked before use.", 
        "Every record stands passcode-verified before use.", 
        "Every record stands passcode-checked before use.", 
        "Every record stands tap-verified before use.", 
        "Every record stands tap-checked before use.", 
        "Every record stands faceprint-verified before use.", 
        "Every record stands faceprint-checked before use.", 
        "Every record stands fingervein-verified before use.", 
        "Every record stands fingervein-checked before use.", 
        "Every record stands palmvein-verified before use.", 
        "Every record stands palmvein-checked before use.", 
        "Every record stands retinascan-verified before use.", 
        "Every record stands retinascan-checked before use.", 
        "Every record stands irisscan-verified before use.", 
        "Every record stands irisscan-checked before use.", 
        "Every record stands dnasample-verified before use.", 
        "Every record stands dnasample-checked before use.", 
        "Every record stands bloodsample-verified before use.", 
        "Every record stands bloodsample-checked before use.", 
        "Every record stands urinesample-verified before use.", 
        "Every record stands urinesample-checked before use.", 
        "Every record stands hairsample-verified before use.", 
        "Every record stands hairsample-checked before use.", 
        "Every record stands salivasample-verified before use.", 
        "Every record stands salivasample-checked before use.", 
        "Every record stands breathalyser-verified before use.", 
        "Every record stands breathalyser-checked before use.", 
        "Every record stands breathalyzer-verified before use.", 
        "Every record stands breathalyzer-checked before use.", 
        "Every record stands polygraph-verified before use.", 
        "Every record stands polygraph-checked before use.", 
        "Every record stands lie-verified before use.", 
        "Every record stands lie-checked before use.", 
        "Every record stands truth-verified before use.", 
        "Every record stands truth-checked before use.", 
        "Every record stands stress-verified before use.", 
        "Every record stands stress-checked before use.", 
        "Every record stands gaitanalysis-verified before use.", 
        "Every record stands gaitanalysis-checked before use.", 
        "Every record stands mousedynamics-verified before use.", 
        "Every record stands mousedynamics-checked before use.", 
        "Every record stands firmware-verified before use.", 
        "Every record stands firmware-checked before use.", 
        "Every record stands kernel-verified before use.", 
        "Every record stands kernel-checked before use.", 
        "Every record stands bios-verified before use.", 
        "Every record stands bios-checked before use.", 
        "Every record stands uefi-verified before use.", 
        "Every record stands uefi-checked before use.", 
        "Every record stands tpm-verified before use.", 
        "Every record stands tpm-checked before use.", 
        "Every record stands hsm-verified before use.", 
        "Every record stands hsm-checked before use.", 
        "Every record stands yubikey-verified before use.", 
        "Every record stands yubikey-checked before use.", 
        "Every record stands smarttoken-verified before use.", 
        "Every record stands smarttoken-checked before use.", 
        "Every record stands rfidtag-verified before use.", 
        "Every record stands rfidtag-checked before use.", 
        "Every record stands nfccard-verified before use.", 
        "Every record stands nfccard-checked before use.", 
        "Every record stands chipcard-verified before use.", 
        "Every record stands chipcard-checked before use.", 
        "Every record stands simcard-verified before use.", 
        "Every record stands simcard-checked before use.", 
        "Every record stands esim-verified before use.", 
        "Every record stands esim-checked before use.", 
        "Every record stands imei-verified before use.", 
        "Every record stands imei-checked before use.", 
        "Every record stands imsi-verified before use.", 
        "Every record stands imsi-checked before use.", 
        "Every record stands macaddress-verified before use.", 
        "Every record stands macaddress-checked before use.", 
        "Every record stands ipaddress-verified before use.", 
        "Every record stands ipaddress-checked before use.", 
        "Every record stands geolocation-verified before use.", 
        "Every record stands geolocation-checked before use.", 
        "Every record stands gpscoordinate-verified before use.", 
        "Every record stands gpscoordinate-checked before use.", 
        "Every record stands celltower-verified before use.", 
        "Every record stands celltower-checked before use.", 
        "Every record stands wifitriangulation-verified before use.", 
        "Every record stands wifitriangulation-checked before use.", 
        "Every record stands bluetoothbeacon-verified before use.", 
        "Every record stands bluetoothbeacon-checked before use.", 
        "Every record stands uwb-verified before use.", 
        "Every record stands uwb-checked before use.", 
        "Every record stands lidarpoint-verified before use.", 
        "Every record stands lidarpoint-checked before use.", 
        "Every record stands radarreturn-verified before use.", 
        "Every record stands radarreturn-checked before use.", 
        "Every record stands sonarecho-verified before use.", 
        "Every record stands sonarecho-checked before use.", 
        "Every record stands thermalimage-verified before use.", 
        "Every record stands thermalimage-checked before use.", 
        "Every record stands nightvision-verified before use.", 
        "Every record stands nightvision-checked before use.", 
        "Every record stands xrayimage-verified before use.", 
        "Every record stands xrayimage-checked before use.", 
        "Every record stands ctscan-verified before use.", 
        "Every record stands ctscan-checked before use.", 
        "Every record stands petscan-verified before use.", 
        "Every record stands petscan-checked before use.", 
        "Every record stands fmri-verified before use.", 
        "Every record stands fmri-checked before use.", 
        "Every record stands eeg-verified before use.", 
        "Every record stands eeg-checked before use.", 
        "Every record stands ecg-verified before use.", 
        "Every record stands ecg-checked before use.", 
        "Every record stands ekg-verified before use.", 
        "Every record stands ekg-checked before use.", 
        "The record stands hologram-verified.", 
        "The record stands ultrasonic-verified.", 
        "The record stands telescopic-verified.", 
        "The record stands microscopic-verified.", 
        "The record stands endoscopic-verified.", 
        "The record stands spectroscopic-verified.", 
        "The record stands heartbeat-verified.", 
        "The record stands brainwave-verified.", 
        "The record stands eyelash-verified.", 
        "The record stands eyebrow-verified.", 
        "The record stands fingernail-verified.", 
        "The record stands chin-verified.", 
        "The record stands brow-verified.", 
        "The record stands temple-verified.", 
        "The record stands scalp-verified.", 
        "The record stands stencil-verified.", 
        "The record stands bionic-verified.", 
        "The record stands muon-verified.", 
        "The record stands neutrino-verified.", 
        "The record stands isotope-verified.", 
        "The record stands hologram-checked.", 
        "The record stands ultrasonic-checked.", 
        "The record stands heartbeat-checked.", 
        "The record stands brainwave-checked.", 
        "The record stands eyelash-checked.", 
        "The record stands fingernail-checked.", 
        "The record stands chin-checked.", 
        "The record stands stencil-checked.", 
        "The record stands bionic-checked.", 
        "The record stands muon-checked.", 
        "The record stands isotope-checked.", 
    )

    def test_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMPOUNDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Every record stands lidar-verified "
            "before use."))
        self.assertFalse(
            _scan(mod, "Every record stands ankle-checked "
            "before use."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))



class SealClaimScanLexiconFixR20Tests(unittest.TestCase):
    """Ruling 776: lexicon limb."""

    RECORDS = (
        "The records are nurseproof by outside writers.", 
        "The records are farmerproof by outside writers.", 
        "The records are pirateproof by outside writers.", 
        "The records are meteorproof by outside writers.", 
        "The records are asteroidproof by outside writers.", 
        "The records are cometproof by outside writers.", 
        "The records are pollenproof by outside writers.", 
        "The records are bacteriaproof by outside writers.", 
        "The records are fungusproof by outside writers.", 
        "The records are fumeproof by outside writers.", 
        "The records are ashproof by outside writers.", 
        "The records are sootproof by outside writers.", 
        "The records are glareproof by outside writers.", 
        "The records are sunproof by outside writers.", 
        "The records are moonproof by outside writers.", 
        "The records are unscanned by outside writers.", 
        "The records are untranscribed by outside writers.", 
        "The records are untranslated by outside writers.", 
        "The records are uncopied by outside writers.", 
        "The records are unduplicated by outside writers.", 
        "The records are unshared by outside writers.", 
        "The records are unprinted by outside writers.", 
        "The records are unemailed by outside writers.", 
        "The records are unuploaded by outside writers.", 
        "The records are unarchived by outside writers.", 
        "The records are unmirrored by outside writers.", 
        "The records are uncloned by outside writers.", 
        "The records are unforwarded by outside writers.", 
        "The records are unexported by outside writers.", 
        "The records are undisclosed by outside writers.", 
        "The records are unviewed by outside writers.", 
        "The records are unlisted by outside writers.", 
        "The records are unphotocopied by outside writers.", 
        "The records are unxeroxed by outside writers.", 
        "The records are unfaxed by outside writers.", 
        "The records are unstreamed by outside writers.", 
        "The records are unbroadcast by outside writers.", 
        "The records are unpublished by outside writers.", 
        "The records are cockroachproof by outside writers.", 
        "The records are bedbugproof by outside writers.", 
        "The records are fleaproof by outside writers.", 
        "The records are shrinkproof by outside writers.", 
        "The records are erosionproof by outside writers.", 
        "The records are abrasionproof by outside writers.", 
        "The records are ripproof by outside writers.", 
        "The records are burstproof by outside writers.", 
        "The records are unstamped by outside writers.", 
        "The records are unlabeled by outside writers.", 
        "The records are unlabelled by outside writers.", 
        "The records are untagged by outside writers.", 
        "The records are unindexed by outside writers.", 
        "The records are unarchived by outside writers.", 
        "The records are unsynced by outside writers.", 
        "The records are unmirrored by outside writers.", 
        "The records are unreplicated by outside writers.", 
        "The records are unhashed by outside writers.", 
        "The records are unsalted by outside writers.", 
    )
    STORE = (
        "The store is cockroachproof.", "The store is fleaproof.", 
        "The store is tickproof.", "The store is bedbugproof.", 
        "The store is miteproof.", "The store is scorpionproof.", 
        "The store is slugproof.", "The store is snailproof.", 
        "The store is wolfproof.", "The store is foxproof.", 
        "The store is raccoonproof.", "The store is skunkproof.", 
        "The store is batproof.", "The store is crowproof.", 
        "The store is gooseproof.", "The store is butterflyproof.", 
        "The store is tempestproof.", "The store is firestormproof.", 
        "The store is ashproof.", "The store is lavaproof.", 
        "The store is emberproof.", "The store is cinderproof.", 
        "The store is basaltproof.", "The store is slateproof.", 
        "The store is quartzproof.", "The store is sandstoneproof.", 
        "The store is limestoneproof.", "The store is concreteproof.", 
        "The store is brickproof.", "The store is ivoryproof.", 
        "The store is silkproof.", "The store is cottonproof.", 
        "The store is nylonproof.", "The store is velvetproof.", 
        "The store is scamproof.", "The store is spamproof.", 
        "The store is malwareproof.", "The store is ransomwareproof.", 
        "The store is phishingproof.", "The store is cyberproof.", 
        "The store is pathogenproof.", "The store is toxinproof.", 
        "The store is venomproof.", "The store is allergenproof.", 
        "The store is pollenproof.", "The store is bacteriaproof.", 
    )

    def test_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS + self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are adultproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are unvaried by outside writers."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))



class SealClaimScanAssertedFixR20Tests(unittest.TestCase):
    """Ruling 777: asserted form limb."""

    JOURNAL = (
        "The journal yells integrity for every reader.", 
        "The journal screams integrity for every reader.", 
        "The journal exclaims integrity for every reader.", 
        "The journal utters integrity for every reader.", 
        "The journal murmurs integrity for every reader.", 
        "The journal whispers integrity for every reader.", 
        "The journal blurts integrity for every reader.", 
        "The journal chants integrity for every reader.", 
        "The journal intones integrity for every reader.", 
        "The journal declaims integrity for every reader.", 
        "The journal retells integrity for every reader.", 
        "The journal theorises integrity for every reader.", 
        "The journal theorizes integrity for every reader.", 
        "The journal hypothesises integrity for every reader.", 
        "The journal hypothesizes integrity for every reader.", 
        "The journal proscribes integrity for every reader.", 
        "The journal legislates integrity for every reader.", 
        "The journal cheers integrity for every reader.", 
        "The journal hypothesises integrity for every reader.", 
        "The journal hypothesizes integrity for every reader.", 
        "The journal theorises integrity for every reader.", 
        "The journal theorizes integrity for every reader.", 
        "The journal opines integrity for every reader.", 
        "The journal deems integrity for every reader.", 
        "The journal reckons integrity for every reader.", 
        "The journal concludes integrity for every reader.", 
        "The journal determines integrity for every reader.", 
        "The journal judges integrity for every reader.", 
        "The journal rules integrity for every reader.", 
        "The journal finds integrity for every reader.", 
        "The journal hints integrity for every reader.", 
        "The journal issues integrity for every reader.", 
        "The journal releases integrity for every reader.", 
        "The journal emits integrity for every reader.", 
        "The journal syndicates integrity for every reader.", 
        "The journal exclaims integrity for every reader.", 
        "The journal bellows integrity for every reader.", 
        "The journal roars integrity for every reader.", 
        "The journal murmurs integrity for every reader.", 
        "The journal mutters integrity for every reader.", 
        "The journal intones integrity for every reader.", 
        "The journal recites integrity for every reader.", 
        "The journal chants integrity for every reader.", 
        "The journal toasts integrity for every reader.", 
        "The journal derives integrity for every reader.", 
        "The journal gathers integrity for every reader.", 
        "The journal rehearses integrity for every reader.", 
        "The journal enjoins integrity for every reader.", 
        "The journal theorises integrity for every reader.", 
        "The journal perceives integrity for every reader.", 
        "The journal concludes integrity for every reader.", 
        "The journal figures integrity for every reader.", 
        "The journal reads integrity for every reader.", 
        "The journal reckons integrity for every reader.", 
        "The journal instructs integrity for every reader.", 
        "The journal retells integrity for every reader.", 
        "The journal computes integrity for every reader.", 
        "The journal hypothesises integrity for every reader.", 
        "The journal theorizes integrity for every reader.", 
        "The journal moots integrity for every reader.", 
        "The journal directs integrity for every reader.", 
        "The journal cheers integrity for every reader.", 
        "The journal calculates integrity for every reader.", 
        "The journal gauges integrity for every reader.", 
        "The journal estimates integrity for every reader.", 
        "The journal opines integrity for every reader.", 
        "The journal admits integrity for every reader.", 
        "The journal recognises integrity for every reader.", 
        "The journal observes integrity for every reader.", 
        "The journal discerns integrity for every reader.", 
        "The journal concedes integrity for every reader.", 
        "The journal hypothesizes integrity for every reader.", 
        "The journal acknowledges integrity for every reader.", 
        "The journal recognizes integrity for every reader.", 
        "The journal works integrity for every reader.", 
    )
    MECHANISM = (
        "The mechanism yells total integrity of the journal.", 
        "The mechanism screams total integrity of the journal.", 
        "The mechanism exclaims total integrity of the journal.", 
        "The mechanism utters total integrity of the journal.", 
        "The mechanism murmurs total integrity of the journal.", 
        "The mechanism whispers total integrity of the journal.", 
        "The mechanism blurts total integrity of the journal.", 
        "The mechanism chants total integrity of the journal.", 
        "The mechanism intones total integrity of the journal.", 
        "The mechanism declaims total integrity of the journal.", 
        "The mechanism retells total integrity of the journal.", 
        "The mechanism theorises total integrity of the journal.", 
        "The mechanism theorizes total integrity of the journal.", 
        "The mechanism hypothesises total integrity of the journal.", 
        "The mechanism hypothesizes total integrity of the journal.", 
        "The mechanism proscribes total integrity of the journal.", 
        "The mechanism legislates total integrity of the journal.", 
        "The mechanism derives total integrity of the journal.", 
        "The mechanism gathers total integrity of the journal.", 
        "The mechanism rehearses total integrity of the journal.", 
        "The mechanism enjoins total integrity of the journal.", 
        "The mechanism theorises total integrity of the journal.", 
        "The mechanism perceives total integrity of the journal.", 
        "The mechanism concludes total integrity of the journal.", 
        "The mechanism figures total integrity of the journal.", 
        "The mechanism reads total integrity of the journal.", 
        "The mechanism reckons total integrity of the journal.", 
        "The mechanism instructs total integrity of the journal.", 
        "The mechanism retells total integrity of the journal.", 
        "The mechanism computes total integrity of the journal.", 
        "The mechanism hypothesises total integrity of the journal.", 
        "The mechanism theorizes total integrity of the journal.", 
        "The mechanism moots total integrity of the journal.", 
        "The mechanism directs total integrity of the journal.", 
        "The mechanism cheers total integrity of the journal.", 
        "The mechanism calculates total integrity of the journal.", 
        "The mechanism gauges total integrity of the journal.", 
        "The mechanism estimates total integrity of the journal.", 
        "The mechanism opines total integrity of the journal.", 
        "The mechanism admits total integrity of the journal.", 
        "The mechanism recognises total integrity of the journal.", 
        "The mechanism observes total integrity of the journal.", 
        "The mechanism discerns total integrity of the journal.", 
        "The mechanism concedes total integrity of the journal.", 
        "The mechanism hypothesizes total integrity of the journal.", 
        "The mechanism acknowledges total integrity of the journal.", 
        "The mechanism recognizes total integrity of the journal.", 
        "The mechanism works total integrity of the journal.", 
    )

    def test_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL + self.MECHANISM:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal consecrates integrity for every "
            "reader."))
        self.assertTrue(
            _scan(mod, "Integrity label for the journal schedule."))
        self.assertTrue(_travel(
            mod, "Integrity label for the journal schedule."))



class SealClaimScanUnconditionalFixR20Tests(unittest.TestCase):
    """Ruling 778: unconditional marker limb."""

    MARKED = (
        "The seal guarantees protection conditional on the deployment confinement fact without any exception.", 
        "The seal guarantees protection conditional on the deployment confinement fact in all circumstances.", 
        "The seal guarantees protection conditional on the deployment confinement fact under all circumstances.", 
        "The seal guarantees protection conditional on the deployment confinement fact without qualification.", 
        "The seal guarantees protection conditional on the deployment confinement fact without reservation.", 
        "The seal guarantees protection conditional on the deployment confinement fact without limitation.", 
        "The seal guarantees protection conditional on the deployment confinement fact in every circumstance.", 
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
            "the deployment confinement fact without exception."))



class StandingAssembliesFixR20Tests(unittest.TestCase):
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
