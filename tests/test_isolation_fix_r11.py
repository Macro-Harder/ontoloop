"""Fix round 11 tests for Region 5: the isolation copy act.

Written test first for the positions charged at Round 11 triage
rulings 358, 359, and 360: an accepted shape subclass instance
carrying its own mutable instance state standing accepted, a
member carrying only a UUID, a timezone, or a pure path standing
refused, and a member carrying mutable state standing inside a
WeakSet inside a fallback value passing by identity. Each class
pins its cure beside the standing forms its charge protects,
including the Fix round 9 and 10 refusal and attribute forms.
"""

import unittest
import weakref
from datetime import date, time, timedelta, timezone
from decimal import Decimal
from enum import Enum, IntEnum
from fractions import Fraction
from pathlib import PurePath, PurePosixPath
from uuid import UUID

from tests.harness import require

REFUSAL_MESSAGE = "enum member with mutable instance state in bundle copy"


class R11Member(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"
    AA = "aa"
    AB = "ab"
    AC = "ac"
    AD = "ad"
    AE = "ae"
    AF = "af"
    AG = "ag"
    AH = "ah"
    AI = "ai"
    AJ = "aj"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class DecimalSub(Decimal):
    pass


class DateSub(date):
    pass


class FractionSub(Fraction):
    pass


class TimeSub(time):
    pass


class TimedeltaSub(timedelta):
    pass


class TupleSub(tuple):
    pass


class FrozensetSub(frozenset):
    pass


def _sub_with_list(factory):
    value = factory()
    value.held = ["original"]
    return value


class TestRuling358SubclassInstanceState(unittest.TestCase):
    """Ruling 358: an accepted shape carrying added mutable state."""

    def _assert_refused(self, module, member, workflow):
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": member})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")
        self.assertIsNone(found["bundle"])

    def test_decimal_subclass_with_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.A
        member.shape = _sub_with_list(lambda: DecimalSub("1.5"))
        self._assert_refused(module, member, "r11 sub decimal workflow")

    def test_date_subclass_with_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.B
        member.shape = _sub_with_list(lambda: DateSub(2024, 1, 2))
        self._assert_refused(module, member, "r11 sub date workflow")

    def test_fraction_subclass_with_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.C
        member.shape = _sub_with_list(lambda: FractionSub(1, 3))
        self._assert_refused(module, member, "r11 sub fraction workflow")

    def test_time_subclass_with_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.D
        member.shape = _sub_with_list(lambda: TimeSub(1, 2))
        self._assert_refused(module, member, "r11 sub time workflow")

    def test_timedelta_subclass_with_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.E
        member.shape = _sub_with_list(lambda: TimedeltaSub(days=2))
        self._assert_refused(module, member, "r11 sub timedelta workflow")

    def test_tuple_subclass_with_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.F
        member.shape = _sub_with_list(lambda: TupleSub((Decimal("1.5"),)))
        self._assert_refused(module, member, "r11 sub tuple workflow")

    def test_frozenset_subclass_with_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.G
        member.shape = _sub_with_list(
            lambda: FrozensetSub({Decimal("1.5")})
        )
        self._assert_refused(module, member, "r11 sub frozenset workflow")

    def test_subclass_with_list_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.H
        member.shape = _sub_with_list(lambda: DecimalSub("2.5"))
        workflow = "r11 sub fallback workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": Holder(member)})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")

    def test_exact_instances_with_no_added_state_stand_shared(self):
        module = require("ontoloop.consumption")
        member = R11Member.I
        member.shape = Decimal("1.5")
        recorded = module.record_promotion(
            "r11 exact decimal workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover("r11 exact decimal workflow")
        self.assertIs(found["bundle"]["part"], member)
        member = R11Member.J
        member.shape = DateSub(2024, 3, 4)
        recorded = module.record_promotion(
            "r11 subclass clean workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover("r11 subclass clean workflow")
        self.assertIs(found["bundle"]["part"], member)

    def test_subclass_with_only_immutable_added_state_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R11Member.K
        shape = DecimalSub("1.5")
        shape.extra = Decimal("2.5")
        member.shape = shape
        recorded = module.record_promotion(
            "r11 subclass immutable extra workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover("r11 subclass immutable extra workflow")
        self.assertIs(found["bundle"]["part"], member)


class TestRuling359UnnamedImmutableShapes(unittest.TestCase):
    """Ruling 359: UUID, timezone, and pure path shapes stand accepted."""

    def _assert_shared(self, module, member, workflow):
        recorded = module.record_promotion(workflow, {"part": member})
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover(workflow)
        self.assertIs(found["bundle"]["part"], member)

    def test_uuid_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R11Member.L
        member.ident = UUID("12345678-1234-5678-1234-567812345678")
        self._assert_shared(module, member, "r11 shape uuid workflow")

    def test_timezone_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R11Member.M
        member.zone = timezone(timedelta(hours=-5))
        self._assert_shared(module, member, "r11 shape timezone workflow")
        member = R11Member.N
        member.zone = timezone.utc
        self._assert_shared(module, member, "r11 shape utc workflow")

    def test_pure_path_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R11Member.O
        member.path = PurePath("alpha/beta")
        self._assert_shared(module, member, "r11 shape pure path workflow")
        member = R11Member.P
        member.path = PurePosixPath("alpha/beta")
        self._assert_shared(
            module, member, "r11 shape pure posix workflow"
        )

    def test_tuple_holding_only_a_uuid_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R11Member.Q
        member.pack = (UUID("12345678-1234-5678-1234-567812345678"),)
        self._assert_shared(module, member, "r11 shape uuid tuple workflow")

    def test_mutable_attribute_still_refused_beside_the_shapes(self):
        module = require("ontoloop.consumption")
        member = R11Member.R
        member.held = ["original"]
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(
                "r11 shape mutable workflow", {"part": member}
            )
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        member = R11Member.S
        member.pack = (Decimal("1.5"), ["original"])
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(
                "r11 shape mixed workflow", {"part": member}
            )
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)


class TestRuling360WeakSetFallbackScan(unittest.TestCase):
    """Ruling 360: the fallback scan walks a WeakSet form."""

    def test_member_in_weakset_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.T
        member.held = ["original"]
        holder = Holder(weakref.WeakSet([member]))
        workflow = "r11 weakset fallback workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": holder})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")
        self.assertIsNone(found["bundle"])

    def test_member_in_weakset_nested_in_holder_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R11Member.U
        member.held = ["original"]
        holder = Holder([weakref.WeakSet([member])])
        workflow = "r11 weakset nested workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": holder})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_holder_with_clean_member_in_weakset_still_copies(self):
        module = require("ontoloop.consumption")
        member = R11Member.V
        holder = Holder(weakref.WeakSet([member]))
        workflow = "r11 weakset clean workflow"
        recorded = module.record_promotion(workflow, {"part": holder})
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertEqual(list(returned.part), [member])
        found = module.discover(workflow)
        self.assertIsNot(found["bundle"]["part"], holder)
        self.assertEqual(list(found["bundle"]["part"].part), [member])


if __name__ == "__main__":
    unittest.main()
