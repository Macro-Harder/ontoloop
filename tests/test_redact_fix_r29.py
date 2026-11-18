"""Fix round 29 tests for Region 4: redacting append path.

Written first for rulings 1479 to 1482 of the Round 29
triage. Ruling 1479, identity S15-R29-CAPRED-1, Medium:
an encoded token wrapped at 8 characters whose fragments
each carry an interior character other than a comma, a
semicolon, a dash, a full stop, or an underscore,
standing beside a clean copy of the same token, reaches
the journal in every fragment. Ruling 1480, identity
S15-R29-CAPRED-2, Medium: a single copy of the definite
encoded token carrying interior characters other than
commas, two semicolons, two dashes, or, in the hex form,
two semicolons standing inside the one token, standing
beside a clean copy, reaches the journal whole in its
dressed form, and the same token carrying one interior
semicolon stands redacted in its head only, a tail
segment surviving. Ruling 1481, identity
S15-R29-CAPRED-3, Medium: a single copy of the definite
encoded token carrying a run of interior commas, two
commas standing together inside the one token, or a
single comma beside a double comma, or a comma and
semicolon pair, standing beside a clean copy, reaches
the journal whole in its comma run form. Ruling 1482,
identity S15-R29-CAPRED-4, Low: a wrapped token carrying
three intervening entries in total, three benign words
standing together after the third fragment, words
standing after the first, third, and fifth fragments,
two words after the first fragment and a third word
later, or three words standing after the first fragment,
stands redacted in its reached fragments only, and the
fragment positions standing past the point the two entry
total of the landed joining bound is spent reach the
journal. The standing poles pin the forms that decide
correctly before the cure: the charged forms of rulings
1383 to 1387, the clean token alone, two clean copies,
and the detection boundary forms standing alone.
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
LONG_WRAPPED16 = _wrap(LONG_TOKEN, 16)
LONG_FRAGMENTS16 = LONG_WRAPPED16.split("\n")
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
DASH_FRAGMENTS8 = _interior_fragments("-")
DASH_WRAPPED8 = "\n".join(DASH_FRAGMENTS8)
DOT_FRAGMENTS8 = _interior_fragments(".")
DOT_WRAPPED8 = "\n".join(DOT_FRAGMENTS8)
UNDERSCORE_FRAGMENTS8 = _interior_fragments("_")
UNDERSCORE_WRAPPED8 = "\n".join(UNDERSCORE_FRAGMENTS8)
COMMA_FRAGMENTS8 = _interior_fragments(",")
COMMA_WRAPPED8 = "\n".join(COMMA_FRAGMENTS8)
DOUBLE_COMMA_FRAGMENTS8 = _interior_fragments(",,")
DOUBLE_COMMA_WRAPPED8 = "\n".join(DOUBLE_COMMA_FRAGMENTS8)

SEMI_TOKEN_TWO = TOKEN[:14] + ";" + TOKEN[14:30] + ";" + TOKEN[30:]
SEMI_TOKEN_ONE = TOKEN[:22] + ";" + TOKEN[22:]
SEMI_TOKEN_ONE_TAIL = TOKEN[20:22] + ";" + TOKEN[22:]
DASH_TOKEN_TWO = TOKEN[:14] + "-" + TOKEN[14:30] + "-" + TOKEN[30:]
SEMI_HEX_TWO = (
    HEX_TOKEN[:20] + ";" + HEX_TOKEN[20:40] + ";" + HEX_TOKEN[40:]
)
DOUBLE_COMMA_TOKEN = TOKEN[:14] + ",," + TOKEN[14:]
SINGLE_AND_DOUBLE_TOKEN = (
    TOKEN[:14] + "," + TOKEN[14:30] + ",," + TOKEN[30:]
)
COMMA_SEMI_TOKEN = TOKEN[:14] + ",;" + TOKEN[14:]
COMMA_TOKEN_TWO = TOKEN[:14] + "," + TOKEN[14:30] + "," + TOKEN[30:]

TRIPLE_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + ["hello", "world", "again"] + FRAGMENTS8[3:]
)
TRIPLE_SPREAD8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:3]
    + ["world"] + FRAGMENTS8[3:5] + ["again"] + FRAGMENTS8[5:]
)
TRIPLE_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world", "again"] + FRAGMENTS8[1:]
)
TRIPLE_TWO_AND_ONE8 = "\n".join(
    FRAGMENTS8[:1] + ["hello", "world"] + FRAGMENTS8[1:4]
    + ["again"] + FRAGMENTS8[4:]
)
DOUBLE_TOGETHER8 = "\n".join(
    FRAGMENTS8[:3] + ["hello", "world"] + FRAGMENTS8[3:]
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


class TestRedactFixR29Setup(unittest.TestCase):
    """The probed tokens and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_interior_char_fragments_join_after_strip(self):
        for char, dressed in (
            (";", SEMI_FRAGMENTS8),
            ("-", DASH_FRAGMENTS8),
            (".", DOT_FRAGMENTS8),
            ("_", UNDERSCORE_FRAGMENTS8),
        ):
            joined = "".join(
                fragment.replace(char, "") for fragment in dressed
            )
            self.assertEqual(joined, TOKEN)
            self.assertEqual(len(dressed), 6)

    def test_interior_single_tokens_restored_after_strip(self):
        self.assertEqual(SEMI_TOKEN_TWO.replace(";", ""), TOKEN)
        self.assertEqual(SEMI_TOKEN_ONE.replace(";", ""), TOKEN)
        self.assertEqual(SEMI_TOKEN_ONE[20:], SEMI_TOKEN_ONE_TAIL)
        self.assertEqual(DASH_TOKEN_TWO.replace("-", ""), TOKEN)
        self.assertEqual(SEMI_HEX_TWO.replace(";", ""), HEX_TOKEN)

    def test_comma_run_tokens_restored_after_strip(self):
        self.assertEqual(DOUBLE_COMMA_TOKEN.replace(",", ""), TOKEN)
        self.assertEqual(
            SINGLE_AND_DOUBLE_TOKEN.replace(",", ""), TOKEN
        )
        stripped = COMMA_SEMI_TOKEN.replace(",", "").replace(";", "")
        self.assertEqual(stripped, TOKEN)

    def test_triple_intervening_fragments_join_to_token(self):
        words = ("hello", "world", "again")
        for form in (
            TRIPLE_TOGETHER8,
            TRIPLE_SPREAD8,
            TRIPLE_AFTER_FIRST8,
            TRIPLE_TWO_AND_ONE8,
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in words)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in words), 3
            )


