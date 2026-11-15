"""Fix round 15 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 15 triage
rulings 530, 531, 532, 533, 534, and 535: an uncopyable value in
a function annotation or in a function globals mapping in the
holding walk, a dictionary view or mapping proxy in a function
globals mapping in the replacements collection and the node
walk, a view or proxy in the state of a bound method wrapped
function or a property accessor function, the components of a
slice standing on its own in a fallback holder, an accepted
shape subclass instance carrying mutable added state, and the
socket, frame, traceback, coroutine, and async generator forms
inside a fallback holder. Each class pins its cure beside the
standing forms its charge protects.
"""

import asyncio
import socket
import sys
import threading
import types
import unittest
from datetime import datetime
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from ipaddress import IPv4Address
from types import MappingProxyType

from tests.harness import require

REFUSAL_MESSAGE = "enum member with mutable instance state in bundle copy"
UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"
SHAPE_MESSAGE = (
    "accepted shape subclass instance with mutable added state "
    "in bundle copy"
)


class R15Member(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class DecimalSub(Decimal):
    pass


class DecimalSlot(Decimal):
    __slots__ = ("held",)


class FractionSub(Fraction):
    pass


class FractionSlot(Fraction):
    __slots__ = ("held",)


class DateTimeSub(datetime):
    pass


class IPv4Sub(IPv4Address):
    pass


def _member_with_list(name):
    member = getattr(R15Member, name)
    member.held = ["original"]
    return member


def _generator():
    yield 1


async def _coroutine():
    return 1


async def _async_generator():
    yield 1


def _assert_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), REFUSAL_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


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


