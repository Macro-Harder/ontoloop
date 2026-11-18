"""Fix round 32 tests for Region 3: redacting append path.

Written first for ruling 1794 of the Round 32 triage.
Ruling 1794, identity S15-R32-CAPRED-1, Low: a wrapped
token carrying eight intervening core carrying entries
in total, eight benign words standing together after
the third fragment, eight words standing together after
the first fragment, two words after the first fragment
and one word after each of the second, third, and
fourth fragments and three words after the fifth, or
four words after the first fragment and four more after
the fourth, stands redacted in part only beside a clean
copy, fragment positions after the intervening entries
reaching the journal unredacted and uncounted, carrying
tail fragments in every form and the head fragment in
one form, because the split joining skip and every
extension skip of the landed act count toward one total
of seven intervening entries for the one assembly. The
same standing holds at nine intervening entries standing
together after the third fragment, and at eight
intervening entries inside a wrapping whose fragments
each carry a semicolon in the fragment interior. The
standing poles pin the forms that decide correctly
before the cure: the seven entry forms of ruling 1688,
the eight entry distribution that stands decided whole
in the raising paper, one word standing between every
pair of fragments with three more words standing in the
last gap, the clean token alone, two clean copies, and
the detection boundary forms standing alone and beside
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
SEMI_WRAPPED8 = "\n".join(SEMI_FRAGMENTS8)

SIX_WORDS = ["hello", "world", "again", "fourth", "fifth", "sixth"]
SEVEN_WORDS = SIX_WORDS + ["seventh"]
EIGHT_WORDS = SEVEN_WORDS + ["eighth"]
NINE_WORDS = EIGHT_WORDS + ["ninth"]
EIGHT_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + EIGHT_WORDS + FRAGMENTS8[3:]
)
EIGHT_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + EIGHT_WORDS + FRAGMENTS8[1:]
)
EIGHT_SPREAD_A8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world"] + FRAGMENTS8[1:2]
    + ["again"] + FRAGMENTS8[2:3] + ["fourth"]
    + FRAGMENTS8[3:4] + ["fifth"] + FRAGMENTS8[4:5]
    + ["sixth", "seventh", "eighth"] + FRAGMENTS8[5:]
)
EIGHT_SPREAD_B8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world", "again", "fourth"]
    + FRAGMENTS8[1:4]
    + ["fifth", "sixth", "seventh", "eighth"] + FRAGMENTS8[4:]
)
EIGHT_EACH_GAP8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + ["hello"] + FRAGMENTS8[2:3] + ["hello"]
    + FRAGMENTS8[3:4] + ["hello"] + FRAGMENTS8[4:5]
    + ["hello", "world", "again"] + FRAGMENTS8[5:]
)
SEMI_EIGHT_TOGETHER8 = "\n".join(
    SEMI_FRAGMENTS8[:3] + EIGHT_WORDS + SEMI_FRAGMENTS8[3:]
)
NINE_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + NINE_WORDS + FRAGMENTS8[3:]
)
SEVEN_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + SEVEN_WORDS + FRAGMENTS8[3:]
)
SIX_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + SIX_WORDS + FRAGMENTS8[3:]
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


class TestRedactFixR32Setup(unittest.TestCase):
    """The probed token and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_eight_intervening_fragments_join_to_token(self):
        for form in (
            EIGHT_TOGETHER8,
            EIGHT_AFTER_FIRST8,
            EIGHT_SPREAD_A8,
            EIGHT_SPREAD_B8,
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in EIGHT_WORDS)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in EIGHT_WORDS), 8
            )

    def test_nine_intervening_fragments_join_to_token(self):
        parts = NINE_TOGETHER8.split("\n")
        joined = "".join(p for p in parts if p not in NINE_WORDS)
        self.assertEqual(joined, TOKEN)
        self.assertEqual(
            sum(1 for p in parts if p in NINE_WORDS), 9
        )


class TestRedactFixR32EightIntervening(unittest.TestCase):
    """Ruling 1794: a wrapping carrying eight intervening
    entries in total, and nine in the together form."""

    def test_eight_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [EIGHT_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        for word in EIGHT_WORDS:
            self.assertIn(word, outcome["redacted_material"])

    def test_eight_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, EIGHT_TOGETHER8], 7, FRAGMENTS8
        )
        self.assertIn("eighth", outcome["redacted_material"])

    def test_eight_after_first_redacted_whole_head_included(self):
        outcome = _assert_append(
            self, [EIGHT_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_spread_two_one_one_one_three_redacted_whole(self):
        outcome = _assert_append(
            self, [EIGHT_SPREAD_A8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eighth", outcome["redacted_material"])

    def test_spread_four_after_first_four_after_fourth_whole(self):
        outcome = _assert_append(
            self, [EIGHT_SPREAD_B8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eighth", outcome["redacted_material"])

    def test_semicolon_eight_together_redacted_whole(self):
        _assert_append(
            self, [SEMI_EIGHT_TOGETHER8, TOKEN], 7, SEMI_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_nine_together_redacted_whole(self):
        outcome = _assert_append(
            self, [NINE_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("ninth", outcome["redacted_material"])

    def test_decoded_spans_cover_every_eight_fragment(self):
        module = require("ontoloop.redact")
        text = EIGHT_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        for word in EIGHT_WORDS:
            self.assertNotIn(word, covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [EIGHT_TOGETHER8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR32Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_seven_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [SEVEN_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("seventh", outcome["redacted_material"])

    def test_six_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [SIX_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("sixth", outcome["redacted_material"])

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_eight_each_gap_decided_whole_standing(self):
        outcome = _assert_append(
            self, [EIGHT_EACH_GAP8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("again", outcome["redacted_material"])

    def test_eight_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, EIGHT_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], EIGHT_TOGETHER8)

    def test_eight_after_first_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, EIGHT_AFTER_FIRST8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], EIGHT_AFTER_FIRST8
        )

    def test_semicolon_eight_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_EIGHT_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], SEMI_EIGHT_TOGETHER8
        )

    def test_eight_together_beside_plain_assignment(self):
        _assert_append(
            self, [EIGHT_TOGETHER8, ASSIGNMENT], 1, FRAGMENTS8
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