class TestRedactFixR29InteriorCharFragments(unittest.TestCase):
    """Ruling 1479: fragments carrying an interior character
    other than a comma."""

    def test_semicolon_fragments_redacted_whole(self):
        _assert_append(
            self, [SEMI_WRAPPED8, TOKEN], 7, SEMI_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_dash_fragments_redacted_whole(self):
        _assert_append(
            self, [DASH_WRAPPED8, TOKEN], 7, DASH_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_full_stop_fragments_redacted_whole(self):
        _assert_append(
            self, [DOT_WRAPPED8, TOKEN], 7, DOT_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_underscore_fragments_redacted_whole(self):
        _assert_append(
            self, [UNDERSCORE_WRAPPED8, TOKEN], 7,
            UNDERSCORE_FRAGMENTS8, token_absent=TOKEN,
        )

    def test_semicolon_fragments_clean_first_redacted_whole(self):
        _assert_append(
            self, [TOKEN, SEMI_WRAPPED8], 7, SEMI_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_decoded_spans_cover_every_semicolon_fragment(self):
        module = require("ontoloop.redact")
        text = SEMI_WRAPPED8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in SEMI_FRAGMENTS8:
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
            module, store_module, [SEMI_WRAPPED8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in SEMI_FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR29InteriorCharSingleToken(unittest.TestCase):
    """Ruling 1480: a single token carrying interior characters
    other than commas."""

    def test_two_semicolons_redacted_beside_clean(self):
        _assert_append(
            self, [SEMI_TOKEN_TWO, TOKEN], 2,
            [SEMI_TOKEN_TWO], token_absent=TOKEN,
        )

    def test_two_semicolons_clean_first_redacted(self):
        _assert_append(
            self, [TOKEN, SEMI_TOKEN_TWO], 2,
            [SEMI_TOKEN_TWO], token_absent=TOKEN,
        )

    def test_two_dashes_redacted_beside_clean(self):
        _assert_append(
            self, [DASH_TOKEN_TWO, TOKEN], 2,
            [DASH_TOKEN_TWO], token_absent=TOKEN,
        )

    def test_hex_two_semicolons_redacted_beside_clean(self):
        _assert_append(
            self, [SEMI_HEX_TWO, HEX_TOKEN], 2,
            [SEMI_HEX_TWO], token_absent=HEX_TOKEN,
        )

    def test_one_semicolon_redacted_whole_beside_clean(self):
        _assert_append(
            self, [SEMI_TOKEN_ONE, TOKEN], 2,
            [SEMI_TOKEN_ONE_TAIL], token_absent=TOKEN,
        )

    def test_decoded_spans_cover_semicolon_token_whole(self):
        module = require("ontoloop.redact")
        text = SEMI_TOKEN_TWO + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        self.assertIn(SEMI_TOKEN_TWO, covered)
        self.assertIn(TOKEN, covered)

    def test_golden_store_canonical_bytes_carry_no_dressed_token(
        self,
    ):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [SEMI_TOKEN_TWO, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        self.assertNotIn(
            SEMI_TOKEN_TWO.encode("utf-8"),
            store["records"][-1]["canonical_bytes"],
        )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR29CommaRunSingleToken(unittest.TestCase):
    """Ruling 1481: a single token carrying a run of interior
    commas."""

    def test_double_comma_redacted_beside_clean(self):
        _assert_append(
            self, [DOUBLE_COMMA_TOKEN, TOKEN], 2,
            [DOUBLE_COMMA_TOKEN], token_absent=TOKEN,
        )

    def test_double_comma_clean_first_redacted(self):
        _assert_append(
            self, [TOKEN, DOUBLE_COMMA_TOKEN], 2,
            [DOUBLE_COMMA_TOKEN], token_absent=TOKEN,
        )

    def test_single_and_double_comma_redacted_beside_clean(self):
        _assert_append(
            self, [SINGLE_AND_DOUBLE_TOKEN, TOKEN], 2,
            [SINGLE_AND_DOUBLE_TOKEN], token_absent=TOKEN,
        )

    def test_comma_semicolon_pair_redacted_beside_clean(self):
        _assert_append(
            self, [COMMA_SEMI_TOKEN, TOKEN], 2,
            [COMMA_SEMI_TOKEN], token_absent=TOKEN,
        )

    def test_decoded_spans_cover_double_comma_token_whole(self):
        module = require("ontoloop.redact")
        text = DOUBLE_COMMA_TOKEN + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        self.assertIn(DOUBLE_COMMA_TOKEN, covered)
        self.assertIn(TOKEN, covered)

    def test_golden_store_canonical_bytes_carry_no_comma_token(
        self,
    ):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [DOUBLE_COMMA_TOKEN, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        self.assertNotIn(
            DOUBLE_COMMA_TOKEN.encode("utf-8"),
            store["records"][-1]["canonical_bytes"],
        )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR29TripleIntervening(unittest.TestCase):
    """Ruling 1482: a wrapping carrying three intervening
    entries in total."""

    def test_three_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [TRIPLE_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])
        self.assertIn("world", outcome["redacted_material"])
        self.assertIn("again", outcome["redacted_material"])

    def test_three_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, TRIPLE_TOGETHER8], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_words_spread_after_first_third_fifth_redacted(self):
        outcome = _assert_append(
            self, [TRIPLE_SPREAD8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("world", outcome["redacted_material"])
        self.assertIn("again", outcome["redacted_material"])

    def test_three_words_after_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TRIPLE_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_two_after_first_and_one_later_redacted_whole(self):
        outcome = _assert_append(
            self, [TRIPLE_TWO_AND_ONE8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("again", outcome["redacted_material"])

    def test_decoded_spans_cover_every_triple_fragment(self):
        module = require("ontoloop.redact")
        text = TRIPLE_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("hello", covered)
        self.assertNotIn("world", covered)
        self.assertNotIn("again", covered)


class TestRedactFixR29Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_ruling_1383_separated_wrapping_still_redacts(self):
        separated = " , ".join(FRAGMENTS8)
        _assert_append(self, [separated, TOKEN], 7, FRAGMENTS8)

    def test_ruling_1384_interrupted_after_one_still_redacts(self):
        form = "\n".join(FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:])
        outcome = _assert_append(self, [form, TOKEN], 7, FRAGMENTS8)
        self.assertIn("hello", outcome["redacted_material"])

    def test_ruling_1385_interior_comma_fragments_still_redact(
        self,
    ):
        _assert_append(
            self, [COMMA_WRAPPED8, TOKEN], 7, COMMA_FRAGMENTS8,
            token_absent=TOKEN,
        )

    def test_ruling_1386_two_intervening_still_redacts(self):
        outcome = _assert_append(
            self, [DOUBLE_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])
        self.assertIn("world", outcome["redacted_material"])

    def test_ruling_1387_interior_commas_still_redact(self):
        _assert_append(
            self, [COMMA_TOKEN_TWO, TOKEN], 2,
            [COMMA_TOKEN_TWO], token_absent=TOKEN,
        )

    def test_fragment_double_comma_interior_still_redacts(self):
        _assert_append(
            self, [DOUBLE_COMMA_WRAPPED8, TOKEN], 7,
            DOUBLE_COMMA_FRAGMENTS8, token_absent=TOKEN,
        )

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_long_wrapped_at_16_still_redacts(self):
        _assert_append(
            self, [LONG_WRAPPED16, LONG_TOKEN], 9, LONG_FRAGMENTS16
        )

    def test_semicolon_fragments_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_WRAPPED8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], SEMI_WRAPPED8)

    def test_semicolon_token_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_TOKEN_TWO
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], SEMI_TOKEN_TWO)

    def test_double_comma_token_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, DOUBLE_COMMA_TOKEN
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], DOUBLE_COMMA_TOKEN
        )

    def test_triple_intervening_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, TRIPLE_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], TRIPLE_TOGETHER8
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
