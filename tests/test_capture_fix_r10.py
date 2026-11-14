"""Fix round 10 tests for Region 4: capture measurement.

Written first for two positions at Round 10
triage ruling 334 point 4: ruling 317 (S15-R10-CR-1, the
capture payload byte form merged defect, with the
container limbs of Lead Engineer line E-9 counted in
this act and nowhere else) and ruling 318
(S15-R10-CR-2, the capture payload measurement of
mapping keys toward the journal line size). No test
here pins the payload form position ruled not a
defect at ruling 317.
"""

import collections
import collections.abc
import types
import unittest

from tests.harness import require

CLEAN = "a routine clean note"
BIG = 40000


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


class TestCaptureFixR10ByteFormContainers(unittest.TestCase):
    """Ruling 317: the byte form reading reads containers in substance."""

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

    def test_memoryview_in_deque_as_mapping_value_refused(self):
        outcome = self._payload(
            collections.deque([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_memoryview_in_userlist_as_mapping_value_refused(self):
        outcome = self._payload(
            collections.UserList([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_memoryview_in_userdict_as_mapping_value_refused(self):
        outcome = self._payload(
            collections.UserDict({"inner": memoryview(b"x" * BIG)})
        )
        self._assert_refused(outcome)

    def test_memoryview_in_chainmap_as_mapping_value_refused(self):
        outcome = self._payload(
            collections.ChainMap({"inner": memoryview(b"x" * BIG)})
        )
        self._assert_refused(outcome)

    def test_memoryview_in_mapping_proxy_as_mapping_value_refused(self):
        outcome = self._payload(
            types.MappingProxyType({"inner": memoryview(b"x" * BIG)})
        )
        self._assert_refused(outcome)

    def test_bytes_in_abstract_sequence_as_mapping_value_refused(self):
        outcome = self._payload(_AbstractSequence([b"x" * BIG]))
        self._assert_refused(outcome)

    def test_memoryview_in_abstract_sequence_as_mapping_value_refused(self):
        outcome = self._payload(
            _AbstractSequence([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_string_in_abstract_sequence_as_mapping_value_refused(self):
        outcome = self._payload(_AbstractSequence(["x" * BIG]))
        self._assert_refused(outcome)

    def test_bytes_in_abstract_set_as_mapping_value_refused(self):
        outcome = self._payload(_AbstractSet([b"x" * BIG]))
        self._assert_refused(outcome)

    def test_memoryview_in_abstract_set_as_mapping_value_refused(self):
        outcome = self._payload(
            _AbstractSet([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_string_in_abstract_set_as_mapping_value_refused(self):
        outcome = self._payload(_AbstractSet(["x" * BIG]))
        self._assert_refused(outcome)

    def test_bytes_in_abstract_mapping_as_mapping_value_refused(self):
        outcome = self._payload(
            _AbstractMapping({"inner": b"x" * BIG})
        )
        self._assert_refused(outcome)

    def test_memoryview_in_abstract_mapping_as_mapping_value_refused(self):
        outcome = self._payload(
            _AbstractMapping({"inner": memoryview(b"x" * BIG)})
        )
        self._assert_refused(outcome)

    def test_string_in_abstract_mapping_as_mapping_value_refused(self):
        outcome = self._payload(
            _AbstractMapping({"inner": "x" * BIG})
        )
        self._assert_refused(outcome)

    def test_memoryview_in_ordereddict_as_mapping_value_refused(self):
        outcome = self._payload(
            collections.OrderedDict({"inner": memoryview(b"x" * BIG)})
        )
        self._assert_refused(outcome)

    def test_memoryview_nested_deque_inside_list_refused(self):
        outcome = self._payload(
            [collections.deque([memoryview(b"x" * BIG)])]
        )
        self._assert_refused(outcome)

    def test_small_memoryview_in_deque_accepted(self):
        outcome = self._payload(
            collections.deque([memoryview(b"a small clean note")])
        )
        self._assert_accepted(outcome)

    def test_small_value_in_abstract_sequence_accepted(self):
        outcome = self._payload(_AbstractSequence([CLEAN]))
        self._assert_accepted(outcome)

    def test_small_value_in_abstract_mapping_accepted(self):
        outcome = self._payload(_AbstractMapping({"inner": CLEAN}))
        self._assert_accepted(outcome)

    def test_cyclic_deque_small_memoryview_accepted_no_hang(self):
        container = collections.deque()
        container.append(memoryview(b"a small clean note"))
        container.append(container)
        outcome = self._payload(container)
        self._assert_accepted(outcome)

    def test_cyclic_abstract_sequence_small_value_accepted_no_hang(self):
        container = _AbstractSequence([CLEAN])
        container._data.append(container)
        outcome = self._payload(container)
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


class TestCaptureFixR10JournalLineKeyCounting(unittest.TestCase):
    """Ruling 318: keys count toward the journal line size."""

    def _assert_refused(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["accepted"])
        self.assertFalse(outcome["truncation_written"])
        self.assertFalse(outcome["partial_record_written"])

    def _assert_accepted(self, outcome):
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["refused"])

    def test_four_keys_20000_each_refused(self):
        module = require("ontoloop.capture")
        payload = {}
        for letter in ("a", "b", "c", "d"):
            payload[letter * 20000] = CLEAN
        outcome = module.capture_payload(payload)
        self._assert_refused(outcome)

    def test_two_keys_30000_beside_two_values_30000_refused(self):
        module = require("ontoloop.capture")
        payload = {
            "a" * 30000: b"v" * 30000,
            "b" * 30000: b"w" * 30000,
        }
        outcome = module.capture_payload(payload)
        self._assert_refused(outcome)

    def test_single_small_key_payload_accepted(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload({"note": CLEAN})
        self._assert_accepted(outcome)

    def test_two_keys_20000_each_beside_small_values_accepted(self):
        module = require("ontoloop.capture")
        payload = {
            ("a" * 20000): CLEAN,
            ("b" * 20000): CLEAN,
        }
        outcome = module.capture_payload(payload)
        self._assert_accepted(outcome)

    def test_one_key_20000_beside_one_value_20000_accepted(self):
        module = require("ontoloop.capture")
        payload = {"k" * 20000: "v" * 20000}
        outcome = module.capture_payload(payload)
        self._assert_accepted(outcome)

    def test_single_key_40000_still_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload({"k" * 40000: CLEAN})
        self._assert_refused(outcome)

    def test_standing_two_field_payloads_decide_as_they_stand(self):
        module = require("ontoloop.capture")
        at_cap = module.capture_payload("at cap")
        self._assert_accepted(at_cap)
        over_cap = module.capture_payload("over cap")
        self._assert_refused(over_cap)


if __name__ == "__main__":
    unittest.main()
