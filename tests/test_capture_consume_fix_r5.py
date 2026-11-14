"""Fix round 5 tests for Region 6: capture, consume, registry.

Written test first for the four acts charged at Round 5
triage ruling 86 point 6: ruling 80 (N-43, the top level
assembly_state value gathered as content), ruling 60
(N-23, the ingest tool docstring stating the return form
as built, documentation limb only), ruling 61 (N-24, the
ingest digest taken over a canonical form distinguishing
type as well as content), and ruling 76 (N-39, the
promotion registry holding and returning its own copy).
Each class pins its act beside the standing forms its
charge protects.
"""

import hashlib
import unittest

from tests.harness import require


class TestRedactFixR5TopStateValue(unittest.TestCase):
    """Fix round 5, ruling 80: top level state value as content.

    Hit material standing as the top level assembly_state
    value, in byte form and in text form, beside clean
    content refuses whole, as the same material standing
    as an ordinary value, as a mapping key, or under a
    nested assembly_state key already does. The state
    only and zero byte forms keep the fail closed form
    the value content floor states, and a clean assembly
    still releases.
    """

    def test_hit_bytes_as_top_state_value_beside_clean_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {"assembly_state": hit, "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_text_as_top_state_value_beside_clean_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "assembly_state": hit.decode("utf-8"),
                "content": "a routine clean note",
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_same_hit_as_ordinary_value_control_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {"note": hit, "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_same_hit_as_key_control_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {hit: "a routine clean note", "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_same_hit_under_nested_state_key_control_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "content": "a routine clean note",
                "nested": {"assembly_state": hit},
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_state_value_inside_a_mapping_beside_clean_refuses(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "assembly_state": {"detail": hit},
                "content": "a routine clean note",
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")

    def test_state_only_hit_value_still_fails_closed_on_the_floor(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan({"assembly_state": hit})
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_state_only_and_zero_byte_forms_still_fail_closed(self):
        module = require("ontoloop.redact")
        for assembly in (
            {"assembly_state": "ready"},
            {"assembly_state": "ready", "content": ""},
            {"assembly_state": "ready", "content": b""},
        ):
            outcome = module.exit_scan(assembly)
            self.assertTrue(outcome["refused"])
            self.assertEqual(
                outcome["form"], "no exit scan result, no exit"
            )

    def test_clean_state_label_beside_clean_content_still_releases(self):
        module = require("ontoloop.redact")
        for state in ("ready", "planted uncleared hit"):
            outcome = module.exit_scan(
                {
                    "assembly_state": state,
                    "content": "a routine clean note",
                }
            )
            self.assertFalse(outcome["refused"])


class TestConsumeFixR5IngestDocstring(unittest.TestCase):
    """Fix round 5, ruling 60: the ingest docstring as built.

    Documentation limb only. A live call stands beside
    the corrected docstring, in the form of the Round 3
    consume cures: the call result and the docstring
    agree key for key, the return carrying exactly the
    keys ingested and material_digest, and no recording
    act, record list, or record position standing stated.
    """

    def test_live_call_return_form(self):
        module = require("ontoloop.service_layer")
        result = module.ingest_tool("alpha")
        self.assertEqual(
            sorted(result.keys()), ["ingested", "material_digest"]
        )
        self.assertTrue(result["ingested"])
        self.assertEqual(
            result["material_digest"],
            hashlib.sha256("alpha".encode("utf-8")).hexdigest(),
        )

    def test_docstring_states_the_return_as_built(self):
        module = require("ontoloop.service_layer")
        docstring = module.ingest_tool.__doc__
        self.assertIn("ingested", docstring)
        self.assertIn("material_digest", docstring)
        self.assertNotIn("record list", docstring)
        self.assertNotIn("record position", docstring)
        self.assertNotIn("records the material digest", docstring)


class TestConsumeFixR5IngestDigest(unittest.TestCase):
    """Fix round 5, ruling 61: the ingest digest canonical form.

    The digest stands taken over a canonical form that
    distinguishes type as well as content, in the form
    the consumption module digest helper governs: byte
    material over its bytes, string material over its
    UTF-8 encoding, and other material over a key sorted
    encoding. String material, the form all standing
    tests use, digests exactly as it does today.
    """

    def test_byte_material_and_its_string_spelling_differ(self):
        module = require("ontoloop.service_layer")
        byte_digest = module.ingest_tool(b"alpha")["material_digest"]
        string_digest = module.ingest_tool("b'alpha'")["material_digest"]
        self.assertNotEqual(byte_digest, string_digest)
        self.assertEqual(
            byte_digest, hashlib.sha256(b"alpha").hexdigest()
        )

    def test_no_material_and_the_string_none_differ(self):
        module = require("ontoloop.service_layer")
        none_digest = module.ingest_tool()["material_digest"]
        explicit_digest = module.ingest_tool(None)["material_digest"]
        string_digest = module.ingest_tool("None")["material_digest"]
        self.assertEqual(none_digest, explicit_digest)
        self.assertNotEqual(none_digest, string_digest)

    def test_equal_mappings_in_different_key_order_share_one_digest(self):
        module = require("ontoloop.service_layer")
        first = module.ingest_tool({"a": 1, "b": 2})["material_digest"]
        second = module.ingest_tool({"b": 2, "a": 1})["material_digest"]
        self.assertEqual(first, second)

    def test_differing_mappings_differ(self):
        module = require("ontoloop.service_layer")
        first = module.ingest_tool({"a": 1, "b": 2})["material_digest"]
        second = module.ingest_tool({"a": 1, "b": 3})["material_digest"]
        self.assertNotEqual(first, second)

    def test_string_material_digest_stands_as_today(self):
        module = require("ontoloop.service_layer")
        for material in ("alpha", "a routine clean note", ""):
            result = module.ingest_tool(material)
            self.assertEqual(
                result["material_digest"],
                hashlib.sha256(material.encode("utf-8")).hexdigest(),
            )
            repeat = module.ingest_tool(material)
            self.assertEqual(
                repeat["material_digest"], result["material_digest"]
            )


class TestConsumeFixR5RegistryCopy(unittest.TestCase):
    """Fix round 5, ruling 76: the registry holds its own copy.

    A mutation of the bundle object a caller passed,
    after recording, and a mutation of a bundle object
    a surface returned each leave what later consumers
    receive unchanged, at the store limb and at the
    return limb. The standing string bundle callers
    still record and discover as pinned.
    """

    def test_mutation_of_passed_bundle_after_recording_does_not_rewrite(self):
        module = require("ontoloop.consumption")
        workflow = "fix r5 registry store limb"
        bundle = {"version": "one", "items": ["a"]}
        module.record_promotion(workflow, bundle)
        bundle["version"] = "tampered"
        bundle["items"].append("b")
        bundle["extra"] = True
        found = module.discover(workflow=workflow)
        self.assertEqual(
            found["bundle"], {"version": "one", "items": ["a"]}
        )

    def test_mutation_of_discovered_bundle_does_not_rewrite(self):
        module = require("ontoloop.consumption")
        workflow = "fix r5 registry return limb"
        caller_bundle = {"version": "one", "items": ["a"]}
        module.record_promotion(workflow, caller_bundle)
        found = module.discover(workflow=workflow)
        found["bundle"]["version"] = "tampered"
        found["bundle"]["items"].append("b")
        later = module.discover(workflow=workflow)
        self.assertEqual(
            later["bundle"], {"version": "one", "items": ["a"]}
        )
        self.assertEqual(
            caller_bundle, {"version": "one", "items": ["a"]}
        )

    def test_mutation_of_record_return_bundle_does_not_rewrite(self):
        module = require("ontoloop.consumption")
        workflow = "fix r5 registry record return limb"
        recorded = module.record_promotion(
            workflow, {"version": "one", "items": ["a"]}
        )
        recorded["bundle"]["version"] = "tampered"
        recorded["bundle"]["items"].append("b")
        found = module.discover(workflow=workflow)
        self.assertEqual(
            found["bundle"], {"version": "one", "items": ["a"]}
        )

    def test_string_bundle_callers_still_record_and_discover(self):
        module = require("ontoloop.consumption")
        workflow = "fix r5 registry string bundle"
        recorded = module.record_promotion(workflow, "bundle version 1")
        self.assertTrue(recorded["recorded"])
        self.assertEqual(recorded["bundle"], "bundle version 1")
        found = module.discover(workflow=workflow)
        self.assertEqual(found["answer"], "promotion")
        self.assertFalse(found["is_error"])
        self.assertEqual(found["bundle"], "bundle version 1")


if __name__ == "__main__":
    unittest.main()
