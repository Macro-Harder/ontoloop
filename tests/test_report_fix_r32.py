"""Fix round 32, Region 1: report seal claim scan pins.

Rulings 1782 to 1789 of the Round 32 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R32-REPG-1 to 8 and the Confinement paper findings
S15-R32-CONF-1 to 11 in their absorbed limbs, on the
templates those papers state. A form probed in both
raising papers on the one template stands counted once,
in the form of the triage merges.
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


class SealClaimScanInabilityFixR32Tests(unittest.TestCase):
    """Ruling 1782: inability limb, followers and windows."""

    MODAL_REPG_WORDS = dict.fromkeys((
        "electroplated", "passivated", "parkerized", "casehardened",
        "shotpeened", "beadblasted", "electropolished", "deburred",
        "chamfered", "threaded", "grooved", "slotted", "splined",
        "broached", "shampooed", "conditioned", "exfoliated",
        "sanitised", "poached", "sauteed", "grilled", "broiled",
        "seared", "blanched", "parboiled", "hemmed", "tailored",
        "upholstered", "honed", "milled", "sliced", "diced",
        "grated", "battered", "breaded", "primed",
    ))

    MODAL_CONF_WORDS = dict.fromkeys((
        "adorned", "bordered", "bossed", "capped", "corded",
        "cornered", "cuffed", "curtained", "cushioned", "decked",
        "decorated", "edged", "engirdled", "festooned", "flanged",
        "flanked", "flecked", "flocked", "floored", "fluted",
        "foiled", "foliated", "frilled", "fringed", "furled",
        "furnished", "garlanded", "gloved", "gowned", "grained",
        "grooved", "hafted", "haltered", "hatched", "headed",
        "heeled", "helmeted", "hooded", "hoofed", "horned", "husked",
        "jacketed", "jeweled", "keeled", "kilted", "knobbed",
        "lapped", "legged", "lidded", "limbed", "looped", "maned",
        "mantled", "marbled", "masted", "matted", "mittened",
        "mottled", "mouthed", "necked", "nested", "netted", "nosed",
        "notched", "oared", "orbed", "paneled", "papered", "peaked",
        "pelleted", "penciled", "peppered", "perched", "petaled",
        "picked", "pierced", "piled", "pillared", "pimpled",
        "pinked", "piped", "pitched", "pivoted", "plaided",
        "planked", "plumbed", "plumed", "pocketed", "podded",
        "pointed", "poled", "pommelled", "forked", "leaved", "paged",
    ))

    ASSERTED_WORDS = dict.fromkeys((
        "electroplated", "passivated", "parkerized", "casehardened",
        "shotpeened", "beadblasted", "electropolished", "deburred",
        "chamfered", "threaded", "grooved", "slotted", "splined",
        "broached", "shampooed", "conditioned", "exfoliated",
        "sanitised", "poached", "sauteed", "grilled", "broiled",
        "seared", "blanched", "parboiled", "hemmed", "tailored",
        "upholstered", "honed", "milled", "sliced", "diced",
        "grated", "battered", "primed", "adorned", "bordered",
        "bossed", "capped", "corded", "cornered", "cuffed",
        "curtained", "cushioned", "decked", "decorated", "edged",
        "engirdled", "festooned", "flanged", "flanked", "flecked",
        "flocked", "floored", "fluted", "foiled", "foliated",
        "frilled", "fringed", "furled", "furnished", "garlanded",
        "gloved", "gowned", "grained", "hafted", "haltered",
        "hatched", "headed", "heeled", "helmeted", "hooded",
        "hoofed", "horned", "husked", "jacketed", "jeweled",
        "keeled", "kilted", "knobbed", "lapped", "legged", "lidded",
        "limbed", "looped", "maned", "mantled", "marbled", "masted",
        "matted", "mittened", "mottled", "mouthed", "necked",
        "nested", "netted", "nosed", "notched", "oared", "orbed",
        "paneled", "papered", "peaked", "pelleted", "penciled",
        "peppered", "perched", "petaled", "picked", "pierced",
        "piled", "pillared", "pimpled", "pinked", "piped", "pitched",
        "pivoted", "plaided", "planked", "plumbed", "plumed",
        "pocketed", "podded", "pointed", "poled", "pommelled",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "truculently", "belligerently", "obstreperously",
        "recalcitrantly", "intractably", "waywardly", "fractiously",
        "irascibly", "huffily", "broodingly", "admirably", "affably",
        "amicably", "assiduously", "commendably", "conscientiously",
        "cordially", "ecstatically", "excellently", "genially",
        "gloriously", "graciously", "harmoniously", "hospitably",
        "industriously", "jubilantly", "languorously", "laudably",
        "magnificently", "methodically", "obligingly", "oddly",
        "offensively", "ominously", "optimistically", "painfully",
        "passionately", "peremptorily", "perkily", "perseveringly",
        "persistently", "piously", "pleasantly", "ploddingly",
        "poignantly", "portentously", "powerfully", "pragmatically",
        "precariously", "predictably", "prettily", "probingly",
        "prodigally", "proficiently", "profoundly", "profusely",
        "progressively", "prolifically", "prominently", "properly",
        "prophetically", "prosaically", "protectively",
        "protestingly", "prudently", "pugnaciously", "pungently",
        "purposefully", "puzzledly", "quaintly", "quarrelsomely",
        "queasily", "queerly", "quiveringly", "quizzically",
        "rapturously", "sedulously", "sociably", "splendidly",
        "superbly", "triumphantly", "worthily",
    ))

    WINDOW_PLACES = dict.fromkeys((
        "bunkhouse", "clubhouse", "coachhouse", "enginehouse",
        "farmhouse", "flophouse", "guesthouse", "guildhouse",
        "longhouse", "malthouse", "nuthouse", "outhouse",
        "packinghouse", "pesthouse", "pilothouse", "resthouse",
        "safehouse", "springhouse", "stationhouse", "summerhouse",
        "switchhouse", "washhouse", "wheelhouse", "whorehouse",
        "cemetery", "chancellery", "exchange", "plantation",
        "precinct", "ranch", "refuge", "reservoir", "residence",
        "schoolhouse", "slaughteryard", "stockade", "vineyard",
        "yard",
    ))

    MODAL = tuple(
        "Records cannot be %s by outsiders." % word
        for word in MODAL_REPG_WORDS) + tuple(
        "Records cannot be %s after writing." % word
        for word in MODAL_CONF_WORDS)

    ASSERTED = tuple(
        "Records are %s by outsiders." % word
        for word in ASSERTED_WORDS)

    WINDOWS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in WINDOW_WORDS) + tuple(
        "Records cannot in any %s be altered after writing."
        % place for place in WINDOW_PLACES)

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
            _scan(mod, "Records cannot be fluorinated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are fluorinated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be drilled after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot petulantly be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any millhouse be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any slaughterhouse be altered "
            "after writing."))
        self.assertFalse(
            _scan(mod, "Records cannot be annealed by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are breaded by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanGoverningFixR32Tests(unittest.TestCase):
    """Ruling 1783: governing condition limb."""

    PHRASING_WORDS = dict.fromkeys((
        "under the reign of", "under the ukase of",
        "under the firman of", "under the rescript of",
        "under the enactment of", "under the sceptre of",
        "by the sceptre of", "under the throne of",
        "by the throne of", "under the mitre of",
        "under the tiara of", "under the pallium of",
        "under the mastery of", "by the mastery of",
        "under the supremacy of", "by the supremacy of",
        "under the ascendancy of", "under the crown of",
        "by the crown of", "under the rod of", "under the lash of",
        "under orders from", "by the adjuration of",
        "by the allocution of", "by the arbitrament of",
        "by the award of", "by the bill of",
        "by the capitulation of", "by the caveat of",
        "by the citation of", "by the commandment of",
        "by the condemnation of", "by the custom of",
        "by the declaration of", "by the deliverance of",
        "by the dictum of", "by the directive of",
        "by the discipline of", "by the dispensation of",
        "by the disposition of", "by the dogma of", "by the doom of",
        "by the enactment of", "by the enforcement of",
        "by the enjoinder of", "by the entail of",
        "by the epistle of", "by the establishment of",
        "by the exaction of", "by the exhortation of",
        "by the finding of", "by the formulary of",
        "by the guideline of", "by the imperative of",
        "by the imposition of", "by the instrument of",
        "by the manifesto of", "by the measure of",
        "by the missive of", "by the notice of",
        "by the notification of", "by the oath of",
        "by the obligation of", "by the observance of",
        "by the pact of", "by the patent of", "by the petition of",
        "by the placard of", "by the plea of", "by the precept of",
        "by the prescription of", "by the pronouncement of",
        "by the proposal of", "by the protocol of",
        "by the requirement of", "by the requisition of",
        "by the resolution of", "by the rubric of",
        "by the scroll of", "by the sentence of",
        "by the settlement of", "by the stipulation of",
        "by the syllabus of", "by the testament of",
        "by the provision of", "under the adjuration of",
        "under the allocution of", "under the arbitrament of",
        "under the award of", "under the bill of",
        "under the capitulation of", "under the caveat of",
        "under the citation of", "under the commandment of",
        "under the condemnation of", "under the custom of",
        "under the declaration of", "under the deliverance of",
        "under the dictum of", "under the directive of",
        "under the discipline of", "under the dispensation of",
        "under the disposition of", "under the dogma of",
        "under the doom of", "under the enforcement of",
        "under the enjoinder of", "under the entail of",
        "under the epistle of", "under the establishment of",
        "under the exaction of", "under the exhortation of",
        "under the finding of", "under the formulary of",
        "under the guideline of", "under the imperative of",
        "under the imposition of", "under the instrument of",
        "under the manifesto of", "under the measure of",
        "under the missive of", "under the notice of",
        "under the notification of", "under the oath of",
        "under the obligation of", "under the observance of",
        "under the pact of", "under the patent of",
        "under the petition of", "under the placard of",
        "under the plea of", "under the precept of",
        "under the prescription of", "under the pronouncement of",
        "under the proposal of", "under the protocol of",
        "under the requirement of", "under the requisition of",
        "under the resolution of", "under the rubric of",
        "under the scroll of", "under the sentence of",
        "under the settlement of", "under the stipulation of",
        "under the syllabus of", "under the testament of",
        "under the determination of", "under the proclamation of",
        "under the summons of",
    ))

    TRAILING_WORDS = dict.fromkeys((
        "in whatsoever manner", "by whatsoever means",
        "for howsoever long", "until whatsoever time",
        "in whencesoever place", "at whencesoever time",
        "through whencesoever place", "in any clime where",
        "in every clime where", "wheresoever and whensoever",
        "thithersoever", "in whatsoever clime",
        "through whatsoever clime", "by whatsoever road",
        "in whatsoever land", "through whatsoever land",
        "in whatsoever realm", "through whatsoever realm",
        "for whatsoever span", "as and howsoever",
        "as and whensoever", "howsoever and whenever",
        "howsoever and whensoever", "if and as", "if and wherein",
        "if and whithersoever", "once and wherein",
        "once and whithersoever", "whensoever and howsoever",
        "whensoever and wherein", "whensoever and whithersoever",
        "when and as", "when and wherein", "when and whithersoever",
        "whenever and as", "whenever and wherein",
        "whenever and whithersoever",
    ))

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in PHRASING_WORDS)

    TRAILING = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact holds." % form for form in TRAILING_WORDS)

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather of "
        "the day." % phrase for phrase in PHRASING_WORDS)

    WEATHER_TRAILING = tuple(
        "The seal guarantees protection %s the weather of "
        "the day holds." % form for form in TRAILING_WORDS)

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
            mod, "The seal guarantees protection under the "
            "jurisdiction of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the "
            "government of the deployment confinement fact."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR32Tests(unittest.TestCase):
    """Ruling 1784: prefixed compound limb."""

    PREFIX_WORDS = dict.fromkeys((
        "phyllo", "phyco", "rhizo", "anthropo", "oxy", "sulfo",
        "bromo", "fluoro", "iodo", "hydroxy", "carboxy", "methyl",
        "ethyl", "phenyl", "benzo", "naphtho", "anthra", "azo",
        "diazo", "peroxo", "epoxy", "ethoxy", "methoxy", "amphi",
        "botano", "calori", "carcino", "cephalo", "dynamo", "ergo",
        "ethno", "galacto", "geronto", "glosso", "hyalo", "icono",
        "irido", "karyo", "kerato", "kineto", "lepto", "leuco",
        "logo", "melano", "metallo", "meteoro", "narco", "neutro",
        "oculo", "odonto", "oligo", "onco", "onto", "ophio",
        "organo", "osmo", "ostio", "pachy", "paedo", "palato",
        "pancreato", "pedo", "phago", "phoro", "phreno", "piezo",
        "placo", "plasmo", "pleuro", "pod", "polio", "poro",
        "psychro", "ptero", "pulmo", "pyelo", "pyo", "recto", "reno",
        "retino", "rhabdo", "rheo", "rhodo", "sacro", "salpingo",
        "sapro", "schizo", "scinti", "sclero", "scoto", "sebo",
        "semio", "sialo", "somato", "somno", "spermo", "spheno",
        "sphygmo", "spiro", "spleno", "sporo", "stego", "steno",
        "sterno", "stomato", "strepto", "stylo", "sudo", "tachy",
        "tarso", "taxo", "tecto", "teleo", "teno", "terato",
        "thalasso", "thanato", "theco", "thoraco", "thrombo",
        "thymo", "thyro", "toco", "tomo", "tono", "topo", "traumato",
        "tricho", "trocho", "tropho", "tropo", "tylo", "tympano",
        "ulno", "umbilico", "uro", "utero", "veno", "ventro",
        "vermi", "vertebro", "vesico", "vestibulo", "viscero",
        "vitreo", "vulvo", "xero", "xipho", "xylo", "zygo", "zymo",
    ))

    ELEMENT_WORDS = dict.fromkeys((
        "satinwood", "snakewood", "spaltedwood", "burlwood",
        "heartwood", "sapwood", "driftwood", "bogwood", "ironbark",
        "silkyoak", "apricotwood", "aspenwood", "avocado", "banyan",
        "baywood", "beechwood", "birchbark", "blackwood", "bluegum",
        "buckeye", "catalpa", "cedarel", "chestnutwood",
        "chinaberry", "coffeewood", "cottonwood", "cucumberwood",
        "cypresswood", "elderwood", "eucalyptus", "figwood",
        "firwood", "granadillo", "grapevine", "guava", "hawthorn",
        "hazelwood", "hickorywood", "hollywood", "honeylocust",
        "hornwood", "jacaranda", "jatoba", "juniperwood", "kauri",
        "kiaat", "lancewood", "lemonwood", "locustwood", "logwood",
        "loquat", "macassar", "madrone", "magnoliawood", "manzanita",
        "mesquite", "monkeypod", "mulberrywood", "nectarine",
        "oleander", "osagewood", "paldao", "palmwood", "papaya",
        "paulownia", "peachwood", "pecanwood", "pistachio",
        "planetree", "poplarwood", "quince", "rambutan", "redbud",
        "redgum", "redoak", "rowanwood", "sassafraswood",
        "serviceberry", "sourwood", "spanishcedar", "sycamorewood",
        "tamarindwood", "tigerwood", "tuliptree", "whiteoak",
        "willowwood", "yewwood",
    ))

    PREFIX_VERIFIED = tuple(
        "Every record stands %sverified before use." % prefix
        for prefix in PREFIX_WORDS)

    PREFIX_CHECKED = tuple(
        "Every record stands %schecked before use." % prefix
        for prefix in PREFIX_WORDS)

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in ELEMENT_WORDS)

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
            mod, "Every record stands ectoverified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands xenoverified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands ebonite-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands ashwood-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands zebrawood-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands verified before use."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR32Tests(unittest.TestCase):
    """Ruling 1785: concept root list and un wording limb."""

    WORDINGS = dict.fromkeys((
        "unescorted", "unaccompanied", "untenanted", "uninhabited",
        "unsheltered", "unbuttressed", "unwindowed", "unblinded",
        "unstockaded", "unpalisaded", "unmoated", "unturreted",
        "unbattlemented", "unsearchlighted", "unsirened",
        "rainresistant", "flameresistant", "falloutproof",
        "briarproof", "crinkleproof", "draughtproof",
        "fractureproof", "kinkproof", "larvaproof", "ovenproof",
        "pelletproof", "perspirationproof", "pinholeproof",
        "rubproof", "scaldproof", "seepageproof", "shakeproof",
        "shellproof", "skidproof", "slickproof", "slideproof",
        "slipproof", "slopproof", "slushproof", "smearproof",
        "spotproof", "squashproof", "squeakproof", "stinkproof",
        "streakproof", "strikeproof", "stripproof", "sweatproof",
        "swellproof", "tiltproof", "torrentproof", "torsionproof",
        "trickleproof", "tripproof", "tumbleproof", "viperproof",
        "voiceproof", "voltageproof", "washproof",
        "bacteriaresistant", "blightresistant", "bruiseresistant",
        "chipresistant", "collisionresistant", "creepresistant",
        "crinkleresistant", "curlresistant", "dampresistant",
        "diseaseresistant", "distortionresistant",
        "droughtresistant", "erosionresistant", "fatigueresistant",
        "flexresistant", "foldresistant", "fractureresistant",
        "freezeresistant", "frictionresistant", "fungusresistant",
        "gasresistant", "germresistant", "gnawresistant",
        "hailresistant", "insectresistant", "moistureresistant",
        "oxidationresistant", "ozoneresistant", "pierceresistant",
        "pillingresistant", "radiationresistant", "rotresistant",
        "scaldresistant", "shrinkresistant", "skidresistant",
        "smearresistant", "sootresistant", "sparkresistant",
        "spillresistant", "strainresistant", "streakresistant",
        "stressresistant", "stripresistant", "swellresistant",
        "thornresistant", "tideresistant", "tiltresistant",
        "torsionresistant", "toxinresistant", "trickleresistant",
        "tripresistant", "tumbleresistant", "typhoonresistant",
        "venomresistant", "vibrationresistant", "viperresistant",
        "virusresistant", "voltageresistant", "washresistant",
        "waspresistant", "unbonneted", "unbooted", "unbridged",
        "uncaparisoned", "uncasemented", "unchaperoned", "uncloaked",
        "unclothed", "uncombed", "uncorseted", "uncowled",
        "uncrated", "uncrowned", "undecked", "undecorated",
        "undraped", "undressed", "unfeathered", "unflagged",
        "unfledged", "unfrocked", "unfurnished", "ungarlanded",
        "ungarmented", "ungarnished", "ungirdled", "ungloved",
        "ungowned", "unhampered", "unhatted", "unhelmeted",
        "unhorsed", "unjacketed", "unjeweled", "unkenneled",
        "unlidded", "unmantled", "unmasted", "unmitred", "unpapered",
        "unpillared", "unplanked", "unplumed", "unpoliced",
        "unrobed", "unsashed", "unshawled", "unshod", "unsleeved",
        "unsocked", "unstockinged", "unswaddled", "untented",
        "unturbaned", "unvested", "unwreathed",
    ))

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
            mod, "The records are unalarmed by outside writers."))
        self.assertFalse(_scan(
            mod, "The store is ungated."))
        self.assertFalse(_scan(
            mod, "The records are solventresistant by outside "
            "writers."))
        self.assertFalse(_scan(
            mod, "The store is stabproof."))
        self.assertFalse(_scan(
            mod, "The store is acidproof."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanAssertedFixR32Tests(unittest.TestCase):
    """Ruling 1786: asserted form limb."""

    VERB_WORDS = dict.fromkeys((
        "undulates", "fizzes", "effervesces", "coagulates",
        "congeals", "solidifies", "liquefies", "condenses",
        "precipitates", "denatures", "oxidizes", "tarnishes",
        "blooms", "blossoms", "germinates", "sprouts", "buds",
        "flowers", "fruits", "sheds", "molts", "hibernates",
        "migrates", "swarms", "flocks", "pulses", "quakes",
        "tremors", "convulses", "spasms", "jerks", "cowers",
        "squats", "curtsies", "genuflects", "prostrates", "grovels",
        "writhes", "wriggles", "squirms", "aches", "beams",
        "blisters", "bounces", "buckles", "budges", "bulges",
        "burgeons", "bursts", "cascades", "chokes", "chugs",
        "churns", "claps", "clashes", "clings", "clogs", "clots",
        "clouds", "clumps", "coasts", "coils", "collapses",
        "collides", "combusts", "cools", "cramps", "creases",
        "crinkles", "crisps", "crumples", "curdles", "curls",
        "curves", "dangles", "darkens", "darts", "dashes", "dazzles",
        "declines", "decomposes", "deepens", "deflates", "deforms",
        "deliquesces", "deluges", "dents", "derails", "descends",
        "desiccates", "detonates", "develops", "deviates", "dies",
        "diffuses", "dilates", "dims", "dings", "dips", "discharges",
        "discolors", "disintegrates", "disperses", "dissolves",
        "distends", "distills", "distorts", "diverges", "divides",
        "dodges", "dulls", "dumps", "dusts", "dwells", "dyes",
        "eases", "ebbs", "edges", "elapses", "elongates", "eludes",
        "embarks", "emerges", "empties", "encroaches", "ends",
        "endures", "enfolds", "engages", "engorges", "engulfs",
        "enlarges", "ensues", "entangles", "enters", "entwines",
        "envelops", "erodes", "erupts", "evades", "evaporates",
        "evens", "everts", "evolves", "expires", "explodes",
        "exults",
    ))

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in VERB_WORDS)

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL_VERBS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal bleeds integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal seeps integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal reverberates integrity for every "
            "reader."))
        self.assertFalse(_scan(
            mod, "The journal drools integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanMarkerFixR32Tests(unittest.TestCase):
    """Ruling 1787: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    REPG_MARKER_WORDS = (
        "right or wrong", "in prosperity or adversity",
        "through fortune and misfortune", "till the fat lady sings",
        "until the twelfth of never", "for a thousand years",
        "for ten thousand years", "down the ages",
        "till the last breath", "while breath remains",
        "as long as breath lasts", "beyond the grave",
        "from the womb to the tomb", "through all weathers",
        "in wind and rain", "through wind and rain",
        "by night and by day", "in darkness and in light",
        "through darkness and light", "while the stars shine",
        "as long as the stars shine", "till the oceans dry",
        "while the oceans roll", "as long as the oceans roll",
    )

    CONF_MARKER_WORDS = (
        "as long as the moon endures", "as long as the sun shines",
        "as long as the world lasts", "for all the centuries",
        "for all the millennia", "for all the years",
        "for the life of the world", "in all the years",
        "in all time", "in every century",
        "through all the centuries", "through every century",
        "through the life of the world", "throughout all time",
        "till resurrection day", "till the crack of doom",
        "till the day of judgment", "till the final judgment",
        "till the heavens fall", "till the resurrection",
        "till the rivers dry", "till the seas dry",
        "till the sky falls", "till time itself ends",
        "to the crack of doom", "to the worlds end",
        "until the crack of doom", "until the day of judgment",
        "until the final judgment", "until the world ends",
    )

    COMMA_ONLY_WORDS = (
        "unto the last generation", "from now until forever",
    )

    APPENDED = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker)
        for marker in dict.fromkeys(
            REPG_MARKER_WORDS + CONF_MARKER_WORDS))

    COMMA = tuple(
        "%s, %s." % (_GOVERNED_CLAIM, marker)
        for marker in dict.fromkeys(
            REPG_MARKER_WORDS + CONF_MARKER_WORDS
            + COMMA_ONLY_WORDS))

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
        self.assertTrue(_scan(mod, self.BASE + "."))
        self.assertFalse(_scan(mod, self.BASE + " without fail."))
        self.assertFalse(_scan(
            mod, self.BASE + " come hell or high water."))
        self.assertFalse(_scan(
            mod, self.BASE + " till the end of the world."))
        self.assertFalse(_scan(
            mod, self.BASE + " unto the last generation."))
        self.assertFalse(_scan(
            mod, self.BASE + " from now until forever."))


