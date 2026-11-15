"""Fix round 16 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 16 triage
rulings 572, 573, 574, 575, 576, and 577: a dictionary view or a
mapping proxy captured in a closure cell of a function or standing
in the attribute mapping of a function, the rebuild landing
breaking alias sharing at a bound method and at a shared globals
mapping, an accepted shape subclass instance of a family outside
the four families of ruling 534 carrying mutable added state, a
value of a further uncopyable type inside a fallback value, and
a property carrying a clean accessor beside a rebuilt accessor.
Each class pins its cure beside the standing forms its charge
protects.
"""

import contextvars
import mmap
import select
import socket
import sqlite3
import ssl
import sys
import tempfile
import threading
import types
import unittest
from datetime import date, time, timedelta
from decimal import Decimal
from enum import Enum
from ipaddress import IPv4Network, IPv6Address
from pathlib import PurePosixPath
from types import MappingProxyType

from tests.harness import require

REFUSAL_MESSAGE = "enum member with mutable instance state in bundle copy"
UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"
SHAPE_MESSAGE = (
    "accepted shape subclass instance with mutable added state "
    "in bundle copy"
)


class R16Member(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class PairHolder:
    """A plain custom class instance holding two parts."""

    def __init__(self, first, second):
        self.first = first
        self.second = second


class Service:
    def __init__(self):
        self.tags = ["original"]


class DecimalSub(Decimal):
    pass


class DateSub(date):
    pass


class TimeSub(time):
    pass


class TimedeltaSub(timedelta):
    pass


class IPv6Sub(IPv6Address):
    pass


class IPv4NetSub(IPv4Network):
    pass


class PurePosixSub(PurePosixPath):
    pass


def _assert_uncopyable_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), UNCOPYABLE_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _assert_shape_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), SHAPE_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _template():
    return 1


def _template_value(value=None):
    return value


def _template_method(self, value=None):
    return value


def _synthetic_function(globals_map):
    return types.FunctionType(_template.__code__, globals_map, "synthetic")


def _synthetic_carrier(template, globals_map, defaults=None,
                       annotations=None):
    func = types.FunctionType(
        template.__code__, globals_map, template.__name__
    )
    if defaults is not None:
        func.__defaults__ = defaults
    if annotations is not None:
        func.__annotations__ = annotations
    return func


def _make_closure_template():
    marker = None

    def template():
        return marker

    return template


def _make_closure_default_template():
    marker = None

    def template(value=None):
        return (marker, value)

    return template


_CLOSURE_TEMPLATE = _make_closure_template()
_CLOSURE_DEFAULT_TEMPLATE = _make_closure_default_template()


def _closure_over(value):
    return types.FunctionType(
        _CLOSURE_TEMPLATE.__code__, {"__builtins__": {}}, "closure_fn",
        None, (types.CellType(value),),
    )


