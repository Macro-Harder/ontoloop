"""Fix round 25, Region 1: report seal claim scan pins.

Rulings 1093 to 1099 of the Round 25 triage. Each class pins
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


_GOVERNED_CLAIM = ("The seal guarantees protection conditional on "
                   "the deployment confinement fact")


class SealClaimScanInabilityFixR25Tests(unittest.TestCase):
    """Ruling 1093: inability limb, followers and windows."""

    MODAL_OUTSIDER = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "gasified", "atomised", "extinguished", "drowned",
            "mulched", "minced", "mashed", "pureed",
        ))

    ASSERTED_OUTSIDER = tuple(
        "Records are %s by outsiders." % word for word in (
            "gasified", "atomised", "extinguished", "drowned",
            "mulched", "minced", "mashed", "pureed",
            "laced", "bricked", "boarded",
        ))

    MODAL_FASTENING = tuple(
        "Records cannot be %s after writing." % word for word in (
            "brazed", "manacled", "fettered", "swaddled", "plated",
            "coated", "glazed", "laced", "bricked", "boarded",
        ))

    ASSERTED_AFTER = tuple(
        "Records are %s after writing." % word for word in (
            "brazed", "manacled", "fettered", "swaddled", "plated",
            "coated", "glazed",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "cheerlessly", "somberly", "glumly", "ruefully",
            "wistfully", "pensively", "moodily", "sulkily",
            "grumpily", "crossly", "brusquely", "curtly",
            "peaceably", "restlessly", "fitfully", "drowsily",
            "sleepily", "woodenly", "impassively", "apathetically",
            "indifferently", "lethargically", "torpidly", "inertly",
            "passively", "resignedly", "fatalistically",
        ))

    WINDOW_PLACES = tuple(
        "Records cannot in any %s be altered after writing."
        % word for word in (
            "dormer", "cupola",
        ))

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_OUTSIDER + self.MODAL_FASTENING:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_AFTER + self.ASSERTED_OUTSIDER:
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
            mod, "Records cannot be fused after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any scullery be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot solemnly be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot mournfully be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot be evaporated by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanGoverningFixR25Tests(unittest.TestCase):
    """Ruling 1094: governing condition limb."""

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in (
            "at the say-so of", "by the dictate of",
            "under the dictate of", "by the guidance of",
            "by the stewardship of", "under the stewardship of",
            "by the presidency of", "by the chairmanship of",
            "by the power of", "by the right of",
            "by the grant of", "under the grant of",
            "by the permit of", "under the permit of",
            "by the agreement of", "with the agreement of",
            "under the agreement of", "by the leadership of",
            "by the management of", "by the control of",
            "by the governance of", "under the governance of",
            "by the administration of",
            "under the administration of",
            "by the regulation of", "under the regulation of",
            "by the law of", "under the law of",
            "by the standards of", "by the provisions of",
        ))

    TRAILING = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact holds." % form for form in (
            "whenever", "assuming", "granted", "supposing",
            "insofar as", "so far as", "to the extent", "where",
            "whereas",
        )) + (
            "The seal guarantees protection before the "
            "deployment confinement fact fails.",
        )

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather."
        % phrase for phrase in (
            "at the say-so of", "by the dictate of",
            "under the dictate of", "by the guidance of",
            "by the stewardship of", "under the stewardship of",
            "by the presidency of", "by the chairmanship of",
            "by the power of", "by the right of",
            "by the grant of", "under the grant of",
            "by the permit of", "under the permit of",
            "by the agreement of", "with the agreement of",
            "under the agreement of", "by the leadership of",
            "by the management of", "by the control of",
            "by the governance of", "under the governance of",
            "by the administration of",
            "under the administration of",
            "by the regulation of", "under the regulation of",
            "by the law of", "under the law of",
            "by the standards of", "by the provisions of",
        ))

    WEATHER_TRAILING = tuple(
        "The seal guarantees protection %s the weather holds."
        % form for form in (
            "whenever", "assuming", "granted", "supposing",
            "insofar as", "so far as", "to the extent", "where",
            "whereas",
        )) + (
            "The seal guarantees protection before the weather "
            "fails.",
        )

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
        for statement in self.WEATHER_PHRASINGS + self.WEATHER_TRAILING:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the leave "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the mandate "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection once the "
            "deployment confinement fact holds."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR25Tests(unittest.TestCase):
    """Ruling 1095: prefixed compound limb."""

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in (
            "redwood", "sequoia", "cypress", "juniper", "larch",
            "fir", "yew", "boxwood", "topaz", "citrine", "lapis",
            "malachite", "magnetite", "pyrite", "azurite", "mercury",
        ))

    PREFIXES = (
        "petro", "necro",
        "acousto", "gravito", "nucleo", "isotopo", "stereo",
        "holo", "endoscopo", "laparo", "broncho", "colono",
        "cysto", "hystero", "laryngo", "naso", "otolaryngo",
        "pharyngo", "procto", "uretero", "vaso", "angio",
        "arterio", "phlebo", "lympho", "myelo", "chondro",
        "syndesmo",
    )

    PREFIX_VERIFIED = tuple(
        "The record stands %s-verified." % prefix
        for prefix in PREFIXES)

    PREFIX_CHECKED = tuple(
        "The record stands %s-checked." % prefix
        for prefix in PREFIXES)

    def test_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ELEMENTS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_prefixes_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIX_VERIFIED + self.PREFIX_CHECKED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "Every record stands teak-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands balsa-verified before use."))
        self.assertFalse(_scan(
            mod, "The record stands ferro-verified."))
        self.assertFalse(_scan(
            mod, "The record stands vibro-checked."))
        self.assertFalse(_scan(
            mod, "The record stands verified."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR25Tests(unittest.TestCase):
    """Ruling 1096: lexicon and un wording limb."""

    UN_WORDS = (
        "unclipped", "unwelded", "unbarred", "unpadlocked",
        "unchained", "unleashed", "unmoored", "unanchored",
        "untethered", "unshackled", "unfettered", "unmanacled",
    )

    RECORD_UN = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDS)

    STORE_UN = tuple(
        "The store is %s." % word for word in UN_WORDS)

    RECORD_PROOF = tuple(
        "The records are %s by outside writers." % word
        for word in ("bugproof", "riotproof", "warproof"))

    STORE_PROOF = tuple(
        "The store is %s." % word
        for word in ("bugproof", "riotproof", "warproof"))

    def test_record_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORD_UN + self.RECORD_PROOF:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE_UN + self.STORE_PROOF:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are bulletproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are freezeproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are unclasped by outside writers."))
        self.assertFalse(_scan(mod, "The store is dustproof."))
        self.assertFalse(_scan(
            mod, "The records are ratproof by outside writers."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanAssertedFixR25Tests(unittest.TestCase):
    """Ruling 1097: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "twangs", "puffs", "blows", "belches", "glares",
            "gapes", "leers", "titters", "snickers", "guffaws",
            "flouts", "spurns", "rebuffs", "repudiates",
            "disavows", "renounces", "abjures", "forswears",
            "grumbles", "howls", "sniffles", "thunders",
            "rumbles", "clatters", "rattles", "clinks", "chimes",
            "tolls", "peals", "tinkles", "jingles", "jangles",
            "strums", "plucks", "bows", "toots", "beeps", "bleeps",
        ))

    MECHANISM_VERBS = (
        "The mechanism twangs total integrity of the journal.",
    )

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

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal whistles integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal chirrups integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal jabbers integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))


