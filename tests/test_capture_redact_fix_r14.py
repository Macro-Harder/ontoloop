"""Fix round 14 tests for Region 5: capture and redact.

Written first for two positions at Round 14
triage ruling 504 point 5: ruling 491 (R14-CR-1,
with the StopIteration limb of Lead Engineer
line E-12 counted in it, the capture byte form
lengthless indexed access listing ending on the
StopIteration end signal of its container) and
ruling 492 (Lead Engineer line E-13, the redact
floor gathering on a keys view, values view, or
items view element of the state only mapping
standing inside a container element at the top
level). No test here pins the KeyError, ValueError,
or TypeError terminator forms as defects: those
forms stand in their parity standing at ruling
491 and stand pinned here as controls only. No
test here pins the iterator forms of the byte
form reading, whose position stands ruled not a
defect inside Round 11 ruling 353, and no test
here pins the payload form position ruled not a
defect inside Round 10 ruling 317. No act here
touches the material gathering act or the state
read act.
"""

import collections
import unittest

from tests.harness import require

CLEAN = "a routine clean note"
BIG = 40000
STATES = ("scan cannot run", "ready", "some unknown state")


class _StopIterationIndexedOnly:
    """A container carrying an indexed access act alone.

    The class stands in no sequence, set, mapping,
    view, or iterable form, and carries no length
    act and no iteration act of its own. Its access
    returns its elements in order and raises
    StopIteration past its last element, the end
    signal list() reads as the end of the listing.
    """

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        if index >= len(self._items):
            raise StopIteration
        return self._items[index]


class _StopIterationSubclass(StopIteration):
    """An end signal standing in a subclass of StopIteration."""


class _SubclassSignalIndexedOnly(_StopIterationIndexedOnly):
    """The lengthless form ending on a subclass end signal."""

    def __getitem__(self, index):
        if index >= len(self._items):
            raise _StopIterationSubclass
        return self._items[index]


class _IndexErrorIndexedOnly:
    """The lengthless form ending its listing on IndexError."""

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        return self._items[index]


class _KeyErrorIndexedOnly:
    """The lengthless form whose access raises KeyError at its end."""

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        if index >= len(self._items):
            raise KeyError(index)
        return self._items[index]


class _ValueErrorIndexedOnly:
    """The lengthless form whose access raises ValueError at its end."""

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        if index >= len(self._items):
            raise ValueError(index)
        return self._items[index]


class _TypeErrorIndexedOnly:
    """The lengthless form whose access raises TypeError at its end."""

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        if index >= len(self._items):
            raise TypeError(index)
        return self._items[index]


class _TwoActStopIteration:
    """A container carrying a length act beside its access act.

    Its access raises StopIteration past its last
    element. The two act form of the same reading
    decides this signal in substance in its standing
    form, as the Round 14 triage probes record.
    """

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        if index >= len(self._items):
            raise StopIteration
        return self._items[index]


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