class TestRuling572ClosureCellViewAndProxy(unittest.TestCase):
    """Ruling 572: a view or proxy in a closure cell copies apart."""

    def test_values_view_in_closure_cell_inside_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        func = _closure_over(source.values())
        recorded = module.record_promotion(
            "r16 closure view holder wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, func)
        cell_copy = returned.__closure__[0].cell_contents
        self.assertIs(type(cell_copy), list)
        self.assertEqual(cell_copy, [[1]])
        source["k"].append(99)
        self.assertEqual(returned(), [[1]])
        found = module.discover("r16 closure view holder wf")
        discovered = found["bundle"]["part"].part
        self.assertEqual(discovered(), [[1]])

    def test_proxy_in_closure_cell_inside_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        func = _closure_over(MappingProxyType(source))
        recorded = module.record_promotion(
            "r16 closure proxy holder wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, func)
        cell_copy = returned.__closure__[0].cell_contents
        self.assertIs(type(cell_copy), dict)
        self.assertEqual(cell_copy, {"k": [1]})
        source["k"].append(99)
        found = module.discover("r16 closure proxy holder wf")
        discovered = found["bundle"]["part"].part
        self.assertEqual(
            discovered.__closure__[0].cell_contents, {"k": [1]}
        )

    def test_values_view_in_closure_cell_as_direct_value_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        func = _closure_over(source.values())
        recorded = module.record_promotion(
            "r16 closure view direct wf", {"part": func}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, func)
        self.assertEqual(
            returned.__closure__[0].cell_contents, [[1]]
        )
        source["k"].append(99)
        found = module.discover("r16 closure view direct wf")
        self.assertEqual(found["bundle"]["part"](), [[1]])

    def test_rebuilt_function_still_copies_closure_view_apart(self):
        module = require("ontoloop.consumption")
        cell_source = {"k": [1]}
        default_source = {"d": [2]}

        func = types.FunctionType(
            _CLOSURE_DEFAULT_TEMPLATE.__code__, {"__builtins__": {}},
            "closure_fn", (default_source.values(),),
            (types.CellType(cell_source.values()),),
        )
        recorded = module.record_promotion(
            "r16 closure rebuilt wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, func)
        self.assertEqual(returned.__defaults__[0], [[2]])
        self.assertEqual(
            returned.__closure__[0].cell_contents, [[1]]
        )
        cell_source["k"].append(99)
        default_source["d"].append(99)
        found = module.discover("r16 closure rebuilt wf")
        discovered = found["bundle"]["part"].part
        self.assertEqual(discovered.__defaults__[0], [[2]])
        self.assertEqual(discovered(), ([[1]], [[2]]))

    def test_view_in_closure_of_property_getter_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _closure_over(source.values())
        prop = property(getter)
        recorded = module.record_promotion(
            "r16 closure property wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIsNot(returned.fget, getter)
        self.assertEqual(
            returned.fget.__closure__[0].cell_contents, [[1]]
        )
        source["k"].append(99)
        found = module.discover("r16 closure property wf")
        discovered = found["bundle"]["part"].part
        self.assertEqual(discovered.fget(), [[1]])

    def test_clean_closure_function_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        func = _closure_over(7)
        recorded = module.record_promotion(
            "r16 closure clean wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIs(returned, func)
        self.assertEqual(returned(), 7)

    def test_member_in_closure_cell_still_refused(self):
        module = require("ontoloop.consumption")
        member = R16Member.A
        member.held = ["original"]
        func = _closure_over(member)
        with self.assertRaises(ValueError) as caught:
            module.record_promotion(
                "r16 closure member wf", {"part": Holder(func)}
            )
        self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
        found = module.discover("r16 closure member wf")
        self.assertEqual(found["answer"], "no promotion")


class TestRuling573AttributeMappingViewAndProxy(unittest.TestCase):
    """Ruling 573: a view or proxy in a function attribute copies apart."""

    def _attributed_function(self, value):
        func = _synthetic_function({"__builtins__": {}})
        func.held = value
        return func

    def test_values_view_in_attribute_inside_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        func = self._attributed_function(source.values())
        recorded = module.record_promotion(
            "r16 attribute view holder wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, func)
        self.assertIs(type(returned.held), list)
        self.assertEqual(returned.held, [[1]])
        source["k"].append(99)
        found = module.discover("r16 attribute view holder wf")
        self.assertEqual(found["bundle"]["part"].part.held, [[1]])

    def test_proxy_in_attribute_inside_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        func = self._attributed_function(MappingProxyType(source))
        recorded = module.record_promotion(
            "r16 attribute proxy holder wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, func)
        self.assertIs(type(returned.held), dict)
        self.assertEqual(returned.held, {"k": [1]})
        source["k"].append(99)
        found = module.discover("r16 attribute proxy holder wf")
        self.assertEqual(
            found["bundle"]["part"].part.held, {"k": [1]}
        )

    def test_values_view_in_attribute_as_direct_value_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        func = self._attributed_function(source.values())
        recorded = module.record_promotion(
            "r16 attribute view direct wf", {"part": func}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, func)
        self.assertEqual(returned.held, [[1]])
        source["k"].append(99)
        found = module.discover("r16 attribute view direct wf")
        self.assertEqual(found["bundle"]["part"].held, [[1]])

    def test_clean_attribute_function_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        func = self._attributed_function(7)
        recorded = module.record_promotion(
            "r16 attribute clean wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIs(returned, func)
        self.assertEqual(returned.held, 7)

    def test_lock_in_attribute_still_refused(self):
        module = require("ontoloop.consumption")
        func = self._attributed_function(threading.Lock())
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r16 attribute lock wf",
        )


class TestRuling574RebuildAliasSharing(unittest.TestCase):
    """Ruling 574: the rebuild landing carries alias sharing."""

    def test_rebuilt_bound_method_shares_the_landed_bound_object(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        service = Service()
        func = _synthetic_carrier(
            _template_method, {"__builtins__": {}},
            defaults=(source.values(),),
        )
        method = types.MethodType(func, service)
        holder = PairHolder(service, method)
        recorded = module.record_promotion(
            "r16 alias method wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned.first, service)
        self.assertIs(returned.second.__self__, returned.first)
        self.assertEqual(returned.second.__defaults__[0], [["v"]])
        found = module.discover("r16 alias method wf")
        discovered = found["bundle"]["part"]
        self.assertIs(discovered.second.__self__, discovered.first)
        discovered.first.tags.append("copy side")
        self.assertEqual(discovered.second.__self__.tags,
                         ["original", "copy side"])
        self.assertEqual(service.tags, ["original"])

    def test_two_rebuilt_functions_share_one_copied_globals(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        shared = {"__builtins__": {}, "held": source.values()}
        first = _synthetic_function(shared)
        second = _synthetic_function(shared)
        holder = PairHolder(first, second)
        recorded = module.record_promotion(
            "r16 alias globals wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned.first, first)
        self.assertIsNot(returned.second, second)
        self.assertIs(returned.first.__globals__,
                      returned.second.__globals__)
        self.assertIsNot(returned.first.__globals__, shared)
        self.assertEqual(returned.first.__globals__["held"], [[1]])
        source["k"].append(99)
        found = module.discover("r16 alias globals wf")
        discovered = found["bundle"]["part"]
        self.assertIs(discovered.first.__globals__,
                      discovered.second.__globals__)
        self.assertEqual(
            discovered.first.__globals__["held"], [[1]]
        )

    def test_clean_bound_method_alias_still_carried(self):
        module = require("ontoloop.consumption")
        service = Service()
        func = _synthetic_carrier(
            _template_method, {"__builtins__": {}}
        )
        method = types.MethodType(func, service)
        holder = PairHolder(service, method)
        recorded = module.record_promotion(
            "r16 alias method clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned.first, service)
        self.assertIs(returned.second.__self__, returned.first)

    def test_two_occurrences_of_one_rebuilt_function_stand_as_one(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        func = _synthetic_carrier(
            _template_value, {"__builtins__": {}},
            defaults=(source.values(),),
        )
        holder = PairHolder(func, func)
        recorded = module.record_promotion(
            "r16 alias one function wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned.first, func)
        self.assertIs(returned.second, returned.first)
        self.assertEqual(returned.first.__defaults__[0], [[1]])


def _shape_positions(case, module, make, label):
    _assert_shape_refused(
        case, module, {"part": make()}, label + " direct wf"
    )
    _assert_shape_refused(
        case, module, {"part": Holder(make())}, label + " holder wf"
    )
    _assert_shape_refused(
        case, module, {"part": {"inner": make()}},
        label + " mapping wf",
    )
    _assert_shape_refused(
        case, module, {"part": [make()]}, label + " container wf"
    )


class TestRuling575ShapeSubclassOutsideFourFamilies(unittest.TestCase):
    """Ruling 575: shape families outside the four refuse alike."""

    def test_date_subclass_with_mutable_added_state_is_refused(self):
        module = require("ontoloop.consumption")

        def make():
            value = DateSub(2026, 1, 2)
            value.held = ["original"]
            return value

        _shape_positions(self, module, make, "r16 shape date")

    def test_time_subclass_with_mutable_added_state_is_refused(self):
        module = require("ontoloop.consumption")

        def make():
            value = TimeSub(3, 4, 5)
            value.held = ["original"]
            return value

        _shape_positions(self, module, make, "r16 shape time")

    def test_timedelta_subclass_with_mutable_added_state_is_refused(self):
        module = require("ontoloop.consumption")

        def make():
            value = TimedeltaSub(days=2)
            value.held = ["original"]
            return value

        _shape_positions(self, module, make, "r16 shape timedelta")

    def test_ipv6_subclass_with_mutable_added_state_is_refused(self):
        module = require("ontoloop.consumption")

        def make():
            value = IPv6Sub("::1")
            value.held = ["original"]
            return value

        _shape_positions(self, module, make, "r16 shape ipv6")

    def test_ipv4network_subclass_with_mutable_added_state_is_refused(self):
        module = require("ontoloop.consumption")

        def make():
            value = IPv4NetSub("10.0.0.0/8")
            value.held = ["original"]
            return value

        _shape_positions(self, module, make, "r16 shape ipv4net")

    def test_pure_path_subclass_with_mutable_added_state_is_refused(self):
        module = require("ontoloop.consumption")

        def make():
            value = PurePosixSub("a/b")
            value.held = ["original"]
            return value

        _shape_positions(self, module, make, "r16 shape path")

    def test_plain_shape_instances_still_record(self):
        module = require("ontoloop.consumption")
        plains = [
            date(2026, 1, 2), time(3, 4, 5), timedelta(days=2),
            IPv6Address("::1"), IPv4Network("10.0.0.0/8"),
            PurePosixPath("a/b"),
        ]
        for index, value in enumerate(plains):
            recorded = module.record_promotion(
                "r16 shape plain %d wf" % index, {"part": value}
            )
            self.assertEqual(recorded["bundle"]["part"], value)
            found = module.discover("r16 shape plain %d wf" % index)
            self.assertEqual(found["bundle"]["part"], value)

    def test_subclass_with_no_added_state_still_records(self):
        module = require("ontoloop.consumption")
        values = [
            DateSub(2026, 1, 2), TimeSub(3, 4, 5),
            TimedeltaSub(days=2), IPv6Sub("::1"),
            IPv4NetSub("10.0.0.0/8"), PurePosixSub("a/b"),
        ]
        for index, value in enumerate(values):
            recorded = module.record_promotion(
                "r16 shape clean %d wf" % index, {"part": value}
            )
            self.assertEqual(recorded["bundle"]["part"], value)
            self.assertIs(type(recorded["bundle"]["part"]), type(value))

    def test_subclass_with_immutable_added_state_still_records(self):
        module = require("ontoloop.consumption")
        date_value = DateSub(2026, 1, 2)
        date_value.held = "clean"
        ipv6_value = IPv6Sub("::1")
        ipv6_value.held = 7
        for index, value in enumerate([date_value, ipv6_value]):
            recorded = module.record_promotion(
                "r16 shape immutable %d wf" % index, {"part": value}
            )
            self.assertEqual(recorded["bundle"]["part"], value)
            found = module.discover(
                "r16 shape immutable %d wf" % index
            )
            self.assertEqual(found["bundle"]["part"], value)

    def test_decimal_family_still_refused(self):
        module = require("ontoloop.consumption")
        value = DecimalSub("1.5")
        value.held = ["original"]
        _assert_shape_refused(
            self, module, {"part": Holder(value)},
            "r16 shape decimal control wf",
        )


class TestRuling576FurtherUncopyableTypes(unittest.TestCase):
    """Ruling 576: further uncopyable types return the refusal."""

    def test_file_objects_inside_a_holder_are_refused(self):
        module = require("ontoloop.consumption")
        handle = tempfile.NamedTemporaryFile(
            mode="wb", suffix=".bin", delete=False
        )
        handle.write(b"data")
        handle.close()
        path = handle.name
        streams = []
        try:
            streams.append(open(path, "rb"))
            streams.append(open(path, "r"))
            streams.append(open(path, "rb", buffering=0))
            for index, stream in enumerate(streams):
                _assert_uncopyable_refused(
                    self, module, {"part": Holder(stream)},
                    "r16 file holder %d wf" % index,
                )
            _assert_uncopyable_refused(
                self, module, {"part": streams[0]},
                "r16 file direct wf",
            )
        finally:
            for stream in streams:
                stream.close()

    def test_thread_local_inside_holder_and_mapping_value_refused(self):
        module = require("ontoloop.consumption")
        local = threading.local()
        local.held = 1
        _assert_uncopyable_refused(
            self, module, {"part": Holder(local)},
            "r16 thread local holder wf",
        )
        _assert_uncopyable_refused(
            self, module, {"part": {"inner": local}},
            "r16 thread local mapping wf",
        )

    def test_sqlite_connection_inside_holder_and_nested_refused(self):
        module = require("ontoloop.consumption")
        connection = sqlite3.connect(":memory:")
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(connection)},
                "r16 sqlite holder wf",
            )
            _assert_uncopyable_refused(
                self, module, {"part": Holder([connection])},
                "r16 sqlite nested wf",
            )
        finally:
            connection.close()

    def test_mmap_inside_holder_and_as_direct_value_refused(self):
        module = require("ontoloop.consumption")
        mapping = mmap.mmap(-1, 8)
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(mapping)},
                "r16 mmap holder wf",
            )
            _assert_uncopyable_refused(
                self, module, {"part": mapping},
                "r16 mmap direct wf",
            )
        finally:
            mapping.close()

    def test_memoryview_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(memoryview(b"abc"))},
            "r16 memoryview holder wf",
        )

    def test_context_object_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(contextvars.Context())},
            "r16 context holder wf",
        )

    def test_ssl_context_inside_holder_and_as_direct_value_refused(self):
        module = require("ontoloop.consumption")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        _assert_uncopyable_refused(
            self, module, {"part": Holder(context)},
            "r16 ssl holder wf",
        )
        _assert_uncopyable_refused(
            self, module, {"part": context},
            "r16 ssl direct wf",
        )

    def test_epoll_object_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        poller = select.epoll()
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(poller)},
                "r16 epoll holder wf",
            )
        finally:
            poller.close()

    def test_socket_inside_a_holder_still_refused(self):
        module = require("ontoloop.consumption")
        left, right = socket.socketpair()
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(left)},
                "r16 socket control wf",
            )
        finally:
            left.close()
            right.close()

    def test_bytesio_inside_a_holder_still_records(self):
        module = require("ontoloop.consumption")
        import io

        recorded = module.record_promotion(
            "r16 bytesio control wf", {"part": Holder(io.BytesIO(b"xy"))}
        )
        self.assertEqual(recorded["bundle"]["part"].part.read(), b"xy")
        found = module.discover("r16 bytesio control wf")
        self.assertEqual(found["bundle"]["part"].part.read(), b"xy")

    def test_plain_list_inside_a_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r16 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])

    def test_memoryview_at_walked_position_still_copies_as_bytearray(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r16 memoryview walked wf", {"part": memoryview(b"abc")}
        )
        copied = recorded["bundle"]["part"]
        self.assertIs(type(copied), bytearray)
        self.assertEqual(bytes(copied), b"abc")
        listed = module.record_promotion(
            "r16 memoryview listed wf", {"part": [memoryview(b"de")]}
        )
        self.assertIs(type(listed["bundle"]["part"][0]), bytearray)
        self.assertEqual(bytes(listed["bundle"]["part"][0]), b"de")


