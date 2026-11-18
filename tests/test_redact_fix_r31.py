"""Fix round 31 tests for Region 4: redacting append path.

Written first for ruling 1688 of the Round 31 triage.
Ruling 1688, identity S15-R31-CAPRED-1, Low: a wrapped
token carrying six intervening core carrying entries
in total, six benign words standing together after
the third fragment, six words standing together after
the first fragment, two words after the first fragment
and one word after each of the second, third, fourth,
and fifth fragments, three words after the first
fragment and three more after the fourth, or one word
standing between every pair of fragments with a second
word standing in the last gap, stands redacted in part
only beside a clean copy, fragment positions after the
intervening entries reaching the journal unredacted
and uncounted, carrying tail fragments in every form
and the head fragment in one form, because the split
joining skip and every extension skip of the landed
act count toward one total of five intervening entries
for the one assembly. The same standing holds at seven
intervening entries standing together after the third
fragment, and at six intervening entries inside a
wrapping whose fragments each carry a semicolon in
the fragment interior. The standing poles pin the
forms that decide correctly before the cure: the
charged forms of rulings 1479 to 1482 and 1581, the
clean token alone, two clean copies, and the detection
boundary forms standing alone.
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
SEMI_WRAPPED8 = "\n".join(SEMI_FRAGMENTS8)

SIX_WORDS = ["hello", "world", "again", "fourth", "fifth", "sixth"]
SEVEN_WORDS = SIX_WORDS + ["seventh"]
SIX_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + SIX_WORDS + FRAGMENTS8[3:]
)
SIX_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + SIX_WORDS + FRAGMENTS8[1:]
)
SIX_SPREAD8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world"] + FRAGMENTS8[1:2]
    + ["again"] + FRAGMENTS8[2:3] + ["fourth"]
    + FRAGMENTS8[3:4] + ["fifth"] + FRAGMENTS8[4:5]
    + ["sixth"] + FRAGMENTS8[5:]
)
SIX_THREE_AND_THREE8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world", "again"] + FRAGMENTS8[1:4]
    + ["fourth", "fifth", "sixth"] + FRAGMENTS8[4:]
)
SIX_EACH_GAP8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + ["world"] + FRAGMENTS8[2:3] + ["again"]
    + FRAGMENTS8[3:4] + ["fourth"] + FRAGMENTS8[4:5]
    + ["fifth", "sixth"] + FRAGMENTS8[5:]
)
SEVEN_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + SEVEN_WORDS + FRAGMENTS8[3:]
)
SEMI_SIX_TOGETHER8 = "\n".join(
    SEMI_FRAGMENTS8[:3] + SIX_WORDS + SEMI_FRAGMENTS8[3:]
)
QUAD_WORDS = ["hello", "world", "again", "fourth"]
QUAD_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + QUAD_WORDS + FRAGMENTS8[3:]
)
FIVE_EACH8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + ["hello"] + FRAGMENTS8[2:3] + ["hello"]
    + FRAGMENTS8[3:4] + ["hello"] + FRAGMENTS8[4:5]
    + ["hello"] + FRAGMENTS8[5:]
)
SEMI_QUAD_TOGETHER8 = "\n".join(
    SEMI_FRAGMENTS8[:3] + QUAD_WORDS + SEMI_FRAGMENTS8[3:]
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


class TestRedactFixR31Setup(unittest.TestCase):
    """The probed token and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_six_intervening_fragments_join_to_token(self):
        for form in (
            SIX_TOGETHER8,
            SIX_AFTER_FIRST8,
            SIX_SPREAD8,
            SIX_THREE_AND_THREE8,
            SIX_EACH_GAP8,
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in SIX_WORDS)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in SIX_WORDS), 6
            )

    def test_seven_intervening_fragments_join_to_token(self):
        parts = SEVEN_TOGETHER8.split("\n")
        joined = "".join(p for p in parts if p not in SEVEN_WORDS)
        self.assertEqual(joined, TOKEN)
        self.assertEqual(
            sum(1 for p in parts if p in SEVEN_WORDS), 7
        )


class TestRedactFixR31SixIntervening(unittest.TestCase):
    """Ruling 1688: a wrapping carrying six intervening
    entries in total, and seven in the together form."""

    def test_six_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [SIX_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        for word in SIX_WORDS:
            self.assertIn(word, outcome["redacted_material"])

    def test_six_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, SIX_TOGETHER8], 7, FRAGMENTS8
        )
        self.assertIn("sixth", outcome["redacted_material"])

    def test_six_after_first_redacted_whole_head_included(self):
        outcome = _assert_append(
            self, [SIX_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_two_after_first_one_after_each_next_redacted(self):
        outcome = _assert_append(
            self, [SIX_SPREAD8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("sixth", outcome["redacted_material"])

    def test_three_after_first_three_after_fourth_redacted(self):
        outcome = _assert_append(
            self, [SIX_THREE_AND_THREE8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("sixth", outcome["redacted_material"])

    def test_one_in_every_gap_second_in_last_redacted(self):
        outcome = _assert_append(
            self, [SIX_EACH_GAP8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("sixth", outcome["redacted_material"])

    def test_seven_together_redacted_whole(self):
        outcome = _assert_append(
            self, [SEVEN_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("seventh", outcome["redacted_material"])

    def test_semicolon_six_together_redacted_whole(self):
        _assert_append(
            self, [SEMI_SIX_TOGETHER8, TOKEN], 7, SEMI_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_decoded_spans_cover_every_six_fragment(self):
        module = require("ontoloop.redact")
        text = SIX_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        for word in SIX_WORDS:
            self.assertNotIn(word, covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [SIX_TOGETHER8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR31Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_ruling_1581_four_together_still_redacts(self):
        outcome = _assert_append(
            self, [QUAD_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("fourth", outcome["redacted_material"])

    def test_ruling_1581_five_each_still_redacts(self):
        outcome = _assert_append(
            self, [FIVE_EACH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_ruling_1479_semicolon_quad_still_redacts(self):
        _assert_append(
            self, [SEMI_QUAD_TOGETHER8, TOKEN], 7, SEMI_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_six_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SIX_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], SIX_TOGETHER8)

    def test_seven_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEVEN_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], SEVEN_TOGETHER8)

    def test_semicolon_six_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_SIX_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], SEMI_SIX_TOGETHER8
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
