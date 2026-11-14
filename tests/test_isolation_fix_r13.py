"""Fix round 13 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 13 triage
rulings 441, 442, 443, 444, 445, 446, and 447: the mirror and
interface shapes of the ipaddress family and an Ellipsis value in
the immutability reading, the components a slice carries, slot
state standing in a slot declared with a name carrying a leading
double underscore, the default values a function carries, the
bound method form and the property form in the fallback scan,
and the governed refusal for a value the fallback deep copy act
cannot copy. Each class pins its cure beside the standing forms
its charge protects.
"""

import threading
import types
import unittest
from datetime import datetime, timedelta, tzinfo
from decimal import Decimal
from enum import Enum
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from types import MappingProxyType

from tests.harness import require

REFUSAL_MESSAGE = "enum member with mutable instance state in bundle copy"
UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class R13Member(Enum):
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
    AK = "ak"
    AL = "al"
    AM = "am"
    AN = "an"
    AO = "ao"
    AP = "ap"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class DunderHolder:
    """A holder carrying its state in a double underscore slot."""

    __slots__ = ("__held",)

    def set_held(self, value):
        self.__held = value

    def get_held(self):
        return self.__held


class DecimalDunderSlot(Decimal):
    __slots__ = ("__held",)

    def set_held(self, value):
        self.__held = value

    def get_held(self):
        return self.__held


class TzDunderSlot(tzinfo):
    __slots__ = ("__held",)

    def set_held(self, value):
        self.__held = value

    def get_held(self):
        return self.__held

    def utcoffset(self, dt):
        return timedelta(hours=-5)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "DUNDER"


class NetworkWithState(IPv4Network):
    """An IPv4Network subclass instance admitting added state."""


class AddressWithState(IPv6Address):
    """An IPv6Address subclass instance admitting added state."""


def _member_with_list(name):
    member = getattr(R13Member, name)
    member.held = ["original"]
    return member


def _assert_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _assert_shared(case, module, member, workflow):
    recorded = module.record_promotion(workflow, {"part": member})
    case.assertIs(recorded["bundle"]["part"], member)
    found = module.discover(workflow)
    case.assertIs(found["bundle"]["part"], member)


