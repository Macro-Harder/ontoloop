"""Fix round 23, Region 1: report seal claim scan pins.

Rulings 958 to 964 of the Round 23 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers on the templates those papers state. A form probed
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


class SealClaimScanInabilityFixR23Tests(unittest.TestCase):
    """Ruling 958: inability limb, followers and windows."""

    MODAL_FOLLOWERS = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "exhumed", "liquefied", "vaporised", "atomized",
            "disintegrated", "eradicated", "plundered", "pillaged",
            "scorched", "singed",
        ))

    ASSERTED_FOLLOWERS = tuple(
        "Records are %s by outsiders." % word for word in (
            "exhumed", "liquefied", "plundered",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "sluggishly", "mischievously", "solemnly", "ritually",
            "noisily", "frantically",
            "earnestly", "dispassionately", "unemotionally",
            "placidly", "tranquilly", "peacefully", "restfully",
            "purely", "obviously", "seemingly", "avowedly",
            "professedly", "smoothly", "steadily", "firmly",
            "fixedly", "resolutely", "steadfastly", "doggedly",
            "stubbornly", "obstinately", "mulishly", "pigheadedly",
            "wittingly", "consciously",
        ))

    WINDOW_PLACES = tuple(
        "Records cannot in any %s be altered after writing."
        % word for word in (
            "zoo",
            "muniment room", "columbarium", "magazine", "coop",
            "hutch", "alcove", "cubicle", "booth", "stall",
            "larder", "cellarage",
        ))

    MODAL_FASTENING = tuple(
        "Records cannot be %s after writing." % word for word in (
            "shackled", "anchored", "embedded", "lodged", "wedged",
            "crimped", "secured", "hitched", "coupled", "hinged",
            "pegged", "dowelled", "mortised", "tenoned", "braced",
            "buttressed", "propped", "shored", "girded", "banded",
            "strapped", "belted", "collared", "ringed", "hooped",
            "caged", "corralled", "enclosed", "encircled",
            "surrounded", "ring-fenced", "hedged", "sheltered",
            "housed", "quartered", "billeted", "garrisoned",
            "manned", "patrolled", "sentinelled",
        ))

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_FOLLOWERS + self.MODAL_FASTENING:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_FOLLOWERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOW_WORDS + self.WINDOW_PLACES:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be welded after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any sanctum be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot frankly be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot be fingerprinted by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanGoverningFixR23Tests(unittest.TestCase):
    """Ruling 959: governing condition limb."""

    TRAILING = (
        "The seal guarantees protection if the deployment "
        "confinement fact holds.",
        "The seal guarantees protection when the deployment "
        "confinement fact holds.",
        "The seal guarantees protection whenever the deployment "
        "confinement fact holds.",
        "The seal guarantees protection while the deployment "
        "confinement fact holds.",
        "The seal guarantees protection whilst the deployment "
        "confinement fact holds.",
        "The seal guarantees protection where the deployment "
        "confinement fact holds.",
        "The seal guarantees protection in cases where the "
        "deployment confinement fact holds.",
        "The seal guarantees protection in so far as the "
        "deployment confinement fact holds.",
        "The seal guarantees protection to the extent that the "
        "deployment confinement fact holds.",
        "The seal guarantees protection only while the deployment "
        "confinement fact holds.",
    )

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in (
            "on the order of", "by the consent of",
            "by the approval of", "by the instruction of",
            "by the say-so of", "by the command of",
            "on the command of", "by the request of",
            "by the determination of", "on the determination of",
            "by the findings of", "on the findings of",
            "pursuant to the direction of",
            "following the direction of",
            "subject to the direction of", "by the oversight of",
            "on the oversight of", "by the supervision of",
            "under the urging of", "under the insistence of",
            "by the insistence of", "under the demand of",
            "by the demand of", "under the invitation of",
            "by the invitation of", "under the suggestion of",
            "by the suggestion of", "under the decision of",
            "at the decision of", "under the ruling of",
            "at the ruling of", "under the judgment of",
            "at the judgment of", "under the verdict of",
            "at the verdict of", "under the licence of",
            "at the licence of", "under the license of",
            "at the license of", "on the licence of",
            "on the license of",
        ))

    WEATHER_TRAILING = tuple(
        "The seal guarantees protection %s the weather holds."
        % word for word in ("if", "when", "while"))

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather." % phrase
        for phrase in (
            "on the order of", "by the consent of",
            "by the approval of", "by the instruction of",
            "by the say-so of", "by the command of",
            "on the command of", "by the request of",
            "by the determination of", "on the determination of",
            "by the findings of", "on the findings of",
            "pursuant to the direction of",
            "following the direction of",
            "subject to the direction of", "by the oversight of",
            "on the oversight of", "by the supervision of",
            "under the urging of", "under the insistence of",
            "by the insistence of", "under the demand of",
            "by the demand of", "under the invitation of",
            "by the invitation of", "under the suggestion of",
            "by the suggestion of", "under the decision of",
            "at the decision of", "under the ruling of",
            "at the ruling of", "under the judgment of",
            "at the judgment of", "under the verdict of",
            "at the verdict of", "under the licence of",
            "at the licence of", "under the license of",
            "at the license of", "on the licence of",
            "on the license of",
        ))

    def test_trailing_forms_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.TRAILING:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_phrasings_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PHRASINGS:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_conditions_still_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER_TRAILING + self.WEATHER_PHRASINGS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection on the "
            "instructions of the deployment confinement fact."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR23Tests(unittest.TestCase):
    """Ruling 960: prefixed compound limb."""

    FIRST_ELEMENTS = tuple(
        "Every record stands %s-verified before use." % word
        for word in (
            "teak", "oak", "pine", "cedar", "walnut", "opal",
            "turquoise", "hematite", "calcite", "agate", "jasper",
            "amethyst", "luna", "gastro", "nephro", "osteo",
            "ophthalmo",
        ))

    PREFIXES = (
        "techno", "chemo", "chrono", "litho", "phono", "seismo",
        "seleno", "baro", "hygro", "anemo", "ombro", "nepho",
        "chiro", "podo", "rhino", "oto", "ophthalmo", "stetho",
        "myo", "osteo", "arthro", "encephalo", "hepato", "nephro",
        "gastro", "pneumo", "haemo", "hemo", "leuko", "erythro",
        "cyto", "histo", "embryo", "phyto", "myco", "bacterio",
        "viro", "protozoo", "entomo", "ichthyo", "ornitho",
        "herpeto", "malaco", "helmintho",
    )

    COMPOUNDS = tuple(
        "The record stands %s-verified." % prefix
        for prefix in PREFIXES) + tuple(
        "The record stands %s-checked." % prefix
        for prefix in PREFIXES)

    def test_first_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FIRST_ELEMENTS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_prefixes_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMPOUNDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "Every record stands titanium-verified "
            "before use."))
        self.assertFalse(_scan(
            mod, "Every record stands optic-verified before use."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR23Tests(unittest.TestCase):
    """Ruling 961: lexicon limb."""

    RECORD_PROOF = tuple(
        "The records are %s by outside writers." % word
        for word in (
            "dropproof", "pierceproof", "cutproof", "wearproof",
            "peelproof", "breakproof", "dripproof", "decayproof",
            "lionproof", "tigerproof", "elephantproof",
            "horseproof",
        ))

    RECORD_UN = tuple(
        "The records are %s by outside writers." % word
        for word in (
            "unhidden", "unglued", "untaped", "unpinned",
            "unstapled", "unfolded", "unboxed", "uncovered",
        ))

    STORE_PROOF = tuple(
        "The store is %s." % word for word in (
            "roachproof", "amethystproof", "citrineproof",
            "aquamarineproof", "moonstoneproof", "sunstoneproof",
            "labradoriteproof", "hematiteproof", "magnetiteproof",
            "pyriteproof", "malachiteproof", "azuriteproof",
            "turquoiseproof", "lapisproof", "carnelianproof",
            "chalcedonyproof", "acrylicproof", "winterproof",
            "dripproof",
        ))

    def test_record_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORD_PROOF + self.RECORD_UN:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE_PROOF:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are bulletproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are unsealed by outside writers."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanAssertedFixR23Tests(unittest.TestCase):
    """Ruling 962: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "pants", "wheezes", "coughs", "sneezes", "snores",
            "laughs", "giggles", "scoffs", "sneers", "jeers",
            "taunts", "derides", "ridicules", "mimics",
            "whistles", "writes", "prints", "posts", "gestures",
            "nods", "winks", "smiles", "chuckles", "sniffs",
            "hiccups", "burps", "yawns", "blinks", "stares",
            "glances", "peeks", "peers", "protests", "confesses",
            "allows", "urges", "pleads", "begs",
        ))

    MECHANISM_VERBS = tuple(
        "The mechanism %s total integrity of the journal." % verb
        for verb in ("pants", "wheezes", "scoffs"))

    ASSERTED_FOLLOWERS = tuple(
        "Records are %s by outsiders." % word for word in (
            "shackled", "embedded", "lodged", "wedged", "crimped",
            "hitched", "coupled", "pegged", "braced", "buttressed",
            "girded", "banded", "strapped", "caged", "corralled",
            "enclosed", "encircled", "surrounded", "hedged",
            "sheltered", "housed", "garrisoned", "patrolled",
        ))

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL_VERBS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_mechanism_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MECHANISM_VERBS:
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
            mod, "The journal whispers integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal trills integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))


