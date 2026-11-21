"""Fix round 37, Region 1: report seal claim scan pins.

Rulings 2421 to 2438 of the Round 37 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R37-REPG-1 to 8 and the Confinement paper findings
S15-R37-CONF-1 to 10, on the templates those papers
state. The two papers stand severed in this round: no
form stands counted in two rulings, and the convergent
forms stand inside the Confinement rulings alone.
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

_PLAIN_CONTROLS_TRUE = (_GOVERNED_CLAIM + ".",)
_PLAIN_CONTROLS_FALSE = ()

class SealClaimScanInabilityRepGFixR37Tests(unittest.TestCase):
    """Ruling 2421, S15-R37-REPG-1: inability windows and followers."""

    FOLLOWERS = dict.fromkeys((
        "sprayed", "dipped",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "tactfully", "tamely", "tardily",
        "tastefully", "teasingly", "tempestuously",
        "temptingly", "tenaciously", "tensely",
        "tepidly", "terribly", "terrifyingly",
        "tersely", "thickly", "thinly",
        "thirstily", "thoughtlessly", "thriftily",
        "thrillingly", "trivially", "tropically",
        "troublesomely", "trustingly", "turbulently",
        "twitchily",
    ))

    MODAL = tuple(
        "Records cannot be %s after writing." % word
        for word in FOLLOWERS)

    ASSERTED = tuple(
        "Records are %s by outsiders." % word
        for word in FOLLOWERS)

    WINDOWS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in WINDOW_WORDS)

    CONTROL_FALSE = (
        "Records cannot be electroplated by outsiders.",
        "Records cannot truculently be altered after writing.",
        "Records cannot be quilted by outsiders.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "The seal does not guarantee protection.",
    )

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
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanGoverningRepGFixR37Tests(unittest.TestCase):
    """Ruling 2422, S15-R37-REPG-2: trailing governing forms."""

    TRAILING_PLACES = dict.fromkeys((
        "lighthouse", "watchtower",
        "windmill", "watermill",
        "tannery", "brewery",
        "distillery", "refinery",
        "shipyard", "dockyard",
        "timberyard", "brickyard",
    ))

    TRAILING_TIMES = dict.fromkeys((
        "millennium", "year",
        "month", "week",
        "day", "hour",
        "moment",
    ))

    GOVERNED = tuple(
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
        "The seal guarantees protection in whatsoever %s "
        "the weather holds." % place
        for place in TRAILING_PLACES) + tuple(
        "The seal guarantees protection through whatsoever %s "
        "the weather holds." % place
        for place in TRAILING_PLACES) + tuple(
        "The seal guarantees protection for whatsoever %s "
        "the weather holds." % form
        for form in TRAILING_TIMES)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "The seal guarantees protection by the scroll of "
        "the deployment confinement fact.",
    )

    CONTROL_FALSE = (
        "The seal guarantees protection.",
    )

    def test_trailing_stand_governed(self):
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
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)


class SealClaimScanCompoundRepGFixR37Tests(unittest.TestCase):
    """Ruling 2423, S15-R37-REPG-3: prefixed compounds."""

    PREFIXES = dict.fromkeys((
        "urethro", "myringo", "uvulo",
        "zygomato",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "antler", "whalebone",
    ))

    PREFIX_FORMS = tuple(
        "Every record stands %sverified before use." % prefix
        for prefix in PREFIXES) + tuple(
        "Every record stands %schecked before use." % prefix
        for prefix in PREFIXES)

    ELEMENT_FORMS = tuple(
        "Every record stands %s-verified before use." % element
        for element in FIRST_ELEMENTS)

    CONTROL_FALSE = (
        "Every record stands amphiverified before use.",
        "Every record stands verified before use.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

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


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanLexiconRepGFixR37Tests(unittest.TestCase):
    """Ruling 2424, S15-R37-REPG-4: un, proof, resistant wordings."""

    UN_WORDINGS = dict.fromkeys((
        "unstrung",
    ))

    PROOF_WORDINGS = dict.fromkeys((
        "aardvarkproof", "albatrossproof", "anacondaproof",
        "angelfishproof", "antelopeproof", "apeproof",
        "armadilloproof", "axolotlproof", "baboonproof",
        "basiliskproof", "binturongproof", "blackbirdproof",
        "bluebirdproof", "boaproof", "bonoboproof",
        "bullproof", "canaryproof", "capybaraproof",
        "caribouproof", "cassowaryproof", "catfishproof",
        "caymanproof", "chameleonproof", "chimpanzeeproof",
        "chinchillaproof", "chipmunkproof", "cicadaproof",
    ))

    RESIST_WORDINGS = dict.fromkeys((
        "aardvarkresistant", "albatrossresistant", "anacondaresistant",
        "angelfishresistant", "anteloperesistant", "aperesistant",
        "armadilloresistant", "axolotlresistant", "baboonresistant",
        "basiliskresistant", "batresistant", "beaverresistant",
        "binturongresistant", "blackbirdresistant", "bluebirdresistant",
        "boaresistant", "bonoboresistant", "bullresistant",
        "butterflyresistant", "canaryresistant", "capybararesistant",
        "caribouresistant", "cassowaryresistant", "catfishresistant",
        "caymanresistant", "chameleonresistant", "chickenresistant",
        "chimpanzeeresistant", "chinchillaresistant", "chipmunkresistant",
        "cicadaresistant",
    ))

    UN_RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDINGS)

    UN_STORE = tuple(
        "The store is %s." % word
        for word in UN_WORDINGS)

    STORE_WORDINGS = tuple(
        "The store is %s." % word
        for word in list(PROOF_WORDINGS) + list(RESIST_WORDINGS))

    CONTROL_FALSE = (
        "The records are unescorted by outside writers.",
        "The store is unescorted.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_un_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.UN_RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_un_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.UN_STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE_WORDINGS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanAssertedRepGFixR37Tests(unittest.TestCase):
    """Ruling 2425, S15-R37-REPG-5: claim verbs."""

    VERBS = dict.fromkeys((
        "electrolyzes", "iodizes", "blanches",
        "distempers",
    ))

    FORMS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in VERBS)

    CONTROL_FALSE = (
        "The journal narrates integrity for every reader.",
        "The journal undulates integrity for every reader.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "Integrity label for the journal schedule.",
    )

    def test_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanMarkerRepGFixR37Tests(unittest.TestCase):
    """Ruling 2426, S15-R37-REPG-6: unconditional markers."""

    MARKERS = dict.fromkeys((
        "as long as the icecaps stand", "till the glaciers melt",
        "until the icecaps melt", "till the tides turn",
        "until the seasons turn", "while the planets turn",
        "till the comets return", "until the comets return",
        "while the glaciers calve",
    ))

    APPENDED = tuple(
        _GOVERNED_CLAIM + " %s." % marker
        for marker in MARKERS)

    COMMA = tuple(
        _GOVERNED_CLAIM + ", %s." % marker
        for marker in MARKERS)

    CONTROL_FALSE = (
        _GOVERNED_CLAIM + " as long as the rivers run.",
        _GOVERNED_CLAIM + ", as long as the rivers run.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_appended_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.APPENDED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_comma_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMMA:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanNegationRepGFixR37Tests(unittest.TestCase):
    """Ruling 2427, S15-R37-REPG-7: negation narrowing roots."""

    ROOTS = dict.fromkeys((
        "hingeable", "hammerable",
    ))

    NO_FORMS = tuple(
        "No record is %s after writing." % root
        for root in ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in ROOTS)

    ASSERTED_AT_POLE = tuple(
        "Records are %s after writing." % root
        for root in ROOTS)

    CONTROL_FALSE = (
        "No record is harvestable after writing.",
        "No record can be harvestable after writing.",
        "Records are hidden by outsiders.",
        "No data leaves the store.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "The seal does not guarantee protection.",
        "No bundle name was hidden in this record.",
    )

    def test_no_opening_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_analogues_stand_judged(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_AT_POLE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanConceptRepGFixR37Tests(unittest.TestCase):
    """Ruling 2428, S15-R37-REPG-8: roots outside judged roots."""

    ROOTS = dict.fromkeys((
        "gradeable", "grazeable", "greetable",
        "grieveable", "groanable", "grooveable",
        "growable", "guessable", "guideable",
        "gulpable", "gushable", "grindable",
        "hatchable", "healable", "heapable",
        "heatable", "hoistable", "holdable",
    ))

    VERBS = dict.fromkeys((
        "graded", "granted", "grazed",
        "greeted", "grown", "guessed",
        "guided",
    ))

    ROOT_FORMS = tuple(
        "No record is %s after writing." % root
        for root in ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in ROOTS) + tuple(
        "Records are %s after writing." % root
        for root in ROOTS) + tuple(
        "The record is %s after writing." % root
        for root in ROOTS)

    VERB_FORMS = tuple(
        "Records are %s after writing." % verb
        for verb in VERBS) + tuple(
        "No record is %s after writing." % verb
        for verb in VERBS) + tuple(
        "No record can be %s after writing." % verb
        for verb in VERBS)

    CONTROL_FALSE = (
        "Records are excerpted after writing.",
        "No record is excerpted after writing.",
        "Records are leased after writing.",
        "No record can be leased after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_roots_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanWindowConfFixR37Tests(unittest.TestCase):
    """Ruling 2429, S15-R37-CONF-1: window words."""

    WINDOW_WORDS = dict.fromkeys((
        "peculiarly", "perfectly", "pertinently",
        "pervasively", "pessimistically", "piercingly",
        "pleasingly", "plentifully", "pliantly",
        "poetically", "poorly", "popularly",
        "potently", "predominantly", "preferably",
        "prematurely", "presently", "pressingly",
        "prevalently", "primarily", "principally",
        "probably", "productively", "prospectively",
        "prosperously", "provably", "punctually",
        "quaveringly", "quirkily", "radiantly",
        "raggedly", "rampantly", "randomly",
        "rapidly", "raptly", "rationally",
        "raucously", "ravenously", "recently",
        "receptively", "redundantly", "reflectively",
        "refreshingly", "regally", "regionally",
        "regularly", "relatively", "relevantly",
        "religiously", "repellently", "repetitively",
        "repressively", "reputedly", "reservedly",
        "resiliently", "resonantly", "resourcefully",
        "respectably", "respectfully", "responsibly",
        "responsively", "restively", "restrainedly",
        "restrictively", "resultantly", "retaliatorily",
        "reticently", "reverently", "reversely",
        "revoltingly", "rewardingly", "rhapsodically",
        "rhetorically", "rhythmically", "richly",
        "righteously", "rightfully", "rigorously",
        "riotously", "ripely", "riskily",
        "roaringly", "robustly", "rogishly",
        "romantically", "roundly", "rousingly",
        "routinely", "rowdily", "ruggedly",
        "ruinously", "ruminatively", "rurally",
        "sacredly", "sadly", "sagely",
        "saintly", "saliently", "salubriously",
        "salutarily", "sanctimoniously", "sanely",
        "sanguinely", "sapiently", "sarcastically",
        "sardonically", "sartorially", "sassily",
        "satisfactorily", "satisfyingly", "saucily",
        "savorily", "savvily", "scarcely",
        "scarily", "scathingly", "scenically",
        "schematically", "scholastically", "scientifically",
        "scintillatingly", "scurrilously", "secludedly",
        "secondarily", "secretively", "sectarianly",
        "secularly", "sedimentarily", "seditiously",
        "seductively", "seedily", "segmentally",
        "selectively", "selfishly", "semantically",
        "seniorly", "sensationally", "senselessly",
        "sensibly", "sensitively", "sensually",
        "sententiously", "sentimentally", "sequentially",
        "serially", "servilely", "sexily",
        "shabbily", "shadily", "shakily",
        "shallowly", "shapelessly", "shapely",
        "sheepishly", "sheerly", "shimmeringly",
        "shingly", "shockingly", "shoddily",
        "shrilly", "shrinkingly", "shudderingly",
        "shyly", "sickeningly", "sighingly",
        "silkily", "sillily", "simperingly",
        "singingly", "singularly", "sinlessly",
        "sireningly", "sisterly", "situationally",
        "sizzlingly", "skeptically", "skilfully",
        "skillfully", "skimpily", "skittishly",
        "slackly", "slantingly", "slantwise",
        "slapdashly", "slatternly", "slavishly",
        "sleekly", "sleeplessly", "slenderly",
        "slickly", "slightly", "slimily",
        "slimly", "slingingly", "slinkingly",
        "slipperily", "slippily", "slitheringly",
        "slobberingly", "slogingly", "slopingly",
        "sloppily", "sloshingly", "slothfully",
        "sludgily", "slumberingly", "slumbrously",
        "slummily", "slurringly", "slushily",
        "sluttily", "smackingly", "smartingly",
        "smartly", "smearily", "smellily",
        "smilingly", "smirkingly", "smolderingly",
        "smotheringly", "smugly", "smuttily",
        "snakingly", "snarlingly", "snazzily",
        "sneakingly", "sneezingly", "snidely",
        "sniggeringly", "snippily", "snippishly",
        "snitchingly", "snobbishly", "snoopily",
        "snootily", "snoozily", "snoringly",
        "snortingly", "snottily", "snoutily",
        "snubbingly", "snuffily", "snuffingly",
        "snugly", "soapily", "soaringly",
        "sobbingly", "socially", "societally",
        "sociologically", "soddenly", "soggily",
        "sojurningly", "solacingly", "solarily",
    ))

    WINDOWS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in WINDOW_WORDS)

    CONTROL_FALSE = (
        "Records cannot irksomely be altered after writing.",
        "Records cannot ably be altered after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOWS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanFollowerConfFixR37Tests(unittest.TestCase):
    """Ruling 2430, S15-R37-CONF-2: followers."""

    FOLLOWERS_BOTH = dict.fromkeys((
        "baled", "berthed", "crayoned",
        "debossed", "docked", "fired",
        "footed", "gridded", "heaped",
        "kilned", "margined", "ruled",
        "sacked", "shaved", "tiered",
    ))

    MODAL_ONLY = dict.fromkeys((
        "inked", "leashed", "mounted",
        "paginated", "titled",
    ))

    MODAL = tuple(
        "Records cannot be %s after writing." % word
        for word in FOLLOWERS_BOTH)

    ASSERTED = tuple(
        "Records are %s by outsiders." % word
        for word in FOLLOWERS_BOTH)

    MODAL_ONLY_FORMS = tuple(
        "Records cannot be %s after writing." % word
        for word in MODAL_ONLY)

    CONTROL_FALSE = (
        "Records cannot be patinated after writing.",
        "Records are patinated by outsiders.",
        "Records cannot be asphalted after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

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

    def test_modal_only_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_ONLY_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanCompoundConfFixR37Tests(unittest.TestCase):
    """Ruling 2431, S15-R37-CONF-3: prefixed compounds."""

    PREFIXES = dict.fromkeys((
        "calci", "carbo", "fluo",
        "mito", "ped", "pharma",
        "physio", "proteo", "psych",
        "recti", "reni", "reti",
        "septi", "somni", "tauto",
        "tectono", "thalamo", "theo",
        "therio", "tibio", "torso",
        "tribo", "ventri", "vini",
        "volt",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "bark", "bone-china", "papyrus",
        "parchment", "root", "thorn",
        "vellum", "vine",
    ))

    PREFIX_FORMS = tuple(
        "Every record stands %sverified before use." % prefix
        for prefix in PREFIXES) + tuple(
        "Every record stands %schecked before use." % prefix
        for prefix in PREFIXES)

    ELEMENT_FORMS = tuple(
        "Every record stands %s-verified before use." % element
        for element in FIRST_ELEMENTS)

    CONTROL_FALSE = (
        "Every record stands pantoverified before use.",
        "Every record stands zebranowood-verified before use.",
        "Every record stands verified before use.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

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


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanProofConfFixR37Tests(unittest.TestCase):
    """Ruling 2432, S15-R37-CONF-4: proof and resistant wordings."""

    PROOF_WORDINGS = dict.fromkeys((
        "alpacaproof", "bisonproof", "bobcatproof",
        "buffaloproof", "cheetahproof", "cobraproof",
        "dolphinproof", "emuproof", "falconproof",
        "ferretproof", "finchproof", "flamingoproof",
        "gazelleproof", "gerbilproof", "giraffeproof",
        "gnuproof", "gorillaproof", "hamsterproof",
        "hawkproof", "jaguarproof", "jayproof",
        "kiwiproof", "kuduproof", "larkproof",
        "leopardproof", "lobsterproof", "magpieproof",
        "mallardproof", "manateeproof", "marmotproof",
        "martenproof", "meerkatproof", "minkproof",
        "mongooseproof", "muskratproof", "narwhalproof",
        "nightingaleproof", "octopusproof", "okapiproof",
        "orangutanproof", "orcaproof", "oryxproof",
        "ospreyproof", "ostrichproof", "oysterproof",
        "pangolinproof", "parakeetproof", "partridgeproof",
        "peccaryproof", "pheasantproof", "pikaproof",
        "pikeproof", "ploverproof", "polecatproof",
        "porpoiseproof", "possumproof", "prawnproof",
        "pronghornproof", "puffinproof", "pumaproof",
        "quetzalproof", "quokkaproof", "railproof",
        "ramproof", "rattlesnakeproof", "rayproof",
        "reindeerproof", "rheaproof", "robinproof",
        "roosterproof", "sableproof", "salamanderproof",
        "sardineproof", "seahorseproof", "servalproof",
        "shrimpproof", "skinkproof", "slothproof",
        "snipeproof", "snowleopardproof", "soleproof",
        "sparrowproof", "spoonbillproof", "squidproof",
        "starlingproof", "stingrayproof", "stoatproof",
        "sturgeonproof", "swallowproof", "swiftproof",
        "swordfishproof", "tahrproof", "tamarinproof",
        "tapirproof", "tarantulaproof", "tarsierproof",
        "tasmaniandevilproof", "tealproof", "tenrecproof",
        "ternproof", "thrushproof", "tilapiaproof",
        "toucanproof", "tunaproof", "turnstoneproof",
        "vicunaproof", "warthogproof", "waterbuffaloproof",
        "weaverproof", "whelkproof", "whippetproof",
        "wigeonproof", "wildcatproof", "wilddogproof",
        "wildebeestproof", "wolverineproof", "woodcockproof",
        "woodpeckerproof", "wrasseproof", "wrenproof",
        "zebuproof", "zorillaproof",
    ))

    RESIST_WORDINGS = dict.fromkeys((
        "alpacaresistant", "badgerresistant", "beaverresistant",
        "bisonresistant", "bobcatresistant", "buffaloresistant",
        "catresistant", "cheetahresistant", "cobraresistant",
        "dolphinresistant", "emuresistant", "falconresistant",
        "ferretresistant", "finchresistant", "flamingoresistant",
        "frogresistant", "gazelleresistant", "gerbilresistant",
        "girafferesistant", "gnuresistant", "gorillaresistant",
        "hamsterresistant", "hawkresistant", "hornetresistant",
        "jaguarresistant", "jayresistant", "kiwiresistant",
        "kuduresistant", "larkresistant", "leopardresistant",
        "lizardresistant", "lobsterresistant", "magpieresistant",
        "mallardresistant", "manateeresistant", "marmotresistant",
        "martenresistant", "meerkatresistant", "minkresistant",
        "mongooseresistant", "muskratresistant", "narwhalresistant",
        "nightingaleresistant", "octopusresistant", "okapiresistant",
        "opossumresistant", "orangutanresistant", "orcaresistant",
        "oryxresistant", "ospreyresistant", "ostrichresistant",
        "oysterresistant", "pangolinresistant", "parakeetresistant",
        "partridgeresistant", "peccaryresistant", "pheasantresistant",
        "pikaresistant", "pikeresistant", "ploverresistant",
        "polecatresistant", "porcupineresistant", "porpoiseresistant",
        "possumresistant", "prawnresistant", "pronghornresistant",
        "puffinresistant", "pumaresistant", "quetzalresistant",
        "quokkaresistant", "railresistant", "ramresistant",
        "rattlesnakeresistant", "rayresistant", "reindeerresistant",
        "robinresistant", "roosterresistant", "sableresistant",
        "salamanderresistant", "sardineresistant", "seahorseresistant",
        "servalresistant", "shrewresistant", "shrimpresistant",
        "skinkresistant", "slothresistant", "slugresistant",
        "sniperesistant", "snowleopardresistant", "soleresistant",
        "sparrowresistant", "spoonbillresistant", "squidresistant",
        "starlingresistant", "stingrayresistant", "stoatresistant",
        "sturgeonresistant", "swallowresistant", "swiftresistant",
        "swordfishresistant", "tahrresistant", "tamarinresistant",
        "tapirresistant", "tarantularesistant", "tarsierresistant",
        "tasmaniandevilresistant", "tealresistant", "tenrecresistant",
        "ternresistant", "thrushresistant", "tickresistant",
        "tilapiaresistant", "tortoiseresistant", "toucanresistant",
        "tunaresistant", "turnstoneresistant", "vicunaresistant",
        "warthogresistant", "waterbuffaloresistant", "weaverresistant",
        "whelkresistant", "whippetresistant", "wigeonresistant",
        "wildcatresistant", "wilddogresistant", "wildebeestresistant",
        "wolverineresistant", "woodcockresistant", "woodpeckerresistant",
        "wrasseresistant", "wrenresistant", "zeburesistant",
        "zorillaresistant",
    ))

    WORDINGS = dict.fromkeys(
        list(PROOF_WORDINGS) + list(RESIST_WORDINGS))

    RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in WORDINGS)

    STORE = tuple(
        "The store is %s." % word
        for word in WORDINGS)

    CONTROL_FALSE = (
        "The store is henproof.",
        "The store is foxresistant.",
        "The store is anvilproof.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_records_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanUnConfFixR37Tests(unittest.TestCase):
    """Ruling 2433, S15-R37-CONF-5: un wordings."""

    UN_WORDINGS = dict.fromkeys((
        "unadjudicated", "unarmed", "uncoded",
        "unconcluded", "undecided", "unembossed",
        "unfinalized", "ungraded", "unidentified",
        "unjudged", "unlettered", "unmerged",
        "unmined", "unnamed", "unranked",
        "unrated", "unresolved", "unscored",
        "unsegmented", "unsensored", "unsettled",
        "unsplit", "untitled", "untried",
        "untriggered", "unvalved",
    ))

    RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDINGS)

    STORE = tuple(
        "The store is %s." % word
        for word in UN_WORDINGS)

    CONTROL_FALSE = (
        "The records are uncurled by outside writers.",
        "The store is unbadged.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_records_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanGoverningConfFixR37Tests(unittest.TestCase):
    """Ruling 2434, S15-R37-CONF-6: governing instruments."""

    INSTRUMENTS = dict.fromkeys((
        "acceptance", "accreditation",
        "acknowledgement", "acknowledgment",
        "avowal", "bond",
        "convention", "deputation",
        "empowerment", "enablement",
        "favour", "favor",
        "pledge", "prerogative",
        "privilege", "profession",
        "recognition", "trust",
        "understanding", "validation",
        "verification", "vow",
    ))

    PHRASINGS = tuple(
        "by the %s of" % inst for inst in INSTRUMENTS) + tuple(
        "under the %s of" % inst for inst in INSTRUMENTS)

    GOVERNED = tuple(
        "The seal guarantees protection %s "
        "the deployment confinement fact." % phrase
        for phrase in PHRASINGS)

    WEATHER = tuple(
        "The seal guarantees protection %s the weather." % phrase
        for phrase in PHRASINGS)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "The seal guarantees protection by the abnegation of "
        "the deployment confinement fact.",
        "The seal guarantees protection by the justification of "
        "the deployment confinement fact.",
    )

    CONTROL_FALSE = (
        "The seal guarantees protection.",
    )

    def test_phrasings_stand_governed(self):
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
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)


class SealClaimScanMarkerConfFixR37Tests(unittest.TestCase):
    """Ruling 2435, S15-R37-CONF-7: unconditional markers."""

    MARKERS_BOTH = dict.fromkeys((
        "as long as the aqueducts endure", "as long as the aqueducts stand",
        "as long as the ascents endure", "as long as the ascents stand",
        "as long as the avenues endure", "as long as the avenues stand",
        "as long as the bastions endure", "as long as the bastions stand",
        "as long as the beacons endure", "as long as the beacons stand",
        "as long as the boulevards endure", "as long as the boulevards stand",
        "as long as the breakwaters endure", "as long as the bridges endure",
        "as long as the bridges stand", "as long as the canals endure",
        "as long as the canals stand", "as long as the canyons endure",
        "as long as the castles endure", "as long as the citadels endure",
        "as long as the citadels stand", "as long as the cliffs endure",
        "as long as the dams endure", "as long as the dams stand",
        "as long as the declines stand", "as long as the deltas endure",
        "as long as the descents endure", "as long as the descents stand",
        "as long as the ditches endure", "as long as the ditches stand",
        "as long as the docks endure", "as long as the docks stand",
        "as long as the domes endure", "as long as the domes stand",
        "as long as the downs endure", "as long as the downs stand",
        "as long as the earthworks endure", "as long as the earthworks stand",
        "as long as the embankments endure", "as long as the embankments stand",
        "as long as the esplanades endure", "as long as the esplanades stand",
        "as long as the estuaries endure", "as long as the ferries endure",
        "as long as the ferries stand", "as long as the fields endure",
        "as long as the fields stand", "as long as the fords endure",
        "as long as the fords stand", "as long as the forests endure",
        "as long as the fortresses endure", "as long as the fortresses stand",
        "as long as the fosse endure", "as long as the fosse stand",
        "as long as the freeways endure", "as long as the freeways stand",
        "as long as the gardens endure", "as long as the gardens stand",
        "as long as the gorges endure", "as long as the grades endure",
        "as long as the grades stand", "as long as the greens endure",
        "as long as the greens stand", "as long as the groves endure",
        "as long as the groves stand", "as long as the hairpins endure",
        "as long as the hairpins stand", "as long as the heaths endure",
        "as long as the heaths stand", "as long as the highways endure",
        "as long as the highways stand", "as long as the hills endure",
        "as long as the inclines endure", "as long as the inclines stand",
        "as long as the islands endure", "as long as the jetties endure",
        "as long as the jetties stand", "as long as the keeps stand",
        "as long as the knolls endure", "as long as the knolls stand",
        "as long as the lanes endure", "as long as the lanes stand",
        "as long as the levees endure", "as long as the levees stand",
        "as long as the lighthouses endure", "as long as the lighthouses stand",
        "as long as the magazines endure", "as long as the magazines stand",
        "as long as the minarets endure", "as long as the minarets stand",
        "as long as the moats endure", "as long as the moors endure",
        "as long as the moors stand", "as long as the mounds endure",
        "as long as the mounds stand", "as long as the needles endure",
        "as long as the needles stand", "as long as the orchards endure",
        "as long as the orchards stand", "as long as the parks endure",
        "as long as the parks stand", "as long as the passes endure",
        "as long as the passes stand", "as long as the peninsulas endure",
        "as long as the piers endure", "as long as the piers stand",
        "as long as the pillboxes endure", "as long as the pillboxes stand",
        "as long as the pinnacles endure", "as long as the plateaus endure",
        "as long as the plazas endure", "as long as the plazas stand",
        "as long as the porches endure", "as long as the porches stand",
        "as long as the promenades endure", "as long as the promenades stand",
        "as long as the quays endure", "as long as the quays stand",
        "as long as the ramparts endure", "as long as the ramparts stand",
        "as long as the ravines endure", "as long as the redoubts endure",
        "as long as the redoubts stand", "as long as the ridges endure",
        "as long as the roads endure", "as long as the roads stand",
        "as long as the saddles endure", "as long as the saddles stand",
        "as long as the savannas endure", "as long as the seawalls endure",
        "as long as the seawalls stand", "as long as the silos endure",
        "as long as the silos stand", "as long as the slopes endure",
        "as long as the sluices endure", "as long as the sluices stand",
        "as long as the spires endure", "as long as the spires stand",
        "as long as the squares endure", "as long as the squares stand",
        "as long as the steeples endure", "as long as the steeples stand",
        "as long as the steppes endure", "as long as the storehouses endure",
        "as long as the storehouses stand", "as long as the strongholds endure",
        "as long as the strongholds stand", "as long as the summits endure",
        "as long as the switchbacks endure", "as long as the switchbacks stand",
        "as long as the terraces endure", "as long as the towers endure",
        "as long as the towers stand", "as long as the tracks endure",
        "as long as the trails endure", "as long as the trails stand",
        "as long as the tunnels endure", "as long as the tunnels stand",
        "as long as the turnpikes endure", "as long as the turnpikes stand",
        "as long as the turrets endure", "as long as the valleys endure",
        "as long as the viaducts endure", "as long as the viaducts stand",
        "as long as the volcanoes endure", "as long as the walkways endure",
        "as long as the walkways stand", "as long as the warehouses endure",
        "as long as the watchtowers endure", "as long as the watchtowers stand",
        "as long as the waterfalls endure", "as long as the weirs endure",
        "as long as the weirs stand", "as long as the wharves endure",
        "as long as the wharves stand", "as long as the woods endure",
        "as long as the woods stand", "until the hills fall",
        "till the hills fall", "until the earth stops turning",
        "till the earth stops turning", "until the moon falls",
        "until the lakes dry up", "till the lakes dry up",
        "until the springs dry up", "till the springs dry up",
        "until the wells dry up", "till the wells dry up",
        "until the cliffs crumble", "until the towers crumble",
        "till the towers crumble", "until the walls crumble",
        "till the walls crumble", "until the gates rust",
        "till the gates rust", "until the chains rust",
        "till the chains rust", "until time runs out",
        "till time runs out",
    ))

    MARKERS_APPENDED_ONLY = dict.fromkeys((
        "as long as the breakwaters stand", "as long as the castles stand",
        "as long as the channels endure", "as long as the declines endure",
        "as long as the harbours endure", "as long as the keeps endure",
        "as long as the locks endure", "as long as the locks stand",
        "as long as the moats stand", "as long as the tracks stand",
        "as long as the turrets stand", "as long as the warehouses stand",
        "until the seals break", "till the seals break",
        "until the locks break", "till the locks break",
        "until the last star fades", "till the last star fades",
    ))

    MARKERS_COMMA_ONLY = dict.fromkeys((
        "until the oceans dry up", "till the oceans dry up",
    ))

    APPENDED = tuple(
        _GOVERNED_CLAIM + " %s." % marker
        for marker in list(MARKERS_BOTH) + list(MARKERS_APPENDED_ONLY))

    COMMA = tuple(
        _GOVERNED_CLAIM + ", %s." % marker
        for marker in list(MARKERS_BOTH) + list(MARKERS_COMMA_ONLY))

    CONTROL_FALSE = (
        _GOVERNED_CLAIM + " as long as the rivers run.",
        _GOVERNED_CLAIM + ", as long as the rivers run.",
        _GOVERNED_CLAIM + " as long as the oceans stand.",
        _GOVERNED_CLAIM + ", as long as the oceans stand.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_appended_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.APPENDED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_comma_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMMA:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanJournalConfFixR37Tests(unittest.TestCase):
    """Ruling 2436, S15-R37-CONF-8: journal verbs.

    The verb scores stands in no pin of this class: its
    cure stands stopped and referred, in the form the
    builder paper states, and it stands recorded in
    STOPPED_REFERRAL below with no pole asserted.
    """

    VERBS = dict.fromkeys((
        "acidifies", "alkalizes", "badges",
        "brands", "brasses", "bronzes",
        "casehardens", "chalks", "charcoals",
        "charts", "chromes", "coppers",
        "debosses", "decarburizes", "descales",
        "detempers", "drafts", "embosses",
        "enamels", "engraves", "etherizes",
        "files", "flags", "gilds",
        "glazes", "grades", "graphs",
        "grids", "indexes", "inks",
        "keratinizes", "labels", "letters",
        "lines", "lipophilizes", "maps",
        "margins", "marks", "nickels",
        "numbers", "pepsinizes", "phosphatizes",
        "plates", "plots", "ranks",
        "rates", "refines", "scribes",
        "shellacs", "signs", "smelts",
        "sorts", "sterilizes", "sulfurizes",
        "tags", "tannizes", "tins",
        "titles", "traces", "varnishes",
        "zincs",
    ))

    STOPPED_REFERRAL = ("scores",)

    FORMS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in VERBS)

    CONTROL_FALSE = (
        "The journal ablates integrity for every reader.",
        "The journal nebulizes integrity for every reader.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "Integrity label for the journal schedule.",
    )

    def test_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanNegationConfFixR37Tests(unittest.TestCase):
    """Ruling 2437, S15-R37-CONF-9: negation forms."""

    ROOTS = dict.fromkeys((
        "definable", "distillable", "drillable",
        "dyeable", "erodible", "escapable",
        "fadable", "fastenable", "fermentable",
        "flavourable", "flawable", "fossilizable",
        "frayable", "frostable", "scratchable",
    ))

    VERBS = dict.fromkeys((
        "defined", "distilled", "dyed",
        "eroded", "escaped", "evaporated",
        "excavated", "extruded",
    ))

    NO_ROOT_FORMS = tuple(
        "No record is %s after writing." % root
        for root in ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in ROOTS)

    NO_VERB_FORMS = tuple(
        "No record is %s after writing." % verb
        for verb in VERBS) + tuple(
        "No record can be %s after writing." % verb
        for verb in VERBS)

    ASSERTED_AT_POLE = tuple(
        "The record is %s after writing." % root
        for root in ROOTS) + tuple(
        "Records are %s after writing." % root
        for root in ROOTS) + tuple(
        "Records are %s after writing." % verb
        for verb in VERBS)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = ()

    def test_no_roots_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_ROOT_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_no_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_VERB_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    def test_asserted_analogues_stand_judged(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_AT_POLE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



class SealClaimScanDisclosureConfFixR37Tests(unittest.TestCase):
    """Ruling 2438, S15-R37-CONF-10: disclosure roots and verbs."""

    ROOTS = dict.fromkeys((
        "bendable", "comparable", "datable",
        "deducible", "detectable", "determinable",
        "diagnosable", "diagrammable", "digestible",
        "dilutable", "dimmable", "dispensable",
        "dissolvable", "dividable", "dockable",
        "documentable", "drainable", "drinkable",
        "drivable", "dryable", "educable",
        "electable", "elevatable", "eliminable",
        "emittable", "employable", "enjoyable",
        "ensurable", "equatable", "equippable",
        "erectable", "escalable", "evacuable",
        "evadable", "evaporable", "evictable",
        "exactable", "excavatable", "exceedable",
        "excisable", "excitable", "excludable",
        "excusable", "exemptible", "exilable",
        "expansible", "expectable", "expeditable",
        "expellable", "expendable", "explicable",
        "explodable", "exploitable", "explorable",
        "expressible", "extendible", "extensible",
        "exterminable", "extraditable", "extricable",
        "extrudable", "factorable",
    ))

    VERBS = dict.fromkeys((
        "calculated", "derived", "detected",
        "determined", "diluted", "dimmed",
        "dispensed", "dissolved", "divided",
        "docked", "drained", "dried",
        "educated", "elected", "elevated",
        "eliminated", "emitted", "employed",
        "enjoyed", "equated", "equipped",
        "erected", "escalated", "estimated",
        "evacuated", "evaded", "evaluated",
        "evicted", "evoked", "exacted",
        "exceeded", "excised", "excited",
        "excluded", "excused", "exempted",
        "exhausted", "exiled", "expected",
        "expedited", "expelled", "expended",
        "explained", "exploded", "exploited",
        "explored", "expressed", "exterminated",
        "extradited", "extricated",
    ))

    ROOT_FORMS = tuple(
        "The record is %s after writing." % root
        for root in ROOTS) + tuple(
        "Records are %s after writing." % root
        for root in ROOTS) + tuple(
        "No record is %s after writing." % root
        for root in ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in ROOTS)

    VERB_FORMS = tuple(
        "Records are %s after writing." % verb
        for verb in VERBS) + tuple(
        "No record is %s after writing." % verb
        for verb in VERBS) + tuple(
        "No record can be %s after writing." % verb
        for verb in VERBS)

    CONTROL_FALSE = (
        "Records are markable after writing.",
        "No record is markable after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_roots_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    CONTROL_FALSE = _PLAIN_CONTROLS_FALSE

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)



if __name__ == "__main__":
    unittest.main()
