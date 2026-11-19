"""Fix round 33, Region 1: report seal claim scan pins.

Rulings 1889 to 1896 of the Round 33 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R33-REPG-1 to 8 and the Confinement paper findings
S15-R33-CONF-1 to 11 in their absorbed limbs, on the
templates those papers state. A form probed in both
raising papers on the one template stands counted once,
in the form of the triage merges. Divided forms standing
at pole on the governing base in one construction stand
pinned in the controls of their class in that construction.
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


class SealClaimScanInabilityFixR33Tests(unittest.TestCase):
    """Ruling 1889: inability limb, followers and windows."""

    MODAL_REPG_WORDS = dict.fromkeys((
        "pressed", "wrung", "scoured",
        "iced", "sugared", "basted",
        "swaged", "knurled", "reamed",
        "planed", "chiselled", "whittled",
        "lathed", "cast", "extruded",
        "calendered", "marquetried",
    ))

    MODAL_CONF_WORDS = dict.fromkeys((
        "antiqued", "appliqued", "barbed",
        "beaded", "bevelled", "blotched",
        "cambered", "chased", "chiselled",
        "cleated", "clinched", "coiled",
        "encrusted", "featherstitched", "ferruled",
        "filigreed", "filleted", "ribbed",
        "scalloped", "scrolled", "seamed",
        "spangled", "splinted", "studded",
        "tasselled", "tessellated", "thatched",
        "trellised", "tufted", "veined",
        "wattled", "whorled", "winged",
        "zoned", "stencilled",
    ))

    ASSERTED_WORDS = dict.fromkeys((
        "pressed", "wrung", "scoured",
        "iced", "sugared", "basted",
        "swaged", "knurled", "reamed",
        "planed", "chiselled", "whittled",
        "lathed", "cast", "extruded",
        "calendered", "marquetried", "spiced",
        "starched", "antiqued", "appliqued",
        "barbed", "beaded", "bevelled",
        "blotched", "cambered", "chased",
        "cleated", "clinched", "coiled",
        "encrusted", "featherstitched", "ferruled",
        "filigreed", "filleted", "ribbed",
        "scalloped", "scrolled", "seamed",
        "spangled", "splinted", "studded",
        "tasselled", "tessellated", "thatched",
        "trellised", "tufted", "veined",
        "wattled", "whorled", "winged",
        "zoned", "felted", "spindled",
        "spiralled",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "crankily", "grouchily", "churlishly",
        "boorishly", "rudely", "hostilely",
        "antagonistically", "scoffingly", "sneeringly",
        "jeeringly", "tauntingly", "abjectly",
        "abstrusely", "acerbically", "acquiescently",
        "acrimoniously", "adroitly", "agitatedly",
        "alarmingly", "ambitiously", "amorously",
        "amusingly", "anarchically", "angelically",
        "animatedly", "annoyingly", "appallingly",
        "appealingly", "appreciatively", "apprehensively",
        "approvingly", "ardently", "arguably",
        "arrogantly", "articulately", "artificially",
        "artistically", "assertively", "astoundingly",
        "attentively", "attractively", "austerely",
        "avidly", "bashfully", "beseechingly",
        "blissfully", "boastfully", "brightly",
        "brilliantly", "busily", "calculatingly",
        "capriciously", "ceremoniously", "challengingly",
        "charmingly", "cheaply", "childishly",
        "chirpily", "chivalrously", "circularly",
        "civilly", "clammily", "cleanly",
        "cleverly", "coarsely", "colourfully",
        "comfortably", "commandingly", "commonly",
        "compactly", "compassionately", "competitively",
        "complacently", "complexly", "comprehensively",
        "compulsively", "conceitedly", "concentratedly",
        "concernedly", "concertedly", "concisely",
        "condemnably", "condescendingly", "confidentially",
        "conformably", "congenially", "considerately",
        "consistently", "consolingly", "constantly",
        "constitutionally", "constructively", "contemptibly",
        "contentedly", "continually", "continuously",
        "contradictorily", "contrarily", "conveniently",
        "conventionally", "conversely", "convincingly",
        "coquettishly", "cosily", "courteously",
        "coweringly", "coyly", "crassly",
        "crazily", "creatively", "credibly",
        "creepily", "crisply", "critically",
        "crookedly", "crudely", "cryptically",
        "currently", "cursedly", "customarily",
        "cynically", "daintily", "damply",
        "dangerously", "dapperly",
    ))

    WINDOW_PLACES = dict.fromkeys((
        "academy", "aerodrome", "cabana",
        "cafe", "cafeteria", "campanile",
        "campus", "canteen", "capitol",
        "chalet", "chateau", "circus",
        "college", "colony", "customs",
        "fountain", "landing", "martello",
        "palazzo", "pigeonhouse", "promenade",
        "pyramid", "quay", "rampart",
        "viaduct", "wharf",
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
            _scan(mod, "Records cannot be electroplated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are electroplated by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot truculently be altered "
            "after writing."))
        self.assertFalse(
            _scan(mod, "Records cannot be spiced by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be starched by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are stencilled by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanGoverningFixR33Tests(unittest.TestCase):
    """Ruling 1890: governing condition limb."""

    PHRASING_WORDS = dict.fromkeys((
        "under the baton of", "by the baton of", "under the whip of",
        "by the yoke of", "under the wand of", "under the staff of",
        "under the crozier of", "under the crosier of", "under the mace of",
        "by the mace of", "under the signet of", "under the sceptre and orb of",
        "under the orb of", "by the orb of", "under the fist of",
        "under the gauntlet of", "under the lash and rod of", "under the sword of",
        "by the sword of", "under the banner of", "by the banner of",
        "under the standard of", "under the ensign of", "under the colours of",
        "under the flag of", "by the flag of", "by the ion of",
        "by the absolution of", "by the accession of", "by the accord of",
        "by the adjudication of", "by the admonition of", "by the adoption of",
        "by the affirmation of", "by the allowance of", "by the amendment of",
        "by the announcement of", "by the arbitration of", "by the arrangement of",
        "by the assertion of", "by the assessment of", "by the assumption of",
        "by the assurance of", "by the attestation of", "by the authorisation of",
        "by the authorization of", "under the ion of", "under the absolution of",
        "under the accession of", "under the accord of", "under the adjudication of",
        "under the admonition of", "under the adoption of", "under the affirmation of",
        "under the allowance of", "under the amendment of", "under the announcement of",
        "under the arbitration of", "under the arrangement of", "under the assertion of",
        "under the assessment of", "under the assumption of", "under the assurance of",
        "under the attestation of", "under the authorisation of", "under the authorization of",
        "under the acquiescence of", "under the appointment of", "under the assignment of",
    ))

    TRAILING_FORMS = dict.fromkeys((
        "in whatsoever parish the deployment confinement fact holds", "through whatsoever parish the deployment confinement fact holds", "in whatsoever county the deployment confinement fact holds",
        "through whatsoever county the deployment confinement fact holds", "in whatsoever shire the deployment confinement fact holds", "through whatsoever shire the deployment confinement fact holds",
        "in whatsoever borough the deployment confinement fact holds", "for whatsoever term the deployment confinement fact holds", "for whatsoever duration the deployment confinement fact holds",
        "in whatsoever era the deployment confinement fact holds", "through whatsoever era the deployment confinement fact holds", "by whatsoever path the deployment confinement fact holds",
        "through whatsoever pass the deployment confinement fact holds", "in whatsoever valley the deployment confinement fact holds", "through whatsoever valley the deployment confinement fact holds",
        "in whatsoever harbour the deployment confinement fact holds", "in whatsoever haven the deployment confinement fact holds", "for whatsoever season the deployment confinement fact holds",
        "in whatsoever season the deployment confinement fact holds", "by whatsoever channel the deployment confinement fact holds", "through whatsoever channel the deployment confinement fact holds",
    ))

    TRAILING_CONF_FORMS = dict.fromkeys((
        "howsoever and when", "howsoever and wheresoever", "howsoever and wherever",
    ))

    GOVERNED = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in PHRASING_WORDS)

    TRAILING = tuple(
        "The seal guarantees protection %s." % form
        for form in TRAILING_FORMS) + tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact holds." % form
        for form in TRAILING_CONF_FORMS)

    WEATHER = tuple(
        "The seal guarantees protection %s the weather "
        "of the day." % phrase for phrase in PHRASING_WORDS)

    TRAILING_WEATHER = tuple(
        statement.replace(
            "the deployment confinement fact holds",
            "the weather holds") for statement in TRAILING)

    def test_phrasings_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_trailing_forms_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.TRAILING:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_conditions_still_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER + self.TRAILING_WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the reign of "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection in whatsoever manner "
            "the deployment confinement fact holds."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR33Tests(unittest.TestCase):
    """Ruling 1891: prefixed compound limb."""

    PREFIX_WORDS = dict.fromkeys((
        "stibo", "vanado", "mangano",
        "cobalto", "mercurio", "cadmio",
        "baryto", "strontio", "alumino",
        "magneso", "calcico", "potassio",
        "sodico", "lithio", "germano",
        "gallo", "indico", "thallo",
        "iridio", "pallado", "rhodio",
        "rutheno", "niobo", "tungsto",
        "rhenio", "hafnio", "lanthano",
        "cerio", "praseo", "neodymo",
        "samario", "europio", "gadolino",
        "terbio", "holmio", "erbio",
        "thulio", "ytterbio", "lutetio",
        "actino", "adeno", "balneo",
        "bary", "brady", "caryo",
        "celo", "cerebro", "cervico",
        "choro", "cito", "colpo",
        "coreo", "costo", "cranio",
        "crystallo", "dextro", "dino",
        "dorsi", "dorso", "gnatho",
        "gono", "gyno", "iatro",
        "iono", "kero", "kinesi",
        "kinesio", "labio", "lamino",
        "leio", "leipo", "loco",
        "mammo",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "verawood", "arganwood", "corkwood",
        "pumicewood", "alderwood", "gumwood",
        "abura", "afrormosia", "agba",
        "almondwood", "amendoim", "angelique",
        "anigre", "apitong", "avodire",
        "balau", "balsam", "banak",
        "baobab", "larchwood", "laurelwood",
        "lilacwood", "limewood", "sprucewood",
    ))

    PREFIXES = tuple(
        "Every record stands %sverified before use." % word
        for word in PREFIX_WORDS) + tuple(
        "Every record stands %schecked before use." % word
        for word in PREFIX_WORDS) + (
        "Every record stands dysprochecked before use.",)

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % word
        for word in FIRST_ELEMENTS)

    def test_prefixes_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIXES:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ELEMENTS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Every record stands phylloverified before use."))
        self.assertFalse(
            _scan(mod, "Every record stands satinwood-verified before use."))
        self.assertFalse(
            _scan(mod, "Every record stands dysproverified before use."))
        self.assertFalse(
            _scan(mod, "Every record stands verified before use."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR33Tests(unittest.TestCase):
    """Ruling 1892: concept root list and un wording limb."""

    WORDINGS = dict.fromkeys((
        "unwebbed", "unthatched", "unslated",
        "unstuccoed", "unwainscoted", "undomed",
        "unarched", "uncolumned", "unbalustraded",
        "unditched", "untrenched", "unbanked",
        "undammed", "undleveed", "unbermed",
        "unreveted", "unfaced", "uninsulated",
        "unlagged", "unclad", "wrinkeresistant",
        "verminresistant", "borerproof", "lightningresistant",
        "quakeresistant", "vandalresistant", "theftresistant",
        "coalproof", "cobwebproof", "featherproof",
        "filthproof", "forkproof", "gallproof",
        "goreproof", "gravelproof", "hookproof",
        "lanceproof", "leafproof", "nettleproof",
        "oakproof", "pebbleproof", "pitchproof",
        "quillproof", "razorproof", "reedproof",
        "resinproof", "rootproof", "sapproof",
        "screwproof", "seaproof", "serpentproof",
        "shaleproof", "siltproof", "soapproof",
        "spongeproof", "springproof", "sproutproof",
        "stakeproof", "strawproof", "stringproof",
        "swampproof", "tarproof", "timberproof",
        "trapproof", "treeproof", "trenchproof",
        "troutproof", "twigproof", "vineproof",
        "wadproof", "walnutproof", "wandproof",
        "waxproof", "yeastproof", "arrowresistant",
        "bladeresistant", "blizzardresistant", "cinderresistant",
        "clawresistant", "climateresistant", "coalresistant",
        "cobwebresistant", "daggerresistant", "dewresistant",
        "emberresistant", "fangresistant", "featherresistant",
        "filthresistant", "foamresistant", "fogresistant",
        "forkresistant", "gallresistant", "goreresistant",
        "gravelresistant", "gritresistant", "hookresistant",
        "ironresistant", "lanceresistant", "leafresistant",
        "leatherresistant", "nailresistant", "needleresistant",
        "nettleresistant", "oakresistant", "pebbleresistant",
        "pineresistant", "pitchresistant", "pollenresistant",
        "quillresistant", "razorresistant", "reedresistant",
        "resinresistant", "rockresistant", "rootresistant",
        "sapresistant", "scaleresistant", "scorpionresistant",
        "screwresistant", "searesistant", "serpentresistant",
        "shaleresistant", "shellresistant", "siltresistant",
        "slateresistant", "sleetresistant", "snailresistant",
        "snakeresistant", "soapresistant", "spearresistant",
        "spiderresistant", "spikeresistant", "splashresistant",
        "spongeresistant", "sprayresistant", "springresistant",
        "sproutresistant", "stabresistant", "stakeresistant",
        "steelresistant", "stingresistant", "stoneresistant",
        "stormresistant", "strawresistant", "stringresistant",
        "surgeresistant", "swampresistant", "swordresistant",
        "timberresistant", "tinresistant", "torrentresistant",
        "trapresistant", "treeresistant", "trenchresistant",
        "troutresistant", "twigresistant", "vineresistant",
        "voiceresistant", "wadresistant", "walnutresistant",
        "wandresistant", "wardresistant", "waveresistant",
        "waxresistant", "weedresistant", "weevilresistant",
        "wetresistant", "whaleresistant", "wheatresistant",
        "wheelresistant", "whipresistant", "whirlresistant",
        "whirlwindresistant", "woodresistant", "woolresistant",
        "wormresistant", "xrayresistant", "yeastresistant",
        "zincresistant", "unbarbed", "unbeaded",
        "unberibboned", "unblindfolded", "unblockaded",
        "unbreeched", "uncoiffed", "uncordoned",
        "uncostumed", "uncravatted", "undiademed",
        "undiapered",
    ))

    RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in WORDINGS)

    STORE = tuple(
        "The store is %s." % word for word in WORDINGS)

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
        self.assertFalse(
            _scan(mod, "The records are unescorted by outside writers."))
        self.assertFalse(_scan(mod, "The store is unescorted."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanAssertedFixR33Tests(unittest.TestCase):
    """Ruling 1893: asserted form limb."""

    VERB_WORDS = dict.fromkeys((
        "glimmers", "flares", "coruscates",
        "scintillates", "filtrates", "osmoses",
        "permeates", "pervades", "suffuses",
        "imbues", "steeps", "perspires",
        "respires", "transpires", "lactates",
        "suppurates", "ulcerates", "festers",
        "flakes", "cracks", "splits",
        "ruptures", "fractures", "shatters",
        "splinters", "tears", "rips",
        "accretes", "agglomerates", "agglutinates",
        "aggregates", "amalgamates", "calcifies",
        "caramelizes", "carbonates", "carbonizes",
        "catalyzes", "cauterizes", "chlorinates",
        "coalesces", "coheres", "composts",
        "concentrates", "concretes", "dehydrates",
        "desalinates", "desulfurizes", "detoxifies",
        "devitrifies", "dialyzes", "dimerizes",
        "emulsifies", "esterifies", "fluorinates",
        "fossilizes", "fractionates", "gelatinizes",
        "granulates", "graphitizes", "homogenizes",
        "hydrates", "hydrogenates", "hydrolyses",
        "hydrolyzes", "hydroxylates", "isomerizes",
        "lactonizes", "leaches", "lignifies",
        "lyophilizes", "macerates", "magnetizes",
        "melanizes", "mercerizes", "metabolizes",
        "mineralizes", "nitrates", "nitrifies",
        "oxidises", "ozonizes", "pasteurizes",
        "peptizes", "petrifies", "phosphates",
        "plastinates", "polymerises", "polymerizes",
        "proteolyzes", "pulverizes", "pyrolyzes",
        "racemizes", "recrystallizes", "saccharifies",
        "salinizes", "saponifies", "saturates",
        "sediments", "silicifies", "sinters",
        "solubilizes", "solvates", "sublimates",
        "sulfates", "sulfonates", "sulphates",
        "sulphonates", "vulcanises", "vulcanizes",
    ))

    VERBS = tuple(
        "The journal %s integrity for every reader." % word
        for word in VERB_WORDS)

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERBS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "The journal undulates integrity for every reader."))
        self.assertTrue(
            _scan(mod, "Integrity label for the journal schedule."))


class SealClaimScanMarkerFixR33Tests(unittest.TestCase):
    """Ruling 1894: unconditional marker limb."""

    APPENDED_WORDINGS = dict.fromkeys((
        "until hell freezes over", "when hell freezes over", "while the sun shines",
        "while rivers run", "as long as rivers run", "in rain and shine",
        "for ages and ages", "as long as time endures", "till the last trumpet",
        "while the moon endures", "while the tides roll", "as long as the tides roll",
        "while the rivers flow", "till the wells run dry", "in joy and sorrow",
        "through tears and laughter", "for love nor money", "through foul and fair",
        "in foul and fair", "from kingdom come", "as long as grass grows",
        "as long as the earth endures", "as long as the heavens endure", "as long as the seas shall last",
        "as long as the world shall stand", "for as long as the sun rises", "for the life of the earth",
        "for the whole of time", "in all the ages", "in every generation",
        "through the life of the earth", "through the whole of time", "till the earth ends",
        "till the final day", "till the heavens crumble", "till the life of the earth ends",
        "till the mountains fall", "until judgment day", "until the earth ends",
        "until the final day", "until the mountains fall", "until the oceans dry",
        "until time itself stops",
    ))

    COMMA_WORDINGS = dict.fromkeys((
        "until hell freezes over", "when hell freezes over", "while the sun shines",
        "while rivers run", "as long as rivers run", "in rain and shine",
        "for ages and ages", "till the last trumpet", "while the tides roll",
        "as long as the tides roll", "while the rivers flow", "till the wells run dry",
        "in joy and sorrow", "through tears and laughter", "for love nor money",
        "through foul and fair", "in foul and fair", "from kingdom come",
        "until the last trumpet", "till the tide turns forever", "as long as grass grows",
        "as long as the heavens endure", "as long as the seas shall last", "as long as the world shall stand",
        "for as long as the sun rises", "for the life of the earth", "for the whole of time",
        "in all the ages", "in every generation", "through the life of the earth",
        "through the whole of time", "till the earth ends", "till the final day",
        "till the heavens crumble", "till the life of the earth ends", "till the mountains fall",
        "until judgment day", "until the earth ends", "until the final day",
        "until the mountains fall", "until the oceans dry", "until time itself stops",
    ))

    APPENDED = tuple(
        _GOVERNED_CLAIM + " %s." % wording
        for wording in APPENDED_WORDINGS)

    COMMA = tuple(
        _GOVERNED_CLAIM + ", %s" % wording
        for wording in COMMA_WORDINGS)

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
            mod, _GOVERNED_CLAIM + ", right or wrong"))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + " until the last trumpet."))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + " till the tide turns forever."))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + ", as long as time endures"))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + ", while the moon endures"))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + ", as long as the earth endures"))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanNegationFixR33Tests(unittest.TestCase):
    """Ruling 1895: negation narrowing limb."""

    REPG_ROOTS = dict.fromkeys((
        "annexed", "impounded", "subpoenaed",
        "lodged",
    ))

    CONF_CAN_BE = dict.fromkeys((
        "bandaged", "carved", "chained",
        "cleared", "compiled", "compressed",
        "delivered", "enamelled", "highlighted",
        "identified", "located",
    ))

    CONF_IS = dict.fromkeys((
        "bandagable", "categorizable", "chainable",
        "clearable", "collectable", "compilable",
        "compressible", "deliverable", "enamellable",
        "flaggable", "graphable", "highlightable",
    ))

    NO_FORMS = tuple(
        "No record is %s after writing." % word
        for word in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % word
        for word in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % word
        for word in CONF_CAN_BE) + tuple(
        "No record is %s after writing." % word
        for word in CONF_IS)

    ASSERTED = tuple(
        "Records are %s after writing." % word
        for word in REPG_ROOTS) + tuple(
        "Records are %s after writing." % word
        for word in CONF_CAN_BE) + tuple(
        "The record is %s after writing." % word
        for word in CONF_IS)

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
        self.assertTrue(
            _scan(mod, "No bundle name was hidden in this record."))
        self.assertFalse(
            _scan(mod, "Records are hidden by outsiders."))
        self.assertFalse(_scan(mod, "No data leaves the store."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanConceptRootsFixR33Tests(unittest.TestCase):
    """Ruling 1896: roots outside the judged concept roots."""

    REPG_ROOTS = dict.fromkeys((
        "beaconed", "downlinked", "hocked",
        "rebated", "teleported", "telexed",
        "tokenised", "uplinked", "classified",
        "coded", "deposed", "escrowed",
        "issued", "keyed", "numbered",
        "paginated", "qr-coded", "typewritten",
        "bussed", "clouded", "patched",
        "servered", "switched", "vanned",
    ))

    CONF_ROOTS = dict.fromkeys((
        "activatable", "addressable", "aggregable",
        "allocatable", "analyzable", "animatable",
        "approximable", "arbitrable", "assignable",
        "automatable", "averagable", "backupable",
        "batchable", "bindable", "blendable",
        "bundleable", "calculable", "calibratable",
        "cancelable", "channelable", "chargeable",
        "chunkable", "cipherable", "claimable",
        "classable", "clusterable", "codeable",
        "colorable", "combinable", "computable",
        "concatenable", "deduplicatable", "deformable",
        "delegable", "derivable", "detachable",
        "dialable", "dictable", "digestable",
        "digitalizable", "dimensionable", "disableable",
        "discardable", "discoverable", "displayable",
        "emulatable", "enableable", "enforceable",
        "enrichable", "estimable", "evaluable",
        "exchangeable", "executable", "exercisable",
        "exhaustible", "explainable", "expressable",
        "extendable", "fabricable", "facsimilable",
        "fileable", "findable", "flattenable",
        "fragmentable", "freezable", "fulfillable",
        "generatable", "governable", "gradable",
        "groupable", "hostable",
    ))

    CONF_VERBS = dict.fromkeys((
        "activated", "allocated", "analyzed",
        "animated", "approximated", "automated",
        "averaged", "batched", "blended",
        "calibrated", "canceled", "chunked",
        "ciphered", "clustered", "coded",
        "combined", "concatenated", "deduplicated",
        "deformed", "delegated", "detached",
        "dialed", "digested", "dimensioned",
        "disabled", "discarded", "emulated",
        "enabled", "enforced", "enriched",
        "exchanged", "executed", "exercised",
        "extended", "flattened", "fragmented",
        "fulfilled", "generated", "grouped",
        "indicated", "induced", "inferred",
        "inflated", "informed", "ingested",
        "inherited", "initiated", "injected",
        "inputted", "installed", "instanced",
        "integrated", "interfaced", "interleaved",
        "interrogated", "intersected", "intervened",
        "introduced", "invalidated", "inverted",
    ))

    F2_CAN_BE = dict.fromkeys((
        "antiqued", "appliqued", "barbed",
        "beaded", "bevelled", "blotched",
        "cambered", "chased", "chiselled",
        "cleated", "clinched", "coiled",
        "encrusted", "featherstitched", "ferruled",
        "filigreed", "filleted", "ribbed",
        "scalloped", "scrolled", "seamed",
        "spangled", "splinted", "studded",
        "tasselled", "tessellated", "thatched",
        "trellised", "tufted", "veined",
        "wattled", "whorled", "winged",
        "zoned", "felted", "spindled",
        "spiralled",
    ))

    F2_IS = dict.fromkeys((
        "antiquable", "appliquable", "barbable",
        "beadable", "bevellable", "blotchable",
        "camberable", "chasable", "chisellable",
        "cleatable", "clinchable", "coilable",
        "encrustable", "featherstitchable", "ferrulable",
        "filigreable", "filletable", "ribbable",
        "scallopable", "seamable", "spanglable",
        "splintable", "studdable", "tassellable",
        "tessellatable", "thatchable", "trellisable",
        "tuftable", "veinable", "wattlable",
        "whorlable", "wingable", "zonable",
        "feltable", "spindlable", "spirallable",
    ))

    REPG_FORMS = tuple(
        form % word for word in REPG_ROOTS for form in (
            "No record is %s after writing.",
            "No record can be %s after writing.",
            "Records are %s after writing."))

    CONF_ROOT_FORMS = tuple(
        form % word for word in CONF_ROOTS for form in (
            "The record is %s after writing.",
            "No record is %s after writing."))

    CONF_VERB_FORMS = tuple(
        form % word for word in CONF_VERBS for form in (
            "Records are %s after writing.",
            "No record can be %s after writing."))

    F2_FORMS = tuple(
        "No record can be %s after writing." % word
        for word in F2_CAN_BE) + tuple(
        "No record is %s after writing." % word
        for word in F2_IS)

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

    def test_finding2_no_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.F2_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records are excerpted after writing."))
        self.assertFalse(
            _scan(mod, "No record is excerpted after writing."))
        self.assertFalse(
            _scan(mod, "Records are leased after writing."))
        self.assertFalse(
            _scan(mod, "No record can be leased after writing."))
        self.assertFalse(
            _scan(mod, "Records are rescanned after writing."))
        self.assertFalse(
            _scan(mod, "No record can be stencilled after writing."))
        self.assertFalse(
            _scan(mod, "No record is scrollable after writing."))
        self.assertFalse(
            _scan(mod, "No record is stencillable after writing."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

