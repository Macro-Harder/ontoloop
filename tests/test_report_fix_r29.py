"""Fix round 29, Region 1: report seal claim scan pins.

Rulings 1459 to 1466 of the Round 29 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers, the Report and golden span paper findings 1 to 7
and the Confinement paper findings 1 to 11 in their absorbed
limbs, on the templates those papers state. A form probed
in both raising papers on the one template stands counted
once, in the form of the triage merges: the unhasped wording
of ruling 1462 stands counted once, and the asserted forms
of the Confinement Finding 2 followers stand pinned at
ruling 1463, their modal forms at ruling 1459, the followers
counted once at ruling 1459.
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


class SealClaimScanInabilityFixR29Tests(unittest.TestCase):
    """Ruling 1459: inability limb, followers and windows."""

    MODAL_FOLLOWERS = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "fluorinated", "nitrated", "sulfonated", "polymerized",
            "ozonized", "brominated", "iodized", "silicified",
        ))

    ASSERTED_FOLLOWERS = tuple(
        "Records are %s by outsiders." % word for word in (
            "fluorinated", "nitrated", "sulfonated", "polymerized",
            "ozonized", "brominated", "iodized", "silicified",
        ))

    CONF_MODAL = tuple(
        "Records cannot be %s after writing." % word for word in (
            "drenched", "scuffed",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "covetously", "distractedly", "greedily", "grudgingly",
            "indignantly", "wrathfully",
        ))

    WINDOW_PHRASE = (
        "Records cannot in any slaughterhouse be altered "
        "after writing.",
    )

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_FOLLOWERS + self.CONF_MODAL:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_FOLLOWERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOW_WORDS + self.WINDOW_PHRASE:
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
            mod, "Records cannot be carbonized by outsiders."))
        self.assertFalse(_scan(
            mod, "Records are carbonized by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot be condensed by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanGoverningFixR29Tests(unittest.TestCase):
    """Ruling 1460: governing condition limb."""

    PHRASING_WORDS = (
        "under the protectorate of", "under the sovereignty of",
        "under the suzerainty of", "under the hegemony of",
        "by the statute of", "under the statute of",
    )

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in PHRASING_WORDS)

    TRAILING_WORDS = (
        "at whatever time", "in whatever place", "at any place",
        "in any time", "through every place",
        "if and whenever", "if and wherever", "once and only when",
        "when and only when", "when and whenever",
        "whenever and wheresoever", "where and whenever",
    )

    TRAILING = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact holds." % form for form in TRAILING_WORDS)

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather."
        % phrase for phrase in PHRASING_WORDS)

    WEATHER_TRAILING = tuple(
        "The seal guarantees protection %s the weather holds."
        % form for form in TRAILING_WORDS)

    def test_phrasings_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PHRASINGS:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_trailing_forms_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.TRAILING:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_conditions_still_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.WEATHER_PHRASINGS + self.WEATHER_TRAILING):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the "
            "protectorate of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the "
            "sovereignty of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection whensoever the "
            "deployment confinement fact holds."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection if and only when "
            "the deployment confinement fact holds."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR29Tests(unittest.TestCase):
    """Ruling 1461: prefixed compound limb."""

    PREFIX_VERIFIED = tuple(
        "The record stands %s-verified." % prefix
        for prefix in ("ecto", "cis"))

    PREFIX_CHECKED = tuple(
        "The record stands %s-checked." % prefix
        for prefix in ("ecto", "cis"))

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in ("ebonite", "rattan", "wicker"))

    def test_prefixes_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIX_VERIFIED + self.PREFIX_CHECKED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ELEMENTS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "Every record stands pecan-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands cocobolo-verified "
            "before use."))
        self.assertFalse(_scan(
            mod, "The record stands meso-verified."))
        self.assertFalse(_scan(
            mod, "The record stands ana-verified."))
        self.assertFalse(_scan(
            mod, "The record stands endo-verified."))
        self.assertFalse(_scan(
            mod, "The record stands verified."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR29Tests(unittest.TestCase):
    """Ruling 1462: concept root list and un wording limb."""

    WORDINGS = (
        "unshuttered", "unhasped", "uncurbed", "unreined",
        "fangproof", "beakproof", "hoofproof", "hornproof",
        "tuskproof",
        "bladeproof", "blastresistant", "floodresistant",
        "glareresistant", "nailproof", "needleproof",
        "odorresistant", "odourresistant", "pinproof",
        "spikeproof", "vaporresistant", "vapourresistant",
    )

    RECORD_WORDINGS = tuple(
        "The records are %s by outside writers." % word
        for word in WORDINGS)

    STORE_WORDINGS = tuple(
        "The store is %s." % word for word in WORDINGS)

    def test_record_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORD_WORDINGS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE_WORDINGS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are unstrapped by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are unbridled by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are corrosionresistant by outside "
            "writers."))
        self.assertFalse(_scan(
            mod, "The records are clawproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are godproof by outside writers."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanAssertedFixR29Tests(unittest.TestCase):
    """Ruling 1463: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "drools", "crawls", "creeps", "dances", "marches",
            "shudders", "sweats",
        ))

    CONF_ASSERTED = tuple(
        "Records are %s by outsiders." % word for word in (
            "drenched", "scuffed",
        ))

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL_VERBS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_conf_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONF_ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal kneels integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal blushes integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal hiccups integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))


