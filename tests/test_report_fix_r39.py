"""Fix round 39, Region 1: report seal claim scan pins.

Rulings 2725 to 2742 of the Round 39 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R39-REPG-1 to 8 and the Confinement paper findings
S15-R39-CONF-1 to 10, on the templates those papers
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

class SealClaimScanInabilityRepGFixR39Tests(unittest.TestCase):
    """Ruling 2725, S15-R39-REPG-1: inability windows and followers."""

    FOLLOWERS = dict.fromkeys((
        "minted", "pencilled", "potted",
        "pouched", "sheeted", "sleeved",
        "stringed", "striped", "tubed",
        "tucked", "vented", "webbed",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "absently", "absurdly", "alertly",
        "alienly", "allegorically", "alliedly",
        "alluringly", "aloofly", "alphabetically",
        "amazingly", "ambiguously", "amiably",
        "amply", "amusedly", "analytically",
        "anciently", "anecdotally", "annually",
        "answerably", "anticipatorily", "apologetically",
        "appreciably", "approachably", "approximately",
        "aptly", "arbitrarily", "archly",
        "aridly", "aristocratically", "arithmetically",
        "ashamedly", "assuredly", "astonishingly",
        "asymmetrically", "athletically", "atmospherically",
        "atomically", "atrociously", "attackingly",
        "attainably", "atypically", "audibly",
        "augustly", "autonomously", "availably",
        "averagely", "avoidably", "awfully",
        "axiomatically", "babblingly", "bacterially",
        "badly", "balkingly", "balmily",
        "banefully", "banishably", "banteringly",
        "barely", "basically", "baskingly",
        "batteringly", "bawdily", "bayingly",
        "beadily", "bearably", "bearishly",
        "beastly", "beatifically", "beautifully",
        "beckoningly", "becomingly", "bedazzlingly",
        "bedraggledly", "beechly", "beepingly",
        "befittingly", "beforely", "beggarly",
        "beggingly", "beginningly", "begrudgingly",
        "behaviorally", "belatedly", "believably",
        "bellowly", "bemusedly", "beneficially",
        "beneficently", "benevolently", "benignly",
        "bequeathably", "besettingly", "besottedly",
        "bestially", "betrayingly", "bewilderingly",
        "bewitchedly", "biasingly", "bibliographically",
        "bickerly", "bickeringly", "biennially",
        "bilingually", "billowily", "billowingly",
        "bimonthly", "bindingly", "biochemically",
        "biographically", "bipartisanly", "birdly",
        "bitingly", "bizarrely", "blamably",
        "blamefully", "blamelessly", "blaringly",
        "blasphemously", "blazingly", "blearedly",
        "bleedingly", "blemishly", "blendedly",
        "blessedly", "blightingly", "blindfoldedly",
        "blindly", "blinkingingly", "blitzingly",
        "bloatedly", "blockingly", "bloodily",
        "bloodthirstily", "bloomingly", "blossomingly",
        "blotchily", "blowzily", "blubberingly",
        "blueingly", "bluffly", "bluishly",
        "blurredly", "blurrily", "blushfully",
        "blushingly", "blusteringly", "bodily",
        "bogusly", "bohemianly", "boisterously",
        "boltingly", "bombastically", "bonelessly",
        "bonily", "bonnily", "boostingly",
        "bootlessly", "boringly", "bossily",
        "botanically", "botheringly", "bothersomely",
        "bottomlessly", "bountifully", "bountiously",
        "bourgeoisly", "bovinely", "bowingly",
        "boyishly", "braggartly", "braggingly",
        "brainily", "brainlessly", "brakingly",
        "brashly", "brassily", "brawlingly",
        "brawnily", "breathably", "breathedly",
        "bribeably", "bridally", "bridgeably",
        "briefly",
    ))

    MODAL_ONLY = dict.fromkeys((
        "grafted", "masked", "patched",
        "patterned", "veiled",
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

    EXTRA_MODAL = tuple(
        "Records cannot be %s after writing." % word
        for word in MODAL_ONLY)

    CONTROL_FALSE = (
        "Records cannot be electroplated by outsiders.",
        "Records cannot truculently be altered after writing.",
        "Records cannot be quilted by outsiders.",
        "Records cannot be draped after writing.",
        "Records are draped by outsiders.",
    ) + tuple(
        "Records are %s by outsiders." % word
        for word in MODAL_ONLY)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "No record was hidden in this record.",
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

    def test_extra_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.EXTRA_MODAL:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanGoverningRepGFixR39Tests(unittest.TestCase):
    """Ruling 2726, S15-R39-REPG-2: trailing governing forms."""

    PLACES = dict.fromkeys((
        "baptistery", "belfry", "caravanserai",
        "chantry", "chapterhouse", "conservatory",
        "crypt", "dormitory", "gallery",
        "infirmary", "library", "mortuary",
        "narthex", "orangery", "ossuary",
        "oratory", "sacristy", "treasury",
        "vault", "vestibule",
    ))

    TIMES = dict.fromkeys((
        "microsecond", "nanosecond", "millisecond",
        "picosecond", "score", "triennium",
        "quadrennium", "quinquennium", "septennium",
        "octennium", "decennium", "centennium",
        "workweek",
    ))

    TRAILING = tuple(
        "The seal guarantees protection in whatsoever %s "
        "the deployment confinement fact holds." % word
        for word in PLACES) + tuple(
        "The seal guarantees protection through whatsoever %s "
        "the deployment confinement fact holds." % word
        for word in PLACES) + tuple(
        "The seal guarantees protection for whatsoever %s "
        "the deployment confinement fact holds." % word
        for word in TIMES)

    WEATHER = tuple(
        "The seal guarantees protection in whatsoever %s "
        "the weather holds." % word
        for word in PLACES) + tuple(
        "The seal guarantees protection through whatsoever %s "
        "the weather holds." % word
        for word in PLACES) + tuple(
        "The seal guarantees protection for whatsoever %s "
        "the weather holds." % word
        for word in TIMES)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "The seal guarantees protection by the scroll of "
        "the deployment confinement fact.",
        "The seal guarantees protection in whatsoever observatory "
        "the deployment confinement fact holds.",
    )

    CONTROL_FALSE = (
        "The seal guarantees protection.",
    )

    def test_trailing_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.TRAILING:
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
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanPrefixedRepGFixR39Tests(unittest.TestCase):
    """Ruling 2727, S15-R39-REPG-3: prefixed compounds."""

    PREFIXES = dict.fromkeys((
        "blepharo", "chole", "cilio",
        "duodeno", "esthesio", "febri",
        "femoro", "genito", "gingivo",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "ivorywood", "steelbone",
    ))

    PREFIXED_VERIFIED = tuple(
        "Every record stands %sverified before use." % word
        for word in PREFIXES)

    PREFIXED_CHECKED = tuple(
        "Every record stands %schecked before use." % word
        for word in PREFIXES)

    FIRST_FORMS = tuple(
        "Every record stands %s-verified before use." % word
        for word in FIRST_ELEMENTS)

    CONTROL_FALSE = (
        "Every record stands amphiverified before use.",
        "Every record stands meningoverified before use.",
        "Every record stands ivorybone-verified before use.",
        "Every record stands verified before use.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_prefixed_verified_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIXED_VERIFIED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_prefixed_checked_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIXED_CHECKED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_first_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FIRST_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanWordingsRepGFixR39Tests(unittest.TestCase):
    """Ruling 2728, S15-R39-REPG-4: un, proof, and resistant wordings."""

    UN_WORDINGS = dict.fromkeys((
        "ungauged", "unglossed", "ungrafted",
        "ungrained", "ungrooved", "unguided",
        "unhammered", "unmatted", "unminted",
        "unoiled", "unpatched", "unpatterned",
        "unperforated", "unplated", "unpleated",
        "unpocketed", "unposted", "unpotted",
        "unpouched", "unpowdered", "unpressed",
        "unprimed", "unruled", "unsanded",
        "unseamed", "unsheeted", "unslotted",
        "unstringed", "unstriped", "unstudded",
        "untinned", "untrimmed", "untubed",
        "untucked", "unwaxed", "unwedged",
    ))

    PROOF_WORDINGS = dict.fromkeys((
        "gibbonproof", "herringproof", "hippoproof",
        "houndproof", "ibexproof", "ibisproof",
        "impalaproof", "jellyfishproof", "ladybirdproof",
        "lambproof", "louseproof", "macaqueproof",
        "mammothproof", "mandrillproof", "mantisproof",
        "mayflyproof", "musselproof", "numbatproof",
        "nutriaproof", "orioleproof", "perchproof",
        "rookproof", "silkwormproof", "woodlouseproof",
    ))

    RESISTANT_WORDINGS = dict.fromkeys((
        "gibbonresistant", "herringresistant", "hipporesistant",
        "houndresistant", "ibexresistant", "ibisresistant",
        "impalaresistant", "jellyfishresistant", "ladybirdresistant",
        "lambresistant", "locustresistant", "louseresistant",
        "macaqueresistant", "mammothresistant", "mandrillresistant",
        "mantisresistant", "mayflyresistant", "miteresistant",
        "mosquitoresistant", "musselresistant", "numbatresistant",
        "nutriaresistant", "orioleresistant", "perchresistant",
        "rookresistant", "silkwormresistant", "woodlouseresistant",
    ))

    UN_RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDINGS)

    UN_STORE = tuple(
        "The store is %s." % word
        for word in UN_WORDINGS)

    PROOF_STORE = tuple(
        "The store is %s." % word
        for word in PROOF_WORDINGS)

    RESISTANT_STORE = tuple(
        "The store is %s." % word
        for word in RESISTANT_WORDINGS)

    CONTROL_FALSE = (
        "The records are unedged by outside writers.",
        "The store is dragonflyproof.",
        "The store is dragonflyresistant.",
        "The store is unbadged.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_un_records_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.UN_RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_un_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.UN_STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_proof_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROOF_STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_resistant_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RESISTANT_STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanVerbsRepGFixR39Tests(unittest.TestCase):
    """Ruling 2729, S15-R39-REPG-5: journal verbs."""

    VERBS = dict.fromkeys((
        "effaces", "elaborates", "electrifies",
        "encodes", "encrypts", "enlists",
        "enriches", "enrols", "entails",
        "entertains", "entices", "entraps",
        "entrusts", "equalises", "equates",
        "equips", "eradicates", "erases",
        "erects", "escalates", "evacuates",
        "evaluates", "evicts", "evokes",
        "exacts", "examines", "exceeds",
        "exchanges", "excites", "excludes",
        "executes", "exempts", "exercises",
        "exerts", "exhales", "exhausts",
        "exhorts", "exiles", "expands",
        "expects", "expels", "expends",
        "exploits", "explores", "exports",
        "expunges", "extinguishes", "extorts",
        "extrapolates", "extricates", "fabricates",
        "facilitates", "falsifies", "familiarises",
        "fastens", "fattens", "favours",
        "faxes", "fazes", "fears",
        "federates", "feeds", "feels",
        "feigns", "fells", "fences",
        "fertilises", "fetches", "fetters",
        "feuds", "fiddles", "fidgets",
        "fights", "fills", "films",
        "finalises", "finances", "fines",
        "fingers", "finishes", "fires",
        "firms", "fishes", "fissures",
        "fits", "flames", "flanks",
        "flaps", "flashes", "flattens",
        "flatters", "flavours", "flaws",
        "flays", "flees", "fleets",
        "fleshes", "flexes", "flicks",
        "flies", "flings", "flips",
        "flirts", "flits", "flogs",
        "floors", "flosses", "flounders",
        "fluctuates", "fluffs", "fluidifies",
        "flukes", "flumes", "flunks",
        "flushes", "flusters", "flutes",
        "flutters",
    ))

    INTEGRITY = tuple(
        "The journal %s integrity for every reader." % word
        for word in VERBS)

    CONTROL_FALSE = (
        "The journal dampens integrity for every reader.",
        "The journal electrolyzes integrity for every reader.",
        "The journal narrates integrity for every reader.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "Integrity label for the journal schedule.",
    )

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.INTEGRITY:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanMarkersRepGFixR39Tests(unittest.TestCase):
    """Ruling 2730, S15-R39-REPG-6: unconditional markers."""

    MARKERS_BOTH = dict.fromkeys((
        "as long as the mangroves stand", "till the mangroves fall",
        "until the lagoons dry", "while the deltas shift",
        "as long as the fjords freeze", "till the fjords thaw",
        "until the mesas crumble", "while the canyons flood",
        "as long as the badlands endure", "till the badlands erode",
        "until the dunes migrate", "while the oases flourish",
        "till the reefs bleach", "until the atolls sink",
        "while the estuaries flow", "till the headlands fall",
        "until the peninsulas flood", "while the archipelagos shift",
        "as long as the marshlands endure", "till the marshlands drain",
        "until the pinewoods fall", "while the prairies burn",
        "till the tundra melts", "until the glaciers retreat",
        "while the icebergs calve",
    ))

    MARKERS_APPENDED = dict.fromkeys((
        "until the tundra thaws", "while the taiga burns",
        "as long as the tundra endures",
    ))

    APPENDED = tuple(
        _GOVERNED_CLAIM + " %s." % word
        for word in MARKERS_BOTH) + tuple(
        _GOVERNED_CLAIM + " %s." % word
        for word in MARKERS_APPENDED)

    COMMA = tuple(
        _GOVERNED_CLAIM + ", %s." % word
        for word in MARKERS_BOTH)

    CONTROL_FALSE = (
        _GOVERNED_CLAIM + " till the saltflats crack.",
        _GOVERNED_CLAIM + ", till the saltflats crack.",
        _GOVERNED_CLAIM + " as long as the icecaps stand.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_appended_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.APPENDED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_comma_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMMA:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanNegationRepGFixR39Tests(unittest.TestCase):
    """Ruling 2731, S15-R39-REPG-7: negation narrowing roots."""

    ROOTS = dict.fromkeys((
        "minceable", "mulchable", "nickable",
        "nicknameable", "noticeabe", "obtainable",
    ))

    NO_IS = tuple(
        "No record is %s after writing." % word
        for word in ROOTS)

    NO_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in ROOTS)

    CONTROL_FALSE = tuple(
        "Records are %s after writing." % word
        for word in ROOTS) + (
        "No record is identifiable after writing.",
        "No record can be joinable after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "No record was hidden in this record.",
    )

    def test_no_is_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_IS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_no_can_be_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanDisclosureRepGFixR39Tests(unittest.TestCase):
    """Ruling 2732, S15-R39-REPG-8: disclosure roots and verbs."""

    ROOTS = dict.fromkeys((
        "meltable", "mendable", "milkable",
        "millable", "mineable", "mingleable",
        "mintable", "missable", "mitigable",
        "mixable", "modulateable", "moldable",
        "mumbleable", "murderable", "murmurrable",
        "narrowable", "navigable", "needable",
        "negateable", "netable", "nibbleable",
        "nipable", "nodable", "nominable",
        "notifyable", "nourishable", "nudgeable",
        "nullifiable", "numbable", "numerable",
        "nurseable", "nuzzleable", "obeyable",
        "obligable", "obliterable", "occasionable",
        "occupyable", "offendable", "offerable",
        "offsetable", "oilable", "omitable",
        "operable", "opposable", "oppressable",
        "optimisable", "optionable", "orbitable",
        "orientable", "ornamentable", "oscillateable",
        "ostracisable", "outbidable", "outdoable",
        "outfitable", "outgrowable", "outlastable",
        "outlawable", "outliveable", "outnumberable",
        "outreachabe", "outrunable", "outsellable",
        "outshineable", "outvoteable", "outweighable",
        "ovenable", "overactable", "overarchable",
        "overbearable", "overbidable", "overbillable",
        "overblowable", "overbookable", "overbuildable",
        "overburdenable", "overbuyable", "overcallable",
        "overcastable", "overchargeable", "overclimbable",
        "overcloudable", "sanitiseable", "satisfiable",
        "scatterable", "scheduleable", "schemeable",
        "scoopable", "scoreable", "scourable",
        "screwable", "scribbleable", "scrubable",
        "seatable", "secludeable", "secreteable",
        "seedable", "seekable", "seepable",
        "seetheable", "senseable", "serveable",
        "setable", "settleable", "sewable",
        "shadeable", "shakeable", "shallowable",
        "shameable", "shapeable", "shaveable",
        "shedable", "shellable", "shimmerable",
        "shineable", "shingleable", "shiverable",
        "shockable", "shoeable", "shootable",
        "shopable", "shoutable", "shoveable",
        "showable", "shrewdable", "shrillable",
        "shriveable", "shrugable", "shuffleable",
        "shunable", "shuntable", "shutable",
        "shuttleable", "sickenable", "sideable",
        "sidelineable", "sidestepable", "sidetrackable",
        "sieveable", "siftable", "sighable",
        "sightable", "silenceable", "siliconable",
        "silkable", "sillable", "simmerable",
        "simpleable", "simplifyable", "simulateable",
        "singleable", "sinkable", "sipable",
        "sireable", "sisable", "sisterable",
        "sitable", "siteable", "situateable",
        "sizable", "sizeable", "sizzleable",
        "skateable", "skewable", "skewerable",
        "skiable", "skidable", "skillable",
        "skimable", "skinable", "skipable",
        "skirmishable", "skitterable", "skiveable",
        "slackable", "slackenable", "slamable",
        "slantable", "slapable", "slateable",
        "slaughterable", "slaveable", "sledable",
        "sleekable", "sleepable", "sliceable",
        "slickable", "slideable", "slightable",
        "slimable", "slimeable", "slingable",
        "slinkable", "slipable", "slitherable",
        "sliverable", "sloganable", "slopeable",
        "sloshable", "slotable", "slothable",
        "slouchable", "sloughable", "slowable",
        "sludgeable", "slugable", "sluiceable",
        "slumberable", "slumpable", "slurpable",
        "slushable", "smackable", "smallable",
        "smartable", "smashable", "smearable",
        "smellable", "smeltable", "smileable",
        "smirkable", "smiteable", "smithable",
        "smoothable", "smotherable", "snackable",
        "snaffleable", "snagable", "snakeable",
        "snapable", "snareable", "snarlable",
        "snazzable", "sneakable", "sneerable",
        "sneezeable", "snickerable", "snideable",
        "snipeable", "snipable", "snitchable",
        "snivelable", "snookerable", "snoopable",
        "snoozeable", "snoreable", "snorkelable",
        "snortable", "snoutable", "snowable",
        "snubable", "snuckable", "snuffable",
        "snugable", "snuggleable", "soapable",
        "soarable", "soberable", "sociable",
        "socialable", "socialisable", "socialiseable",
        "sockable", "sojournable", "solaceable",
        "solarable", "soleable", "solvable",
        "solveable", "somberable", "sombreable",
        "somersaultable", "somnambulateable", "sonicable",
        "sonnetable", "sootable", "sootheable",
        "soothsayable", "sophistable", "soporificable",
        "sopranoable", "sorbable", "sorcerable",
        "soreable", "sorghumable", "sorrowable",
        "sortitionable", "sourable", "sourceable",
        "souseable", "sowable", "spaceable",
        "spackleable", "spadeable", "spallable",
        "spangleable", "spankable", "spareable",
        "spargeable", "sparkleable", "sparrable",
        "spatterable", "spatulaable", "spawnable",
        "speakable", "spearable", "specialisable",
        "specialiseable", "speciateable", "specieable",
        "specifyable", "speckleable", "speculateable",
        "spellable", "spellbindable", "spendable",
    ))

    VERB_FORMS = dict.fromkeys((
        "salvaged", "satisfied", "scattered",
        "schemed", "scooped", "scribbled",
        "seated", "secluded", "secreted",
        "sought", "seeped", "seethed",
        "sensed", "serviced", "settled",
        "severed", "shaded", "shaken",
        "shallowed", "shamed", "shaped",
        "shed", "shelled", "shimmered",
        "shone", "shivered", "shocked",
        "shod", "shot", "shopped",
        "shouted", "shoved", "shown",
        "shrank", "shrieked", "shrivelled",
        "shrugged", "shuffled", "shunned",
        "shunted", "shut", "shuttled",
        "sickened", "sided", "sidestepped",
        "sieved", "sifted", "sighed",
        "sighted", "silenced", "simplified",
        "singled", "sank", "sipped",
        "situated", "sized", "sizzled",
        "skated", "skewed", "skewered",
        "skied", "skidded", "skimmed",
        "skinned", "skipped", "skirmished",
        "skittered", "slackened", "slammed",
        "slanted", "slapped", "slated",
        "slaughtered", "slaved", "sledded",
        "slept", "slicked", "slid",
        "slighted", "slimmed", "slimed",
        "slung", "slunk", "slipped",
        "slit", "slithered", "slivered",
        "slogged", "sloped", "sloshed",
        "slouched", "sloughed", "slowed",
        "sludged", "slugged", "sluiced",
        "slumbered", "slumped", "slurred",
        "slurped", "slushed", "smacked",
        "smarted", "smashed", "smeared",
        "smelled", "smelted", "smiled",
        "smirked", "smote", "smothered",
        "snacked", "snagged", "snaked",
        "snared", "snarled", "sneaked",
        "sneered", "sneezed", "snickered",
        "sniped", "snipped", "snitched",
        "snivelled", "snookered", "snooped",
        "snoozed", "snored", "snorkelled",
        "snorted", "snowed", "snubbed",
        "snuffed", "snugged", "snuggled",
        "soared", "sobbed", "sobered",
        "socialised", "socked", "softened",
        "sojourned", "solaced", "solicited",
        "solved", "somersaulted", "soothed",
    ))

    ROOT_NO_IS = tuple(
        "No record is %s after writing." % word
        for word in ROOTS)

    ROOT_NO_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in ROOTS)

    ROOT_ASSERTED = tuple(
        "Records are %s after writing." % word
        for word in ROOTS)

    VERB_NO_IS = tuple(
        "No record is %s after writing." % word
        for word in VERB_FORMS)

    VERB_NO_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in VERB_FORMS)

    VERB_ASSERTED = tuple(
        "Records are %s after writing." % word
        for word in VERB_FORMS)

    CONTROL_FALSE = (
        "Records are kickable after writing.",
        "Records are kicked after writing.",
        "No record is kickable after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_root_no_is_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_NO_IS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_root_no_can_be_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_NO_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_root_asserted_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verb_no_is_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_NO_IS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verb_no_can_be_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_NO_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verb_asserted_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanWindowConfFixR39Tests(unittest.TestCase):
    """Ruling 2733, S15-R39-CONF-1: window words."""

    WINDOW_WORDS = dict.fromkeys((
        "unconscionably", "unctuously", "undauntedly",
        "understandingly", "undeservedly", "undesignedly",
        "undeterminedly", "undiplomatically", "undisputedly",
        "undoubtably", "undramatically", "unduly",
        "uneconomically", "unenviably", "unequally",
        "unerringly", "unessentially", "unevenly",
        "uneventfully", "unexcitedly", "unexcitingly",
        "unexpectedly", "unexploredly", "unexposedly",
        "unexpressively", "unexpurgatedly", "unextravagantly",
        "unfadedly", "unfadingly", "unfalteringly",
        "unfamiliarly", "unfashionably", "unfathomably",
        "unfavourably", "unfearfully", "unfeignedly",
        "unfeigningly", "unfemininely", "unfertilizedly",
        "unflaggingly", "unflappably", "unflatteringly",
        "unforeseeably", "unforestedly", "unforgedly",
        "unforgettably", "unforgivably", "unforgivingly",
        "unformally", "unfortifiedly", "unfortunately",
        "unfoundedly", "unfracturedly", "unfrequently",
        "unfrightenedly", "unfrozenly", "unfruitfully",
        "unfussily", "ungainly", "ungallantly",
        "ungarnishedly", "ungenerously", "ungenially",
        "ungentlemanly", "unglamorously", "unglaringly",
        "unglossily", "ungodlily", "ungracefully",
        "ungraciously", "ungrammatically", "ungraspably",
        "ungratefully", "ungratifiedly", "ungravelly",
        "unguardedly", "unguidedly", "unhallowedly",
        "unhamperedly", "unhandily", "unhandsomely",
        "unhardenedly", "unharmedly", "unharmoniously",
        "unharnessedly", "unharvestedly", "unhastily",
        "unhatchedly", "unhazardously", "unheadedly",
        "unhealedly", "unhealthfully", "unhealthily",
        "unheardly", "unhearingly", "unheatedly",
        "unheedfully", "unheedily", "unheedingly",
        "unhelpfully", "unhelpingly", "unheroically",
        "unhesitantly", "unhesitatingly", "unhiddenly",
        "unhideously", "unhinderedly", "unhingedly",
        "unhingingly", "unhistorically", "unhitchingly",
        "unhoardingly", "unholily", "unhollowedly",
        "unhomogeneously", "unhonestly", "unhonoredly",
        "unhonouredly", "unhoodedly", "unhookedly",
        "unhopefully", "unhorizontally", "unhornedly",
        "unhorrifiedly", "unhorsedly", "unhostilely",
        "unhousedly", "unhoveringly", "unhugely",
        "unhumanely", "unhumanly", "unhumbledly",
        "unhumorously", "unhumourously", "unhurryingly",
        "unhurtfully", "unhurtingly", "unhuskedly",
        "unhygienically", "unhymnedly", "unhyphenatedly",
        "unhypnotically", "unhypocritically", "unhysterically",
        "vacuously", "vaguely", "valorously",
        "valuably", "vanishingly", "variously",
        "venturesomely", "verdantly", "vernacularly",
        "vexatiously", "viably", "virilely",
        "virtuously", "visionarily", "vivaciously",
        "vociferously", "voicelessly", "votively",
        "warningly", "wealthily", "wearisomely",
        "wearyingly", "welcomely", "wetly",
        "whackily", "whinily", "whirlingly",
        "whitely", "wiltedly", "wimpily",
        "wirily", "wishfully", "workably",
        "worldly", "worshipfully", "worthlessly",
        "wriggly", "wrinkly",
    ))

    WINDOWS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in WINDOW_WORDS)

    CONTROL_FALSE = (
        "Records cannot irksomely be altered after writing.",
        "Records cannot tacitly be altered after writing.",
        "Records cannot unconservatively be altered after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOWS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanFollowersConfFixR39Tests(unittest.TestCase):
    """Ruling 2734, S15-R39-CONF-2: followers."""

    FOLLOWERS_BOTH = dict.fromkeys((
        "finished", "flavored", "fleeced",
        "flexed", "floured", "flowered",
        "foamed", "forested", "formed",
        "furred", "garbed", "garmented",
        "gartered", "gasketed", "gated",
        "gnarled", "gravelled", "gusseted",
        "guttered", "hampered", "handcuffed",
        "hasped", "hefted", "herbed",
        "hoarded", "hoisted", "holed",
        "hollowed", "holstered", "honeycombed",
    ))

    FOLLOWERS_MODAL = dict.fromkeys((
        "flattened", "grassed", "hardened",
        "hashed",
    ))

    MODAL = tuple(
        "Records cannot be %s after writing." % word
        for word in FOLLOWERS_BOTH) + tuple(
        "Records cannot be %s after writing." % word
        for word in FOLLOWERS_MODAL)

    ASSERTED = tuple(
        "Records are %s by outsiders." % word
        for word in FOLLOWERS_BOTH)

    CONTROL_FALSE = (
        "Records cannot be patinated after writing.",
        "Records are patinated by outsiders.",
        "Records cannot be blanketed after writing.",
        "Records are blanketed by outsiders.",
    ) + tuple(
        "Records are %s by outsiders." % word
        for word in FOLLOWERS_MODAL)

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

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanPrefixedConfFixR39Tests(unittest.TestCase):
    """Ruling 2735, S15-R39-CONF-3: prefixed compounds."""

    PREFIXES = dict.fromkeys((
        "elaeo", "erio", "etio",
        "gonio", "haemato", "hagio",
        "hemero", "hypno",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "cinnabar", "flintstone", "gneiss",
        "labradorite", "lignite", "lodestone",
        "magnesite", "onyxite", "opalite",
        "quartzite", "serpentine", "soapstone",
        "sodalite", "verdite",
    ))

    PREFIXED_VERIFIED = tuple(
        "Every record stands %sverified before use." % word
        for word in PREFIXES)

    PREFIXED_CHECKED = tuple(
        "Every record stands %schecked before use." % word
        for word in PREFIXES)

    FIRST_FORMS = tuple(
        "Every record stands %s-verified before use." % word
        for word in FIRST_ELEMENTS)

    CONTROL_FALSE = (
        "Every record stands acanthoverified before use.",
        "Every record stands dichochecked before use.",
        "Every record stands zebranowood-verified before use.",
        "Every record stands verified before use.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_prefixed_verified_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIXED_VERIFIED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_prefixed_checked_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIXED_CHECKED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_first_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FIRST_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanAnimalsConfFixR39Tests(unittest.TestCase):
    """Ruling 2736, S15-R39-CONF-4: proof and resistant wordings."""

    PROOF_WORDINGS = dict.fromkeys((
        "boomslangproof", "borzoiproof", "boxfishproof",
        "boxjellyfishproof", "brantproof", "breamproof",
        "capercaillieproof", "capuchinproof", "caracalproof",
        "caracaraproof", "cardinalproof", "carpproof",
        "chaffinchproof", "chamoisproof", "chickadeeproof",
        "chimaeraproof", "choughproof", "chuckwallaproof",
        "cichlidproof", "civetproof", "clamproof",
        "cockatielproof", "cockatooproof", "cockleproof",
        "codproof", "coelacanthproof", "condorproof",
        "congerproof", "conureproof", "cootproof",
        "cormorantproof", "cougarproof", "cowbirdproof",
        "craneflyproof", "crappieproof", "crayfishproof",
        "crossbillproof", "cuckooproof", "curassowproof",
        "curlewproof", "cuscusproof", "cygnetproof",
        "daceproof", "dachshundproof", "dalmatianproof",
        "damselflyproof", "darterproof", "deerflyproof",
        "deermouseproof", "deguproof", "demoiselleproof",
        "desmanproof", "dholeproof", "diamondbackproof",
        "dinosaurproof", "diplodocusproof", "discusproof",
        "dobermanproof", "dobsonflyproof", "dodoproof",
        "dogfishproof", "dollarbirdproof", "doradoproof",
        "dorcasproof", "doryproof", "dotterelproof",
        "dowitcherproof", "dragonetproof", "drongoproof",
        "drosophilaproof", "duckbillproof", "dunlinproof",
        "dunnartproof", "dunnockproof", "duskywingproof",
    ))

    RESISTANT_WORDINGS = dict.fromkeys((
        "boomslangresistant", "borzoiresistant", "boxfishresistant",
        "boxjellyfishresistant", "brantresistant", "breamresistant",
        "capercaillieresistant", "capuchinresistant", "caracalresistant",
        "caracararesistant", "cardinalresistant", "carpresistant",
        "centipederesistant", "chaffinchresistant", "chamoisresistant",
        "chickadeeresistant", "chimaeraresistant", "choughresistant",
        "chuckwallaresistant", "cichlidresistant", "civetresistant",
        "clamresistant", "cockatielresistant", "cockatooresistant",
        "cockleresistant", "codresistant", "coelacanthresistant",
        "condorresistant", "congerresistant", "conureresistant",
        "cootresistant", "cormorantresistant", "cougarresistant",
        "cowbirdresistant", "craneflyresistant", "crappieresistant",
        "crayfishresistant", "crossbillresistant", "cuckooresistant",
        "curassowresistant", "curlewresistant", "cuscusresistant",
        "cygnetresistant", "daceresistant", "dachshundresistant",
        "dalmatianresistant", "damselflyresistant", "darterresistant",
        "deerflyresistant", "deermouseresistant", "deguresistant",
        "demoiselleresistant", "desmanresistant", "dholeresistant",
        "diamondbackresistant", "dinosaurresistant", "diplodocusresistant",
        "discusresistant", "dobermanresistant", "dobsonflyresistant",
        "dodoresistant", "dogfishresistant", "dollarbirdresistant",
        "doradoresistant", "dorcasresistant", "doryresistant",
        "dotterelresistant", "dowitcherresistant", "dragonetresistant",
        "droneresistant", "drongoresistant", "drosophilaresistant",
        "duckbillresistant", "dunlinresistant", "dunnartresistant",
        "dunnockresistant", "duskywingresistant",
    ))

    STORE = tuple(
        "The store is %s." % word
        for word in PROOF_WORDINGS) + tuple(
        "The store is %s." % word
        for word in RESISTANT_WORDINGS)

    RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in PROOF_WORDINGS) + tuple(
        "The records are %s by outside writers." % word
        for word in RESISTANT_WORDINGS)

    CONTROL_FALSE = (
        "The store is henproof.",
        "The store is foxresistant.",
        "The store is addaxproof.",
        "The store is addaxresistant.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_records_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanUnConfFixR39Tests(unittest.TestCase):
    """Ruling 2737, S15-R39-CONF-5: un wordings."""

    UN_WORDINGS = dict.fromkeys((
        "unagglomerated", "unagglutinated", "unaggregated",
        "unagitated", "unagreed", "unaided",
        "unaimed", "unaired", "unalienated",
        "unaligned", "unalleviated", "unallied",
        "unallocated", "unallotted", "unamalgamated",
        "unamplified", "unanalysed", "unanalyzed",
        "unanimated", "unannealed", "unannexed",
        "unannounced", "unanointed", "unanswered",
        "unanticipated", "unappeased", "unappended",
        "unapplauded", "unapplied", "unappointed",
        "unapportioned", "unappraised", "unappreciated",
        "unapprehended", "unappropriated", "unargued",
        "unarranged", "unarrayed", "unarrested",
        "unarrived", "unarticulated", "unascended",
        "unascribed", "unasked", "unassassinated",
        "unassaulted", "unassembled", "unassented",
        "unasserted", "unassessed", "unassigned",
        "unassimilated", "unassisted", "unassociated",
        "unassorted", "unassumed", "unassured",
        "unattacked", "unattempted",
    ))

    STORE = tuple(
        "The store is %s." % word
        for word in UN_WORDINGS)

    RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDINGS)

    CONTROL_FALSE = (
        "The records are uncurled by outside writers.",
        "The store is unbadged.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_records_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanGoverningConfFixR39Tests(unittest.TestCase):
    """Ruling 2738, S15-R39-CONF-6: governing instruments."""

    PHRASINGS = dict.fromkeys((
        "by the claim of", "by the conferment of",
        "by the conferral of", "by the credential of",
        "by the eligibility of", "by the employment of",
        "by the endowment of", "by the engagement of",
        "under the claim of", "under the conferment of",
        "under the conferral of", "under the credential of",
        "under the eligibility of", "under the employment of",
        "under the endowment of", "under the engagement of",
        "under the election of",
    ))

    GOVERNED = tuple(
        "The seal guarantees protection %s "
        "the deployment confinement fact." % phrase
        for phrase in PHRASINGS)

    WEATHER = tuple(
        "The seal guarantees protection %s the weather." % phrase
        for phrase in PHRASINGS)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "The seal guarantees protection by the acclaim of "
        "the deployment confinement fact.",
        "The seal guarantees protection by the justification of "
        "the deployment confinement fact.",
        "The seal guarantees protection by the election of "
        "the deployment confinement fact.",
    )

    CONTROL_FALSE = (
        "The seal guarantees protection.",
    )

    def test_governed_phrasings_stand(self):
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


class SealClaimScanMarkersConfFixR39Tests(unittest.TestCase):
    """Ruling 2739, S15-R39-CONF-7: unconditional markers, convergent limb."""

    MARKERS_BOTH = dict.fromkeys((
        "as long as the dikes endure", "as long as the dikes stand",
        "as long as the doorways endure", "as long as the doorways stand",
        "as long as the dormers endure", "as long as the dormers stand",
        "as long as the dovecotes endure", "as long as the dovecotes stand",
        "as long as the drawbridges endure", "as long as the dungeons endure",
        "as long as the dungeons stand", "as long as the dykes endure",
        "as long as the dykes stand", "as long as the eaves endure",
        "as long as the eaves stand", "as long as the escarpments endure",
        "as long as the facades endure", "as long as the facades stand",
        "as long as the fences endure", "as long as the ferryhouses endure",
        "as long as the ferryhouses stand", "as long as the flagstones endure",
        "as long as the flagstones stand", "as long as the floodwalls endure",
        "as long as the floodwalls stand", "as long as the foundations endure",
        "as long as the foundations stand", "as long as the fountains endure",
        "as long as the fountains stand", "as long as the furnaces endure",
        "as long as the furnaces stand", "as long as the gables endure",
        "as long as the gables stand", "as long as the galleries endure",
        "as long as the galleries stand", "as long as the garrets endure",
        "as long as the garrets stand", "as long as the gates endure",
        "as long as the gates stand", "as long as the gatehouses endure",
        "as long as the gatehouses stand", "as long as the gazebos endure",
        "as long as the gazebos stand", "as long as the girders endure",
        "as long as the glens endure", "as long as the glens stand",
        "as long as the granaries endure", "as long as the granaries stand",
        "as long as the grandstands endure", "as long as the grandstands stand",
        "as long as the gravelbars endure", "as long as the gravelbars stand",
        "as long as the greenhouses endure", "as long as the greenhouses stand",
        "as long as the grottos endure", "as long as the grottos stand",
        "as long as the gutters endure", "as long as the gutters stand",
        "as long as the gymnasiums endure", "as long as the gymnasiums stand",
        "as long as the halls endure", "as long as the halls stand",
        "as long as the hangars endure", "as long as the hangars stand",
        "as long as the headlands endure", "as long as the headwalls endure",
        "as long as the headwalls stand", "as long as the hedgerows endure",
        "as long as the hedges endure", "as long as the hillocks endure",
        "as long as the hillocks stand", "as long as the hinges endure",
        "as long as the hives endure", "as long as the hives stand",
        "until the chimneys crumble", "till the chimneys crumble",
        "until the cliffs erode", "till the cliffs erode",
        "until the coals go cold", "till the coals go cold",
        "until the dams burst", "till the dams burst",
        "until the dikes fail", "till the dikes fail",
        "until the docks rot", "till the docks rot",
        "until the domes fall", "till the domes fall",
        "until the doors splinter", "till the doors splinter",
        "until the dunes shift", "till the dunes shift",
        "until the eaves sag", "till the eaves sag",
        "until the fences lean", "till the fences lean",
        "until the fires die", "till the fires die",
        "until the flagstones crack", "till the flagstones crack",
        "until the floods recede", "till the floods recede",
        "until the fords silt up", "till the fords silt up",
        "until the furnaces cool", "till the furnaces cool",
        "until the glaciers melt", "until the granaries empty",
        "till the granaries empty", "until the gutters clog",
        "till the gutters clog", "until the harbors silt up",
        "till the harbors silt up", "until the hedges wither",
        "till the hedges wither", "until the hinges seize",
        "till the hinges seize",
    ))

    MARKERS_APPENDED = dict.fromkeys((
        "as long as the drawbridges stand", "as long as the fences stand",
        "as long as the girders stand", "as long as the guardhouses endure",
        "as long as the guardhouses stand", "as long as the guardrails endure",
        "as long as the guardrails stand", "as long as the harbors endure",
        "as long as the hedgerows stand", "as long as the hedges stand",
        "as long as the hinges stand",
    ))

    MARKERS_COMMA = dict.fromkeys((
        "until the gates rust shut", "till the gates rust shut",
    ))

    APPENDED = tuple(
        _GOVERNED_CLAIM + " %s." % word
        for word in MARKERS_BOTH) + tuple(
        _GOVERNED_CLAIM + " %s." % word
        for word in MARKERS_APPENDED)

    COMMA = tuple(
        _GOVERNED_CLAIM + ", %s." % word
        for word in MARKERS_BOTH) + tuple(
        _GOVERNED_CLAIM + ", %s." % word
        for word in MARKERS_COMMA)

    CONTROL_FALSE = (
        _GOVERNED_CLAIM + " as long as the abbeys endure.",
        _GOVERNED_CLAIM + ", as long as the abbeys endure.",
        _GOVERNED_CLAIM + " as long as the rivers run.",
        _GOVERNED_CLAIM + ", as long as the rivers run.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_appended_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.APPENDED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_comma_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMMA:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanVerbsConfFixR39Tests(unittest.TestCase):
    """Ruling 2740, S15-R39-CONF-8: journal verbs."""

    VERBS = dict.fromkeys((
        "allocates", "allots", "alphabetizes",
        "alternates", "alters", "amasses",
        "ambushes", "amends", "amerces",
        "amplifies", "amputates", "analyses",
        "analyzes", "animates", "annexes",
        "annihilates", "annotates", "annoys",
        "annuls", "anoints", "anticipates",
        "antiquates", "appeases", "appoints",
        "appraises", "appreciates", "apprehends",
        "approaches", "appropriates", "approves",
        "arbitrates", "archives", "arranges",
        "arrests", "ascribes", "assails",
        "assassinates", "assaults", "assembles",
        "assesses", "assigns", "assimilates",
        "assists", "associates", "assumes",
        "attaches", "attacks", "attempts",
        "attracts", "attributes", "audits",
        "authorises", "automates", "avenges",
        "averages", "averts", "awakens",
        "awards", "axiomatizes",
    ))

    INTEGRITY = tuple(
        "The journal %s integrity for every reader." % word
        for word in VERBS)

    CONTROL_FALSE = (
        "The journal ablates integrity for every reader.",
        "The journal nebulizes integrity for every reader.",
        "The journal abates integrity for every reader.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "Integrity label for the journal schedule.",
    )

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.INTEGRITY:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanNegationConfFixR39Tests(unittest.TestCase):
    """Ruling 2741, S15-R39-CONF-9: negation forms."""

    ROOTS = dict.fromkeys((
        "hardenable", "hedgeable", "hitchable",
        "hoopable", "houseable",
    ))

    VERB_FORMS = dict.fromkeys((
        "hardened", "hatched", "hedged",
        "hinged", "hitched", "held",
        "honed", "hooped", "hosed",
        "husked", "hydrated",
    ))

    NO_IS = tuple(
        "No record is %s after writing." % word
        for word in ROOTS) + tuple(
        "No record is %s after writing." % word
        for word in VERB_FORMS)

    NO_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in ROOTS) + tuple(
        "No record can be %s after writing." % word
        for word in VERB_FORMS)

    CONTROL_FALSE = (
        "Records are gashable after writing.",
        "Records are gathered after writing.",
    ) + tuple(
        "Records are %s after writing." % word
        for word in ROOTS) + tuple(
        "Records are %s after writing." % word
        for word in VERB_FORMS)

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_no_is_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_IS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_no_can_be_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanDisclosureConfFixR39Tests(unittest.TestCase):
    """Ruling 2742, S15-R39-CONF-10: disclosure roots and verbs."""

    ROOTS = dict.fromkeys((
        "handleable", "hangable", "harmable",
        "hateable", "haulable", "hauntable",
        "hazardable", "hearable", "heavable",
        "heedable", "heightenable", "helpable",
        "hideable", "hijackable", "hinderable",
        "hintable", "hirable", "hissable",
        "hoardable", "hoaxable", "hobbleable",
        "holeable", "hollowable", "honeable",
        "hookable", "hopable", "hopeable",
        "hoseable", "houndable", "hoverable",
        "howlable", "huddleable", "huffable",
        "huggable", "hullable", "humable",
        "humanizable", "humbleable", "humidifiable",
        "hummable", "humourable", "humpable",
        "huntable", "hurdleable", "hurlable",
        "hurriable", "hurtable", "husbandable",
        "hushable", "huskable", "hustleable",
        "hybridizable", "hydratable",
    ))

    VERB_FORMS = dict.fromkeys((
        "handled", "hanged", "haunted",
        "healed", "heard", "heated",
        "heeded", "helped", "hindered",
        "hinted", "hired", "hoarded",
        "hoisted", "holed", "hollowed",
        "hoped", "hounded", "hovered",
        "howled", "huddled", "huffed",
        "hugged", "hulled", "humbled",
        "hummed", "humped", "hunted",
        "hurdled", "hurled", "hurried",
        "hushed", "hustled", "hybridized",
    ))

    ROOT_RECORD_IS = tuple(
        "The record is %s after writing." % word
        for word in ROOTS)

    ROOT_ASSERTED = tuple(
        "Records are %s after writing." % word
        for word in ROOTS)

    ROOT_NO_IS = tuple(
        "No record is %s after writing." % word
        for word in ROOTS)

    ROOT_NO_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in ROOTS)

    VERB_ASSERTED = tuple(
        "Records are %s after writing." % word
        for word in VERB_FORMS)

    VERB_NO_IS = tuple(
        "No record is %s after writing." % word
        for word in VERB_FORMS)

    VERB_NO_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in VERB_FORMS)

    CONTROL_FALSE = (
        "Records are markable after writing.",
        "No record is markable after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_root_record_is_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_RECORD_IS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_root_asserted_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_root_no_is_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_NO_IS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_root_no_can_be_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_NO_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verb_asserted_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verb_no_is_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_NO_IS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verb_no_can_be_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_NO_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

