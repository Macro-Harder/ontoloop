"""Fix round 10 tests for Region 6: the isolation copy act.

Written test first for the positions charged at Round 10 triage
rulings 321, 322, and 323: an enum member carrying mutable
instance state standing inside a deep copy fallback value, a
deque part losing its bound on copy and a tuple subclass whose
constructor takes a leading argument copying as an empty tuple,
and the immutability reading of the enum refusal refusing
members carrying only immutable state in shapes it does not
name. Each class pins its cure beside the standing forms its
charge protects, including the Fix round 9 refusal and
attribute forms.
"""

import unittest
from collections import deque
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum, IntEnum
from fractions import Fraction

from tests.harness import require

REFUSAL_MESSAGE = "enum member with mutable instance state in bundle copy"


class R10Member(Enum):
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


class R10IntMember(IntEnum):
    A = 1
    B = 2
    C = 3
    D = 4


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class DequeSub(deque):
    pass


class TupleSub(tuple):
    pass


class LeadTuple(tuple):
    """A tuple subclass whose constructor takes a leading argument."""

    def __new__(cls, lead, items=()):
        return super().__new__(cls, tuple(items))

    def __init__(self, lead, items=()):
        pass


class TestRuling321FallbackEnumRefusal(unittest.TestCase):
    """Ruling 321: the fallback interior stands under the refusal."""

    def test_holder_at_mapping_value_position_is_refused(self):
        module = require("ontoloop.consumption")
        member = R10Member.A
        member.held = ["original"]
        workflow = "r10 fallback mapping workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": Holder(member)})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")
        self.assertIsNone(found["bundle"])

    def test_holder_inside_a_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R10Member.B
        member.held = ["original"]
        workflow = "r10 fallback list workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"items": [Holder(member)]})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")

    def test_holder_inside_a_tuple_is_refused(self):
        module = require("ontoloop.consumption")
        member = R10IntMember.A
        member.held = ["original"]
        workflow = "r10 fallback tuple workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"pair": (Holder(member), 1)})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_member_nested_inside_holder_containers_is_refused(self):
        module = require("ontoloop.consumption")
        member = R10Member.C
        member.held = ["original"]
        holder = Holder({"nested": [member]})
        workflow = "r10 fallback nested workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": holder})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_holder_carrying_a_clean_member_still_copies(self):
        module = require("ontoloop.consumption")
        member = R10Member.D
        holder = Holder(member)
        workflow = "r10 fallback clean workflow"
        recorded = module.record_promotion(workflow, {"part": holder})
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, member)
        found = module.discover(workflow)
        self.assertIsNot(found["bundle"]["part"], holder)
        self.assertIs(found["bundle"]["part"].part, member)


