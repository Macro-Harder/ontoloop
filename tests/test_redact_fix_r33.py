"""Fix round 33 tests for Region 4: redacting append path.

Written first for ruling 1916 of the Round 33 triage.
Ruling 1916, identity S15-R33-CAPRED-1, Low: a wrapped
token carrying ten intervening core carrying entries
in total, ten words standing together after the third
fragment, ten words standing together after the first
fragment, two words after the first fragment and one
word after each of the second, third, and fourth
fragments and five words after the fifth, five words
after the first fragment and five more after the
fourth, two words standing between every pair of
fragments, one word standing between every pair of
fragments in the first four gaps and six words in the
last gap, or ten words inside a wrapping whose
fragments each carry a semicolon in the fragment
interior, stands redacted in part only beside a clean
copy, fragment positions after the intervening entries
reaching the journal unredacted and uncounted, because
the split joining skip and every extension skip of the
landed act count toward one total of nine intervening
entries for the one assembly. The same standing holds
at eleven intervening entries standing together after
the third fragment, at eleven standing together after
the first fragment, at eleven spread at three words
after the first fragment and one word after each of
the second, third, and fourth fragments and five words
after the fifth, at twelve standing together after the
third fragment, and at fifteen spread at three words
standing between every pair of fragments and at
fifteen standing together after the third fragment.
The standing poles pin the forms that decide correctly
before the cure: the nine entry forms of ruling 1794,
the eight and seven entry forms of the earlier rounds,
the clean token alone, two clean copies, and the
detection boundary forms standing alone and beside a
plain assignment line.
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

SIX_WORDS = ["hello", "world", "again", "fourth", "fifth", "sixth"]
SEVEN_WORDS = SIX_WORDS + ["seventh"]
EIGHT_WORDS = SEVEN_WORDS + ["eighth"]
NINE_WORDS = EIGHT_WORDS + ["ninth"]
TEN_WORDS = NINE_WORDS + ["tenth"]
ELEVEN_WORDS = TEN_WORDS + ["eleventh"]
TWELVE_WORDS = ELEVEN_WORDS + ["twelfth"]
FIFTEEN_WORDS = TWELVE_WORDS + [
    "thirteenth", "fourteenth", "fifteenth",
]

TEN_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + TEN_WORDS + FRAGMENTS8[3:]
)
ELEVEN_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + ELEVEN_WORDS + FRAGMENTS8[3:]
)
TWELVE_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + TWELVE_WORDS + FRAGMENTS8[3:]
)
FIFTEEN_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + FIFTEEN_WORDS + FRAGMENTS8[3:]
)
TEN_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + TEN_WORDS + FRAGMENTS8[1:]
)
ELEVEN_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + ELEVEN_WORDS + FRAGMENTS8[1:]
)
TEN_SPREAD_A8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world"] + FRAGMENTS8[1:2]
    + ["again"] + FRAGMENTS8[2:3] + ["fourth"]
    + FRAGMENTS8[3:4] + ["fifth"] + FRAGMENTS8[4:5]
    + ["sixth", "seventh", "eighth", "ninth", "tenth"]
    + FRAGMENTS8[5:]
)
ELEVEN_SPREAD8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world", "again"] + FRAGMENTS8[1:2]
    + ["fourth"] + FRAGMENTS8[2:3] + ["fifth"]
    + FRAGMENTS8[3:4] + ["sixth"] + FRAGMENTS8[4:5]
    + ["seventh", "eighth", "ninth", "tenth", "eleventh"]
    + FRAGMENTS8[5:]
)
TEN_SPREAD_B8 = "\n".join(
    FRAGMENTS8[:1] + TEN_WORDS[:5] + FRAGMENTS8[1:4]
    + TEN_WORDS[5:] + FRAGMENTS8[4:]
)
SEMI_TEN_TOGETHER8 = "\n".join(
    SEMI_FRAGMENTS8[:3] + TEN_WORDS + SEMI_FRAGMENTS8[3:]
)
TEN_UNIFORM8 = "\n".join(
    FRAGMENTS8[:1] + TEN_WORDS[0:2] + FRAGMENTS8[1:2]
    + TEN_WORDS[2:4] + FRAGMENTS8[2:3] + TEN_WORDS[4:6]
    + FRAGMENTS8[3:4] + TEN_WORDS[6:8] + FRAGMENTS8[4:5]
    + TEN_WORDS[8:10] + FRAGMENTS8[5:]
)
TEN_LAST_GAP8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + ["world"] + FRAGMENTS8[2:3] + ["again"]
    + FRAGMENTS8[3:4] + ["fourth"] + FRAGMENTS8[4:5]
    + ["fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    + FRAGMENTS8[5:]
)
FIFTEEN_UNIFORM8 = "\n".join(
    FRAGMENTS8[:1] + FIFTEEN_WORDS[0:3] + FRAGMENTS8[1:2]
    + FIFTEEN_WORDS[3:6] + FRAGMENTS8[2:3] + FIFTEEN_WORDS[6:9]
    + FRAGMENTS8[3:4] + FIFTEEN_WORDS[9:12] + FRAGMENTS8[4:5]
    + FIFTEEN_WORDS[12:15] + FRAGMENTS8[5:]
)
NINE_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + NINE_WORDS + FRAGMENTS8[3:]
)
EIGHT_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + EIGHT_WORDS + FRAGMENTS8[3:]
)
SEVEN_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + SEVEN_WORDS + FRAGMENTS8[3:]
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


class TestRedactFixR33Setup(unittest.TestCase):
    """The probed token and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_ten_intervening_fragments_join_to_token(self):
        for form, words in (
            (TEN_TOGETHER8, TEN_WORDS),
            (TEN_AFTER_FIRST8, TEN_WORDS),
            (TEN_SPREAD_A8, TEN_WORDS),
            (TEN_SPREAD_B8, TEN_WORDS),
            (TEN_UNIFORM8, TEN_WORDS),
            (TEN_LAST_GAP8, TEN_WORDS),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in words)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in words), 10
            )

    def test_further_totals_fragments_join_to_token(self):
        for form, words, total in (
            (ELEVEN_TOGETHER8, ELEVEN_WORDS, 11),
            (ELEVEN_AFTER_FIRST8, ELEVEN_WORDS, 11),
            (ELEVEN_SPREAD8, ELEVEN_WORDS, 11),
            (TWELVE_TOGETHER8, TWELVE_WORDS, 12),
            (FIFTEEN_TOGETHER8, FIFTEEN_WORDS, 15),
            (FIFTEEN_UNIFORM8, FIFTEEN_WORDS, 15),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in words)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in words), total
            )


