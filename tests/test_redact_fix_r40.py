"""Fix round 40 tests for Region 7: redacting append path.

Written first for ruling 2900 of the Round 40 triage.
Ruling 2900, identity S15-R40-CAPRED-1, Low: on the
redacting append path, a definite token standing in
few fragments wrapped beside a clean copy stands
redacted in part only, the later fragments standing
in the redacted material and in the journal bytes at
every gap probed, because the consecutive joining of
_wrapped_token_spans takes a first fragment joined
with the cores of the first intervening entries where
that joined core decides definite, so the fragments
standing after the intervening entries stand reached
by no act and the append writes them whole. The
charged forms stand in the constructions the raising
paper states severally: the token in two fragments of
twenty two characters each beside a clean copy, with
ten, one hundred, seven hundred sixty six, seven
hundred sixty seven, and seven hundred sixty nine
single character intervening entries after the first
fragment, at hits_redacted 4 on the landed form with
the second fragment standing in each form; the same
ten entry form in clean first order; the token in
three fragments of fifteen, fifteen, and fourteen
characters with ten intervening entries after the
first fragment, the second and third fragments
standing, and with seven hundred sixty eight
intervening entries after the second fragment, the
third fragment standing; and the two fragment form
with two character intervening entries, the second
fragment standing. The direct span act forms stand
charged beside the append forms: on the direct act
the two fragment text at ten, at seven hundred sixty
six, and at seven hundred sixty nine intervening
entries carries spans at the first fragment and at
the cores of the first intervening entries, and the
second fragment carries no span in any form. The
standing poles pin the forms that decide correctly
before the cure: the two fragment wrapping with no
intervening entry beside a clean copy, the two
fragment forms with word length intervening entries,
the alone and beside plain assignment forms of the
construction standing in their detection boundary
forms, the bare six fragment wrapping beside a clean
copy, the clean token alone, and the plain assignment
and clean material forms. No form of this file grades
the capture ring position standing carried open and
ungraded at ruling 2745, in either direction: every
form of this file stands in the few fragment
construction of the finding itself, at the gaps the
raising paper names for that construction.
"""

import base64
import unittest

from tests.harness import require

PLAIN = b"password = " + b"a" * 20
TOKEN = base64.b64encode(PLAIN).decode("ascii")
ASSIGNMENT = "password = PlainValue999"

FRAGMENTS2 = [TOKEN[:22], TOKEN[22:]]
FRAGMENTS3 = [TOKEN[:15], TOKEN[15:30], TOKEN[30:]]


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


def _gap_form(fragments, after, entries):
    return "\n".join(
        fragments[:after] + list(entries) + fragments[after:]
    )


def _x(count):
    return ["x"] * count


F2_GAP10 = _gap_form(FRAGMENTS2, 1, _x(10))
F2_GAP100 = _gap_form(FRAGMENTS2, 1, _x(100))
F2_GAP766 = _gap_form(FRAGMENTS2, 1, _x(766))
F2_GAP767 = _gap_form(FRAGMENTS2, 1, _x(767))
F2_GAP769 = _gap_form(FRAGMENTS2, 1, _x(769))
F2_NO_GAP = "\n".join(FRAGMENTS2)
F2_GAP10_XX = _gap_form(FRAGMENTS2, 1, ["xx"] * 10)
F2_GAP10_HELLO = _gap_form(FRAGMENTS2, 1, ["hello"] * 10)
F2_GAP766_HELLO = _gap_form(FRAGMENTS2, 1, ["hello"] * 766)
F3_GAP10 = _gap_form(FRAGMENTS3, 1, _x(10))
F3_GAP768_AFTER_SECOND = _gap_form(FRAGMENTS3, 2, _x(768))


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


def _covered(test, text):
    module = require("ontoloop.redact")
    spans = module._decoded_spans(text, 4, "decoded definite hit")
    return [text[start:end] for start, end, layer, cls in spans]


