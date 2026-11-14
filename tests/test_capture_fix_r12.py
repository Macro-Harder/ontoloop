"""Fix round 12 tests for Region 6: capture and redact.

Written first for two positions at Round 12
triage ruling 415 point 6: ruling 405 (S15-R12-CR-1
with Lead Engineer line E-7 counted in this act and
nowhere else, the capture payload byte form reading
of a ChainMap shadowed entry and of a container
form that iterates by indexed access alone) and
ruling 406 (S15-R12-CR-2, the redact floor gathering
honouring the top level state skip in every branch
it walks). No test here pins the iterator forms of
the byte form reading, whose position stands ruled
not a defect inside Round 11 ruling 353, and no
test here pins the payload form position ruled not
a defect inside Round 10 ruling 317. No act here
touches the material gathering act or the state
read act.
"""

import collections
import collections.abc
import types
import unittest

from tests.harness import require

CLEAN = "a routine clean note"
BIG = 40000


class _IndexedOnly:
    """A container carrying a length act and an indexed access act alone.

    The class stands in no sequence, set, mapping,
    view, or iterable form, and carries no iteration
    act of its own.
    """

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)


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


class _AbstractMapping(collections.abc.Mapping):
    def __init__(self, data):
        self._data = dict(data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


class TestCaptureFixR12ChainMapShadowed(unittest.TestCase):
    """Ruling 405, ChainMap limb: every chained map stands read."""

    def _assert_refused(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["accepted"])
        self.assertFalse(outcome["truncation_written"])
        self.assertFalse(outcome["partial_record_written"])

    def _assert_accepted(self, outcome):
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["refused"])

    def _payload(self, value):
        module = require("ontoloop.capture")
        return module.capture_payload({"note": value})

    def test_shadowed_memoryview_as_mapping_value_refused(self):
        outcome = self._payload(
            collections.ChainMap(
                {"a": b"a small value"},
                {"a": memoryview(b"x" * BIG)},
            )
        )
        self._assert_refused(outcome)

    def test_shadowed_memoryview_inside_tuple_refused(self):
        outcome = self._payload(
            (
                collections.ChainMap(
                    {"a": b"a small value"},
                    {"a": memoryview(b"x" * BIG)},
                ),
            )
        )
        self._assert_refused(outcome)

    def test_shadowed_bytes_as_mapping_value_refused(self):
        outcome = self._payload(
            collections.ChainMap(
                {"a": b"a small value"},
                {"a": b"x" * BIG},
            )
        )
        self._assert_refused(outcome)

    def test_shadowed_string_as_mapping_value_refused(self):
        outcome = self._payload(
            collections.ChainMap(
                {"a": "a small value"},
                {"a": "x" * BIG},
            )
        )
        self._assert_refused(outcome)

    def test_shadowed_entry_in_third_map_refused(self):
        outcome = self._payload(
            collections.ChainMap(
                {"a": b"a small value"},
                {"b": b"another small value"},
                {"a": memoryview(b"x" * BIG)},
            )
        )
        self._assert_refused(outcome)

    def test_byte_form_reads_every_chained_map_in_substance(self):
        module = require("ontoloop.capture")
        form = module._value_byte_form(
            collections.ChainMap(
                {"a": b"small"},
                {"a": b"x" * 100},
            )
        )
        self.assertEqual(len(form), len("a") + 5 + len("a") + 100)

    def test_small_shadowed_memoryview_accepted(self):
        outcome = self._payload(
            collections.ChainMap(
                {"a": b"a small value"},
                {"a": memoryview(b"a small clean note")},
            )
        )
        self._assert_accepted(outcome)

    def test_distinct_key_in_second_map_control_refused(self):
        outcome = self._payload(
            collections.ChainMap(
                {"a": b"a small value"},
                {"b": memoryview(b"x" * BIG)},
            )
        )
        self._assert_refused(outcome)

    def test_first_map_memoryview_control_refused(self):
        outcome = self._payload(
            collections.ChainMap(
                {"a": memoryview(b"x" * BIG)},
                {"a": b"a small value"},
            )
        )
        self._assert_refused(outcome)

    def test_distinct_key_40000_control_refused(self):
        outcome = self._payload(
            collections.ChainMap(
                {"a": b"a small value"},
                {"k" * BIG: CLEAN},
            )
        )
        self._assert_refused(outcome)

    def test_ordereddict_control_refused(self):
        outcome = self._payload(
            collections.OrderedDict(
                {"inner": memoryview(b"x" * BIG)}
            )
        )
        self._assert_refused(outcome)

    def test_mapping_proxy_control_refused(self):
        outcome = self._payload(
            types.MappingProxyType(
                {"inner": memoryview(b"x" * BIG)}
            )
        )
        self._assert_refused(outcome)

    def test_cyclic_chainmap_small_accepted_no_hang(self):
        chain = collections.ChainMap({"a": b"a small value"})
        chain.maps.append({"b": chain})
        outcome = self._payload(chain)
        self._assert_accepted(outcome)

    def test_standing_capture_payload_pins_still_pass(self):
        module = require("ontoloop.capture")
        small = module.capture_payload(
            {"note": memoryview(b"a small clean note")}
        )
        self._assert_accepted(small)
        at_cap = module.capture_payload("at cap")
        self._assert_accepted(at_cap)
        over_cap = module.capture_payload("over cap")
        self._assert_refused(over_cap)


