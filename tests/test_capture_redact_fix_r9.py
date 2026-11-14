"""Fix round 9 tests for Region 5: capture and redaction.

Written first for six positions at Round 9
triage ruling 295 point 5: ruling 259 (S15-R9-CR-1, the
computation inputs hash guard), ruling 260 (S15-R9-CR-2,
the shared rule hash guard), ruling 275 (the material
reading merged defect, S15-R9-CR-3 with R9-CONSUME-2,
R9-CONSUME-3, and R9-CONSUME-4 counted in this act and
nowhere else), ruling 276 (S15-R9-CR-4, the exit scan
abstract set form), ruling 277 (S15-R9-CR-5, the capture
payload measurement), and ruling 278 (the state read
merged defect, S15-R9-CR-6 with Lead Engineer line E-11
counted in this act and nowhere else). No test here pins the generator
form ruled not a defect at Round 6 ruling 133.
"""

import array
import collections
import collections.abc
import unittest

from tests.harness import require

CLEAN = "a routine clean note"


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


def _definite(classification):
    if "firing_records" not in classification:
        return False
    for layer in classification["firing_records"].values():
        for record in layer:
            if record["outcome"] == "definite":
                return True
    return False


class _AbstractSequence(collections.abc.Sequence):
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)


class _AbstractSet(collections.abc.Set):
    def __init__(self, data):
        self._data = set(data)

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class _SetSubclass(set):
    pass


class _FrozensetSubclass(frozenset):
    pass


class TestCaptureFixR9ComputationInputsHashGuard(unittest.TestCase):
    """Ruling 259: a name whose hashing raises ValueError."""

    def test_writable_memoryview_name_raises_governed_form(self):
        module = require("ontoloop.capture")
        name = memoryview(bytearray(b"signature"))
        with self.assertRaises(ValueError) as caught:
            module.computation_inputs(name)
        self.assertEqual(
            str(caught.exception), "unknown computation: %r" % (name,)
        )

    def test_list_name_raises_governed_form(self):
        module = require("ontoloop.capture")
        with self.assertRaises(ValueError) as caught:
            module.computation_inputs(["signature"])
        self.assertEqual(
            str(caught.exception), "unknown computation: ['signature']"
        )

    def test_standing_names_return_input_tuples(self):
        module = require("ontoloop.capture")
        self.assertEqual(
            module.computation_inputs("signature"),
            (
                "review target identity",
                "task kind",
                "template or instruction version in force",
                "signature version",
            ),
        )
        self.assertEqual(
            module.computation_inputs("group_key"),
            (
                "review target identity",
                "task kind",
                "template or instruction version in force",
            ),
        )
        self.assertEqual(
            module.computation_inputs("pool_stamp"),
            ("store sequence order", "group first acceptance"),
        )


class TestRedactFixR9SharedRuleHashGuard(unittest.TestCase):
    """Ruling 260: a layer whose hashing raises ValueError."""

    def test_writable_memoryview_layer_raises_governed_form(self):
        module = require("ontoloop.redact")
        layer = memoryview(bytearray(b"one"))
        with self.assertRaises(ValueError) as caught:
            module.shared_rule(layer)
        self.assertEqual(
            str(caught.exception), "unknown layer: %r" % (layer,)
        )

    def test_list_layer_raises_governed_form(self):
        module = require("ontoloop.redact")
        with self.assertRaises(ValueError) as caught:
            module.shared_rule([1])
        self.assertEqual(str(caught.exception), "unknown layer: [1]")

    def test_standing_layers_return_six_distinct_rules(self):
        module = require("ontoloop.redact")
        rules = [module.shared_rule(layer) for layer in range(1, 7)]
        self.assertEqual(len(rules), 6)
        self.assertEqual(len(set(rules)), 6)


