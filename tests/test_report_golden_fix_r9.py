"""Fix round 9, Region 1: report and golden pins.

Rulings 248 to 255 of the Round 9 triage. Each class pins
the probed forms of its ruling beside the standing forms
that must keep deciding as they decide.
"""

import unittest
from collections import UserDict
from types import MappingProxyType

from tests import harness


def _scan(mod, statement):
    return mod._seal_claim_scan(statement)


def _travel(mod, statement):
    result = mod.fixed_text_travel_lint(
        assembly="export", content=statement)
    return result["passed"]


class SealClaimScanJuxtaposedSubjectsFixR9Tests(unittest.TestCase):
    """Ruling 248, first limb: juxtaposed negated clauses."""

    FORMS = (
        "The seal guarantees protection expiry never occurs.",
        "The seal guarantees protection records never expire.",
        "The seal guarantees protection it never expires.",
        "The seal guarantees protection the long schedule never expires.",
        "The seal guarantees protection the long schedule cannot expire.",
        "The seal guarantees protection the long schedule is not expired.",
        "The seal guarantees protection the long schedule has not expired.",
        "The seal guarantees protection the old record never expires.",
        "The seal guarantees protection the sealed records never expire.",
        "The seal guarantees protection sealed records never expire.",
        "The seal guarantees protection 100 records never expire.",
        "The seal guarantees protection 100 records cannot expire.",
        "The seal guarantees protection all 100 records never expire.",
        "The seal guarantees protection one hundred records never expire.",
        "The seal guarantees protection every record never expires.",
        "The seal guarantees protection each record never expires.",
        "The seal guarantees protection the schedule need not expire.",
        "The seal guarantees protection the schedule had never expired.",
        "The seal guarantees protection schedules had not expired.",
        "The seal guarantees protection the backup need not stand sealed.",
    )

    def test_juxtaposed_subject_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_charged_and_genuine_forms_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "The seal guarantees protection the schedule never expires.",
            "The seal guarantees protection the schedule cannot expire.",
            "The seal guarantees protection the schedule does not expire.",
            "The seal guarantees protection the record never expires.",
            "The seal guarantees protection the schedule could not expire.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        for statement in (
            "The seal guarantees protection conditional on "
            "the deployment confinement fact.",
            "The seal guarantees protection conditional on "
            "signed strength.",
            "The seal does not guarantee protection.",
        ):
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])
        travel = mod.fixed_text_travel_lint(assembly="export")
        self.assertTrue(travel["passed"])


class SealClaimScanIntroducersFixR9Tests(unittest.TestCase):
    """Ruling 248, second limb: further introducer forms."""

    SINGLE_WORD = (
        "noticing", "perceiving", "discovering", "overlooking",
        "disregarding", "declaring", "stating", "asserting",
        "via", "through", "without", "whereupon", "inasmuch",
        "touching", "respecting", "mentioning", "relating",
        "pertaining", "involving", "allowing", "requiring",
        "having", "expecting", "hoping",
    )

    PHRASES = (
        "The seal guarantees protection in spite of expiry never occurs.",
        "The seal guarantees protection apart from expiry never occurs.",
        "The seal guarantees protection due to expiry never occurs.",
        "The seal guarantees protection instead of expiry never occurs.",
        "The seal guarantees protection rather than expiry never occurs.",
        "The seal guarantees protection touching a backup not under seal.",
        "The seal guarantees protection respecting a backup not under seal.",
        "The seal guarantees protection overlooking a backup not under seal.",
        "The seal guarantees protection mentioning a backup not under seal.",
    )

    def test_single_word_introducer_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for word in self.SINGLE_WORD:
            statement = (
                "The seal guarantees protection %s expiry never occurs."
                % word)
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_phrase_introducer_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PHRASES:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_charged_introducer_forms_still_fail(self):
        mod = harness.require("ontoloop.report")
        for word in ("regarding", "concerning", "noting", "observing",
                     "upon", "using", "believing"):
            statement = (
                "The seal guarantees protection %s expiry never occurs."
                % word)
            self.assertFalse(_scan(mod, statement), statement)


