"""Fix round 24, Region 1: report seal claim scan pins.

Rulings 1019 to 1025 of the Round 24 triage. Each class pins
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


class SealClaimScanInabilityFixR24Tests(unittest.TestCase):
    """Ruling 1019: inability limb, followers and windows."""

    MODAL_OUTSIDER = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "evaporated", "cremated", "shattered", "boiled",
            "sublimed", "calcined", "carbonised", "carbonized",
            "petrified", "fossilised", "fossilized", "mummified",
            "embalmed",
        ))

    MODAL_FASTENING = tuple(
        "Records cannot be %s after writing." % word for word in (
            "fused", "plastered", "mortared", "grouted", "caulked",
            "tarred", "enameled", "chromed", "galvanised",
            "galvanized", "anodised", "anodized", "silvered",
            "nickeled", "bronzed", "coppered",
            "roped", "wired", "sheathed", "swathed", "bundled",
            "interlocked", "meshed",
        ))

    ASSERTED_AFTER = tuple(
        "Records are %s after writing." % word for word in (
            "fused", "plastered", "mortared", "grouted", "caulked",
            "tarred", "enameled", "chromed", "galvanised",
            "galvanized", "anodised", "anodized", "silvered",
            "nickeled", "bronzed", "coppered",
        ))

    ASSERTED_OUTSIDER = tuple(
        "Records are %s by outsiders." % word for word in (
            "roped", "wired", "fused", "caulked", "grouted",
            "mortared", "tarred", "sheathed", "swathed", "bundled",
            "interlocked", "meshed",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "mournfully", "casually", "absentmindedly",
            "absent-mindedly", "gloomily", "wearily", "wildly",
            "equably", "stoically", "phlegmatically", "purposely",
            "unhurriedly", "leisurely", "languidly", "drearily",
            "dully", "tediously", "ponderously", "laboriously",
            "painstakingly", "meticulously", "scrupulously",
            "punctiliously", "fastidiously", "rigidly",
            "inflexibly", "unyieldingly", "unbendingly",
            "adamantly", "unwaveringly", "unswervingly",
            "devotedly", "loyally", "dutifully", "obediently",
            "submissively",
        ))

    WINDOW_PLACES = tuple(
        "Records cannot in any %s be altered after writing."
        % word for word in (
            "scullery", "mezzanine", "byre", "sty", "roost",
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
            mod, "Records cannot be exhumed by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot in any sanctum be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot solemnly be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot be dissolved by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanGoverningFixR24Tests(unittest.TestCase):
    """Ruling 1020: governing condition limb."""

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in (
            "under the leave of", "on the leave of",
            "under the behest of", "by the mandate of",
            "on the mandate of", "under the mandate of",
            "by the decree of", "on the decree of",
            "under the decree of", "by the edict of",
            "on the edict of", "under the edict of",
            "by the fiat of", "under the fiat of",
            "by the sanction of", "by the assent of",
            "with the assent of", "under the assent of",
            "by the concurrence of", "with the concurrence of",
            "by the acquiescence of", "under the order of",
            "under the word of", "by the charge of",
            "by the commission of", "by the charter of",
            "under the charter of", "by the bidding of",
            "under the bidding of", "by the summons of",
            "at the summons of", "by the instigation of",
            "at the instigation of", "on the instigation of",
            "under the instigation of", "by the urging of",
            "by the advice of", "at the advice of",
            "under the advice of", "at the mandate of",
            "at the blessing of", "by the endorsement of",
            "at the endorsement of", "under the endorsement of",
            "following the order of", "pursuant to the order of",
            "by the writ of", "under the writ of",
            "at the authority of", "at the will of",
            "by the wish of", "by the desire of",
            "by the pleasure of", "by the call of",
            "by the nomination of", "by the appointment of",
            "by the election of", "by the selection of",
            "by the choice of", "by the designation of",
            "by the assignment of",
        ))

    TRAILING = (
        "The seal guarantees protection once the deployment "
        "confinement fact holds.",
        "The seal guarantees protection until the deployment "
        "confinement fact holds.",
        "The seal guarantees protection unless the deployment "
        "confinement fact fails.",
        "The seal guarantees protection if and only if the "
        "deployment confinement fact holds.",
        "The seal guarantees protection on the condition the "
        "deployment confinement fact holds.",
    )

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather." % phrase
        for phrase in (
            "under the leave of", "on the leave of",
            "under the behest of", "by the mandate of",
            "on the mandate of", "under the mandate of",
            "by the decree of", "on the decree of",
            "under the decree of", "by the edict of",
            "on the edict of", "under the edict of",
            "by the fiat of", "under the fiat of",
            "by the sanction of", "by the assent of",
            "with the assent of", "under the assent of",
            "by the concurrence of", "with the concurrence of",
            "by the acquiescence of", "under the order of",
            "under the word of", "by the charge of",
            "by the commission of", "by the charter of",
            "under the charter of", "by the bidding of",
            "under the bidding of", "by the summons of",
            "at the summons of", "by the instigation of",
            "at the instigation of", "on the instigation of",
            "under the instigation of", "by the urging of",
            "by the advice of", "at the advice of",
            "under the advice of", "at the mandate of",
            "at the blessing of", "by the endorsement of",
            "at the endorsement of", "under the endorsement of",
            "following the order of", "pursuant to the order of",
            "by the writ of", "under the writ of",
            "at the authority of", "at the will of",
            "by the wish of", "by the desire of",
            "by the pleasure of", "by the call of",
            "by the nomination of", "by the appointment of",
            "by the election of", "by the selection of",
            "by the choice of", "by the designation of",
            "by the assignment of",
        ))

    WEATHER_TRAILING = (
        "The seal guarantees protection once the weather holds.",
        "The seal guarantees protection until the weather holds.",
        "The seal guarantees protection unless the weather fails.",
        "The seal guarantees protection if and only if the "
        "weather holds.",
        "The seal guarantees protection on the condition the "
        "weather holds.",
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
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the leave of "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection as long as the "
            "deployment confinement fact holds."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR24Tests(unittest.TestCase):
    """Ruling 1021: prefixed compound limb."""

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in (
            "balsa", "rosewood", "elm", "ash", "birch", "cherry",
            "hickory", "poplar", "spruce", "willow", "beech",
            "chestnut", "sandalwood", "ironwood", "lignum",
            "pumice", "shale", "travertine", "alabaster", "gypsum",
            "mica", "feldspar", "beryl", "spinel", "zircon",
            "garnet", "peridot", "tourmaline",
            "chromium", "manganese", "palladium", "iridium",
            "osmium", "rhodium", "sulfur", "boron", "silicon",
            "zirconium", "niobium", "tantalum", "rhenium",
            "lutetium", "hafnium", "thallium", "bismuth",
            "polonium", "radium", "uranium", "plutonium",
            "thorium", "lithium", "sodium", "potassium",
            "calcium", "barium", "strontium", "gallium", "indium",
            "tin", "antimony", "tellurium", "iodine", "bromine",
            "chlorine", "fluorine",
        ))

    PREFIX_VERIFIED = tuple(
        "The record stands %s-verified." % prefix for prefix in (
            "vibro", "turbo", "gyro", "dendro", "glacio",
            "paleonto", "galvano",
            "ferro", "glyco", "lipo", "thio", "telluro",
            "arseno", "boro", "silico", "titano", "zircono",
            "tantalo", "rheno", "platino", "argento", "zinco",
            "chloro", "xantho", "cyano", "nitro", "amino",
        ))

    PREFIX_CHECKED = tuple(
        "The record stands %s-checked." % prefix for prefix in (
            "vibro", "turbo", "gyro", "dendro", "glacio",
            "paleonto", "galvano",
            "ferro", "glyco", "lipo", "thio", "telluro",
            "arseno", "boro", "silico", "titano", "zircono",
            "tantalo", "rheno", "platino", "argento", "zinco",
            "chloro", "xantho", "cyano", "nitro", "amino",
        ))

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
            mod, "The record stands techno-verified."))
        self.assertFalse(_scan(
            mod, "The record stands verified."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR24Tests(unittest.TestCase):
    """Ruling 1022: lexicon limb."""

    RECORD_PROOF = tuple(
        "The records are %s by outside writers." % word
        for word in (
            "grimeproof", "goatproof", "cowproof", "pigproof",
            "chickenproof", "coyoteproof",
        ))

    RECORD_UN = tuple(
        "The records are %s by outside writers." % word
        for word in (
            "unclasped", "unbuckled", "unbuttoned", "unhooked",
            "untied", "unknotted", "unlaced", "unrolled",
            "unfurled", "unsewn", "unriveted", "unscrewed",
            "unnailed", "unhinged", "uncorked", "unplugged",
        ))

    STORE_UN = tuple(
        "The store is %s." % word for word in (
            "unclasped", "unbuckled", "unbuttoned", "unhooked",
            "untied", "unknotted", "unlaced", "unrolled",
            "unfurled", "unsewn", "unriveted", "unscrewed",
            "unnailed", "unhinged", "uncorked", "unplugged",
        ))

    RECORD_CONF = tuple(
        "The records are %s by outside writers." % word
        for word in (
            "freezeproof", "verminproof", "midgeproof",
        ))

    STORE_CONF = tuple(
        "The store is %s." % word for word in (
            "freezeproof", "verminproof", "midgeproof",
            "caterpillarproof",
        ))

    def test_record_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.RECORD_PROOF + self.RECORD_UN + self.RECORD_CONF):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE_UN + self.STORE_CONF:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are bulletproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are roachproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The store is dustproof."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanAssertedFixR24Tests(unittest.TestCase):
    """Ruling 1023: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "snuffles", "gurgles", "jabbers", "prattles",
            "smirks", "grins", "frowns", "scowls", "grimaces",
            "pouts", "sulks", "broods",
            "dozes", "snoozes", "slumbers", "drowses", "naps",
            "reclines", "lounges", "lingers", "dawdles",
            "hesitates", "falters", "stumbles",
            "scribbles", "scrawls", "doodles", "paints", "stamps",
            "types",
            "mocks", "belittles", "disparages", "denigrates",
            "decries", "reviles", "vilifies", "maligns", "insults",
            "offends", "affronts", "snubs", "slights", "disdains",
            "scorns", "despises", "detests", "loathes", "abhors",
            "execrates", "anathematizes", "damns", "curses",
            "blasphemes", "profanes",
            "lampoon",
            "chirrups", "oinks", "gibbers", "shrieks", "twitters",
            "yammers", "witters", "rambles", "whimpers",
        ))

    MECHANISM_VERBS = tuple(
        "The mechanism %s total integrity of the journal." % verb
        for verb in (
            "snuffles", "gurgles", "jabbers", "prattles",
            "smirks", "grins",
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

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal whistles integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal pants integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))


