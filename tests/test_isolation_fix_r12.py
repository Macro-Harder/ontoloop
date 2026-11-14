"""Fix round 12 tests for Region 5: the isolation copy act.

Written test first for the positions charged at Round 12 triage
rulings 400, 401, 402, 403, and 404: slot state of an accepted
shape subclass instance, the tzinfo a date or time value carries,
the unnamed immutable shapes ZoneInfo, tzinfo, IPv4Address,
IPv6Network, compiled pattern, and slice, the fallback scan forms
WeakKeyDictionary, WeakValueDictionary, weakref, partial, and
function closure cells, and dictionary views at any position and
a mapping proxy inside a fallback value. Each class pins its cure
beside the standing forms its charge protects.
"""

import functools
import re
import unittest
import weakref
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from ipaddress import IPv4Address, IPv6Network
from pathlib import PurePath
from types import MappingProxyType
from zoneinfo import ZoneInfo

from tests.harness import require

REFUSAL_MESSAGE = "enum member with mutable instance state in bundle copy"


class R12Member(Enum):
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
    AQ = "aq"
    AR = "ar"
    AS = "as"
    AT = "at"
    AU = "au"
    AV = "av"
    AW = "aw"
    AX = "ax"
    AY = "ay"
    AZ = "az"
    BA = "ba"
    BB = "bb"
    BC = "bc"
    BD = "bd"
    BE = "be"
    BF = "bf"
    BG = "bg"
    BH = "bh"
    BI = "bi"
    BJ = "bj"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class DecimalSlot(Decimal):
    __slots__ = ("held",)


class DateSlot(date):
    __slots__ = ("held",)


class FractionSlot(Fraction):
    __slots__ = ("held",)


class TimeSlot(time):
    __slots__ = ("held",)


class TimedeltaSlot(timedelta):
    __slots__ = ("held",)


class PurePathSlot(PurePath):
    __slots__ = ("held",)


class CleanTz(tzinfo):
    """A custom tzinfo carrying no attribute state at all."""

    def utcoffset(self, dt):
        return timedelta(hours=-5)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "CLEAN"


class ListTz(tzinfo):
    """A custom tzinfo carrying a list in its instance mapping."""

    def utcoffset(self, dt):
        return timedelta(hours=-5)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "LIST"


def _slot_with_list(factory):
    value = factory()
    value.held = ["original"]
    return value


def _member_with_list(name):
    member = getattr(R12Member, name)
    member.held = ["original"]
    return member


