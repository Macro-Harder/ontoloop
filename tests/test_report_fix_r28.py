"""Fix round 28, Region 1: report seal claim scan pins.

Rulings 1367 to 1373 of the Round 28 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers, the Report and golden span paper findings 1 to 7
and the Confinement paper findings 1 to 7 in their absorbed
limbs, on the templates those papers state. A form probed
in both raising papers on the one template stands counted
once, in the form of the triage merges.
"""

import unittest

from tests import harness


def _scan(mod, statement):
    return mod._seal_claim_scan(statement)


def _travel(mod, statement):
    result = mod.fixed_text_travel_lint(
        assembly="export", content=statement)
    return result["passed"]


_GOVERNED_CLAIM = ("The seal guarantees protection conditional on "
                   "the deployment confinement fact")


class SealClaimScanInabilityFixR28Tests(unittest.TestCase):
    """Ruling 1367: inability limb, followers and windows."""

    MODAL_FOLLOWERS = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "condensed", "solidified", "ionized", "electrolyzed",
            "filtered", "purified", "refined", "vulcanized",
            "tanned",
        ))

    ASSERTED_FOLLOWERS = tuple(
        "Records are %s by outsiders." % word for word in (
            "condensed", "ionized", "electrolyzed", "filtered",
            "purified", "refined", "vulcanized", "tanned",
        ))

    CONF_MODAL = tuple(
        "Records cannot be %s after writing." % word for word in (
            "abraded", "bent", "blackened", "browned", "chopped",
            "gashed", "oxidised", "oxidized", "rusted", "slashed",
            "snapped", "soiled", "split", "twisted", "yellowed",
        ))

    CONF_ASSERTED = tuple(
        "Records are %s by outsiders." % word for word in (
            "abraded", "bent", "blackened", "browned", "chopped",
            "gashed", "oxidised", "oxidized", "rusted", "slashed",
            "snapped", "soiled", "split", "twisted", "yellowed",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "feverishly", "franticly", "hectically", "madly",
            "harshly", "sullenly", "peevishly", "irritably",
        ))

    CONF_WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "bewilderedly", "bitterly", "confusedly", "dazedly",
            "despairingly", "enviously", "fearfully",
        ))

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_FOLLOWERS + self.CONF_MODAL:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.ASSERTED_FOLLOWERS + self.CONF_ASSERTED):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOW_WORDS + self.CONF_WINDOW_WORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be fermented by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be blistered after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot joylessly be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records are solidified by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot be distilled by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanGoverningFixR28Tests(unittest.TestCase):
    """Ruling 1368: governing condition limb."""

    PHRASING_WORDS = (
        "under the regency of", "by the protectorate of",
        "by the consulship of", "by the tribunate of",
        "by the archdiocese of", "by the patriarchate of",
        "by the khanate of", "by the receivership of",
        "by the tutelage of", "by the sponsorship of",
        "by the admiralty of", "by the sovereignty of",
        "by the dominion of", "under the dominion of",
        "by the hegemony of", "by the suzerainty of",
        "by the overlordship of", "under the overlordship of",
        "by the wardenship of", "by the keepership of",
        "by the intendancy of", "by the comptrollership of",
        "by the treasurership of",
    )

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in PHRASING_WORDS)

    TRAILING_WORDS = (
        "wheresoever", "whithersoever", "at any time",
        "in any place", "in every place", "for the whole time",
        "through all the time", "at all times", "in all places",
    )

    TRAILING = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact holds." % form for form in TRAILING_WORDS)

    CONF_TRAILING = (
        "The seal guarantees protection if and only when the "
        "deployment confinement fact holds.",
        "The seal guarantees protection once and whenever the "
        "deployment confinement fact holds.",
    )

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather."
        % phrase for phrase in PHRASING_WORDS)

    WEATHER_TRAILING = tuple(
        "The seal guarantees protection %s the weather holds."
        % form for form in TRAILING_WORDS)

    WEATHER_CONF_TRAILING = (
        "The seal guarantees protection if and only when the "
        "weather holds.",
        "The seal guarantees protection once and whenever the "
        "weather holds.",
    )

    def test_phrasings_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PHRASINGS:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_trailing_forms_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.TRAILING + self.CONF_TRAILING:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_conditions_still_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.WEATHER_PHRASINGS + self.WEATHER_TRAILING
                + self.WEATHER_CONF_TRAILING):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the regency "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the "
            "tutelage of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection during such "
            "time as the deployment confinement fact holds."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection whenever the "
            "deployment confinement fact holds."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR28Tests(unittest.TestCase):
    """Ruling 1369: prefixed compound limb."""

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in (
            "pecan", "aspen", "holly", "magnolia", "olivewood",
            "camphorwood", "myrtlewood", "persimmon",
        ))

    PREFIXES = ("meso", "contra", "de", "dis")

    PREFIX_VERIFIED = tuple(
        "The record stands %s-verified." % prefix
        for prefix in PREFIXES)

    PREFIX_CHECKED = tuple(
        "The record stands %s-checked." % prefix
        for prefix in PREFIXES)

    CONF_PREFIXES = tuple(
        "The record stands %s-%s." % (prefix, root)
        for prefix in ("ana", "ortho")
        for root in ("verified", "checked"))

    def test_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ELEMENTS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_prefixes_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.PREFIX_VERIFIED + self.PREFIX_CHECKED
                + self.CONF_PREFIXES):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "Every record stands wenge-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands ebony-verified before use."))
        self.assertFalse(_scan(
            mod, "The record stands aniso-verified."))
        self.assertFalse(_scan(
            mod, "The record stands proto-verified."))
        self.assertFalse(_scan(
            mod, "The record stands verified."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR28Tests(unittest.TestCase):
    """Ruling 1370: concept root list and un wording limb."""

    UN_WORDS = (
        "unbridled", "unsaddled", "unmuzzled", "unhandcuffed",
        "ungagged", "unhooded", "uncapped", "unthreaded",
    )

    RECORD_UN = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDS)

    STORE_UN = tuple(
        "The store is %s." % word for word in UN_WORDS)

    RECORD_PROOF = (
        "The records are thornproof by outside writers.",
    )

    STORE_PROOF = ("The store is thornproof.",)

    RESISTANT_WORDS = (
        "abrasionresistant", "acidresistant", "alkaliresistant",
        "chemicalresistant", "coldresistant", "dustresistant",
        "greaseresistant", "heatresistant", "impactresistant",
        "oilresistant", "punctureresistant", "shockresistant",
        "sunresistant", "tearresistant", "weatherresistant",
        "windresistant",
    )

    RECORD_RESISTANT = tuple(
        "The records are %s by outside writers." % word
        for word in RESISTANT_WORDS)

    STORE_RESISTANT = tuple(
        "The store is %s." % word for word in RESISTANT_WORDS)

    def test_record_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.RECORD_UN + self.RECORD_PROOF
                + self.RECORD_RESISTANT):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.STORE_UN + self.STORE_PROOF
                + self.STORE_RESISTANT):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are unstrapped by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are corrosionresistant by outside "
            "writers."))
        self.assertFalse(_scan(
            mod, "The records are godproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are acidproof by outside writers."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanAssertedFixR28Tests(unittest.TestCase):
    """Ruling 1371: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "kneels", "crouches", "stretches", "weeps", "baaes",
            "lowes", "whickers",
        ))

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL_VERBS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal blushes integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal bangs integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal sobs integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))


class SealClaimScanMarkerFixR28Tests(unittest.TestCase):
    """Ruling 1372: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "happen what may", "at all events",
            "whatever may happen", "whatever befalls",
            "whatever ensues", "whatever transpires",
            "whatever occurs", "no matter the consequence",
            "for generations", "for the rest of time",
            "from generation to generation",
            "through all the years", "through the ages",
        ))

    COMMA_MARKERS = tuple(
        "%s, %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "whatever may happen", "whatever befalls",
            "whatever ensues", "whatever transpires",
            "whatever occurs", "no matter the consequence",
            "at all events", "whatever the outcome",
            "whatever the result", "no exceptions",
        ))

    def test_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MARKERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_comma_clause_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMMA_MARKERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(mod, self.BASE + "."))
        self.assertFalse(_scan(mod, self.BASE + " without fail."))
        self.assertFalse(_scan(mod, self.BASE + " ab aeterno."))
        self.assertFalse(_scan(
            mod, self.BASE + " no exceptions."))
        self.assertFalse(_scan(
            mod, self.BASE + " come what may."))


