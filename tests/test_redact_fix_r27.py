"""Fix round 27 tests for Region 4: redacting append path.

Written first for rulings 1290, 1291, and 1292 of the
Round 27 triage. Ruling 1290, identity S15-R27-CR-1,
Medium: a copy of a definite encoded token whose
decoration stands beyond the landed bound of the Fix
round 26 cure at ruling 1199, five characters at one
edge beside any character at the other edge, any edge
of six or more characters, or nine or more edge
characters in total, standing beside a clean copy of
the same token, reaches the journal unredacted and
uncounted. Ruling 1291, identity S15-R27-CR-2,
Medium: an encoded token wrapped at 8 characters
whose fragments carry punctuation dress, comma
separated fragments, a bracketed list form, or a
quotation around the whole wrapping, standing beside
a clean copy, reaches the journal in every fragment.
Ruling 1292, identity S15-R27-CR-3, Low, counted
severally: an encoded token wrapped at 8 characters
whose fragments stand interrupted by a benign
alphabet word, standing beside a clean copy, stands
redacted in the fragments before the interruption
only, and the fragments after the interruption reach
the journal, decoding to the tail of the definite
value. Ruling 1293 stands NOT A DEFECT as a cost
measurement and carries no pin here. The standing
poles pin the forms that decide correctly before the
cure: the charged forms of rulings 1199 to 1201, the
clean token alone, two clean copies, and the
detection boundary forms standing alone.
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
WRAPPED12 = _wrap(TOKEN, 12)
FRAGMENTS12 = WRAPPED12.split("\n")
LONG_WRAPPED8 = _wrap(LONG_TOKEN, 8)
LONG_FRAGMENTS8 = LONG_WRAPPED8.split("\n")
LONG_WRAPPED16 = _wrap(LONG_TOKEN, 16)
LONG_FRAGMENTS16 = LONG_WRAPPED16.split("\n")
GOLDEN_ANCHOR = (
    "c91e73191bb5ef6cd2db017b12e101a5a1f12d5be8e7b4e430e7604e4d6038ee"
)

DRESSED_COMMA_NEWLINE = ",\n".join(FRAGMENTS8)
DRESSED_COMMA_SPACE = ", ".join(FRAGMENTS8)
DRESSED_BRACKETED = "[" + ", ".join(FRAGMENTS8) + "]"
DRESSED_QUOTED = '"' + WRAPPED8 + '"'
DRESSED_COMMA12 = ", ".join(FRAGMENTS12)
INTERRUPTED8 = "\n".join(
    FRAGMENTS8[:3] + ["hello"] + FRAGMENTS8[3:]
)
INTERRUPTED_LONG8 = "\n".join(
    LONG_FRAGMENTS8[:8] + ["hello"] + LONG_FRAGMENTS8[8:]
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


class TestRedactFixR27Setup(unittest.TestCase):
    """The probed tokens and dressed forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_dressed_fragments_join_to_token_after_strip(self):
        alphabet = set(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvwxyz0123456789+/="
        )
        for dressed in (
            DRESSED_COMMA_NEWLINE,
            DRESSED_COMMA_SPACE,
            DRESSED_BRACKETED,
            DRESSED_QUOTED,
        ):
            cores = []
            for raw in dressed.split():
                core = raw.strip("".join(
                    chr(c) for c in range(33, 127)
                    if chr(c) not in alphabet
                ))
                cores.append(core)
            self.assertEqual("".join(cores), TOKEN)

    def test_interrupted_fragments_join_to_token(self):
        parts = INTERRUPTED8.split("\n")
        self.assertEqual(parts[3], "hello")
        joined = "".join(p for p in parts if p != "hello")
        self.assertEqual(joined, TOKEN)
        self.assertEqual(len(FRAGMENTS8), 6)

    def test_long_interrupted_fragments_join_to_long_token(self):
        parts = INTERRUPTED_LONG8.split("\n")
        self.assertEqual(parts[8], "hello")
        joined = "".join(p for p in parts if p != "hello")
        self.assertEqual(joined, LONG_TOKEN)
        self.assertEqual(len(LONG_FRAGMENTS8), 16)