class TestRuling400SlotState(unittest.TestCase):
    """Ruling 400: slot state beside the instance attribute mapping."""

    def _assert_refused(self, module, member, workflow):
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": member})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")
        self.assertIsNone(found["bundle"])

    def test_decimal_subclass_slot_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.A
        member.shape = _slot_with_list(lambda: DecimalSlot("1.5"))
        self._assert_refused(module, member, "r12 slot decimal workflow")

    def test_date_subclass_slot_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.B
        member.shape = _slot_with_list(lambda: DateSlot(2024, 1, 2))
        self._assert_refused(module, member, "r12 slot date workflow")

    def test_fraction_subclass_slot_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.C
        member.shape = _slot_with_list(lambda: FractionSlot(1, 3))
        self._assert_refused(module, member, "r12 slot fraction workflow")

    def test_time_subclass_slot_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.D
        member.shape = _slot_with_list(lambda: TimeSlot(1, 2))
        self._assert_refused(module, member, "r12 slot time workflow")

    def test_timedelta_subclass_slot_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.E
        member.shape = _slot_with_list(lambda: TimedeltaSlot(days=2))
        self._assert_refused(module, member, "r12 slot timedelta workflow")

    def test_pure_path_subclass_slot_list_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.F
        member.shape = _slot_with_list(lambda: PurePathSlot("alpha/beta"))
        self._assert_refused(module, member, "r12 slot pure path workflow")

    def test_slot_list_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.G
        member.shape = _slot_with_list(lambda: DecimalSlot("2.5"))
        workflow = "r12 slot fallback workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": Holder(member)})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")

    def test_slot_list_nested_in_a_tuple_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.H
        member.shape = (_slot_with_list(lambda: DecimalSlot("3.5")),)
        self._assert_refused(module, member, "r12 slot tuple workflow")

    def test_subclass_with_only_immutable_slot_state_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.I
        shape = DecimalSlot("1.5")
        shape.held = Decimal("2.5")
        member.shape = shape
        recorded = module.record_promotion(
            "r12 slot immutable workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover("r12 slot immutable workflow")
        self.assertIs(found["bundle"]["part"], member)

    def test_exact_instances_with_no_added_state_stand_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.J
        member.shape = Decimal("1.5")
        recorded = module.record_promotion(
            "r12 slot exact workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover("r12 slot exact workflow")
        self.assertIs(found["bundle"]["part"], member)


class TestRuling401TzinfoComponent(unittest.TestCase):
    """Ruling 401: the tzinfo a date or time value carries."""

    def test_datetime_carrying_a_list_tzinfo_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.K
        zone = ListTz()
        zone.held = ["original"]
        member.when = datetime(2024, 1, 2, 3, 4, tzinfo=zone)
        workflow = "r12 tzinfo datetime workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": member})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")

    def test_time_carrying_a_list_tzinfo_is_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.L
        zone = ListTz()
        zone.held = ["original"]
        member.at = time(1, 2, tzinfo=zone)
        workflow = "r12 tzinfo time workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": member})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")

    def test_datetime_and_time_carrying_zoneinfo_stand_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.M
        member.when = datetime(
            2024, 1, 2, 3, 4, tzinfo=ZoneInfo("America/Chicago")
        )
        recorded = module.record_promotion(
            "r12 tzinfo zoneinfo datetime workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)
        member = R12Member.N
        member.at = time(1, 2, tzinfo=ZoneInfo("America/Chicago"))
        recorded = module.record_promotion(
            "r12 tzinfo zoneinfo time workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover("r12 tzinfo zoneinfo time workflow")
        self.assertIs(found["bundle"]["part"], member)

    def test_datetime_carrying_a_clean_custom_tzinfo_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.O
        member.when = datetime(2024, 1, 2, 3, 4, tzinfo=CleanTz())
        recorded = module.record_promotion(
            "r12 tzinfo clean workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover("r12 tzinfo clean workflow")
        self.assertIs(found["bundle"]["part"], member)

    def test_datetime_carrying_timezone_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.P
        member.when = datetime(2024, 1, 2, 3, 4, tzinfo=timezone.utc)
        recorded = module.record_promotion(
            "r12 tzinfo timezone workflow", {"part": member}
        )
        self.assertIs(recorded["bundle"]["part"], member)


class TestRuling402UnnamedShapes(unittest.TestCase):
    """Ruling 402: unnamed immutable shapes stand accepted."""

    def _assert_shared(self, module, member, workflow):
        recorded = module.record_promotion(workflow, {"part": member})
        self.assertIs(recorded["bundle"]["part"], member)
        found = module.discover(workflow)
        self.assertIs(found["bundle"]["part"], member)

    def test_zoneinfo_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.Q
        member.zone = ZoneInfo("America/Chicago")
        self._assert_shared(module, member, "r12 shape zoneinfo workflow")

    def test_tuple_holding_only_a_zoneinfo_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.R
        member.pack = (ZoneInfo("America/Chicago"),)
        self._assert_shared(module, member, "r12 shape zoneinfo tuple wf")

    def test_clean_custom_tzinfo_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.S
        member.zone = CleanTz()
        self._assert_shared(module, member, "r12 shape clean tz workflow")

    def test_base_tzinfo_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.T
        member.zone = tzinfo()
        self._assert_shared(module, member, "r12 shape base tz workflow")

    def test_ipv4address_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.U
        member.address = IPv4Address("192.0.2.1")
        self._assert_shared(module, member, "r12 shape ipv4 workflow")

    def test_ipv6network_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.V
        member.network = IPv6Network("2001:db8::/32")
        self._assert_shared(module, member, "r12 shape ipv6net workflow")

    def test_compiled_pattern_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.W
        member.pattern = re.compile("alpha+")
        self._assert_shared(module, member, "r12 shape pattern workflow")

    def test_slice_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.X
        member.part_slice = slice(1, 9, 2)
        self._assert_shared(module, member, "r12 shape slice workflow")

    def test_tuple_holding_only_such_shapes_stands_shared(self):
        module = require("ontoloop.consumption")
        member = R12Member.Y
        member.pack = (
            ZoneInfo("UTC"),
            IPv4Address("192.0.2.1"),
            re.compile("beta"),
            slice(0, 3),
        )
        self._assert_shared(module, member, "r12 shape tuple workflow")

    def test_tzinfo_carrying_a_list_still_refused(self):
        module = require("ontoloop.consumption")
        member = R12Member.Z
        zone = ListTz()
        zone.held = ["original"]
        member.zone = zone
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(
                "r12 shape tz list workflow", {"part": member}
            )
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_list_attribute_still_refused_beside_the_shapes(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AA")
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(
                "r12 shape list workflow", {"part": member}
            )
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)


class TestRuling403FallbackScanForms(unittest.TestCase):
    """Ruling 403: the fallback scan walks the reachable forms."""

    def _assert_refused(self, module, bundle, workflow):
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, bundle)
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")
        self.assertIsNone(found["bundle"])

    def test_member_in_weakvalue_dictionary_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AB")
        holder = Holder(weakref.WeakValueDictionary({"k": member}))
        self._assert_refused(
            module, {"part": holder}, "r12 weakvalue holder workflow"
        )

    def test_member_in_weakvalue_dictionary_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AC")
        bundle = {"part": weakref.WeakValueDictionary({"k": member})}
        self._assert_refused(module, bundle, "r12 weakvalue direct wf")

    def test_member_as_weakkey_dictionary_key_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AD")
        holder = Holder(weakref.WeakKeyDictionary({member: "v"}))
        self._assert_refused(
            module, {"part": holder}, "r12 weakkey key workflow"
        )

    def test_member_as_weakkey_dictionary_value_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AE")
        mapping, anchor = _weakkey_with_value(member)
        holder = Holder(mapping)
        self._assert_refused(
            module,
            {"part": holder, "anchor": anchor},
            "r12 weakkey value workflow",
        )

    def test_member_behind_a_weakref_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AF")
        holder = Holder(weakref.ref(member))
        self._assert_refused(
            module, {"part": holder}, "r12 weakref holder workflow"
        )

    def test_member_behind_a_weakref_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AG")
        self._assert_refused(
            module, {"part": weakref.ref(member)}, "r12 weakref direct wf"
        )

    def test_member_in_a_partial_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AH")
        holder = Holder(functools.partial(lambda item: item, member))
        self._assert_refused(
            module, {"part": holder}, "r12 partial holder workflow"
        )

    def test_member_in_a_partial_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AI")
        bundle = {"part": functools.partial(lambda item: item, member)}
        self._assert_refused(module, bundle, "r12 partial direct wf")

    def test_member_in_a_partial_keyword_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AJ")
        holder = Holder(
            functools.partial(lambda item=None: item, item=member)
        )
        self._assert_refused(
            module, {"part": holder}, "r12 partial keyword workflow"
        )

    def test_member_in_a_closure_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AK")

        def make():
            def read():
                return member

            return read

        holder = Holder(make())
        self._assert_refused(
            module, {"part": holder}, "r12 closure holder workflow"
        )

    def test_member_in_a_closure_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AL")

        def make():
            def read():
                return member

            return read

        self._assert_refused(
            module, {"part": make()}, "r12 closure direct workflow"
        )

    def test_clean_member_behind_the_same_forms_still_copies(self):
        module = require("ontoloop.consumption")
        member = R12Member.AM
        holder = Holder(weakref.WeakValueDictionary({"k": member}))
        recorded = module.record_promotion(
            "r12 weakvalue clean workflow", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part["k"], member)
        holder = Holder(weakref.ref(member))
        recorded = module.record_promotion(
            "r12 weakref clean workflow", {"part": holder}
        )
        self.assertIs(recorded["bundle"]["part"].part(), member)
        holder = Holder(functools.partial(lambda item: item, member))
        recorded = module.record_promotion(
            "r12 partial clean workflow", {"part": holder}
        )
        self.assertIs(recorded["bundle"]["part"].part.args[0], member)

        def make():
            def read():
                return member

            return read

        holder = Holder(make())
        recorded = module.record_promotion(
            "r12 closure clean workflow", {"part": holder}
        )
        copied_fn = recorded["bundle"]["part"].part
        self.assertIs(copied_fn.__closure__[0].cell_contents, member)


class _WeakKey:
    pass


def _weakkey_with_value(member):
    """Return a WeakKeyDictionary holding the member as a value.

    A WeakKeyDictionary maps weak keys to values; the member stands
    as an ordinary value under a key the caller keeps alive through
    the anchor the helper also returns.
    """

    anchor = _WeakKey()
    mapping = weakref.WeakKeyDictionary()
    mapping[anchor] = member
    return mapping, anchor


class TestRuling404ViewsAndProxyInFallback(unittest.TestCase):
    """Ruling 404: views at any position, proxy inside a fallback."""

    def test_values_view_as_mapping_value_copies_as_a_list(self):
        module = require("ontoloop.consumption")
        source = {"a": ["one"], "b": 2}
        recorded = module.record_promotion(
            "r12 view values workflow", {"part": source.values()}
        )
        copied = recorded["bundle"]["part"]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [["one"], 2])
        source["a"].append("caller mutation")
        found = module.discover("r12 view values workflow")
        self.assertEqual(found["bundle"]["part"], [["one"], 2])

    def test_keys_view_as_mapping_value_copies_as_a_list(self):
        module = require("ontoloop.consumption")
        source = {"a": 1, "b": 2}
        recorded = module.record_promotion(
            "r12 view keys workflow", {"part": source.keys()}
        )
        copied = recorded["bundle"]["part"]
        self.assertIs(type(copied), list)
        self.assertEqual(sorted(copied), ["a", "b"])

    def test_items_view_as_mapping_value_copies_as_a_list_of_pairs(self):
        module = require("ontoloop.consumption")
        source = {"a": ["one"]}
        recorded = module.record_promotion(
            "r12 view items workflow", {"part": source.items()}
        )
        copied = recorded["bundle"]["part"]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [("a", ["one"])])
        source["a"].append("caller mutation")
        found = module.discover("r12 view items workflow")
        self.assertEqual(found["bundle"]["part"], [("a", ["one"])])

    def test_values_view_inside_a_holder_copies_as_a_list(self):
        module = require("ontoloop.consumption")
        source = {"a": ["one"], "b": 2}
        holder = Holder(source.values())
        recorded = module.record_promotion(
            "r12 view holder workflow", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(type(returned.part), list)
        self.assertEqual(returned.part, [["one"], 2])
        source["a"].append("caller mutation")
        found = module.discover("r12 view holder workflow")
        self.assertEqual(found["bundle"]["part"].part, [["one"], 2])

    def test_items_view_inside_a_holder_copies_as_a_list_of_pairs(self):
        module = require("ontoloop.consumption")
        source = {"a": 1}
        holder = Holder(source.items())
        recorded = module.record_promotion(
            "r12 view items holder workflow", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIs(type(returned.part), list)
        self.assertEqual(returned.part, [("a", 1)])

    def test_proxy_inside_a_holder_copies_as_a_fresh_mapping(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        holder = Holder(MappingProxyType(source))
        recorded = module.record_promotion(
            "r12 proxy holder workflow", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(type(returned.part), dict)
        self.assertEqual(returned.part, {"k": ["v"]})
        source["k"].append("caller mutation")
        found = module.discover("r12 proxy holder workflow")
        self.assertEqual(found["bundle"]["part"].part, {"k": ["v"]})

    def test_proxy_inside_a_holder_holding_a_clean_member_copies(self):
        module = require("ontoloop.consumption")
        member = R12Member.AN
        holder = Holder(MappingProxyType({"k": member}))
        recorded = module.record_promotion(
            "r12 proxy member workflow", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIs(type(returned.part), dict)
        self.assertIs(returned.part["k"], member)

    def test_proxy_inside_a_holder_holding_a_list_member_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AO")
        holder = Holder(MappingProxyType({"k": member}))
        workflow = "r12 proxy mutable workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": holder})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover(workflow)
        self.assertEqual(found["answer"], "no promotion")

    def test_view_inside_a_holder_holding_a_list_member_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("AP")
        source = {"k": member}
        holder = Holder(source.values())
        workflow = "r12 view mutable workflow"
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(workflow, {"part": holder})
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_proxy_as_mapping_value_still_copies_as_a_mapping(self):
        module = require("ontoloop.consumption")
        proxy = MappingProxyType({"k": ["v"]})
        recorded = module.record_promotion(
            "r12 proxy standing workflow", {"part": proxy}
        )
        copied = recorded["bundle"]["part"]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": ["v"]})


if __name__ == "__main__":
    unittest.main()