class TestRuling530HoldingWalkAnnotationsAndGlobals(unittest.TestCase):
    """Ruling 530: annotations and globals stand read for uncopyable."""

    def test_generator_in_an_annotation_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")

        def read(value: _generator() = None):
            return value

        _assert_uncopyable_refused(
            self, module, {"part": Holder(read)},
            "r15 annotation generator holder wf",
        )

    def test_lock_in_an_annotation_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")

        def read(value: threading.Lock() = None):
            return value

        _assert_uncopyable_refused(
            self, module, {"part": Holder(read)},
            "r15 annotation lock holder wf",
        )

    def test_lock_in_an_annotation_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")

        def read(value: threading.Lock() = None):
            return value

        _assert_uncopyable_refused(
            self, module, {"part": read},
            "r15 annotation lock direct wf",
        )

    def test_generator_in_synthetic_globals_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": _generator()}
        )
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r15 globals generator holder wf",
        )

    def test_lock_in_synthetic_globals_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": threading.Lock()}
        )
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r15 globals lock holder wf",
        )

    def test_generator_in_synthetic_globals_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": _generator()}
        )
        _assert_uncopyable_refused(
            self, module, {"part": func},
            "r15 globals generator direct wf",
        )

    def test_lock_in_module_function_globals_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        namespace = types.ModuleType("r15_synthetic_module")
        namespace.__dict__["__builtins__"] = {}
        namespace.__dict__["held_value"] = threading.Lock()
        exec(
            "def module_function():\n    return 1\n",
            namespace.__dict__,
        )
        func = namespace.__dict__["module_function"]
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r15 globals module function wf",
        )

    def test_module_in_synthetic_globals_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": types}
        )
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r15 globals module holder wf",
        )

    def test_cell_in_synthetic_globals_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": types.CellType(["x"])}
        )
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r15 globals cell holder wf",
        )

    def test_clean_synthetic_globals_function_still_copies(self):
        module = require("ontoloop.consumption")
        member = R15Member.A
        func = _synthetic_function(
            {"__builtins__": {}, "held_member": member}
        )
        holder = Holder(func)
        recorded = module.record_promotion(
            "r15 globals clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, func)
        self.assertIs(
            returned.part.__globals__["held_member"], member
        )

    def test_clean_annotation_function_still_copies(self):
        module = require("ontoloop.consumption")

        def read(value: int = None):
            return value

        holder = Holder(read)
        recorded = module.record_promotion(
            "r15 annotation clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, read)

    def test_generator_in_a_default_still_refused_beside_annotations(self):
        module = require("ontoloop.consumption")

        def read(value=_generator()):
            return value

        _assert_uncopyable_refused(
            self, module, {"part": Holder(read)},
            "r15 default generator control wf",
        )

    def test_member_in_an_annotation_still_refused_beside_uncopyable(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("B")

        def read(value: member = None):
            return value

        _assert_refused(
            self, module, {"part": Holder(read)},
            "r15 annotation member control wf",
        )

    def test_member_in_synthetic_globals_still_refused_beside_uncopyable(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("C")
        func = _synthetic_function(
            {"__builtins__": {}, "held_member": member}
        )
        _assert_refused(
            self, module, {"part": Holder(func)},
            "r15 globals member control wf",
        )


class TestRuling531GlobalsViewAndProxy(unittest.TestCase):
    """Ruling 531: a view or proxy in globals stands copied apart."""

    def test_values_view_in_globals_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": source.values()}
        )
        recorded = module.record_promotion(
            "r15 globals view wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, func)
        copied = returned.__globals__["held_value"]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [["v"]])
        self.assertIsNot(returned.__globals__, func.__globals__)
        source["k"].append("caller mutation")
        found = module.discover("r15 globals view wf")
        self.assertEqual(
            found["bundle"]["part"].part.__globals__["held_value"],
            [["v"]],
        )

    def test_proxy_in_globals_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": MappingProxyType(source)}
        )
        recorded = module.record_promotion(
            "r15 globals proxy wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, func)
        copied = returned.__globals__["held_value"]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": ["v"]})
        source["k"].append("caller mutation")
        found = module.discover("r15 globals proxy wf")
        self.assertEqual(
            found["bundle"]["part"].part.__globals__["held_value"],
            {"k": ["v"]},
        )

    def test_items_view_in_globals_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": source.items()}
        )
        recorded = module.record_promotion(
            "r15 globals items view wf", {"part": Holder(func)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, func)
        copied = returned.__globals__["held_value"]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [("k", ["v"])])
        source["k"].append("caller mutation")
        found = module.discover("r15 globals items view wf")
        self.assertEqual(
            found["bundle"]["part"].part.__globals__["held_value"],
            [("k", ["v"])],
        )

    def test_keys_view_in_globals_as_direct_value_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        func = _synthetic_function(
            {"__builtins__": {}, "held_value": source.keys()}
        )
        recorded = module.record_promotion(
            "r15 globals keys view direct wf", {"part": func}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, func)
        copied = returned.__globals__["held_value"]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, ["k"])

    def test_clean_synthetic_globals_function_still_shared(self):
        module = require("ontoloop.consumption")
        member = R15Member.D
        func = _synthetic_function(
            {"__builtins__": {}, "held_member": member}
        )
        holder = Holder(func)
        recorded = module.record_promotion(
            "r15 globals view clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, func)


class MethodTarget:
    def __init__(self):
        self.held = ["target state"]


def _bound_method(defaults=None, annotations=None):
    func = _synthetic_carrier(
        _template_method, {"__builtins__": {}}, defaults, annotations
    )
    target = MethodTarget()
    return types.MethodType(func, target), target


def _property_with(getter_defaults=None, getter_annotations=None,
                   setter_defaults=None, setter_annotations=None):
    getter = None
    setter = None
    if getter_defaults is not None or getter_annotations is not None:
        getter = _synthetic_carrier(
            _template_method, {"__builtins__": {}},
            getter_defaults, getter_annotations,
        )
    if setter_defaults is not None or setter_annotations is not None:
        setter = _synthetic_carrier(
            _template_method, {"__builtins__": {}},
            setter_defaults, setter_annotations,
        )
    return property(getter, setter), getter, setter


class TestRuling532PropertyAndBoundMethod(unittest.TestCase):
    """Ruling 532: the rebuild lands on a method and on a property."""

    def test_view_in_bound_method_default_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        method, target = _bound_method(defaults=(source.values(),))
        recorded = module.record_promotion(
            "r15 method view default wf", {"part": Holder(method)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, method)
        self.assertIsNot(returned.__func__, method.__func__)
        copied = returned.__func__.__defaults__[0]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [["v"]])
        self.assertIsNot(returned.__self__, target)
        source["k"].append("caller mutation")
        found = module.discover("r15 method view default wf")
        self.assertEqual(
            found["bundle"]["part"].part.__func__.__defaults__[0],
            [["v"]],
        )

    def test_proxy_in_bound_method_default_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        method, target = _bound_method(
            defaults=(MappingProxyType(source),)
        )
        recorded = module.record_promotion(
            "r15 method proxy default wf", {"part": Holder(method)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned.__func__, method.__func__)
        copied = returned.__func__.__defaults__[0]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": ["v"]})
        source["k"].append("caller mutation")
        found = module.discover("r15 method proxy default wf")
        self.assertEqual(
            found["bundle"]["part"].part.__func__.__defaults__[0],
            {"k": ["v"]},
        )

    def test_view_in_bound_method_annotation_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        method, target = _bound_method(
            annotations={"value": source.values()}
        )
        recorded = module.record_promotion(
            "r15 method view annotation wf", {"part": Holder(method)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned.__func__, method.__func__)
        copied = returned.__func__.__annotations__["value"]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [["v"]])
        source["k"].append("caller mutation")
        found = module.discover("r15 method view annotation wf")
        self.assertEqual(
            found["bundle"]["part"].part.__func__
            .__annotations__["value"],
            [["v"]],
        )

    def test_proxy_in_bound_method_annotation_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        method, target = _bound_method(
            annotations={"value": MappingProxyType(source)}
        )
        recorded = module.record_promotion(
            "r15 method proxy annotation wf", {"part": Holder(method)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned.__func__, method.__func__)
        copied = returned.__func__.__annotations__["value"]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": ["v"]})

    def test_view_in_property_getter_default_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        prop, getter, setter = _property_with(
            getter_defaults=(source.values(),)
        )
        recorded = module.record_promotion(
            "r15 property getter view default wf",
            {"part": Holder(prop)},
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIsNot(returned.fget, getter)
        copied = returned.fget.__defaults__[0]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [["v"]])
        source["k"].append("caller mutation")
        found = module.discover("r15 property getter view default wf")
        self.assertEqual(
            found["bundle"]["part"].part.fget.__defaults__[0],
            [["v"]],
        )

    def test_proxy_in_property_getter_annotation_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        prop, getter, setter = _property_with(
            getter_annotations={"value": MappingProxyType(source)}
        )
        recorded = module.record_promotion(
            "r15 property getter proxy annotation wf",
            {"part": Holder(prop)},
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIsNot(returned.fget, getter)
        copied = returned.fget.__annotations__["value"]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": ["v"]})

    def test_proxy_in_property_setter_default_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        prop, getter, setter = _property_with(
            setter_defaults=(MappingProxyType(source),)
        )
        recorded = module.record_promotion(
            "r15 property setter proxy default wf",
            {"part": Holder(prop)},
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIsNot(returned.fset, setter)
        copied = returned.fset.__defaults__[0]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": ["v"]})
        source["k"].append("caller mutation")
        found = module.discover("r15 property setter proxy default wf")
        self.assertEqual(
            found["bundle"]["part"].part.fset.__defaults__[0],
            {"k": ["v"]},
        )

    def test_view_in_property_setter_annotation_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        prop, getter, setter = _property_with(
            setter_annotations={"value": source.values()}
        )
        recorded = module.record_promotion(
            "r15 property setter view annotation wf",
            {"part": Holder(prop)},
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, prop)
        self.assertIsNot(returned.fset, setter)
        copied = returned.fset.__annotations__["value"]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [["v"]])

    def test_clean_bound_method_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        method, target = _bound_method(defaults=(R15Member.E,))
        holder = Holder(method)
        recorded = module.record_promotion(
            "r15 method clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part.__func__, method.__func__)
        self.assertEqual(returned.part(), R15Member.E)

    def test_clean_property_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        prop, getter, setter = _property_with(
            getter_defaults=(R15Member.F,)
        )
        holder = Holder(prop)
        recorded = module.record_promotion(
            "r15 property clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, prop)


class TestRuling533SliceComponents(unittest.TestCase):
    """Ruling 533: a slice standing on its own stands read by parts."""

    def test_member_component_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("G")
        _assert_refused(
            self, module, {"part": Holder(slice(member, 4))},
            "r15 slice member wf",
        )

    def test_generator_component_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(slice(_generator(), 4))},
            "r15 slice generator wf",
        )

    def test_lock_component_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(slice(0, threading.Lock()))},
            "r15 slice lock wf",
        )

    def test_lock_component_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": slice(threading.Lock(), 4)},
            "r15 slice lock direct wf",
        )

    def test_view_component_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        part = slice(source.values(), 4)
        recorded = module.record_promotion(
            "r15 slice view wf", {"part": Holder(part)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, part)
        self.assertIs(type(returned.start), list)
        self.assertEqual(returned.start, [["v"]])
        self.assertEqual(returned.stop, 4)
        source["k"].append("caller mutation")
        found = module.discover("r15 slice view wf")
        self.assertEqual(
            found["bundle"]["part"].part.start, [["v"]]
        )

    def test_proxy_component_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        part = slice(MappingProxyType(source), 4)
        recorded = module.record_promotion(
            "r15 slice proxy wf", {"part": Holder(part)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, part)
        self.assertIs(type(returned.start), dict)
        self.assertEqual(returned.start, {"k": ["v"]})
        source["k"].append("caller mutation")
        found = module.discover("r15 slice proxy wf")
        self.assertEqual(
            found["bundle"]["part"].part.start, {"k": ["v"]}
        )

    def test_clean_slice_inside_a_holder_still_copies(self):
        module = require("ontoloop.consumption")
        holder = Holder(slice(1, 10, 2))
        recorded = module.record_promotion(
            "r15 slice clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertEqual(returned.part, slice(1, 10, 2))

    def test_member_carrying_a_slice_with_a_lock_still_refused(self):
        module = require("ontoloop.consumption")
        member = R15Member.H
        member.held_slice = slice(threading.Lock(), 4)
        _assert_refused(
            self, module, {"part": Holder(member)},
            "r15 slice member carried control wf",
        )


class TestRuling534AcceptedShapeSubclassState(unittest.TestCase):
    """Ruling 534: mutable added state on a shape subclass refuses."""

    def _decimal_with_list(self):
        value = DecimalSub("1.5")
        value.held = ["original"]
        return value

    def _decimal_slot_with_list(self):
        value = DecimalSlot("1.5")
        value.held = ["original"]
        return value

    def _fraction_slot_with_list(self):
        value = FractionSlot(1, 3)
        value.held = ["original"]
        return value

    def _fraction_with_list(self):
        value = FractionSub(1, 3)
        value.held = ["original"]
        return value

    def _datetime_with_list(self):
        value = DateTimeSub(2024, 1, 2, 3, 4, 5)
        value.held = ["original"]
        return value

    def _ipv4_with_list(self):
        value = IPv4Sub("192.0.2.1")
        value.held = ["original"]
        return value

    def test_decimal_direct_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module, {"part": self._decimal_with_list()},
            "r15 shape decimal direct wf",
        )

    def test_decimal_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": Holder(self._decimal_with_list())},
            "r15 shape decimal holder wf",
        )

    def test_decimal_as_a_mapping_value_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": {"inner": self._decimal_with_list()}},
            "r15 shape decimal mapping wf",
        )

    def test_decimal_in_a_container_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": [self._decimal_with_list()]},
            "r15 shape decimal container wf",
        )

    def test_decimal_slot_direct_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module, {"part": self._decimal_slot_with_list()},
            "r15 shape decimal slot direct wf",
        )

    def test_decimal_slot_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": Holder(self._decimal_slot_with_list())},
            "r15 shape decimal slot holder wf",
        )

    def test_fraction_slot_direct_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module, {"part": self._fraction_slot_with_list()},
            "r15 shape fraction direct wf",
        )

    def test_fraction_slot_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": Holder(self._fraction_slot_with_list())},
            "r15 shape fraction holder wf",
        )

    def test_fraction_slot_as_a_mapping_value_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": {"inner": self._fraction_slot_with_list()}},
            "r15 shape fraction mapping wf",
        )

    def test_fraction_slot_in_a_container_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": [self._fraction_slot_with_list()]},
            "r15 shape fraction container wf",
        )

    def test_fraction_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": Holder(self._fraction_with_list())},
            "r15 shape fraction dict holder wf",
        )

    def test_datetime_direct_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module, {"part": self._datetime_with_list()},
            "r15 shape datetime direct wf",
        )

    def test_datetime_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": Holder(self._datetime_with_list())},
            "r15 shape datetime holder wf",
        )

    def test_datetime_as_a_mapping_value_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": {"inner": self._datetime_with_list()}},
            "r15 shape datetime mapping wf",
        )

    def test_datetime_in_a_container_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": [self._datetime_with_list()]},
            "r15 shape datetime container wf",
        )

    def test_ipv4_direct_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module, {"part": self._ipv4_with_list()},
            "r15 shape ipv4 direct wf",
        )

    def test_ipv4_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": Holder(self._ipv4_with_list())},
            "r15 shape ipv4 holder wf",
        )

    def test_ipv4_as_a_mapping_value_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": {"inner": self._ipv4_with_list()}},
            "r15 shape ipv4 mapping wf",
        )

    def test_ipv4_in_a_container_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_shape_refused(
            self, module,
            {"part": [self._ipv4_with_list()]},
            "r15 shape ipv4 container wf",
        )

    def test_plain_shape_instances_still_record(self):
        module = require("ontoloop.consumption")
        bundle = {
            "decimal": Decimal("1.5"),
            "fraction": Fraction(1, 3),
            "moment": datetime(2024, 1, 2, 3, 4, 5),
            "address": IPv4Address("192.0.2.1"),
        }
        recorded = module.record_promotion(
            "r15 shape plain wf", {"part": bundle}
        )
        returned = recorded["bundle"]["part"]
        self.assertEqual(returned["decimal"], Decimal("1.5"))
        self.assertIs(type(returned["decimal"]), Decimal)
        self.assertEqual(returned["fraction"], Fraction(1, 3))
        self.assertIs(type(returned["fraction"]), Fraction)
        self.assertEqual(
            returned["moment"], datetime(2024, 1, 2, 3, 4, 5)
        )
        self.assertIs(type(returned["moment"]), datetime)
        self.assertEqual(
            returned["address"], IPv4Address("192.0.2.1")
        )
        self.assertIs(type(returned["address"]), IPv4Address)

    def test_subclass_with_no_added_state_still_records(self):
        module = require("ontoloop.consumption")
        value = DecimalSub("2.5")
        recorded = module.record_promotion(
            "r15 shape subclass clean wf", {"part": value}
        )
        returned = recorded["bundle"]["part"]
        self.assertEqual(returned, Decimal("2.5"))
        self.assertIsInstance(returned, DecimalSub)

    def test_subclass_with_immutable_added_state_still_shared(self):
        module = require("ontoloop.consumption")
        value = DecimalSub("1.5")
        value.held = "clean text"
        recorded = module.record_promotion(
            "r15 shape subclass immutable wf", {"part": value}
        )
        returned = recorded["bundle"]["part"]
        self.assertIs(returned, value)
        self.assertEqual(returned.held, "clean text")