class TestRedactFixR9MaterialUnenumeratedContainers(unittest.TestCase):
    """Ruling 275: container forms _material_items did not name."""

    def _hit(self):
        return _hit_bytes(require("ontoloop.redact"))

    def _fires(self, material):
        module = require("ontoloop.redact")
        return _definite(module.classify_material(material))

    def test_hit_in_abstract_sequence_top_level_fires(self):
        self.assertTrue(self._fires(_AbstractSequence([self._hit()])))

    def test_hit_in_abstract_sequence_as_mapping_value_fires(self):
        material = {"note": _AbstractSequence([self._hit()])}
        self.assertTrue(self._fires(material))

    def test_hit_text_in_abstract_sequence_in_list_fires(self):
        hit_text = self._hit().decode("utf-8")
        self.assertTrue(self._fires([_AbstractSequence([hit_text])]))

    def test_mv_in_abstract_sequence_fires(self):
        material = _AbstractSequence([memoryview(self._hit())])
        self.assertTrue(self._fires(material))

    def test_hit_in_abstract_set_top_level_fires(self):
        self.assertTrue(self._fires(_AbstractSet([self._hit()])))

    def test_hit_in_abstract_set_as_mapping_value_fires(self):
        self.assertTrue(self._fires({"note": _AbstractSet([self._hit()])}))

    def test_hit_in_byte_array_signed_top_level_fires(self):
        self.assertTrue(self._fires(array.array("b", self._hit())))

    def test_hit_in_byte_array_unsigned_as_mapping_value_fires(self):
        material = {"note": array.array("B", self._hit())}
        self.assertTrue(self._fires(material))

    def test_hit_in_byte_array_inside_list_fires(self):
        self.assertTrue(self._fires([array.array("b", self._hit())]))

    def test_mv_in_values_view_as_mapping_value_fires(self):
        inner = {"detail": memoryview(self._hit())}
        self.assertTrue(self._fires({"note": inner.values()}))

    def test_mv_in_items_view_top_level_fires(self):
        material = {"detail": memoryview(self._hit())}.items()
        self.assertTrue(self._fires(material))

    def test_mv_as_key_in_keys_view_fires(self):
        material = {memoryview(self._hit()): CLEAN}.keys()
        self.assertTrue(self._fires(material))

    def test_mv_in_userdict_values_view_as_mapping_value_fires(self):
        wrapped = collections.UserDict({"detail": memoryview(self._hit())})
        self.assertTrue(self._fires({"note": wrapped.values()}))

    def test_append_abstract_sequence_hit_not_appended_unexamined(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        hit = _hit_bytes(module)
        store = store_module.golden_record_store()
        outcome = module.append_redacted(
            store, _AbstractSequence([hit]), scope="run one"
        )
        self.assertTrue(outcome["refused"] or outcome["hits_redacted"] == 1)
        journal = b"\n".join(
            record["canonical_bytes"] for record in store["records"]
        )
        self.assertNotIn(hit, journal)

    def test_append_byte_array_hit_not_appended_unexamined(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        hit = _hit_bytes(module)
        store = store_module.golden_record_store()
        outcome = module.append_redacted(
            store, array.array("b", hit), scope="run one"
        )
        self.assertTrue(outcome["refused"] or outcome["hits_redacted"] == 1)
        journal = b"\n".join(
            record["canonical_bytes"] for record in store["records"]
        )
        self.assertNotIn(hit, journal)

    def test_clean_forms_stay_clean(self):
        module = require("ontoloop.redact")
        clean = CLEAN.encode("utf-8")
        forms = (
            _AbstractSequence([clean]),
            {"note": _AbstractSequence([clean])},
            _AbstractSet([clean]),
            {"note": _AbstractSet([clean])},
            array.array("b", clean),
            {"note": array.array("B", clean)},
            [array.array("b", clean)],
            {"note": {"detail": memoryview(clean)}.values()},
            {"detail": memoryview(clean)}.items(),
            {memoryview(clean): CLEAN}.keys(),
            {
                "note": collections.UserDict(
                    {"detail": memoryview(clean)}
                ).values()
            },
        )
        for material in forms:
            self.assertFalse(
                _definite(module.classify_material(material)),
                "clean form fired: %r" % (material,),
            )


class TestRedactFixR9ExitScanAbstractSet(unittest.TestCase):
    """Ruling 276: the exit scan gathering and the abstract set."""

    def _scan(self, module, value):
        return module.exit_scan({"note": value, "content": CLEAN})

    def _assert_refuses_whole(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_in_abstract_set_nested_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(self._scan(module, _AbstractSet([hit])))

    def test_hit_in_abstract_set_inside_list_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, [_AbstractSet([hit])])
        )

    def test_hit_in_abstract_set_inside_abstract_sequence_refuses(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, _AbstractSequence([_AbstractSet([hit])]))
        )

    def test_readonly_mv_in_abstract_set_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, _AbstractSet([memoryview(hit)]))
        )

    def test_clean_abstract_set_releases(self):
        module = require("ontoloop.redact")
        clean = CLEAN.encode("utf-8")
        outcome = self._scan(module, _AbstractSet([clean]))
        self.assertFalse(outcome["refused"])

    def test_set_subclass_controls_refuse_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(self._scan(module, _SetSubclass([hit])))
        self._assert_refuses_whole(
            self._scan(module, _FrozensetSubclass([hit]))
        )