class SealClaimScanSeparatorsFixR9Tests(unittest.TestCase):
    """Ruling 248, third limb: separators and conjunctive adverbs."""

    SEPARATORS = (
        "<", "`", "$", "_", "'", '"', "•", "·",
        "§", "…", "€", "«", "»",
    )

    ADVERBS = (
        "consequently", "accordingly", "hence", "thus",
        "subsequently", "afterwards", "instead", "otherwise",
        "likewise", "similarly", "finally", "then", "besides",
        "simultaneously",
    )

    def test_separator_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for sign in self.SEPARATORS:
            statement = (
                "The seal guarantees protection %s expiry never occurs."
                % sign)
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_adverb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for word in self.ADVERBS:
            statement = (
                "The seal guarantees protection %s expiry never occurs."
                % word)
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_charged_separators_and_adverbs_still_fail(self):
        mod = harness.require("ontoloop.report")
        for sign in (",", "*", "^", "~", "|", "&", "/", "\\"):
            statement = (
                "The seal guarantees protection %s expiry never occurs."
                % sign)
            self.assertFalse(_scan(mod, statement), statement)
        for word in ("however", "moreover", "therefore",
                     "meanwhile", "furthermore"):
            statement = (
                "The seal guarantees protection %s expiry never occurs."
                % word)
            self.assertFalse(_scan(mod, statement), statement)


class SealClaimScanInabilityFixR9Tests(unittest.TestCase):
    """Ruling 249: the inability limb."""

    MODAL_AND_WINDOW_FORMS = (
        "Records dare never be altered after writing.",
        "Records need never be altered after writing.",
        "Records need not be altered after writing.",
        "Records cannot in any manner be altered after writing.",
        "Records cannot in any fashion be altered after writing.",
        "Records cannot by any method be altered after writing.",
        "Records cannot under any guise be altered after writing.",
        "Records cannot at any point be altered after writing.",
        "Records cannot for any purpose be altered after writing.",
        "Records cannot absolutely be altered.",
        "Records cannot by any conceivable means at any time under "
        "any circumstance in any way be altered.",
    )

    FOLLOWER_FORMS = (
        "Records cannot be photographed by outsiders.",
        "Records cannot be transcribed by outsiders.",
        "Records cannot be duplicated by outsiders.",
        "Records cannot be downloaded by outsiders.",
        "Records cannot be printed by outsiders.",
        "Records cannot be forwarded by outsiders.",
        "Records cannot be shared by outsiders.",
        "Records cannot be duplicated after writing.",
        "Records cannot be intercepted after writing.",
        "Records cannot be transmitted after writing.",
        "Records cannot be moved after writing.",
        "Records cannot be renamed after writing.",
        "Records cannot be spoofed after writing.",
        "Records cannot be replayed after writing.",
        "Records cannot be sniffed after writing.",
        "Heads cannot be duplicated by any outsider.",
        "Heads cannot be replicated by any outsider.",
        "Heads cannot be extracted by any outsider.",
        "Heads cannot be intercepted by any outsider.",
        "Records cannot be replayed by any outsider.",
    )

    ASSERTED_FOLLOWER_FORMS = (
        "Records are duplicated after writing.",
        "Records are intercepted after writing.",
        "Records are forwarded by outsiders.",
        "Records are shared by outsiders.",
        "Records are printed by outsiders.",
        "Records are photographed by outsiders.",
    )

    def test_modal_and_window_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL_AND_WINDOW_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_follower_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FOLLOWER_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_follower_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED_FOLLOWER_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_charged_forms_and_negated_claims_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "Records cannot by any means be altered after writing.",
            "Records cannot be altered after writing.",
            "Records cannot simply be altered.",
            "Store files cannot be read by outsiders.",
        ):
            self.assertFalse(_scan(mod, statement), statement)
        self.assertTrue(_scan(mod, "The seal does not guarantee protection."))


class SealClaimScanGoverningPhrasingsFixR9Tests(unittest.TestCase):
    """Ruling 250: governing condition phrasings."""

    GOVERNED = (
        "The seal guarantees protection depending on "
        "the deployment confinement fact.",
        "The seal guarantees protection contingent on "
        "the deployment confinement fact.",
        "The seal guarantees protection conditional upon "
        "the deployment confinement fact.",
        "The seal guarantees protection provided "
        "the deployment confinement fact holds.",
        "The seal guarantees protection provided the signed strength stands.",
        "The seal guarantees protection given "
        "the deployment confinement fact.",
        "The seal guarantees protection given the signed strength.",
        "The seal guarantees protection only at signed strength.",
    )

    WEATHER = (
        "The seal guarantees protection depending on the weather.",
        "The seal guarantees protection contingent on the weather.",
        "The seal guarantees protection conditional upon the weather.",
        "The seal guarantees protection provided the weather holds.",
        "The seal guarantees protection given the weather.",
    )

    def test_governed_phrasings_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_phrasings_still_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_standing_governed_forms_still_pass(self):
        mod = harness.require("ontoloop.report")
        for statement in (
            "The seal guarantees protection conditional on "
            "the deployment confinement fact.",
            "The seal guarantees protection subject to "
            "the deployment confinement fact.",
            "The seal guarantees protection at signed strength only.",
            "The seal guarantees protection only if "
            "the deployment confinement fact holds.",
        ):
            self.assertTrue(_scan(mod, statement), statement)