class TestRuling322DequeBoundAndTupleForm(unittest.TestCase):
    """Ruling 322: the deque bound stands, the tuple helper falls back."""

    def test_plain_bounded_deque_keeps_its_bound(self):
        module = require("ontoloop.consumption")
        part = deque([1, 2], maxlen=3)
        workflow = "r10 deque plain workflow"
        module.record_promotion(workflow, {"part": part})
        part.append(99)
        found = module.discover(workflow)
        copied = found["bundle"]["part"]
        self.assertIs(type(copied), deque)
        self.assertEqual(copied.maxlen, 3)
        self.assertEqual(list(copied), [1, 2])
        copied.append(3)
        copied.append(4)
        self.assertEqual(list(copied), [2, 3, 4])
        self.assertEqual(list(part), [1, 2, 99])
        again = module.discover(workflow)
        self.assertEqual(list(again["bundle"]["part"]), [1, 2])
        self.assertEqual(again["bundle"]["part"].maxlen, 3)

    def test_subclass_bounded_deque_keeps_its_bound(self):
        module = require("ontoloop.consumption")
        part = DequeSub([1, 2], maxlen=3)
        workflow = "r10 deque subclass workflow"
        recorded = module.record_promotion(workflow, {"part": part})
        returned = recorded["bundle"]["part"]
        self.assertIs(type(returned), DequeSub)
        self.assertEqual(returned.maxlen, 3)
        self.assertEqual(list(returned), [1, 2])
        part.append(99)
        found = module.discover(workflow)
        copied = found["bundle"]["part"]
        self.assertIs(type(copied), DequeSub)
        self.assertEqual(copied.maxlen, 3)
        self.assertEqual(list(copied), [1, 2])

    def test_unbounded_deque_still_copies_without_a_bound(self):
        module = require("ontoloop.consumption")
        part = deque([1, 2])
        module.record_promotion("r10 deque unbounded workflow", {"part": part})
        found = module.discover("r10 deque unbounded workflow")
        copied = found["bundle"]["part"]
        self.assertIs(type(copied), deque)
        self.assertIsNone(copied.maxlen)
        self.assertEqual(list(copied), [1, 2])

    def test_lead_argument_tuple_subclass_falls_back_with_its_items(self):
        module = require("ontoloop.consumption")
        part = LeadTuple("tag", (["a"], 2))
        workflow = "r10 lead tuple workflow"
        recorded = module.record_promotion(workflow, {"part": part})
        returned = recorded["bundle"]["part"]
        self.assertIs(type(returned), tuple)
        self.assertEqual(list(returned), [["a"], 2])
        part[0].append("caller mutation")
        found = module.discover(workflow)
        copied = found["bundle"]["part"]
        self.assertIs(type(copied), tuple)
        self.assertEqual(list(copied), [["a"], 2])
        copied[0].append("return mutation")
        self.assertEqual(part[0], ["a", "caller mutation"])
        again = module.discover(workflow)
        self.assertEqual(list(again["bundle"]["part"]), [["a"], 2])

    def test_plain_tuple_subclass_keeps_its_type(self):
        module = require("ontoloop.consumption")
        part = TupleSub((1, 2))
        module.record_promotion("r10 tuple subclass workflow", {"part": part})
        found = module.discover("r10 tuple subclass workflow")
        copied = found["bundle"]["part"]
        self.assertIs(type(copied), TupleSub)
        self.assertEqual(tuple(copied), (1, 2))


class TestRuling323ImmutableShapes(unittest.TestCase):
    """Ruling 323: known immutable attribute shapes stand accepted."""

    def _assert_shared(self, module, member, workflow):
        recorded = module.record_promotion(workflow, {"part": member})
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover(workflow)
        self.assertIs(found["bundle"]["part"], member)

    def test_decimal_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R10Member.E
        member.amount = Decimal("1.5")
        self._assert_shared(module, member, "r10 shape decimal workflow")
        self.assertEqual(member.amount, Decimal("1.5"))

    def test_date_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R10Member.F
        member.day = date(2024, 1, 2)
        self._assert_shared(module, member, "r10 shape date workflow")

    def test_fraction_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R10Member.G
        member.ratio = Fraction(1, 3)
        self._assert_shared(module, member, "r10 shape fraction workflow")

    def test_range_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R10Member.H
        member.span = range(3)
        self._assert_shared(module, member, "r10 shape range workflow")

    def test_enum_member_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R10Member.I
        member.other = R10IntMember.B
        self._assert_shared(module, member, "r10 shape enum workflow")

    def test_frozenset_holding_an_enum_member_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R10Member.J
        member.group = frozenset({R10IntMember.C})
        self._assert_shared(module, member, "r10 shape frozenset workflow")

    def test_tuple_holding_immutable_shapes_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R10Member.K
        member.pack = (Decimal("2.5"), date(2024, 2, 3), Fraction(3, 4))
        self._assert_shared(module, member, "r10 shape tuple workflow")

    def test_datetime_and_timedelta_attributes_stand_shared(self):
        module = require("ontoloop.consumption")
        member = R10Member.L
        member.stamp = datetime(2024, 1, 2, 3, 4, 5)
        self._assert_shared(module, member, "r10 shape datetime workflow")
        member = R10Member.M
        member.gap = timedelta(days=2)
        self._assert_shared(module, member, "r10 shape timedelta workflow")

    def test_int_enum_member_with_decimal_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R10IntMember.D
        member.amount = Decimal("3.5")
        self._assert_shared(module, member, "r10 shape int enum workflow")

    def test_mutable_attribute_still_refused_beside_the_shapes(self):
        module = require("ontoloop.consumption")
        member = R10Member.N
        member.held = ["original"]
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(
                "r10 shape mutable workflow", {"part": member}
            )
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        member = R10Member.O
        member.pack = (Decimal("1.5"), ["original"])
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(
                "r10 shape mixed workflow", {"part": member}
            )
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)


if __name__ == "__main__":
    unittest.main()
