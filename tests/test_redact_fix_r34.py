"""Fix round 34 tests for Region 4: redacting append path.

Written first for ruling 2047 of the Round 34 triage.
Ruling 2047, identity S15-R34-CAPRED-1, Low: on the
redacting append path, a wrapped token carrying one
single gap of intervening entries past the joining
window stands redacted in part only beside a clean
copy, fragment positions after the gap reaching the
journal unredacted and uncounted, because the split
joining of the landed act runs in a window of twenty
four stream entries and each extension skip stands
bounded by that window in its own right. The gap
standing after the first fragment passes in part at
twenty three intervening entries and at every larger
gap probed, and a gap standing after the second,
third, fourth, or fifth fragment passes in part at
twenty five intervening entries and at every larger
gap probed, the passing forms standing at twenty
five together after the third fragment in both
orders, at twenty six, thirty, and forty together
after the third fragment, at twenty three, twenty
four, and twenty five together after the first
fragment, at twenty five together after the second,
fourth, and fifth fragments, at twenty five inside
a wrapping whose fragments each carry a semicolon
in the fragment interior, and at twenty five in one
gap beside one word standing in another gap. The
standing poles pin the forms that decide correctly
before the cure: the cured bounds of the landed form
at twenty four together after the third fragment,
at twenty two after the first fragment, and at
twenty three and twenty four after the second,
fourth, and fifth fragments, the spread forms whose
single gaps all stand inside their bounds at totals
of twenty five and forty intervening entries, the
clean token alone, two clean copies, and the
detection boundary forms standing alone and beside
a plain assignment line.
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
    "thirtyeighth thirtyninth fortieth"
).split()

TWENTY_WORDS = WORDS[:20]
TWENTY_TWO_WORDS = WORDS[:22]
TWENTY_THREE_WORDS = WORDS[:23]
TWENTY_FOUR_WORDS = WORDS[:24]
TWENTY_FIVE_WORDS = WORDS[:25]
TWENTY_SIX_WORDS = WORDS[:26]
THIRTY_WORDS = WORDS[:30]
FORTY_WORDS = WORDS[:40]


def _gap_form(after, words, fragments=None):
    fragments = FRAGMENTS8 if fragments is None else fragments
    return "\n".join(
        fragments[:after] + list(words) + fragments[after:]
    )


TWENTY_FIVE_TOGETHER8 = _gap_form(3, TWENTY_FIVE_WORDS)
TWENTY_SIX_TOGETHER8 = _gap_form(3, TWENTY_SIX_WORDS)
THIRTY_TOGETHER8 = _gap_form(3, THIRTY_WORDS)
FORTY_TOGETHER8 = _gap_form(3, FORTY_WORDS)
TWENTY_THREE_AFTER_FIRST8 = _gap_form(1, TWENTY_THREE_WORDS)
TWENTY_FOUR_AFTER_FIRST8 = _gap_form(1, TWENTY_FOUR_WORDS)
TWENTY_FIVE_AFTER_FIRST8 = _gap_form(1, TWENTY_FIVE_WORDS)
TWENTY_FIVE_AFTER_SECOND8 = _gap_form(2, TWENTY_FIVE_WORDS)
TWENTY_FIVE_AFTER_FOURTH8 = _gap_form(4, TWENTY_FIVE_WORDS)
TWENTY_FIVE_AFTER_FIFTH8 = _gap_form(5, TWENTY_FIVE_WORDS)
SEMI_TWENTY_FIVE_TOGETHER8 = _gap_form(
    3, TWENTY_FIVE_WORDS, SEMI_FRAGMENTS8
)
TWENTY_FIVE_SECOND_ONE_EACH8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + TWENTY_FIVE_WORDS + FRAGMENTS8[2:3] + ["again"]
    + FRAGMENTS8[3:]
)
TWENTY_FIVE_THIRD_ONE_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:3]
    + TWENTY_FIVE_WORDS + FRAGMENTS8[3:]
)
TWENTY_FOUR_TOGETHER8 = _gap_form(3, TWENTY_FOUR_WORDS)
TWENTY_TWO_AFTER_FIRST8 = _gap_form(1, TWENTY_TWO_WORDS)
TWENTY_FOUR_AFTER_SECOND8 = _gap_form(2, TWENTY_FOUR_WORDS)
TWENTY_FOUR_AFTER_FOURTH8 = _gap_form(4, TWENTY_FOUR_WORDS)
TWENTY_FOUR_AFTER_FIFTH8 = _gap_form(5, TWENTY_FOUR_WORDS)
FIVE_EVERY_GAP8 = "\n".join(
    FRAGMENTS8[:1] + WORDS[0:5] + FRAGMENTS8[1:2]
    + WORDS[5:10] + FRAGMENTS8[2:3] + WORDS[10:15]
    + FRAGMENTS8[3:4] + WORDS[15:20] + FRAGMENTS8[4:5]
    + WORDS[20:25] + FRAGMENTS8[5:]
)
TWENTY_TWENTY_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:1] + TWENTY_WORDS + FRAGMENTS8[1:3]
    + WORDS[20:40] + FRAGMENTS8[3:]
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


class TestRedactFixR34Setup(unittest.TestCase):
    """The probed token and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_single_gap_forms_fragments_join_to_token(self):
        for form, words in (
            (TWENTY_FIVE_TOGETHER8, TWENTY_FIVE_WORDS),
            (TWENTY_FIVE_AFTER_FIRST8, TWENTY_FIVE_WORDS),
            (TWENTY_FIVE_AFTER_SECOND8, TWENTY_FIVE_WORDS),
            (TWENTY_FIVE_AFTER_FOURTH8, TWENTY_FIVE_WORDS),
            (TWENTY_FIVE_AFTER_FIFTH8, TWENTY_FIVE_WORDS),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in words)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in words), 25
            )

    def test_further_single_gap_forms_join_to_token(self):
        for form, words, total in (
            (TWENTY_SIX_TOGETHER8, TWENTY_SIX_WORDS, 26),
            (THIRTY_TOGETHER8, THIRTY_WORDS, 30),
            (FORTY_TOGETHER8, FORTY_WORDS, 40),
            (TWENTY_THREE_AFTER_FIRST8, TWENTY_THREE_WORDS, 23),
            (TWENTY_FOUR_AFTER_FIRST8, TWENTY_FOUR_WORDS, 24),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in words)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in words), total
            )


