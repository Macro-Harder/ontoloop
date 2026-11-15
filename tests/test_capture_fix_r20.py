"""Fix round 20, ruling 802: deep nesting governed refusal.

Deep finite nesting in a walked container form meets a
governed refusal in the standing refused form at
capture_payload, in place of an ungoverned RecursionError.
"""

import unittest

from tests.harness import require

MODULE = "ontoloop.capture"

REFUSED = {
    "accepted": False,
    "truncated": False,
    "refused": True,
    "truncation_written": False,
    "partial_record_written": False,
}

ACCEPTED = {
    "accepted": True,
    "truncated": False,
    "refused": False,
    "truncation_written": False,
    "partial_record_written": False,
}

DEPTH = 1500


def _nested_list(depth):
    value = "leaf"
    for _ in range(depth):
        value = [value]
    return value


def _nested_mapping(depth):
    value = "leaf"
    for _ in range(depth):
        value = {"k": value}
    return value


def _nested_tuple(depth):
    value = "leaf"
    for _ in range(depth):
        value = (value,)
    return value


class TestDeepNestingGovernedRefusal(unittest.TestCase):

    def test_list_nested_deep_as_mapping_value_refused(self):
        module = require(MODULE)
        result = module.capture_payload({"k": _nested_list(DEPTH)})
        self.assertEqual(result, REFUSED)

    def test_mapping_nested_deep_as_mapping_value_refused(self):
        module = require(MODULE)
        result = module.capture_payload({"k": _nested_mapping(DEPTH)})
        self.assertEqual(result, REFUSED)

    def test_tuple_nested_deep_as_mapping_value_refused(self):
        module = require(MODULE)
        result = module.capture_payload({"k": _nested_tuple(DEPTH)})
        self.assertEqual(result, REFUSED)

    def test_tuple_nested_deep_as_mapping_key_refused(self):
        module = require(MODULE)
        result = module.capture_payload({_nested_tuple(DEPTH): "x"})
        self.assertEqual(result, REFUSED)


class TestCaptureStandingFormsStillStand(unittest.TestCase):

    def test_shallow_list_nesting_still_accepted(self):
        module = require(MODULE)
        result = module.capture_payload({"k": _nested_list(100)})
        self.assertEqual(result, ACCEPTED)

    def test_at_cap_fixture_still_accepted(self):
        module = require(MODULE)
        result = module.capture_payload("at cap")
        self.assertEqual(result, ACCEPTED)


if __name__ == "__main__":
    unittest.main()
