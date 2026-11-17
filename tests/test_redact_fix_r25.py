"""Fix round 25 tests for Region 4: redacting append path.

Written first for rulings 1108 and 1109 of the Round 25
triage. Ruling 1108, identity S15-R25-CR-1, Medium: a
copy of a definite encoded token carrying a decoration,
standing beside a clean copy of the same token, reaches
the journal unredacted and uncounted, because the
decoded span computation resolves only the clean
whitespace separated token. Ruling 1109, identity
S15-R25-CR-2, Low: a line wrapped encoded token standing
beside a plain assignment or a clean token stands
redacted in its first fragment only, its remaining
fragments reaching the journal unredacted and uncounted.
The standing poles pin the forms that decide correctly
before the cure: the clean token alone, two clean
copies, the charged forms of ruling 1032, the decorated
token beside a plain assignment standing replaced under
the whole text fallback, and the detection boundary
forms, the decorated token alone and the wrapped token
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
WRAPPED = "\n".join(
    TOKEN[start:start + 16] for start in range(0, len(TOKEN), 16)
)
FRAGMENTS = WRAPPED.split("\n")
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


class TestRedactFixR25Setup(unittest.TestCase):
    """The probed token and fragments stand in governed form."""

    def test_token_decodes_definite_at_depth_1_base64(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)
        self.assertEqual(
            result["decoding_round_fields"], ["round 1: base64"]
        )

    def test_hex_token_decodes_definite(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(HEX_TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(
            result["decoding_round_fields"], ["round 1: hex"]
        )

    def test_wrapped_fragments_join_to_token_first_resolves(self):
        module = require("ontoloop.redact")
        self.assertEqual("".join(FRAGMENTS), TOKEN)
        self.assertEqual(len(FRAGMENTS), 3)
        first = module.decoded_candidate(FRAGMENTS[0])
        self.assertEqual(first["outcome"], "definite hit")
        for fragment in FRAGMENTS[1:]:
            result = module.decoded_candidate(fragment)
            self.assertNotEqual(result["outcome"], "definite hit")


class TestRedactFixR25Decorated(unittest.TestCase):
    """Ruling 1108: the decorated copy beside a clean copy."""

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

    def test_parenthesised_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted(["(" + TOKEN + ")", TOKEN])

    def test_double_quoted_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted(['"' + TOKEN + '"', TOKEN])

    def test_square_bracketed_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted(["[" + TOKEN + "]", TOKEN])

    def test_trailing_comma_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted([TOKEN + ",", TOKEN])

    def test_trailing_full_stop_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted([TOKEN + ".", TOKEN])

    def test_trailing_semicolon_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted([TOKEN + ";", TOKEN])

    def test_fused_prefix_copy_redacted_beside_clean(self):
        self._assert_decorated_redacted(["xx" + TOKEN, TOKEN])

    def test_hex_parenthesised_copy_redacted_beside_clean_hex(self):
        self._assert_decorated_redacted(
            ["(" + HEX_TOKEN + ")", HEX_TOKEN], token=HEX_TOKEN
        )

    def test_clean_first_decorated_copy_redacted(self):
        self._assert_decorated_redacted([TOKEN, TOKEN + ","])

    def test_decoded_spans_cover_decorated_and_clean_copies(self):
        module = require("ontoloop.redact")
        text = "(" + TOKEN + ")\n" + TOKEN
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
            module, store_module, ["(" + TOKEN + ")", TOKEN]
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 2)
        appended_record = store["records"][-1]
        self.assertNotIn(
            TOKEN.encode("utf-8"), appended_record["canonical_bytes"]
        )
        self.assertNotIn(
            ("(" + TOKEN + ")").encode("utf-8"),
            appended_record["canonical_bytes"],
        )
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))


class TestRedactFixR25Wrapped(unittest.TestCase):
    """Ruling 1109: the wrapped token redacted in every fragment."""

    def _assert_wrapped_redacted(self, material, hits):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], hits)
        self.assertEqual(len(store["records"]), before + 1)
        for fragment in FRAGMENTS:
            self.assertNotIn(fragment, outcome["redacted_material"])
            self.assertNotIn(
                fragment.encode("utf-8"), _journal_bytes(store)
            )
        return outcome

    def test_wrapped_beside_plain_assignment_redacted_whole(self):
        self._assert_wrapped_redacted([ASSIGNMENT, WRAPPED], 4)

    def test_wrapped_beside_clean_token_redacted_whole(self):
        self._assert_wrapped_redacted([WRAPPED, TOKEN], 4)

    def test_decoded_spans_cover_every_fragment(self):
        module = require("ontoloop.redact")
        text = ASSIGNMENT + "\n" + WRAPPED
        spans = module._decoded_spans(text, 4, "decoded definite hit")
        covered = [text[start:end] for start, end, layer, cls in spans]
        for fragment in FRAGMENTS:
            self.assertIn(fragment, covered)


class TestRedactFixR25Standing(unittest.TestCase):
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

    def test_wrapped_token_alone_detection_boundary(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, WRAPPED)
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["redacted_material"], WRAPPED)

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