class SealClaimScanMarkerFixR29Tests(unittest.TestCase):
    """Ruling 1464: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "come what will", "at all hazards",
            "under any conditions", "in any circumstance",
            "happen what will", "be the outcome what it may",
            "as long as time lasts", "through all generations",
            "while time endures",
        ))

    COMMA_MARKERS = tuple(
        "%s, %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "come what will", "at all hazards",
            "under any conditions", "regardless of the outcome",
            "no matter what befalls",
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
        self.assertFalse(_scan(mod, self.BASE + " come what may."))
        self.assertFalse(_scan(
            mod, self.BASE + " no exceptions."))
        self.assertFalse(_scan(
            mod, self.BASE + " regardless of the outcome."))
        self.assertFalse(_scan(
            mod, self.BASE + " no matter what befalls."))
        self.assertFalse(_scan(
            mod, self.BASE + " for generations."))


class SealClaimScanNegationFixR29Tests(unittest.TestCase):
    """Ruling 1465: negation narrowing limb, No opening form."""

    PROBED_IS = (
        "No record is replicated after writing.",
        "No record is fetchable after writing.",
        "No record is listable after writing.",
        "No record is retrievable after writing.",
    )

    PROBED_CAN_BE = (
        "No record can be replicated after writing.",
        "No record can be aired after writing.",
        "No record can be narrated after writing.",
        "No record can be recited after writing.",
        "No record can be retrieved after writing.",
    )

    ASSERTED_ANALOGUES = (
        "Records are replicated after writing.",
        "The record is fetchable after writing.",
        "The record is listable after writing.",
        "The record is retrievable after writing.",
        "Records are aired after writing.",
        "Records are narrated after writing.",
        "Records are recited after writing.",
        "Records are retrieved after writing.",
    )

    def test_probed_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED_IS + self.PROBED_CAN_BE:
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
            mod, "No record is initialed after writing."))
        self.assertFalse(_scan(
            mod, "No record can be tracked after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanSyndicationFixR29Tests(unittest.TestCase):
    """Ruling 1466: the syndicatable root, severally."""

    PROBED = (
        "The record is syndicatable after writing.",
        "No record is syndicatable after writing.",
    )

    def test_probed_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_neighbouring_roots_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The record is disclosable after writing."))
        self.assertFalse(_scan(
            mod, "No record is disclosable after writing."))
        self.assertFalse(_scan(
            mod, "The record is mailable after writing."))
        self.assertFalse(_scan(
            mod, "No record is mailable after writing."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


if __name__ == "__main__":
    unittest.main()
