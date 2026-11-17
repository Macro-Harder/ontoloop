"""Fix round 22, Region 1: report seal claim scan pins.

Rulings 899 to 904 of the Round 22 triage. Each class pins
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


class SealClaimScanInabilityFixR22Tests(unittest.TestCase):
    """Ruling 899: inability limb, followers and windows."""

    MODAL_OUTSIDERS = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "misfiled", "dissolved", "vaporized", "pulverized",
            "auctioned", "pawned", "leased", "borrowed", "rifled",
            "torched", "flooded", "swapped", "melted", "crushed",
            "smashed", "mangled", "fractured", "splintered",
            "punctured", "perforated", "severed", "contaminated",
        ))

    MODAL_WRITING = tuple(
        "Records cannot be %s after writing." % word for word in (
            "welded", "cemented", "encased", "enshrined", "frozen",
            "vaulted", "entombed", "interred", "guarded",
            "armoured", "armored", "fortified", "fenced",
            "walled", "moated", "turreted",
        ))

    ASSERTED = (
        "Records are rifled by outsiders.",
        "Records are auctioned by outsiders.",
        "Records are pawned by outsiders.",
    )

    WINDOW_PLACES = tuple(
        "Records cannot in any %s be altered after writing."
        % word for word in (
            "sanctum", "armory", "oubliette", "garret", "turret",
            "dovecote", "bindery",
            "stupa", "guildhall", "townhall", "jailhouse",
            "penitentiary", "reformatory", "smithy", "stable",
            "kennel",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "frankly", "coolly", "blandly", "blithely", "breezily",
            "lightly", "plainly", "bluntly", "tartly", "dryly",
            "wryly", "mildly", "meekly", "humbly", "softly",
            "surely", "duly", "keenly", "warmly", "stiffly",
            "primly", "demurely", "sedately", "staidly", "soberly",
            "gravely", "sternly", "grimly", "dourly", "bleakly",
            "patiently",
            "reluctantly", "hesitantly", "confidently",
            "foolishly", "clumsily", "gracefully", "awkwardly",
            "furiously", "desperately", "impatiently",
            "hopelessly",
        ))

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
        for statement in self.WINDOW_PLACES + self.WINDOW_WORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be fingerprinted "
                  "by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot in any pantry be altered "
            "after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanGoverningFixR22Tests(unittest.TestCase):
    """Ruling 900: governing condition limb."""

    GOVERNED = tuple(
        "The seal guarantees protection %s." % phrase
        for phrase in (
            "in the event the deployment confinement fact holds",
            "in the case the deployment confinement fact holds",
            "in the circumstance that the deployment "
            "confinement fact holds",
            "in the situation that the deployment "
            "confinement fact holds",
            "on the occasion that the deployment "
            "confinement fact holds",
            "in the instance that the deployment "
            "confinement fact holds",
            "side by side with the deployment confinement fact",
            "hand in hand with the deployment confinement fact",
            "paired with the deployment confinement fact",
            "coupled with the deployment confinement fact",
            "in vassalage to the deployment confinement fact",
            "in fealty to the deployment confinement fact",
            "in the grasp of the deployment confinement fact",
            "through the instrumentality of the deployment "
            "confinement fact",
            "on the instructions of the deployment "
            "confinement fact",
            "on the guidance of the deployment confinement fact",
            "on the prompting of the deployment confinement fact",
            "on the urging of the deployment confinement fact",
            "on the insistence of the deployment "
            "confinement fact",
            "at the insistence of the deployment "
            "confinement fact",
            "on the demand of the deployment confinement fact",
            "at the demand of the deployment confinement fact",
            "on the invitation of the deployment "
            "confinement fact",
            "on the suggestion of the deployment "
            "confinement fact",
            "by the decision of the deployment confinement fact",
            "on the decision of the deployment confinement fact",
            "by the ruling of the deployment confinement fact",
            "on the ruling of the deployment confinement fact",
            "by the judgment of the deployment confinement fact",
            "by the verdict of the deployment confinement fact",
            "by the warrant of the deployment confinement fact",
            "under the warrant of the deployment "
            "confinement fact",
            "by the licence of the deployment confinement fact",
            "by the license of the deployment confinement fact",
            "accountable to the deployment confinement fact",
            "deferring to the deployment confinement fact",
            "owing obedience to the deployment confinement fact",
            "under the wing of the deployment confinement fact",
            "under the protection of the deployment "
            "confinement fact",
            "in service to the deployment confinement fact",
            "in support of the deployment confinement fact",
            "on the application of the deployment "
            "confinement fact",
            "at the suit of the deployment confinement fact",
        ))

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
            mod, "The seal guarantees protection in subordination "
            "to the deployment confinement fact."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanPrefixedFixR22Tests(unittest.TestCase):
    """Ruling 901: prefixed compound limb."""

    COMPOUNDS = tuple(
        "Every record stands %s-verified before use." % word
        for word in (
            "porcelain", "slate", "limestone", "sandstone",
            "flint", "brass", "pewter", "zinc", "nickel",
            "chrome", "ruby", "sapphire", "emerald", "pearl",
            "coral", "amber", "linen", "cotton", "wool",
            "denim", "canvas", "cardboard", "cork",
        )) + (
        "Every record stands porcelain-checked before use.",
    ) + tuple(
        "The record stands %s-%s." % (prefix, root)
        for prefix in (
            "optic", "xeno", "cryo", "pyro", "hydro", "aero",
            "astro", "cosmo", "helio", "geo", "bio", "zoo",
            "neuro", "cardio", "dermato", "spectro", "chromo",
            "electro", "magneto", "sono", "palaeo", "paleo",
            "thermo", "opto", "electro-optic",
        )
        for root in ("verified", "checked")
    ) + (
        "The record stands archi-checked.",
    ) + tuple(
        "Every record stands %s-%s before use." % (element, root)
        for element in (
            "footprint", "irisprint", "veinprint", "gaitprint",
            "keystrokeprint", "scrollprint", "handprint",
            "headprint", "scentprint", "breathprint",
            "pulseprint", "brainwaveprint", "heartbeatprint",
            "skinprint", "nailprint", "hairprint", "toothprint",
            "boneprint",
        )
        for root in ("checked", "verified")
    )

    def test_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMPOUNDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Every record stands obsidian-verified "
                  "before use."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR22Tests(unittest.TestCase):
    """Ruling 902: lexicon limb."""

    RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in (
            "alkaliproof", "sparkproof", "arrowproof",
            "spearproof", "clubproof", "fileproof",
            "crowbarproof",
            "unstitched", "unwrapped", "unmounted", "unframed",
            "unglazed", "unvarnished", "unpolished", "unpainted",
            "unlined", "unpadded",
            "unsecured", "unapproved", "unlicensed",
            "uncorroborated", "unformatted", "unclassified",
        ))

    STORE = tuple(
        "The store is %s." % word for word in (
            "hornetproof", "centipedeproof", "millipedeproof",
            "earwigproof", "silverfishproof", "alkaliproof",
            "inkproof", "bloodproof", "gritproof", "lintproof",
            "staticproof", "liceproof", "dustmiteproof",
            "thripsproof", "scaleproof", "mealybugproof",
            "whiteflyproof", "cutwormproof", "armywormproof",
            "hornwormproof", "stinkbugproof", "agateproof",
            "jasperproof", "onyxproof", "topazproof",
            "garnetproof", "berylproof", "spinelproof",
            "zirconproof", "peridotproof", "tourmalineproof",
            "satinproof", "tweedproof", "twillproof",
            "flannelproof", "jerseyproof", "chiffonproof",
            "organzaproof", "tulleproof", "feltproof",
            "suedeproof", "nubuckproof", "corduroyproof",
            "seersuckerproof", "cambricproof", "muslinproof",
            "gauzeproof", "burlapproof", "juteproof",
            "sisalproof", "coirproof", "raffiaproof",
            "keyloggerproof", "infostealerproof", "exploitproof",
            "zerodayproof", "backdoorproof", "surgeproof",
            "fogproof", "mistproof", "dewproof", "humidityproof",
            "moistureproof", "dampproof",
        ))

    def test_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS + self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are droneproof by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are unfiled by outside writers."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanAssertedFixR22Tests(unittest.TestCase):
    """Ruling 903: asserted form limb."""

    JOURNAL = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "mumbles", "chatters", "babbles", "editorializes",
            "moralizes", "articulates", "enunciates", "vocalizes",
            "drawls", "lisps", "stammers",
            "trills", "chirps", "croaks", "coos", "purrs",
            "hisses", "tweets", "cheeps", "peeps", "clucks",
            "cackles", "gobbles", "quacks", "honks", "squawks",
            "screeches", "hoots", "barks", "yelps", "whines",
            "growls", "snarls", "meows", "miaows", "moos",
            "baas", "bleats", "neighs", "whinnies", "brays",
            "snorts", "grunts", "squeals", "squeaks", "chitters",
            "clicks", "buzzes", "drones", "sighs", "gasps",
            "sobs", "wails", "moans", "groans", "stutters",
            "lilts",
        ))

    MECHANISM = tuple(
        "The mechanism %s total integrity of the journal."
        % verb for verb in (
            "mumbles", "vocalizes",
            "requires", "demands", "governs", "regulates",
            "oversees", "supervises", "manages", "administers",
            "handles", "operates", "runs", "guides",
        ))

    ASSERTED_FOLLOWERS = tuple(
        "Records are %s by outsiders." % word for word in (
            "welded", "cemented", "encased", "enshrined",
            "vaulted", "entombed", "interred", "buried",
            "hidden", "fenced", "moated", "turreted",
        ))

    def test_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL + self.MECHANISM:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_FOLLOWERS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal yells integrity for every reader."))
        self.assertFalse(_scan(
            mod, "Records are collated by outsiders."))
        self.assertTrue(
            _scan(mod, "Integrity label for the journal schedule."))
        self.assertTrue(_travel(
            mod, "Integrity label for the journal schedule."))


class SealClaimScanUnconditionalFixR22Tests(unittest.TestCase):
    """Ruling 904: unconditional marker limb."""

    MARKED = tuple(
        "The seal guarantees protection conditional on "
        "the deployment confinement fact %s." % marker
        for marker in (
            "whatever happens", "rain or shine",
            "through thick and thin", "to the end of time",
            "for eternity", "once and for all", "beyond question",
            "for good", "in any case", "at any cost",
            "come hell or high water", "by any means",
            "in every way", "for all eternity",
            "till the end of time", "until the end of time",
            "without end", "categorically", "beyond doubt",
            "at every moment", "on every occasion", "evermore",
            "world without end", "henceforth and forever",
            "now and forever", "under any circumstances",
            "everlastingly", "now and always",
        ))

    def test_marked_claims_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MARKED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        self.assertFalse(_scan(
            mod, "The seal guarantees protection conditional on "
            "the deployment confinement fact for all time."))


class StandingAssembliesFixR22Tests(unittest.TestCase):
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