_GOVERNED_CLAIM = ("The seal guarantees protection conditional on "
                   "the deployment confinement fact")


class SealClaimScanMarkerFixR24Tests(unittest.TestCase):
    """Ruling 1024: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "at any price", "in all weathers",
            "through fire and water", "sink or swim",
            "till doomsday", "until doomsday", "positively",
            "definitely", "certainly", "undoubtedly",
            "beyond all doubt", "to perpetuity",
            "from this day forward", "immutably", "irreversibly",
            "definitively", "decisively", "emphatically",
            "through sleet or snow", "in fair weather or foul",
            "for aye", "till the cows come home",
            "until the cows come home", "till kingdom come",
            "until kingdom come", "to the last", "to the very end",
            "through to the end", "all the way",
            "every inch of the way", "no doubt",
            "beyond a shadow of a doubt", "past doubt",
            "past question", "incontestably", "indisputably",
            "irrefutably", "undeniably", "unmistakably",
            "patently", "manifestly", "decidedly",
            "by fair means or foul", "by fire or sword",
            "with fire and sword", "through flood and fire",
            "cost what it may", "to the last breath",
            "to all eternity", "throughout eternity",
            "for all the days", "all the days of my life",
            "while the world stands", "as long as the world stands",
            "till the stars fall", "until the stars fall",
            "till heaven falls", "in saecula saeculorum",
            "per omnia saecula", "from this day forth",
            "unfailingly", "invariably", "sempiternally",
            "in perpetuum", "beyond recall", "beyond remedy",
            "limitlessly", "boundlessly", "over and over",
            "again and again", "time and again", "time after time",
            "day after day", "year after year", "on and on",
            "onwards and upwards", "to the bitter end",
            "until the very end", "till the very end",
            "to the end of the line", "down to the wire",
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
        self.assertFalse(_scan(mod, self.BASE + " for perpetuity."))
        self.assertFalse(_scan(mod, self.BASE + " without fail."))


class SealClaimScanNegationFixR24Tests(unittest.TestCase):
    """Ruling 1025: negation narrowing reaching beyond alter."""

    PROBED_IS = tuple(
        "No record is %s after writing." % word for word in (
            "changeable", "modifiable", "editable", "rewritable",
            "tamperable", "sealable", "accessible", "reachable",
            "leakable", "unchangeable", "immutable", "inviolable",
            "airtight", "hermetic", "secure", "locked", "confined",
            "contained", "protected", "shielded", "verified",
            "signed", "deletable", "erasable", "breachable",
            "penetrable",
        ))

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word for word in (
            "changeable", "rewritten", "changed", "modified",
            "deleted", "erased",
        ))

    def test_probed_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED_IS + self.PROBED_CAN_BE:
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
            mod, "No record can be altered after writing."))
        self.assertFalse(_scan(
            mod, "Records are unalterable after writing."))
        self.assertFalse(_scan(
            mod, "No record is impenetrable after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


if __name__ == "__main__":
    unittest.main()
