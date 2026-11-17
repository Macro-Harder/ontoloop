"""Fix round 26 tests for Region 4: redacting append path.

Written first for rulings 1199, 1200, and 1201 of the
Round 26 triage. Ruling 1199, identity S15-R26-CR-1,
Medium: a copy of a definite encoded token whose
decoration totals five or more edge characters, standing
beside a clean copy of the same token, reaches the
journal unredacted and uncounted, because the decorated
resolution tries at most four edge characters in total,
short of its stated bound of up to four characters at
each edge severally and short of the five character
single edge forms. Ruling 1200, identity S15-R26-CR-2,
Medium: an encoded token wrapped at 8 or at 12
characters, standing beside a clean copy, reaches the
journal in every fragment, because no fragment resolves
definite exactly and the wrapped resolution stands gated
on a fragment resolving exactly, although the fragments
join and decode to the whole definite value. Ruling
1201, identity S15-R26-CR-3, Low, counted severally: a
longer definite token wrapped at 16 characters into
eight fragments stands redacted in its first six
fragments only, the longest joining the wrapped
resolution tries, and its last two fragments reach the
journal, decoding to the tail of the definite value.
The standing poles pin the forms that decide correctly
before the cure: the clean token alone, two clean
copies, the charged forms of ruling 1032, the decorated
token beside a plain assignment standing replaced under
the whole text fallback, and the detection boundary
forms, the decorated token alone and the wrapped tokens
alone, each resolving no definite hit and standing
appended unredacted in that standing form.
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
WRAPPED4 = _wrap(TOKEN, 4)
FRAGMENTS4 = WRAPPED4.split("\n")
LONG_WRAPPED = _wrap(LONG_TOKEN, 16)
LONG_FRAGMENTS = LONG_WRAPPED.split("\n")
GOLDEN_ANCHOR = (
    "c91e73191bb5ef6cd2db017b12e101a5a1f12d5be8e7b4e430e7604e4d6038ee"
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


class TestRedactFixR26Setup(unittest.TestCase):
    """The probed tokens and fragments stand in governed form."""

    def test_token_decodes_definite_at_depth_1_base64(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)

    def test_wrapped8_fragments_join_none_resolves_definite(self):
        module = require("ontoloop.redact")
        self.assertEqual("".join(FRAGMENTS8), TOKEN)
        self.assertEqual(len(FRAGMENTS8), 6)
        for fragment in FRAGMENTS8:
            result = module.decoded_candidate(fragment)
            self.assertNotEqual(result["outcome"], "definite hit")

    def test_wrapped12_fragments_join_none_resolves_exactly(self):
        module = require("ontoloop.redact")
        self.assertEqual("".join(FRAGMENTS12), TOKEN)
        self.assertEqual(len(FRAGMENTS12), 4)
        for fragment in FRAGMENTS12:
            result = module.decoded_candidate(fragment)
            self.assertNotEqual(result["outcome"], "definite hit")

    def test_longer_token_wrapped_into_eight_fragments(self):
        module = require("ontoloop.redact")
        self.assertEqual(len(LONG_TOKEN), 124)
        self.assertEqual("".join(LONG_FRAGMENTS), LONG_TOKEN)
        self.assertEqual(len(LONG_FRAGMENTS), 8)
        first = module.decoded_candidate(LONG_FRAGMENTS[0])
        self.assertEqual(first["outcome"], "definite hit")
        joined = module.decoded_candidate(LONG_TOKEN)
        self.assertEqual(joined["outcome"], "definite hit")


class TestRedactFixR26Decorated(unittest.TestCase):
    """Ruling 1199: the decorated copy beside a clean copy."""

    def _assert_decorated_redacted(self, material, token=TOKEN):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 2)
        self.assertEqual(len(store["records"]), before + 1)
        self.assertNotIn(token, outcome["redacted_material"])
        self.assertNotIn(token.encode("utf-8"), _journal_bytes(store))
        return outcome

    def test_triple_parenthesised_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted(
            ["(((" + TOKEN + ")))", TOKEN]
        )

    def test_double_brackets_trailing_comma_copy_redacted(self):
        self._assert_decorated_redacted(
            ["[[" + TOKEN + "]],", TOKEN]
        )

    def test_fused_five_prefix_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted(["xxxxx" + TOKEN, TOKEN])

    def test_five_trailing_brackets_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted([TOKEN + "]]]]]", TOKEN])

    def test_hex_triple_parenthesised_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted(
            ["(((" + HEX_TOKEN + ")))", HEX_TOKEN], token=HEX_TOKEN
        )

    def test_four_at_each_edge_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted(
            ["((((" + TOKEN + "))))", TOKEN]
        )

    def test_clean_first_triple_parenthesised_copy_redacted(self):
        self._assert_decorated_redacted(
            [TOKEN, "(((" + TOKEN + ")))"]
        )

    def test_decoded_spans_cover_triple_and_clean_copies(self):
        module = require("ontoloop.redact")
        text = "(((" + TOKEN + ")))\n" + TOKEN
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
            module, store_module, ["(((" + TOKEN + ")))", TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        appended_record = store["records"][-1]
        self.assertNotIn(
            TOKEN.encode("utf-8"), appended_record["canonical_bytes"]
        )
        self.assertNotIn(
            ("(((" + TOKEN + ")))").encode("utf-8"),
            appended_record["canonical_bytes"],
        )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR26WrappedGate(unittest.TestCase):
    """Ruling 1200: the wrapped resolution gate on the joined value."""

    def _assert_wrapped_redacted(self, material, fragments, hits):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], hits)
        self.assertEqual(len(store["records"]), before + 1)
        for fragment in fragments:
            self.assertNotIn(fragment, outcome["redacted_material"])
            self.assertNotIn(
                fragment.encode("utf-8"), _journal_bytes(store)
            )
        return outcome

    def test_wrapped_at_8_beside_clean_redacted_whole(self):
        self._assert_wrapped_redacted([WRAPPED8, TOKEN], FRAGMENTS8, 7)

    def test_wrapped_at_12_beside_clean_redacted_whole(self):
        self._assert_wrapped_redacted(
            [WRAPPED12, TOKEN], FRAGMENTS12, 5
        )

    def test_wrapped_at_4_beside_clean_redacted_whole(self):
        self._assert_wrapped_redacted([WRAPPED4, TOKEN], FRAGMENTS4, 12)

    def test_decoded_spans_cover_every_fragment_at_8(self):
        module = require("ontoloop.redact")
        text = WRAPPED8 + "\n" + TOKEN
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS8:
            self.assertIn(fragment, covered)
        self.assertIn(TOKEN, covered)


class TestRedactFixR26WrappedCount(unittest.TestCase):
    """Ruling 1201: the joining count beyond six fragments."""

    def _assert_long_redacted(self, material, hits):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], hits)
        self.assertEqual(len(store["records"]), before + 1)
        for fragment in LONG_FRAGMENTS:
            self.assertNotIn(fragment, outcome["redacted_material"])
            self.assertNotIn(
                fragment.encode("utf-8"), _journal_bytes(store)
            )
        return outcome

    def test_long_wrapped_beside_clean_redacted_whole(self):
        self._assert_long_redacted([LONG_WRAPPED, LONG_TOKEN], 9)

    def test_long_wrapped_beside_assignment_redacted_whole(self):
        self._assert_long_redacted([ASSIGNMENT, LONG_WRAPPED], 9)

    def test_decoded_spans_cover_every_long_fragment(self):
        module = require("ontoloop.redact")
        text = ASSIGNMENT + "\n" + LONG_WRAPPED
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in LONG_FRAGMENTS:
            self.assertIn(fragment, covered)


class TestRedactFixR26Standing(unittest.TestCase):
    """Standing poles deciding in their standing forms."""

    def test_clean_token_alone_redacted_once(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, TOKEN)
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertNotIn(TOKEN, outcome["redacted_material"])
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))

    def test_two_clean_copies_redacted_twice(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, [TOKEN, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        self.assertNotIn(TOKEN, outcome["redacted_material"])
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))

    def test_ruling_1032_mixed_form_still_redacts_token(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, [ASSIGNMENT, TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        self.assertNotIn(TOKEN, outcome["redacted_material"])
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))

    def test_decorated_beside_plain_assignment_standing_form(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, ["(" + TOKEN + ")", ASSIGNMENT]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertNotIn(TOKEN, outcome["redacted_material"])
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))

    def test_decorated_token_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        material = "(" + TOKEN + ")"
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], material)

    def test_wrapped_at_16_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        wrapped = _wrap(TOKEN, 16)
        store, before, outcome = _append(module, store_module, wrapped)
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], wrapped)

    def test_wrapped_at_8_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, WRAPPED8)
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], WRAPPED8)

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
