"""Fix round 30 tests for Region 4: redacting append path.

Written first for ruling 1581 of the Round 30 triage.
Ruling 1581, identity S15-R30-CAPRED-1, Low: a wrapped
token carrying four intervening core carrying entries
in total, four benign words standing together after
the third fragment, four words standing together after
the first fragment, one word standing after each of
the first four fragments, or two words after the first
fragment and two more after the fourth, stands redacted
in part only beside a clean copy, fragment positions
after the intervening entries reaching the journal
unredacted and uncounted, carrying tail fragments in
every form and the head fragment in one form, because
the split joining skip and every extension skip of the
landed act count toward one total of three intervening
entries for the one assembly. The same standing holds
at five intervening entries, the word hello standing
between every pair of fragments, and at four
intervening entries inside a wrapping whose fragments
each carry a semicolon in the fragment interior. The
standing poles pin the forms that decide correctly
before the cure: the charged forms of rulings 1479 to
1482, the clean token alone, two clean copies, and the
detection boundary forms standing alone.
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

QUAD_WORDS = ["hello", "world", "again", "fourth"]
QUAD_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + QUAD_WORDS + FRAGMENTS8[3:]
)
QUAD_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + QUAD_WORDS + FRAGMENTS8[1:]
)
QUAD_SPREAD8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + ["world"] + FRAGMENTS8[2:3] + ["again"]
    + FRAGMENTS8[3:4] + ["fourth"] + FRAGMENTS8[4:]
)
QUAD_TWO_AND_TWO8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world"] + FRAGMENTS8[1:4]
    + ["again", "fourth"] + FRAGMENTS8[4:]
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
TRIPLE_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + ["hello", "world", "again"] + FRAGMENTS8[3:]
)
TRIPLE_SPREAD8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:3]
    + ["world"] + FRAGMENTS8[3:5] + ["again"] + FRAGMENTS8[5:]
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


class TestRedactFixR30Setup(unittest.TestCase):
    """The probed token and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_quad_intervening_fragments_join_to_token(self):
        for form in (
            QUAD_TOGETHER8,
            QUAD_AFTER_FIRST8,
            QUAD_SPREAD8,
            QUAD_TWO_AND_TWO8,
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in QUAD_WORDS)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in QUAD_WORDS), 4
            )

    def test_five_intervening_fragments_join_to_token(self):
        parts = FIVE_EACH8.split("\n")
        joined = "".join(p for p in parts if p != "hello")
        self.assertEqual(joined, TOKEN)
        self.assertEqual(sum(1 for p in parts if p == "hello"), 5)


class TestRedactFixR30QuadIntervening(unittest.TestCase):
    """Ruling 1581: a wrapping carrying four intervening
    entries in total, and five in the same form."""

    def test_four_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [QUAD_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        for word in QUAD_WORDS:
            self.assertIn(word, outcome["redacted_material"])

    def test_four_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, QUAD_TOGETHER8], 7, FRAGMENTS8
        )
        self.assertIn("fourth", outcome["redacted_material"])

    def test_four_after_first_redacted_whole_head_included(self):
        outcome = _assert_append(
            self, [QUAD_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_one_after_each_of_first_four_redacted_whole(self):
        outcome = _assert_append(
            self, [QUAD_SPREAD8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("fourth", outcome["redacted_material"])

    def test_two_after_first_and_two_after_fourth_redacted(self):
        outcome = _assert_append(
            self, [QUAD_TWO_AND_TWO8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("again", outcome["redacted_material"])

    def test_five_between_every_pair_redacted_whole(self):
        outcome = _assert_append(
            self, [FIVE_EACH8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_semicolon_quad_together_redacted_whole(self):
        _assert_append(
            self, [SEMI_QUAD_TOGETHER8, TOKEN], 7, SEMI_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_decoded_spans_cover_every_quad_fragment(self):
        module = require("ontoloop.redact")
        text = QUAD_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        for word in QUAD_WORDS:
            self.assertNotIn(word, covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [QUAD_TOGETHER8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR30Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_ruling_1482_three_together_still_redacts(self):
        outcome = _assert_append(
            self, [TRIPLE_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("again", outcome["redacted_material"])

    def test_ruling_1482_three_spread_still_redacts(self):
        outcome = _assert_append(
            self, [TRIPLE_SPREAD8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("world", outcome["redacted_material"])

    def test_ruling_1479_semicolon_fragments_still_redact(self):
        _assert_append(
            self, [SEMI_WRAPPED8, TOKEN], 7, SEMI_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_quad_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, QUAD_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], QUAD_TOGETHER8)

    def test_five_each_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, FIVE_EACH8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], FIVE_EACH8)

    def test_semicolon_quad_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_QUAD_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], SEMI_QUAD_TOGETHER8
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