class SealClaimScanPrefixedCompoundsFixR9Tests(unittest.TestCase):
    """Ruling 251: the prefixed compound limb."""

    COMPOUNDS = (
        "Every record stands tri-checked before use.",
        "Every record stands dual-checked before use.",
        "Every record stands twice-checked before use.",
        "Every record stands well-checked before use.",
        "Every record stands fully-verified before use.",
        "The record stands x-verified.",
        "The record stands super-verified.",
        "The record stands anti-verified.",
        "The record stands extra-verified.",
        "The record stands trans-verified.",
        "The record stands intra-checked.",
        "The record stands neo-verified.",
        "The record stands omni-verified.",
        "The record stands poly-verified.",
    )

    def test_prefixed_compounds_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMPOUNDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_charged_compounds_still_fail_and_governed_pass(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Every record stands inter-checked before use."))
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))


class SealClaimScanLexiconFixR9Tests(unittest.TestCase):
    """Ruling 252: the lexicon limb."""

    WORDINGS = (
        "The journal is fireproof.",
        "Records stand faultless after writing.",
        "Records stand flawless after writing.",
        "Records stand frozen after writing.",
        "The store stands guarded against outside writers.",
        "Records stand deathless after writing.",
        "Records stand timeless after writing.",
        "The store is bombproof.",
        "The store is fireproof.",
        "The store is waterproof.",
        "The store is weatherproof.",
        "The store is shatterproof.",
        "The store is rustproof.",
        "The store is soundproof.",
        "The store is childproof.",
        "Every record stands scrutinized before use.",
        "Every record stands ratified before use.",
        "Every record stands accredited before use.",
        "Records stand irrevocable after writing.",
        "Records stand irreversible after writing.",
        "The store is ironclad.",
        "Records stand indomitable after writing.",
        "Records stand unshakable after writing.",
        "The records are invincible by outside writers.",
        "The records are irreversible by outside writers.",
        "The records are irrevocable by outside writers.",
        "Heads stand initialled for every actor.",
        "Heads stand franked for every actor.",
    )

    def test_lexicon_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WORDINGS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_governed_and_clean_forms_still_pass(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod,
            "The seal guarantees protection conditional on "
            "the deployment confinement fact."))
        result = mod.lint_report_construction()
        self.assertTrue(result["seal_claim_lint_passed"])
        self.assertTrue(result["fixed_text_travel_lint_passed"])


class SealClaimScanAssertedVerbsFixR9Tests(unittest.TestCase):
    """Ruling 253: the asserted form limb."""

    VERB_FORMS = (
        "The journal cements integrity for every reader.",
        "The journal entrenches integrity for every reader.",
        "The journal enshrines integrity for every reader.",
        "The journal shows integrity for every reader.",
        "The journal displays integrity for every reader.",
        "The journal manifests integrity for every reader.",
        "The journal exemplifies integrity for every reader.",
        "The journal typifies integrity for every reader.",
        "The journal buttresses integrity for every reader.",
        "The journal champions integrity for every reader.",
        "The journal advances integrity for every reader.",
        "The journal boosts integrity for every reader.",
        "The journal elevates integrity for every reader.",
        "The journal enhances integrity for every reader.",
        "The journal augments integrity for every reader.",
        "The journal undergirds integrity for every reader.",
        "The mechanism pledges total integrity of the journal.",
        "The mechanism promises total integrity of the journal.",
        "The mechanism commits total integrity of the journal.",
        "The mechanism conveys total integrity of the journal.",
        "The mechanism asserts total integrity of the journal.",
        "The mechanism declares total integrity of the journal.",
        "The mechanism proclaims total integrity of the journal.",
        "The mechanism affirms total integrity of the journal.",
    )

    def test_asserted_verb_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.VERB_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_fragment_boundary_still_holds(self):
        mod = harness.require("ontoloop.report")
        statement = "Integrity label for the journal schedule."
        self.assertTrue(_scan(mod, statement), statement)
        self.assertTrue(_travel(mod, statement), statement)
        self.assertFalse(
            _scan(mod, "The journal gives integrity for every reader."))
        self.assertFalse(
            _scan(mod, "The journal secures integrity for every reader."))


