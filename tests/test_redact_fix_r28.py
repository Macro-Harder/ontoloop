"""Fix round 28 tests for Region 4: redacting append path.

Written first for rulings 1383 to 1387 of the Round 28
triage. Ruling 1383, identity S15-R28-CAPRED-1, Medium:
an encoded token wrapped at 8 characters whose fragments
stand separated by a separator token standing alone
between each pair of fragments, a comma, a semicolon, or
a dash standing as its own whitespace separated token,
standing beside a clean copy of the same token, reaches
the journal in every fragment. Ruling 1384, identity
S15-R28-CAPRED-2, Medium: an encoded token wrapped at 8
characters whose fragments stand interrupted by a benign
alphabet word standing after exactly one fragment,
standing beside a clean copy, reaches the journal in
every fragment. Ruling 1385, identity S15-R28-CAPRED-4,
Medium: an encoded token wrapped at 8 characters whose
fragments each carry a comma in the fragment interior,
standing beside a clean copy, reaches the journal in
every fragment. Ruling 1386, identity S15-R28-CAPRED-3,
Low, counted severally: a wrapped token interrupted at
two intervening tokens, two benign words standing
together after the third fragment, or a second
intervening word standing later in the same wrapping,
stands redacted in its leading fragments only, and the
fragments after the interruption reach the journal,
decoding to the tail of the definite value. Ruling 1387,
identity S15-R28-CAPRED-5, Medium: a single copy of the
definite encoded token carrying interior commas, two
commas standing inside the one token, standing beside a
clean copy of the same token, reaches the journal whole
in its comma form. The standing poles pin the forms that
decide correctly before the cure: the charged forms of
rulings 1199 to 1201 and 1290 to 1292, the clean token
alone, two clean copies, and the detection boundary forms standing
alone.
"""

import base64
import unittest

from tests.harness import require

PLAIN = b"password = " + b"a" * 20
TOKEN = base64.b64encode(PLAIN).decode("ascii")
HEX_TOKEN = PLAIN.hex()
ASSIGNMENT = "password = PlainValue999"
LONG_PLAIN = b"password = " + b"b" * 80
LONG_TOKEN = base64.b64encode(LONG_PLAIN).decode("ascii")


def _wrap(token, width):
    return "\n".join(
        token[start:start + width]
        for start in range(0, len(token), width)
    )


WRAPPED8 = _wrap(TOKEN, 8)
FRAGMENTS8 = WRAPPED8.split("\n")
LONG_WRAPPED8 = _wrap(LONG_TOKEN, 8)
LONG_FRAGMENTS8 = LONG_WRAPPED8.split("\n")
LONG_WRAPPED16 = _wrap(LONG_TOKEN, 16)
LONG_FRAGMENTS16 = LONG_WRAPPED16.split("\n")
GOLDEN_ANCHOR = (
    "c91e73191bb5ef6cd2db017b12e101a5a1f12d5be8e7b4e430e7604e4d6038ee"
)

SEPARATED_COMMA = " , ".join(FRAGMENTS8)
SEPARATED_COMMA_LINES = "\n,\n".join(FRAGMENTS8)
SEPARATED_SEMICOLON = " ; ".join(FRAGMENTS8)
SEPARATED_DASH = " - ".join(FRAGMENTS8)
INTERRUPTED_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:]
)
INTERRUPTED_FIRST_LONG8 = "\n".join(
    LONG_FRAGMENTS8[:1] + ["hello"] + LONG_FRAGMENTS8[1:]
)
INTERRUPTED_THIRD8 = "\n".join(
    FRAGMENTS8[:3] + ["hello"] + FRAGMENTS8[3:]
)


def _interior_fragment(fragment):
    if len(fragment) > 4:
        return fragment[:4] + "," + fragment[4:]
    return fragment[:2] + "," + fragment[2:]


