"""Fix round 11 tests for Region 3: capture measurement.

Written first for two positions at Round 11
triage ruling 370 point 3: ruling 353 (S15-R11-CR-1, the
capture payload byte form merged defect, with the
general iterable and values view limbs of Lead
Engineer line E-7 counted in this act and nowhere
else) and ruling 354 (S15-R11-CR-2, the capture payload
byte form reading on a UserString value). No test
here pins the iterator forms of the byte form
reading, whose position stands ruled not a defect
at ruling 353, beyond pinning that those forms stand
unmeasured in their standing leaf form, and no test
here pins the payload form position ruled not a
defect inside Round 10 ruling 317.
"""

import collections
import unittest

from tests.harness import require

CLEAN = "a routine clean note"
BIG = 40000


class _GeneralIterable:
    """A container carrying an iteration act alone.

    The class stands in no sequence, set, mapping,
    view, or array form, and carries no length act
    and no item access act.
    """

    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)


class TestCaptureFixR11GeneralIterableAndViews(unittest.TestCase):
    """Ruling 353: the byte form reading reaches new container forms."""

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

    def test_memoryview_in_general_iterable_as_mapping_value_refused(self):
        outcome = self._payload(
            _GeneralIterable([memoryview(b"x" * BIG)])
        )
        self._assert_refused(outcome)

    def test_bytes_in_general_iterable_as_mapping_value_refused(self):
        outcome = self._payload(_GeneralIterable([b"x" * BIG]))
        self._assert_refused(outcome)

    def test_string_in_general_iterable_as_mapping_value_refused(self):
        outcome = self._payload(_GeneralIterable(["x" * BIG]))
        self._assert_refused(outcome)

    def test_mapping_value_in_general_iterable_refused(self):
        outcome = self._payload(
            _GeneralIterable([{"inner": memoryview(b"x" * BIG)}])
        )
        self._assert_refused(outcome)

    def test_memoryview_nested_general_iterable_inside_list_refused(self):
        outcome = self._payload(
            [_GeneralIterable([memoryview(b"x" * BIG)])]
        )
        self._assert_refused(outcome)

    def test_memoryview_in_values_view_as_mapping_value_refused(self):
        outcome = self._payload(
            {"inner": memoryview(b"x" * BIG)}.values()
        )
        self._assert_refused(outcome)

    def test_memoryview_in_userdict_values_view_refused(self):
        outcome = self._payload(
            collections.UserDict(
                {"inner": memoryview(b"x" * BIG)}
            ).values()
        )
        self._assert_refused(outcome)

    def test_memoryview_in_chainmap_values_view_refused(self):
        outcome = self._payload(
            collections.ChainMap(
                {"inner": memoryview(b"x" * BIG)}
            ).values()
        )
        self._assert_refused(outcome)

    def test_memoryview_in_items_view_as_mapping_value_refused(self):
        outcome = self._payload(
            {"inner": memoryview(b"x" * BIG)}.items()
        )
        self._assert_refused(outcome)

    def test_memoryview_key_in_keys_view_as_mapping_value_refused(self):
        outcome = self._payload(
            {memoryview(b"x" * BIG): "inner"}.keys()
        )
        self._assert_refused(outcome)

    def test_small_memoryview_in_general_iterable_accepted(self):
        outcome = self._payload(
            _GeneralIterable([memoryview(b"a small clean note")])
        )
        self._assert_accepted(outcome)

    def test_small_memoryview_in_values_view_accepted(self):
        outcome = self._payload(
            {"inner": memoryview(b"a small clean note")}.values()
        )
        self._assert_accepted(outcome)

    def test_small_value_in_general_iterable_accepted(self):
        outcome = self._payload(_GeneralIterable([CLEAN]))
        self._assert_accepted(outcome)

    def test_cyclic_general_iterable_small_accepted_no_hang(self):
        container = _GeneralIterable([memoryview(b"a small clean note")])
        container._items.append(container)
        outcome = self._payload(container)
        self._assert_accepted(outcome)

    def test_memoryview_in_generator_stands_in_leaf_form_accepted(self):
        def _generate():
            yield memoryview(b"x" * BIG)

        outcome = self._payload(_generate())
        self._assert_accepted(outcome)

    def test_memoryview_in_zip_stands_in_leaf_form_accepted(self):
        outcome = self._payload(zip([memoryview(b"x" * BIG)]))
        self._assert_accepted(outcome)

    def test_memoryview_in_map_stands_in_leaf_form_accepted(self):
        outcome = self._payload(map(lambda item: item, [memoryview(b"x" * BIG)]))
        self._assert_accepted(outcome)

    def test_memoryview_in_enumerate_stands_in_leaf_form_accepted(self):
        outcome = self._payload(enumerate([memoryview(b"x" * BIG)]))
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


class TestCaptureFixR11UserString(unittest.TestCase):
    """Ruling 354: a UserString stands read as the text it carries."""

    def _assert_refused(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["accepted"])
        self.assertFalse(outcome["truncation_written"])
        self.assertFalse(outcome["partial_record_written"])

    def _assert_accepted(self, outcome):
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["refused"])

    def test_small_userstring_as_mapping_value_accepted(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": collections.UserString(CLEAN)}
        )
        self._assert_accepted(outcome)

    def test_two_character_userstring_as_mapping_value_accepted(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": collections.UserString("ab")}
        )
        self._assert_accepted(outcome)

    def test_empty_userstring_as_mapping_value_accepted(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": collections.UserString("")}
        )
        self._assert_accepted(outcome)

    def test_userstring_40000_as_mapping_value_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": collections.UserString("x" * BIG)}
        )
        self._assert_refused(outcome)

    def test_userstring_40000_inside_list_as_mapping_value_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": [collections.UserString("x" * BIG)]}
        )
        self._assert_refused(outcome)

    def test_small_userstring_inside_list_as_mapping_value_accepted(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {"note": [collections.UserString(CLEAN)]}
        )
        self._assert_accepted(outcome)

    def test_small_userstring_as_mapping_key_accepted(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {collections.UserString("note"): CLEAN}
        )
        self._assert_accepted(outcome)

    def test_userstring_40000_as_mapping_key_refused(self):
        module = require("ontoloop.capture")
        outcome = module.capture_payload(
            {collections.UserString("k" * BIG): CLEAN}
        )
        self._assert_refused(outcome)

    def test_standing_capture_payload_pins_still_pass(self):
        module = require("ontoloop.capture")
        small = module.capture_payload({"note": CLEAN})
        self._assert_accepted(small)
        at_cap = module.capture_payload("at cap")
        self._assert_accepted(at_cap)
        over_cap = module.capture_payload("over cap")
        self._assert_refused(over_cap)


if __name__ == "__main__":
    unittest.main()