_GOVERNED_CLAIM = ("The seal guarantees protection conditional on "
                   "the deployment confinement fact")


class SealClaimScanMarkerFixR23Tests(unittest.TestCase):
    """Ruling 963: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "no matter the cost", "regardless",
            "through hell and high water", "whatever the weather",
            "in sickness and in health", "for richer or poorer",
            "through joy and sorrow", "for better or worse",
            "in good times and bad", "hell or high water",
            "by hook or by crook", "whatever it takes",
            "to the end of days", "until the end of days",
            "for keeps", "once for all", "endlessly", "perpetually",
            "always", "in any event", "without doubt",
            "unquestionably", "outright", "utterly", "wholly",
            "for perpetuity", "undyingly", "deathlessly",
            "imperishably", "indestructibly", "unchangeably",
            "completely", "entirely", "in full", "by all means",
            "for always", "always and forever",
            "one hundred percent", "totally", "downright",
            "through and through", "root and branch",
            "lock stock and barrel", "bag and baggage",
            "hook line and sinker", "in toto", "in its entirety",
            "without restriction", "unreservedly",
            "unqualifiedly", "flatly", "point blank",
            "unto perpetuity", "henceforth", "from henceforth",
            "from now on", "henceforward", "thenceforth",
            "thenceforward", "ever after", "hereafter",
            "for the duration", "for life", "lifelong",
            "perennially", "interminably", "ceaselessly",
            "incessantly", "unendingly", "unremittingly",
            "immortally", "undiminished", "undiminishing",
            "unabated", "unabating",
        ))

    def test_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MARKERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(mod, self.BASE + "."))
        self.assertFalse(_scan(mod, self.BASE + " now and forever."))
        self.assertFalse(_scan(mod, self.BASE + " for all eternity."))
        self.assertFalse(_scan(mod, self.BASE + " without fail."))


class SealClaimScanNegationFixR23Tests(unittest.TestCase):
    """Ruling 964: negation reading overreach."""

    PROBED = (
        "No record can be altered after writing.",
        "No record is alterable after writing.",
    )

    def test_probed_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED:
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
            mod, "Records are unalterable after writing."))
        self.assertFalse(_scan(
            mod, "The records cannot be altered after writing."))
        self.assertFalse(_scan(
            mod, "No record could ever be altered after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))


if __name__ == "__main__":
    unittest.main()