class TestRedactFixR40Setup(unittest.TestCase):
    """The probed token and charged forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_two_fragment_forms_join_to_token(self):
        for form in (F2_GAP10, F2_GAP766, F2_GAP769, F2_GAP10_XX):
            parts = form.split("\n")
            joined = "".join(
                p for p in parts if p in FRAGMENTS2
            )
            self.assertEqual(joined, TOKEN)

    def test_three_fragment_forms_join_to_token(self):
        for form in (F3_GAP10, F3_GAP768_AFTER_SECOND):
            parts = form.split("\n")
            joined = "".join(
                p for p in parts if p in FRAGMENTS3
            )
            self.assertEqual(joined, TOKEN)


class TestRedactFixR40FewFragments(unittest.TestCase):
    """Ruling 2900: few fragments beside a clean copy."""

    def test_two_fragments_gap_ten_append_redacted_whole(self):
        outcome = _assert_append(
            self, [F2_GAP10, TOKEN], 3, FRAGMENTS2
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_two_fragments_gap_hundred_append_redacted_whole(self):
        outcome = _assert_append(
            self, [F2_GAP100, TOKEN], 3, FRAGMENTS2
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_two_fragments_gap_766_append_redacted_whole(self):
        outcome = _assert_append(
            self, [F2_GAP766, TOKEN], 3, FRAGMENTS2
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_two_fragments_gap_767_append_redacted_whole(self):
        outcome = _assert_append(
            self, [F2_GAP767, TOKEN], 3, FRAGMENTS2
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_two_fragments_gap_769_append_redacted_whole(self):
        outcome = _assert_append(
            self, [F2_GAP769, TOKEN], 3, FRAGMENTS2
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_two_fragments_gap_ten_clean_first_append_whole(self):
        outcome = _assert_append(
            self, [TOKEN, F2_GAP10], 3, FRAGMENTS2
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_two_fragments_gap_ten_spans_cover_every_fragment(self):
        covered = _covered(self, F2_GAP10 + "\n" + TOKEN)
        for fragment in FRAGMENTS2:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_two_fragments_gap_766_spans_cover_every_fragment(self):
        covered = _covered(self, F2_GAP766 + "\n" + TOKEN)
        for fragment in FRAGMENTS2:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_two_fragments_gap_769_spans_cover_every_fragment(self):
        covered = _covered(self, F2_GAP769 + "\n" + TOKEN)
        for fragment in FRAGMENTS2:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_three_fragments_gap_ten_append_redacted_whole(self):
        outcome = _assert_append(
            self, [F3_GAP10, TOKEN], 4, FRAGMENTS3
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_three_fragments_gap_768_after_second_append_whole(self):
        outcome = _assert_append(
            self, [F3_GAP768_AFTER_SECOND, TOKEN], 4, FRAGMENTS3
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_two_fragments_two_char_entries_append_whole(self):
        outcome = _assert_append(
            self, [F2_GAP10_XX, TOKEN], 3, FRAGMENTS2
        )
        self.assertIn("xx", outcome["redacted_material"])

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [F2_GAP10, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 3)
        for fragment in FRAGMENTS2:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR40Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_two_fragments_no_gap_beside_clean_redacted_whole(self):
        _assert_append(self, [F2_NO_GAP, TOKEN], 3, FRAGMENTS2)

    def test_two_fragments_gap_ten_hello_beside_clean_whole(self):
        outcome = _assert_append(
            self, [F2_GAP10_HELLO, TOKEN], 3, FRAGMENTS2
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_two_fragments_gap_766_hello_beside_clean_whole(self):
        outcome = _assert_append(
            self, [F2_GAP766_HELLO, TOKEN], 3, FRAGMENTS2
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_two_fragments_gap_ten_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, F2_GAP10
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], F2_GAP10)

    def test_two_fragments_gap_ten_beside_plain_assignment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, [F2_GAP10, ASSIGNMENT]
        )
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 1)
        journal = _journal_bytes(store)
        for fragment in FRAGMENTS2:
            self.assertNotIn(fragment, outcome["redacted_material"])
            self.assertNotIn(fragment.encode("utf-8"), journal)

    def test_bare_wrapped_at_8_beside_clean_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

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
