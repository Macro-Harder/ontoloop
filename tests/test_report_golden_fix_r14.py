"""Fix round 14, Region 1: report and golden pins.

Rulings 474 to 478 of the Round 14 triage. Each class pins
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


class SealClaimScanInabilityFixR14Tests(unittest.TestCase):
    """Ruling 474: inability limb, followers and windows."""

    FOLLOWERS = (
        "Records cannot be inscribed by outsiders.",
        "Records cannot be engraved by outsiders.",
        "Records cannot be etched by outsiders.",
        "Records cannot be carved by outsiders.",
        "Records cannot be drafted by outsiders.",
        "Records cannot be penned by outsiders.",
        "Records cannot be authored by outsiders.",
        "Records cannot be composed by outsiders.",
        "Records cannot be seized by outsiders.",
        "Records cannot be posted after writing.",
        "Records cannot be mailed after writing.",
        "Records cannot be mapped after writing.",
        "Records cannot be charted after writing.",
        "Records cannot be graphed after writing.",
        "Records cannot be drawn after writing.",
        "Records cannot be painted after writing.",
        "Records cannot be sketched after writing.",
        "Records cannot be stamped after writing.",
        "Records cannot be marked after writing.",
        "Records cannot be labelled after writing.",
        "Records cannot be tagged after writing.",
        "Records cannot be flagged after writing.",
        "Records cannot be highlighted after writing.",
        "Records cannot be underlined after writing.",
        "Records cannot be shown after writing.",
        "Records cannot be presented after writing.",
        "Records cannot be described after writing.",
        "Records cannot be defined after writing.",
        "Records cannot be named after writing.",
        "Records cannot be captioned after writing.",
        "Records cannot be digitised by outsiders.",
        "Records cannot be digitized by outsiders.",
        "Records cannot be backed by outsiders.",
        "Records cannot be played by outsiders.",
        "Records cannot be imported by outsiders.",
        "Records cannot be queried by outsiders.",
        "Records cannot be searched by outsiders.",
        "Records cannot be located by outsiders.",
        "Records cannot be identified by outsiders.",
    )

    ASSERTED = (
        "Records are seized by outsiders.",
        "Records are posted by outsiders.",
        "Records are marked by outsiders.",
        "Records are described by outsiders.",
    )

    WINDOWS = (
        "Records cannot in any continent be altered after writing.",
        "Records cannot on any continent be altered after writing.",
        "Records cannot in any ocean be altered after writing.",
        "Records cannot in any desert be altered after writing.",
        "Records cannot in any era be altered after writing.",
        "Records cannot in any decade be altered after writing.",
        "Records cannot in any season be altered after writing.",
        "Records cannot in any climate be altered after writing.",
        "Records cannot at any altitude be altered after writing.",
        "Records cannot in any court be altered after writing.",
        "Records cannot by any actor be altered after writing.",
        "Records cannot by any hand be altered after writing.",
        "Records cannot by any tool be altered after writing.",
        "Records cannot in any script be altered after writing.",
        "Records cannot in any tongue be altered after writing.",
        "Records cannot in any harbour be altered after writing.",
        "Records cannot in any harbor be altered after writing.",
        "Records cannot in any theatre be altered after writing.",
        "Records cannot in any theater be altered after writing.",
        "Records cannot in any temple be altered after writing.",
        "Records cannot in any palace be altered after writing.",
        "Records cannot in any prison be altered after writing.",
        "Records cannot in any school be altered after writing.",
        "Records cannot in any hospital be altered after writing.",
        "Records cannot in any galaxy be altered after writing.",
        "Records cannot in any forest be altered after writing.",
        "Records cannot in any valley be altered after writing.",
        "Records cannot in any mountain be altered after writing.",
        "Records cannot in any island be altered after writing.",
        "Records cannot in any peninsula be altered after writing.",
        "Records cannot in any hemisphere be altered after writing.",
        "Records cannot in any zone be altered after writing.",
        "Records cannot in any region be altered after writing.",
        "Records cannot in any district be altered after writing.",
        "Records cannot in any neighbourhood be altered after writing.",
        "Records cannot in any neighborhood be altered after writing.",
        "Records cannot in any community be altered after writing.",
        "Records cannot in any society be altered after writing.",
        "Records cannot in any culture be altered after writing.",
        "Records cannot in any epoch be altered after writing.",
        "Records cannot in any age be altered after writing.",
        "Records cannot in any period be altered after writing.",
        "Records cannot in any millennium be altered after writing.",
        "Records cannot in any trial be altered after writing.",
        "Records cannot with any tool be altered after writing.",
        "Records cannot using any instrument be altered after writing.",
        "Records cannot by any agent be altered after writing.",
        "Records cannot by any authority be altered after writing.",
        "Records cannot under any order be altered after writing.",
        "Records cannot mentally be altered after writing.",
        "Records cannot illegally be altered after writing.",
        "Records cannot again be altered after writing.",
        "Records cannot at any stage be altered.",
        "Records cannot on any computer be altered.",
        "Records cannot by any entity be altered.",
        "Records cannot by any user be altered.",
        "Records cannot in any generation be altered.",
        "Records cannot quietly be altered.",
        "Records cannot lawfully be altered.",
        "Records cannot unlawfully be altered.",
        "Records cannot safely be altered.",
        "Records cannot partially be altered.",
        "Records cannot completely be altered.",
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
            "Records cannot be narrated by outsiders.",
            "Records cannot be cracked after writing.",
            "Records cannot in any country be altered after writing.",
            "Records cannot in any world be altered after writing.",
            "Records cannot under any conditions be altered after writing.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(mod, "The seal does not guarantee protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanGoverningFixR14Tests(unittest.TestCase):
    """Ruling 475: governing condition limb."""

    GOVERNED = (
        "The seal guarantees protection regulated by the deployment confinement fact.",
        "The seal guarantees protection dictated by the deployment confinement fact.",
        "The seal guarantees protection mandated by the deployment confinement fact.",
        "The seal guarantees protection ordered by the deployment confinement fact.",
        "The seal guarantees protection decreed by the deployment confinement fact.",
        "The seal guarantees protection prescribed by the deployment confinement fact.",
        "The seal guarantees protection stipulated by the deployment confinement fact.",
        "The seal guarantees protection ruled by the deployment confinement fact.",
        "The seal guarantees protection by reason of the deployment confinement fact.",
        "The seal guarantees protection on the grounds of the deployment confinement fact.",
        "The seal guarantees protection on grounds of the deployment confinement fact.",
        "The seal guarantees protection in response to the deployment confinement fact.",
        "The seal guarantees protection in reaction to the deployment confinement fact.",
        "The seal guarantees protection in conformity to the deployment confinement fact.",
        "The seal guarantees protection at the mercy of the deployment confinement fact.",
        "The seal guarantees protection in thrall to the deployment confinement fact.",
        "The seal guarantees protection subordinate to the deployment confinement fact.",
        "The seal guarantees protection answerable to the deployment confinement fact.",
        "The seal guarantees protection beholden to the deployment confinement fact.",
        "The seal guarantees protection thanks to the deployment confinement fact.",
        "The seal guarantees protection because of the deployment confinement fact.",
        "The seal guarantees protection resting purely on the deployment confinement fact.",
        "The seal guarantees protection conditional purely on the deployment confinement fact.",
        "The seal guarantees protection contingent purely on the deployment confinement fact.",
        "The seal guarantees protection dependent purely on the deployment confinement fact.",
        "The seal guarantees protection based purely on the deployment confinement fact.",
        "The seal guarantees protection founded purely on the deployment confinement fact.",
        "The seal guarantees protection hinging purely on the deployment confinement fact.",
        "The seal guarantees protection founded exclusively on the deployment confinement fact.",
        "The seal guarantees protection hinging exclusively on the deployment confinement fact.",
        "The seal guarantees protection as governed by the deployment confinement fact.",
        "The seal guarantees protection as regulated by the deployment confinement fact.",
        "The seal guarantees protection as dictated by the deployment confinement fact.",
        "The seal guarantees protection as decreed by the deployment confinement fact.",
        "The seal guarantees protection as ordered by the deployment confinement fact.",
        "The seal guarantees protection as ruled by the deployment confinement fact.",
        "The seal guarantees protection in terms of the deployment confinement fact.",
        "The seal guarantees protection with regard to the deployment confinement fact.",
        "The seal guarantees protection with respect to the deployment confinement fact.",
        "The seal guarantees protection in regard to the deployment confinement fact.",
        "The seal guarantees protection in reference to the deployment confinement fact.",
        "The seal guarantees protection in relation to the deployment confinement fact.",
        "The seal guarantees protection under the guidance of the deployment confinement fact.",
        "The seal guarantees protection under the control of the deployment confinement fact.",
        "The seal guarantees protection under the supervision of the deployment confinement fact.",
        "The seal guarantees protection under the oversight of the deployment confinement fact.",
        "The seal guarantees protection within the scope of the deployment confinement fact.",
        "The seal guarantees protection within the framework of the deployment confinement fact.",
        "The seal guarantees protection within the confines of the deployment confinement fact.",
        "The seal guarantees protection inside the bounds of the deployment confinement fact.",
        "The seal guarantees protection in the framework of the deployment confinement fact.",
        "The seal guarantees protection in the context of the deployment confinement fact.",
        "The seal guarantees protection depending upon the deployment confinement fact.",
        "The seal guarantees protection against the backdrop of the deployment confinement fact.",
        "The seal guarantees protection as per the deployment confinement fact.",
        "The seal guarantees protection per the deployment confinement fact.",
        "The seal guarantees protection following the deployment confinement fact.",
        "The seal guarantees protection behind the deployment confinement fact.",
        "The seal guarantees protection alongside the deployment confinement fact.",
    )

    WEATHER = (
        "The seal guarantees protection regulated by the weather holds.",
        "The seal guarantees protection dictated by the weather holds.",
        "The seal guarantees protection because of the weather holds.",
        "The seal guarantees protection thanks to the weather holds.",
        "The seal guarantees protection as governed by the weather holds.",
        "The seal guarantees protection as per the weather holds.",
        "The seal guarantees protection in response to the weather holds.",
        "The seal guarantees protection with regard to the weather holds.",
        "The seal guarantees protection following the weather holds.",
        "The seal guarantees protection per the weather holds.",
        "The seal guarantees protection on the grounds of the weather holds.",
        "The seal guarantees protection resting purely on the weather holds.",
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
            "The seal guarantees protection governed by the deployment confinement fact.",
            "The seal guarantees protection pursuant to the deployment confinement fact.",
            "The seal guarantees protection by virtue of the deployment confinement fact.",
            "The seal guarantees protection in conformity with the deployment confinement fact.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
        self.assertFalse(_scan(mod, "The seal guarantees protection."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanPrefixedFixR14Tests(unittest.TestCase):
    """Ruling 476: prefixed compound limb."""

    FORMS = (
        "The record stands digital-verified.",
        "Every record stands digital-checked before use.",
        "The record stands electronic-verified.",
        "Every record stands electronic-checked before use.",
        "The record stands remote-verified.",
        "Every record stands remote-checked before use.",
        "The record stands global-verified.",
        "Every record stands global-checked before use.",
        "The record stands local-verified.",
        "Every record stands local-checked before use.",
        "The record stands national-verified.",
        "Every record stands national-checked before use.",
        "The record stands federal-verified.",
        "Every record stands federal-checked before use.",
        "The record stands system-verified.",
        "Every record stands system-checked before use.",
        "The record stands network-verified.",
        "Every record stands network-checked before use.",
        "The record stands server-verified.",
        "Every record stands server-checked before use.",
        "The record stands mobile-verified.",
        "Every record stands mobile-checked before use.",
        "The record stands quantum-verified.",
        "Every record stands quantum-checked before use.",
        "The record stands mega-examined.",
        "The record stands pro-examined.",
        "The record stands mega-scrutinized.",
        "The record stands pro-scrutinized.",
        "The record stands mega-monitored.",
        "The record stands mega-observed.",
        "The record stands mega-authenticated.",
        "The record stands pro-authenticated.",
        "The record stands mega-perused.",
        "The record stands mega-glimpsed.",
        "The record stands mega-spied.",
        "The record stands mega-skimmed.",
        "The record stands mega-browsed.",
        "The record stands mega-surveyed.",
        "The record stands mega-videotaped.",
        "The record stands mega-audiotaped.",
        "The record stands multiple-verified.",
        "The record stands partly-verified.",
        "The record stands wholly-verified.",
        "The record stands thoroughly-verified.",
        "The record stands carefully-verified.",
        "The record stands rigorously-verified.",
        "The record stands strictly-verified.",
        "The record stands closely-verified.",
        "The record stands deeply-verified.",
        "The record stands truly-verified.",
        "The record stands really-verified.",
        "The record stands genuinely-verified.",
        "The record stands officially-verified.",
        "The record stands legally-verified.",
        "The record stands informally-verified.",
        "The record stands privately-verified.",
        "The record stands secretly-verified.",
        "The record stands jointly-verified.",
        "The record stands mutually-verified.",
        "The record stands individually-verified.",
        "The record stands separately-verified.",
        "The record stands internally-verified.",
        "The record stands multiple-checked.",
        "The record stands partly-checked.",
        "The record stands wholly-checked.",
        "The record stands thoroughly-checked.",
        "The record stands carefully-checked.",
        "The record stands rigorously-checked.",
        "The record stands strictly-checked.",
        "The record stands closely-checked.",
        "The record stands deeply-checked.",
        "The record stands truly-checked.",
        "The record stands really-checked.",
        "The record stands genuinely-checked.",
        "The record stands officially-checked.",
        "The record stands legally-checked.",
        "The record stands informally-checked.",
        "The record stands privately-checked.",
        "The record stands secretly-checked.",
        "The record stands jointly-checked.",
        "The record stands mutually-checked.",
        "The record stands individually-checked.",
        "The record stands separately-checked.",
        "The record stands internally-checked.",
        "Every record stands platform-checked before use.",
        "Every record stands device-checked before use.",
        "Every record stands software-checked before use.",
        "Every record stands algorithm-checked before use.",
        "Every record stands ai-checked before use.",
        "Every record stands robot-checked before use.",
        "Every record stands drone-checked before use.",
        "Every record stands satellite-checked before use.",
        "Every record stands worldwide-checked before use.",
        "Every record stands nationwide-checked before use.",
        "Every record stands company-checked before use.",
        "Every record stands industrywide-checked before use.",
        "Every record stands community-checked before use.",
        "Every record stands society-checked before use.",
        "Every record stands church-checked before use.",
        "Every record stands school-checked before use.",
        "Every record stands university-checked before use.",
        "Every record stands hospital-checked before use.",
        "Every record stands bank-checked before use.",
        "Every record stands police-checked before use.",
        "Every record stands army-checked before use.",
        "Every record stands navy-checked before use.",
        "Every record stands council-checked before use.",
        "Every record stands committee-checked before use.",
        "Every record stands tribunal-checked before use.",
        "Every record stands senate-checked before use.",
        "Every record stands parliament-checked before use.",
        "Every record stands ministry-checked before use.",
        "Every record stands department-checked before use.",
        "Every record stands division-checked before use.",
        "Every record stands branch-checked before use.",
        "Every record stands unit-checked before use.",
        "Every record stands squad-checked before use.",
        "Every record stands veteran-checked before use.",
    )

    def test_prefixed_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "The record stands smart-verified.",
            "The record stands mega-verified.",
            "The record stands mega-audited.",
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


class SealClaimScanLexiconFixR14Tests(unittest.TestCase):
    """Ruling 477: lexicon limb."""

    FORMS = (
        "Records stand unscarred after writing.",
        "Records stand undamaged after writing.",
        "Records stand unharmed after writing.",
        "Records stand unbroken after writing.",
        "Records stand unbruised after writing.",
        "Records stand unwounded after writing.",
        "Records stand unchipped after writing.",
        "Records stand untorn after writing.",
        "The records are unscarred by outside writers.",
        "The records are undamaged by outside writers.",
        "The records are unbroken by outside writers.",
        "Heads stand wax-stamped for every actor.",
        "Heads stand steel-stamped for every actor.",
        "Heads stand iron-stamped for every actor.",
        "Heads stand hand-etched for every actor.",
        "Heads stand acid-etched for every actor.",
        "Heads stand copper-etched for every actor.",
        "Heads stand stone-etched for every actor.",
        "Heads stand wood-etched for every actor.",
        "Heads stand glass-etched for every actor.",
        "The store is unending.",
        "The store is absolute.",
        "The store is pure.",
        "The store is intact.",
        "The store is whole.",
        "The store is complete.",
        "The store is total.",
        "The store is supreme.",
        "The store is ultimate.",
        "The store is undoubted.",
        "The store is armoured.",
        "The store is armored.",
        "The store is bolted.",
        "The store is chained.",
        "The store is bound.",
        "The store is tied.",
        "The store is fastened.",
        "Records stand lightproof after writing.",
        "Records stand vacuum-sealed after writing.",
        "The records are enduring by outside writers.",
        "The records are failproof by outside writers.",
        "The records are dirtproof by outside writers.",
        "The records are spillproof by outside writers.",
        "The records are splinterproof by outside writers.",
        "The records are chipproof by outside writers.",
        "The records are fadeproof by outside writers.",
        "The records are wrinkleproof by outside writers.",
        "The records are creaseproof by outside writers.",
        "The records are odourproof by outside writers.",
        "The records are vaporproof by outside writers.",
        "The records are vapourproof by outside writers.",
        "The records are germproof by outside writers.",
        "The records are mothproof by outside writers.",
        "The records are mildewproof by outside writers.",
        "The records are corrosionproof by outside writers.",
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
        self.assertFalse(_scan(mod, "The store is unimpregnable."))
        self.assertFalse(_scan(mod, "Records stand untainted after writing."))
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanAssertedFixR14Tests(unittest.TestCase):
    """Ruling 478: asserted form limb."""

    FORMS = (
        "The journal projects integrity for every reader.",
        "The journal bespeaks integrity for every reader.",
        "The journal flaunts integrity for every reader.",
        "The journal boasts integrity for every reader.",
        "The journal sports integrity for every reader.",
        "The journal reveals integrity for every reader.",
        "The journal discloses integrity for every reader.",
        "The journal exposes integrity for every reader.",
        "The journal unveils integrity for every reader.",
        "The mechanism projects total integrity of the journal.",
        "The mechanism flaunts total integrity of the journal.",
        "The mechanism endorses total integrity of the journal.",
        "The mechanism boasts total integrity of the journal.",
        "The mechanism swears total integrity of the journal.",
        "The mechanism witnesses total integrity of the journal.",
        "The mechanism consolidates total integrity of the journal.",
        "The mechanism shelters total integrity of the journal.",
    )

    def test_asserted_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_and_fragment_boundary_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal exudes integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal embodies integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The mechanism trumpets total integrity of the journal."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))
        self.assertTrue(_travel(
            mod, "Integrity label for the journal schedule."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


if __name__ == "__main__":
    unittest.main()
