"""Fix round 24 tests for Region 4: redacting append path.

Written first for ruling 1032 of the Round 24 triage,
identity S15-R24-CR-1, Medium: a definite hit that the
layer 4 decoding engine resolves, standing as an
encoded token in the material, reaches the journal
unredacted and uncounted wherever the joined text the
append writes carries any unrelated underlying span,
because the span mapping for layers 4 and 6 returns
the underlying spans of the whole text whenever any
exist and never returns the decoded token span beside
them. The control form, the token standing alone with
no unrelated span in the text, redacts correctly in
its standing form and stands pinned here unchanged.
"""

import base64
import unittest

from tests.harness import require

PLAIN = b"password = " + b"a" * 20
TOKEN = base64.b64encode(PLAIN).decode("ascii")
HEX_TOKEN = PLAIN.hex()
ASSIGNMENT = "password = PlainValue999"
DECLARATION = "credential type: plain words only"
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


class TestRedactFixR24Setup(unittest.TestCase):
    """The probed token stands in its governed setup form."""

    def test_token_decodes_definite_at_depth_1_base64(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(result["decoding_depth_reached"], 1)
        self.assertEqual(
            result["decoding_round_fields"], ["round 1: base64"]
        )

    def test_token_raises_no_layer_3_entropy_firing(self):
        module = require("ontoloop.redact")
        self.assertEqual(len(TOKEN), 44)
        self.assertLess(module._entropy(TOKEN), 4.5)

    def test_hex_token_decodes_definite(self):
        module = require("ontoloop.redact")
        result = module.decoded_candidate(HEX_TOKEN)
        self.assertEqual(result["outcome"], "definite hit")
        self.assertEqual(
            result["decoding_round_fields"], ["round 1: hex"]
        )

    def test_mixed_material_classifies_in_governed_records(self):
        module = require("ontoloop.redact")
        result = module.classify_material([ASSIGNMENT, TOKEN])
        records = result["firing_records"]
        self.assertTrue(
            any(r["outcome"] == "definite" for r in records[1])
        )
        self.assertTrue(
            any(r["outcome"] == "definite" for r in records[4])
        )
        self.assertTrue(
            any(r["outcome"] == "definite" for r in records[6])
        )


class TestRedactFixR24MixedForms(unittest.TestCase):
    """Ruling 1032: the decoded hit beside an unrelated span."""

    def _assert_token_redacted(self, material, token=TOKEN):
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

    def test_mixed_list_assignment_first_redacts_token(self):
        self._assert_token_redacted([ASSIGNMENT, TOKEN])

    def test_mixed_list_token_first_redacts_token(self):
        self._assert_token_redacted([TOKEN, ASSIGNMENT])

    def test_mixed_tuple_redacts_token(self):
        self._assert_token_redacted((ASSIGNMENT, TOKEN))

    def test_mixed_mapping_values_redact_token(self):
        self._assert_token_redacted(
            {"first": ASSIGNMENT, "second": TOKEN}
        )

    def test_mixed_string_material_redacts_token(self):
        self._assert_token_redacted(ASSIGNMENT + "\n" + TOKEN)

    def test_mixed_longer_first_item_redacts_token(self):
        outcome = self._assert_token_redacted(
            ["note " + ASSIGNMENT + " end", TOKEN]
        )
        self.assertTrue(
            outcome["redacted_material"].startswith("note ")
        )
        self.assertTrue(outcome["redacted_material"].endswith(
            "layer 4 decoded definite hit"
        ) or "layer" in outcome["redacted_material"])

    def test_mixed_declaration_divert_redacts_token(self):
        self._assert_token_redacted([DECLARATION, TOKEN])

    def test_mixed_pattern_divert_redacts_token(self):
        module = require("ontoloop.redact")
        shape = module.secret_bearing_shapes()[0]
        material = [shape["raw_bytes"].decode("utf-8"), TOKEN]
        self._assert_token_redacted(material)

    def test_mixed_hex_token_redacts_beside_assignment(self):
        self._assert_token_redacted(
            [ASSIGNMENT, HEX_TOKEN], token=HEX_TOKEN
        )

    def test_layer_4_span_mapping_includes_decoded_span(self):
        module = require("ontoloop.redact")
        text = ASSIGNMENT + "\n" + TOKEN
        spans = module._definite_record_spans(
            {"layer": 4, "class": "decoded definite hit"}, text
        )
        token_start = text.index(TOKEN)
        self.assertIn(
            (token_start, token_start + len(TOKEN),
             4, "decoded definite hit"),
            spans,
        )
        self.assertTrue(
            any(start == 0 for start, end, layer, cls in spans)
        )

    def test_layer_6_span_mapping_includes_decoded_span(self):
        module = require("ontoloop.redact")
        text = ASSIGNMENT + "\n" + TOKEN
        spans = module._definite_record_spans(
            {"layer": 6, "class": "assembly as a whole"}, text
        )
        token_start = text.index(TOKEN)
        self.assertIn(
            (token_start, token_start + len(TOKEN),
             6, "assembly as a whole"),
            spans,
        )
        self.assertTrue(
            any(start == 0 for start, end, layer, cls in spans)
        )

    def test_redact_text_mixed_counts_both_regions(self):
        module = require("ontoloop.redact")
        text = ASSIGNMENT + "\n" + TOKEN
        redacted, placeholders, hits, unspanned = module._redact_text(
            text, "run one"
        )
        self.assertFalse(unspanned)
        self.assertEqual(hits, 2)
        self.assertNotIn(TOKEN, redacted)
        self.assertNotIn(ASSIGNMENT, redacted)


class TestRedactFixR24Controls(unittest.TestCase):
    """Control forms standing correct before the cure, unchanged."""

    def test_token_alone_redacted_once(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(module, store_module, TOKEN)
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertNotIn(TOKEN, outcome["redacted_material"])
        self.assertNotIn(TOKEN.encode("utf-8"), _journal_bytes(store))

    def test_hex_token_alone_redacted_once(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, HEX_TOKEN
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertNotIn(HEX_TOKEN, outcome["redacted_material"])

    def test_plain_assignment_alone_redacted_once(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, ASSIGNMENT
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertNotIn("PlainValue999", outcome["redacted_material"])

    def test_declaration_alone_redacted_once(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, DECLARATION
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertNotIn("plain words only", outcome["redacted_material"])

    def test_clean_material_unchanged(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        material = "a routine note about lunch"
        store, before, outcome = _append(module, store_module, material)
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(outcome["placeholders"], [])
        self.assertEqual(outcome["redacted_material"], material)

    def test_append_refused_where_definite_record_has_no_span(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        store, before, outcome = _append(
            module, store_module, {"password": "x"}
        )
        self.assertFalse(outcome["appended"])
        self.assertFalse(outcome["reported_appended"])
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 0)
        self.assertEqual(len(store["records"]), before)

    def test_each_governed_shape_redacted_once(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        for shape in module.secret_bearing_shapes():
            store = store_module.golden_record_store()
            material = shape["raw_bytes"].decode("utf-8")
            outcome = module.append_redacted(
                store, material, scope="run one"
            )
            self.assertTrue(outcome["appended"])
            self.assertEqual(outcome["hits_redacted"], 1)
            self.assertNotIn(material, outcome["redacted_material"])
            self.assertNotIn(shape["raw_bytes"], _journal_bytes(store))

    def test_golden_anchor_unmoved(self):
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        self.assertEqual(
            store["signature_object"]["signature"], GOLDEN_ANCHOR
        )


if __name__ == "__main__":
    unittest.main()
