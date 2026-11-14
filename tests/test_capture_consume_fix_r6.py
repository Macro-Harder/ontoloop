"""Fix round 6 tests for Region 6: capture, redact, consume.

Written test first for the six positions charged at Round 6
triage ruling 136 point 6: ruling 108 (S15-R6-CR-1,
computation_inputs on an unhashable name), ruling 109
(S15-R6-CR-2, shared_rule on an unhashable layer), ruling
133 second limb only (line D-7, a memoryview value and a
mapping proxy value at the exit scan gathering acts),
ruling 105 (R6-CONSUME-1, the canonical digest type
collisions), ruling 106 (R6-CONSUME-2, the digest of set
bearing material stable across processes), and ruling
107 (R6-CONSUME-3, mixed and tuple key mappings at the
digest surfaces). Each class pins its act beside the
standing forms its charge protects. No test in this file
pins the generator form of line D-7, which ruling 133
rules NOT A DEFECT on its first limb.
"""

import hashlib
import os
import subprocess
import sys
import types
import unittest

from tests.harness import require

SYSTEM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ingest_digest(module, material):
    return module.ingest_tool(material)["material_digest"]


def _consumption_digest(module, material):
    return module.load_with_hash_check(material)["computed_hash"]


class TestCaptureFixR6ComputationInputs(unittest.TestCase):
    """Fix round 6, ruling 108: an unhashable computation name.

    A list name and a mapping name raise the stated
    ValueError form for a name outside the three
    computation names, as hashable outsiders already do,
    and the standing names still return their input
    tuples.
    """

    def test_list_name_raises_value_error(self):
        module = require("ontoloop.capture")
        with self.assertRaises(ValueError):
            module.computation_inputs(["signature"])

    def test_mapping_name_raises_value_error(self):
        module = require("ontoloop.capture")
        with self.assertRaises(ValueError):
            module.computation_inputs({"name": "signature"})

    def test_hashable_outsiders_still_raise_value_error(self):
        module = require("ontoloop.capture")
        for name in ("bogus", None, 5):
            with self.assertRaises(ValueError):
                module.computation_inputs(name)

    def test_standing_names_still_return_their_input_tuples(self):
        module = require("ontoloop.capture")
        for name in ("signature", "group_key", "pool_stamp"):
            result = module.computation_inputs(name)
            self.assertIsInstance(result, tuple)
            self.assertTrue(result)
            self.assertNotIn("review outcome", result)
            self.assertNotIn("correction", result)


class TestRedactFixR6SharedRule(unittest.TestCase):
    """Fix round 6, ruling 109: an unhashable layer.

    A list layer and a mapping layer raise the stated
    ValueError form for a layer outside the six, as
    hashable outsiders already do, and the six standing
    layers still return their rule texts.
    """

    def test_list_layer_raises_value_error(self):
        module = require("ontoloop.redact")
        with self.assertRaises(ValueError):
            module.shared_rule([1])

    def test_mapping_layer_raises_value_error(self):
        module = require("ontoloop.redact")
        with self.assertRaises(ValueError):
            module.shared_rule({"layer": 1})

    def test_hashable_outsiders_still_raise_value_error(self):
        module = require("ontoloop.redact")
        for layer in ("1", 0, 1.5, None):
            with self.assertRaises(ValueError):
                module.shared_rule(layer)

    def test_six_standing_layers_still_return_their_rule_texts(self):
        module = require("ontoloop.redact")
        texts = [module.shared_rule(layer) for layer in (1, 2, 3, 4, 5, 6)]
        self.assertEqual(len(set(texts)), 6)
        for text in texts:
            self.assertTrue(text)


