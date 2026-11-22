"""Fix round 38 tests for Region 4: redacting append path.

Written first for ruling 2593 of the Round 38 triage.
Ruling 2593, identity S15-R38-CAPRED-1, Low: on the
redacting append path, a wrapped token carrying one
single gap of intervening entries past the joining
window stands redacted in part only beside a clean
copy, fragment positions after the gap reaching the
journal unredacted and uncounted, because the split
joining of the landed act runs in a window of three
hundred eighty four stream entries and each extension
skip stands bounded by that window in its own right.
The gap standing after the first fragment passes in
part at three hundred eighty three intervening
entries, and a gap standing after a later fragment
passes in part at three hundred eighty five
intervening entries, the passing forms standing at
three hundred eighty five together after the third
fragment on the append path itself, at three hundred
eighty three after the first fragment in both orders
on the direct span act, and at three hundred eighty
five after the second, fourth, and fifth fragments,
and at three hundred eighty five inside a wrapping
whose fragments each carry a semicolon in the
fragment interior. The charged forms of this file
stand in the single character intervening entry
construction of the raising paper, the construction
whose past window runs completed on the bench in
that round on both evidence routes. The standing
poles pin the forms that decide correctly before
the cure: the cured bounds of the landed form at
three hundred eighty four together after the third
fragment, at three hundred eighty two after the
first fragment, and at three hundred eighty four
after the second, fourth, and fifth fragments, the
spread forms whose single gaps all stand inside
their bounds at totals of ninety, one hundred
ninety two, three hundred eighty four, and seven
hundred sixty eight intervening entries, the clean
token alone, two clean copies, and the detection
boundary forms standing alone and beside a plain
assignment line. The intervening entries of the
standing single gap forms cycle the twelve probe
words of the raising papers in their own probe
construction, hello through twelfth in order,
repeated to the count the form names.
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

BASE12 = [
    "hello", "world", "again", "fourth", "fifth", "sixth",
    "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth",
]
CYCLE_SET = set(BASE12)


def _cycle(count):
    return [BASE12[index % len(BASE12)] for index in range(count)]


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

X383 = ["x"] * 383
X385 = ["x"] * 385
GAP_382 = _cycle(382)
GAP_384 = _cycle(384)


def _gap_form(after, words, fragments=None):
    fragments = FRAGMENTS8 if fragments is None else fragments
    return "\n".join(
        fragments[:after] + list(words) + fragments[after:]
    )


X385_TOGETHER8 = _gap_form(3, X385)
X383_AFTER_FIRST8 = _gap_form(1, X383)
X385_AFTER_SECOND8 = _gap_form(2, X385)
X385_AFTER_FOURTH8 = _gap_form(4, X385)
X385_AFTER_FIFTH8 = _gap_form(5, X385)
SEMI_X385_TOGETHER8 = _gap_form(3, X385, SEMI_FRAGMENTS8)
MIXED_X385_AFTER_SECOND8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + X385 + FRAGMENTS8[2:]
)
G384_TOGETHER8 = _gap_form(3, GAP_384)
G382_AFTER_FIRST8 = _gap_form(1, GAP_382)
G384_AFTER_SECOND8 = _gap_form(2, GAP_384)
G384_AFTER_FOURTH8 = _gap_form(4, GAP_384)
G384_AFTER_FIFTH8 = _gap_form(5, GAP_384)
EIGHTEEN_EVERY_GAP8 = "\n".join(
    FRAGMENTS8[:1] + WORDS[0:18] + FRAGMENTS8[1:2]
    + WORDS[18:36] + FRAGMENTS8[2:3] + WORDS[36:54]
    + FRAGMENTS8[3:4] + WORDS[54:72] + FRAGMENTS8[4:5]
    + WORDS[72:90] + FRAGMENTS8[5:]
)
NINETY_SIX_NINETY_SIX_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:3] + WORDS[:96] + FRAGMENTS8[3:4]
    + WORDS[:96] + FRAGMENTS8[4:]
)
G192_G192_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:3] + _cycle(192) + FRAGMENTS8[3:4]
    + _cycle(192) + FRAGMENTS8[4:]
)
G384_G384_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:3] + GAP_384 + FRAGMENTS8[3:4]
    + GAP_384 + FRAGMENTS8[4:]
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


def _assert_cycle_words_stand(test, outcome):
    for word in BASE12:
        test.assertIn(word, outcome["redacted_material"])


def _covered(test, text):
    module = require("ontoloop.redact")
    spans = module._decoded_spans(text, 4, "decoded definite hit")
    return [text[start:end] for start, end, layer, cls in spans]


class TestRedactFixR38Setup(unittest.TestCase):
    """The probed token and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_single_gap_x_forms_fragments_join_to_token(self):
        for form, total in (
            (X385_TOGETHER8, 385),
            (X383_AFTER_FIRST8, 383),
            (X385_AFTER_SECOND8, 385),
            (X385_AFTER_FOURTH8, 385),
            (X385_AFTER_FIFTH8, 385),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p != "x")
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p == "x"), total
            )

    def test_bound_cycle_forms_fragments_join_to_token(self):
        for form, total in (
            (G384_TOGETHER8, 384),
            (G382_AFTER_FIRST8, 382),
            (G384_G384_TWO_GAPS8, 768),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in CYCLE_SET)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in CYCLE_SET), total
            )