class TestCaptureFixR14StopIterationListing(unittest.TestCase):
    """Ruling 491, R14-CR-1: the StopIteration end signal form."""

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

    def test_byte_form_of_stopiteration_container_states_content(
        self,
    ):
        module = require("ontoloop.capture")
        form = module._value_byte_form(
            _StopIterationIndexedOnly([b"ab", b"cde"])
        )
        self.assertEqual(form, b"abcde")

    def test_byte_form_counts_memoryview_in_stopiteration_container(
        self,
    ):
        module = require("ontoloop.capture")
        form = module._value_byte_form(
            _StopIterationIndexedOnly([memoryview(b"x" * 100)])
        )
        self.assertEqual(len(form), 100)

    def test_memoryview_stopiteration_container_mapping_value_refused(
        self,
    ):
        outcome = self._payload(
            _StopIterationIndexedOnly([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_small_memoryview_stopiteration_container_accepted(self):
        outcome = self._payload(
            _StopIterationIndexedOnly(
                [memoryview(b"a small clean note")]
            )
        )
        self._assert_accepted(outcome)

    def test_small_value_stopiteration_container_accepted(self):
        outcome = self._payload(_StopIterationIndexedOnly([CLEAN]))
        self._assert_accepted(outcome)

    def test_stopiteration_container_nested_in_list_refused(self):
        outcome = self._payload(
            [_StopIterationIndexedOnly([memoryview(b"x" * BIG)])]
        )
        self._assert_refused(outcome)

    def test_stopiteration_container_nested_in_list_small_accepted(
        self,
    ):
        outcome = self._payload(
            [_StopIterationIndexedOnly([CLEAN])]
        )
        self._assert_accepted(outcome)

    def test_subclass_signal_container_refused_on_oversize(self):
        outcome = self._payload(
            _SubclassSignalIndexedOnly([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_subclass_signal_container_accepted_on_small(self):
        outcome = self._payload(
            _SubclassSignalIndexedOnly([CLEAN])
        )
        self._assert_accepted(outcome)

    def test_stopiteration_container_nested_in_same_form_refused(
        self,
    ):
        outcome = self._payload(
            _StopIterationIndexedOnly(
                [_StopIterationIndexedOnly([memoryview(b"x" * BIG)])]
            )
        )
        self._assert_refused(outcome)

    def test_index_error_form_still_refuses_and_accepts(self):
        self._assert_refused(
            self._payload(
                _IndexErrorIndexedOnly([memoryview(b"x" * BIG)])
            )
        )
        self._assert_accepted(
            self._payload(_IndexErrorIndexedOnly([CLEAN]))
        )

    def test_two_act_stopiteration_form_still_decides_in_substance(
        self,
    ):
        self._assert_refused(
            self._payload(
                _TwoActStopIteration([memoryview(b"x" * BIG)])
            )
        )
        self._assert_accepted(
            self._payload(_TwoActStopIteration([CLEAN]))
        )

    def test_key_error_form_stands_in_parity(self):
        module = require("ontoloop.capture")
        with self.assertRaises(KeyError):
            module.capture_payload(
                {"note": _KeyErrorIndexedOnly([CLEAN])}
            )

    def test_value_error_form_stands_in_parity(self):
        module = require("ontoloop.capture")
        with self.assertRaises(ValueError):
            module.capture_payload(
                {"note": _ValueErrorIndexedOnly([CLEAN])}
            )

    def test_type_error_form_stands_in_parity(self):
        module = require("ontoloop.capture")
        with self.assertRaises(TypeError):
            module.capture_payload(
                {"note": _TypeErrorIndexedOnly([CLEAN])}
            )


class _SequenceContainer(collections.abc.Sequence):
    """A container element standing in the abstract sequence form."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]


class TestRedactFixR14FloorNestedViewElement(unittest.TestCase):
    """Ruling 492, Lead Engineer line E-13: the nested view forms."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def _scan(self, assembly):
        module = require("ontoloop.redact")
        return module.exit_scan(assembly)

    def test_tuple_keys_view_element_fails_closed_each_state(self):
        for state in STATES:
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan([(mapping.keys(),)])
                )

    def test_tuple_values_view_element_fails_closed_each_state(
        self,
    ):
        for state in STATES:
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan([(mapping.values(),)])
                )

    def test_tuple_items_view_element_fails_closed_each_state(self):
        for state in STATES:
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan([(mapping.items(),)])
                )

    def test_list_container_keys_view_element_fails_closed(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan([[mapping.keys()]])
                )

    def test_deque_container_keys_view_element_fails_closed(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan(
                        [collections.deque([mapping.keys()])]
                    )
                )

    def test_deque_container_values_view_element_fails_closed(
        self,
    ):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan(
                        [collections.deque([mapping.values()])]
                    )
                )

    def test_userlist_container_items_view_element_fails_closed(
        self,
    ):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan(
                        [collections.UserList([mapping.items()])]
                    )
                )

    def test_abstract_sequence_container_keys_view_fails_closed(
        self,
    ):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan(
                        [_SequenceContainer([mapping.keys()])]
                    )
                )

    def test_double_nested_tuple_keys_view_fails_closed(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan([((mapping.keys(),),)])
                )

    def test_floor_counts_no_content_on_nested_view_elements(self):
        module = require("ontoloop.redact")
        mapping = {"assembly_state": "some unknown state"}
        self.assertEqual(
            module._assembly_content(
                [(mapping.keys(),)], _skip_top_state=True
            ),
            [],
        )
        self.assertEqual(
            module._assembly_content(
                [(mapping.values(),)], _skip_top_state=True
            ),
            [],
        )
        self.assertEqual(
            module._assembly_content(
                [(mapping.items(),)], _skip_top_state=True
            ),
            [],
        )

    def test_floor_nested_view_counts_only_content_beside_state(
        self,
    ):
        module = require("ontoloop.redact")
        mapping = {"assembly_state": "ready", "content": CLEAN}
        self.assertEqual(
            module._assembly_content(
                [(mapping.keys(),)], _skip_top_state=True
            ),
            ["content"],
        )
        self.assertEqual(
            module._assembly_content(
                [(mapping.values(),)], _skip_top_state=True
            ),
            [CLEAN],
        )

    def test_nested_view_with_content_beside_state_releases(self):
        mapping = {"assembly_state": "ready", "content": CLEAN}
        outcome = self._scan([(mapping.keys(),)])
        self.assertFalse(outcome["refused"])

    def test_top_level_view_element_control_still_fails_closed(
        self,
    ):
        mapping = {"assembly_state": "some unknown state"}
        self._assert_fails_closed(self._scan([mapping.keys()]))
        self._assert_fails_closed(self._scan([mapping.values()]))

    def test_hit_as_state_value_beside_clean_content_refuses_whole(
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

    def test_clean_ready_assembly_with_real_content_releases(self):
        outcome = self._scan(
            [
                ("assembly_state", "ready"),
                ("content", CLEAN),
            ]
        )
        self.assertFalse(outcome["refused"])


if __name__ == "__main__":
    unittest.main()
