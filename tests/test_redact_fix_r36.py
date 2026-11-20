"""Fix round 36 tests for Region 4: redacting append path.

Written first for ruling 2307 of the Round 36 triage.
Ruling 2307, identity S15-R36-CAPRED-1, Low: on the
redacting append path, a wrapped token carrying one
single gap of intervening entries past the joining
window stands redacted in part only beside a clean
copy, fragment positions after the gap reaching the
journal unredacted and uncounted, because the split
joining of the landed act runs in a window of ninety
six stream entries and each extension skip stands
bounded by that window in its own right. The gap
standing after the first fragment passes in part at
ninety five intervening entries and at every larger
gap probed, and a gap standing after the second,
third, fourth, or fifth fragment passes in part at
ninety seven intervening entries and at every larger
gap probed, the passing forms standing at ninety
seven together after the third fragment in both
orders, at one hundred and one hundred twenty eight
together after the third fragment, at ninety five,
ninety six, and one hundred twenty eight together
after the first fragment, at ninety seven together
after the second, fourth, and fifth fragments, at
ninety seven inside a wrapping whose fragments each
carry a semicolon in the fragment interior, and at
ninety seven in one gap beside one word standing in
another gap. The standing poles pin the forms that
decide correctly before the cure: the cured bounds
of the landed form at ninety six together after the
third fragment, at ninety four after the first
fragment, and at ninety six after the second,
fourth, and fifth fragments, the spread forms whose
single gaps all stand inside their bounds at totals
of ninety, ninety six, and one hundred ninety two
intervening entries, the clean token alone, two
clean copies, and the detection boundary forms
standing alone and beside a plain assignment line.
"""

import base64
import unittest

from tests.harness import require

PLAIN = b"password = " + b"a" * 20
TOKEN = base64.b64encode(PLAIN).decode("ascii")
ASSIGNMENT = "password = PlainValue999"


def _wrap(token, width):
    return "\n".join(
        token[start:start + width]
        for start in range(0, len(token), width)
    )


WRAPPED8 = _wrap(TOKEN, 8)
FRAGMENTS8 = WRAPPED8.split("\n")
GOLDEN_ANCHOR = (
    "c91e73191bb5ef6cd2db017b12e101a5a1f12d5be8e7b4e430e7604e4d6038ee"
)


def _interior_fragments(char):
    dressed = []
    for fragment in FRAGMENTS8:
        if len(fragment) > 4:
            dressed.append(fragment[:4] + char + fragment[4:])
        else:
            dressed.append(fragment[:2] + char + fragment[2:])
    return dressed


SEMI_FRAGMENTS8 = _interior_fragments(";")

WORDS = (
    "hello world again fourth fifth sixth seventh eighth ninth "
    "tenth eleventh twelfth thirteenth fourteenth fifteenth "
    "sixteenth seventeenth eighteenth nineteenth twentieth "
    "twentyfirst twentysecond twentythird twentyfourth "
    "twentyfifth twentysixth twentyseventh twentyeighth "
    "twentyninth thirtieth thirtyfirst thirtysecond thirtythird "
    "thirtyfourth thirtyfifth thirtysixth thirtyseventh "
    "thirtyeighth thirtyninth fortieth fortyfirst fortysecond "
    "fortythird fortyfourth fortyfifth fortysixth fortyseventh "
    "fortyeighth fortyninth fiftieth fiftyfirst fiftysecond "
    "fiftythird fiftyfourth fiftyfifth fiftysixth fiftyseventh "
    "fiftyeighth fiftyninth sixtieth sixtyfirst sixtysecond "
    "sixtythird sixtyfourth sixtyfifth sixtysixth sixtyseventh "
    "sixtyeighth sixtyninth seventieth seventyfirst seventysecond "
    "seventythird seventyfourth seventyfifth seventysixth "
    "seventyseventh seventyeighth seventyninth eightieth "
    "eightyfirst eightysecond eightythird eightyfourth "
    "eightyfifth eightysixth eightyseventh eightyeighth "
    "eightyninth ninetieth ninetyfirst ninetysecond ninetythird "
    "ninetyfourth ninetyfifth ninetysixth ninetyseventh "
    "ninetyeighth ninetyninth hundredth hundredfirst "
    "hundredsecond hundredthird hundredfourth hundredfifth "
    "hundredsixth hundredseventh hundredeighth hundredninth "
    "hundredtenth hundredeleventh hundredtwelfth "
    "hundredthirteenth hundredfourteenth hundredfifteenth "
    "hundredsixteenth hundredseventeenth hundredeighteenth "
    "hundrednineteenth hundredtwentieth hundredtwentyfirst "
    "hundredtwentysecond hundredtwentythird hundredtwentyfourth "
    "hundredtwentyfifth hundredtwentysixth hundredtwentyseventh "
    "hundredtwentyeighth"
).split()

