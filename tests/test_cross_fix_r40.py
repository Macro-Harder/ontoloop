"""Fix round 40 tests for Region 2: cross split audit family.

Charge pinned here, from design/steps/step-15-r40-triage.md:
ruling 2898 (the Dataset paper position, roster 3234,
finding S15-R40-DATA-1, Low, at entry N-1568, absorbing the
Cross split paper position, roster 3235, finding
S15-R40-CROSS-1, Low, at entry N-1567, and the Eval paper
position, roster 3236, finding S15-R40-EVAL-1, Low, at
entry N-1569, on the one sentinel identity ground: the
sentinel all thirteen probe discriminating equality spoof
at the dataset instruction item surface, value side, items
side, bool key side, and pairs position, a form claiming
equality as a bool true against any form except the
thirteen bare forms the landed sentinel limb probes with,
the bare plain object beside bare probe forms of the
twelve landed probe classes, withholding against each of
them by returning false, by raising, by returning a non
bool truthy claim, or by returning the not implemented
form, in the forms K1 to K8 the Dataset paper states
severally).
The cure stands on ontoloop/cross_split_audit.py alone;
dataset.py stands untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest

from tests import harness
from tests.test_cross_fix_r20 import (
    CLEAN_TEXT,
    HOLDOUT_TEXT,
)
from tests.test_cross_fix_r24 import (
    dataset_bundle,
    keys_view,
)
from tests.test_cross_fix_r31 import (
    governed_items_view,
    governed_values_view,
)
from tests.test_cross_fix_r36 import (
    all_five_key_keys_view,
    all_five_values_view,
    spoof_make,
)
from tests.test_cross_fix_r36 import (
    check_dataset_spoof_refused as check_refused,
)
from tests.test_cross_fix_r36 import (
    check_direct_and_wrapper_fire_on_spoof,
)
from tests.test_cross_fix_r37 import (
    raising_seven_key_keys_view,
    raising_seven_values_view,
    seven_items_view,
    seven_key_keys_view,
    seven_values_view,
)
from tests.test_cross_fix_r38 import (
    nine_items_view,
    nine_key_keys_view,
    nine_values_view,
    raising_nine_key_keys_view,
    raising_nine_values_view,
)
from tests.test_cross_fix_r39 import (
    eleven_items_view,
    eleven_key_keys_view,
    eleven_values_view,
    raising_eleven_key_keys_view,
    raising_eleven_values_view,
)

OCCASIONS = ("candidate construction", "promotion")

_PROBE_NAMES_THIRTEEN = {
    "_SeamSentinelProbe", "_SeamSentinelProbeOther",
    "_SeamSentinelProbeFurther", "_SeamSentinelProbeLast",
    "_SeamSentinelProbeBeyond", "_SeamSentinelProbeFinal",
    "_SeamSentinelProbeAfter", "_SeamSentinelProbeOuter",
    "_SeamSentinelProbeNext", "_SeamSentinelProbeFarther",
    "_SeamSentinelProbePast", "_SeamSentinelProbeOutermost",
}


def _is_thirteen_form(other):
    if type(other) is object:
        return True
    return type(other).__name__ in _PROBE_NAMES_THIRTEEN


class AllThirteenProbeSpoof:
    """An object whose equality reading returns true
    against any form except the thirteen bare forms the
    landed sentinel limb probes with, a bare plain object
    and bare probe forms of the twelve landed probe
    classes, against each of which it returns false."""

    def __eq__(self, other):
        if _is_thirteen_form(other):
            return False
        return True

    def __ne__(self, other):
        if _is_thirteen_form(other):
            return True
        return False

    __hash__ = object.__hash__


class RaisingAllThirteenProbeSpoof:
    """An object whose equality reading returns true
    against any form, and raises against each of the
    thirteen bare forms the landed sentinel limb probes
    with."""

    def __eq__(self, other):
        if _is_thirteen_form(other):
            raise ValueError("no reading")
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


class NonBoolAllThirteenProbeSpoof:
    """An object whose equality reading returns true as a
    bool against any form except the thirteen bare forms
    the landed sentinel limb probes with, against each of
    which it returns a non bool truthy claim."""

    def __eq__(self, other):
        if _is_thirteen_form(other):
            return 1
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


class NotImplementedAllThirteenProbeSpoof:
    """An object whose equality reading returns true as a
    bool against any form except the thirteen bare forms
    the landed sentinel limb probes with, against each of
    which it returns the not implemented form."""

    def __eq__(self, other):
        if _is_thirteen_form(other):
            return NotImplemented
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


def thirteen_values_view():
    return {1: AllThirteenProbeSpoof()}.values()


def thirteen_items_view():
    return {1: AllThirteenProbeSpoof()}.items()


def thirteen_key_keys_view():
    return {(AllThirteenProbeSpoof(),): 1}.keys()


def raising_thirteen_values_view():
    return {1: RaisingAllThirteenProbeSpoof()}.values()


def raising_thirteen_key_keys_view():
    return {(RaisingAllThirteenProbeSpoof(),): 1}.keys()


def nonbool_thirteen_values_view():
    return {1: NonBoolAllThirteenProbeSpoof()}.values()


def notimpl_thirteen_values_view():
    return {1: NotImplementedAllThirteenProbeSpoof()}.values()


class Ruling2898SentinelAllThirteenProbeSpoofTests(
        unittest.TestCase):
    """Ruling 2898, S15-R40-DATA-1 absorbing
    S15-R40-CROSS-1 and S15-R40-EVAL-1: the sentinel all
    thirteen probe discriminating equality spoof at the
    dataset instruction item surface: an object whose
    equality reading claims equality with the governed
    material while withholding a bool true claim against
    every bare form of the extended sentinel panel of the
    landed limb, the bare plain object and the bare probe
    forms of all twelve probe classes, by returning false
    against each of them, by raising against each of
    them, by returning a non bool truthy claim against
    each of them, or by returning the not implemented
    form against each of them, presented in place of
    governed material at the value side, the items side,
    the bool key side, and the pairs position, in the
    forms K1 to K8 the Dataset paper states severally,
    stands refused at the dataset surface, the direct
    act and the promote wrapper firing in parity with
    their controls."""

    def test_all_thirteen_spoof_value_forms_refused(self):
        check_refused(
            self, thirteen_values_view, governed_values_view)
        check_refused(
            self, thirteen_items_view, governed_items_view)
        check_refused(
            self, raising_thirteen_values_view,
            governed_values_view)

    def test_all_thirteen_spoof_key_forms_refused(self):
        check_refused(
            self, thirteen_key_keys_view, keys_view,
            comparisons=2)
        check_refused(
            self, raising_thirteen_key_keys_view, keys_view,
            comparisons=2)

    def test_all_thirteen_spoof_at_pairs_refused(self):
        check_refused(
            self, thirteen_values_view, governed_values_view,
            wrapkey="pairs")

    def test_all_thirteen_spoof_further_withholding_refused(self):
        check_refused(
            self, nonbool_thirteen_values_view,
            governed_values_view)
        check_refused(
            self, notimpl_thirteen_values_view,
            governed_values_view)

    def test_all_thirteen_spoof_direct_and_wrapper_fire(self):
        check_direct_and_wrapper_fire_on_spoof(
            self, thirteen_values_view, governed_values_view)
        check_direct_and_wrapper_fire_on_spoof(
            self, thirteen_key_keys_view, keys_view)
        check_refused(
            self, thirteen_values_view, governed_values_view)

    def test_earlier_sentinel_poles_stand(self):
        check_refused(
            self, eleven_values_view, governed_values_view)
        check_refused(
            self, eleven_items_view, governed_items_view)
        check_refused(
            self, raising_eleven_values_view,
            governed_values_view)
        check_refused(
            self, eleven_key_keys_view, keys_view,
            comparisons=2)
        check_refused(
            self, raising_eleven_key_keys_view, keys_view,
            comparisons=2)
        check_refused(
            self, nine_values_view, governed_values_view)
        check_refused(
            self, nine_items_view, governed_items_view)
        check_refused(
            self, raising_nine_values_view,
            governed_values_view)
        check_refused(
            self, nine_key_keys_view, keys_view,
            comparisons=2)
        check_refused(
            self, raising_nine_key_keys_view, keys_view,
            comparisons=2)
        check_refused(
            self, seven_values_view, governed_values_view)
        check_refused(
            self, seven_items_view, governed_items_view)
        check_refused(
            self, raising_seven_values_view,
            governed_values_view)
        check_refused(
            self, seven_key_keys_view, keys_view,
            comparisons=2)
        check_refused(
            self, raising_seven_key_keys_view, keys_view,
            comparisons=2)
        check_refused(
            self, all_five_values_view, governed_values_view)
        check_refused(
            self, all_five_values_view, governed_values_view,
            wrapkey="pairs")
        check_refused(
            self, all_five_key_keys_view, keys_view,
            comparisons=2)

    def test_all_thirteen_spoof_clean_pole_clears(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_instruction_item(
            CLEAN_TEXT,
            {"items": [spoof_make(
                thirteen_values_view, governed_values_view)]},
            occasion="promotion")
        self.assertFalse(result["fired"])
        self.assertEqual(result["comparisons"], 1)
        dataset = harness.require("ontoloop.dataset")
        result = dataset.test_instruction_items_against_holdout(
            dataset_bundle(CLEAN_TEXT, lambda: {
                "items": [spoof_make(
                    thirteen_values_view, governed_values_view)]}),
            occasion="promotion")
        self.assertFalse(result["fired"])


if __name__ == "__main__":
    unittest.main()