class SealClaimScanNegationFixR28Tests(unittest.TestCase):
    """Ruling 1373: negation narrowing limb, No opening form."""

    PROBED_WORDS = (
        "initialed", "typeset", "plotted", "stencilled",
        "stenciled", "lithographed", "mimeographed",
        "telecopied", "exhibited", "showcased", "paraded",
        "flaunted", "trumpeted", "heralded", "proclaimed",
        "announced", "declared", "pronounced", "decreed",
        "ordained", "mandated", "legislated", "enacted",
        "sanctioned", "licensed", "patented", "trademarked",
        "enlisted", "inducted", "pledged", "vowed",
        "guaranteed", "warranted", "insured", "bonded",
        "underwritten",
    )

    PROBED_IS = tuple(
        "No record is %s after writing." % word
        for word in PROBED_WORDS)

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in PROBED_WORDS)

    CONF_IS = tuple(
        "No record is %s after writing." % word for word in (
            "disclosable", "mailable", "postable",
        ))

    CONF_CAN_BE = tuple(
        "No record can be %s after writing." % word for word in (
            "disclosed", "mailed", "posted", "shipped",
        ))

    ASSERTED_ANALOGUES = tuple(
        "Records are %s after writing." % word
        for word in PROBED_WORDS) + (
        "The record is disclosable after writing.",
        "The record is mailable after writing.",
        "The record is postable after writing.",
        "Records are disclosed after writing.",
        "Records are mailed after writing.",
        "Records are posted after writing.",
        "Records are shipped after writing.",
    )

    def test_probed_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED_IS + self.PROBED_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_conf_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONF_IS + self.CONF_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_analogues_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_ANALOGUES:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "No bundle name was hidden in this record."))
        self.assertFalse(_scan(
            mod, "Records are hidden by outsiders."))
        self.assertFalse(_scan(mod, "No data leaves the store."))
        self.assertFalse(_scan(
            mod, "No record is fingerprinted after writing."))
        self.assertFalse(_scan(
            mod, "No record is embossed after writing."))
        self.assertFalse(_scan(
            mod, "No record can be tracked after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


if __name__ == "__main__":
    unittest.main()