class TestRuling535FallbackHolderEscapeForms(unittest.TestCase):
    """Ruling 535: further uncopyable forms return the refusal."""

    def test_socket_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(sock)},
                "r15 escape socket holder wf",
            )
        finally:
            sock.close()

    def test_socket_as_a_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            _assert_uncopyable_refused(
                self, module, {"part": sock},
                "r15 escape socket direct wf",
            )
        finally:
            sock.close()

    def test_frame_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        frame = sys._getframe()
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(frame)},
                "r15 escape frame holder wf",
            )
        finally:
            del frame

    def test_frame_nested_in_a_list_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        frame = sys._getframe()
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder([frame])},
                "r15 escape frame nested wf",
            )
        finally:
            del frame

    def test_traceback_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        try:
            raise RuntimeError("probe")
        except RuntimeError:
            traceback = sys.exc_info()[2]
        _assert_uncopyable_refused(
            self, module, {"part": Holder(traceback)},
            "r15 escape traceback holder wf",
        )

    def test_coroutine_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        coro = _coroutine()
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(coro)},
                "r15 escape coroutine holder wf",
            )
        finally:
            coro.close()

    def test_async_generator_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        agen = _async_generator()
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(agen)},
                "r15 escape async generator holder wf",
            )
        finally:
            asyncio.run(agen.aclose())

    def test_thread_inside_a_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(threading.Thread(target=lambda: None))},
            "r15 escape thread control wf",
        )

    def test_plain_list_inside_a_holder_still_records(self):
        module = require("ontoloop.consumption")
        holder = Holder(["plain"])
        recorded = module.record_promotion(
            "r15 escape plain wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertEqual(returned.part, ["plain"])
        self.assertIsNot(returned.part, holder.part)


if __name__ == "__main__":
    unittest.main()