class TestRedactFixR6GatheringViewForms(unittest.TestCase):
    """Fix round 6, ruling 133, second limb only: view forms.

    Hit material standing in a memoryview value, in byte
    form and in text form, and hit material standing
    under a mapping proxy value, beside clean content,
    each refuse whole, as the same material standing as
    an ordinary value does. A clean memoryview value and
    a clean mapping proxy value still release.
    """

    def test_hit_bytes_in_memoryview_value_beside_clean_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {"note": memoryview(hit), "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_text_in_memoryview_value_beside_clean_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {
                "note": memoryview(hit.decode("utf-8").encode("utf-8")),
                "content": "a routine clean note",
            }
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_bytes_under_mapping_proxy_value_beside_clean_refuses(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        proxy = types.MappingProxyType({"detail": hit})
        outcome = module.exit_scan(
            {"note": proxy, "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_bytes_as_key_inside_mapping_proxy_value_refuses(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        proxy = types.MappingProxyType({hit: "a routine clean note"})
        outcome = module.exit_scan(
            {"note": proxy, "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")

    def test_same_hit_as_ordinary_value_control_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = module.secret_bearing_shapes()[0]["raw_bytes"]
        outcome = module.exit_scan(
            {"note": hit, "content": "a routine clean note"}
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")

    def test_clean_memoryview_and_clean_proxy_values_still_release(self):
        module = require("ontoloop.redact")
        clean_proxy = types.MappingProxyType(
            {"detail": "a routine clean note"}
        )
        for value in (memoryview(b"a routine clean note"), clean_proxy):
            outcome = module.exit_scan(
                {"note": value, "content": "a routine clean note"}
            )
            self.assertFalse(outcome["refused"])


class TestConsumeFixR6DigestTypeDistinction(unittest.TestCase):
    """Fix round 6, ruling 105: digest type collisions.

    On both digest helpers, through ingest_tool and
    through load_with_hash_check, each probed pair of
    distinct materials returns differing digests, beside
    the charged pairs of ruling 61 still standing apart
    and string material still digesting as it did.
    """

    PAIRS = (
        (1, "1"),
        (0, "0"),
        (True, "true"),
        (False, "false"),
        (None, "null"),
        (1.5, "1.5"),
        ([1, 2], "[1, 2]"),
        ({"a": 1}, '{"a": 1}'),
        ((1, 2), [1, 2]),
    )

    def test_ingest_digest_pairs_stand_apart(self):
        module = require("ontoloop.service_layer")
        for first, second in self.PAIRS:
            self.assertNotEqual(
                _ingest_digest(module, first),
                _ingest_digest(module, second),
                "pair %r and %r" % (first, second),
            )

    def test_consumption_digest_pairs_stand_apart(self):
        module = require("ontoloop.consumption")
        for first, second in self.PAIRS:
            self.assertNotEqual(
                _consumption_digest(module, first),
                _consumption_digest(module, second),
                "pair %r and %r" % (first, second),
            )

    def test_the_two_helpers_agree_on_the_same_material(self):
        service = require("ontoloop.service_layer")
        consumption = require("ontoloop.consumption")
        for material in (1, None, [1, 2], {"a": 1}, (1, 2), "alpha",
                         b"alpha"):
            self.assertEqual(
                _ingest_digest(service, material),
                _consumption_digest(consumption, material),
            )

    def test_charged_pairs_of_ruling_61_still_stand_apart(self):
        module = require("ontoloop.service_layer")
        self.assertNotEqual(
            _ingest_digest(module, b"alpha"),
            _ingest_digest(module, "b'alpha'"),
        )
        self.assertNotEqual(
            _ingest_digest(module, None),
            _ingest_digest(module, "None"),
        )
        self.assertEqual(
            _ingest_digest(module, {"a": 1, "b": 2}),
            _ingest_digest(module, {"b": 2, "a": 1}),
        )

    def test_string_material_digest_stands_as_today(self):
        module = require("ontoloop.service_layer")
        for material in ("alpha", "a routine clean note", ""):
            self.assertEqual(
                _ingest_digest(module, material),
                hashlib.sha256(material.encode("utf-8")).hexdigest(),
            )


class TestConsumeFixR6SetDigestStability(unittest.TestCase):
    """Fix round 6, ruling 106: set bearing digest stability.

    The digest of a set of strings, and of a mapping
    holding a set of strings, stands the same under two
    differing process hash orderings, computed in child
    processes under two hash seeds, and the same as the
    digest computed in this process.
    """

    def _digest_in_process(self, hash_seed, expression):
        code = (
            "import sys; sys.path.insert(0, %r);"
            "from ontoloop import service_layer;"
            "print(service_layer.ingest_tool(%s)['material_digest'])"
            % (SYSTEM_ROOT, expression)
        )
        env = dict(os.environ)
        env["PYTHONHASHSEED"] = str(hash_seed)
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, env=env, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def test_set_digest_stable_across_process_orderings(self):
        expression = "{'beta', 'alpha', 'gamma'}"
        first = self._digest_in_process(0, expression)
        second = self._digest_in_process(1, expression)
        self.assertEqual(first, second)
        module = require("ontoloop.service_layer")
        self.assertEqual(
            first,
            _ingest_digest(module, {"beta", "alpha", "gamma"}),
        )

    def test_set_bearing_mapping_digest_stable_across_processes(self):
        expression = "{'k': {'beta', 'alpha', 'gamma'}}"
        first = self._digest_in_process(0, expression)
        second = self._digest_in_process(42, expression)
        self.assertEqual(first, second)
        module = require("ontoloop.consumption")
        self.assertEqual(
            first,
            _consumption_digest(module, {"k": {"beta", "alpha", "gamma"}}),
        )


class TestConsumeFixR6MappingKeyForms(unittest.TestCase):
    """Fix round 6, ruling 107: mixed and tuple key mappings.

    A mapping with mixed keys and a mapping with a tuple
    key meet a governed form at each digest surface,
    ingest_tool, load_with_hash_check,
    load_with_hash_mismatch, and verify_tool, with no
    exception, beside the standing mapping forms still
    returning their standing digests.
    """

    MIXED = None
    TUPLE_KEYED = None

    def _forms(self):
        return ({1: "a", "b": 2}, {(1, 2): "x"})

    def test_ingest_tool_meets_both_key_forms_without_exception(self):
        module = require("ontoloop.service_layer")
        for material in self._forms():
            result = module.ingest_tool(material)
            self.assertTrue(result["ingested"])
            self.assertEqual(len(result["material_digest"]), 64)

    def test_mixed_key_digest_ignores_entry_order(self):
        module = require("ontoloop.service_layer")
        first = _ingest_digest(module, {1: "a", "b": 2})
        second = _ingest_digest(module, {"b": 2, 1: "a"})
        self.assertEqual(first, second)

    def test_load_with_hash_check_meets_both_key_forms(self):
        module = require("ontoloop.consumption")
        for material in self._forms():
            outcome = module.load_with_hash_check(material)
            self.assertFalse(outcome["loaded"])
            self.assertEqual(outcome["position"], "unloadable")
            self.assertIn("load_refusal_record", outcome)
            matched = module.load_with_hash_check(
                material, expected_hash=outcome["computed_hash"]
            )
            self.assertTrue(matched["loaded"])

    def test_load_with_hash_mismatch_meets_both_key_forms(self):
        module = require("ontoloop.consumption")
        for material in self._forms():
            same = module.load_with_hash_mismatch(
                material, tool_material=material
            )
            self.assertTrue(same["loaded"])
            self.assertEqual(same["position"], "loadable")

    def test_verify_tool_meets_both_key_forms(self):
        module = require("ontoloop.service_layer")
        for material in self._forms():
            outcome = module.verify_tool(material)
            self.assertFalse(outcome["loaded"])
            self.assertEqual(outcome["position"], "unloadable")

    def test_standing_mapping_forms_still_return_standing_digests(self):
        module = require("ontoloop.service_layer")
        self.assertEqual(
            _ingest_digest(module, {"a": 1, "b": 2}),
            _ingest_digest(module, {"b": 2, "a": 1}),
        )
        self.assertNotEqual(
            _ingest_digest(module, {"a": 1}),
            _ingest_digest(module, {"a": 2}),
        )


if __name__ == "__main__":
    unittest.main()