class TestCaptureFixR9PayloadMeasurement(unittest.TestCase):
    """Ruling 277: the measurement reads values and keys in full."""

    def _assert_refused(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["accepted"])
        self.assertFalse(outcome["truncation_written"])
        self.assertFalse(outcome["partial_record_written"])

    def test_memoryview_value_40000_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": memoryview(b"x" * 40000)}
        )
        self._assert_refused(outcome)

    def test_memoryview_value_70000_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": memoryview(b"x" * 70000)}
        )
        self._assert_refused(outcome)

    def test_memoryview_nested_in_list_value_40000_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": [memoryview(b"x" * 40000)]}
        )
        self._assert_refused(outcome)

    def test_key_40000_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload({"k" * 40000: CLEAN})
        self._assert_refused(outcome)

    def test_key_70000_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload({"k" * 70000: CLEAN})
        self._assert_refused(outcome)

    def test_small_memoryview_value_accepted(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": memoryview(b"a small clean note")}
        )
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["refused"])

    def test_standing_two_field_payloads_decide_as_they_stand(self):
        module = require("ontoloop.capture")
        at_cap = module.capture_payload("at cap")
        self.assertTrue(at_cap["accepted"])
        self.assertFalse(at_cap["refused"])
        over_cap = module.capture_payload("over cap")
        self._assert_refused(over_cap)


class TestRedactFixR9StateReadSequenceOfPairs(unittest.TestCase):
    """Ruling 278: the state read on a sequence of pairs assembly."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def test_list_of_pairs_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            ("assembly_state", "scan cannot run"),
            ("content", CLEAN),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_tuple_of_pairs_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = (
            ("assembly_state", "scan cannot run"),
            ("content", CLEAN),
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_set_of_pairs_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = {
            ("assembly_state", "scan cannot run"),
            ("content", CLEAN),
        }
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_userlist_of_pairs_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = collections.UserList(
            [
                ("assembly_state", "scan cannot run"),
                ("content", CLEAN),
            ]
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_hit_pair_form_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        outcome = module.exit_scan([("note", hit), ("content", CLEAN)])
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_ready_pair_form_releases(self):
        module = require("ontoloop.redact")
        assembly = [("assembly_state", "ready"), ("content", CLEAN)]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_clean_pair_list_without_state_entry_releases(self):
        module = require("ontoloop.redact")
        assembly = [("note", CLEAN), ("content", CLEAN)]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])


if __name__ == "__main__":
    unittest.main()
