"""Fix round 26, Region 1: report seal claim scan pins.

Rulings 1182 to 1188 of the Round 26 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers, the Report and golden span paper findings N1 to N7
and the Confinement paper findings 1 to 8 in their absorbed
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


class SealClaimScanInabilityFixR26Tests(unittest.TestCase):
    """Ruling 1182: inability limb, followers and windows."""

    MODAL_OUTSIDER = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "macerated", "emulsified", "homogenized", "desiccated",
            "vitrified", "pyrolyzed", "irradiated", "microwaved",
            "granulated", "powdered", "charred", "withered",
            "putrefied", "decomposed", "dissected", "pulped",
            "distilled", "brewed", "pickled", "smoked",
        ))

    ASSERTED_OUTSIDER = tuple(
        "Records are %s by outsiders." % word for word in (
            "macerated", "emulsified", "homogenized", "desiccated",
            "vitrified", "pyrolyzed", "irradiated", "microwaved",
            "granulated", "powdered", "charred", "withered",
            "putrefied", "decomposed", "dissected", "pulped",
            "distilled", "brewed", "pickled", "smoked",
        ))

    MODAL_FASTENING = tuple(
        "Records cannot be %s after writing." % word for word in (
            "attached", "affixed", "annexed", "bonded", "adhered",
            "gummed", "epoxied", "concreted", "harnessed", "yoked",
            "linked", "joined", "magnetized", "velcroed",
            "gripped", "tiled",
        ))

    ASSERTED_FASTENING = tuple(
        "Records are %s after writing." % word for word in (
            "attached", "affixed", "annexed", "bonded", "adhered",
            "gummed", "epoxied", "concreted", "harnessed", "yoked",
            "linked", "joined", "magnetized", "velcroed",
            "gripped", "tiled",
        ))

    CONF_MODAL = tuple(
        "Records cannot be %s after writing." % word for word in (
            "dyed", "stained", "bleached", "charred", "toasted",
            "roasted", "baked", "fried", "steamed", "smoked",
            "cured", "pickled", "salted", "seasoned", "flavoured",
            "sculpted", "moulded", "hammered", "pulverised",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "sorrowfully", "despondently", "woefully", "dolefully",
            "lugubriously", "plaintively", "tearfully", "icily",
            "frostily", "heavily", "blankly", "vacantly",
            "faintly", "feebly", "lifelessly", "helplessly",
            "vainly", "fruitlessly", "dejectedly", "morosely",
            "downheartedly", "disheartenedly", "disconsolately",
            "inconsolably", "crestfallenly",
        ))

    WINDOW_PLACES = tuple(
        "Records cannot in any %s be altered after writing."
        % word for word in (
            "apse", "burrow", "warren", "den", "lair", "nest",
            "perch", "pigeonry", "fishery", "hatchery",
            "amphitheatre", "hippodrome", "palaestra", "hammam",
        ))

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.MODAL_OUTSIDER + self.MODAL_FASTENING
                + self.CONF_MODAL):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.ASSERTED_OUTSIDER + self.ASSERTED_FASTENING):
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
            _scan(mod, "Records cannot be gasified by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be liquefied by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be atomized by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot be soldered after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot be laminated after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any scullery be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot grimly be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot solemnly be altered "
            "after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))



class SealClaimScanGoverningFixR26Tests(unittest.TestCase):
    """Ruling 1183: governing condition limb."""

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in (
            "by the auspices of", "by the guardianship of",
            "under the guardianship of", "by the custodianship of",
            "by the trusteeship of", "by the regency of",
            "by the governorship of", "by the premiership of",
            "by the chancellorship of", "by the magistracy of",
            "by the tribunal of", "by the agency of",
            "by the instrumentality of", "by the ministry of",
            "under the ministry of", "by the office of",
            "by the hands of", "by the say of", "under the say of",
            "by the covenant of", "under the covenant of",
            "by the compact of", "under the compact of",
            "by the treaty of", "under the treaty of",
            "by the ordinance of", "under the ordinance of",
            "by the code of", "under the code of",
            "by the canon of", "under the canon of",
            "by the doctrine of", "under the doctrine of",
            "by the tenets of", "under the tenets of",
            "by the principles of", "under the principles of",
            "by the ethics of", "under the ethics of",
            "by the constitution of", "under the constitution of",
            "by the bylaws of", "under the bylaws of",
        ))

    TRAILING = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact holds." % form for form in (
            "so long as", "as long as", "while", "whilst", "once",
            "until", "in case", "in the event",
            "in the event that", "on condition",
            "on the condition", "only while", "only when",
            "only if", "if", "when", "given", "given that",
            "as and when", "if and when", "when and if",
        )) + (
            "The seal guarantees protection with the deployment "
            "confinement fact holding.",
            "The seal guarantees protection pending the "
            "deployment confinement fact holding.",
        )

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather."
        % phrase for phrase in (
            "by the auspices of", "by the guardianship of",
            "under the guardianship of", "by the custodianship of",
            "by the trusteeship of", "by the regency of",
            "by the governorship of", "by the premiership of",
            "by the chancellorship of", "by the magistracy of",
            "by the tribunal of", "by the agency of",
            "by the instrumentality of", "by the ministry of",
            "under the ministry of", "by the office of",
            "by the hands of", "by the say of", "under the say of",
            "by the covenant of", "under the covenant of",
            "by the compact of", "under the compact of",
            "by the treaty of", "under the treaty of",
            "by the ordinance of", "under the ordinance of",
            "by the code of", "under the code of",
            "by the canon of", "under the canon of",
            "by the doctrine of", "under the doctrine of",
            "by the tenets of", "under the tenets of",
            "by the principles of", "under the principles of",
            "by the ethics of", "under the ethics of",
            "by the constitution of", "under the constitution of",
            "by the bylaws of", "under the bylaws of",
        ))

    WEATHER_TRAILING = tuple(
        "The seal guarantees protection %s the weather holds."
        % form for form in (
            "so long as", "as long as", "while", "whilst", "once",
            "until", "in case", "in the event",
            "in the event that", "on condition",
            "on the condition", "only while", "only when",
            "only if", "if", "when", "given", "given that",
            "as and when", "if and when", "when and if",
        )) + (
            "The seal guarantees protection with the weather "
            "holding.",
            "The seal guarantees protection pending the weather "
            "holding.",
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
        for statement in (
                self.WEATHER_PHRASINGS + self.WEATHER_TRAILING):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the mandate "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the leave "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the hand "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection subject to "
            "the deployment confinement fact holding."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))



class SealClaimScanCompoundFixR26Tests(unittest.TestCase):
    """Ruling 1184: prefixed compound limb."""

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in (
            "basswood", "alder", "hornbeam", "hazel", "sycamore",
            "olive", "talc", "dolomite", "chert", "jadeite",
            "nephrite", "corundum", "aquamarine", "moonstone",
            "sunstone", "bloodstone", "carnelian", "chalcedony",
            "sardonyx", "chrysoprase", "horn", "shell", "jet",
        ))

    PREFIXES = (
        "hemato", "patho", "pharmaco", "toxico", "sidero",
        "chalco", "auro", "cupro", "stanno", "plumbo", "sarco",
        "sero", "circum", "peri", "dia", "tetra", "octa",
        "ennea", "anthro", "morpho", "geno", "pheno", "pluvio",
        "anem",
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
            mod, "Every record stands ebony-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands quartz-verified "
            "before use."))
        self.assertFalse(_scan(
            mod, "The record stands ferro-verified."))
        self.assertFalse(_scan(
            mod, "The record stands cardio-checked."))
        self.assertFalse(_scan(
            mod, "The record stands verified."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR26Tests(unittest.TestCase):
    """Ruling 1185: concept root list and un wording limb."""

    UN_WORDS = (
        "unclamped", "untacked", "unpegged", "uncrimped",
        "unmeshed", "unfused", "uncaulked", "ungrouted",
        "unmortared", "unplastered", "untarred", "unenamelled",
        "unroped", "unwired", "unsheathed", "unswathed",
        "unbundled", "uncoupled", "unhitched", "unbelted",
        "unbanded", "uncollared", "unringed", "unhooped",
        "uncaged", "unfenced", "unarmoured", "unarmored",
        "unfortified", "unvaulted", "unentombed", "unenshrined",
        "unencased", "uncemented", "unsoldered", "unattached",
        "unaffixed", "unbonded", "ungummed", "ungilded",
        "unpanelled", "untiled", "unroofed", "unharnessed",
        "unyoked", "unjoined",
    )

    RECORD_UN = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDS)

    STORE_UN = tuple(
        "The store is %s." % word for word in UN_WORDS)

    PROOF_WORDS = (
        "daggerproof", "shrapnelproof", "swordproof",
        "vacuumproof", "xrayproof", "seepproof", "stingproof",
        "leechproof", "gnawproof", "peckproof", "clawproof",
    )

    RECORD_PROOF = tuple(
        "The records are %s by outside writers." % word
        for word in PROOF_WORDS)

    STORE_PROOF = tuple(
        "The store is %s." % word for word in PROOF_WORDS)

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
            mod, "The records are unclasped by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are unclipped by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are bugproof by outside writers."))
        self.assertFalse(_scan(mod, "The store is dustproof."))
        self.assertFalse(_scan(
            mod, "The records are ratproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are quakeproof by outside writers."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))



class SealClaimScanAssertedFixR26Tests(unittest.TestCase):
    """Ruling 1186: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "bangs", "blares", "clangs", "clanks", "crashes",
            "creaks", "drums", "pounds", "thumps", "gazes",
            "squints", "winces", "cringes", "flinches",
            "chortles", "teehees", "disclaims", "dismisses",
            "disowns", "refutes", "rejects", "bobs", "hobbles",
            "limps", "lurches", "quivers", "shakes", "shivers",
            "spins", "staggers", "struts", "sways", "teeters",
            "trembles", "twirls", "whirls", "wobbles",
            "fanfares", "crows", "yowls", "caterwauls", "yaps",
            "bugles", "clarions", "flourishes", "insures",
        ))

    MECHANISM_VERBS = tuple(
        "The mechanism %s total integrity of the journal."
        % verb for verb in (
            "blares", "chortles", "disowns", "spins",
        ))

    CONF_ASSERTED = tuple(
        "Records are %s by outsiders." % word for word in (
            "dyed", "stained", "bleached", "charred", "toasted",
            "roasted", "baked", "fried", "steamed", "smoked",
            "cured", "pickled", "salted", "seasoned", "flavoured",
            "sculpted", "moulded", "hammered", "pulverised",
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

    def test_conf_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONF_ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal honks integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal frowns integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal chirrups integrity for every "
            "reader."))
        self.assertFalse(_scan(
            mod, "The journal twangs integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The mechanism honks total integrity of the "
            "journal."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))