class SealClaimScanNegationFixR32Tests(unittest.TestCase):
    """Ruling 1788: negation narrowing limb, No opening form."""

    REPG_ROOT_WORDS = dict.fromkeys((
        "captioned", "charted", "collateralised", "datestamped",
        "flagged", "graphed", "labelled", "mapped", "noted",
        "referenced", "sampled", "timestamped",
    ))

    CONF_CAN_BE_WORDS = dict.fromkeys((
        "affixed", "banded", "belted", "braced", "bracketed",
        "collared", "crimped", "encircled", "garnished", "girdled",
        "harnessed", "housed", "jointed", "laced", "leaved",
        "meshed", "mortised", "pegged", "penned", "pitted",
        "plastered", "plated", "polished",
    ))

    CONF_IS_WORDS = dict.fromkeys((
        "affixable", "bandable", "beltable", "braceable",
        "bracketable", "collarable", "crimpable", "encirclable",
        "garnishable", "girdable", "harnessable", "housable",
        "jointable", "laceable", "leavable", "meshable",
        "mortisable", "plasterable", "platable", "polishable",
    ))

    PROBED_IS = tuple(
        "No record is %s after writing." % word
        for word in REPG_ROOT_WORDS) + tuple(
        "No record is %s after writing." % word
        for word in CONF_IS_WORDS)

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in REPG_ROOT_WORDS) + tuple(
        "No record can be %s after writing." % word
        for word in CONF_CAN_BE_WORDS)

    ASSERTED_ANALOGUES = tuple(
        "Records are %s after writing." % word
        for word in REPG_ROOT_WORDS)

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

    def test_asserted_analogues_and_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_ANALOGUES:
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


