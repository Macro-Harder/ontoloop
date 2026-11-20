"""Fix round 35, Region 1: report seal claim scan pins.

Rulings 2158 to 2165 of the Round 35 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R35-REPG-1 to 8 and the Confinement paper findings
S15-R35-CONF-1 to 11 in their absorbed limbs, on the
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

class SealClaimScanInabilityFixR35Tests(unittest.TestCase):
    """Ruling 2158: inability limb, followers and windows."""

    MODAL_REPG_WORDS = dict.fromkeys((
        "pounced", "repoussed", "damascened",
        "nielloed", "cobalted", "leaded",
        "zincified", "phosphated",
    ))

    MODAL_CONF_WORDS = dict.fromkeys((
        "earthed", "ebonized", "effaced",
        "electrified", "electroformed", "elongated",
        "enlarged", "entangled", "excavated",
        "exteriorized", "faced", "faceted",
        "facetted", "enriched", "expanded",
        "extended",
    ))

    ASSERTED_WORDS = dict.fromkeys((
        "pounced", "repoussed", "damascened",
        "nielloed", "cobalted", "leaded",
        "zincified", "phosphated", "earthed",
        "ebonized", "effaced", "electrified",
        "electroformed", "elongated", "enlarged",
        "entangled", "excavated", "exteriorized",
        "faced", "faceted", "facetted",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "mordantly", "vitriolically", "menacingly",
        "threateningly", "balefully", "blackly",
        "lividly", "heatedly", "hotly",
        "ideally", "ignorantly", "illustriously",
        "immediately", "immensely", "impartially",
        "impeccably", "imperfectly", "impersonally",
        "implicitly", "impossibly", "impressively",
        "improbably", "impulsively", "inactively",
        "inadequately", "inappropriately", "inaudibly",
        "incidentally", "incoherently", "inconclusively",
        "inconveniently", "incorrectly", "indecently",
        "independently", "indiscreetly", "indistinctly",
        "indolently", "indubitably", "indulgently",
        "ineffably", "ineffectively", "inefficiently",
        "inelegantly", "ineloquently", "ineptly",
        "inescapably", "inevitably", "inexactly",
        "inexcusably", "inexhaustibly", "inexorably",
        "inexpensively", "inexpertly", "inexplicably",
        "inexpressibly", "inextricably", "infallibly",
        "infamously", "infectiously", "infinitely",
        "infirmly", "informally", "infrequently",
        "ingeniously", "ingenuously", "ingloriously",
        "injudiciously", "injuriously", "innocently",
        "innocuously", "inoffensively", "inopportunely",
        "inordinately", "inquisitively", "insanely",
        "insatiably", "inscrutably", "insecurely",
        "insensibly", "insensitively", "inseparably",
        "insidiously", "insignificantly", "insincerely",
        "insipidly", "insistently", "instinctively",
        "instructively", "instrumentally", "insufficiently",
        "insultingly", "insuperably", "intactly",
        "intangibly", "integrally", "intellectually",
        "intelligently", "intelligibly", "intensely",
        "intensively", "interactively", "interestingly",
        "intermittently", "intricately", "intuitively",
        "involuntarily", "inwardly", "irately",
        "ironically", "irrationally", "irregularly",
        "irresistibly", "irresolutely", "irresponsibly",
        "irritatingly",
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
        self.assertFalse(
            _scan(mod, "Records are electroplated by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot truculently be altered "
            "after writing."))
        for word in ("enriched", "expanded", "extended"):
            self.assertFalse(_scan(
                mod, "Records are %s by outsiders." % word))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanGoverningFixR35Tests(unittest.TestCase):
    """Ruling 2159: governing condition limb."""

    PHRASINGS = dict.fromkeys((
        "by the staff of", "by the wand of",
        "by the axe of", "under the axe of",
        "by the spear of", "under the spear of",
        "by the shield of", "under the shield of",
        "by the helm of", "under the helm of",
        "by the signet of", "by the signet ring of",
        "under the signet ring of", "by the chop of",
        "under the chop of", "by the tally of",
        "under the tally of", "by the countersign of",
        "under the countersign of", "by the password of",
        "under the password of", "by the watchword of",
        "under the watchword of", "by the glove of",
        "under the glove of", "by the gauntlet of",
        "by the entitlement of", "by the enumeration of",
        "by the enunciation of", "by the escalation of",
        "by the estimation of", "by the evaluation of",
        "by the examination of", "by the exception of",
        "by the exchange of", "by the exclusion of",
        "by the execution of", "by the exemption of",
        "by the exercise of", "by the exhibition of",
        "by the expansion of", "by the expectation of",
        "by the explanation of", "by the exploration of",
        "by the exposition of", "by the expression of",
        "by the extension of", "by the extraction of",
        "by the fabrication of", "by the facilitation of",
        "by the federation of", "by the filing of",
        "by the finalization of", "by the generation of",
        "by the graduation of", "by the harmonization of",
        "by the hesitation of", "by the identification of",
        "by the illumination of", "by the illustration of",
        "by the imitation of", "by the immersion of",
        "by the immigration of", "by the impairment of",
        "by the implementation of", "by the implication of",
        "by the importation of", "by the impression of",
        "by the imprisonment of", "by the improvement of",
        "by the inauguration of", "by the incarceration of",
        "by the inception of", "by the incision of",
        "by the inclination of", "by the inclusion of",
        "by the incorporation of", "by the increment of",
        "by the incubation of", "by the incursion of",
        "by the indemnification of", "by the indemnity of",
        "by the indication of", "by the induction of",
        "by the indulgence of", "by the industrialization of",
        "by the inference of", "by the infiltration of",
        "by the inflation of", "by the inflection of",
        "by the information of", "by the infringement of",
        "by the infusion of", "by the ingestion of",
        "by the inheritance of", "by the inhibition of",
        "by the initiation of", "by the injection of",
        "by the innovation of", "by the inquiry of",
        "by the inquisition of", "by the inscription of",
        "by the insertion of", "by the inspection of",
        "by the inspiration of", "by the installation of",
        "by the institution of", "by the instrumentation of",
        "by the insulation of", "by the insurance of",
        "by the insurrection of", "by the integration of",
        "by the intensification of", "by the intention of",
        "by the interaction of", "by the intercession of",
        "by the interchange of", "by the interconnection of",
        "by the interdiction of", "by the interest of",
        "by the interference of", "by the interjection of",
        "by the intermission of", "by the interpretation of",
        "by the interrogation of", "by the interruption of",
        "by the intersection of", "by the intervention of",
        "by the interview of", "by the intimation of",
        "by the intimidation of", "by the intonation of",
        "by the introduction of", "by the intrusion of",
        "by the inundation of", "by the invasion of",
        "by the invention of", "by the inventory of",
        "by the inversion of", "by the investigation of",
        "by the invocation of", "by the involvement of",
        "by the irradiation of", "by the irrigation of",
        "by the irritation of", "by the isolation of",
        "by the issuance of", "by the iteration of",
        "by the itinerary of", "by the influence of",
        "under the entitlement of", "under the enumeration of",
        "under the enunciation of", "under the escalation of",
        "under the estimation of", "under the evaluation of",
        "under the examination of", "under the exception of",
        "under the exchange of", "under the exclusion of",
        "under the execution of", "under the exemption of",
        "under the exercise of", "under the exhibition of",
        "under the expansion of", "under the expectation of",
        "under the explanation of", "under the exploration of",
        "under the exposition of", "under the expression of",
        "under the extension of", "under the extraction of",
        "under the fabrication of", "under the facilitation of",
        "under the federation of", "under the filing of",
        "under the finalization of", "under the generation of",
        "under the graduation of", "under the harmonization of",
        "under the hesitation of", "under the identification of",
        "under the illumination of", "under the illustration of",
        "under the imitation of", "under the immersion of",
        "under the immigration of", "under the impairment of",
        "under the implementation of", "under the implication of",
        "under the importation of", "under the impression of",
        "under the imprisonment of", "under the improvement of",
        "under the inauguration of", "under the incarceration of",
        "under the inception of", "under the incision of",
        "under the inclination of", "under the inclusion of",
        "under the incorporation of", "under the increment of",
        "under the incubation of", "under the incursion of",
        "under the indemnification of", "under the indemnity of",
        "under the indication of", "under the induction of",
        "under the indulgence of", "under the industrialization of",
        "under the inference of", "under the infiltration of",
        "under the inflation of", "under the inflection of",
        "under the information of", "under the infringement of",
        "under the infusion of", "under the ingestion of",
        "under the inheritance of", "under the inhibition of",
        "under the initiation of", "under the injection of",
        "under the innovation of", "under the inquiry of",
        "under the inquisition of", "under the inscription of",
        "under the insertion of", "under the inspection of",
        "under the inspiration of", "under the installation of",
        "under the institution of", "under the instrumentation of",
        "under the insulation of", "under the insurance of",
        "under the insurrection of", "under the integration of",
        "under the intensification of", "under the intention of",
        "under the interaction of", "under the intercession of",
        "under the interchange of", "under the interconnection of",
        "under the interdiction of", "under the interest of",
        "under the interference of", "under the interjection of",
        "under the intermission of", "under the interpretation of",
        "under the interrogation of", "under the interruption of",
        "under the intersection of", "under the intervention of",
        "under the interview of", "under the intimation of",
        "under the intimidation of", "under the intonation of",
        "under the introduction of", "under the intrusion of",
        "under the inundation of", "under the invasion of",
        "under the invention of", "under the inventory of",
        "under the inversion of", "under the investigation of",
        "under the invocation of", "under the involvement of",
        "under the irradiation of", "under the irrigation of",
        "under the irritation of", "under the isolation of",
        "under the issuance of", "under the iteration of",
        "under the itinerary of",
    ))

    TRAILING = dict.fromkeys((
        "in whatsoever precinct the deployment confinement fact holds",
        "through whatsoever precinct the deployment confinement fact holds",
        "in whatsoever canton the deployment confinement fact holds",
        "through whatsoever canton the deployment confinement fact holds",
        "in whatsoever commune the deployment confinement fact holds",
        "through whatsoever commune the deployment confinement fact holds",
        "in whatsoever municipality the deployment confinement fact holds",
        "through whatsoever municipality the deployment confinement fact holds",
        "in whatsoever settlement the deployment confinement fact holds",
        "through whatsoever settlement the deployment confinement fact holds",
        "in whatsoever outpost the deployment confinement fact holds",
        "through whatsoever outpost the deployment confinement fact holds",
        "in whatsoever colony the deployment confinement fact holds",
        "through whatsoever colony the deployment confinement fact holds",
        "in whatsoever protectorate the deployment confinement fact holds",
        "through whatsoever protectorate the deployment confinement fact holds",
        "in whatsoever enclave the deployment confinement fact holds",
        "through whatsoever enclave the deployment confinement fact holds",
        "in whatsoever frontier the deployment confinement fact holds",
        "through whatsoever frontier the deployment confinement fact holds",
        "in whatsoever borderland the deployment confinement fact holds",
        "through whatsoever borderland the deployment confinement fact holds",
        "in whatsoever heartland the deployment confinement fact holds",
        "through whatsoever heartland the deployment confinement fact holds",
        "in whatsoever hinterland the deployment confinement fact holds",
        "through whatsoever hinterland the deployment confinement fact holds",
        "in whatsoever lowland the deployment confinement fact holds",
        "through whatsoever lowland the deployment confinement fact holds",
        "in whatsoever highland the deployment confinement fact holds",
        "through whatsoever highland the deployment confinement fact holds",
        "in whatsoever midland the deployment confinement fact holds",
        "through whatsoever midland the deployment confinement fact holds",
        "in whatsoever upland the deployment confinement fact holds",
        "through whatsoever upland the deployment confinement fact holds",
        "in whatsoever prefecture the deployment confinement fact holds",
        "through whatsoever prefecture the deployment confinement fact holds",
        "in whatsoever arrondissement the deployment confinement fact holds",
        "through whatsoever arrondissement the deployment confinement fact holds",
        "in whatsoever department the deployment confinement fact holds",
        "through whatsoever department the deployment confinement fact holds",
        "in whatsoever governorate the deployment confinement fact holds",
        "through whatsoever governorate the deployment confinement fact holds",
        "in whatsoever emirate the deployment confinement fact holds",
        "through whatsoever emirate the deployment confinement fact holds",
        "in whatsoever sultanate the deployment confinement fact holds",
        "through whatsoever sultanate the deployment confinement fact holds",
        "in whatsoever caliphate the deployment confinement fact holds",
        "through whatsoever caliphate the deployment confinement fact holds",
        "in whatsoever bishopric the deployment confinement fact holds",
        "through whatsoever bishopric the deployment confinement fact holds",
        "in whatsoever archdiocese the deployment confinement fact holds",
        "through whatsoever archdiocese the deployment confinement fact holds",
        "in whatsoever presbytery the deployment confinement fact holds",
        "through whatsoever presbytery the deployment confinement fact holds",
        "in whatsoever synod the deployment confinement fact holds",
        "through whatsoever synod the deployment confinement fact holds",
        "in whatsoever conclave the deployment confinement fact holds",
        "through whatsoever conclave the deployment confinement fact holds",
        "through whatsoever borough the deployment confinement fact holds",
        "for whatsoever epoch the deployment confinement fact holds",
        "for whatsoever era the deployment confinement fact holds",
        "for whatsoever aeon the deployment confinement fact holds",
        "for whatsoever century the deployment confinement fact holds",
        "for whatsoever decade the deployment confinement fact holds",
        "for whatsoever lifetime the deployment confinement fact holds",
        "for whatsoever generation the deployment confinement fact holds",
    ))

    TRAILING_CONF = (
        "wherein and howsoever",
        "wherein and wheresoever",
        "wherein and whithersoever",
    )

    GOVERNED = tuple(
        "The seal guarantees protection %s "
        "the deployment confinement fact." % phrase
        for phrase in PHRASINGS) + tuple(
        "The seal guarantees protection %s." % form
        for form in TRAILING) + tuple(
        "The seal guarantees protection %s "
        "the deployment confinement fact holds." % form
        for form in TRAILING_CONF)

    WEATHER = tuple(
        "The seal guarantees protection %s the weather." % phrase
        for phrase in PHRASINGS) + tuple(
        "The seal guarantees protection %s." % form.replace(
            "the deployment confinement fact holds", "the weather holds")
        for form in TRAILING) + tuple(
        "The seal guarantees protection %s the weather holds." % form
        for form in TRAILING_CONF)

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
        for phrase in ("under the staff of", "under the wand of",
                       "under the signet of", "under the gauntlet of",
                       "by the mace of", "under the mace of"):
            self.assertTrue(_scan(
                mod, "The seal guarantees protection %s "
                "the deployment confinement fact." % phrase))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection in whatsoever "
            "borough the deployment confinement fact holds."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the "
            "abjuration of the deployment confinement fact."))
        self.assertFalse(_scan(
            mod, "The seal guarantees protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanCompoundFixR35Tests(unittest.TestCase):
    """Ruling 2160: prefixed compound limb."""

    PREFIXES = dict.fromkeys((
        "actinio", "arachno", "arsenico",
        "borato", "caesio", "calcio",
        "chlorito", "dysprosio", "fungio",
        "gadolinio", "germanio", "hydrargyro",
        "hydroxo", "hypochloro", "indio",
        "litio", "magnesio", "mercapto",
        "nitrito", "osmiumo", "oxo",
        "perchloro", "phosphato", "phosphoro",
        "promethio", "protactinio", "rubidio",
        "selenio", "silicato", "sodio",
        "stibio", "sulfato", "sulfito",
        "technetio", "tellurio", "thallio",
        "thiolo", "trito", "tungsteno",
        "vanadio", "virio", "wolframio",
        "zincio", "latero", "ligno",
        "limno", "lumbo", "lyso",
        "mano", "masto", "medico",
        "medio", "megalo", "melo",
        "mero", "metro", "moto",
        "myxo", "nemato", "nocti",
        "nomo", "nono", "noso",
        "noto", "novo", "nudo",
        "nulli", "nutri", "nycto",
        "occipito", "oeco", "oeno",
        "oleo", "olfacto", "omaso",
        "omento", "omo", "omphalo",
        "oneiro", "onomato", "onycho",
        "oophoro", "opaco", "operculo",
        "opisto", "oplo", "orbi",
        "orbito", "orchido", "orchio",
        "orecto", "oro", "oscheo",
        "oscillo", "osseo", "ovario",
        "ovi", "ovo", "oxalo",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "cocobolowood", "ziricotewood", "bocotewood",
        "leadwood", "mopanewood", "tambotiwood",
        "pangawood", "ovangkolwood", "merbauwood",
        "irokowood", "sapelewood", "utilewood",
        "idigbowood", "afrormosiawood", "agbawood",
        "obechewood", "wawawood", "alstoniawood",
        "antiariswood", "pommelewood", "kataloxwood",
        "chaktewood", "chechenwood", "granadillowood",
        "hormigowood", "jobillowood", "machichewood",
        "nargustawood", "tzalamwood", "massarandubawood",
        "andirobawood", "crabwood", "carapawood",
        "virolawood", "cedrelawood", "khayawood",
        "tiamawood", "kosipowood", "limbawood",
        "frakewood", "ayouswood", "sambawood",
        "tatajubawood", "jatobawood", "tonkawood",
        "santoswood", "aroeirawood", "sucupirawood",
        "angelimwood", "tauariwood", "jequitibawood",
        "copaibawood", "freijowood", "marupawood",
        "simaroubawood", "hawthornwood", "hemlockwood",
        "hornbeamwood", "koawood", "lindenwood",
        "mangowood", "mesquitewood", "monkeypodwood",
        "orangewood", "papayawood", "persimmonwood",
        "pistachiowood", "purpleheartwood", "sequoiawood",
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
            mod, "Every record stands apricotwood-verified "
            "before use."))
        self.assertFalse(_scan(
            mod, "Every record stands verified before use."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanLexiconFixR35Tests(unittest.TestCase):
    """Ruling 2161: concept roots, un and resistant wordings."""

    WORDINGS = dict.fromkeys((
        "unpilastered", "unparapeted", "unembattled",
        "untrellised", "uncolonnaded", "uncupolaed",
        "unsteepled", "ungabled", "uneaved",
        "unbattened", "unpaneled", "unmullioned",
        "untransomed", "unthresholded", "unjambed",
        "unfenestrated", "unclerestoried", "unlanterned",
        "undormered", "unmansarded", "unhipped",
        "unpitched", "unflashed", "unguttered",
        "undownspouted", "earthquakeresistant", "seismicresistant",
        "hurricaneresistant", "infiltrationproof", "camelproof",
        "candleproof", "cattleproof", "charcoalproof",
        "clayproof", "cliffproof", "cloudproof",
        "corkproof", "cornproof", "crabproof",
        "craneproof", "crocodileproof", "dandelionproof",
        "desertproof", "donkeyproof", "doveproof",
        "duckproof", "eagleproof", "eelproof",
        "elkproof", "camelresistant", "candleresistant",
        "caterpillarresistant", "cattleresistant", "charcoalresistant",
        "clayresistant", "cliffresistant", "cloudresistant",
        "cockroachresistant", "cometresistant", "coralresistant",
        "corkresistant", "cornresistant", "coyoteresistant",
        "crabresistant", "craneresistant", "cricketresistant",
        "crocodileresistant", "crowresistant", "cycloneresistant",
        "dandelionresistant", "deerresistant", "desertresistant",
        "dogresistant", "donkeyresistant", "doveresistant",
        "duckresistant", "eagleresistant", "eelresistant",
        "elephantresistant", "elkresistant", "unclenched",
        "unclogged", "unclosed", "uncluttered",
        "uncoated", "uncoiled", "uncompacted",
        "uncompelled", "unconcealed", "uncondensed",
        "unconfined", "unconstrained", "uncontorted",
        "uncontracted", "uncontrolled", "uncooked",
        "uncooled", "uncoordinated", "uncorrected",
        "uncorroded", "uncounted", "uncramped",
        "uncreased", "uncropped", "uncrossed",
        "uncrowded", "uncrumpled", "uncrystallized",
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

class SealClaimScanAssertedFixR35Tests(unittest.TestCase):
    """Ruling 2162: asserted form reading, journal verbs."""

    VERBS = dict.fromkeys((
        "sputters", "reeks", "tempers",
        "quenches", "patinates", "blues",
        "browns", "silvers", "yellows",
        "reddens", "whitens", "blackens",
        "brightens", "fades", "stains",
        "spots", "blotches", "streaks",
        "mottles", "speckles", "hygroscopes",
        "impregnates", "incinerates", "incorporates",
        "incubates", "indurates", "infiltrates",
        "inflates", "infuses", "ingests",
        "injects", "inoculates", "inseminates",
        "inserts", "insulates", "intensifies",
        "intercalates", "interconverts", "interfuses",
        "intermixes", "internalizes", "interpenetrates",
        "interpolates", "ionizes", "irradiates",
        "lacquers", "laminates", "levigates",
        "lithifies", "lixiviates", "lubricates",
        "malts", "marinates", "masticates",
        "matures", "metallizes", "metamorphoses",
        "methylates", "micronizes", "mills",
        "mollifies", "mummifies",
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

class SealClaimScanMarkerFixR35Tests(unittest.TestCase):
    """Ruling 2163: unconditional marker reading."""

    APPENDED_MARKERS = dict.fromkeys((
        "till the sun dies", "until the mountains crumble",
        "till time stands still", "until time stands still",
        "while time lasts", "while the tides turn",
        "till the tides stop", "until the sun burns out",
        "as long as memory lasts", "as long as the rivers flow",
        "as long as the seas endure", "as long as the stones endure",
        "till the stones crumble", "until the stones crumble",
        "as long as the bays stand", "as long as the capes stand",
        "as long as the dunes stand", "as long as the fjords stand",
        "as long as the glaciers stand", "as long as the lagoons stand",
        "as long as the marshes stand", "as long as the meadows stand",
        "as long as the peaks stand", "as long as the reefs stand",
        "as long as the ridges stand", "as long as the savannas stand",
        "as long as the steppes stand", "as long as the tundras stand",
        "as long as the volcanoes stand", "as long as the waterfalls stand",
        "as long as the wetlands stand", "as long as the woodlands stand",
        "till the hills crumble", "until the hills crumble",
        "till the valleys fill", "until the valleys fill",
        "as long as the harbours stand", "as long as the harbors stand",
        "as long as the inlets stand", "as long as the islets stand",
        "as long as the peninsulas stand", "as long as the canyons stand",
        "as long as the gorges stand", "as long as the ravines stand",
        "as long as the deltas stand", "as long as the estuaries stand",
        "as long as the headlands stand", "as long as the sky endures",
        "as long as the land endures", "as long as the plateaus stand",
    ))

    COMMA_MARKERS = dict.fromkeys((
        "till the sun dies", "until the mountains crumble",
        "till time stands still", "until time stands still",
        "while time lasts", "while the tides turn",
        "till the tides stop", "until the sun burns out",
        "as long as memory lasts", "as long as the rivers flow",
        "as long as the seas endure", "as long as the stones endure",
        "till the stones crumble", "until the stones crumble",
        "as long as the bays stand", "as long as the capes stand",
        "as long as the dunes stand", "as long as the fjords stand",
        "as long as the glaciers stand", "as long as the lagoons stand",
        "as long as the marshes stand", "as long as the meadows stand",
        "as long as the peaks stand", "as long as the reefs stand",
        "as long as the ridges stand", "as long as the savannas stand",
        "as long as the steppes stand", "as long as the tundras stand",
        "as long as the volcanoes stand", "as long as the waterfalls stand",
        "as long as the wetlands stand", "as long as the woodlands stand",
        "till the hills crumble", "until the hills crumble",
        "till the valleys fill", "until the valleys fill",
        "as long as the harbours stand", "as long as the harbors stand",
        "as long as the inlets stand", "as long as the islets stand",
        "as long as the peninsulas stand", "as long as the canyons stand",
        "as long as the gorges stand", "as long as the ravines stand",
        "as long as the deltas stand", "as long as the estuaries stand",
        "as long as the headlands stand",
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
            mod, _GOVERNED_CLAIM + " till the mountains crumble."))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + ", till the mountains crumble."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanNegationFixR35Tests(unittest.TestCase):
    """Ruling 2164: negation narrowing, roots judged asserted."""

    REPG_ROOTS = dict.fromkeys((
        "chartered", "devisable", "levied",
        "surveyed", "taxed",
    ))

    CONF_VERBS = dict.fromkeys((
        "cropped", "transformed",
    ))

    NO_FORMS = tuple(
        "No record is %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % verb
        for verb in CONF_VERBS)

    ASSERTED = tuple(
        "Records are %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "Records are %s after writing." % verb
        for verb in CONF_VERBS)

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

class SealClaimScanConceptFixR35Tests(unittest.TestCase):
    """Ruling 2165: roots outside the judged concept roots."""

    REPG_ROOTS = dict.fromkeys((
        "amortisable", "amortizable", "assessed",
        "billable", "budgeted", "calendared",
        "capitalisable", "capitalizable", "conscripted",
        "costed", "deductible", "defendable",
        "demandable", "depreciable", "hypothecable",
        "incorporated", "indemnifiable", "justiciable",
        "licenced", "litigable", "mustered",
        "priced", "prosecutable", "receivable",
        "refundable", "reimbursable", "renewable",
        "revivable", "subrogable", "tolled",
        "waivable",
    ))

    CONF_ROOTS = dict.fromkeys((
        "citable", "compactable", "croppable",
        "enumerable", "illustratable", "imageable",
        "indentable", "inkable", "insertable",
        "invoiceable", "itemizable", "laminatable",
        "letterable", "obscurable", "omittable",
        "paginatable", "panelable", "paperable",
        "paragraphable", "parcelable", "parenthesizable",
        "pencilable", "perforatable", "permutable",
        "pieceable", "pigeonholable", "pigmentable",
        "pilable", "pipable", "pointable",
        "pollable", "poolable", "promotable",
        "promptable", "proofable", "propagatable",
        "propellable", "proposable", "protractible",
        "provable", "prunable", "scorable",
        "scrawlable", "scribable", "spacable",
    ))

    CONF_VERBS = dict.fromkeys((
        "colorized", "compacted", "computed",
        "imaged", "indented", "inked",
        "inserted", "obscured", "omitted",
        "paragraphed", "perforated", "permuted",
        "pieced", "pigeonholed", "pigmented",
        "polled", "pooled", "ported",
        "prefaced", "prefixed", "privileged",
        "probed", "procured", "produced",
        "profiled", "prohibited", "promoted",
        "proofed", "propagated", "proved",
        "provided", "pruned", "scored",
        "scrawled", "scribed", "stripped",
    ))

    FORMS = tuple(
        "No record is %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "Records are %s after writing." % root
        for root in REPG_ROOTS) + tuple(
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