WORDS_SET = set(WORDS)
NINETY_FOUR_WORDS = WORDS[:94]
NINETY_FIVE_WORDS = WORDS[:95]
NINETY_SIX_WORDS = WORDS[:96]
NINETY_SEVEN_WORDS = WORDS[:97]
HUNDRED_WORDS = WORDS[:100]
HUNDRED_TWENTY_EIGHT_WORDS = WORDS[:128]


def _gap_form(after, words, fragments=None):
    fragments = FRAGMENTS8 if fragments is None else fragments
    return "\n".join(
        fragments[:after] + list(words) + fragments[after:]
    )


NINETY_SEVEN_TOGETHER8 = _gap_form(3, NINETY_SEVEN_WORDS)
HUNDRED_TOGETHER8 = _gap_form(3, HUNDRED_WORDS)
HUNDRED_TWENTY_EIGHT_TOGETHER8 = _gap_form(
    3, HUNDRED_TWENTY_EIGHT_WORDS
)
NINETY_FIVE_AFTER_FIRST8 = _gap_form(1, NINETY_FIVE_WORDS)
NINETY_SIX_AFTER_FIRST8 = _gap_form(1, NINETY_SIX_WORDS)
HUNDRED_TWENTY_EIGHT_AFTER_FIRST8 = _gap_form(
    1, HUNDRED_TWENTY_EIGHT_WORDS
)
NINETY_SEVEN_AFTER_SECOND8 = _gap_form(2, NINETY_SEVEN_WORDS)
NINETY_SEVEN_AFTER_FOURTH8 = _gap_form(4, NINETY_SEVEN_WORDS)
NINETY_SEVEN_AFTER_FIFTH8 = _gap_form(5, NINETY_SEVEN_WORDS)
SEMI_NINETY_SEVEN_TOGETHER8 = _gap_form(
    3, NINETY_SEVEN_WORDS, SEMI_FRAGMENTS8
)
NINETY_SEVEN_SECOND_ONE_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + NINETY_SEVEN_WORDS + FRAGMENTS8[2:]
)
NINETY_SEVEN_THIRD_ONE_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:3]
    + NINETY_SEVEN_WORDS + FRAGMENTS8[3:]
)
NINETY_SIX_TOGETHER8 = _gap_form(3, NINETY_SIX_WORDS)
NINETY_FOUR_AFTER_FIRST8 = _gap_form(1, NINETY_FOUR_WORDS)
NINETY_SIX_AFTER_SECOND8 = _gap_form(2, NINETY_SIX_WORDS)
NINETY_SIX_AFTER_FOURTH8 = _gap_form(4, NINETY_SIX_WORDS)
NINETY_SIX_AFTER_FIFTH8 = _gap_form(5, NINETY_SIX_WORDS)
EIGHTEEN_EVERY_GAP8 = "\n".join(
    FRAGMENTS8[:1] + WORDS[0:18] + FRAGMENTS8[1:2]
    + WORDS[18:36] + FRAGMENTS8[2:3] + WORDS[36:54]
    + FRAGMENTS8[3:4] + WORDS[54:72] + FRAGMENTS8[4:5]
    + WORDS[72:90] + FRAGMENTS8[5:]
)
FORTY_EIGHT_FORTY_EIGHT_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:1] + WORDS[:48] + FRAGMENTS8[1:3]
    + WORDS[48:96] + FRAGMENTS8[3:]
)
NINETY_SIX_NINETY_SIX_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:3] + WORDS[:96] + FRAGMENTS8[3:4]
    + WORDS[:96] + FRAGMENTS8[4:]
)