class SealClaimScanMarkerFixR26Tests(unittest.TestCase):
    """Ruling 1187: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "whatever comes", "whatever the cost", "fair or foul",
            "in weal or woe", "weal or woe", "win or lose",
            "live or die", "make or break", "boom or bust",
            "feast or famine", "now or never", "all or nothing",
            "body and soul", "heart and soul",
            "from first to last", "from start to finish",
            "from beginning to end", "alpha and omega",
            "once and always", "at all places", "in all places",
            "in all conditions", "under every condition",
            "without hesitation", "in aeternum",
            "saecula saeculorum", "sine fine", "sine die",
            "beyond eternity", "across eternity", "outside time",
            "beyond time", "against all odds",
            "come wind or weather", "wind or weather",
            "storm or calm", "in storm or calm", "in peace or war",
            "in war or peace", "in life or death", "living or dead",
            "dead or alive", "alive or dead",
            "till the end of days", "through all time",
            "till eternity", "until eternity",
            "to the ends of the earth", "without respite",
            "without pause", "without interruption",
            "without a break", "without cessation",
            "without surcease", "without reprieve",
            "around the clock", "day and night", "night and day",
            "at all hours", "for all seasons", "in all seasons",
            "without letup", "nonstop", "semper", "without mercy",
            "without pity",
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
        self.assertFalse(_scan(mod, self.BASE + " come what may."))
        self.assertFalse(_scan(
            mod, self.BASE + " by hook or crook."))



class SealClaimScanNegationFixR26Tests(unittest.TestCase):
    """Ruling 1188: negation narrowing limb, No opening form."""

    PROBED_IS = tuple(
        "No record is %s after writing." % word for word in (
            "anchored", "archived", "attackproof", "bombproof",
            "branded", "bugged", "bulletproof", "burglarproof",
            "carried", "catalogued", "childproof", "chronicled",
            "circulated", "circumvented", "cloned", "compromised",
            "controlled", "conveyed", "cosigned", "countersigned",
            "decrypted", "dictated", "dispatched", "disseminated",
            "distributed", "diverted", "doctored", "drillproof",
            "dustproof", "emailed", "embezzled", "embossed",
            "engraved", "entryproof", "errorless", "etched",
            "exfiltrated", "exposed", "fabricated", "faxed",
            "filched", "filmed", "fireproof", "foolproof",
            "fraudproof", "hallmarked", "harvested", "immaculate",
            "impassable", "impersonated", "impervious", "imprinted",
            "inalterable", "indissoluble", "inscribed",
            "intrusionproof", "invulnerable", "isolated", "lifted",
            "logged", "looted", "manipulated", "memorised",
            "mirrored", "notarised", "notarized", "overheard",
            "paraphrased", "photocopied", "photographed",
            "pickproof", "pilfered", "pinched", "postmarked",
            "pristine", "proofread", "published", "purged",
            "purloined", "quarantined", "quoted", "reconstructed",
            "recreated", "regenerated", "reissued", "relayed",
            "resealed", "restricted", "retyped", "riskless",
            "rustproof", "scraped", "segregated", "shatterproof",
            "siphoned", "smudgeproof", "smuggled", "snatched",
            "soundproof", "spotless", "streamed", "swiped",
            "synced", "taped", "televised", "theftproof",
            "thiefproof", "transcribed", "unassailable",
            "unchanging", "uncracked", "unhackable", "unmarked",
            "unopened", "unpicked", "unsealed", "unspoofed",
            "uploaded", "vandalproof", "watermarked", "waterproof",
            "weatherproof", "wiped", "wiretapped", "xeroxed",
            "redactable", "expungeable", "extinguishable",
            "shatterable", "burnable", "shreddable", "defaceable",
            "vandalizable", "sabotageable",
        ))

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word for word in (
            "anchored", "archived", "attackproof", "bombproof",
            "branded", "bugged", "bulletproof", "burglarproof",
            "carried", "catalogued", "childproof", "chronicled",
            "redacted", "expunged", "obliterated", "annihilated",
            "extinguished", "shattered", "burned", "shredded",
            "defaced", "vandalized", "sabotaged",
        ))

    ASSERTED_ANALOGUES = tuple(
        "The record is %s after writing." % word for word in (
            "redactable", "expungeable", "extinguishable",
            "shatterable", "burnable", "shreddable", "defaceable",
            "vandalizable", "sabotageable",
        )) + tuple(
            "Records are %s after writing." % word for word in (
                "redacted", "expunged", "obliterated",
                "annihilated", "extinguished", "shattered",
                "burned", "shredded", "defaced", "vandalized",
                "sabotaged",
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
            mod, "No record is alterable after writing."))
        self.assertFalse(_scan(
            mod, "No record is deletable after writing."))
        self.assertFalse(_scan(
            mod, "No record is erasable after writing."))
        self.assertFalse(_scan(
            mod, "No record is crackproof after writing."))
        self.assertFalse(_scan(
            mod, "No record can be crackproof after writing."))
        self.assertFalse(_scan(
            mod, "No record is impenetrable after writing."))
        self.assertFalse(_scan(
            mod, "Records are unalterable after writing."))
        self.assertFalse(_scan(
            mod, "The records cannot be altered after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


if __name__ == "__main__":
    unittest.main()