class TestRuling441MirrorShapes(unittest.TestCase):
    """Ruling 441: mirror shapes, interface shapes, and Ellipsis."""

    def test_ipv6address_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.A
        member.shape = IPv6Address("2001:db8::1")
        _assert_shared(self, module, member, "r13 mirror ipv6addr wf")

    def test_ipv4network_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.B
        member.shape = IPv4Network("192.0.2.0/24")
        _assert_shared(self, module, member, "r13 mirror ipv4net wf")

    def test_ipv6interface_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.C
        member.shape = IPv6Interface("2001:db8::1/32")
        _assert_shared(self, module, member, "r13 mirror ipv6iface wf")

    def test_ipv4interface_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.D
        member.shape = IPv4Interface("192.0.2.1/24")
        _assert_shared(self, module, member, "r13 mirror ipv4iface wf")

    def test_tuple_holding_only_an_ipv6address_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.E
        member.shape = (IPv6Address("2001:db8::1"),)
        _assert_shared(self, module, member, "r13 mirror tuple wf")

    def test_tuple_holding_only_mirror_shapes_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.F
        member.shape = (
            IPv4Network("192.0.2.0/24"),
            IPv6Interface("2001:db8::1/32"),
            IPv4Address("192.0.2.1"),
            IPv6Network("2001:db8::/32"),
        )
        _assert_shared(self, module, member, "r13 mirror tuple all wf")

    def test_ellipsis_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.G
        member.shape = Ellipsis
        _assert_shared(self, module, member, "r13 mirror ellipsis wf")

    def test_ipv4network_with_added_list_state_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.H
        shape = NetworkWithState("192.0.2.0/24")
        shape.extra = ["original"]
        member.shape = shape
        _assert_refused(
            self, module, {"part": member}, "r13 mirror net state wf"
        )

    def test_ipv6address_with_added_list_state_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.I
        shape = AddressWithState("2001:db8::1")
        shape.extra = ["original"]
        member.shape = shape
        _assert_refused(
            self, module, {"part": member}, "r13 mirror addr state wf"
        )

    def test_list_attribute_still_refused_beside_the_shapes(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("J")
        _assert_refused(
            self, module, {"part": member}, "r13 mirror list wf"
        )


class TestRuling442SliceComponents(unittest.TestCase):
    """Ruling 442: the components a slice carries stand read."""

    def test_slice_with_a_list_at_its_start_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.K
        member.shape = slice(["original"], 5)
        _assert_refused(
            self, module, {"part": member}, "r13 slice start wf"
        )

    def test_slice_with_a_list_at_its_stop_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.L
        member.shape = slice(0, ["original"])
        _assert_refused(
            self, module, {"part": member}, "r13 slice stop wf"
        )

    def test_slice_with_a_list_at_its_step_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.M
        member.shape = slice(0, 5, ["original"])
        _assert_refused(
            self, module, {"part": member}, "r13 slice step wf"
        )

    def test_slice_with_a_list_component_inside_a_tuple_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.N
        member.shape = (slice(["original"], 5),)
        _assert_refused(
            self, module, {"part": member}, "r13 slice tuple wf"
        )

    def test_slice_with_integer_components_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.O
        member.shape = slice(1, 9, 2)
        _assert_shared(self, module, member, "r13 slice int wf")

    def test_slice_with_immutable_components_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.P
        member.shape = slice(Decimal("1.5"), Decimal("9.5"))
        _assert_shared(self, module, member, "r13 slice decimal wf")


class TestRuling443DunderSlots(unittest.TestCase):
    """Ruling 443: slots declared with a leading double underscore."""

    def test_decimal_subclass_dunder_slot_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.Q
        shape = DecimalDunderSlot("1.5")
        shape.set_held(["original"])
        member.shape = shape
        _assert_refused(
            self, module, {"part": member}, "r13 dunder decimal wf"
        )

    def test_tzinfo_dunder_slot_list_behind_a_datetime_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.R
        zone = TzDunderSlot()
        zone.set_held(["original"])
        member.when = datetime(2024, 1, 2, 3, 4, tzinfo=zone)
        _assert_refused(
            self, module, {"part": member}, "r13 dunder tzinfo wf"
        )

    def test_member_in_a_holder_dunder_slot_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("S")
        holder = DunderHolder()
        holder.set_held(member)
        _assert_refused(
            self, module, {"part": holder}, "r13 dunder holder wf"
        )

    def test_decimal_dunder_slot_list_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = R13Member.T
        shape = DecimalDunderSlot("2.5")
        shape.set_held(["original"])
        member.shape = shape
        _assert_refused(
            self,
            module,
            {"part": Holder(member)},
            "r13 dunder decimal holder wf",
        )

    def test_proxy_in_a_holder_dunder_slot_copies_as_a_mapping(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        holder = DunderHolder()
        holder.set_held(MappingProxyType(source))
        recorded = module.record_promotion(
            "r13 dunder proxy wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(type(returned.get_held()), dict)
        self.assertEqual(returned.get_held(), {"k": ["v"]})
        source["k"].append("caller mutation")
        found = module.discover("r13 dunder proxy wf")
        self.assertEqual(found["bundle"]["part"].get_held(), {"k": ["v"]})

    def test_decimal_dunder_slot_immutable_state_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R13Member.U
        shape = DecimalDunderSlot("1.5")
        shape.set_held(Decimal("2.5"))
        member.shape = shape
        _assert_shared(self, module, member, "r13 dunder immutable wf")

    def test_plain_list_in_a_holder_dunder_slot_copies_apart(self):
        module = require("ontoloop.consumption")
        holder = DunderHolder()
        holder.set_held(["plain"])
        recorded = module.record_promotion(
            "r13 dunder plain list wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertEqual(returned.get_held(), ["plain"])
        self.assertIsNot(returned.get_held(), holder.get_held())
        holder.get_held().append("caller mutation")
        found = module.discover("r13 dunder plain list wf")
        self.assertEqual(found["bundle"]["part"].get_held(), ["plain"])


class TestRuling444FunctionDefaults(unittest.TestCase):
    """Ruling 444: the default values a function carries stand read."""

    def test_member_in_a_positional_default_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("V")

        def read(value=member):
            return value

        _assert_refused(
            self,
            module,
            {"part": Holder(read)},
            "r13 default positional holder wf",
        )

    def test_member_in_a_keyword_default_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("W")

        def read(*, value=member):
            return value

        _assert_refused(
            self,
            module,
            {"part": Holder(read)},
            "r13 default keyword holder wf",
        )

    def test_member_in_a_positional_default_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("X")

        def read(value=member):
            return value

        _assert_refused(
            self, module, {"part": read}, "r13 default positional direct wf"
        )

    def test_member_in_a_keyword_default_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("Y")

        def read(*, value=member):
            return value

        _assert_refused(
            self, module, {"part": read}, "r13 default keyword direct wf"
        )

    def test_view_in_a_positional_default_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}

        def read(value=source.values()):
            return value

        recorded = module.record_promotion(
            "r13 default view wf", {"part": Holder(read)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, read)
        copied_default = returned.__defaults__[0]
        self.assertIs(type(copied_default), list)
        self.assertEqual(copied_default, [["v"]])
        source["k"].append("caller mutation")
        found = module.discover("r13 default view wf")
        self.assertEqual(
            found["bundle"]["part"].part.__defaults__[0], [["v"]]
        )

    def test_view_in_a_keyword_default_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}

        def read(*, value=source.values()):
            return value

        recorded = module.record_promotion(
            "r13 default kwview wf", {"part": Holder(read)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, read)
        copied_default = returned.__kwdefaults__["value"]
        self.assertIs(type(copied_default), list)
        self.assertEqual(copied_default, [["v"]])
        source["k"].append("caller mutation")
        found = module.discover("r13 default kwview wf")
        self.assertEqual(
            found["bundle"]["part"].part.__kwdefaults__["value"], [["v"]]
        )

    def test_proxy_in_a_positional_default_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}

        def read(value=MappingProxyType(source)):
            return value

        recorded = module.record_promotion(
            "r13 default proxy wf", {"part": Holder(read)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, read)
        copied_default = returned.__defaults__[0]
        self.assertIs(type(copied_default), dict)
        self.assertEqual(copied_default, {"k": ["v"]})
        source["k"].append("caller mutation")
        found = module.discover("r13 default proxy wf")
        self.assertEqual(
            found["bundle"]["part"].part.__defaults__[0], {"k": ["v"]}
        )

    def test_clean_member_in_a_default_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        member = R13Member.Z

        def read(value=member):
            return value

        holder = Holder(read)
        recorded = module.record_promotion(
            "r13 default clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, read)
        self.assertIs(returned.part.__defaults__[0], member)


class _BoundObject:
    def __init__(self, part):
        self.part = part

    def read(self):
        return self.part


class TestRuling445BoundMethods(unittest.TestCase):
    """Ruling 445: a bound method stands read through its two parts."""

    def test_bound_object_holding_a_member_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AA")
        bound = _BoundObject(member)
        _assert_refused(
            self,
            module,
            {"part": Holder(bound.read)},
            "r13 method object holder wf",
        )

    def test_wrapped_function_closure_member_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AB")

        def build(captured):
            def inner(self):
                return captured

            return inner

        class Target:
            pass

        method = types.MethodType(build(member), Target())
        _assert_refused(
            self,
            module,
            {"part": Holder(method)},
            "r13 method closure holder wf",
        )

    def test_bound_object_holding_a_member_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AC")
        bound = _BoundObject(member)
        _assert_refused(
            self, module, {"part": bound.read}, "r13 method direct wf"
        )

    def test_clean_bound_method_still_copies_apart(self):
        module = require("ontoloop.consumption")
        bound = _BoundObject(["plain"])
        recorded = module.record_promotion(
            "r13 method clean wf", {"part": Holder(bound.read)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned.__self__, bound)
        self.assertEqual(returned.__self__.part, ["plain"])
        self.assertIsNot(returned.__self__.part, bound.part)

    def test_bound_object_holding_a_view_copies_the_view_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        bound = _BoundObject(source.values())
        recorded = module.record_promotion(
            "r13 method view wf", {"part": Holder(bound.read)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIs(type(returned.__self__.part), list)
        self.assertEqual(returned.__self__.part, [["v"]])
        source["k"].append("caller mutation")
        found = module.discover("r13 method view wf")
        self.assertEqual(
            found["bundle"]["part"].part.__self__.part, [["v"]]
        )


class TestRuling446PropertyForms(unittest.TestCase):
    """Ruling 446: a property stands read through its accessors."""

    def test_getter_closure_holding_a_member_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AD")

        def build(captured):
            def getter(self):
                return captured

            return property(getter)

        _assert_refused(
            self,
            module,
            {"part": Holder(build(member))},
            "r13 property getter wf",
        )

    def test_setter_closure_holding_a_member_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AE")

        def build(captured):
            def getter(self):
                return None

            def setter(self, value):
                self.stored = captured

            return property(getter, setter)

        _assert_refused(
            self,
            module,
            {"part": Holder(build(member))},
            "r13 property setter wf",
        )

    def test_deleter_closure_holding_a_member_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AF")

        def build(captured):
            def getter(self):
                return None

            def deleter(self):
                self.stored = captured

            return property(getter, None, deleter)

        _assert_refused(
            self,
            module,
            {"part": Holder(build(member))},
            "r13 property deleter wf",
        )

    def test_clean_property_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        prop = property(lambda self: 42)
        holder = Holder(prop)
        recorded = module.record_promotion(
            "r13 property clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, prop)


class TestRuling447FallbackEscape(unittest.TestCase):
    """Ruling 447: an uncopyable fallback value stands refused."""

    def _assert_uncopyable_refused(self, module, bundle, workflow):
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, bundle)
        self.assertEqual(str(caught.exception), UNCOPYABLE_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")
        self.assertIsNone(found["bundle"])

    def test_generator_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")

        def stream():
            yield 1

        self._assert_uncopyable_refused(
            module, {"part": Holder(stream())}, "r13 escape generator wf"
        )

    def test_lock_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        self._assert_uncopyable_refused(
            module,
            {"part": Holder(threading.Lock())},
            "r13 escape lock wf",
        )

    def test_generator_as_a_direct_value_is_refused(self):
        module = require("ontoloop.consumption")

        def stream():
            yield 1

        self._assert_uncopyable_refused(
            module, {"part": stream()}, "r13 escape generator direct wf"
        )

    def test_lock_nested_in_a_list_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        self._assert_uncopyable_refused(
            module,
            {"part": Holder([threading.Lock()])},
            "r13 escape lock nested wf",
        )

    def test_plain_list_inside_a_holder_still_records(self):
        module = require("ontoloop.consumption")
        holder = Holder(["plain"])
        recorded = module.record_promotion(
            "r13 escape plain wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertEqual(returned.part, ["plain"])
        self.assertIsNot(returned.part, holder.part)


if __name__ == "__main__":
    unittest.main()
