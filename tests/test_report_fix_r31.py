"""Fix round 31, Region 1: report seal claim scan pins.

Rulings 1665 to 1672 of the Round 31 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers, the Report and golden span paper findings 1 to 8
and the Confinement paper findings 1 to 11 in their absorbed
limbs, on the templates those papers state. A form probed
in both raising papers on the one template stands counted
once, in the form of the triage merges: the greased, oiled,
knitted, and soaped followers of ruling 1665, the
cherrywood, dogwood, and linden elements of ruling 1667,
the unmanned, unpatrolled, unattended, and unsupervised
wordings of ruling 1668, the nine shared journal verbs of
ruling 1669, and the airmailed, couriered, telegraphed, and
telephoned verbs of ruling 1672 each stand counted once.
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


class SealClaimScanInabilityFixR31Tests(unittest.TestCase):
    """Ruling 1665: inability limb, followers and windows."""

    REPG_FOLLOWERS = (
        "iodinated", "dehydrogenated", "isomerized",
        "depolymerized", "pelletized", "micronized", "silanized",
        "brushed", "buffed", "oiled", "greased", "rinsed",
        "scrubbed", "dusted", "vacuumed", "ironed", "knitted",
        "soaped", "mopped", "swept", "hosed", "shotblasted",
        "tempered",
    )

    CONF_FOLLOWERS = (
        "brined", "brightened", "chiseled", "colored",
        "coloured", "covered", "crocheted", "darkened",
        "dulled", "embroidered", "greased", "greened",
        "hydrated", "inlaid", "knitted", "layered",
        "lightened", "lined", "lubricated", "marinated",
        "moisturized", "molded", "monogrammed", "oiled",
        "overlaid", "packaged", "padded", "pleated", "quilted",
        "reddened", "saturated", "shellacked", "soaped",
        "steeped", "surfaced", "tinted", "trimmed", "veneered",
        "blued",
    )

    MODAL_REPG = tuple(
        "Records cannot be %s by outsiders." % word
        for word in REPG_FOLLOWERS)

    MODAL_CONF = tuple(
        "Records cannot be %s after writing." % word
        for word in CONF_FOLLOWERS)

    ASSERTED = tuple(
        "Records are %s by outsiders." % word
        for word in dict.fromkeys(
            REPG_FOLLOWERS + CONF_FOLLOWERS + ("folded",)))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "sourly", "fretfully", "longingly", "offhandedly",
            "acidly", "caustically",
            "cautiously", "curiously", "diligently", "gladly",
            "gratefully", "hastily", "hopefully", "idly",
            "joyfully", "lazily", "politely", "promptly",
            "seriously", "thankfully", "thoughtfully", "wisely",
            "yearningly",
        ))

    WINDOW_PHRASES = tuple(
        "Records cannot in any %s be altered after writing."
        % place for place in (
            "alehouse", "birdhouse", "cookhouse", "customhouse",
            "doghouse", "dollhouse", "firehouse", "glasshouse",
            "henhouse", "icehouse", "madhouse", "manor",
            "meetinghouse", "penthouse", "roadhouse",
            "roundhouse", "statehouse", "teahouse", "tollhouse",
            "townhouse", "treehouse",
        ))

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_REPG + self.MODAL_CONF:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOW_WORDS + self.WINDOW_PHRASES:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be fluorinated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are fluorinated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be acetylated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are acetylated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be drilled after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot petulantly be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot covetously be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any millhouse be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any slaughterhouse be altered "
            "after writing."))
        self.assertFalse(
            _scan(mod, "Records cannot be folded by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be brominated by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanGoverningFixR31Tests(unittest.TestCase):
    """Ruling 1666: governing condition limb."""

    INSTRUMENTS = (
        "anathema", "assize", "ban", "breve", "cession",
        "concord", "concordat", "decretal", "diktat",
        "encyclical", "fatwa", "injunction", "interdict",
        "levy", "subpoena",
    )

    PHRASING_WORDS = (
        "under the government of", "under the hand of",
        "under the seal of", "by the seal of",
        "under the sign manual of",
    ) + tuple(
        "%s the %s of" % (prep, name)
        for name in INSTRUMENTS for prep in ("by", "under"))

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in PHRASING_WORDS)

    TRAILING_REPG = tuple(
        "The seal guarantees protection %s." % form for form in (
            "in all places where the deployment confinement "
            "fact holds",
            "through whatsoever place the deployment "
            "confinement fact holds",
            "whatsoever place the deployment confinement "
            "fact holds",
            "in whatsoever place the deployment confinement "
            "fact holds",
            "at whatsoever time the deployment confinement "
            "fact holds",
            "for whatsoever time the deployment confinement "
            "fact holds",
            "by whatever place the deployment confinement "
            "fact holds",
            "under whatever place the deployment confinement "
            "fact holds",
            "whencesoever the deployment confinement fact holds",
            "thencesoever the deployment confinement fact holds",
        ))

    TRAILING_CONF_WORDS = (
        "if and howsoever", "if and whensoever",
        "once and howsoever", "once and whensoever",
        "when and howsoever", "when and whensoever",
        "whenever and whensoever",
    )

    TRAILING_CONF = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact holds." % form
        for form in TRAILING_CONF_WORDS)

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather."
        % phrase for phrase in PHRASING_WORDS)

    WEATHER_TRAILING = tuple(
        "The seal guarantees protection %s." % form for form in (
            "in all places where the weather holds",
            "through whatsoever place the weather holds",
            "whatsoever place the weather holds",
            "in whatsoever place the weather holds",
            "at whatsoever time the weather holds",
            "for whatsoever time the weather holds",
            "by whatever place the weather holds",
            "under whatever place the weather holds",
            "whencesoever the weather holds",
            "thencesoever the weather holds",
        )) + tuple(
        "The seal guarantees protection %s the weather holds."
        % form for form in TRAILING_CONF_WORDS)

    def test_phrasings_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PHRASINGS:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_trailing_forms_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.TRAILING_REPG + self.TRAILING_CONF:
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
            mod, "The seal guarantees protection by the statute of "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the "
            "jurisdiction of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the bull of "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection wheresoever the "
            "deployment confinement fact holds."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection at whatever time "
            "the deployment confinement fact holds."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection if and "
            "wheresoever the deployment confinement fact holds."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR31Tests(unittest.TestCase):
    """Ruling 1667: prefixed compound limb."""

    PREFIX_VERIFIED = tuple(
        "The record stands %s-verified." % prefix
        for prefix in ("archaeo", "sym", "dermo"))

    PREFIX_CHECKED = (
        "The record stands dermo-checked.",
    )

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in dict.fromkeys((
            "linden", "pearwood", "applewood", "cherrywood",
            "plumwood", "dogwood", "wengewood",
            "acacia", "balsawood", "cane", "cedarwood",
            "celluloid", "clay", "ebonywood", "felt", "galalith",
            "gutta", "hemlock", "ivorine", "laurel",
            "mahoganywood", "mimosa", "mud", "myrtle", "oakwood",
            "osier", "pinewood", "reed", "rush", "sassafras",
            "straw", "tamarack", "teakwood", "thatch", "tupelo",
            "vulcanite", "walnutwood", "wax", "xylonite",
            "butternut",
        )))

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
            mod, "The record stands ecto-verified."))
        self.assertFalse(_scan(
            mod, "The record stands biblio-verified."))
        self.assertFalse(_scan(
            mod, "Every record stands pecan-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands ebonite-verified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands ashwood-verified before use."))
        self.assertFalse(_scan(
            mod, "The record stands verified."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR31Tests(unittest.TestCase):
    """Ruling 1668: concept root list and un wording limb."""

    WORDINGS = dict.fromkeys((
        "unattended", "unsupervised", "unpatrolled", "unmanned",
        "unstaffed", "unattired",
        "wearresistant", "crushresistant", "pestresistant",
        "alcoholresistant", "axeproof", "dirtresistant",
        "slipresistant", "sweatresistant", "wrinkleresistant",
        "unboarded", "unbricked", "unfloored", "ungrilled",
        "unhedged", "unhoused", "unlatticed", "unnetted",
        "unpaved", "unrailed", "unshingled", "unslatted",
        "unblanketed", "uncanopied", "uncarpeted", "unceiled",
        "unawned",
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
            mod, "The records are unguarded by outside writers."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanAssertedFixR31Tests(unittest.TestCase):
    """Ruling 1669: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in dict.fromkeys((
            "bleeds", "drips", "seeps", "excretes", "secretes",
            "vomits", "rocks", "glistens", "glitters", "sparkles",
            "shimmers", "gleams", "glows", "flickers", "blazes",
            "smoulders", "steams", "smokes", "bubbles", "foams",
            "froths", "boils", "simmers", "percolates",
            "ferments", "putrefies", "rots", "decays",
            "moulders", "crumbles", "withers", "wilts", "droops",
            "sags", "swells", "palpitates", "resonates",
            "burns", "floats", "floods", "flows", "freezes",
            "glides", "itches", "leaks", "melts", "sinks",
            "sizzles", "sleeps", "slides", "slithers", "sparks",
            "splashes", "stings", "stinks", "stoops", "swims",
            "swings", "ticks", "tingles", "trickles", "trips",
            "trudges", "twinkles", "waddles", "wanders", "warms",
            "waves", "wiggles",
        )))

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL_VERBS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal drools integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal crawls integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal salivates integrity for every "
            "reader."))
        self.assertFalse(_scan(
            mod, "The journal sweats integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanMarkerFixR31Tests(unittest.TestCase):
    """Ruling 1670: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKER_WORDS = (
        "till the end of the world", "until the end of the world",
        "through rain and shine", "snow or shine",
        "through calm and storm", "at any hazard", "in any clime",
        "in every clime", "through all climes",
        "till time shall be no more", "while time shall last",
        "as long as time shall last", "to ages of ages",
        "relentlessly", "indefatigably", "night or day",
        "winter or summer", "in winter and in summer",
        "through winter and summer", "in sickness or in health",
        "in life and in death", "through life and death",
        "by land and by sea", "on land and sea",
        "by sea and by land", "in heaven and on earth",
        "on earth and in heaven", "through heaven and earth",
        "to heaven and back", "till the seas run dry",
        "until the seas run dry", "till the rivers run dry",
        "while the rivers run", "so long as the rivers run",
        "till the mountains crumble", "while the mountains stand",
        "as long as the mountains stand", "till the sun burns out",
        "while the sun burns", "as long as the sun burns",
        "till the moon falls", "while the moon shines",
        "as long as the moon shines",
        "in all ages", "in every age", "through every generation",
        "until the last trump",
    )

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker)
        for marker in MARKER_WORDS)

    COMMA_MARKERS = tuple(
        "%s, %s." % (_GOVERNED_CLAIM, marker)
        for marker in MARKER_WORDS + ("forevermore",))

    def test_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MARKERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_comma_clause_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMMA_MARKERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(mod, self.BASE + "."))
        self.assertFalse(_scan(mod, self.BASE + " without fail."))
        self.assertFalse(_scan(mod, self.BASE + " come what may."))
        self.assertFalse(_scan(
            mod, self.BASE + " through all generations."))
        self.assertFalse(_scan(
            mod, self.BASE + " as long as time lasts."))
        self.assertFalse(_scan(
            mod, self.BASE + " for all the ages."))
        self.assertFalse(_scan(
            mod, self.BASE + " till judgment day."))


class SealClaimScanNegationFixR31Tests(unittest.TestCase):
    """Ruling 1671: negation narrowing limb, No opening form."""

    CAN_BE_WORDS = dict.fromkeys((
        "booked", "entered", "wired",
        "bagged", "bottled", "braided", "buckled", "buried",
        "buttoned", "canned", "cemented", "clamped", "clasped",
        "clipped", "corked", "docketed", "encased", "enshrined",
        "entombed", "enveloped", "fenced", "framed", "gilded",
        "hidden", "hooked", "interred", "jarred", "knotted",
        "lacquered", "lashed", "lettered", "microfiched",
        "moated", "moored", "nailed", "outlined", "padlocked",
        "pasted", "pictured", "pinned", "plaited", "plugged",
        "riveted", "screwed", "sewn", "stapled", "stitched",
        "stoppered", "tacked", "tethered", "tinned", "tooled",
        "turreted", "welded", "woven", "wrapped", "zipped",
    ))

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in CAN_BE_WORDS)

    PROBED_IS = tuple(
        "No record is %s after writing." % word for word in (
            "booked", "entered", "wired",
            "clippable", "linkable", "wireable",
        ))

    ASSERTED_ANALOGUES = tuple(
        "Records are %s after writing." % word
        for word in CAN_BE_WORDS) + tuple(
        "The record is %s after writing." % word for word in (
            "clippable", "linkable", "wireable",
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
            mod, "No record is fingerprinted after writing."))
        self.assertFalse(_scan(
            mod, "No record is replicated after writing."))
        self.assertFalse(_scan(
            mod, "No record can be boxed after writing."))
        self.assertFalse(_scan(
            mod, "No record can be vaulted after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanConceptRootsFixR31Tests(unittest.TestCase):
    """Ruling 1672: roots outside the judged concept roots."""

    ROOTS = (
        "couriered", "airmailed", "telegraphed", "telephoned",
        "inventoried", "forked", "queued", "routed", "remitted",
        "assigned", "deeded", "titled",
    )

    PROBED_IS = tuple(
        "No record is %s after writing." % word for word in ROOTS)

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in ROOTS)

    ASSERTED = tuple(
        "Records are %s after writing." % word for word in ROOTS)

    CONF_ROOT_WORDS = (
        "bloggable", "codable", "messageable", "pageable",
        "phonable", "sendable", "tweetable", "watchable",
    )

    CONF_ROOT_ASSERTED = tuple(
        "The record is %s after writing." % word
        for word in CONF_ROOT_WORDS)

    CONF_ROOT_NO = tuple(
        "No record is %s after writing." % word
        for word in CONF_ROOT_WORDS)

    CONF_VERBS = (
        "droned", "ferried", "freighted", "hauled", "jetted",
        "messaged", "paged", "phoned", "taxied", "trucked",
        "wagoned",
    )

    CONF_ASSERTED = tuple(
        "Records are %s after writing." % word
        for word in CONF_VERBS)

    CONF_NO = tuple(
        "No record can be %s after writing." % word
        for word in CONF_VERBS)

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

    def test_asserted_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_conf_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.CONF_ROOT_ASSERTED + self.CONF_ROOT_NO
                + self.CONF_ASSERTED + self.CONF_NO):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_neighbouring_roots_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The record is disclosable after writing."))
        self.assertFalse(_scan(
            mod, "No record is disclosable after writing."))
        self.assertFalse(_scan(
            mod, "The record is mailable after writing."))
        self.assertFalse(_scan(
            mod, "No record is mailable after writing."))
        self.assertFalse(_scan(
            mod, "Records are replicated after writing."))
        self.assertFalse(_scan(
            mod, "No record is syndicatable after writing."))
        self.assertFalse(_scan(
            mod, "The record is textable after writing."))
        self.assertFalse(_scan(
            mod, "Records are banked after writing."))
        self.assertFalse(_scan(
            mod, "No record can be banked after writing."))
        self.assertFalse(_scan(
            mod, "Records are excerpted after writing."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


if __name__ == "__main__":
    unittest.main()
