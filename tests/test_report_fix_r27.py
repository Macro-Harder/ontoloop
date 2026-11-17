"""Fix round 27, Region 1: report seal claim scan pins.

Rulings 1270 to 1276 of the Round 27 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide. Statements stand
built from the probed word and phrase sets of the raising
papers, the Report and golden span paper findings 1 to 7
and the Confinement paper findings 1 to 8 in their absorbed
limbs, on the templates those papers state. A form probed
in both raising papers on the one template stands counted
once, in the form of the triage merges.
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


class SealClaimScanInabilityFixR27Tests(unittest.TestCase):
    """Ruling 1270: inability limb, followers and windows."""

    MODAL_OUTSIDER = tuple(
        "Records cannot be %s by outsiders." % word for word in (
            "fermented", "carbonated", "aerated", "hydrogenated",
            "oxygenated", "chlorinated", "ozonated",
            "crystallized", "sintered", "annealed", "quenched",
            "centrifuged", "decanted", "gelatinized",
            "caramelized", "lyophilized", "dehydrated",
            "rehydrated", "sterilized", "sanitized", "fumigated",
            "perfumed",
        ))

    ASSERTED_OUTSIDER = tuple(
        "Records are %s by outsiders." % word for word in (
            "fermented", "carbonated", "aerated", "hydrogenated",
            "oxygenated", "chlorinated", "ozonated",
            "crystallized", "sintered", "annealed", "quenched",
            "centrifuged", "decanted", "gelatinized",
            "caramelized", "lyophilized", "dehydrated",
            "rehydrated", "sterilized", "sanitized", "fumigated",
            "perfumed",
        ))

    CONF_MODAL = tuple(
        "Records cannot be %s after writing." % word for word in (
            "blistered", "peeled", "flaked", "chipped", "dented",
            "warped", "corroded", "eroded", "tarnished", "pitted",
            "scarred", "frayed", "soaked", "waterlogged",
            "mildewed", "rotted", "decayed", "crumbled",
            "discoloured", "discolored", "faded", "smudged",
            "blotted", "scratched", "gouged", "nicked", "creased",
            "crumpled", "torn", "ripped",
        ))

    WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "joylessly", "mirthlessly", "lightlessly",
            "sunlessly", "breathlessly", "soundlessly",
            "wordlessly", "speechlessly", "desolately",
            "forlornly", "wretchedly", "miserably", "unhappily",
            "dismally", "wanly", "ashenly", "greyly", "grayly",
            "darkly", "dimly", "murkily", "foggily", "mistily",
            "cloudily", "stormily", "rainily", "snowily",
            "windily",
        ))

    CONF_WINDOW_WORDS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in (
            "numbly", "perplexedly", "resentfully", "stunnedly",
            "uneasily", "worriedly", "jealously",
        ))

    CONF_WINDOW_PLACES = tuple(
        "Records cannot in any %s be altered after writing."
        % word for word in (
            "caravanserai", "madrasa", "ziggurat",
        ))

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_OUTSIDER + self.CONF_MODAL:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_OUTSIDER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.WINDOW_WORDS + self.CONF_WINDOW_WORDS
                + self.CONF_WINDOW_PLACES):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be macerated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records cannot be attached after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot be dyed after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot in any scullery be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot solemnly be altered "
            "after writing."))
        self.assertFalse(_scan(
            mod, "Records cannot be vaporized by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot be riveted by outsiders."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanGoverningFixR27Tests(unittest.TestCase):
    """Ruling 1271: governing condition limb."""

    PHRASING_WORDS = (
        "by the superintendence of", "under the superintendence of",
        "by the vice-regency of", "by the deputyship of",
        "by the lieutenancy of", "by the prefecture of",
        "by the diocese of", "by the bishopric of",
        "by the papacy of", "by the caliphate of",
        "by the sultanate of", "by the emirate of",
        "by the shogunate of", "by the viceroyalty of",
        "by the provostship of", "by the chancellery of",
        "by the secretariat of", "by the directorate of",
        "under the commission of",
        "by the aegis of", "by the patronage of",
        "by the rule of", "by the statutes of",
        "under the rule of", "under the statutes of",
    )

    PHRASINGS = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact." % phrase for phrase in PHRASING_WORDS)

    TRAILING_WORDS = (
        "wherever", "whensoever", "when and where",
        "where and when", "as and where", "whenever and wherever",
    )

    TRAILING = tuple(
        "The seal guarantees protection %s the deployment "
        "confinement fact holds." % form for form in TRAILING_WORDS)

    WEATHER_PHRASINGS = tuple(
        "The seal guarantees protection %s the weather."
        % phrase for phrase in PHRASING_WORDS)

    WEATHER_TRAILING = tuple(
        "The seal guarantees protection %s the weather holds."
        % form for form in TRAILING_WORDS)

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
            mod, "The seal guarantees protection by the auspices "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the commission "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the stewardship "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection whenever the "
            "deployment confinement fact holds."))
        self.assertFalse(
            _scan(mod, "The seal guarantees protection."))


class SealClaimScanCompoundFixR27Tests(unittest.TestCase):
    """Ruling 1272: prefixed compound limb."""

    ELEMENTS = tuple(
        "Every record stands %s-verified before use." % element
        for element in (
            "wenge", "zebrawood", "cocobolo", "padauk", "iroko",
            "sapele", "bubinga", "merbau", "purpleheart",
            "bloodwood", "kingwood", "tulipwood", "bocote",
            "ziricote", "ovangkol", "koa", "tamarind", "mango",
            "andesite", "apatite", "arkose", "breccia", "diorite",
            "fluorite", "gabbro", "hornblende", "motherofpearl",
            "mudstone", "orthoclase", "rhyolite", "siltstone",
            "tortoiseshell",
        ))

    PREFIXES = (
        "algo", "aniso", "allo", "apo", "cata", "dys", "eu",
        "agro", "eco",
    )

    PREFIX_VERIFIED = tuple(
        "The record stands %s-verified." % prefix
        for prefix in PREFIXES)

    PREFIX_CHECKED = tuple(
        "The record stands %s-checked." % prefix
        for prefix in PREFIXES)

    SYN_VERIFIED = ("The record stands syn-verified.",)

    def test_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ELEMENTS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_prefixes_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.PREFIX_VERIFIED + self.PREFIX_CHECKED
                + self.SYN_VERIFIED):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "Every record stands basswood-verified "
            "before use."))
        self.assertFalse(_scan(
            mod, "Every record stands mahogany-verified "
            "before use."))
        self.assertFalse(_scan(
            mod, "The record stands ferro-verified."))
        self.assertFalse(_scan(
            mod, "The record stands xeno-verified."))
        self.assertFalse(_scan(
            mod, "The record stands verified."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanLexiconFixR27Tests(unittest.TestCase):
    """Ruling 1273: concept root list and un wording limb."""

    UN_WORDS = (
        "unstrapped", "unlashed", "uncinched", "unsnapped",
        "unveiled", "unshrouded", "unpacked",
    )

    RECORD_UN = tuple(
        "The records are %s by outside writers." % word
        for word in UN_WORDS)

    STORE_UN = tuple(
        "The store is %s." % word for word in UN_WORDS)

    PROOF_WORDS = (
        "godproof", "devilproof", "angelproof", "demonproof",
        "ghostproof", "magicproof", "curseproof", "hexproof",
        "evilproof", "sinproof", "guiltproof", "shameproof",
        "fearproof", "painproof",
    )

    RECORD_PROOF = tuple(
        "The records are %s by outside writers." % word
        for word in PROOF_WORDS)

    STORE_PROOF = tuple(
        "The store is %s." % word for word in PROOF_WORDS)

    RESISTANT_WORDS = (
        "corrosionresistant", "drillresistant", "fireresistant",
        "mothresistant", "pickresistant", "ratresistant",
        "rustresistant", "scratchresistant", "termiteresistant",
        "waterresistant",
    )

    RECORD_RESISTANT = tuple(
        "The records are %s by outside writers." % word
        for word in RESISTANT_WORDS)

    STORE_RESISTANT = tuple(
        "The store is %s." % word for word in RESISTANT_WORDS)

    def test_record_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.RECORD_UN + self.RECORD_PROOF
                + self.RECORD_RESISTANT):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in (
                self.STORE_UN + self.STORE_PROOF
                + self.STORE_RESISTANT):
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are unclamped by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are unriveted by outside writers."))
        self.assertFalse(_scan(
            mod, "The records are bugproof by outside writers."))
        self.assertFalse(_scan(mod, "The store is dustproof."))
        self.assertFalse(_scan(
            mod, "The records are deathproof by outside writers."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


class SealClaimScanAssertedFixR27Tests(unittest.TestCase):
    """Ruling 1274: asserted form limb."""

    JOURNAL_VERBS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in (
            "blushes", "shrugs", "daydreams", "dreamt",
            "improvises", "beatboxes", "caws", "twitches",
            "throbs", "pulsates", "vibrates", "oscillates",
            "gyrates", "pirouettes", "somersaults", "hops",
            "skips", "leaps", "bounds",
            "booms", "crackles", "pops", "resounds",
            "reverberates", "rings", "rustles", "snaps", "thuds",
            "whirs",
        ))

    MECHANISM_VERBS = tuple(
        "The mechanism %s total integrity of the journal."
        % verb for verb in (
            "blushes", "shrugs", "daydreams",
        ))

    CONF_ASSERTED = tuple(
        "Records are %s by outsiders." % word for word in (
            "blistered", "peeled", "flaked", "chipped", "dented",
            "warped", "corroded", "eroded", "tarnished", "pitted",
            "scarred", "frayed", "soaked", "waterlogged",
            "mildewed", "rotted", "decayed", "crumbled",
            "discoloured", "discolored", "faded", "smudged",
            "blotted", "scratched", "gouged", "nicked", "creased",
            "crumpled", "torn", "ripped",
        ))

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.JOURNAL_VERBS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_mechanism_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MECHANISM_VERBS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_conf_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONF_ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal bangs integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal honks integrity for every reader."))
        self.assertFalse(_scan(
            mod, "The journal chirrups integrity for every "
            "reader."))
        self.assertFalse(_scan(
            mod, "The mechanism honks total integrity of the "
            "journal."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))


class SealClaimScanMarkerFixR27Tests(unittest.TestCase):
    """Ruling 1275: unconditional marker limb."""

    BASE = _GOVERNED_CLAIM

    MARKERS = tuple(
        "%s %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "in spite of everything", "despite everything",
            "to kingdom come", "usque ad finem", "in infinitum",
            "sine termino", "sine limite", "neverending",
            "to doomsday",
            "ab aeterno", "aeviternally", "for all generations",
            "from everlasting to everlasting",
            "in all generations", "through eternity",
            "till death", "till the last day",
            "to all generations", "until the last day",
        ))

    COMMA_MARKERS = tuple(
        "%s, %s." % (_GOVERNED_CLAIM, marker) for marker in (
            "without end", "to the end of time", "for all time",
            "in perpetuity", "world without end",
            "throughout eternity", "without limit",
            "without limits", "no matter what", "eternally",
            "perpetually", "endlessly", "ceaselessly",
        ))

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
        self.assertFalse(_scan(mod, self.BASE + " whatever comes."))
        self.assertFalse(_scan(
            mod, self.BASE + " to perpetuity."))
        self.assertFalse(_scan(
            mod, self.BASE + " for all eternity."))


class SealClaimScanNegationFixR27Tests(unittest.TestCase):
    """Ruling 1276: negation narrowing limb, No opening form."""

    PROBED_WORDS = (
        "fingerprinted", "barcoded", "microchipped", "tagged",
        "monitored", "recorded", "videotaped", "audiotaped",
        "preserved", "conserved", "frozen", "encapsulated",
        "embedded", "encoded", "encrypted", "decoded",
        "scrambled", "hashed", "tokenized", "anonymized",
        "masked", "cloaked", "veiled", "shrouded", "insulated",
        "buffered", "backed",
    )

    PROBED_IS = tuple(
        "No record is %s after writing." % word
        for word in PROBED_WORDS)

    PROBED_CAN_BE = tuple(
        "No record can be %s after writing." % word
        for word in PROBED_WORDS)

    CONF_IS = tuple(
        "No record is %s after writing." % word for word in (
            "fingerprintable", "unscannable", "annotatable",
            "broadcastable", "cacheable", "forwardable",
            "scannable", "summarisable", "translatable",
        ))

    CONF_CAN_BE = tuple(
        "No record can be %s after writing." % word for word in (
            "fingerprinted", "annotated", "backed", "beamed",
            "cached", "cited", "displayed", "forwarded",
            "mentioned", "projected", "scanned", "summarised",
            "summarized", "translated",
        ))

    ASSERTED_ANALOGUES = tuple(
        "Records are %s after writing." % word
        for word in PROBED_WORDS) + tuple(
        "The record is %s after writing." % word for word in (
            "fingerprintable", "unscannable", "annotatable",
            "broadcastable", "cacheable", "forwardable",
            "scannable", "summarisable", "translatable",
        )) + tuple(
        "Records are %s after writing." % word for word in (
            "fingerprinted", "annotated", "backed", "beamed",
            "cached", "cited", "displayed", "forwarded",
            "mentioned", "projected", "scanned", "summarised",
            "summarized", "translated",
        ))

    def test_probed_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PROBED_IS + self.PROBED_CAN_BE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_conf_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.CONF_IS + self.CONF_CAN_BE:
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
            mod, "No record is anchored after writing."))
        self.assertFalse(_scan(
            mod, "No record is watermarked after writing."))
        self.assertFalse(_scan(
            mod, "No record is tracked after writing."))
        self.assertFalse(_scan(
            mod, "No record is traced after writing."))
        self.assertFalse(_scan(
            mod, "No record is duplicated after writing."))
        self.assertFalse(_scan(
            mod, "No record can be tracked after writing."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))


if __name__ == "__main__":
    unittest.main()