INTERIOR_FRAGMENTS8 = [_interior_fragment(f) for f in FRAGMENTS8]
INTERIOR_WRAPPED8 = "\n".join(INTERIOR_FRAGMENTS8)
DOUBLE_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + ["hello", "world"] + FRAGMENTS8[3:]
)
DOUBLE_LATER8 = "\n".join(
    FRAGMENTS8[:3] + ["hello"] + FRAGMENTS8[3:5]
    + ["world"] + FRAGMENTS8[5:]
)
INTERIOR_TOKEN_TWO = TOKEN[:14] + "," + TOKEN[14:30] + "," + TOKEN[30:]
INTERIOR_TOKEN_ONE = TOKEN[:22] + "," + TOKEN[22:]
INTERIOR_TOKEN_ONE_TAIL = INTERIOR_TOKEN_ONE[20:]
INTERIOR_HEX_TWO = (
    HEX_TOKEN[:20] + "," + HEX_TOKEN[20:40] + "," + HEX_TOKEN[40:]
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


class TestRedactFixR28Setup(unittest.TestCase):
    """The probed tokens and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_separated_fragments_join_to_token(self):
        parts = SEPARATED_COMMA.split()
        fragments = [p for p in parts if p != ","]
        self.assertEqual("".join(fragments), TOKEN)
        self.assertEqual(len(FRAGMENTS8), 6)

    def test_interrupted_first_fragments_join_to_token(self):
        parts = INTERRUPTED_FIRST8.split("\n")
        self.assertEqual(parts[1], "hello")
        joined = "".join(p for p in parts if p != "hello")
        self.assertEqual(joined, TOKEN)

    def test_interior_fragments_join_to_token_after_strip(self):
        joined = "".join(
            fragment.replace(",", "")
            for fragment in INTERIOR_FRAGMENTS8
        )
        self.assertEqual(joined, TOKEN)
        for fragment in INTERIOR_FRAGMENTS8:
            self.assertIn(",", fragment[1:-1] + fragment[-1:])

    def test_double_interrupted_fragments_join_to_token(self):
        for form in (DOUBLE_TOGETHER8, DOUBLE_LATER8):
            parts = form.split("\n")
            joined = "".join(
                p for p in parts if p not in ("hello", "world")
            )
            self.assertEqual(joined, TOKEN)

    def test_interior_token_restored_after_strip(self):
        self.assertEqual(INTERIOR_TOKEN_TWO.replace(",", ""), TOKEN)
        self.assertEqual(INTERIOR_TOKEN_ONE.replace(",", ""), TOKEN)
        self.assertEqual(INTERIOR_HEX_TWO.replace(",", ""), HEX_TOKEN)


class TestRedactFixR28SeparatedWrapped(unittest.TestCase):
    """Ruling 1383: fragments separated by a separator token."""

    def test_comma_token_separated_redacted_whole(self):
        _assert_append(
            self, [SEPARATED_COMMA, TOKEN], 7, FRAGMENTS8
        )

    def test_comma_token_on_own_line_redacted_whole(self):
        _assert_append(
            self, [SEPARATED_COMMA_LINES, TOKEN], 7, FRAGMENTS8
        )

    def test_semicolon_token_separated_redacted_whole(self):
        _assert_append(
            self, [SEPARATED_SEMICOLON, TOKEN], 7, FRAGMENTS8
        )

    def test_dash_token_separated_redacted_whole(self):
        _assert_append(
            self, [SEPARATED_DASH, TOKEN], 7, FRAGMENTS8
        )

    def test_clean_first_separated_redacted_whole(self):
        _assert_append(
            self, [TOKEN, SEPARATED_COMMA], 7, FRAGMENTS8
        )

    def test_decoded_spans_cover_every_separated_fragment(self):
        module = require("ontoloop.redact")
        text = SEPARATED_COMMA + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn(",", covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [SEPARATED_SEMICOLON, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR28InterruptedAfterOne(unittest.TestCase):
    """Ruling 1384: a wrapping interrupted after one fragment."""

    def test_interrupted_after_one_redacted_whole_word_stands(self):
        outcome = _assert_append(
            self, [INTERRUPTED_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_interrupted_after_one_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, INTERRUPTED_FIRST8], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_interrupted_after_one_long_redacted_whole(self):
        outcome = _assert_append(
            self, [INTERRUPTED_FIRST_LONG8, LONG_TOKEN],
            17, LONG_FRAGMENTS8,
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_decoded_spans_cover_every_fragment_after_one(self):
        module = require("ontoloop.redact")
        text = INTERRUPTED_FIRST8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("hello", covered)


class TestRedactFixR28InteriorFragments(unittest.TestCase):
    """Ruling 1385: fragments carrying a comma in the interior."""

    def test_interior_fragments_redacted_whole(self):
        _assert_append(
            self, [INTERIOR_WRAPPED8, TOKEN], 7, INTERIOR_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_interior_fragments_clean_first_redacted_whole(self):
        _assert_append(
            self, [TOKEN, INTERIOR_WRAPPED8], 7, INTERIOR_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_decoded_spans_cover_every_interior_fragment(self):
        module = require("ontoloop.redact")
        text = INTERIOR_WRAPPED8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in INTERIOR_FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [INTERIOR_WRAPPED8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in INTERIOR_FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR28DoubleInterrupted(unittest.TestCase):
    """Ruling 1386: a wrapping interrupted at two tokens."""

    def test_two_words_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [DOUBLE_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])
        self.assertIn("world", outcome["redacted_material"])

    def test_second_word_later_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [DOUBLE_LATER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])
        self.assertIn("world", outcome["redacted_material"])

    def test_two_words_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, DOUBLE_TOGETHER8], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])
        self.assertIn("world", outcome["redacted_material"])

    def test_decoded_spans_cover_every_doubly_interrupted_fragment(
        self,
    ):
        module = require("ontoloop.redact")
        text = DOUBLE_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("hello", covered)
        self.assertNotIn("world", covered)


class TestRedactFixR28InteriorSingleToken(unittest.TestCase):
    """Ruling 1387: a single token carrying interior commas."""

    def test_two_interior_commas_redacted_beside_clean(self):
        _assert_append(
            self, [INTERIOR_TOKEN_TWO, TOKEN], 2,
            [INTERIOR_TOKEN_TWO], token_absent=TOKEN,
        )

    def test_two_interior_commas_clean_first_redacted(self):
        _assert_append(
            self, [TOKEN, INTERIOR_TOKEN_TWO], 2,
            [INTERIOR_TOKEN_TWO], token_absent=TOKEN,
        )

    def test_one_interior_comma_redacted_whole_beside_clean(self):
        _assert_append(
            self, [INTERIOR_TOKEN_ONE, TOKEN], 2,
            [INTERIOR_TOKEN_ONE_TAIL], token_absent=TOKEN,
        )

    def test_hex_two_interior_commas_redacted_beside_clean(self):
        _assert_append(
            self, [INTERIOR_HEX_TWO, HEX_TOKEN], 2,
            [INTERIOR_HEX_TWO], token_absent=HEX_TOKEN,
        )

    def test_decoded_spans_cover_interior_token_whole(self):
        module = require("ontoloop.redact")
        text = INTERIOR_TOKEN_TWO + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        self.assertIn(INTERIOR_TOKEN_TWO, covered)
        self.assertIn(TOKEN, covered)

    def test_golden_store_canonical_bytes_carry_no_interior_token(
        self,
    ):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [INTERIOR_TOKEN_TWO, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        self.assertNotIn(
            INTERIOR_TOKEN_TWO.encode("utf-8"),
            store["records"][-1]["canonical_bytes"],
        )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR28Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_ruling_1290_beyond_bound_form_still_redacts(self):
        _assert_append(
            self, ["(((((" + TOKEN + ")", TOKEN], 2, [], TOKEN
        )

    def test_ruling_1291_dressed_wrapping_still_redacts(self):
        dressed = ", ".join(FRAGMENTS8)
        _assert_append(self, [dressed, TOKEN], 7, FRAGMENTS8)

    def test_ruling_1292_interrupted_at_third_still_redacts(self):
        outcome = _assert_append(
            self, [INTERRUPTED_THIRD8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_ruling_1200_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_ruling_1201_long_wrapped_at_16_still_redacts(self):
        _assert_append(
            self, [LONG_WRAPPED16, LONG_TOKEN], 9, LONG_FRAGMENTS16
        )

    def test_separated_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEPARATED_COMMA
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], SEPARATED_COMMA)

    def test_interrupted_after_one_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, INTERRUPTED_FIRST8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], INTERRUPTED_FIRST8
        )

    def test_interior_fragments_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, INTERIOR_WRAPPED8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], INTERIOR_WRAPPED8
        )

    def test_double_interrupted_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, DOUBLE_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], DOUBLE_TOGETHER8
        )

    def test_interior_token_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, INTERIOR_TOKEN_TWO
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], INTERIOR_TOKEN_TWO
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

    def test_benign_dressed_fragments_beside_clean_stand(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        benign = "abcd1234, efgh5678, ijkl9012"
        store, before, outcome = _append(
            module, store_module, [TOKEN, benign]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertIn(benign, outcome["redacted_material"])

    def test_benign_separated_fragments_beside_clean_stand(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        benign = "abcd1234 , efgh5678 , ijkl9012"
        store, before, outcome = _append(
            module, store_module, [TOKEN, benign]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertIn(benign, outcome["redacted_material"])

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
