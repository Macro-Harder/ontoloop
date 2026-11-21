"""Fix round 38, Region 1: report seal claim scan pins.

Rulings 2573 to 2590 of the Round 38 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R38-REPG-1 to 8 and the Confinement paper findings
S15-R38-CONF-1 to 10, on the templates those papers
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

class SealClaimScanInabilityRepGFixR38Tests(unittest.TestCase):
    """Ruling 2573, S15-R38-REPG-1: inability windows and followers."""

    FOLLOWERS = dict.fromkeys((
        "draped", "ejected", "engulfed",
        "entrenched", "escorted", "feathered",
        "fitted", "flapped", "fledged",
        "fleshed", "flushed", "fuelled",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "validly", "vapidly", "variably",
        "vastly", "vehemently", "venerably",
        "venomously", "verbally", "verbosely",
        "veritably", "vertically", "vibrantly",
        "vicariously", "victoriously", "vigilantly",
        "vigorously", "villainously", "virulently",
        "visibly", "viscerally", "visually",
        "vitally", "vividly", "vocally",
        "volubly", "voluptuously", "voraciously",
        "vulnerably", "waggishly", "wakefully",
        "warily", "wastefully", "waveringly",
        "weakly", "weepingly", "weirdly",
        "whimsically", "wholesomely", "widely",
        "wincingly", "windingly", "winningly",
        "witlessly", "wittily", "wonderingly",
        "wonderfully", "woozily", "wordily",
        "yieldingly", "youthfully", "zanily",
        "zestfully",
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

    EXTRA_MODAL = (
        "Records cannot be flashed after writing.",
    )

    CONTROL_FALSE = (
        "Records cannot be electroplated by outsiders.",
        "Records cannot truculently be altered after writing.",
        "Records cannot be quilted by outsiders.",
        "Records are flashed by outsiders.",
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

    def test_extra_modal_follower_fails(self):
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


class SealClaimScanGoverningRepGFixR38Tests(unittest.TestCase):
    """Ruling 2574, S15-R38-REPG-2: trailing governing forms."""

    TRAILING_PLACES = dict.fromkeys((
        "observatory", "planetarium",
        "aquarium", "terrarium",
        "sanatorium", "crematorium",
        "auditorium", "mausoleum",
        "colosseum", "cathedral",
        "pagoda", "pavilion",
        "gazebo", "rotunda",
        "atrium", "cloister",
        "refectory", "scriptorium",
    ))

    TRAILING_TIMES = dict.fromkeys((
        "fortnight", "eon",
        "instant", "second",
        "jiffy", "quarter",
        "semester", "trimester",
        "biennium", "lustrum",
        "minute",
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


class SealClaimScanPrefixedRepGFixR38Tests(unittest.TestCase):
    """Ruling 2575, S15-R38-REPG-3: prefixed compounds."""

    PREFIXES = dict.fromkeys((
        "meningo", "pelvio", "phaco",
        "tubo", "typhlo", "urico",
        "uveo", "vagino", "varico",
        "vivi",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "ivorybone", "hornbone", "shellwood",
        "stonewood",
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


class SealClaimScanWordingsRepGFixR38Tests(unittest.TestCase):
    """Ruling 2576, S15-R38-REPG-4: un, proof, resistant wordings."""

    UN_WORDINGS = dict.fromkeys((
        "unedged", "uneffaced", "unfestooned",
        "unfitted", "unflanked", "unflapped",
        "unfleshed", "unflushed", "unfoiled",
        "unfuelled",
    ))

    PROOF_WORDINGS = dict.fromkeys((
        "dragonflyproof", "dugongproof", "dingoproof",
        "dormouseproof", "dragonproof", "drakeproof",
        "dromedaryproof", "duikerproof", "earthwormproof",
        "echidnaproof", "egretproof", "eiderproof",
        "elandproof", "ermineproof", "fireflyproof",
        "flounderproof", "fulmarproof",
    ))

    RESISTANT_WORDINGS = dict.fromkeys((
        "dragonflyresistant", "dugongresistant", "dingoresistant",
        "dormouseresistant", "dragonresistant", "drakeresistant",
        "dromedaryresistant", "duikerresistant", "earthwormresistant",
        "earwigresistant", "echidnaresistant", "egretresistant",
        "eiderresistant", "elandresistant", "ermineresistant",
        "fireflyresistant", "flearesistant", "flounderresistant",
        "fulmarresistant",
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
        "The records are unescorted by outside writers.",
        "The store is unescorted.",
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


class SealClaimScanVerbsRepGFixR38Tests(unittest.TestCase):
    """Ruling 2577, S15-R38-REPG-5: claim verbs."""

    VERBS = dict.fromkeys((
        "dampens", "daunts", "deadens",
        "deafens", "debates", "debunks",
        "deceives", "decides", "decodes",
        "decorates", "decoys", "dedicates",
        "defaces", "defames", "defeats",
        "defers", "defies", "defiles",
        "deflects", "defrauds", "defrosts",
        "defuses", "degrades", "delays",
        "delegates", "deletes", "deludes",
        "demeans", "demolishes", "demotes",
        "denies", "denounces", "departs",
        "depends", "depraves", "depresses",
        "deprives", "deranges", "desecrates",
        "deserts", "designates", "designs",
        "desires", "desists", "desolates",
        "despoils", "destroys", "detaches",
        "details", "detains", "detects",
        "deters", "deteriorates",
    ))

    INTEGRITY = tuple(
        "The journal %s integrity for every reader." % word
        for word in VERBS)

    CONTROL_FALSE = (
        "The journal narrates integrity for every reader.",
        "The journal undulates integrity for every reader.",
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


class SealClaimScanMarkersRepGFixR38Tests(unittest.TestCase):
    """Ruling 2578, S15-R38-REPG-6: unconditional markers."""

    MARKERS_BOTH = dict.fromkeys((
        "till the saltflats crack", "until the steppes burn",
        "while the savannas flood", "as long as the sequoias stand",
        "till the sequoias fall", "until the sycamores fall",
        "while the willows weep", "as long as the waterfalls flow",
        "till the waterfalls dry", "until the whirlpools still",
        "while the waves withdraw", "as long as the wetlands endure",
        "till the wetlands drain", "until the woodlands fall",
        "while the wheatfields wave", "as long as the snowfields stand",
        "till the snowfields melt", "until the starfields fade",
        "while the stormclouds gather", "till the sandbanks shift",
        "until the seacliffs crumble", "while the surf retreats",
    ))

    MARKERS_APPENDED = dict.fromkeys((
        "as long as the saltflats stand", "as long as the sandbanks stand",
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


class SealClaimScanNegationRepGFixR38Tests(unittest.TestCase):
    """Ruling 2579, S15-R38-REPG-7: negation narrowing roots."""

    ROOTS = dict.fromkeys((
        "identifiable", "joinable",
    ))

    NO_IS = tuple(
        "No record is %s after writing." % word
        for word in ROOTS)

    NO_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in ROOTS)

    ASSERTED_ANALOGUES = tuple(
        "Records are %s after writing." % word
        for word in ROOTS)

    CONTROL_FALSE = (
        "No record is harvestable after writing.",
        "No record can be harvestable after writing.",
    )

    CONTROL_TRUE = _PLAIN_CONTROLS_TRUE + (
        "No bundle name was hidden in this record.",
        "The seal does not guarantee protection.",
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

    def test_asserted_analogues_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_ANALOGUES:
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


class SealClaimScanDisclosureRepGFixR38Tests(unittest.TestCase):
    """Ruling 2580, S15-R38-REPG-8: roots outside judged roots."""

    ROOTS = dict.fromkeys((
        "kickable", "killable", "kindleable",
        "kissable", "kneadable", "knifeable",
        "knitable", "knockable", "knotable",
        "knowable", "labelable", "lamentable",
        "laminateable", "lanceable", "landable",
        "lashable", "latheable", "laughable",
        "launchable", "launderable", "lavishable",
        "layerable", "leadable", "leafable",
        "leanable", "leapable", "learnable",
        "lectureable", "leechable", "lendable",
        "lengthenable", "levelable", "levyable",
        "libelable", "lickable", "lightable",
        "likeable", "likenable", "limeable",
        "limitable", "limpable", "lineable",
        "litigateable", "litterable", "liveable",
        "loafable", "loanable", "loatheable",
        "lobable", "loftable", "logable",
        "lookable", "loomable", "loopable",
        "loosenable", "lopable", "loseable",
        "loungeable", "loveable", "lowerable",
        "lubricateable", "lugable", "lullable",
        "lumberable", "lumpable", "lunchable",
        "lungeable", "lurchable", "lureable",
        "lurkable", "lynchable", "ignitable",
        "ignorable", "illuminable", "imitable",
        "impartable", "implantable", "improvable",
        "inclinable", "includable", "increasable",
        "indictable", "inducible", "infestible",
        "infiltratable", "inflatable", "inflectable",
        "inflictable", "influenceable", "informable",
        "infringible", "infusible", "ingestible",
        "inhabitable", "inhalable", "inheritable",
        "inhibitable", "injectable", "inlayable",
        "innovatable", "inputable", "insinuable",
        "inspirable", "installable", "instructable",
        "jettisonable", "judgeable", "jumbleable",
        "jumpable",
    ))

    VERB_FORMS = dict.fromkeys((
        "kicked", "killed", "kindled",
        "kissed", "kneaded", "knifed",
        "knocked", "known", "lamented",
        "lanced", "landed", "laughed",
        "launched", "laundered", "lavished",
        "led", "leafed", "leaned",
        "leaped", "learned", "left",
        "lectured", "leeched", "lengthened",
        "levelled", "libelled", "licked",
        "lighted", "liked", "likened",
        "limed", "limited", "limped",
        "litigated", "littered", "lived",
        "loafed", "loathed", "lobbed",
        "lofted", "looked", "loomed",
        "loosened", "lopped", "lost",
        "lounged", "loved", "lowered",
        "lugged", "lulled", "lumbered",
        "lumped", "lunched", "lunged",
        "lurched", "lured", "lurked",
        "lynched",
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
        "Records are excerpted after writing.",
        "No record is leased after writing.",
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


class SealClaimScanWindowConfFixR38Tests(unittest.TestCase):
    """Ruling 2581, S15-R38-CONF-1: window words, convergent limb."""

    WINDOW_WORDS = dict.fromkeys((
        "tacitly", "tactlessly", "tangentially",
        "tangibly", "tantalizingly", "tastelessly",
        "tautly", "tawdrily", "telegraphically",
        "telepathically", "temperately", "tenably",
        "tentatively", "tenuously", "terminally",
        "terrifically", "territorially", "thanklessly",
        "theatrically", "thematically", "therapeutically",
        "thermally", "thornily", "thriftlessly",
        "tidily", "tightly", "timelessly",
        "tirelessly", "tiresomely", "titanically",
        "tolerably", "tolerantly", "tonally",
        "tonelessly", "tonically", "topically",
        "torrentially", "tortuously", "torturously",
        "toughly", "toxicly", "toxically",
        "traditionally", "tragically", "trainedly",
        "traitorously", "transcendently", "transiently",
        "translucently", "transparently", "transversely",
        "traumatically", "travelingly", "treasonably",
        "treasonously", "tremendously", "tremulously",
        "trenchantly", "trendily", "triadically",
        "tribally", "trickily", "triflingly",
        "trimly", "troublingly", "troublously",
        "truantly", "trustfully", "truthlessly",
        "tumultuously", "tunefully", "tunelessly",
        "turbidly", "turgidly", "tutorially",
        "twangily", "tweezingly", "twilightly",
        "tympanically", "tyrannically", "tyrannously",
        "ubiquitously", "uglily", "ultimately",
        "ultramodernly", "unaccountably", "unadvisedly",
        "unaffectedly", "unambitiously", "unamiably",
        "unanimatedly", "unanimously", "unanswerably",
        "unappealingly", "unappreciatively", "unapproachably",
        "unarguably", "unassumingly", "unattachedly",
        "unattainably", "unattendedly", "unattractively",
        "unauthoritatively", "unavailably", "unavoidably",
        "unbearably", "unbelievably", "unbelievingly",
        "unbendably", "unblinkingly", "unblushingly",
        "unboundedly", "unbreakably", "unbridledly",
        "unbrotherly", "unburdenedly", "unbuttonedly",
        "uncannily", "uncaringly", "unceremoniously",
        "unchallengably", "unchallengedly", "unchangingly",
        "uncharitably", "unchastely", "uncheckedly",
        "uncheerfully", "unchivalrously", "uncivilly",
        "uncivilizedly", "unclaimedly", "unclassifiably",
        "uncleverly", "unclimbably", "unclinchably",
        "uncloggedly", "unclumsily", "uncoachedly",
        "uncoatedly", "uncoercively", "uncoherently",
        "uncoincidentally", "uncollaboratively", "uncollapsedly",
        "uncollectively", "uncoloredly", "uncolourably",
        "uncombedly", "uncomfortably", "uncommittedly",
        "uncommonly", "uncommunicatively", "uncomparably",
        "uncompassionately", "uncompatibly", "uncompetitively",
        "uncomplainingly", "uncomplicatedly", "uncompliantly",
        "uncomplimentarily", "uncompoundedly", "uncompressedly",
        "uncompromisingly", "unconcealedly", "unconcernedly",
        "unconcertedly", "unconciliatorily", "uncondemnedly",
        "unconfidently", "unconfinedly", "unconfirmably",
        "unconflictedly", "unconformably", "unconfusedly",
        "uncongenially", "uncongestedly", "unconjugatedly",
        "unconjunctively", "unconnectedly", "unconquerably",
        "unconqueredly", "unconscientiously", "unconsciously",
        "unconsecratedly", "unconsecutively", "unconsentingly",
        "unconsequentially", "unconservatively",
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

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanFollowersConfFixR38Tests(unittest.TestCase):
    """Ruling 2582, S15-R38-CONF-2: followers."""

    FOLLOWERS_BOTH = dict.fromkeys((
        "blanketed", "bridled", "bulked",
        "bunkered", "buoyed", "canopied",
        "cartoned", "chambered", "chocked",
        "choked", "chuted", "cinched",
        "circled", "closeted", "clotted",
        "clubbed", "clutched", "cocked",
        "coffined", "columned", "compassed",
        "computerized",
    ))

    FOLLOWERS_MODAL = dict.fromkeys((
        "clustered", "combined", "compacted",
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

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONTROL_TRUE:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        for statement in self.CONTROL_FALSE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)


class SealClaimScanPrefixedConfFixR38Tests(unittest.TestCase):
    """Ruling 2583, S15-R38-CONF-3: prefixed compounds."""

    PREFIXES = dict.fromkeys((
        "acantho", "archeo", "atmo",
        "bryo", "caco", "calli",
        "cauli", "cero", "chaeto",
        "cheilo", "chilio", "chylo",
        "cine", "concho", "cyatho",
        "cyna", "cyno", "dacryo",
        "deino", "dema", "demo",
        "dexi", "dicho",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "acorn", "arrow", "porphyry",
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
        "Every record stands pantoverified before use.",
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


class SealClaimScanAnimalsConfFixR38Tests(unittest.TestCase):
    """Ruling 2584, S15-R38-CONF-4: proof and resistant wordings."""

    PROOF_WORDINGS = dict.fromkeys((
        "addaxproof", "agoutiproof", "alligatorproof",
        "anchovyproof", "anteaterproof", "arapaimaproof",
        "argaliproof", "arrowcrabproof", "aukproof",
        "aukletproof", "avocetproof", "bactriancamelproof",
        "barbelproof", "barbetproof", "barnacleproof",
        "bassproof", "bassletproof", "beardeddragonproof",
        "belugaproof", "bengaltigerproof", "bettongproof",
        "bichirproof", "bighornproof", "bilbyproof",
        "bitternproof", "blackbuckproof", "blackcapproof",
        "blackflyproof", "blackmarlinproof", "blackswanproof",
        "blennyproof", "bloodhoundproof", "blowfishproof",
        "bluebottleproof", "bluecrabproof", "bluefishproof",
        "bluegillproof", "bluejayproof", "bluemarlinproof",
        "bluetangproof", "bluetitproof", "bluewhaleproof",
        "bobolinkproof", "bobwhiteproof", "bogueproof",
        "bollweevilproof", "bollwormproof", "bombardierbeetleproof",
        "bongoproof", "bontebokproof", "boobyproof",
    ))

    RESISTANT_WORDINGS = dict.fromkeys((
        "addaxresistant", "agoutiresistant", "alligatorresistant",
        "anchovyresistant", "anteaterresistant", "aphidresistant",
        "arapaimaresistant", "argaliresistant", "arrowcrabresistant",
        "aukresistant", "aukletresistant", "avocetresistant",
        "bactriancamelresistant", "barbelresistant", "barbetresistant",
        "barnacleresistant", "bassresistant", "bassletresistant",
        "beardeddragonresistant", "bedbugresistant", "beeresistant",
        "belugaresistant", "bengaltigerresistant", "bettongresistant",
        "bichirresistant", "bighornresistant", "bilbyresistant",
        "bitternresistant", "blackbuckresistant", "blackcapresistant",
        "blackflyresistant", "blackmarlinresistant", "blackswanresistant",
        "blennyresistant", "bloodhoundresistant", "blowfishresistant",
        "bluebottleresistant", "bluecrabresistant", "bluefishresistant",
        "bluegillresistant", "bluejayresistant", "bluemarlinresistant",
        "bluetangresistant", "bluetitresistant", "bluewhaleresistant",
        "bobolinkresistant", "bobwhiteresistant", "bogueresistant",
        "bollweevilresistant", "bollwormresistant", "bombardierbeetleresistant",
        "bongoresistant", "bontebokresistant", "boobyresistant",
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
        "The store is anvilproof.",
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


class SealClaimScanUnConfFixR38Tests(unittest.TestCase):
    """Ruling 2585, S15-R38-CONF-5: un wordings."""

    UN_WORDINGS = dict.fromkeys((
        "unabated", "unabbreviated", "unabdicated",
        "unabolished", "unaborted", "unabraded",
        "unabridged", "unabsorbed", "unabstracted",
        "unabused", "unaccelerated", "unaccented",
        "unaccepted", "unacclaimed", "unacclimated",
        "unaccomplished", "unaccorded", "unaccounted",
        "unaccredited", "unaccrued", "unaccumulated",
        "unaccused", "unaccustomed", "unacknowledged",
        "unacquainted", "unacquiesced", "unacquired",
        "unacquitted", "unacted", "unactuated",
        "unadapted", "unadded", "unaddicted",
        "unaddressed", "unadhered", "unadjoined",
        "unadjourned", "unadjudged", "unadministered",
        "unadmired", "unadmitted", "unadopted",
        "unadored", "unadorned", "unadvanced",
        "unadvantaged", "unadvertised", "unadvised",
        "unadvocated", "unaerated", "unaffiliated",
        "unaffirmed", "unafflicted", "unafforded",
        "unaffronted",
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


class SealClaimScanGoverningConfFixR38Tests(unittest.TestCase):
    """Ruling 2586, S15-R38-CONF-6: governing instruments."""

    PHRASINGS = dict.fromkeys((
        "by the acclaim of", "by the acclamation of",
        "by the act of", "by the advocacy of",
        "by the aid of", "by the allegiance of",
        "by the annunciation of", "by the approbation of",
        "by the assistance of", "by the attornment of",
        "by the authentication of", "by the backing of",
        "by the bail of", "by the ballot of",
        "by the bargain of", "by the benefaction of",
        "by the beneficence of", "by the benefit of",
        "by the benevolence of", "under the acclaim of",
        "under the acclamation of", "under the act of",
        "under the advocacy of", "under the aid of",
        "under the allegiance of", "under the annunciation of",
        "under the approbation of", "under the assistance of",
        "under the attornment of", "under the authentication of",
        "under the backing of", "under the bail of",
        "under the ballot of", "under the bargain of",
        "under the benefaction of", "under the beneficence of",
        "under the benefit of", "under the benevolence of",
    ))

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


class SealClaimScanMarkersConfFixR38Tests(unittest.TestCase):
    """Ruling 2587, S15-R38-CONF-7: unconditional markers, convergent limb."""

    MARKERS_BOTH = dict.fromkeys((
        "as long as the abbeys endure", "as long as the abbeys stand",
        "as long as the abutments endure", "as long as the abutments stand",
        "as long as the arches endure", "as long as the arches stand",
        "as long as the archways endure", "as long as the archways stand",
        "as long as the armories endure", "as long as the arsenals endure",
        "as long as the arsenals stand", "as long as the balustrades endure",
        "as long as the balustrades stand", "as long as the bandstands endure",
        "as long as the banks endure", "as long as the barns endure",
        "as long as the barns stand", "as long as the barracks endure",
        "as long as the barriers endure", "as long as the basins endure",
        "as long as the battlements endure", "as long as the battlements stand",
        "as long as the bayous endure", "as long as the bayous stand",
        "as long as the beaches endure", "as long as the belfries endure",
        "as long as the belfries stand", "as long as the berms endure",
        "as long as the berms stand", "as long as the berths endure",
        "as long as the berths stand", "as long as the bluffs endure",
        "as long as the boardwalks endure", "as long as the boathouses endure",
        "as long as the boathouses stand", "as long as the bollards endure",
        "as long as the bollards stand", "as long as the boulders endure",
        "as long as the boulders stand", "as long as the bowers endure",
        "as long as the bowers stand", "as long as the breezeways endure",
        "as long as the breezeways stand", "as long as the brickworks endure",
        "as long as the bridlepaths endure", "as long as the bridlepaths stand",
        "as long as the brooks endure", "as long as the brooks stand",
        "as long as the buildings endure", "as long as the buildings stand",
        "as long as the bulkheads endure", "as long as the bulkheads stand",
        "as long as the bunkers endure", "as long as the bunkers stand",
        "as long as the bunkhouses endure", "as long as the bunkhouses stand",
        "as long as the buoys endure", "as long as the buoys stand",
        "as long as the buttes endure", "as long as the bypasses endure",
        "as long as the bypasses stand", "as long as the bypaths endure",
        "as long as the bypaths stand", "as long as the byroads endure",
        "as long as the byroads stand", "as long as the byways endure",
        "as long as the byways stand", "as long as the cabins endure",
        "as long as the cabins stand", "as long as the cableways endure",
        "as long as the cairns endure", "as long as the cairns stand",
        "as long as the caves endure", "as long as the caves stand",
        "until the beams rot", "till the beams rot",
        "until the bells crack", "till the bells crack",
        "until the boards warp", "till the boards warp",
        "until the bolts shear", "till the bolts shear",
        "until the books burn", "till the books burn",
        "until the branches fall", "till the branches fall",
        "until the bricks crack", "till the bricks crack",
        "until the brooks dry up", "till the brooks dry up",
        "until the buckets rust", "till the buckets rust",
        "until the cables fray", "till the cables fray",
        "until the candles gutter", "till the candles gutter",
        "until the carts break", "till the carts break",
        "until the caves flood", "till the caves flood",
    ))

    MARKERS_APPENDED = dict.fromkeys((
        "as long as the armories stand", "as long as the bandstands stand",
        "as long as the banks stand", "as long as the barracks stand",
        "as long as the barriers stand", "as long as the boardwalks stand",
        "as long as the brickworks stand", "as long as the cableways stand",
        "until the anchors rust", "till the anchors rust",
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
        _GOVERNED_CLAIM + " as long as the rivers run.",
        _GOVERNED_CLAIM + ", as long as the rivers run.",
        _GOVERNED_CLAIM + " as long as the oceans stand.",
        _GOVERNED_CLAIM + ", as long as the oceans stand.",
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


class SealClaimScanVerbsConfFixR38Tests(unittest.TestCase):
    """Ruling 2588, S15-R38-CONF-8: journal verbs."""

    VERBS = dict.fromkeys((
        "abates", "abbreviates", "abdicates",
        "abolishes", "aborts", "abrades",
        "abridges", "abstracts", "abuses",
        "accelerates", "accents", "accepts",
        "acclimates", "accompanies", "accomplishes",
        "accords", "accounts", "accrues",
        "accumulates", "accuses", "acidulates",
        "acquaints", "acquiesces", "acquires",
        "acquits", "actuates", "adapts",
        "addicts", "addresses", "adheres",
        "adjoins", "adjourns", "adjudges",
        "adjusts", "admires", "adopts",
        "adorns", "advantages", "advises",
        "affiliates", "affixes", "afflicts",
        "aggrandizes", "aggravates", "aggrieves",
        "agitates", "agonizes", "agrees",
        "aids", "alarms", "alerts",
        "alienates", "alights", "aligns",
    ))

    INTEGRITY = tuple(
        "The journal %s integrity for every reader." % word
        for word in VERBS)

    CONTROL_FALSE = (
        "The journal ablates integrity for every reader.",
        "The journal nebulizes integrity for every reader.",
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


class SealClaimScanNegationConfFixR38Tests(unittest.TestCase):
    """Ruling 2589, S15-R38-CONF-9: negation forms."""

    ROOTS = dict.fromkeys((
        "gashable", "gatherable", "glazeable",
        "glueable", "groundable", "groutable",
    ))

    VERB_FORMS = dict.fromkeys((
        "gathered", "glazed", "grained",
        "grated", "greased", "grilled",
        "gripped", "grooved", "grounded",
        "grouted",
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
    )

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


class SealClaimScanDisclosureConfFixR38Tests(unittest.TestCase):
    """Ruling 2590, S15-R38-CONF-10: disclosure roots and verbs."""

    ROOTS = dict.fromkeys((
        "gaugable", "generable", "glaciable",
        "glanceable", "glassable", "gleanable",
        "glideable", "glimpseable", "glossable",
        "glowable", "gnashable", "gnawable",
        "grabbable", "graceable", "graftable",
        "grainable", "grappleable", "graspable",
        "grassable", "grateable", "graveable",
        "greaseable", "griddleable", "grievable",
        "grillable", "grimaceable", "grinable",
        "gripable", "gristable", "grittable",
        "grizzleable", "groomable", "groovable",
        "gropeable", "grossable", "groveable",
        "growlable", "grubbable", "grudgeable",
        "grumbleable", "gruntable", "guidable",
        "gutable", "guzzleable",
    ))

    VERB_FORMS = dict.fromkeys((
        "gauged", "glaciated", "glanced",
        "glassed", "gleaned", "glided",
        "glimpsed", "glossed", "glowed",
        "gnashed", "gnawed", "grabbed",
        "graced", "grafted", "grappled",
        "grasped", "grassed", "graved",
        "griddled", "grieved", "grimaced",
        "grinned", "gristed", "gritted",
        "grizzled", "groaned", "groomed",
        "groped", "grossed", "groved",
        "growled", "grubbed", "grudged",
        "grumbled", "grunted", "gulped",
        "gunned", "gushed", "gusted",
        "gutted", "guzzled", "generalized",
        "gloated", "gobbled", "goggled",
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