class SealClaimScanMarkerFixR25Tests(unittest.TestCase):
    """Ruling 1098: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "by hook or crook", "willy-nilly", "like it or not",
            "ready or not", "believe it or not",
            "for richer for poorer", "until death", "to the grave",
            "from the cradle to the grave", "world without end",
            "ad infinitum", "ad nauseam", "without end",
            "without limit", "without condition",
            "no strings attached", "full stop", "end of story",
            "end of discussion", "case closed", "once for all",
            "first and last", "now and for all time",
            "for all future time", "unto the ages of ages",
            "for everlasting",
            "to eternity", "in eternity", "through all eternity",
            "amen", "without ceasing", "unceasingly",
            "for all ages", "through all ages", "till time ends",
            "until time ends", "anyhow", "anyway", "irrespective",
            "thoroughly", "unambiguously", "unequivocally",
            "explicitly", "evidently",
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
        self.assertFalse(_scan(
            mod, self.BASE + " come hell or high water."))


class SealClaimScanNegationFixR25Tests(unittest.TestCase):
    """Ruling 1099: negation narrowing overreach limb."""

    PROBED_IS = tuple(
        "No record is %s after writing." % word for word in (
            "removable", "copyable", "readable", "viewable",
            "exportable", "shareable", "printable", "downloadable",
            "interceptable", "forgeable", "falsifiable", "spoofable",
            "hackable", "crackable", "breakable", "openable",
            "destroyable", "corruptible", "overwritable",
            "replaceable", "duplicable", "extractable",
            "transmittable", "movable", "replayable", "guarded",
            "walled", "barred", "fortified", "audited", "inspected",
            "examined", "reviewed", "screened", "vetted", "ratified",
            "accredited", "endorsed", "attested", "certified",
            "authenticated", "validated", "confirmed", "checked",
            "stamped", "registered", "enrolled", "initialled",
            "witnessed", "sworn", "everlasting", "eternal",
            "perpetual", "timeless", "indestructible",
            "imperishable", "inaccessible", "untouchable",
            "unbreakable", "unforgeable", "incorruptible",
            "indelible", "inerasable", "irrevocable", "ironclad",
            "sacrosanct", "failsafe", "perfect",
            "counterfeitable", "reproducible", "unlockable",
            "unfastenable", "transferable", "importable",
            "traceable", "trackable", "observable", "searchable",
            "indexable", "recoverable", "restorable",
        ))

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word for word in (
            "removable", "copyable", "readable", "viewable",
            "exportable", "shareable", "printable", "downloadable",
            "interceptable", "forgeable", "falsifiable", "spoofable",
            "copied", "duplicated", "reproduced", "forged",
            "faked", "counterfeited", "opened", "unlocked",
            "removed", "extracted", "read", "overwritten",
            "transferred", "moved", "exported", "shared",
            "recovered", "restored", "hacked", "cracked",
            "stolen", "taken", "seized", "intercepted",
        ))

    PROBED_TENSE = (
        "No record was altered after writing.",
        "No record has been altered after writing.",
        "No record had been altered after writing.",
    )

    ASSERTED_ANALOGUES = tuple(
        "The record is %s after writing." % word for word in (
            "removable", "forgeable", "readable",
        )) + (
            "Records are copied after writing.",
            "Records are altered after writing.",
        )

    def test_probed_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.PROBED_IS + self.PROBED_CAN_BE
                + self.PROBED_TENSE):
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
            mod, "No record is alterable after writing."))
        self.assertFalse(_scan(
            mod, "No record is changeable after writing."))
        self.assertFalse(_scan(
            mod, "No record can be altered after writing."))
        self.assertFalse(_scan(
            mod, "Records are unalterable after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


if __name__ == "__main__":
    unittest.main()
