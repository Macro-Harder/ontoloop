"""Fix round 40, Region 1: report seal claim scan pins.

Rulings 2878 to 2897 of the Round 40 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R40-REPG-1 to 10 and the Confinement paper findings
S15-R40-CONF-1 to 10, on the templates those papers
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

class SealClaimScanInabilityRepGFixR40Tests(unittest.TestCase):
    """Ruling 2878, S15-R40-REPG-1: inability windows and followers."""

    FOLLOWERS = dict.fromkeys((
        "channelled", "concealed", "consolidated",
        "constituted", "constructed", "consumed",
        "crammed", "cramped", "crafted",
        "created", "crested", "cribbed",
        "crunched", "cultivated", "cultured",
        "customised", "dampened", "deepened",
        "defeathered", "defrosted", "degassed",
        "degermed", "dehumidified", "demoulded",
        "demounted", "denatured",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "capably", "carnivorously", "centrally",
        "chiefly", "circumstantially", "classically",
        "climatically", "clinically", "closely",
        "cognitively", "coherently", "coincidentally",
        "collaboratively", "colloquially", "colorfully",
        "commemoratively", "communally", "comparatively",
        "compatibly", "compellingly", "competently",
        "compliantly", "complicatedly", "complimentarily",
        "compulsorily", "computationally", "concentrically",
        "conceptually", "conclusively", "concurrently",
        "conditionally", "confinedly", "confirmatively",
        "conjointly", "consecutively", "consensually",
        "conservatively", "considerably", "consonantly",
        "conspicuously", "contemporaneously", "contentiously",
        "contextually", "contractually", "contrastingly",
        "cooperatively", "coordinately", "correspondently",
        "correspondingly", "cosmically", "costively",
        "cozily", "craggily", "crampedly",
        "creakily", "creamily", "credulously",
        "crucially", "crunchily", "crystallinely",
        "culturally", "cumbersomely", "curatively",
        "curvaceously", "cutely", "cyclically",
        "daily", "danceably", "daringly",
        "dashingly", "dazzlingly", "deadly",
        "deafeningly", "deafly", "dearly",
        "deathly", "debatably", "debonairly",
        "decadently", "decently", "decimally",
        "decoratively", "decorously", "decreasingly",
        "dedicatedly", "deemingly", "deeply",
        "defectively", "defensively", "defensibly",
        "deferentially", "deferently", "deficiently",
        "deformingly", "degenerately", "delineatively",
        "deliriously", "deludingly", "delusively",
        "demandingly", "demeaningly", "dementedly",
        "demeritorily", "demoniacally", "demonstrably",
        "demonstratively", "demystifyingly", "deniably",
        "densely", "denyingly", "departmentally",
        "dependably", "dependently", "depictively",
        "depressingly", "depressively", "depthlessly",
        "deputatively", "derangedly", "derelictly",
        "derivatively", "derogatorily", "descendingly",
        "descriptively", "desertedly", "deservedly",
        "designatingly", "designedly", "desirably",
        "desirously", "despicably", "despitefully",
        "destitutely", "destructively", "detachably",
        "detachedly", "determinably", "determinately",
        "deterministically", "detestably", "detrimentally",
        "devaluatively", "devastatingly", "developmentally",
        "deviantly", "deviatingly", "deviledly",
        "devotionally", "devoutly", "dextrously",
        "diagonally", "dialogically", "diametrically",
        "diaphanously", "dichotomously", "didactically",
        "differently", "difficultly", "diffidently",
        "diffusely", "digestively", "dignifiedly",
        "dilatorily", "dilutely", "dimensionally",
        "diminutively", "dirtily", "disagreeably",
        "disappointedly", "disapprovingly", "disarmingly",
        "disarrangedly", "disastrously", "disbelievingly",
        "disclaimingly", "discomfitedly", "discomfortably",
        "disconnectedly", "discontentedly", "discordantly",
        "discountably", "discourageably", "discouragingly",
        "discourteously", "discrepantly", "discretely",
        "discriminately", "discriminatingly", "discursively",
        "discussively", "diseasedly", "disembarkedly",
        "disembodiedly", "disembowelledly", "disenabledly",
        "disenchantedly", "disengagedly", "disentanglingly",
        "disequilibratedly", "disestablishedly", "disfavoredly",
        "disfiguredly", "disgracefully", "disguisedly",
        "disgustingly", "disharmoniously", "dishearteningly",
        "dishonourably", "disillusionedly", "disincentively",
        "disinclinedly", "disinfectantly", "disingenuously",
        "disinterestedly", "disjointedly", "disjunctively",
        "disklessly", "dislikingly", "dislocatively",
        "dislogically", "disloyally", "dismantlingly",
        "dismountedly", "disobediently", "disobligingly",
        "disorderly", "disorganizedly", "disorientedly",
        "disparately", "dispensably", "dispersedly",
        "dispiritedly", "dispiritingly", "displaceably",
        "displacively", "displeasedly", "displeasingly",
        "disposably", "dispositionally", "disproportionately",
        "disputably", "disputatiously", "disqualifyingly",
        "disquietedly", "disquietingly", "disregardedly",
        "disreputably", "disrespectfully", "disruptively",
        "dissatisfactorily", "dissatisfiedly", "dissatisfyingly",
        "dissemblingly", "dissentiently", "dissentingly",
        "disservely", "dissertatively", "disserviceably",
        "dissidently", "dissimilarly", "dissimilatedly",
        "dissimulatingly", "dissipatively", "dissociatively",
        "dissolubly", "dissolutely", "dissonantly",
        "dissuasively", "distantly", "distastefully",
        "distendedly", "distinctly", "distinctively",
        "distortively", "distractingly", "distractively",
        "distressedly", "distressfully", "distressingly",
        "districtly", "distrustfully", "distrustingly",
        "disturbedly", "disturbingly", "disunitedly",
        "disyllabically", "ditchingly", "dithyrambically",
        "dittographically", "diurnally", "divagatively",
        "divalently", "divergently", "diversely",
        "diversifiably", "divestibly", "dividably",
        "dividedly", "dividually", "divinatively",
        "divinely", "divisibly", "divorceably",
        "dizzily", "dodderingly", "dodgily",
        "dodgingly", "doffedly", "doggily",
        "dogmatizingly", "doingly", "dollishly",
        "dolomitically", "dolorously", "dolourously",
        "domestically", "dominantly", "dominatively",
        "donatorily", "donatively", "donsily",
    ))

    MODAL_ONLY = dict.fromkeys((
        "contained",
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
        "Records are contained by outsiders.",
    )

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

class SealClaimScanGoverningRepGFixR40Tests(unittest.TestCase):
    """Ruling 2879, S15-R40-REPG-2: trailing governing forms."""

    PLACES = dict.fromkeys((
        "nunnery", "shrine", "synagogue",
        "temple", "tower", "transept",
    ))

    TIMES = dict.fromkeys((
        "eternity", "jubilee", "olympiad",
        "quindecennium",
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

class SealClaimScanPrefixedRepGFixR40Tests(unittest.TestCase):
    """Ruling 2880, S15-R40-REPG-3: prefixed compounds."""

    PREFIXES = dict.fromkeys((
        "fructo", "ileo",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "marblebone", "onyxbond", "jadebone",
        "ironbone", "tinbone", "zincbone",
        "oakbone", "pinebone",
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

class SealClaimScanWordingsRepGFixR40Tests(unittest.TestCase):
    """Ruling 2881, S15-R40-REPG-4: un, proof, and resistant wordings."""

    UN_WORDINGS = dict.fromkeys((
        "uncarded", "uncased", "unchamfered",
        "unchannelled", "uncoloured", "uncombined",
        "unconsolidated", "unconstructed", "uncontained",
        "uncrinkled", "uncrisped", "uncrumbled",
        "uncrunched", "uncrusted", "uncultivated",
        "uncultured", "uncustomised", "undampened",
        "undeepened", "undefrosted", "undegraded",
        "undehorned", "undehydrated", "undelinted",
        "undemoulded", "undemounted", "undenatured",
    ))

    PROOF_WORDINGS = dict.fromkeys((
        "piranhaproof", "pythonproof", "stagproof",
    ))

    RESISTANT_WORDINGS = dict.fromkeys((
        "piranharesistant", "pythonresistant", "stagresistant",
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

class SealClaimScanVerbsRepGFixR40Tests(unittest.TestCase):
    """Ruling 2882, S15-R40-REPG-5: journal verbs."""

    VERBS = dict.fromkeys((
        "harvests", "hashes", "ignores",
        "images", "imports", "improves",
        "informs", "initiates", "inspects",
        "installs", "integrates", "intends",
        "interacts", "intercepts", "interfaces",
        "interprets", "interrogates", "interrupts",
        "intersects", "intervenes", "interviews",
        "introduces", "invalidates", "inventories",
        "inverts", "invests", "investigates",
        "invites", "invokes", "involves",
        "iterates", "joins", "journals",
        "justifies", "launches", "layers",
        "learns", "leases", "lends",
        "levels", "levies", "liaises",
        "liberates", "licenses", "lifts",
        "limits", "links", "loads",
        "loans", "locates", "logs",
        "loops", "lowers", "machines",
        "mails", "manipulates", "marshals",
        "masks", "matches", "materialises",
        "maximises", "measures", "mediates",
        "memorises", "mentors", "merges",
        "merits", "messages", "minces",
        "minds", "mines", "minimises",
        "ministers", "mints", "misleads",
        "misses", "mistreats", "mitigates",
        "mixes", "mobilises", "models",
        "moderates", "modernises", "modifies",
        "modulates", "monitors", "motivates",
        "moulds", "mounts", "moves",
        "multiplies", "murders", "musters",
        "mutes", "mutilates", "nails",
        "navigates", "negotiates", "nests",
        "nets", "neutralises", "nominates",
        "normalises", "notices", "notifies",
        "nourishes", "nudges", "nurses",
        "nurtures", "obeys", "obtains",
        "occupies", "omits", "opens",
        "opposes", "optimises", "opts",
        "orbits", "organises", "ostracises",
        "outputs", "overrides", "overturns",
        "overwhelms", "owes", "paces",
        "packages", "packs", "pads",
        "pages", "pains", "pairs",
        "panels", "panics", "parcels",
        "pardons", "pares", "parks",
        "paroles", "parrots", "partners",
        "passes", "patents", "patronises",
        "pays", "peaks", "pecks",
        "pedals", "pegs", "penalises",
        "pensions", "perches", "perfects",
        "perks", "personalises", "phases",
        "phones", "photographs", "phrases",
        "picks", "pickets", "pictures",
        "pieces", "pierces", "piles",
        "pilfers", "pillages", "pills",
        "pilots", "pinches", "pines",
        "pings", "pinpoints", "pins",
        "pioneers", "pipes", "pirates",
        "pitches", "pities", "pivots",
        "placards", "places", "plagues",
        "plans", "plants", "plasters",
        "plays", "pleases", "plods",
        "plops", "ploughs", "plumbs",
        "plunges", "pluralises", "plunders",
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

class SealClaimScanMarkersRepGFixR40Tests(unittest.TestCase):
    """Ruling 2883, S15-R40-REPG-6: unconditional markers."""

    MARKERS_BOTH = dict.fromkeys((
        "till the orchards fall", "until the orchards wither",
        "while the orchards bloom", "as long as the vineyards stand",
        "till the vineyards fail", "until the harbours silt",
        "while the harbours deepen", "as long as the lighthouses shine",
        "till the beacons fade", "until the breakwaters crumble",
        "while the seawalls hold", "as long as the windmills turn",
        "till the windmills stop", "until the quarries flood",
        "until the silos rust", "while the stables shelter",
        "as long as the aviaries stand", "till the apiaries empty",
        "until the greenhouses crack", "while the watermills turn",
        "till the watchtowers fall", "while the causeways hold",
        "till the embankments breach", "until the reservoirs drain",
        "while the aqueducts flow",
    ))

    MARKERS_APPENDED = dict.fromkeys((
        "while the forges glow", "until the signal fires fade",
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

class SealClaimScanNegationRepGFixR40Tests(unittest.TestCase):
    """Ruling 2884, S15-R40-REPG-7: negation narrowing roots."""

    ROOTS = dict.fromkeys((
        "magnetisable", "mouldable", "mutilatable",
        "peelable", "peggable", "perceivable",
        "performable", "perfumable", "pickleable",
        "pillagable", "playable", "plunderable",
        "tarnishable", "testifiable", "toastable",
        "touchable",
    ))

    NO_IS = tuple(
        "No record is %s after writing." % word
        for word in ROOTS)

    NO_CAN = tuple(
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

    def test_no_can_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_CAN:
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

class SealClaimScanDisclosureRepGFixR40Tests(unittest.TestCase):
    """Ruling 2885, S15-R40-REPG-8: disclosure roots and verb forms."""

    ROOTS = dict.fromkeys((
        "machinable", "magnifiable", "maintainable",
        "manageable", "manipulable", "marshallable",
        "materialisable", "maturable", "maximisable",
        "mediatable", "migratable", "mindable",
        "minimisable", "misleadable", "mistreatable",
        "mobilisable", "moderatable", "modernisable",
        "modulatable", "motivatable", "multipliable",
        "musterable", "mutable", "mutterable",
        "nailable", "navigatable", "neutralisable",
        "nominatable", "normalisable", "notifiable",
        "nurtureable", "obstructable", "occupiable",
        "originatable", "oscillatable", "outputable",
        "overridable", "overturnable", "overwhelmable",
        "packagable", "packable", "paddable",
        "painable", "panicable", "pardonable",
        "parkable", "parolable", "parrotable",
        "participable", "partnerable", "passable",
        "patchable", "patrolable", "pavable",
        "peakable", "peckable", "pedalable",
        "peekable", "peepable", "peerable",
        "peltable", "penalisable", "pensionable",
        "perchable", "percolatable", "perishable",
        "perjurable", "perkable", "permeable",
        "permittable", "perplexable", "perseverable",
        "persistable", "personalisable", "persuadable",
        "perturbable", "perusable", "pervadable",
        "petitionable", "phasable", "phrasable",
        "pickable", "picketable", "pierceable",
        "pillable", "pilotable", "pineable",
        "pinpointable", "pinable", "pioneerable",
        "piratable", "pitchable", "pitiable",
        "pivotable", "placardable", "plagueable",
        "planable", "plantable", "pleadable",
        "pleasable", "plopable", "ploughable",
        "pluckable", "plumbable", "plungeable",
        "pluralisable", "tameable", "tangleable",
        "tasteable", "tattooable", "tauntable",
        "telegraphable", "telephoneable", "telescopeable",
        "tellable", "temperable", "templateable",
        "temptable", "tenantable", "tendable",
        "tenseable", "tentable", "termable",
        "terminable", "terraceable", "thankable",
        "thickenable", "thievable", "thinkable",
        "thinnable", "thirstable", "thrashable",
        "threadable", "threatenable", "threshable",
        "thriftable", "thrillable", "thrivable",
        "throbbable", "throneable", "throngable",
        "throwable", "thrustable", "thumbable",
        "thumpable", "thunderable", "thwartable",
        "ticketable", "tickleable", "tidyable",
        "tieable", "tightenable", "tillable",
        "timberable", "tinable", "tingeable",
        "tintable", "tipable", "tireable",
        "titheable", "tobogganable", "toddleable",
        "toeable", "toilable", "tokenable",
        "tolerable", "tollable", "tombable",
        "tonable", "tongable", "toughenable",
        "tourable", "tousleable", "towable",
        "towerable", "toxicable", "tradeable",
        "trailable", "traitorable", "transposable",
        "travelable", "traverseable", "treeable",
        "trembleable", "trenchable", "trespassable",
        "triable", "triangulable", "tributable",
        "trickable", "trickleable", "tridentable",
        "trifleable", "trifurcatable", "trifurcateable",
        "trilateralable", "trillable", "trillionable",
        "trimable", "trineable",
    ))

    VERB_FORMS = dict.fromkeys((
        "tamed", "tangled", "tasted",
        "tattooed", "taunted", "teemed",
        "teetered", "telescoped", "told",
        "tempted", "tenanted", "tended",
        "tensed", "tented", "termed",
        "terminated", "terraced", "terrified",
        "thanked", "thickened", "thieved",
        "thinned", "thirsted", "thrashed",
        "threatened", "threshed", "thrifted",
        "thrilled", "thrived", "throbbed",
        "throned", "thronged", "thrown",
        "thrummed",
    ))

    ROOT_FORMS = tuple(
        "No record is %s after writing." % word
        for word in ROOTS) + tuple(
        "No record can be %s after writing." % word
        for word in ROOTS) + tuple(
        "Records are %s after writing." % word
        for word in ROOTS)

    VERB_FORMS_ALL = tuple(
        "No record is %s after writing." % word
        for word in VERB_FORMS) + tuple(
        "No record can be %s after writing." % word
        for word in VERB_FORMS) + tuple(
        "Records are %s after writing." % word
        for word in VERB_FORMS)

    CONTROL_FALSE = (
        "Records are kickable after writing.",
        "Records are kicked after writing.",
        "No record is kickable after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_root_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_FORMS_ALL:
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

class SealClaimScanAttemptsPluralFixR40Tests(unittest.TestCase):
    """Ruling 2886, S15-R40-REPG-9: attempts, plural subject form."""

    PLURAL = (
        "The journals attempt integrity for every reader.",
    )

    CONTROL_FALSE = (
        "The journal attempts integrity for every reader.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "attempts charged as completed evaluations count",
    )

    def test_plural_subject_fails(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PLURAL:
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

class SealClaimScanShownFurtherFixR40Tests(unittest.TestCase):
    """Ruling 2887, S15-R40-REPG-10: shown, further constructions."""

    SHOWN = (
        "Records are shown before use.",
        "The record was shown after writing.",
        "Records get shown after writing.",
    )

    CONTROL_FALSE = (
        "Records are shown after writing.",
        "No record is shown after writing.",
        "No record can be shown after writing.",
        "No records are shown after writing.",
        "The records are shown after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "The override writes a permanent access record before "
        "any content is shown.",
    )

    def test_shown_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.SHOWN:
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

class SealClaimScanWindowConfFixR40Tests(unittest.TestCase):
    """Ruling 2888, S15-R40-CONF-1: window words, convergent limb."""

    WINDOW_WORDS = dict.fromkeys((
        "immaturely", "immeasurably", "immemorially",
        "immersively", "imminently", "immoderately",
        "immodestly", "immovably", "imperatively",
        "imperceptibly", "imperially", "impertinently",
        "imperviously", "impetuously", "impiously",
        "impishly", "implacably", "implausibly",
        "imploringly", "impolitely", "imponderably",
        "impotently", "impracticably", "impractically",
        "imprecisely", "improvidently", "improvingly",
        "imprudently", "impurely", "imputably",
        "imputatively", "inaccessibly", "inaccurately",
        "inadeptly", "inadmissibly", "inadventurously",
        "inadvisably", "inalienably", "inalterably",
        "inanimately", "inappetently", "inapplicably",
        "inappreciably", "inappreciatively", "inapprehensively",
        "inaptly", "inarguably", "inarticulately",
        "inartistically", "inattentively", "inauspiciously",
        "incalculably", "incandescently", "incantationally",
        "incapably", "incapaciously", "incestuously",
        "incipiently", "incisively", "incivilly",
        "inclemently", "inclinably", "incognitively",
        "incognizantly", "incombustibly", "incommodiously",
        "incommutably", "incomparably", "incompatibly",
        "incompetently", "incomprehensibly", "incomprehensively",
        "incompressibly", "inconceivably", "incongruently",
        "incongruously", "inconsequentially", "inconsiderably",
        "inconsiderately", "inconsistently", "inconstantly",
        "incontinently", "incontrovertibly", "inconvertibly",
        "inconvincingly", "incoordinately", "incorporeally",
        "incorrigibly", "incorruptibly", "increasingly",
        "incredibly", "incrementally", "incriminatingly",
        "inculpably", "incurably", "incuriously",
        "incursively", "indebtedly", "indecipherably",
        "indecorously", "indeliberately", "indelibly",
        "indelicately", "indescribably", "indeterminably",
        "indeterminately", "indicatively", "indigenously",
        "indigently", "indiscernibly", "indiscerptibly",
        "indiscretely", "indiscriminately", "indiscriminatingly",
        "indispensably", "indissolubly", "indistinctively",
        "indistinguishably", "inditedly", "indivertibly",
        "indivisibly", "indoctrinatingly", "indomitably",
        "indorsably", "indrawnly", "inducibly",
        "inductively", "industrially", "inebriantly",
        "inebriatedly", "inedibly", "ineducably",
        "ineducibly", "ineffaceably", "ineffectually",
        "inefficaciously", "ineligibly", "ineluctably",
        "ineludibly", "inemployably", "inenviably",
        "inequably", "inequally", "inequitably",
        "inequivalently", "ineradicably", "inerrably",
        "inerrantly", "inerringly", "inessentially",
        "inestimably", "inevocably", "inexactingly",
        "inexhaustively", "inexpediently", "inexperiencedly",
        "inexpiably", "inexpugnably", "inexpungibly",
        "inextensibly", "inextensively", "inextinguishably",
        "infanticidally", "infatuatedly", "infatuatingly",
        "infectively", "infelicitously", "infestedly",
        "infestingly", "infeudally", "infidelly",
        "infieldly", "infightingly", "xenophobically",
        "xerographically", "yawningly", "yeastily",
        "yelpingly", "yodelingly", "yodellingly",
        "yonderingly", "yonderly", "youngly",
        "yowlingly", "zealotishly", "zestedly",
        "zestingly", "zigzaggingly", "zigzagly",
        "zonally", "zoomorphically", "zygodactyly",
        "zygomorphically", "zymotically",
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

class SealClaimScanFollowersConfFixR40Tests(unittest.TestCase):
    """Ruling 2889, S15-R40-CONF-2: followers, convergent limb."""

    FOLLOWERS = dict.fromkeys((
        "ignited", "illuminated", "immersed",
        "impacted", "imparted", "impeded",
        "impelled", "implanted", "imploded",
        "imposed", "impressed", "incased",
        "incised", "inclined", "included",
        "incubated", "infected", "infested",
        "infiltrated", "infused", "ingrained",
        "inhabited", "inhaled", "inhibited",
        "injured", "inoculated", "instilled",
        "intensified", "interchanged", "interfiled",
        "interfused", "intergraded", "interjoined",
        "interknit", "interlaced", "interlaid",
        "interlaminated", "interlarded", "interlayered",
        "interleafed", "interlined", "interlinked",
        "interlooped", "intermatted",
    ))

    MODAL_ONLY = dict.fromkeys((
        "incorporated", "inflated", "ingested",
        "injected", "inserted", "installed",
        "insulated", "integrated", "initialed",
    ))

    MODAL = tuple(
        "Records cannot be %s after writing." % word
        for word in FOLLOWERS)

    ASSERTED = tuple(
        "Records are %s by outsiders." % word
        for word in FOLLOWERS)

    EXTRA_MODAL = tuple(
        "Records cannot be %s after writing." % word
        for word in MODAL_ONLY)

    CONTROL_FALSE = (
        "Records cannot be patinated after writing.",
        "Records are patinated by outsiders.",
        "Records cannot be blanketed after writing.",
        "Records are blanketed by outsiders.",
    ) + tuple(
        "Records are %s by outsiders." % word
        for word in MODAL_ONLY)

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

class SealClaimScanPrefixedConfFixR40Tests(unittest.TestCase):
    """Ruling 2890, S15-R40-CONF-3: prefixed compounds, convergent limb."""

    PREFIXES = dict.fromkeys((
        "nona", "nyctalo",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "kunzite", "kyanite", "lepidolite",
        "moldavite", "morganite",
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

class SealClaimScanWordingsConfFixR40Tests(unittest.TestCase):
    """Ruling 2891, S15-R40-CONF-4: proof and resistant wordings."""

    PROOF_WORDINGS = dict.fromkeys((
        "flycatcherproof", "funnelwebproof",
    ))

    RESISTANT_WORDINGS = dict.fromkeys((
        "flycatcherresistant", "funnelwebresistant",
    ))

    PROOF_STORE = tuple(
        "The store is %s." % word
        for word in PROOF_WORDINGS)

    PROOF_RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in PROOF_WORDINGS)

    RESISTANT_STORE = tuple(
        "The store is %s." % word
        for word in RESISTANT_WORDINGS)

    RESISTANT_RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in RESISTANT_WORDINGS)

    CONTROL_FALSE = (
        "The store is henproof.",
        "The store is foxresistant.",
        "The store is addaxproof.",
        "The store is addaxresistant.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_proof_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROOF_STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_proof_records_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROOF_RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_resistant_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RESISTANT_STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_resistant_records_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RESISTANT_RECORDS:
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

class SealClaimScanUnConfFixR40Tests(unittest.TestCase):
    """Ruling 2892, S15-R40-CONF-5: un wordings, convergent limb."""

    UN_WORDINGS = dict.fromkeys((
        "unattributed", "unauthorised", "unavailable",
        "unavailing", "unavenged", "unaveraged",
        "unaverted", "unbaked", "unbalanced",
        "unbanned", "unbased", "unbathed",
        "unbattered", "unbattled", "unbeamed",
        "unbearded", "unbeautified", "unbeckoned",
        "unbeclouded", "unbecoming", "unbedded",
        "unbedimmed", "unbedraggled", "unbedrenched",
        "unbedusted",
    ))

    UN_STORE = tuple(
        "The store is %s." % word
        for word in UN_WORDINGS)

    UN_RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDINGS)

    CONTROL_FALSE = (
        "The records are uncurled by outside writers.",
        "The store is unbadged.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_un_store_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.UN_STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_un_records_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.UN_RECORDS:
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

class SealClaimScanGoverningConfFixR40Tests(unittest.TestCase):
    """Ruling 2893, S15-R40-CONF-6: governing instruments."""

    INSTRUMENTS = dict.fromkeys((
        "lease", "policy", "precedent",
    ))

    GOVERNED = tuple(
        "The seal guarantees protection by the %s of "
        "the deployment confinement fact." % word
        for word in INSTRUMENTS) + tuple(
        "The seal guarantees protection under the %s of "
        "the deployment confinement fact." % word
        for word in INSTRUMENTS)

    WEATHER = tuple(
        "The seal guarantees protection by the %s of "
        "the weather." % word
        for word in INSTRUMENTS) + tuple(
        "The seal guarantees protection under the %s of "
        "the weather." % word
        for word in INSTRUMENTS)

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

    def test_governed_stand(self):
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
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

class SealClaimScanMarkersConfFixR40Tests(unittest.TestCase):
    """Ruling 2894, S15-R40-CONF-7: unconditional markers, convergent limb."""

    ASLONG_BOTH = dict.fromkeys((
        "as long as the icebergs endure", "as long as the icebergs stand",
        "as long as the inns endure", "as long as the inns stand",
        "as long as the jungles endure", "as long as the jungles stand",
        "as long as the kilns endure", "as long as the kilns stand",
        "as long as the lakes endure", "as long as the lakes stand",
        "as long as the lanterns endure", "as long as the lanterns stand",
        "as long as the ledges endure", "as long as the lochs endure",
        "as long as the lochs stand", "as long as the lodges endure",
        "as long as the lookouts endure", "as long as the lookouts stand",
        "as long as the looms endure", "as long as the looms stand",
        "as long as the mangroves endure", "as long as the manors endure",
        "as long as the manors stand", "as long as the mansions endure",
        "as long as the mansions stand", "as long as the markets stand",
        "as long as the masts endure", "as long as the masts stand",
        "as long as the mausoleums endure", "as long as the mausoleums stand",
        "as long as the mills stand", "as long as the mines endure",
        "as long as the mines stand", "as long as the monasteries endure",
        "as long as the monasteries stand", "as long as the monuments endure",
        "as long as the monuments stand", "as long as the moorings endure",
        "as long as the moorings stand", "as long as the mosques endure",
        "as long as the mosques stand", "as long as the motels endure",
        "as long as the motels stand", "as long as the mountains endure",
    ))

    ASLONG_APPENDED = dict.fromkeys((
        "as long as the ledges stand", "as long as the lodges stand",
        "as long as the markets endure", "as long as the mills endure",
    ))

    UNTIL_BOTH = dict.fromkeys((
        "until the ice melts", "till the ice melts",
        "until the lakes freeze", "till the lakes freeze",
        "until the lanterns dim", "till the lanterns dim",
        "until the levees break", "till the levees break",
        "until the marshes dry", "till the marshes dry",
        "until the mills stop", "till the mills stop",
        "until the moats drain", "till the moats drain",
    ))

    UNTIL_APPENDED = dict.fromkeys((
        "until the locks rust", "till the locks rust",
    ))

    APPENDED = tuple(
        _GOVERNED_CLAIM + " %s." % word
        for word in ASLONG_BOTH) + tuple(
        _GOVERNED_CLAIM + " %s." % word
        for word in ASLONG_APPENDED) + tuple(
        _GOVERNED_CLAIM + " %s." % word
        for word in UNTIL_BOTH) + tuple(
        _GOVERNED_CLAIM + " %s." % word
        for word in UNTIL_APPENDED)

    COMMA = tuple(
        _GOVERNED_CLAIM + ", %s." % word
        for word in ASLONG_BOTH) + tuple(
        _GOVERNED_CLAIM + ", %s." % word
        for word in UNTIL_BOTH)

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

class SealClaimScanVerbsConfFixR40Tests(unittest.TestCase):
    """Ruling 2895, S15-R40-CONF-8: journal verbs, convergent limb."""

    VERBS = dict.fromkeys((
        "balances", "bans", "batches",
        "blanks", "blurs", "bonds",
        "borders", "borrows", "breaches",
        "breaks", "briefs", "broadens",
        "bruises", "brushes", "budgets",
        "buffers", "builds", "bulks",
        "bumps", "bunches", "bundles",
        "burdens", "buries",
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

class SealClaimScanNegationConfFixR40Tests(unittest.TestCase):
    """Ruling 2896, S15-R40-CONF-9: negation forms, convergent limb."""

    FORMS = (
        "No record is immovable after writing.",
        "No record can be immovable after writing.",
        "No record is inlaid after writing.",
        "No record can be inlaid after writing.",
    )

    CONTROL_FALSE = (
        "Records are immovable after writing.",
        "Records are inlaid after writing.",
        "No record is gashable after writing.",
        "No record is gathered after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_no_opening_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
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

class SealClaimScanDisclosureConfFixR40Tests(unittest.TestCase):
    """Ruling 2897, S15-R40-CONF-10: disclosure roots and verbs."""

    ROOTS = dict.fromkeys((
        "immersible", "impairable", "impeachable",
        "inaugurable", "incisable", "incitable",
        "incorporable", "indicatable", "indorsable",
        "indulgeable", "infectable", "inferable",
        "inferrable", "infestable", "infixable",
        "infringable", "infusable", "ingraftable",
        "injurable", "inlettable", "innovable",
        "inoculable", "inquirable", "insulable",
        "integrable",
    ))

    VERB_FORMS = dict.fromkeys((
        "ignited", "illuminated", "immersed",
        "impaired", "imparted", "implanted",
        "impressed", "improved", "inaugurated",
        "incised", "inclined", "included",
        "increased", "indorsed", "infected",
        "infested", "infixed", "inflicted",
        "infused", "ingrafted", "inhabited",
        "inhaled", "injured", "inoculated",
        "instated", "instilled",
    ))

    ROOT_FORMS = tuple(
        "The record is %s after writing." % word
        for word in ROOTS) + tuple(
        "Records are %s after writing." % word
        for word in ROOTS) + tuple(
        "No record is %s after writing." % word
        for word in ROOTS) + tuple(
        "No record can be %s after writing." % word
        for word in ROOTS)

    VERB_FORMS_ALL = tuple(
        "Records are %s after writing." % word
        for word in VERB_FORMS) + tuple(
        "No record is %s after writing." % word
        for word in VERB_FORMS) + tuple(
        "No record can be %s after writing." % word
        for word in VERB_FORMS)

    CONTROL_FALSE = (
        "Records are markable after writing.",
        "No record is markable after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE

    def test_root_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ROOT_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_FORMS_ALL:
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


if __name__ == "__main__":
    unittest.main()
