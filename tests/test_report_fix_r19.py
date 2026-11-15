"""Fix round 19, Region 1: report and golden pins.

Rulings 716 to 720 of the Round 19 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers on the templates those papers state.
"""

import unittest

from tests import harness


def _scan(mod, statement):
    return mod._seal_claim_scan(statement)


def _travel(mod, statement):
    result = mod.fixed_text_travel_lint(
        assembly="export", content=statement)
    return result["passed"]


def _cannot_be(words, tail):
    return tuple(
        "Records cannot be %s %s" % (word, tail) for word in words)


def _are_by(words):
    return tuple(
        "Records are %s by outsiders." % word for word in words)


def _cannot_window(phrases, tail):
    return tuple(
        "Records cannot %s be altered %s" % (phrase, tail)
        for phrase in phrases)


def _cannot_word(words, tail):
    return tuple(
        "Records cannot %s be altered %s" % (word, tail)
        for word in words)


class SealClaimScanInabilityFixR19Tests(unittest.TestCase):
    """Ruling 716: inability limb, followers and windows."""

    MODAL_OUTSIDERS = _cannot_be((
        "recollected", "remembered",
        "arrested", "conceived", "confiscated", "detained",
        "devised", "impounded", "interrogated", "plotted",
        "pursued", "questioned", "reworded", "transformed",
        "summonsed", "summoned", "subpoenaed", "charged",
        "accused", "indicted", "prosecuted", "tried",
        "sentenced", "fined", "punished", "disciplined",
        "sanctioned", "blacklisted", "barred", "banned",
        "excluded", "expelled", "evicted", "dismissed",
        "discharged", "suspended", "revoked", "cancelled",
        "terminated", "invented", "imagined", "dreamed",
        "hallucinated", "envisioned", "visualised",
        "visualized", "pictured", "outlined", "blueprinted",
    ), "by outsiders.")

    MODAL_WRITING = _cannot_be((
        "attested", "vouched", "guaranteed", "warranted",
        "sworn", "mimeographed", "microfilmed", "laminated",
        "imaged",
    ), "after writing.")

    ASSERTED = _are_by((
        "fathomed", "recalled", "remembered", "recollected",
        "vouched", "guaranteed", "warranted", "mimeographed",
        "laminated", "imaged", "licked",
    ))

    WINDOWS_WRITING = _cannot_window((
        "in any sea", "at any birthday", "at any anniversary",
        "at any wedding", "at any funeral", "at any graduation",
        "at any ceremony", "at any celebration", "at any meeting",
        "at any conference", "at any election", "at any contest",
        "at any game", "at any match", "at any race",
        "at any concert", "on any ground",
        "in any menagerie", "in any casino", "in any bazaar",
        "in any bathhouse", "in any sauna", "on any solstice",
        "on any equinox",
    ), "after writing.")

    WINDOWS_PLAIN = _cannot_window((
        "in any bastion", "in any casino", "in any corridor",
        "in any dam", "in any kiln", "in any lobby",
        "in any salon", "in any sawmill", "in any stairwell",
        "in any menagerie", "in any vivarium", "in any terrarium",
        "in any solarium", "in any sanctuary",
        "in any chapterhouse", "in any scriptorium",
        "in any boathouse", "in any pumphouse", "in any gatehouse",
        "in any powerhouse", "in any storehouse", "in any treasury",
        "in any arsenal", "in any depository",
        "at any conductivity", "at any current", "at any enthalpy",
        "at any entropy", "at any flammability", "at any hardness",
        "at any impedance", "at any molarity", "at any opacity",
        "at any permeability", "at any radioactivity",
        "at any reactance", "at any reflectivity",
        "at any roughness", "at any solubility", "at any toxicity",
        "at any susceptance", "at any admittance",
        "at any reluctance", "at any permittivity",
        "at any resistivity", "at any malleability",
        "at any ductility", "at any brittleness",
        "at any toughness", "at any stiffness", "at any damping",
        "at any inertia", "at any nightfall", "at any daybreak",
        "under any name", "on any date",
    ), ".")

    WINDOW_WORDS_WRITING = _cannot_word((
        "gently", "violently", "overtly", "suddenly", "willingly",
        "deceptively", "mistakenly", "erroneously", "boldly",
        "bravely", "proudly", "honestly", "truthfully",
        "faithfully", "cruelly", "kindly", "ruthlessly",
        "relentlessly", "frequently", "occasionally", "rarely",
        "often", "usually", "especially", "mainly", "initially",
        "previously", "separately", "jointly", "individually",
        "personally", "rightly", "justly", "fairly", "correctly",
        "accurately", "precisely", "exactly", "genuinely",
        "sincerely",
        "brazenly", "flagrantly", "shamelessly", "blatantly",
    ), "after writing.")

    WINDOW_WORDS_PLAIN = _cannot_word((
        "immorally", "sneakily", "unethically", "unscrupulously",
        "vindictively", "wantonly",
    ), ".")

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_OUTSIDERS + self.MODAL_WRITING:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            self.WINDOWS_WRITING + self.WINDOWS_PLAIN
            + self.WINDOW_WORDS_WRITING + self.WINDOW_WORDS_PLAIN
        ):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be known by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot be beheld by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot in any conservatory be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot stealthily be altered "
            "after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanGoverningFixR19Tests(unittest.TestCase):
    """Ruling 717: governing condition limb."""

    PHRASES = (
        "through the agency of", "by direction from",
        "in acknowledgement of", "in acknowledgment of",
        "under the framework of", "with the consent of",
        "by consent of", "at the request of", "by request of",
        "on the request of", "by the behest of",
        "on the behest of", "at the urging of",
        "under the command of", "by command of",
        "under the management of", "under the leadership of",
        "under the conditions of", "on the conditions of",
        "by the conditions of", "under the rules of",
        "by the rules of", "under the laws of", "by the laws of",
        "with authority from", "by authority from",
        "under authority from", "on instruction from",
        "by instruction from", "under instruction from",
        "with permission from", "by permission from",
        "on permission from", "according to", "as sanctioned by",
        "as endorsed by", "as demanded by", "as requested by",
        "on the advice given by", "at the instruction given by",
        "under the authority given by",
        "by the authority given by",
        "in conjunction with", "in concert with", "in tandem with",
        "on the say-so of", "at the instance of",
        "by the grace of", "at the sufferance of",
        "on the initiative of", "under the patronage of",
        "at the prompting of", "in league with",
        "under the sway of", "under the influence of",
        "at the bidding of", "on the bidding of",
        "under command of", "with the blessing of",
        "by the blessing of", "with endorsement of",
        "by endorsement of", "with consent of",
        "with agreement of", "by agreement of",
        "with concurrence of", "in concurrence with",
        "on the instance of", "upon the instruction of",
        "in honour of", "in honor of", "in memory of",
        "in celebration of", "in defiance of", "in spite of",
    )

    GOVERNED = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in PHRASES
    ) + (
        "The seal guarantees protection on the footing that "
        "the deployment confinement fact holds.",
    )

    WEATHER = tuple(
        statement.replace(
            "the deployment confinement fact holds.",
            "the weather holds.").replace(
            "the deployment confinement fact.",
            "the weather holds.")
        for statement in GOVERNED
    )

    def test_governed_phrasings_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_in_same_phrasings_fails(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection with the "
            "authority of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection at the behest of "
            "the deployment confinement fact."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanPrefixedFixR19Tests(unittest.TestCase):
    """Ruling 718: prefixed compound limb."""

    CONF_VERIFIED = tuple(
        "The record stands %s-verified." % prefix for prefix in (
            "lidar", "nfc", "rfid", "gps", "wifi", "bluetooth",
            "scent", "odor", "gaze", "stride", "gesture", "blink",
            "pupil", "waveform", "echo",
        ))

    CONF_CHECKED = tuple(
        "The record stands %s-checked." % prefix for prefix in (
            "lidar", "scent", "gaze",
        ))

    REPORT_VERIFIED = tuple(
        "Every record stands %s-verified before use." % prefix
        for prefix in (
            "rna", "sms", "passport", "licence", "license", "user",
            "identity", "age", "voiceprint", "keycard", "smartcard",
            "sim", "gps", "time", "date", "place", "event",
            "twofactor", "multifactor", "camera", "microphone",
            "keyboard", "diamond", "gold", "iron", "steel", "wood",
            "stone", "glass", "lens", "crystal",
        ))

    REPORT_CHECKED = tuple(
        "Every record stands %s-checked before use." % prefix
        for prefix in (
            "rna", "sms", "passport", "licence", "license", "user",
            "identity", "age", "voiceprint", "keycard", "smartcard",
            "sim", "gps", "time", "date",
        ))

    LEAD_BOTH = tuple(
        "Every record stands %s-%s before use." % (prefix, root)
        for prefix in (
            "ankle", "cheek", "elbow", "electron", "forehead",
            "gamma", "heel", "hydraulic", "jaw", "keypad",
            "knuckle", "lip", "mechanical", "mri", "neck",
            "neutron", "nostril", "photon", "pneumatic", "pupil",
            "robotic", "scent", "shoulder", "smartcard", "toe",
            "ultrasound", "ultraviolet", "voiceprint", "wrist",
            "xray",
        )
        for root in ("checked", "verified")
    )

    def test_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            self.CONF_VERIFIED + self.CONF_CHECKED
            + self.REPORT_VERIFIED + self.REPORT_CHECKED
            + self.LEAD_BOTH
        ):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Every record stands data-checked "
            "before use."))
        self.assertFalse(
            _scan(mod, "Every record stands facial-verified "
            "before use."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR19Tests(unittest.TestCase):
    """Ruling 719: lexicon limb."""

    RECORDS = tuple(
        "The records are %s by outside writers." % wording
        for wording in (
            "adultproof", "workerproof", "employeeproof",
            "managerproof", "clientproof", "customerproof",
            "userproof", "visitorproof", "guestproof",
            "strangerproof", "intruderproof", "attackerproof",
            "enemyproof", "policeproof", "lawyerproof",
            "judgeproof", "governmentproof", "climateproof",
            "seasonproof", "timeproof", "ageproof", "lifeproof",
            "droughtproof", "monsoonproof", "cycloneproof",
            "typhoonproof", "volcanoproof", "thunderproof",
            "waveproof", "tideproof", "currentproof",
            "stressproof", "strainproof", "noiseproof",
            "smellproof", "tasteproof", "feelproof",
            "unvaried", "unmoved", "unweakened", "unpenetrated",
            "unaccessed",
            "antproof", "flyproof", "beetleproof", "spiderproof",
            "snakeproof", "birdproof", "squirrelproof",
            "deerproof", "rabbitproof", "biteproof", "pestproof",
            "termiteproof", "mosquitoproof", "odorproof",
            "steamproof", "splashproof", "sprayproof",
            "foamproof", "powderproof", "granuleproof",
            "unripped", "undented", "uninfected", "unrevised",
            "unamended", "unadjusted", "unadulterated", "unmixed",
            "unalloyed", "undiluted", "unsoftened", "unloosened",
            "unfastened", "unlatched", "unbolted", "unguarded",
            "unshielded", "unprotected", "undefended",
            "unnoticed", "undetected", "undiscovered",
            "unreported", "unrecorded", "unlogged", "unfiled",
            "unstored", "unsaved", "unbacked",
        ))

    STORE = tuple(
        "The store is %s." % wording for wording in (
            "antproof", "waspproof", "beeproof", "mosquitoproof",
            "termiteproof", "spiderproof", "snakeproof",
            "bearproof", "monsoonproof", "typhoonproof",
            "cycloneproof", "droughtproof", "wildfireproof",
            "aluminumproof", "aluminiumproof", "marbleproof",
            "obsidianproof", "pigeonproof",
        ))

    def test_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS + self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)
        self.assertFalse(_scan(mod, "The store is infrangible."))
        self.assertFalse(_travel(mod, "The store is infrangible."))

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are fireproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are tsunamiproof by outside "
            "writers."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanAssertedFixR19Tests(unittest.TestCase):
    """Ruling 720: asserted form limb."""

    JOURNAL = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "consecrates", "sanctifies", "blesses", "pushes",
            "ballyhoos", "cries", "shouts", "voices", "says",
            "tells", "remarks", "mentions", "cites", "quotes",
            "references", "lists", "names", "identifies",
            "hails", "salutes", "commemorates", "immortalizes",
            "immortalises", "memorializes", "memorialises",
            "hypes", "crowns", "alleges", "insinuates",
            "intimates", "rhapsodizes", "garlands", "fetes",
            "adores", "commends", "conjectures", "decrees",
            "deduces", "delineates", "dictates", "enacts",
            "esteems", "founds", "infers", "mandates", "ordains",
            "outlines", "prescribes", "presumes", "recapitulates",
            "repeats", "sketches", "speculates", "summarises",
            "summarizes", "supposes", "surmises", "undertakes",
            "venerates", "ventures",
        )
    ) + (
        "The journal points out integrity for every reader.",
        "The journal draws attention to integrity for every "
        "reader.",
        "The journal calls attention to integrity for every "
        "reader.",
        "The journal focuses on integrity for every reader.",
        "The journal centres on integrity for every reader.",
        "The journal centers on integrity for every reader.",
    )

    MECHANISM = tuple(
        "The mechanism %s total integrity of the journal." % verb
        for verb in (
            "consecrates", "sanctifies", "blesses", "pushes",
            "ballyhoos", "cries", "shouts", "voices", "says",
            "tells", "remarks", "mentions",
            "adores", "ballyhoos", "commends", "conjectures",
            "decrees", "deduces", "delineates", "dictates",
            "enacts", "esteems", "founds", "infers", "mandates",
            "ordains", "outlines", "prescribes", "presumes",
            "recapitulates", "repeats", "sketches", "speculates",
            "summarises", "summarizes", "supposes", "surmises",
            "undertakes", "venerates", "ventures",
        )
    )

    def test_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL + self.MECHANISM:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal advocates integrity for every "
            "reader."))
        self.assertFalse(_scan(
            mod, "The journal sings integrity for every reader."))
        self.assertTrue(
            _scan(mod, "Integrity label for the journal schedule."))
        self.assertTrue(_travel(
            mod, "Integrity label for the journal schedule."))


class StandingAssembliesFixR19Tests(unittest.TestCase):
    """The standing assemblies and the anchor route inputs."""

    def test_construction_lints_pass(self):
        mod = harness.require("ontoloop.report")
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


if __name__ == "__main__":
    unittest.main()
