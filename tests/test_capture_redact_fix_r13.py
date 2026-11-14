"""Fix round 13 tests for Region 5: capture and redact.

Written first for two positions at Round 13
triage ruling 459 point 5: ruling 448 (Lead
Engineer line E-13, the capture payload byte form
reading of a container form that iterates by
indexed access without a length act) and ruling
449 (Lead Engineer line E-14, the redact floor
gathering on a top level element standing as the
keys view or the values view of a state only
mapping). No test here pins the iterator forms of
the byte form reading, whose position stands ruled
not a defect inside Round 11 ruling 353, and no
test here pins the payload form position ruled not
a defect inside Round 10 ruling 317. No act here
touches the material gathering act or the state
read act.
"""

import collections
import unittest

from tests.harness import require

CLEAN = "a routine clean note"
BIG = 40000


class _LengthlessIndexedOnly:
    """A container carrying an indexed access act alone.

    The class stands in no sequence, set, mapping,
    view, or iterable form, and carries no length
    act and no iteration act of its own. Its
    elements stand read by indexed access alone,
    in the form the cross split acts of this system
    read.
    """

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        return self._items[index]


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


class TestCaptureFixR13LengthlessIndexedAccess(unittest.TestCase):
    """Ruling 448, Lead Engineer line E-13: the lengthless form."""

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

    def test_memoryview_in_lengthless_container_as_mapping_value_refused(
        self,
    ):
        outcome = self._payload(
            _LengthlessIndexedOnly([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_bytes_in_lengthless_container_as_mapping_value_refused(
        self,
    ):
        outcome = self._payload(
            _LengthlessIndexedOnly([b"x" * BIG])
        )
        self._assert_refused(outcome)

    def test_string_in_lengthless_container_as_mapping_value_refused(
        self,
    ):
        outcome = self._payload(
            _LengthlessIndexedOnly(["x" * BIG])
        )
        self._assert_refused(outcome)

    def test_mapping_value_in_lengthless_container_refused(self):
        outcome = self._payload(
            _LengthlessIndexedOnly(
                [{"inner": memoryview(b"x" * BIG)}]
            )
        )
        self._assert_refused(outcome)

    def test_memoryview_lengthless_container_nested_in_list_refused(
        self,
    ):
        outcome = self._payload(
            [_LengthlessIndexedOnly([memoryview(b"x" * BIG)])]
        )
        self._assert_refused(outcome)

    def test_memoryview_nested_lengthless_containers_refused(self):
        outcome = self._payload(
            _LengthlessIndexedOnly(
                [_LengthlessIndexedOnly([memoryview(b"x" * BIG)])]
            )
        )
        self._assert_refused(outcome)

    def test_byte_form_of_lengthless_container_states_its_content(
        self,
    ):
        module = require("ontoloop.capture")
        form = module._value_byte_form(
            _LengthlessIndexedOnly([b"ab", b"cde"])
        )
        self.assertEqual(form, b"abcde")

    def test_byte_form_counts_memoryview_in_lengthless_container(
        self,
    ):
        module = require("ontoloop.capture")
        form = module._value_byte_form(
            _LengthlessIndexedOnly([memoryview(b"x" * 100)])
        )
        self.assertEqual(len(form), 100)

    def test_small_memoryview_in_lengthless_container_accepted(self):
        outcome = self._payload(
            _LengthlessIndexedOnly(
                [memoryview(b"a small clean note")]
            )
        )
        self._assert_accepted(outcome)

    def test_small_value_in_lengthless_container_accepted(self):
        outcome = self._payload(_LengthlessIndexedOnly([CLEAN]))
        self._assert_accepted(outcome)

    def test_cyclic_lengthless_container_small_accepted_no_hang(self):
        container = _LengthlessIndexedOnly(
            [memoryview(b"a small clean note")]
        )
        container._items.append(container)
        outcome = self._payload(container)
        self._assert_accepted(outcome)

    def test_plain_mapping_and_list_controls_still_refuse(self):
        self._assert_refused(
            self._payload({"inner": memoryview(b"x" * BIG)})
        )
        self._assert_refused(
            self._payload([memoryview(b"x" * BIG)])
        )

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


class TestRedactFixR13FloorViewElement(unittest.TestCase):
    """Ruling 449, Lead Engineer line E-14: the view element forms."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def _scan(self, assembly):
        module = require("ontoloop.redact")
        return module.exit_scan(assembly)

    def test_list_keys_view_element_unknown_fails_closed(self):
        mapping = {"assembly_state": "some unknown state"}
        self._assert_fails_closed(self._scan([mapping.keys()]))

    def test_list_values_view_element_unknown_fails_closed(self):
        mapping = {"assembly_state": "some unknown state"}
        self._assert_fails_closed(self._scan([mapping.values()]))

    def test_list_keys_view_element_cannot_run_fails_closed(self):
        mapping = {"assembly_state": "scan cannot run"}
        self._assert_fails_closed(self._scan([mapping.keys()]))

    def test_list_values_view_element_cannot_run_fails_closed(self):
        mapping = {"assembly_state": "scan cannot run"}
        self._assert_fails_closed(self._scan([mapping.values()]))

    def test_list_keys_view_element_ready_fails_closed(self):
        mapping = {"assembly_state": "ready"}
        self._assert_fails_closed(self._scan([mapping.keys()]))

    def test_list_values_view_element_ready_fails_closed(self):
        mapping = {"assembly_state": "ready"}
        self._assert_fails_closed(self._scan([mapping.values()]))

    def test_tuple_keys_view_element_ready_fails_closed(self):
        mapping = {"assembly_state": "ready"}
        self._assert_fails_closed(self._scan((mapping.keys(),)))

    def test_tuple_values_view_element_unknown_fails_closed(self):
        mapping = {"assembly_state": "some unknown state"}
        self._assert_fails_closed(self._scan((mapping.values(),)))

    def test_deque_keys_view_element_unknown_fails_closed(self):
        mapping = {"assembly_state": "some unknown state"}
        self._assert_fails_closed(
            self._scan(collections.deque([mapping.keys()]))
        )

    def test_floor_counts_no_content_on_keys_view_element(self):
        module = require("ontoloop.redact")
        mapping = {"assembly_state": "some unknown state"}
        self.assertEqual(
            module._assembly_content(
                [mapping.keys()], _skip_top_state=True
            ),
            [],
        )

    def test_floor_counts_no_content_on_values_view_element(self):
        module = require("ontoloop.redact")
        mapping = {"assembly_state": "some unknown state"}
        self.assertEqual(
            module._assembly_content(
                [mapping.values()], _skip_top_state=True
            ),
            [],
        )

    def test_floor_view_element_counts_only_content_beside_state(
        self,
    ):
        module = require("ontoloop.redact")
        mapping = {"assembly_state": "ready", "content": CLEAN}
        self.assertEqual(
            module._assembly_content(
                [mapping.keys()], _skip_top_state=True
            ),
            ["content"],
        )
        self.assertEqual(
            module._assembly_content(
                [mapping.values()], _skip_top_state=True
            ),
            [CLEAN],
        )

    def test_mapping_control_still_fails_closed(self):
        self._assert_fails_closed(
            self._scan({"assembly_state": "some unknown state"})
        )
        self._assert_fails_closed(
            self._scan([{"assembly_state": "some unknown state"}])
        )

    def test_items_view_element_control_still_fails_closed(self):
        mapping = {"assembly_state": "some unknown state"}
        self._assert_fails_closed(self._scan([mapping.items()]))

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

    def test_hit_in_values_view_element_beside_content_refuses_whole(
        self,
    ):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        mapping = {"assembly_state": hit, "content": CLEAN}
        outcome = module.exit_scan([mapping.values()])
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

    def test_keys_view_with_clean_key_beside_state_releases(self):
        mapping = {"assembly_state": "ready", "content": CLEAN}
        outcome = self._scan([mapping.keys()])
        self.assertFalse(outcome["refused"])

    def test_values_view_with_clean_content_beside_state_releases(
        self,
    ):
        mapping = {"assembly_state": "ready", "content": CLEAN}
        outcome = self._scan([mapping.values()])
        self.assertFalse(outcome["refused"])


if __name__ == "__main__":
    unittest.main()