class TestRedactFixR34SingleGapPastWindow(unittest.TestCase):
    """Ruling 2047: one single gap past the joining window."""

    def test_twenty_five_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [TWENTY_FIVE_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        for word in TWENTY_FIVE_WORDS:
            self.assertIn(word, outcome["redacted_material"])

    def test_twenty_five_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, TWENTY_FIVE_TOGETHER8], 7, FRAGMENTS8
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_twenty_six_together_redacted_whole(self):
        outcome = _assert_append(
            self, [TWENTY_SIX_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentysixth", outcome["redacted_material"])

    def test_thirty_together_redacted_whole(self):
        outcome = _assert_append(
            self, [THIRTY_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("thirtieth", outcome["redacted_material"])

    def test_forty_together_redacted_whole(self):
        outcome = _assert_append(
            self, [FORTY_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("fortieth", outcome["redacted_material"])

    def test_twenty_three_after_first_redacted_whole_head(self):
        outcome = _assert_append(
            self, [TWENTY_THREE_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_twenty_four_after_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FOUR_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfourth", outcome["redacted_material"])

    def test_twenty_five_after_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FIVE_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_twenty_five_after_first_clean_first_whole(self):
        outcome = _assert_append(
            self, [TOKEN, TWENTY_FIVE_AFTER_FIRST8], 7, FRAGMENTS8
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_twenty_five_after_second_redacted_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FIVE_AFTER_SECOND8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_twenty_five_after_fourth_redacted_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FIVE_AFTER_FOURTH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_twenty_five_after_fifth_redacted_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FIVE_AFTER_FIFTH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_semicolon_twenty_five_together_redacted_whole(self):
        _assert_append(
            self, [SEMI_TWENTY_FIVE_TOGETHER8, TOKEN], 7,
            SEMI_FRAGMENTS8, token_absent=TOKEN,
        )

    def test_twenty_five_one_gap_after_second_one_word_gaps(self):
        outcome = _assert_append(
            self, [TWENTY_FIVE_SECOND_ONE_EACH8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_twenty_five_after_third_one_word_after_first(self):
        outcome = _assert_append(
            self, [TWENTY_FIVE_THIRD_ONE_AFTER_FIRST8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_decoded_spans_cover_every_fragment_past_gap(self):
        module = require("ontoloop.redact")
        text = TWENTY_FIVE_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        for word in TWENTY_FIVE_WORDS:
            self.assertNotIn(word, covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [TWENTY_FIVE_TOGETHER8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR34Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_twenty_four_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FOUR_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfourth", outcome["redacted_material"])

    def test_twenty_two_after_first_still_redacts_whole(self):
        outcome = _assert_append(
            self, [TWENTY_TWO_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentysecond", outcome["redacted_material"])

    def test_twenty_four_after_second_still_redacts_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FOUR_AFTER_SECOND8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfourth", outcome["redacted_material"])

    def test_twenty_four_after_fourth_still_redacts_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FOUR_AFTER_FOURTH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfourth", outcome["redacted_material"])

    def test_twenty_four_after_fifth_still_redacts_whole(self):
        outcome = _assert_append(
            self, [TWENTY_FOUR_AFTER_FIFTH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfourth", outcome["redacted_material"])

    def test_five_in_every_gap_total_twenty_five_whole(self):
        outcome = _assert_append(
            self, [FIVE_EVERY_GAP8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twentyfifth", outcome["redacted_material"])

    def test_two_gaps_of_twenty_total_forty_whole(self):
        outcome = _assert_append(
            self, [TWENTY_TWENTY_TWO_GAPS8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("fortieth", outcome["redacted_material"])

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_twenty_five_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, TWENTY_FIVE_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], TWENTY_FIVE_TOGETHER8
        )

    def test_twenty_five_after_first_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, TWENTY_FIVE_AFTER_FIRST8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], TWENTY_FIVE_AFTER_FIRST8
        )

    def test_semicolon_twenty_five_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_TWENTY_FIVE_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], SEMI_TWENTY_FIVE_TOGETHER8
        )

    def test_twenty_five_together_beside_plain_assignment(self):
        _assert_append(
            self, [TWENTY_FIVE_TOGETHER8, ASSIGNMENT], 1, FRAGMENTS8
        )

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