class SealClaimScanConceptRootsFixR32Tests(unittest.TestCase):
    """Ruling 1789: roots outside the judged concept roots."""

    REPG_ROOT_WORDS = dict.fromkeys((
        "receipted", "invoiced", "billed", "vouchered", "ticketed",
        "minuted", "journalled", "diarised", "chauffeured", "carted",
        "barged", "railed", "flown", "airlifted", "parachuted",
        "narrowcast", "podcast", "webcast", "livestreamed",
        "simulcast", "retransmitted", "rebroadcast", "liened",
        "encumbered", "hypothecated", "scheduled", "timetabled",
        "crossreferenced", "footnoted", "headlined", "bylined",
        "datelined", "itemised", "itemized", "enumerated",
        "tabulated", "surveilled", "snapshotted", "thumbnailed",
        "badged",
    ))

    CONF_ROOT_WORDS = dict.fromkeys((
        "callable", "clickable", "commentable", "expandable",
        "flashable", "followable", "formattable", "loadable",
        "mergeable", "networkable", "parsable", "pausable",
        "payable", "pingable", "portable", "processable",
        "programmable", "queryable", "queueable", "renderable",
        "replyable", "resizable", "routable", "saveable", "scalable",
        "scrollable", "segmentable", "selectable", "serializable",
        "servable", "sortable", "stackable", "storable",
        "subscribable", "tappable", "templatable", "transportable",
        "traversable", "triggerable", "typable", "unloadable",
        "upgradeable", "usable", "versionable", "writable",
    ))

    CONF_VERB_WORDS = dict.fromkeys((
        "branched", "called", "clicked", "commented", "deployed",
        "expanded", "flashed", "followed", "formatted", "hosted",
        "loaded", "merged", "networked", "paid", "parsed", "paused",
        "pinged", "processed", "programmed", "released", "rendered",
        "replied", "resized", "scaled", "seeded", "segmented",
        "selected", "serialized", "served", "sorted", "stacked",
        "staged", "subscribed", "tapped", "templated", "transported",
        "traversed", "triggered", "unloaded", "upgraded", "used",
        "versioned", "written",
    ))

    REPG_FORMS = tuple(
        "No record is %s after writing." % word
        for word in REPG_ROOT_WORDS) + tuple(
        "No record can be %s after writing." % word
        for word in REPG_ROOT_WORDS) + tuple(
        "Records are %s after writing." % word
        for word in REPG_ROOT_WORDS)

    CONF_ROOT_FORMS = tuple(
        "The record is %s after writing." % word
        for word in CONF_ROOT_WORDS) + tuple(
        "No record is %s after writing." % word
        for word in CONF_ROOT_WORDS)

    CONF_VERB_FORMS = tuple(
        "Records are %s after writing." % word
        for word in CONF_VERB_WORDS) + tuple(
        "No record can be %s after writing." % word
        for word in CONF_VERB_WORDS)

    def test_repg_roots_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.REPG_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_conf_roots_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONF_ROOT_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_conf_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONF_VERB_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "No record is excerpted after writing."))
        self.assertFalse(_scan(
            mod, "Records are excerpted after writing."))
        self.assertFalse(_scan(
            mod, "No record is leased after writing."))
        self.assertFalse(_scan(
            mod, "Records are rescanned after writing."))
        self.assertFalse(_scan(
            mod, "The record is attachable after writing."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


if __name__ == "__main__":
    unittest.main()