class TestRedactFixR38SingleGapPastWindow(unittest.TestCase):
    """Ruling 2593: one single gap past the joining window."""

    def test_three_eighty_five_together_append_redacted_whole(self):
        outcome = _assert_append(
            self, [X385_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("x", outcome["redacted_material"])

    def test_three_eighty_five_together_spans_cover_every_fragment(self):
        covered = _covered(self, X385_TOGETHER8 + "\n" + TOKEN)
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_three_eighty_three_after_first_spans_cover_head(self):
        covered = _covered(self, X383_AFTER_FIRST8 + "\n" + TOKEN)
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_three_eighty_three_after_first_clean_first_spans(self):
        covered = _covered(self, TOKEN + "\n" + X383_AFTER_FIRST8)
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_three_eighty_five_after_second_spans_cover(self):
        covered = _covered(self, X385_AFTER_SECOND8 + "\n" + TOKEN)
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_three_eighty_five_after_fourth_spans_cover(self):
        covered = _covered(self, X385_AFTER_FOURTH8 + "\n" + TOKEN)
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_three_eighty_five_after_fifth_spans_cover_closing(self):
        covered = _covered(self, X385_AFTER_FIFTH8 + "\n" + TOKEN)
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_semicolon_three_eighty_five_together_spans_cover(self):
        covered = _covered(self, SEMI_X385_TOGETHER8 + "\n" + TOKEN)
        for fragment in SEMI_FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)

    def test_mixed_one_word_then_three_eighty_five_spans_cover(self):
        covered = _covered(self, MIXED_X385_AFTER_SECOND8 + "\n" + TOKEN)
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        self.assertNotIn("x", covered)
        self.assertNotIn("hello", covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [X385_TOGETHER8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR38Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_three_eighty_four_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G384_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_three_eighty_two_after_first_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G382_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_three_eighty_four_after_second_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G384_AFTER_SECOND8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_three_eighty_four_after_fourth_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G384_AFTER_FOURTH8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_three_eighty_four_after_fifth_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G384_AFTER_FIFTH8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_three_eighty_four_together_spans_cover_bound(self):
        covered = _covered(self, G384_TOGETHER8 + "\n" + TOKEN)
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)

    def test_eighteen_in_every_gap_total_ninety_whole(self):
        outcome = _assert_append(
            self, [EIGHTEEN_EVERY_GAP8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eightyninth", outcome["redacted_material"])

    def test_two_gaps_of_ninety_six_total_192_whole(self):
        outcome = _assert_append(
            self, [NINETY_SIX_NINETY_SIX_TWO_GAPS8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

    def test_two_gaps_of_hundred_ninety_two_total_384_whole(self):
        outcome = _assert_append(
            self, [G192_G192_TWO_GAPS8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_two_gaps_of_three_eighty_four_total_768_whole(self):
        outcome = _assert_append(
            self, [G384_G384_TWO_GAPS8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_three_eighty_five_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, X385_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], X385_TOGETHER8
        )

    def test_three_eighty_three_after_first_alone_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, X383_AFTER_FIRST8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], X383_AFTER_FIRST8
        )

    def test_three_eighty_five_together_beside_plain_assignment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module,
            [X385_TOGETHER8, ASSIGNMENT],
        )
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 1)
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