class TestRedactFixR27DecoratedBeyondBound(unittest.TestCase):
    """Ruling 1290: the decorated copy beyond the landed bound."""

    def _check(self, decorated, token=TOKEN):
        _assert_append(self, [decorated, token], 2, [], token)

    def test_fused_value_prefix_copy_redacted_beside_clean(self):
        self._check("value=" + TOKEN)

    def test_fused_value_prefix_trailing_comma_redacted(self):
        self._check("value=" + TOKEN + ",")

    def test_five_prefix_trailing_comma_redacted(self):
        self._check("xxxxx" + TOKEN + ",")

    def test_five_prefix_closing_paren_redacted(self):
        self._check("xxxxx" + TOKEN + ")")

    def test_five_brackets_quote_trail_redacted(self):
        self._check("[[[[[" + TOKEN + '"')

    def test_hex_five_lead_one_trail_redacted(self):
        self._check("(((((" + HEX_TOKEN + ")", HEX_TOKEN)

    def test_hex_six_fused_prefix_redacted(self):
        self._check("value=" + HEX_TOKEN, HEX_TOKEN)

    def test_hex_four_lead_five_trail_redacted(self):
        self._check("((((" + HEX_TOKEN + ")))))", HEX_TOKEN)

    def test_clean_first_beyond_bound_copy_redacted(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module,
            [TOKEN, "(((((" + TOKEN + ")"],
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        self.assertNotIn(TOKEN, outcome["redacted_material"])
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))

    def test_decoded_spans_cover_beyond_bound_and_clean(self):
        module = require("ontoloop.redact")
        text = "(((((" + TOKEN + ")\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        token_starts = [
            start for start, end, layer, cls in spans
            if text[start:end] == TOKEN
        ]
        self.assertEqual(len(token_starts), 2)

    def test_golden_store_canonical_bytes_carry_no_copy(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, ["(((((( " .replace(" ", "") + TOKEN + ")", TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        self.assertNotIn(
            TOKEN.encode("utf-8"), store["records"][-1]["canonical_bytes"]
        )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


def _make_paren_test(lead, trail):
    def _test(self):
        decorated = "(" * lead + TOKEN + ")" * trail
        _assert_append(self, [decorated, TOKEN], 2, [], TOKEN)
    return _test


_PAREN_FORMS = []
for _lead in range(0, 9):
    for _trail in range(0, 9):
        _inside = (
            (_lead <= 4 and _trail <= 4)
            or (_lead == 5 and _trail == 0)
            or (_lead == 0 and _trail == 5)
        )
        if not _inside:
            _PAREN_FORMS.append((_lead, _trail))

for _lead, _trail in _PAREN_FORMS:
    setattr(
        TestRedactFixR27DecoratedBeyondBound,
        "test_paren_lead%d_trail%d_redacted" % (_lead, _trail),
        _make_paren_test(_lead, _trail),
    )


class TestRedactFixR27DressedWrapped(unittest.TestCase):
    """Ruling 1291: the wrapped token in punctuation dress."""

    def test_comma_newline_dress_redacted_whole(self):
        _assert_append(
            self, [DRESSED_COMMA_NEWLINE, TOKEN], 7, FRAGMENTS8
        )

    def test_comma_space_dress_redacted_whole(self):
        _assert_append(
            self, [DRESSED_COMMA_SPACE, TOKEN], 7, FRAGMENTS8
        )

    def test_bracketed_list_dress_redacted_whole(self):
        _assert_append(
            self, [DRESSED_BRACKETED, TOKEN], 7, FRAGMENTS8
        )

    def test_quoted_wrapping_dress_redacted_whole(self):
        _assert_append(
            self, [DRESSED_QUOTED, TOKEN], 7, FRAGMENTS8
        )

    def test_comma_space_dress_at_12_redacted_whole(self):
        _assert_append(
            self, [DRESSED_COMMA12, TOKEN], 5, FRAGMENTS12
        )

    def test_clean_first_dressed_wrapping_redacted_whole(self):
        _assert_append(
            self, [TOKEN, DRESSED_COMMA_SPACE], 7, FRAGMENTS8
        )

    def test_decoded_spans_cover_every_dressed_fragment(self):
        module = require("ontoloop.redact")
        text = DRESSED_COMMA_SPACE + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
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
            module, store_module, [DRESSED_BRACKETED, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR27InterruptedWrapped(unittest.TestCase):
    """Ruling 1292: the wrapped token interrupted by a benign word."""

    def test_interrupted_at_8_redacted_whole_word_stands(self):
        outcome = _assert_append(
            self, [INTERRUPTED8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_interrupted_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, INTERRUPTED8], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_interrupted_long_at_8_redacted_whole(self):
        outcome = _assert_append(
            self, [INTERRUPTED_LONG8, LONG_TOKEN], 17, LONG_FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_decoded_spans_cover_every_interrupted_fragment(self):
        module = require("ontoloop.redact")
        text = INTERRUPTED8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("hello", covered)


class TestRedactFixR27Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_ruling_1199_at_bound_form_still_redacts(self):
        _assert_append(
            self, ["(((" + TOKEN + ")))", TOKEN], 2, [], TOKEN
        )

    def test_ruling_1199_four_at_each_edge_still_redacts(self):
        _assert_append(
            self, ["((((" + TOKEN + "))))", TOKEN], 2, [], TOKEN
        )

    def test_ruling_1200_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_ruling_1201_long_wrapped_at_16_still_redacts(self):
        _assert_append(
            self, [LONG_WRAPPED16, LONG_TOKEN], 9, LONG_FRAGMENTS16
        )

    def test_decorated_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        material = "(" + TOKEN + ")"
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], material)

    def test_beyond_bound_decorated_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        material = "(((((" + TOKEN + ")"
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], material)

    def test_wrapped_at_8_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, WRAPPED8)
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], WRAPPED8)

    def test_dressed_wrapped_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, DRESSED_COMMA_SPACE
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], DRESSED_COMMA_SPACE)

    def test_interrupted_wrapped_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, INTERRUPTED8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], INTERRUPTED8)

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
