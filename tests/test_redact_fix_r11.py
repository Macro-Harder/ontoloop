"""Fix round 11 tests for Region 4: redact state read.

Written first for two positions at Round 11
triage ruling 370 point 4: ruling 355 (the exit
scan state read set and frozenset pair element
defect, S15-R11-CR-3 and Consume Finding 1) and
ruling 356 (Lead Engineer line E-9, the state
read on a pair standing as a dictionary items
view). No act here touches the material gathering
act: ruling 319 stands cured and no charge of
this round lands on it.
"""

import collections
import collections.abc
import unittest

from tests.harness import require

CLEAN = "a routine clean note"


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


class _AbstractSequence(collections.abc.Sequence):
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)


class TestRedactFixR11SetPairElement(unittest.TestCase):
    """Ruling 355: a set or frozenset pair element stands skipped."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def test_state_value_set_state_element_skipped_no_exception(self):
        module = require("ontoloop.redact")
        assembly = [
            {"assembly_state", "scan cannot run"},
            ("content", CLEAN),
        ]
        self.assertIsNone(module._assembly_state_value(assembly))

    def test_state_value_frozenset_state_element_skipped_no_exception(self):
        module = require("ontoloop.redact")
        assembly = [
            frozenset({"assembly_state", "scan cannot run"}),
            ("content", CLEAN),
        ]
        self.assertIsNone(module._assembly_state_value(assembly))

    def test_exit_scan_set_state_element_beside_clean_pair_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            {"assembly_state", "scan cannot run"},
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_exit_scan_frozenset_state_element_beside_clean_pair_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            frozenset({"assembly_state", "scan cannot run"}),
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_exit_scan_plain_clean_set_element_releases_no_exception(self):
        module = require("ontoloop.redact")
        assembly = [
            {"alpha", "beta"},
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_exit_scan_plain_clean_frozenset_element_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            frozenset({"alpha", "beta"}),
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_tuple_assembly_set_element_no_exception(self):
        module = require("ontoloop.redact")
        assembly = (
            {"assembly_state", "scan cannot run"},
            ("content", CLEAN),
        )
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_top_level_set_assembly_set_element_no_exception(self):
        module = require("ontoloop.redact")
        assembly = {
            frozenset({"assembly_state", "scan cannot run"}),
            ("content", CLEAN),
        }
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_readable_state_pair_before_set_element_still_read(self):
        module = require("ontoloop.redact")
        assembly = [
            ("assembly_state", "scan cannot run"),
            {"alpha", "beta"},
            ("content", CLEAN),
        ]
        self.assertEqual(
            module._assembly_state_value(assembly), "scan cannot run"
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_deque_pair_control_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            collections.deque(["assembly_state", "scan cannot run"]),
            collections.deque(["content", CLEAN]),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_abstract_sequence_pair_control_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            _AbstractSequence(["assembly_state", "scan cannot run"]),
            _AbstractSequence(["content", CLEAN]),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_set_of_pairs_control_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = {
            ("assembly_state", "scan cannot run"),
            ("content", CLEAN),
        }
        self._assert_fails_closed(module.exit_scan(assembly))


class TestRedactFixR11ItemsViewPair(unittest.TestCase):
    """Ruling 356: the state read on an items view pair."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def test_state_value_read_on_items_view_pair(self):
        module = require("ontoloop.redact")
        assembly = [
            {"assembly_state": "scan cannot run"}.items(),
            ("content", CLEAN),
        ]
        self.assertEqual(
            module._assembly_state_value(assembly), "scan cannot run"
        )

    def test_list_holding_items_view_pair_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            {"assembly_state": "scan cannot run"}.items(),
            ("content", CLEAN),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_items_view_pair_ready_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            {"assembly_state": "ready"}.items(),
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_items_view_pair_without_state_entry_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            {"note": CLEAN}.items(),
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_items_view_pair_carrying_hit_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        assembly = [
            {"assembly_state": "ready", "note": hit}.items(),
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_list_pair_control_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            ["assembly_state", "scan cannot run"],
            ["content", CLEAN],
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_tuple_pair_control_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            ("assembly_state", "scan cannot run"),
            ("content", CLEAN),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_userlist_pair_control_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            collections.UserList(["assembly_state", "scan cannot run"]),
            collections.UserList(["content", CLEAN]),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_deque_pair_control_still_fails_closed_r356(self):
        module = require("ontoloop.redact")
        assembly = [
            collections.deque(["assembly_state", "scan cannot run"]),
            collections.deque(["content", CLEAN]),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_abstract_sequence_pair_control_still_fails_closed_r356(self):
        module = require("ontoloop.redact")
        assembly = [
            _AbstractSequence(["assembly_state", "scan cannot run"]),
            _AbstractSequence(["content", CLEAN]),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_set_of_pairs_control_still_fails_closed_r356(self):
        module = require("ontoloop.redact")
        assembly = {
            ("assembly_state", "scan cannot run"),
            ("content", CLEAN),
        }
        self._assert_fails_closed(module.exit_scan(assembly))


if __name__ == "__main__":
    unittest.main()
