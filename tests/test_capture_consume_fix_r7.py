"""Fix round 7 tests for Region 6: capture, redact, consume, copy.

Written test first for the seven positions charged at Round 7
triage ruling 190 point 6: ruling 152 (G-05, _material_items
reading a memoryview value as the byte content it views),
ruling 153 (the family 2 gathering merged defect, Capture and
Redact finding 4.1 with Lead Engineer line E-8 counted in this
act and nowhere else, the gathering acts walking the probed
wrapper and view forms), ruling 154 (G-06, the exit scan state
read on a top level assembly standing in any walked mapping
form), ruling 170 (R7-CONSUME-1, one form for the byte like
family at every depth, on both digest helpers), ruling 171
(R7-CONSUME-2, the residual limb of the digest stating a
governed form, on both helpers), ruling 155 (ISO-R7-1, the
registry copy act on a deeply nested bundle), and ruling 156
(ISO-R7-2, the same copy act extended to the memoryview and
mapping proxy forms). Each class pins its act beside the
standing forms its charge protects. No test in this file pins
the generator form, which Round 6 ruling 133 rules NOT A
DEFECT on its first limb.
"""

import collections
import datetime
import decimal
import fractions
import hashlib
import os
import subprocess
import sys
import types
import unittest
from array import array

from tests.harness import require

SYSTEM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLEAN = "a routine clean note"


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


def _definite(classification):
    for layer in classification["firing_records"].values():
        for record in layer:
            if record["outcome"] == "definite":
                return True
    return False


def _ingest_digest(material):
    module = require("ontoloop.service_layer")
    return module.ingest_tool(material)["material_digest"]


def _consumption_digest(material):
    module = require("ontoloop.consumption")
    return module.load_with_hash_check(material)["computed_hash"]


class _ResidualProbe:
    """A residual value whose string form states no content."""

    def __init__(self, held):
        self.held = held

    def __str__(self):
        return "residual probe"