class TestCaptureFixR12IndexedAccess(unittest.TestCase):
    """Ruling 405, Lead Engineer line E-7: the indexed access form."""

    def _assert_refused(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["accepted"])
        self.assertFalse(outcome["truncation_written"])
        self.assertFalse(outcome["partial_record_written"])

    def _assert_accepted(self, outcome):
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["refused"])

    def _payload(self, value):
        module = require("ontoloop.capture")
        return module.capture_payload({"note": value})

    def test_memoryview_in_indexed_container_as_mapping_value_refused(self):
        outcome = self._payload(
            _IndexedOnly([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_bytes_in_indexed_container_as_mapping_value_refused(self):
        outcome = self._payload(_IndexedOnly([b"x" * BIG]))
        self._assert_refused(outcome)

    def test_string_in_indexed_container_as_mapping_value_refused(self):
        outcome = self._payload(_IndexedOnly(["x" * BIG]))
        self._assert_refused(outcome)

    def test_mapping_value_in_indexed_container_refused(self):
        outcome = self._payload(
            _IndexedOnly([{"inner": memoryview(b"x" * BIG)}])
        )
        self._assert_refused(outcome)

    def test_memoryview_nested_indexed_container_inside_list_refused(self):
        outcome = self._payload(
            [_IndexedOnly([memoryview(b"x" * BIG)])]
        )
        self._assert_refused(outcome)

    def test_byte_form_of_indexed_container_states_its_content(self):
        module = require("ontoloop.capture")
        form = module._value_byte_form(
            _IndexedOnly([b"ab", b"cd"])
        )
        self.assertEqual(form, b"abcd")

    def test_small_memoryview_in_indexed_container_accepted(self):
        outcome = self._payload(
            _IndexedOnly([memoryview(b"a small clean note")])
        )
        self._assert_accepted(outcome)

    def test_small_value_in_indexed_container_accepted(self):
        outcome = self._payload(_IndexedOnly([CLEAN]))
        self._assert_accepted(outcome)

    def test_cyclic_indexed_container_small_accepted_no_hang(self):
        container = _IndexedOnly([memoryview(b"a small clean note")])
        container._items.append(container)
        outcome = self._payload(container)
        self._assert_accepted(outcome)

    def test_plain_list_control_refused(self):
        outcome = self._payload([memoryview(b"x" * BIG)])
        self._assert_refused(outcome)


class TestRedactFixR12FloorStateSkip(unittest.TestCase):
    """Ruling 406: the floor gathering honours the state skip in full."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def _scan(self, assembly):
        module = require("ontoloop.redact")
        return module.exit_scan(assembly)

    def _state_only_forms(self, value):
        pair = ("assembly_state", value)
        mapping = {"assembly_state": value}
        return {
            "list": [pair],
            "tuple": (pair,),
            "set": {pair},
            "deque": collections.deque([pair]),
            "userlist": collections.UserList([pair]),
            "abstract sequence": _AbstractSequence([pair]),
            "abstract set": _AbstractSet([pair]),
            "keys view": mapping.keys(),
            "values view": mapping.values(),
            "items view": mapping.items(),
        }

    def test_list_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan([("assembly_state", "some unknown state")])
        )

    def test_tuple_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan((("assembly_state", "some unknown state"),))
        )

    def test_set_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan({("assembly_state", "some unknown state")})
        )

    def test_deque_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan(
                collections.deque(
                    [("assembly_state", "some unknown state")]
                )
            )
        )

    def test_userlist_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan(
                collections.UserList(
                    [("assembly_state", "some unknown state")]
                )
            )
        )

    def test_abstract_sequence_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan(
                _AbstractSequence(
                    [("assembly_state", "some unknown state")]
                )
            )
        )

    def test_abstract_set_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan(
                _AbstractSet(
                    [("assembly_state", "some unknown state")]
                )
            )
        )

    def test_keys_view_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan({"assembly_state": "some unknown state"}.keys())
        )

    def test_values_view_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan(
                {"assembly_state": "some unknown state"}.values()
            )
        )

    def test_items_view_state_only_unknown_fails_closed(self):
        self._assert_fails_closed(
            self._scan({"assembly_state": "some unknown state"}.items())
        )

    def test_every_form_ready_state_fails_closed(self):
        for name, assembly in self._state_only_forms("ready").items():
            with self.subTest(form=name):
                self._assert_fails_closed(self._scan(assembly))

    def test_every_form_planted_label_fails_closed(self):
        forms = self._state_only_forms("planted uncleared hit")
        for name, assembly in forms.items():
            with self.subTest(form=name):
                self._assert_fails_closed(self._scan(assembly))

    def test_every_form_empty_state_value_fails_closed(self):
        for name, assembly in self._state_only_forms("").items():
            with self.subTest(form=name):
                self._assert_fails_closed(self._scan(assembly))

    def test_floor_gathering_counts_no_content_on_state_only_forms(self):
        module = require("ontoloop.redact")
        forms = self._state_only_forms("some unknown state")
        for name, assembly in forms.items():
            with self.subTest(form=name):
                self.assertEqual(
                    module._assembly_content(
                        assembly, _skip_top_state=True
                    ),
                    [],
                )

    def test_mapping_controls_still_fail_closed(self):
        controls = {
            "plain mapping": {"assembly_state": "some unknown state"},
            "mapping proxy": types.MappingProxyType(
                {"assembly_state": "some unknown state"}
            ),
            "userdict": collections.UserDict(
                {"assembly_state": "some unknown state"}
            ),
            "abstract mapping": _AbstractMapping(
                {"assembly_state": "some unknown state"}
            ),
            "plain mapping empty value": {"assembly_state": ""},
        }
        for name, assembly in controls.items():
            with self.subTest(form=name):
                self._assert_fails_closed(self._scan(assembly))

    def test_hit_as_state_value_in_pair_form_beside_content_refuses_whole(
        self,
    ):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        assembly = [
            ("assembly_state", hit),
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_as_state_value_in_items_view_pair_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        assembly = [
            {"assembly_state": hit}.items(),
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_ready_pair_beside_clean_content_still_releases(self):
        outcome = self._scan(
            [
                ("assembly_state", "ready"),
                ("content", CLEAN),
            ]
        )
        self.assertFalse(outcome["refused"])

    def test_values_view_with_clean_content_beside_state_releases(self):
        outcome = self._scan(
            {
                "assembly_state": "some unknown state",
                "content": CLEAN,
            }.values()
        )
        self.assertFalse(outcome["refused"])

    def test_items_view_with_clean_content_beside_state_releases(self):
        outcome = self._scan(
            {
                "assembly_state": "some unknown state",
                "content": CLEAN,
            }.items()
        )
        self.assertFalse(outcome["refused"])

    def test_keys_view_with_clean_key_beside_state_releases(self):
        outcome = self._scan(
            {
                "assembly_state": "some unknown state",
                "content": CLEAN,
            }.keys()
        )
        self.assertFalse(outcome["refused"])

    def test_cannot_run_pair_beside_clean_content_still_fails_closed(
        self,
    ):
        self._assert_fails_closed(
            self._scan(
                [
                    ("assembly_state", "scan cannot run"),
                    ("content", CLEAN),
                ]
            )
        )

    def test_unknown_state_mapping_beside_clean_content_releases(self):
        outcome = self._scan(
            {
                "assembly_state": "some unknown state",
                "content": CLEAN,
            }
        )
        self.assertFalse(outcome["refused"])


if __name__ == "__main__":
    unittest.main()