def _journal_bytes(store):
    return b"\n".join(
        record["canonical_bytes"] for record in store["records"]
    )


def _append(module, store_module, material):
    store = store_module.golden_record_store()
    before = len(store["records"])
    outcome = module.append_redacted(store, material, scope="run one")
    return store, before, outcome


def _assert_append(test, material, hits, absent, token_absent=None):
    module = require("ontoloop.redact")
    store_module = require("ontoloop.store")
    store, before, outcome = _append(module, store_module, material)
    test.assertTrue(outcome["appended"])
    test.assertFalse(outcome["refused"])
    test.assertEqual(outcome["hits_redacted"], hits)
    test.assertEqual(len(store["records"]), before + 1)
    for fragment in absent:
        test.assertNotIn(fragment, outcome["redacted_material"])
        test.assertNotIn(
            fragment.encode("utf-8"), _journal_bytes(store)
        )
    if token_absent is not None:
        test.assertNotIn(token_absent, outcome["redacted_material"])
        test.assertNotIn(
            token_absent.encode("utf-8"), _journal_bytes(store)
        )
    return outcome


class TestRedactFixR36Setup(unittest.TestCase):
    """The probed token and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_single_gap_forms_fragments_join_to_token(self):
        for form, total in (
            (NINETY_SEVEN_TOGETHER8, 97),
            (NINETY_FIVE_AFTER_FIRST8, 95),
            (NINETY_SEVEN_AFTER_SECOND8, 97),
            (NINETY_SEVEN_AFTER_FOURTH8, 97),
            (NINETY_SEVEN_AFTER_FIFTH8, 97),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in WORDS_SET)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in WORDS_SET), total
            )

    def test_further_single_gap_forms_join_to_token(self):
        for form, total in (
            (HUNDRED_TOGETHER8, 100),
            (HUNDRED_TWENTY_EIGHT_TOGETHER8, 128),
            (NINETY_SIX_AFTER_FIRST8, 96),
            (HUNDRED_TWENTY_EIGHT_AFTER_FIRST8, 128),
            (NINETY_SEVEN_SECOND_ONE_AFTER_FIRST8, 98),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in WORDS_SET)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in WORDS_SET), total
            )


class TestRedactFixR36SingleGapPastWindow(unittest.TestCase):
    """Ruling 2307: one single gap past the joining window."""

    def test_ninety_seven_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [NINETY_SEVEN_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        for word in NINETY_SEVEN_WORDS:
            self.assertIn(word, outcome["redacted_material"])

    def test_ninety_seven_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, NINETY_SEVEN_TOGETHER8], 7, FRAGMENTS8
        )
        self.assertIn("ninetyseventh", outcome["redacted_material"])

    def test_hundred_together_redacted_whole(self):
        outcome = _assert_append(
            self, [HUNDRED_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hundredth", outcome["redacted_material"])

    def test_hundred_twenty_eight_together_redacted_whole(self):
        outcome = _assert_append(
            self, [HUNDRED_TWENTY_EIGHT_TOGETHER8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn(
            "hundredtwentyeighth", outcome["redacted_material"]
        )

    def test_ninety_five_after_first_redacted_whole_head(self):
        outcome = _assert_append(
            self, [NINETY_FIVE_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_ninety_six_after_first_redacted_whole(self):
        outcome = _assert_append(
            self, [NINETY_SIX_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

    def test_hundred_twenty_eight_after_first_redacted_whole(self):
        outcome = _assert_append(
            self, [HUNDRED_TWENTY_EIGHT_AFTER_FIRST8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn(
            "hundredtwentyeighth", outcome["redacted_material"]
        )

    def test_ninety_five_after_first_clean_first_whole(self):
        outcome = _assert_append(
            self, [TOKEN, NINETY_FIVE_AFTER_FIRST8], 7, FRAGMENTS8
        )
        self.assertIn("ninetyfifth", outcome["redacted_material"])

    def test_ninety_seven_after_second_redacted_whole(self):
        outcome = _assert_append(
            self, [NINETY_SEVEN_AFTER_SECOND8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetyseventh", outcome["redacted_material"])

    def test_ninety_seven_after_fourth_redacted_whole(self):
        outcome = _assert_append(
            self, [NINETY_SEVEN_AFTER_FOURTH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetyseventh", outcome["redacted_material"])

    def test_ninety_seven_after_fifth_redacted_whole(self):
        outcome = _assert_append(
            self, [NINETY_SEVEN_AFTER_FIFTH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetyseventh", outcome["redacted_material"])

    def test_semicolon_ninety_seven_together_redacted_whole(self):
        _assert_append(
            self, [SEMI_NINETY_SEVEN_TOGETHER8, TOKEN], 7,
            SEMI_FRAGMENTS8, token_absent=TOKEN,
        )

    def test_ninety_seven_one_gap_after_second_one_word_gap(self):
        outcome = _assert_append(
            self, [NINETY_SEVEN_SECOND_ONE_AFTER_FIRST8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn("ninetyseventh", outcome["redacted_material"])

    def test_ninety_seven_after_third_one_word_after_first(self):
        outcome = _assert_append(
            self, [NINETY_SEVEN_THIRD_ONE_AFTER_FIRST8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn("ninetyseventh", outcome["redacted_material"])

    def test_decoded_spans_cover_every_fragment_past_gap(self):
        module = require("ontoloop.redact")
        text = NINETY_SEVEN_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        for word in NINETY_SEVEN_WORDS:
            self.assertNotIn(word, covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [NINETY_SEVEN_TOGETHER8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR36Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_ninety_six_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [NINETY_SIX_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

    def test_ninety_four_after_first_still_redacts_whole(self):
        outcome = _assert_append(
            self, [NINETY_FOUR_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetyfourth", outcome["redacted_material"])

    def test_ninety_six_after_second_still_redacts_whole(self):
        outcome = _assert_append(
            self, [NINETY_SIX_AFTER_SECOND8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

    def test_ninety_six_after_fourth_still_redacts_whole(self):
        outcome = _assert_append(
            self, [NINETY_SIX_AFTER_FOURTH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

    def test_ninety_six_after_fifth_still_redacts_whole(self):
        outcome = _assert_append(
            self, [NINETY_SIX_AFTER_FIFTH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

    def test_eighteen_in_every_gap_total_ninety_whole(self):
        outcome = _assert_append(
            self, [EIGHTEEN_EVERY_GAP8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eightyninth", outcome["redacted_material"])

    def test_two_gaps_of_forty_eight_total_ninety_six_whole(self):
        outcome = _assert_append(
            self, [FORTY_EIGHT_FORTY_EIGHT_TWO_GAPS8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

    def test_two_gaps_of_ninety_six_total_192_whole(self):
        outcome = _assert_append(
            self, [NINETY_SIX_NINETY_SIX_TWO_GAPS8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_ninety_seven_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, NINETY_SEVEN_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], NINETY_SEVEN_TOGETHER8
        )

    def test_ninety_five_after_first_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, NINETY_FIVE_AFTER_FIRST8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], NINETY_FIVE_AFTER_FIRST8
        )

    def test_semicolon_ninety_seven_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_NINETY_SEVEN_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], SEMI_NINETY_SEVEN_TOGETHER8
        )

    def test_ninety_seven_together_beside_plain_assignment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module,
            [NINETY_SEVEN_TOGETHER8, ASSIGNMENT],
        )
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertGreaterEqual(outcome["hits_redacted"], 1)
        journal = _journal_bytes(store)
        for fragment in FRAGMENTS8:
            self.assertNotIn(fragment, outcome["redacted_material"])
            self.assertNotIn(fragment.encode("utf-8"), journal)

    def test_benign_words_beside_clean_token_stand(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, [TOKEN, "hello world"]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertIn("hello world", outcome["redacted_material"])

    def test_plain_assignment_alone_redacted_once(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, ASSIGNMENT
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertNotIn("PlainValue999", outcome["redacted_material"])

    def test_clean_material_unchanged(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        material = "a routine note about lunch"
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["placeholders"], [])
        self.assertEqual(outcome["redacted_material"], material)


if __name__ == "__main__":
    unittest.main()
