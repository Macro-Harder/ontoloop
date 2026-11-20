"""Fix round 36, Region 1: report seal claim scan pins.

Rulings 2292 to 2299 of the Round 36 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R36-REPG-1 to 8 and the Confinement paper findings
S15-R36-CONF-1 to 10 in their absorbed limbs, on the
templates those papers state. A form probed in both
raising papers on the one limb stands counted once, in
the form of the triage merges. Divided forms standing
at pole on the governing base in one construction stand
pinned in the controls of their class in that
construction.
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

class SealClaimScanInabilityFixR36Tests(unittest.TestCase):
    """Ruling 2292: inability limb, followers and windows."""

    FOLLOWERS_BOTH = dict.fromkeys((
        "turned", "ground", "sawn",
        "rolled", "peened", "sherardized",
        "calorized", "aluminized", "siliconized",
        "boronized", "titanized", "vanadized",
        "zirconized", "tantalized", "niobized",
        "rhenized", "iridized", "palladized",
        "rhodinized", "ruthenized", "osmiridized",
        "patinated", "planished", "gessoed",
        "parged", "punched", "rasped",
        "reeded", "ridged", "shingled",
        "smoothed", "spackled", "stuccoed",
        "troweled", "washed", "whitewashed",
    ))

    MODAL_ONLY = dict.fromkeys((
        "stenciled",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "jovially", "judiciously", "justifiably",
        "largely", "lastingly", "laughably",
        "lavishly", "lawlessly", "legibly",
        "lengthily", "leniently", "limply",
        "lingeringly", "literally", "lively",
        "loathingly", "loftily", "logically",
        "lonelily", "loosely", "lovingly",
        "lucidly", "luckily", "luminously",
        "luridly", "lustily", "luxuriously",
        "lyingly", "magically", "maidenly",
        "majestically", "maladroitly", "manageably",
        "manfully", "maniacally", "manly",
        "marginally", "irksomely", "jauntily",
        "laterally", "liberally", "likely",
        "linearly", "lushly", "lustfully",
        "luxuriantly", "lyrically", "magnanimously",
        "martially", "marvelously", "massively",
        "masterfully", "materially", "maternally",
        "mathematically", "maturely", "maximally",
        "meagerly", "meaningfully", "meaninglessly",
        "medically", "medicinally", "meditatively",
        "melodically", "melodiously", "memorably",
        "mercifully", "merrily", "messily",
        "metabolically", "metallically", "metaphorically",
        "microscopically", "militarily", "militantly",
        "mindfully", "mindlessly", "minimally",
        "minutely", "miraculously", "mirthfully",
        "misleadingly", "narrowly", "nasally",
        "nationally", "natively", "naturally",
        "nautically", "nearly", "neatly",
        "nebulously", "necessarily", "needlessly",
        "negatively", "newly", "nicely",
        "nightly", "nimbly", "nocturnally",
        "noiselessly", "nominally", "nonlinearly",
        "nonverbally", "normatively", "nosily",
        "notably", "notoriously", "nourishingly",
        "numerically", "numinously", "nuptially",
        "nutritiously", "nutritively", "nuttily",
        "objectionably", "objectively", "obligately",
        "obliquely", "obliviously", "oblongly",
        "obnoxiously", "obscenely", "obscurely",
        "obsequiously", "obsessively", "obstructively",
        "occupationally", "oceanically", "odiously",
        "odourlessly", "omnipotently", "omnisciently",
        "onerously", "ongoingly", "ontologically",
        "operably", "operantly", "operationally",
        "operatically", "operatively", "opinionatedly",
        "opportunely", "oppositely", "oppressively",
        "optimally", "optionally", "opulently",
        "orally", "oratorically", "orbitally",
        "orderly", "ordinarily", "organically",
        "orientally", "originally", "ornately",
        "ornithologically", "orographically", "orotundly",
        "orthodoxly", "orthogonally", "orthographically",
    ))

    MODAL = tuple(
        "Records cannot be %s by outsiders." % word
        for word in FOLLOWERS_BOTH) + tuple(
        "Records cannot be %s after writing." % word
        for word in MODAL_ONLY) + tuple(
        "Records cannot be %s after writing." % word
        for word in FOLLOWERS_BOTH)

    ASSERTED = tuple(
        "Records are %s by outsiders." % word
        for word in FOLLOWERS_BOTH)

    WINDOWS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in WINDOW_WORDS)

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
        for statement in self.WINDOWS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be electroplated by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot truculently be altered "
            "after writing."))
        self.assertFalse(
            _scan(mod, "Records cannot be quilted by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanGoverningFixR36Tests(unittest.TestCase):
    """Ruling 2293: governing condition limb."""

    PHRASINGS = dict.fromkeys((
        "by the diadem of", "by the coronet of",
        "by the laurel of", "by the ledger of",
        "by the register of", "by the tablet of",
        "by the signet stone of", "by the wax of",
        "by the ribbon of", "by the cord of",
        "by the knot of", "by the key of",
        "by the bolt of", "by the bar of",
        "under the diadem of", "under the coronet of",
        "under the laurel of", "under the ledger of",
        "under the register of", "under the tablet of",
        "under the signet stone of", "under the wax of",
        "under the ribbon of", "under the cord of",
        "under the knot of", "under the key of",
        "under the bolt of", "under the bar of",
        "by the crozier of", "by the mitre of",
        "by the tiara of", "by the seal ring of",
        "by the lock of", "by the standard of",
        "by the ensign of", "by the justification of",
        "by the juxtaposition of", "by the kindling of",
        "by the labeling of", "by the lamentation of",
        "by the laceration of", "by the magnification of",
        "by the magnetization of", "by the maintenance of",
        "by the majority of", "by the making of",
        "by the manifestation of", "by the manipulation of",
        "by the manufacture of", "by the mapping of",
        "by the marginalization of", "by the marking of",
        "by the marriage of", "by the masking of",
        "by the matching of", "by the materialization of",
        "by the maturation of", "by the maximization of",
        "by the measurement of", "by the mediation of",
        "by the meditation of", "by the membership of",
        "by the memorization of", "by the mention of",
        "by the merging of", "by the merit of",
        "by the migration of", "by the mimicry of",
        "by the minimization of", "by the mining of",
        "by the minting of", "by the mirroring of",
        "by the misapplication of", "by the misappropriation of",
        "by the miscalculation of", "by the misclassification of",
        "by the misconception of", "by the misconduct of",
        "by the misdirection of", "by the misinterpretation of",
        "by the misjudgment of", "by the mismanagement of",
        "by the misplacement of", "by the mispricing of",
        "by the misreading of", "by the misrepresentation of",
        "by the misstatement of", "by the misuse of",
        "by the mitigation of", "by the mixing of",
        "by the mobilization of", "by the modeling of",
        "by the moderation of", "by the modification of",
        "by the modulation of", "by the molding of",
        "by the monitoring of", "by the monopoly of",
        "by the monotony of", "by the moralization of",
        "by the morphology of", "by the mortality of",
        "by the mortification of", "by the mortising of",
        "by the motivation of", "by the mounting of",
        "by the mourning of", "by the movement of",
        "by the muddling of", "by the multiplication of",
        "by the munificence of", "by the murder of",
        "by the mutation of", "by the mutilation of",
        "by the muttering of", "by the mystification of",
        "by the mythology of", "by the narration of",
        "by the nationalization of", "by the naturalization of",
        "by the navigation of", "by the necessity of",
        "by the negation of", "by the negotiation of",
        "by the neutralization of", "by the normalization of",
        "by the notation of", "by the nourishment of",
        "by the nucleation of", "by the nullification of",
        "by the numbering of", "by the nurture of",
        "by the obedience of", "by the objection of",
        "by the observation of", "by the obstruction of",
        "by the obtainment of", "by the occupation of",
        "by the occurrence of", "by the offering of",
        "by the offsetting of", "by the omission of",
        "by the opening of", "by the operation of",
        "by the opposition of", "by the oppression of",
        "by the optimization of", "by the orchestration of",
        "by the ordainment of", "by the orientation of",
        "by the origination of", "by the ornamentation of",
        "by the oscillation of", "by the osmosis of",
        "by the ostracism of", "under the justification of",
        "under the juxtaposition of", "under the kindling of",
        "under the labeling of", "under the lamentation of",
        "under the laceration of", "under the magnification of",
        "under the magnetization of", "under the maintenance of",
        "under the majority of", "under the making of",
        "under the manifestation of", "under the manipulation of",
        "under the manufacture of", "under the mapping of",
        "under the marginalization of", "under the marking of",
        "under the marriage of", "under the masking of",
        "under the matching of", "under the materialization of",
        "under the maturation of", "under the maximization of",
        "under the measurement of", "under the mediation of",
        "under the meditation of", "under the membership of",
        "under the memorization of", "under the mention of",
        "under the merging of", "under the merit of",
        "under the migration of", "under the mimicry of",
        "under the minimization of", "under the mining of",
        "under the minting of", "under the mirroring of",
        "under the misapplication of", "under the misappropriation of",
        "under the miscalculation of", "under the misclassification of",
        "under the misconception of", "under the misconduct of",
        "under the misdirection of", "under the misinterpretation of",
        "under the misjudgment of", "under the mismanagement of",
        "under the misplacement of", "under the mispricing of",
        "under the misreading of", "under the misrepresentation of",
        "under the misstatement of", "under the misuse of",
        "under the mitigation of", "under the mixing of",
        "under the mobilization of", "under the modeling of",
        "under the moderation of", "under the modification of",
        "under the modulation of", "under the molding of",
        "under the monitoring of", "under the monopoly of",
        "under the monotony of", "under the moralization of",
        "under the morphology of", "under the mortality of",
        "under the mortification of", "under the mortising of",
        "under the motivation of", "under the mounting of",
        "under the mourning of", "under the movement of",
        "under the muddling of", "under the multiplication of",
        "under the munificence of", "under the murder of",
        "under the mutation of", "under the mutilation of",
        "under the muttering of", "under the mystification of",
        "under the mythology of", "under the narration of",
        "under the nationalization of", "under the naturalization of",
        "under the navigation of", "under the necessity of",
        "under the negation of", "under the negotiation of",
        "under the neutralization of", "under the normalization of",
        "under the notation of", "under the nourishment of",
        "under the nucleation of", "under the nullification of",
        "under the numbering of", "under the nurture of",
        "under the obedience of", "under the objection of",
        "under the observation of", "under the obstruction of",
        "under the obtainment of", "under the occupation of",
        "under the occurrence of", "under the offering of",
        "under the offsetting of", "under the omission of",
        "under the opening of", "under the operation of",
        "under the opposition of", "under the oppression of",
        "under the optimization of", "under the orchestration of",
        "under the ordainment of", "under the orientation of",
        "under the origination of", "under the ornamentation of",
        "under the oscillation of", "under the osmosis of",
        "under the ostracism of", "under the nomination of",
    ))

    TRAILING_PLACES = dict.fromkeys((
        "quarter", "domain",
        "fief", "manor",
        "estate", "parish hall",
        "chapel", "abbey",
        "priory", "monastery",
        "convent", "hermitage",
        "mission", "station",
        "depot", "warehouse",
        "granary", "mill",
        "forge", "foundry",
        "workshop", "atelier",
        "studio", "office",
        "bureau", "agency",
        "institute", "academy",
        "seminary", "college",
        "lyceum", "gymnasium",
        "stadium", "arena",
        "theatre", "amphitheatre",
        "circus", "hippodrome",
        "basilica", "forum",
        "agora", "marketplace",
        "bazaar", "exchange",
        "harbour town",
    ))

    TRAILING_TIMES = dict.fromkeys((
        "reign", "dynasty",
        "lineage", "descent",
        "succession", "tenure",
        "incumbency", "session",
        "sitting", "watch",
        "shift", "tour",
        "rotation",
    ))

    GOVERNED = tuple(
        "The seal guarantees protection %s "
        "the deployment confinement fact." % phrase
        for phrase in PHRASINGS) + tuple(
        "The seal guarantees protection in whatsoever %s "
        "the deployment confinement fact holds." % place
        for place in TRAILING_PLACES) + tuple(
        "The seal guarantees protection through whatsoever %s "
        "the deployment confinement fact holds." % place
        for place in TRAILING_PLACES) + tuple(
        "The seal guarantees protection for whatsoever %s "
        "the deployment confinement fact holds." % form
        for form in TRAILING_TIMES)

    WEATHER = tuple(
        "The seal guarantees protection %s the weather." % phrase
        for phrase in PHRASINGS) + tuple(
        "The seal guarantees protection in whatsoever %s "
        "the weather holds." % place
        for place in TRAILING_PLACES) + tuple(
        "The seal guarantees protection through whatsoever %s "
        "the weather holds." % place
        for place in TRAILING_PLACES) + tuple(
        "The seal guarantees protection for whatsoever %s "
        "the weather holds." % form
        for form in TRAILING_TIMES)

    def test_phrasings_and_trailing_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_conditions_still_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for phrase in ("under the crozier of", "under the mitre of",
                       "under the tiara of", "under the seal ring of",
                       "under the lock of", "under the standard of",
                       "under the ensign of", "by the nomination of",
                       "by the scroll of", "by the charter of"):
            self.assertTrue(_scan(
                mod, "The seal guarantees protection %s "
                "the deployment confinement fact." % phrase))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the "
            "abjuration of the deployment confinement fact."))
        self.assertFalse(_scan(
            mod, "The seal guarantees protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanCompoundFixR36Tests(unittest.TestCase):
    """Ruling 2294: prefixed compound limb."""

    PREFIXES = dict.fromkeys((
        "argyro", "bario", "natro",
        "kali", "beryllo", "cobaltio",
        "erbo", "lantano", "lutecio",
        "neodymio", "niobio", "palladio",
        "praseodymio", "ruthenio", "thorio",
        "titanio", "uranio", "yttrio",
        "zirconio", "americio", "panto",
        "pilo", "plagio", "plano",
        "poikilo", "potamo", "quadri",
        "rubro", "scopio", "sito",
        "skato", "spano", "spargo",
        "sparto", "spasmo", "sphero",
        "spodo", "spondylo", "squamo",
        "stano", "staphylo", "stato",
        "steato", "stecho", "stegano",
        "tacho", "telo", "toxo",
        "typo", "villo", "visco",
        "zeo",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "butternutwood", "acaciawood", "karriwood",
        "marriwood", "tuartwood", "wandoowood",
        "blackbuttwood", "silkyoakwood", "spottedgumwood",
        "ironbarkwood", "coolabahwood", "riverredgumwood",
        "forestredgumwood", "sugargumwood", "peppermintwood",
        "stringybarkwood", "messmatewood", "tallowwood",
        "brushboxwood", "turpentinewood", "coachwood",
        "myrtlebeechwood", "celerytopwood", "huonwood",
        "kingbillywood", "leatherwood", "horizontalwood",
        "boobiallawood", "sheoakwood", "bulloakwood",
        "belahwood", "brigalowwood", "gidyeawood",
        "mulgawood", "myallwood", "boreewood",
        "wilgawood", "kurrajongwood", "quandongwood",
        "merantiwood", "keruingwood", "kapurwood",
        "balauwood", "chengalwood", "resakwood",
        "taunwood", "kwilawood", "zebranowood",
    ))

    PREFIX_FORMS = tuple(
        "Every record stands %sverified before use." % prefix
        for prefix in PREFIXES) + tuple(
        "Every record stands %schecked before use." % prefix
        for prefix in PREFIXES)

    ELEMENT_FORMS = tuple(
        "Every record stands %s-verified before use." % element
        for element in FIRST_ELEMENTS)

    def test_prefixes_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIX_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ELEMENT_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "Every record stands amphiverified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands verified before use."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanLexiconFixR36Tests(unittest.TestCase):
    """Ruling 2295: concept roots, un and resistant wordings."""

    WORDINGS = dict.fromkeys((
        "undocked", "unberthed", "unsplinted",
        "unpropped", "unshored", "unhemmed",
        "unlooped", "unregulated", "unrestricted",
        "unrestrained", "unhindered", "unimpeded",
        "unobstructed", "unblocked", "unshut",
        "unentrenched", "unbunkered", "uncompartmented",
        "unsectioned", "unzoned", "undivided",
        "unseparated", "unsegregated", "unisolated",
        "unmattressed", "uncushioned", "unbuffered",
        "undamped", "unmuffled", "unsilenced",
        "unbaffled", "gopherproof", "hareproof",
        "heronproof", "hyenaproof", "iguanaproof",
        "jackalproof", "kangarooproof", "koalaproof",
        "lemurproof", "llamaproof", "lynxproof",
        "monkeyproof", "mooseproof", "muleproof",
        "ocelotproof", "owlproof", "oxproof",
        "pandaproof", "pantherproof", "parrotproof",
        "peacockproof", "pelicanproof", "penguinproof",
        "ponyproof", "quailproof", "ravenproof",
        "rhinoproof", "salmonproof", "sheepproof",
        "storkproof", "swanproof", "turkeyproof",
        "turtleproof", "vultureproof", "walrusproof",
        "weaselproof", "wombatproof", "yakproof",
        "zebraproof", "whaleproof", "gopherresistant",
        "hareresistant", "heronresistant", "hyenaresistant",
        "iguanaresistant", "jackalresistant", "kangarooresistant",
        "koalaresistant", "lemurresistant", "llamaresistant",
        "lynxresistant", "monkeyresistant", "mooseresistant",
        "muleresistant", "ocelotresistant", "owlresistant",
        "oxresistant", "pandaresistant", "pantherresistant",
        "parrotresistant", "peacockresistant", "pelicanresistant",
        "penguinresistant", "ponyresistant", "quailresistant",
        "ravenresistant", "rhinoresistant", "salmonresistant",
        "sheepresistant", "storkresistant", "swanresistant",
        "turkeyresistant", "turtleresistant", "vultureresistant",
        "walrusresistant", "weaselresistant", "wombatresistant",
        "yakresistant", "zebraresistant", "foxresistant",
        "goatresistant", "horseresistant", "lionresistant",
        "moleresistant", "mouseresistant", "newtresistant",
        "otterresistant", "pigresistant", "pigeonresistant",
        "rabbitresistant", "raccoonresistant", "skunkresistant",
        "squirrelresistant", "tigerresistant", "toadresistant",
        "voleresistant", "wolfresistant", "henproof",
        "henresistant", "uncurled", "undimmed",
        "undipped", "undisguised", "undisplayed",
        "undistorted", "undisturbed", "undocumented",
        "undone", "undrained", "undrawn",
        "undried", "undrilled", "undulled",
        "undyed",
    ))

    RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in WORDINGS)

    STORE = tuple(
        "The store is %s." % word
        for word in WORDINGS)

    def test_record_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are unescorted by outside writers."))
        self.assertFalse(_scan(mod, "The store is unescorted."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanAssertedFixR36Tests(unittest.TestCase):
    """Ruling 2296: asserted form reading, journal verbs."""

    VERBS = dict.fromkeys((
        "neutralizes", "nucleates", "obtrudes",
        "obturates", "opalesces", "pelletizes",
        "penetrates", "perforates", "perfumes",
        "peroxidizes", "pickles", "plasticizes",
        "platinizes", "pollinates", "precools",
        "preheats", "premixes", "pressurizes",
        "pretreates", "quaternizes", "rectifies",
        "refracts", "regenerates", "rehydrates",
        "remineralizes", "resinates", "retards",
        "sanitizes", "nebulizes", "necrotizes",
        "normalizes", "notches", "nullifies",
        "numerates", "numbs", "obfuscates",
        "obliterates", "obscures", "obstructs",
        "occludes", "ochres", "octuples",
        "odorizes", "offsets", "oils",
        "opacifies", "opiates", "oppresses",
        "optimizes", "orchestrates", "orients",
        "originates", "ornaments", "ostracizes",
        "pacifies", "palliates", "palpates",
        "paralyzes", "parches", "pargets",
        "parses", "participates", "partitions",
        "passivates", "pastes", "pastures",
        "patches", "patentizes", "pathologizes",
        "patrols", "patronizes", "patterns",
        "pauses", "paves", "pawns",
        "peels", "pelts", "penalizes",
        "pencils", "performs", "periodizes",
        "perishes", "perjures", "permits",
        "permutes", "perpetrates", "perplexes",
        "persecutes", "perseveres", "persists",
        "personalizes", "persuades", "perturbs",
        "peruses", "pesters", "petalizes",
        "petitions",
    ))

    FORMS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in VERBS)

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal undulates integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanMarkerFixR36Tests(unittest.TestCase):
    """Ruling 2297: unconditional marker reading."""

    APPENDED_MARKERS = dict.fromkeys((
        "as long as the escarpments stand", "as long as the foothills stand",
        "as long as the mesas stand", "as long as the moraines stand",
        "as long as the outcrops stand", "as long as the promontories stand",
        "as long as the ranges stand", "as long as the slopes stand",
        "as long as the spurs stand", "as long as the summits stand",
        "as long as the tablelands stand", "as long as the terraces stand",
        "as long as the watersheds stand", "as long as the bluffs stand",
        "as long as the buttes stand", "as long as the coasts stand",
        "as long as the crags stand", "as long as the gullies stand",
        "as long as the basins stand", "as long as the atolls stand",
        "as long as the archipelagos stand", "till the cliffs crumble",
        "till the towers fall", "until the towers fall",
        "until the rivers dry", "until the wells run dry",
        "till the stars go out", "until the stars go out",
        "while the seas roll", "while the winds blow",
        "till the grass stops growing", "until the grass stops growing",
        "as long as the pinnacles stand", "till the moon burns out",
        "until the moon burns out", "as long as the oceans stand",
        "as long as the badlands stand", "as long as the channels stand",
        "as long as the cirques stand", "as long as the coves stand",
        "as long as the craters stand", "as long as the crests stand",
        "as long as the currents stand", "as long as the ponds stand",
        "as long as the pools stand", "as long as the prairies stand",
        "as long as the rapids stand", "as long as the springs stand",
        "as long as the streams stand", "as long as the taigas stand",
        "as long as the thickets stand", "as long as the tidepools stand",
        "as long as the tributaries stand", "as long as the uplands stand",
        "as long as the vales stand", "as long as the bays endure",
        "as long as the capes endure", "as long as the dunes endure",
        "as long as the fjords endure", "as long as the glaciers endure",
        "as long as the lagoons endure", "as long as the marshes endure",
        "as long as the meadows endure", "as long as the peaks endure",
        "as long as the reefs endure", "until the seas dry",
        "as long as the creeks stand", "as long as memory endures",
        "as long as the playas stand", "as long as the swamps stand",
    ))

    COMMA_MARKERS = dict.fromkeys((
        "as long as the escarpments stand", "as long as the foothills stand",
        "as long as the mesas stand", "as long as the moraines stand",
        "as long as the outcrops stand", "as long as the promontories stand",
        "as long as the ranges stand", "as long as the slopes stand",
        "as long as the spurs stand", "as long as the summits stand",
        "as long as the tablelands stand", "as long as the terraces stand",
        "as long as the watersheds stand", "as long as the bluffs stand",
        "as long as the buttes stand", "as long as the coasts stand",
        "as long as the crags stand", "as long as the gullies stand",
        "as long as the basins stand", "as long as the atolls stand",
        "as long as the archipelagos stand", "till the cliffs crumble",
        "till the towers fall", "until the towers fall",
        "until the rivers dry", "until the wells run dry",
        "till the stars go out", "until the stars go out",
        "while the seas roll", "while the winds blow",
        "till the grass stops growing", "until the grass stops growing",
        "as long as the oceans stand", "as long as the badlands stand",
        "as long as the channels stand", "as long as the cirques stand",
        "as long as the coves stand", "as long as the craters stand",
        "as long as the crests stand", "as long as the currents stand",
        "as long as the ponds stand", "as long as the pools stand",
        "as long as the prairies stand", "as long as the rapids stand",
        "as long as the springs stand", "as long as the streams stand",
        "as long as the taigas stand", "as long as the thickets stand",
        "as long as the tidepools stand", "as long as the tributaries stand",
        "as long as the uplands stand", "as long as the vales stand",
        "as long as the bays endure", "as long as the capes endure",
        "as long as the dunes endure", "as long as the fjords endure",
        "as long as the glaciers endure", "as long as the lagoons endure",
        "as long as the marshes endure", "as long as the meadows endure",
        "as long as the peaks endure", "as long as the reefs endure",
        "until the seas dry",
    ))

    APPENDED = tuple(
        _GOVERNED_CLAIM + " %s." % marker
        for marker in APPENDED_MARKERS)

    COMMA = tuple(
        _GOVERNED_CLAIM + ", %s." % marker
        for marker in COMMA_MARKERS)

    def test_appended_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.APPENDED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_comma_clause_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMMA:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + " right or wrong."))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + ", right or wrong."))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + ", as long as the pinnacles stand."))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + " as long as the shores stand."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanNegationFixR36Tests(unittest.TestCase):
    """Ruling 2298: negation narrowing, roots judged asserted."""

    REPG_FORMS = dict.fromkeys((
        "attached", "bound", "folded",
        "sketched", "underlined", "frankable",
        "sketchable", "underlineable",
    ))

    CONF_VERBS = dict.fromkeys((
        "crumpled", "can be dented", "can be dimpled",
        "can be drilled", "can be folded", "can be glued",
        "can be hammered", "can be oiled", "can be soldered",
        "can be varnished", "can be waxed", "can be thawed",
    ))

    CONF_ROOTS = dict.fromkeys((
        "surveyable", "thawable",
    ))

    NO_FORMS = tuple(
        "No record is %s after writing." % root
        for root in REPG_FORMS) + tuple(
        "No record can be %s after writing." % root
        for root in REPG_FORMS) + tuple(
        "No record can be %s after writing." % verb
        for verb in CONF_VERBS) + tuple(
        "No record is %s after writing." % root
        for root in CONF_ROOTS)

    ASSERTED = tuple(
        "Records are %s after writing." % root
        for root in REPG_FORMS) + tuple(
        "Records are %s after writing." % verb
        for verb in CONF_VERBS) + tuple(
        "Records are %s after writing." % root
        for root in CONF_ROOTS)

    def test_probed_no_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_analogues_and_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)
        self.assertTrue(_scan(
            mod, "No bundle name was hidden in this record."))
        self.assertFalse(_scan(
            mod, "Records are hidden by outsiders."))
        self.assertFalse(_scan(mod, "No data leaves the store."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanConceptFixR36Tests(unittest.TestCase):
    """Ruling 2299: roots outside the judged concept roots."""

    REPG_ROOTS = dict.fromkeys((
        "appendable", "inventoriable", "itemisable",
        "ledgerable", "manifestable", "paginateable",
        "receiptable", "tabulatable", "foldable",
        "boxable", "noteable", "punchable",
        "rateable", "specifiable", "stateable",
        "structurable", "styleable", "valueable",
        "wordable",
    ))

    REPG_VERBS = dict.fromkeys((
        "appended", "arranged", "assembled",
        "attributed", "backdated", "documented",
        "ledgered", "parcelled", "punched",
        "specified", "spelled", "stated",
        "structured", "worded",
    ))

    CONF_ROOTS = dict.fromkeys((
        "severable", "swappable", "symbolizable",
        "tabulatable", "tamable", "teachable",
        "tearable", "teasable", "texturable",
        "trappable", "washable", "wearable",
    ))

    CONF_VERBS = dict.fromkeys((
        "crushed", "cut", "swapped",
        "symbolized", "taught", "teased",
        "textured", "trapped", "washed",
    ))

    FORMS = tuple(
        "No record is %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "Records are %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "Records are %s after writing." % verb
        for verb in REPG_VERBS) + tuple(
        "No record can be %s after writing." % verb
        for verb in REPG_VERBS) + tuple(
        "No record is %s after writing." % verb
        for verb in REPG_VERBS) + tuple(
        "The record is %s after writing." % root
        for root in CONF_ROOTS) + tuple(
        "No record is %s after writing." % root
        for root in CONF_ROOTS) + tuple(
        "Records are %s after writing." % verb
        for verb in CONF_VERBS) + tuple(
        "No record can be %s after writing." % verb
        for verb in CONF_VERBS)

    def test_roots_and_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for root in ("excerpted", "leased", "rescanned"):
            self.assertFalse(_scan(
                mod, "Records are %s after writing." % root))
            self.assertFalse(_scan(
                mod, "No record is %s after writing." % root))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))
