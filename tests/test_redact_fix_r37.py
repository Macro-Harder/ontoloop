"""Fix round 37 tests for Region 4: redacting append path.

Written first for ruling 2443 of the Round 37 triage.
Ruling 2443, identity S15-R37-CAPRED-1, Low: on the
redacting append path, a wrapped token carrying one
single gap of intervening entries past the joining
window stands redacted in part only beside a clean
copy, fragment positions after the gap reaching the
journal unredacted and uncounted, because the split
joining of the landed act runs in a window of one
hundred ninety two stream entries and each extension
skip stands bounded by that window in its own right.
The gap standing after the first fragment passes in
part at one hundred ninety one intervening entries,
and a gap standing after a later fragment passes in
part at one hundred ninety three intervening entries,
the passing forms standing at one hundred ninety
three together after the third fragment in both
orders, at one hundred ninety one after the first
fragment in both orders, at one hundred ninety three
after the second, fourth, and fifth fragments, and
at one hundred ninety three inside a wrapping whose
fragments each carry a semicolon in the fragment
interior. The standing poles pin the forms that
decide correctly before the cure: the cured bounds
of the landed form at one hundred ninety two
together after the third fragment, at one hundred
ninety after the first fragment, and at one hundred
ninety two after the second, fourth, and fifth
fragments, the spread forms whose single gaps all
stand inside their bounds at totals of ninety,
ninety six, one hundred ninety two, and three
hundred eighty four intervening entries, the clean
token alone, two clean copies, and the detection
boundary forms standing alone and beside a plain
assignment line. The intervening entries of the
single gap forms cycle the twelve probe words of
the raising paper in its own probe construction,
hello through twelfth in order, repeated to the
count the form names.
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

GAP_190 = _cycle(190)
GAP_191 = _cycle(191)
GAP_192 = _cycle(192)
GAP_193 = _cycle(193)
GAP_256 = _cycle(256)


def _gap_form(after, words, fragments=None):
    fragments = FRAGMENTS8 if fragments is None else fragments
    return "\n".join(
        fragments[:after] + list(words) + fragments[after:]
    )


G193_TOGETHER8 = _gap_form(3, GAP_193)
G256_TOGETHER8 = _gap_form(3, GAP_256)
G191_AFTER_FIRST8 = _gap_form(1, GAP_191)
G192_AFTER_FIRST8 = _gap_form(1, GAP_192)
G256_AFTER_FIRST8 = _gap_form(1, GAP_256)
G193_AFTER_SECOND8 = _gap_form(2, GAP_193)
G193_AFTER_FOURTH8 = _gap_form(4, GAP_193)
G193_AFTER_FIFTH8 = _gap_form(5, GAP_193)
SEMI_G193_TOGETHER8 = _gap_form(3, GAP_193, SEMI_FRAGMENTS8)
G193_SECOND_ONE_AFTER_FIRST8 = "\n".join(
    FRAGMENTS8[:1] + ["hello"] + FRAGMENTS8[1:2]
    + GAP_193 + FRAGMENTS8[2:]
)
G192_TOGETHER8 = _gap_form(3, GAP_192)
G190_AFTER_FIRST8 = _gap_form(1, GAP_190)
G192_AFTER_SECOND8 = _gap_form(2, GAP_192)
G192_AFTER_FOURTH8 = _gap_form(4, GAP_192)
G192_AFTER_FIFTH8 = _gap_form(5, GAP_192)
EIGHTEEN_EVERY_GAP8 = "\n".join(
    FRAGMENTS8[:1] + WORDS[0:18] + FRAGMENTS8[1:2]
    + WORDS[18:36] + FRAGMENTS8[2:3] + WORDS[36:54]
    + FRAGMENTS8[3:4] + WORDS[54:72] + FRAGMENTS8[4:5]
    + WORDS[72:90] + FRAGMENTS8[5:]
)
FORTY_EIGHT_FORTY_EIGHT_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:1] + WORDS[:48] + FRAGMENTS8[1:3]
    + WORDS[48:96] + FRAGMENTS8[3:]
)
NINETY_SIX_NINETY_SIX_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:3] + WORDS[:96] + FRAGMENTS8[3:4]
    + WORDS[:96] + FRAGMENTS8[4:]
)
G192_G192_TWO_GAPS8 = "\n".join(
    FRAGMENTS8[:3] + GAP_192 + FRAGMENTS8[3:4]
    + GAP_192 + FRAGMENTS8[4:]
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


class TestRedactFixR37Setup(unittest.TestCase):
    """The probed token and new forms stand in governed form."""

    def test_token_decodes_definite_at_depth_1(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_single_gap_forms_fragments_join_to_token(self):
        for form, total in (
            (G193_TOGETHER8, 193),
            (G191_AFTER_FIRST8, 191),
            (G193_AFTER_SECOND8, 193),
            (G193_AFTER_FOURTH8, 193),
            (G193_AFTER_FIFTH8, 193),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in CYCLE_SET)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in CYCLE_SET), total
            )

    def test_further_single_gap_forms_join_to_token(self):
        for form, total in (
            (G256_TOGETHER8, 256),
            (G192_AFTER_FIRST8, 192),
            (G256_AFTER_FIRST8, 256),
            (G193_SECOND_ONE_AFTER_FIRST8, 194),
        ):
            parts = form.split("\n")
            joined = "".join(p for p in parts if p not in CYCLE_SET)
            self.assertEqual(joined, TOKEN)
            self.assertEqual(
                sum(1 for p in parts if p in CYCLE_SET), total
            )


class TestRedactFixR37SingleGapPastWindow(unittest.TestCase):
    """Ruling 2443: one single gap past the joining window."""

    def test_hundred_ninety_three_together_redacted_whole_words_stand(self):
        outcome = _assert_append(
            self, [G193_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_three_together_clean_first_redacted_whole(self):
        outcome = _assert_append(
            self, [TOKEN, G193_TOGETHER8], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_two_hundred_fifty_six_together_redacted_whole(self):
        outcome = _assert_append(
            self, [G256_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_one_after_first_redacted_whole_head(self):
        outcome = _assert_append(
            self, [G191_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_hundred_ninety_two_after_first_redacted_whole(self):
        outcome = _assert_append(
            self, [G192_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_two_hundred_fifty_six_after_first_redacted_whole(self):
        outcome = _assert_append(
            self, [G256_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_one_after_first_clean_first_whole(self):
        outcome = _assert_append(
            self, [TOKEN, G191_AFTER_FIRST8], 7, FRAGMENTS8
        )
        self.assertIn("hello", outcome["redacted_material"])

    def test_hundred_ninety_three_after_second_redacted_whole(self):
        outcome = _assert_append(
            self, [G193_AFTER_SECOND8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_three_after_fourth_redacted_whole(self):
        outcome = _assert_append(
            self, [G193_AFTER_FOURTH8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_three_after_fifth_redacted_whole(self):
        outcome = _assert_append(
            self, [G193_AFTER_FIFTH8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_semicolon_hundred_ninety_three_together_redacted_whole(self):
        _assert_append(
            self, [SEMI_G193_TOGETHER8, TOKEN], 7,
            SEMI_FRAGMENTS8, token_absent=TOKEN,
        )

    def test_hundred_ninety_three_one_gap_after_second_one_word_gap(self):
        outcome = _assert_append(
            self, [G193_SECOND_ONE_AFTER_FIRST8, TOKEN], 7,
            FRAGMENTS8,
        )
        _assert_cycle_words_stand(self, outcome)

    def test_decoded_spans_cover_every_fragment_past_gap(self):
        module = require("ontoloop.redact")
        text = G193_TOGETHER8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)
        for word in CYCLE_SET:
            self.assertNotIn(word, covered)

    def test_golden_store_canonical_bytes_carry_no_fragment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        fresh = store_module.golden_record_store()
        self.assertEqual(
            fresh["signature_object"]["signature"], GOLDEN_ANCHOR
        )
        store, before, outcome = _append(
            module, store_module, [G193_TOGETHER8, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 7)
        for fragment in FRAGMENTS8:
            self.assertNotIn(
                fragment.encode("utf-8"),
                store["records"][-1]["canonical_bytes"],
            )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR37Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        _assert_append(self, TOKEN, 1, [], TOKEN)

    def test_two_clean_copies_redacted_twice(self):
        _assert_append(self, [TOKEN, TOKEN], 2, [], TOKEN)

    def test_bare_wrapped_at_8_still_redacts(self):
        _assert_append(self, [WRAPPED8, TOKEN], 7, FRAGMENTS8)

    def test_hundred_ninety_two_together_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G192_TOGETHER8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_after_first_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G190_AFTER_FIRST8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_two_after_second_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G192_AFTER_SECOND8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_two_after_fourth_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G192_AFTER_FOURTH8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_hundred_ninety_two_after_fifth_still_redacts_whole(self):
        outcome = _assert_append(
            self, [G192_AFTER_FIFTH8, TOKEN], 7, FRAGMENTS8
        )
        _assert_cycle_words_stand(self, outcome)

    def test_eighteen_in_every_gap_total_ninety_whole(self):
        outcome = _assert_append(
            self, [EIGHTEEN_EVERY_GAP8, TOKEN], 7, FRAGMENTS8
        )
        self.assertIn("eightyninth", outcome["redacted_material"])

    def test_two_gaps_of_forty_eight_total_ninety_six_whole(self):
        outcome = _assert_append(
            self, [FORTY_EIGHT_FORTY_EIGHT_TWO_GAPS8, TOKEN], 7,
            FRAGMENTS8,
        )
        self.assertIn("ninetysixth", outcome["redacted_material"])

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

    def test_hundred_ninety_three_together_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, G193_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], G193_TOGETHER8
        )

    def test_hundred_ninety_one_after_first_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, G191_AFTER_FIRST8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], G191_AFTER_FIRST8
        )

    def test_semicolon_hundred_ninety_three_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, SEMI_G193_TOGETHER8
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(
            outcome["redacted_material"], SEMI_G193_TOGETHER8
        )

    def test_hundred_ninety_three_together_beside_plain_assignment(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module,
            [G193_TOGETHER8, ASSIGNMENT],
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