class TestRedactFixR7MaterialMemoryview(unittest.TestCase):
    """Fix round 7, ruling 152: a memoryview value in _material_items.

    classify_material decides on the byte content a memoryview
    views, at the top level, as a mapping value, and as a list
    element, as it decides on the same content standing as
    bytes and as a bytearray, and append_redacted redacts that
    content in its standing form.
    """

    def test_classify_top_level_memoryview_bytes_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self.assertTrue(_definite(module.classify_material(memoryview(hit))))

    def test_classify_top_level_memoryview_text_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        view = memoryview(hit.decode("utf-8").encode("utf-8"))
        self.assertTrue(_definite(module.classify_material(view)))

    def test_classify_memoryview_as_mapping_value_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        result = module.classify_material({"note": memoryview(hit)})
        self.assertTrue(_definite(result))

    def test_classify_memoryview_as_list_element_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        result = module.classify_material([memoryview(hit)])
        self.assertTrue(_definite(result))

    def test_classify_bytes_and_bytearray_controls_fire_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self.assertTrue(_definite(module.classify_material(hit)))
        self.assertTrue(_definite(module.classify_material(bytearray(hit))))

    def test_classify_clean_memoryview_stays_clean(self):
        module = require("ontoloop.redact")
        result = module.classify_material(memoryview(CLEAN.encode("utf-8")))
        self.assertFalse(_definite(result))

    def test_append_redacted_memoryview_redacts_the_hit(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        hit = _hit_bytes(module)
        store = store_module.golden_record_store()
        outcome = module.append_redacted(
            store, memoryview(hit), scope="run one"
        )
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 1)
        self.assertNotIn(
            hit.decode("utf-8"), outcome["redacted_material"]
        )
        journal = b"\n".join(
            record["canonical_bytes"] for record in store["records"]
        )
        self.assertNotIn(hit, journal)

    def test_append_redacted_mapping_memoryview_value_redacts(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        hit = _hit_bytes(module)
        store = store_module.golden_record_store()
        outcome = module.append_redacted(
            store, {"note": memoryview(hit)}, scope="run one"
        )
        self.assertTrue(outcome["appended"])
        self.assertEqual(outcome["hits_redacted"], 1)
        journal = b"\n".join(
            record["canonical_bytes"] for record in store["records"]
        )
        self.assertNotIn(hit, journal)


class TestRedactFixR7GatheringWrapperForms(unittest.TestCase):
    """Fix round 7, ruling 153: the gathering wrapper and view forms.

    Hit material standing in a deque, in a mapping view, in an
    array, in a UserDict, a UserList, a UserString, and in a
    ChainMap, in value position and in key position, beside
    clean content, refuses whole, as the same material standing
    as an ordinary value does. The clean forms of each still
    release, and the cured memoryview and mapping proxy forms
    still refuse whole.
    """

    def _scan(self, module, value):
        return module.exit_scan({"note": value, "content": CLEAN})

    def _assert_refuses_whole(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_in_deque_value_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, collections.deque([hit]))
        )
        self._assert_refuses_whole(
            self._scan(module, collections.deque([hit.decode("utf-8")]))
        )

    def test_hit_in_keys_view_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        view = {hit: CLEAN}.keys()
        self._assert_refuses_whole(self._scan(module, view))

    def test_hit_in_values_view_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        view = {"note": hit}.values()
        self._assert_refuses_whole(self._scan(module, view))

    def test_hit_in_items_view_refuses_whole_in_value_and_key(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, {"note": hit}.items())
        )
        self._assert_refuses_whole(
            self._scan(module, {hit: CLEAN}.items())
        )

    def test_hit_in_array_value_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, array("B", hit))
        )

    def test_hit_in_userdict_value_and_key_refuse_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, collections.UserDict({"note": hit}))
        )
        self._assert_refuses_whole(
            self._scan(module, collections.UserDict({hit: CLEAN}))
        )

    def test_hit_in_userdict_as_top_state_value_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        outcome = module.exit_scan(
            {
                "assembly_state": collections.UserDict({"note": hit}),
                "content": CLEAN,
            }
        )
        self._assert_refuses_whole(outcome)

    def test_hit_in_userlist_value_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, collections.UserList([hit]))
        )

    def test_hit_in_userstring_value_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, collections.UserString(hit.decode("utf-8")))
        )

    def test_hit_in_chainmap_value_and_key_refuse_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, collections.ChainMap({"note": hit}))
        )
        self._assert_refuses_whole(
            self._scan(module, collections.ChainMap({hit: CLEAN}))
        )

    def test_hit_as_userstring_key_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        outcome = module.exit_scan(
            {
                collections.UserString(hit.decode("utf-8")): CLEAN,
                "content": CLEAN,
            }
        )
        self._assert_refuses_whole(outcome)

    def test_memoryview_inside_deque_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, collections.deque([memoryview(hit)]))
        )

    def test_ordinary_value_control_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(self._scan(module, hit))

    def test_cured_memoryview_and_proxy_values_still_refuse_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        proxy = types.MappingProxyType({"detail": hit})
        for value in (memoryview(hit), proxy):
            self._assert_refuses_whole(self._scan(module, value))

    def test_clean_wrapper_and_view_forms_still_release(self):
        module = require("ontoloop.redact")
        clean_proxy = types.MappingProxyType({"detail": CLEAN})
        forms = (
            collections.deque([CLEAN.encode("utf-8")]),
            {CLEAN: "x"}.keys(),
            {"note": CLEAN.encode("utf-8")}.values(),
            {"note": CLEAN.encode("utf-8")}.items(),
            array("B", CLEAN.encode("utf-8")),
            collections.UserDict({"note": CLEAN.encode("utf-8")}),
            collections.UserList([CLEAN.encode("utf-8")]),
            collections.UserString(CLEAN),
            collections.ChainMap({"note": CLEAN.encode("utf-8")}),
            clean_proxy,
        )
        for value in forms:
            outcome = self._scan(module, value)
            self.assertFalse(
                outcome["refused"], "clean form released: %r" % (value,)
            )

    def test_cyclic_deque_beside_clean_fails_closed(self):
        module = require("ontoloop.redact")
        ring = collections.deque([CLEAN])
        ring.append(ring)
        outcome = self._scan(module, ring)
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )


class TestRedactFixR7ProxyStateRead(unittest.TestCase):
    """Fix round 7, ruling 154: the exit scan state read mapping forms.

    A top level assembly standing in any walked mapping form
    carrying the state scan cannot run beside clean content
    returns the fail closed form, as the same assembly standing
    as a plain mapping does.
    """

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def test_proxy_assembly_cannot_run_beside_clean_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = types.MappingProxyType(
            {"assembly_state": "scan cannot run", "content": CLEAN}
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_plain_mapping_cannot_run_control_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = {"assembly_state": "scan cannot run", "content": CLEAN}
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_userdict_assembly_cannot_run_beside_clean_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = collections.UserDict(
            {"assembly_state": "scan cannot run", "content": CLEAN}
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_chainmap_assembly_cannot_run_beside_clean_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = collections.ChainMap(
            {"assembly_state": "scan cannot run", "content": CLEAN}
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_proxy_assembly_carrying_hit_still_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        assembly = types.MappingProxyType(
            {"note": hit, "content": CLEAN}
        )
        outcome = module.exit_scan(assembly)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_proxy_state_only_assembly_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = types.MappingProxyType({"assembly_state": "ready"})
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_proxy_assembly_clean_content_still_releases(self):
        module = require("ontoloop.redact")
        assembly = types.MappingProxyType(
            {"assembly_state": "ready", "content": CLEAN}
        )
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])


class TestConsumeFixR7ByteFamilyDepth(unittest.TestCase):
    """Fix round 7, ruling 170: one byte like form at every depth.

    On both digest helpers the byte like family states one
    form at every depth: bytes, bytearray, and memoryview
    material of the same content return one digest at the top
    level and inside a list, a tuple, and a mapping value,
    beside the charged pairs of ruling 105 still standing
    apart and the string digest form still passing.
    """

    def test_top_level_byte_family_returns_one_digest_on_both(self):
        for digest in (_ingest_digest, _consumption_digest):
            self.assertEqual(digest(b"alpha"), digest(bytearray(b"alpha")))
            self.assertEqual(digest(b"alpha"), digest(memoryview(b"alpha")))
            self.assertEqual(
                digest(bytearray(b"alpha")), digest(memoryview(b"alpha"))
            )

    def test_nested_byte_family_returns_one_digest_on_both(self):
        for digest in (_ingest_digest, _consumption_digest):
            self.assertEqual(
                digest([b"alpha"]), digest([bytearray(b"alpha")])
            )
            self.assertEqual(
                digest([b"alpha"]), digest([memoryview(b"alpha")])
            )
            self.assertEqual(
                digest((b"alpha",)), digest((bytearray(b"alpha"),))
            )
            self.assertEqual(
                digest({"k": b"alpha"}),
                digest({"k": bytearray(b"alpha")}),
            )
            self.assertEqual(
                digest({"k": b"alpha"}),
                digest({"k": memoryview(b"alpha")}),
            )

    def test_the_two_helpers_agree_on_byte_family_material(self):
        for material in (b"alpha", bytearray(b"alpha"),
                         memoryview(b"alpha"), [bytearray(b"alpha")]):
            self.assertEqual(
                _ingest_digest(material), _consumption_digest(material)
            )

    def test_charged_pairs_of_ruling_105_still_stand_apart(self):
        for digest in (_ingest_digest, _consumption_digest):
            self.assertNotEqual(digest(1), digest("1"))
            self.assertNotEqual(digest((1, 2)), digest([1, 2]))
            self.assertNotEqual(digest({"a": 1}), digest('{"a": 1}'))
            self.assertNotEqual(digest([1]), digest(["1"]))

    def test_string_digest_form_still_passes(self):
        for material in ("alpha", CLEAN, ""):
            self.assertEqual(
                _ingest_digest(material),
                hashlib.sha256(material.encode("utf-8")).hexdigest(),
            )
            self.assertEqual(
                _consumption_digest(material),
                hashlib.sha256(material.encode("utf-8")).hexdigest(),
            )


class TestConsumeFixR7ResidualDigest(unittest.TestCase):
    """Fix round 7, ruling 171: the residual limb states a governed form.

    On both digest helpers, two content differing values of one
    residual type whose string form states no content return
    differing digests, a plain object returns one digest across
    processes, and the standing residual forms with content
    bearing string forms still decide as probed, beside the
    named families still deciding as pinned.
    """

    def test_content_differing_probe_values_stand_apart_on_both(self):
        for digest in (_ingest_digest, _consumption_digest):
            self.assertNotEqual(
                digest(_ResidualProbe(1)), digest(_ResidualProbe(2))
            )
            self.assertNotEqual(
                digest(_ResidualProbe([1])), digest(_ResidualProbe([2]))
            )
            self.assertEqual(
                digest(_ResidualProbe(1)), digest(_ResidualProbe(1))
            )

    def test_plain_object_digest_stable_in_process_on_both(self):
        for digest in (_ingest_digest, _consumption_digest):
            self.assertEqual(digest(object()), digest(object()))

    def test_plain_object_digest_stable_across_processes(self):
        code = (
            "import sys; sys.path.insert(0, %r);"
            "from ontoloop import service_layer;"
            "print(service_layer.ingest_tool(object())"
            "['material_digest'])"
            % (SYSTEM_ROOT,)
        )
        digests = []
        for seed in ("0", "42"):
            env = dict(os.environ)
            env["PYTHONHASHSEED"] = seed
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True, text=True, env=env, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            digests.append(result.stdout.strip())
        self.assertEqual(digests[0], digests[1])
        self.assertEqual(digests[0], _ingest_digest(object()))

    def test_content_bearing_residual_forms_still_decide_as_probed(self):
        neighbours = (
            (1 + 2j),
            decimal.Decimal("1.5"),
            fractions.Fraction(1, 2),
            datetime.date(2020, 1, 1),
            range(3),
        )
        for digest in (_ingest_digest, _consumption_digest):
            for value in neighbours:
                self.assertNotEqual(
                    digest(value), digest(str(value)),
                    "residual neighbour %r" % (value,),
                )
            self.assertNotEqual(
                digest(decimal.Decimal("1.5")),
                digest(decimal.Decimal("2.5")),
            )
            self.assertNotEqual(
                digest(range(3)), digest([0, 1, 2])
            )

    def test_named_families_still_decide_as_pinned(self):
        for digest in (_ingest_digest, _consumption_digest):
            self.assertNotEqual(digest(1), digest("1"))
            self.assertNotEqual(digest(None), digest("null"))
            self.assertEqual(
                digest({"a": 1, "b": 2}), digest({"b": 2, "a": 1})
            )


class TestConsumeFixR7RegistryCopyDepth(unittest.TestCase):
    """Fix round 7, ruling 155: the registry copy act at depth 500.

    A bundle nested to depth 500 records and discovers in the
    governed form, its copied form sharing no mutable state
    with the caller bundle in either direction at the deepest
    level, beside the standing registry pins still passing.
    """

    def _nested_bundle(self, depth):
        innermost = ["leaf"]
        bundle = innermost
        for _ in range(depth):
            bundle = [bundle]
        return bundle, innermost

    def _deepest(self, bundle, depth):
        current = bundle
        for _ in range(depth):
            current = current[0]
        return current

    def test_depth_500_bundle_records_and_discovers(self):
        module = require("ontoloop.consumption")
        bundle, innermost = self._nested_bundle(500)
        recorded = module.record_promotion("r7 depth workflow", bundle)
        self.assertTrue(recorded["recorded"])
        found = module.discover("r7 depth workflow")
        self.assertEqual(found["answer"], "promotion")
        deepest = self._deepest(found["bundle"], 500)
        self.assertEqual(deepest, ["leaf"])
        self.assertIsNot(deepest, innermost)

    def test_depth_500_caller_mutation_at_depth_reaches_no_discover(self):
        module = require("ontoloop.consumption")
        bundle, innermost = self._nested_bundle(500)
        module.record_promotion("r7 depth caller workflow", bundle)
        innermost.append("caller mutation")
        found = module.discover("r7 depth caller workflow")
        deepest = self._deepest(found["bundle"], 500)
        self.assertEqual(deepest, ["leaf"])

    def test_depth_500_return_mutation_at_depth_reaches_no_later(self):
        module = require("ontoloop.consumption")
        bundle, _innermost = self._nested_bundle(500)
        module.record_promotion("r7 depth return workflow", bundle)
        found = module.discover("r7 depth return workflow")
        deepest = self._deepest(found["bundle"], 500)
        deepest.append("return mutation")
        again = module.discover("r7 depth return workflow")
        deepest_again = self._deepest(again["bundle"], 500)
        self.assertEqual(deepest_again, ["leaf"])

    def test_standing_registry_forms_still_pass(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r7 standing workflow", "bundle version 1"
        )
        self.assertEqual(recorded["bundle"], "bundle version 1")
        found = module.discover("r7 standing workflow")
        self.assertEqual(found["bundle"], "bundle version 1")
        missing = module.discover("r7 never recorded workflow")
        self.assertEqual(missing["answer"], "no promotion")
        self.assertIsNone(missing["bundle"])


class TestConsumeFixR7RegistryCopyViewForms(unittest.TestCase):
    """Fix round 7, ruling 156: the copy act on view and proxy forms.

    A bundle carrying a memoryview or a mapping proxy part, at
    the top level and nested inside a mapping and a list,
    records and discovers in its readable substance, a mapping
    proxy copied as a fresh mapping of its entries and a
    memoryview copied as an independent mutable byte copy,
    sharing no mutable state with the caller part in either
    direction, beside the standing registry pins still passing.
    """

    def test_memoryview_top_level_bundle_records_and_discovers(self):
        module = require("ontoloop.consumption")
        buffer = bytearray(b"hello")
        recorded = module.record_promotion(
            "r7 mv top workflow", memoryview(buffer)
        )
        self.assertTrue(recorded["recorded"])
        self.assertEqual(bytes(recorded["bundle"]), b"hello")
        found = module.discover("r7 mv top workflow")
        self.assertEqual(bytes(found["bundle"]), b"hello")

    def test_proxy_top_level_bundle_records_and_discovers(self):
        module = require("ontoloop.consumption")
        proxy = types.MappingProxyType({"a": 1})
        recorded = module.record_promotion("r7 proxy top workflow", proxy)
        self.assertTrue(recorded["recorded"])
        self.assertEqual(recorded["bundle"], {"a": 1})
        found = module.discover("r7 proxy top workflow")
        self.assertEqual(found["bundle"], {"a": 1})

    def test_memoryview_in_mapping_and_list_isolated_both_directions(self):
        module = require("ontoloop.consumption")
        buffer = bytearray(b"hello")
        bundle = {"in_map": memoryview(buffer),
                  "in_list": ["x", memoryview(buffer)]}
        module.record_promotion("r7 mv nested workflow", bundle)
        buffer[:] = b"WORLD"
        found = module.discover("r7 mv nested workflow")
        self.assertEqual(bytes(found["bundle"]["in_map"]), b"hello")
        self.assertEqual(bytes(found["bundle"]["in_list"][1]), b"hello")
        found["bundle"]["in_map"][0] = ord("Z")
        found["bundle"]["in_list"][1][0] = ord("Z")
        self.assertEqual(bytes(buffer), b"WORLD")
        again = module.discover("r7 mv nested workflow")
        self.assertEqual(bytes(again["bundle"]["in_map"]), b"hello")
        self.assertEqual(bytes(again["bundle"]["in_list"][1]), b"hello")

    def test_proxy_in_mapping_and_list_isolated_both_directions(self):
        module = require("ontoloop.consumption")
        underlying = {"b": 2}
        proxy = types.MappingProxyType(underlying)
        bundle = {"in_map": proxy, "in_list": ["x", proxy]}
        module.record_promotion("r7 proxy nested workflow", bundle)
        underlying["b"] = 99
        underlying["c"] = 3
        found = module.discover("r7 proxy nested workflow")
        self.assertEqual(found["bundle"]["in_map"], {"b": 2})
        self.assertEqual(found["bundle"]["in_list"][1], {"b": 2})
        found["bundle"]["in_map"]["b"] = 7
        found["bundle"]["in_list"][1]["b"] = 8
        self.assertEqual(underlying, {"b": 99, "c": 3})
        again = module.discover("r7 proxy nested workflow")
        self.assertEqual(again["bundle"]["in_map"], {"b": 2})
        self.assertEqual(again["bundle"]["in_list"][1], {"b": 2})


if __name__ == "__main__":
    unittest.main()