def _clean_accessor():
    return _synthetic_carrier(
        _template_method, {"__builtins__": {}}
    )


def _accessor_with_default(value):
    return _synthetic_carrier(
        _template_method, {"__builtins__": {}}, defaults=(value,)
    )


class TestRuling577PropertyMixedAccessors(unittest.TestCase):
    """Ruling 577: a clean accessor beside a rebuilt one records."""

    def test_view_in_deleter_default_with_clean_getter_setter(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _clean_accessor()
        setter = _clean_accessor()
        deleter = _accessor_with_default(source.values())
        prop = property(getter, setter, deleter)
        recorded = module.record_promotion(
            "r16 property deleter wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIs(returned.fget, getter)
        self.assertIs(returned.fset, setter)
        self.assertIsNot(returned.fdel, deleter)
        self.assertEqual(returned.fdel.__defaults__[0], [[1]])
        source["k"].append(99)
        found = module.discover("r16 property deleter wf")
        self.assertEqual(
            found["bundle"]["part"].part.fdel.__defaults__[0], [[1]]
        )

    def test_view_in_setter_default_with_clean_getter_deleter(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _clean_accessor()
        setter = _accessor_with_default(source.values())
        deleter = _clean_accessor()
        prop = property(getter, setter, deleter)
        recorded = module.record_promotion(
            "r16 property setter wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIs(returned.fget, getter)
        self.assertIs(returned.fdel, deleter)
        self.assertEqual(returned.fset.__defaults__[0], [[1]])
        source["k"].append(99)
        found = module.discover("r16 property setter wf")
        self.assertEqual(
            found["bundle"]["part"].part.fset.__defaults__[0], [[1]]
        )

    def test_view_in_getter_default_with_clean_setter(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _accessor_with_default(source.values())
        setter = _clean_accessor()
        prop = property(getter, setter)
        recorded = module.record_promotion(
            "r16 property getter wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIs(returned.fset, setter)
        self.assertEqual(returned.fget.__defaults__[0], [[1]])
        source["k"].append(99)
        found = module.discover("r16 property getter wf")
        self.assertEqual(
            found["bundle"]["part"].part.fget.__defaults__[0], [[1]]
        )

    def test_view_in_deleter_annotation_with_clean_getter_setter(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _clean_accessor()
        setter = _clean_accessor()
        deleter = _synthetic_carrier(
            _template_method, {"__builtins__": {}},
            annotations={"value": source.values()},
        )
        prop = property(getter, setter, deleter)
        recorded = module.record_promotion(
            "r16 property deleter annotation wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIs(returned.fget, getter)
        self.assertIs(returned.fset, setter)
        self.assertEqual(
            returned.fdel.__annotations__["value"], [[1]]
        )
        source["k"].append(99)
        found = module.discover("r16 property deleter annotation wf")
        self.assertEqual(
            found["bundle"]["part"].part.fdel.__annotations__["value"],
            [[1]],
        )

    def test_view_in_deleter_globals_with_clean_getter_setter(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _clean_accessor()
        setter = _clean_accessor()
        deleter = _synthetic_carrier(
            _template_method,
            {"__builtins__": {}, "held": source.values()},
        )
        prop = property(getter, setter, deleter)
        recorded = module.record_promotion(
            "r16 property deleter globals wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIs(returned.fget, getter)
        self.assertIs(returned.fset, setter)
        self.assertEqual(returned.fdel.__globals__["held"], [[1]])
        source["k"].append(99)
        found = module.discover("r16 property deleter globals wf")
        self.assertEqual(
            found["bundle"]["part"].part.fdel.__globals__["held"],
            [[1]],
        )

    def test_proxy_in_setter_default_with_clean_getter(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _clean_accessor()
        setter = _accessor_with_default(MappingProxyType(source))
        prop = property(getter, setter)
        recorded = module.record_promotion(
            "r16 property setter proxy wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIs(returned.fget, getter)
        copied = returned.fset.__defaults__[0]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": [1]})
        source["k"].append(99)
        found = module.discover("r16 property setter proxy wf")
        self.assertEqual(
            found["bundle"]["part"].part.fset.__defaults__[0],
            {"k": [1]},
        )

    def test_view_in_deleter_default_as_direct_bundle_value(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _clean_accessor()
        setter = _clean_accessor()
        deleter = _accessor_with_default(source.values())
        prop = property(getter, setter, deleter)
        recorded = module.record_promotion(
            "r16 property direct wf", {"part": prop}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, prop)
        self.assertIs(returned.fget, getter)
        self.assertEqual(returned.fdel.__defaults__[0], [[1]])

    def test_sole_accessor_with_view_still_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        deleter = _accessor_with_default(source.values())
        prop = property(None, None, deleter)
        recorded = module.record_promotion(
            "r16 property sole wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertEqual(returned.fdel.__defaults__[0], [[1]])

    def test_all_accessors_with_view_still_copy_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        getter = _accessor_with_default(source.values())
        setter = _accessor_with_default(source.values())
        deleter = _accessor_with_default(source.values())
        prop = property(getter, setter, deleter)
        recorded = module.record_promotion(
            "r16 property all wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertEqual(returned.fget.__defaults__[0], [[1]])
        self.assertEqual(returned.fset.__defaults__[0], [[1]])
        self.assertEqual(returned.fdel.__defaults__[0], [[1]])

    def test_clean_property_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        prop = property(
            _clean_accessor(), _clean_accessor(), _clean_accessor()
        )
        recorded = module.record_promotion(
            "r16 property clean wf", {"part": Holder(prop)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIs(returned, prop)


if __name__ == "__main__":
    unittest.main()
