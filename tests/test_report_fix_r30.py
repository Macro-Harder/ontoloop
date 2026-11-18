"""Fix round 30, Region 1: report seal claim scan pins.

Rulings 1561 to 1568 of the Round 30 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers, the Report and golden span paper findings 1 to 8
and the Confinement paper findings 1 to 10 in their absorbed
limbs, on the templates those papers state. A form probed
in both raising papers on the one template stands counted
once, in the form of the triage merges: the petulantly
wording of ruling 1561, the if and wheresoever form of
ruling 1562, and the solventresistant wording of ruling
1564 each stand counted once, and the asserted forms of
the Confinement Finding 2 followers stand pinned at
ruling 1565, their modal forms at ruling 1561, the
followers counted once at ruling 1561.
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


class SealClaimScanInabilityFixR30Tests(unittest.TestCase):
    """Ruling 1561: inability limb, followers and windows."""

    MODAL_FOLLOWERS = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "acetylated", "alkylated", "amidated", "aminated",
            "carboxylated", "deuterated", "esterified",
            "ethoxylated", "glycosylated", "halogenated",
            "hydroxylated", "methylated", "peroxidized",
            "phosphorylated", "propoxylated", "saponified",
            "thiolated", "decarboxylated", "sulfurized",
            "vulcanised",
        ))

    ASSERTED_FOLLOWERS = tuple(
        "Records are %s by outsiders." % word for word in (
            "acetylated", "alkylated", "amidated", "aminated",
            "carboxylated", "deuterated", "esterified",
            "ethoxylated", "glycosylated", "halogenated",
            "hydroxylated", "methylated", "peroxidized",
            "phosphorylated", "propoxylated", "saponified",
            "thiolated", "decarboxylated", "sulfurized",
            "vulcanised",
        ))

    CONF_MODAL = tuple(
        "Records cannot be %s after writing." % word for word in (
            "drilled", "frosted", "moistened", "polished",
            "sanded", "stretched", "thawed", "wetted", "whitened",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "nonchalantly", "petulantly", "querulously",
            "waspishly", "surlily", "tiredly", "unwillingly",
            "zealously",
        ))

    WINDOW_PHRASE = (
        "Records cannot in any millhouse be altered "
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
            _scan(mod, "Records cannot be fluorinated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are fluorinated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be drenched after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot covetously be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any slaughterhouse be altered "
            "after writing."))
        self.assertFalse(
            _scan(mod, "Records cannot be epoxidized by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are epoxidized by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanGoverningFixR30Tests(unittest.TestCase):
    """Ruling 1562: governing condition limb."""

    PHRASING_WORDS = (
        "under the jurisdiction of", "by the jurisdiction of",
        "under the wardship of", "under the imperium of",
        "by the bull of", "by the concession of",
        "by the firman of", "by the franchise of",
        "by the letters patent of", "by the proclamation of",
        "by the rescript of", "by the ukase of",
    )

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in PHRASING_WORDS)

    TRAILING_WORDS = (
        "at whatever place", "in whatever time",
        "through every time", "at every place",
        "through all places", "at all places",
        "for whatever time", "if and wheresoever",
        "once and wheresoever", "whensoever and wheresoever",
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
            mod, "The seal guarantees protection under the aegis of "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the statute of "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection wheresoever the "
            "deployment confinement fact holds."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection at whatever time "
            "the deployment confinement fact holds."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR30Tests(unittest.TestCase):
    """Ruling 1563: prefixed compound limb."""

    PREFIXES = (
        "biblio", "dactylo", "psycho", "socio", "mechano",
        "microbio",
    )

    PREFIX_VERIFIED = tuple(
        "The record stands %s-verified." % prefix
        for prefix in PREFIXES)

    PREFIX_CHECKED = tuple(
        "The record stands %s-checked." % prefix
        for prefix in PREFIXES)

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in (
            "ipe", "cumaru", "goncalo", "ashwood", "birchwood",
            "elmwood",
        ))

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
            mod, "The record stands ecto-verified."))
        self.assertFalse(_scan(
            mod, "Every record stands pecan-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands ebonite-verified before use."))
        self.assertFalse(_scan(
            mod, "The record stands verified."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR30Tests(unittest.TestCase):
    """Ruling 1564: concept root list and un wording limb."""

    WORDINGS = (
        "unvented", "pickpocketproof", "solventresistant",
        "cutresistant", "frostresistant", "iceresistant",
        "mudresistant", "pressureresistant", "sandresistant",
        "snowresistant", "stabproof",
        "unalarmed", "uncurtained", "undoored", "ungated",
        "unkeyed", "unshaded", "unwalled",
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
            mod, "The records are uncurbed by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are bladeproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are vapourresistant by outside "
            "writers."))
        self.assertFalse(_scan(
            mod, "The records are unbridled by outside writers."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanAssertedFixR30Tests(unittest.TestCase):
    """Ruling 1565: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in ("salivates",))

    CONF_ASSERTED = tuple(
        "Records are %s by outsiders." % word for word in (
            "drilled", "frosted", "moistened", "polished",
            "sanded", "stretched", "thawed", "wetted", "whitened",
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
            mod, "The journal drools integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal crawls integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))


class SealClaimScanMarkerFixR30Tests(unittest.TestCase):
    """Ruling 1566: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "under all skies", "under any skies", "come what might",
            "no matter the weather", "in season and out of season",
            "through prosperity and adversity", "by day and by night",
            "day in day out", "year in year out",
            "without let or hindrance", "in any weather",
            "till the world ends", "so long as the sun shines",
            "while grass grows", "till hell freezes over",
            "for all the ages", "through all the ages",
            "till judgment day",
        ))

    COMMA_MARKERS = tuple(
        "%s, %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "under all skies", "under any skies", "come what might",
            "no matter the weather", "in season and out of season",
            "through prosperity and adversity", "by day and by night",
            "day in day out", "year in year out",
            "without let or hindrance", "in any weather",
            "till the world ends", "so long as the sun shines",
            "while grass grows", "till hell freezes over",
            "do or die", "be the cost what it may",
            "at all events whatsoever",
            "through all generations to come",
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
            mod, self.BASE + " through all generations."))
        self.assertFalse(_scan(
            mod, self.BASE + " as long as time lasts."))


class SealClaimScanNegationFixR30Tests(unittest.TestCase):
    """Ruling 1567: negation narrowing limb, No opening form."""

    PROBED_IS = (
        "No record is pawned after writing.",
        "No record is auctioned after writing.",
    )

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word for word in (
            "pawned", "auctioned", "boxed", "crated", "digitised",
            "digitized", "filed", "shelved", "stored", "texted",
            "vaulted",
        ))

    ASSERTED_ANALOGUES = tuple(
        "Records are %s after writing." % word for word in (
            "pawned", "auctioned", "boxed", "crated", "digitised",
            "digitized", "filed", "shelved", "stored", "texted",
            "vaulted",
        ))

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
            mod, "No record is replicated after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanConceptRootsFixR30Tests(unittest.TestCase):
    """Ruling 1568: roots outside the judged concept roots."""

    ROOTS = (
        "excerpted", "leased", "sublicensed", "franchised",
        "monetized", "reprinted", "resold", "mortgaged",
        "bequeathed", "lent", "subtitled", "dubbed", "rekeyed",
        "relabelled", "renumbered", "reclassified", "reindexed",
        "rescanned",
    )

    PROBED_IS = tuple(
        "No record is %s after writing." % word for word in ROOTS)

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in ROOTS)

    ASSERTED = tuple(
        "Records are %s after writing." % word for word in ROOTS)

    CONF_TEXTABLE = (
        "The record is textable after writing.",
        "No record is textable after writing.",
    )

    CONF_VERBS = ("banked", "cabled", "radioed", "warehoused")

    CONF_ASSERTED = tuple(
        "Records are %s after writing." % word for word in CONF_VERBS)

    CONF_NO = tuple(
        "No record can be %s after writing." % word
        for word in CONF_VERBS)

    def test_probed_is_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED_IS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_probed_can_be_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_conf_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.CONF_TEXTABLE + self.CONF_ASSERTED
                + self.CONF_NO):
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
        self.assertFalse(_scan(
            mod, "Records are replicated after writing."))
        self.assertFalse(_scan(
            mod, "No record is syndicatable after writing."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


if __name__ == "__main__":
    unittest.main()