class GoldenMappingFormsFixR9Tests(unittest.TestCase):
    """Ruling 254: golden readings in the abstract mapping form."""

    def test_mapping_proxy_and_userdict_records_read(self):
        mod = harness.require("ontoloop.golden_span")
        records = mod.golden_record_sets()["records"]
        self.assertTrue(records)
        for record in records.values():
            plain = mod.re_read(record)
            self.assertTrue(plain["read"], plain)
            proxied = mod.re_read(MappingProxyType(dict(record)))
            self.assertTrue(proxied["read"], proxied)
            userdict = mod.re_read(UserDict(dict(record)))
            self.assertTrue(userdict["read"], userdict)

    def test_mapping_proxy_payload_reads(self):
        mod = harness.require("ontoloop.golden_span")
        record = dict(
            next(iter(mod.golden_record_sets()["records"].values())))
        record["payload"] = MappingProxyType(dict(record["payload"]))
        result = mod.re_read(record)
        self.assertTrue(result["read"], result)

    def test_mapping_proxy_results_discharge(self):
        mod = harness.require("ontoloop.golden_span")
        entry = dict(mod.latest_meaning_change_entry())
        plain = mod.discharge_state(entry=entry)
        self.assertTrue(plain["discharged"], plain)
        changed = dict(entry)
        changed["result_of_each_check"] = MappingProxyType(
            dict(entry["result_of_each_check"]))
        state = mod.discharge_state(entry=changed)
        self.assertTrue(state["discharged"], state)
        self.assertFalse(state["bar_stands"])

    def test_standing_refusals_still_refuse(self):
        mod = harness.require("ontoloop.golden_span")
        refused = mod.re_read(("not", "a", "mapping"))
        self.assertFalse(refused["read"])
        entry = dict(mod.latest_meaning_change_entry())
        string_entry = dict(entry)
        string_entry["result_of_each_check"] = "not a mapping"
        state = mod.discharge_state(entry=string_entry)
        self.assertFalse(state["discharged"])
        self.assertTrue(state["bar_stands"])


class _ValueErrorHash:
    def __hash__(self):
        raise ValueError("hash act refuses this value")


class ProductionReportHashGuardFixR9Tests(unittest.TestCase):
    """Ruling 255: counting guards meeting a ValueError hash."""

    def test_value_error_hash_shape_states_no_count(self):
        mod = harness.require("ontoloop.report")
        result = mod.production_report_form(produced_records=[
            {"shape": _ValueErrorHash(), "family": "sealed family"}])
        self.assertEqual(result["production_counts"]["per_shape"], {})
        self.assertEqual(
            result["production_counts"]["per_family"],
            {"sealed family": 1})

    def test_value_error_hash_family_states_no_count(self):
        mod = harness.require("ontoloop.report")
        result = mod.production_report_form(produced_records=[
            {"shape": "sealed shape", "family": _ValueErrorHash()}])
        self.assertEqual(
            result["production_counts"]["per_shape"],
            {"sealed shape": 1})
        self.assertEqual(result["production_counts"]["per_family"], {})

    def test_writable_memoryview_values_state_no_count(self):
        mod = harness.require("ontoloop.report")
        view = memoryview(bytearray(b"shape"))
        result = mod.production_report_form(produced_records=[
            {"shape": view, "family": view}])
        self.assertEqual(result["production_counts"]["per_shape"], {})
        self.assertEqual(result["production_counts"]["per_family"], {})
        self.assertFalse(result["counts_present"])

    def test_standing_forms_still_count(self):
        mod = harness.require("ontoloop.report")
        result = mod.production_report_form(produced_records=[
            {"shape": ["a", "b"], "family": "fam"},
            {"shape": "sealed shape", "family": "fam"},
            MappingProxyType({"shape": "sealed shape", "family": "fam"}),
        ])
        self.assertEqual(
            result["production_counts"]["per_shape"], {"sealed shape": 2})
        self.assertEqual(
            result["production_counts"]["per_family"], {"fam": 3})
        self.assertTrue(result["counts_present"])


if __name__ == "__main__":
    unittest.main()