class TestRedactFixR33TenAndFurtherTotals(unittest.TestCase):
    """Ruling 1916: a wrapping carrying ten intervening
    entries in total, and eleven, twelve, and fifteen."""

    def test_ten_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [TEN_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        for word in TEN_WORDS:
            self.assertIn(word, outcome["redacted_material"])

    def test_ten_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, TEN_TOGETHER8], 7, FRAGMENTS8
        )
        self.assertIn("tenth", outcome["redacted_material"])

    def test_eleven_together_redacted_whole(self):
        outcome = _assert_append(
            self, [ELEVEN_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eleventh", outcome["redacted_material"])

    def test_twelve_together_redacted_whole(self):
        outcome = _assert_append(
            self, [TWELVE_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("twelfth", outcome["redacted_material"])

    def test_ten_after_first_redacted_whole_head_included(self):
        outcome = _assert_append(
            self, [TEN_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_eleven_after_first_redacted_whole(self):
        outcome = _assert_append(
            self, [ELEVEN_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eleventh", outcome["redacted_material"])

    def test_ten_spread_two_one_one_one_five_whole(self):
        outcome = _assert_append(
            self, [TEN_SPREAD_A8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("tenth", outcome["redacted_material"])

    def test_eleven_spread_three_one_one_one_five_whole(self):
        outcome = _assert_append(
            self, [ELEVEN_SPREAD8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eleventh", outcome["redacted_material"])

    def test_ten_spread_five_after_first_five_after_fourth(self):
        outcome = _assert_append(
            self, [TEN_SPREAD_B8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("tenth", outcome["redacted_material"])

    def test_semicolon_ten_together_redacted_whole(self):
        _assert_append(
            self, [SEMI_TEN_TOGETHER8, TOKEN], 7, SEMI_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_ten_uniform_two_between_every_pair_whole(self):
        outcome = _assert_append(
            self, [TEN_UNIFORM8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("tenth", outcome["redacted_material"])

    def test_ten_last_gap_six_in_last_gap_whole(self):
        outcome = _assert_append(
            self, [TEN_LAST_GAP8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("tenth", outcome["redacted_material"])

    def test_fifteen_uniform_three_between_every_pair(self):
        outcome = _assert_append(
            self, [FIFTEEN_UNIFORM8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("fifteenth", outcome["redacted_material"])

    def test_fifteen_together_redacted_whole(self):
        outcome = _assert_append(
            self, [FIFTEEN_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("fifteenth", outcome["redacted_material"])

    def test_decoded_spans_cover_every_ten_fragment(self):
        module = require("ontoloop.redact")
        text = TEN_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        for word in TEN_WORDS:
            self.assertNotIn(word, covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [TEN_TOGETHER8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR33Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_nine_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [NINE_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninth", outcome["redacted_material"])

    def test_eight_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [EIGHT_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eighth", outcome["redacted_material"])

    def test_seven_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [SEVEN_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("seventh", outcome["redacted_material"])

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_ten_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, TEN_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], TEN_TOGETHER8)

    def test_ten_after_first_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, TEN_AFTER_FIRST8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], TEN_AFTER_FIRST8
        )

    def test_semicolon_ten_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_TEN_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], SEMI_TEN_TOGETHER8
        )

    def test_ten_together_beside_plain_assignment(self):
        _assert_append(
            self, [TEN_TOGETHER8, ASSIGNMENT], 1, FRAGMENTS8
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
