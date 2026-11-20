"""Fix round 34 tests for Region 3: promote wrapper.

Written first for one position at Round 34 triage
ruling 2046 (S15-R34-PROM-1, Low). Ruling 2046: a
self referential plain list standing inside a
delegating list form standing inside a mapping
standing as an element of the delegating concrete
container carrier at the composed position, firing
at the promote wrapper in the refusal form,
promotion not proceeding, where the direct act
clears, fired False with comparisons 0, on hit
material and on clean material alike, one ring
beyond ruling 1915. Rulings 1915 and 1687 stand
cured in their bounded forms and stand not reopened
by any pin here: their charged forms stand as poles
beside the new forms, in the forms the Round 34
Promote paper, roster 2823, states at its section 3.
"""

import unittest

from tests.harness import require
from tests.test_promote_fix_r22 import (
    ListSubclass,
    _chainmap_item,
)

HOLDOUT_TEXT = "sealed holdout instruction text"


def _carrier(inner):
    return {"k": ListSubclass([ListSubclass([inner])])}


def _self_list():
    carried = []
    carried.append(carried)
    return carried


def _self_list_clean():
    carried = [7]
    carried.append(carried)
    return carried


def _self_list_via_tuple():
    carried = []
    carried.append((carried,))
    return carried


def _self_mapping():
    carried = {}
    carried["s"] = carried
    return carried


class _WrapperCase(unittest.TestCase):
    def _wrapper(self, holdout_material, items=None, **kwargs):
        module = require("ontoloop.promote")
        if items is None:
            items = [{"instruction_text": HOLDOUT_TEXT}]
        bundle = {
            "instruction_items": items,
            "holdout_items": holdout_material,
        }
        return module.test_instruction_items_against_holdout(
            bundle, occasion="promotion", **kwargs
        )

    def _direct(self, holdout_material):
        module = require("ontoloop.cross_split_audit")
        return module.audit_instruction_item(
            HOLDOUT_TEXT, holdout_material, occasion="promotion"
        )

    def _assert_fires(self, outcome):
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["promotion_proceeds"])

    def _assert_clears(self, outcome):
        self.assertFalse(outcome["fired"])
        self.assertTrue(
            outcome["test_result_carried_on_promotion_record"]
        )

    def _assert_pair_clears(self, make_item, comparisons=0):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], comparisons)

    def _assert_candidate_clears(self, make_item):
        module = require("ontoloop.promote")
        item = make_item() if callable(make_item) else make_item
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(item),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])


class TestPromoteFixR34SelfReferentialInDelegatingListInMapping(
    _WrapperCase
):
    """Ruling 2046, S15-R34-PROM-1: a self referential
    plain list inside a delegating list form inside a
    mapping as an element of the carrier, firing at
    the wrapper in the refusal form where the direct
    act clears, on hit material and on clean material
    alike."""

    def test_self_list_in_deleg_list_in_mapping_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier({"x": ListSubclass([_self_list()])})
        )

    def test_self_list_clean_in_deleg_list_in_mapping_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {"x": ListSubclass([_self_list_clean()])}
            )
        )

    def test_self_list_via_tuple_in_deleg_list_in_mapping_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {"x": ListSubclass([_self_list_via_tuple()])}
            )
        )

    def test_self_list_in_deleg_list_in_mapping_candidate_clears(self):
        self._assert_candidate_clears(
            lambda: _carrier({"x": ListSubclass([_self_list()])})
        )

    def test_self_list_in_mapping_in_carrier_still_clears(self):
        self._assert_pair_clears(
            lambda: _carrier({"x": _self_list()})
        )

    def test_self_list_in_tuple_in_mapping_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier({"x": (_self_list(),)})
        )

    def test_self_list_in_plain_list_in_mapping_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier({"x": [_self_list()]})
        )

    def test_self_list_in_mapping_in_deleg_list_in_mapping_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {"x": ListSubclass([{"y": _self_list()}])}
            )
        )

    def test_self_mapping_in_deleg_list_in_mapping_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {"x": ListSubclass([_self_mapping()])}
            )
        )

    def test_self_list_in_deleg_list_in_carrier_still_fires(self):
        outcome = self._wrapper(_chainmap_item(
            _carrier(ListSubclass([_self_list()]))
        ))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(
            _carrier(ListSubclass([_self_list()]))
        ))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)


if __name__ == "__main__":
    unittest.main()
