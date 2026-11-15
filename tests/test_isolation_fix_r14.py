"""Fix round 14 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 14 triage
rulings 483, 484, 485, 486, and 487: the annotations a function
carries in the fallback scan and the fallback replacements, the
reentrant lock and threading condition forms in the holding walk,
the governed refusal for a cell, classmethod, staticmethod, and
escaping module form inside a fallback holder, the state a
function carries in the holding walk, and the globals mapping a
function reads in the fallback scan. Each class pins its cure
beside the standing forms its charge protects.
"""

import functools
import os
import threading
import types
import unittest
from enum import Enum
from types import MappingProxyType

from tests.harness import require

REFUSAL_MESSAGE = "enum member with mutable instance state in bundle copy"
UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class R14Member(Enum):
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


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


def _member_with_list(name):
    member = getattr(R14Member, name)
    member.held = ["original"]
    return member


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


def _generator():
    yield 1


class TestRuling483FunctionAnnotations(unittest.TestCase):
    """Ruling 483: the annotations a function carries stand read."""

    def test_member_in_a_parameter_annotation_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("A")

        def read(value: member = None):
            return value

        _assert_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 annotation parameter holder wf",
        )

    def test_member_in_a_return_annotation_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("B")

        def read() -> member:
            return None

        _assert_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 annotation return holder wf",
        )

    def test_member_in_a_parameter_annotation_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("C")

        def read(value: member = None):
            return value

        _assert_refused(
            self,
            module,
            {"part": read},
            "r14 annotation parameter direct wf",
        )

    def test_member_in_a_property_getter_annotation_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("D")

        def build(annotated):
            def getter(self):
                return None

            getter.__annotations__ = {"value": annotated}
            return property(getter)

        _assert_refused(
            self,
            module,
            {"part": Holder(build(member))},
            "r14 annotation property getter wf",
        )

    def test_member_in_a_bound_method_function_annotation_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("E")

        def build(annotated):
            def inner(self, value=None):
                return value

            inner.__annotations__ = {"value": annotated}

            class Target:
                pass

            return types.MethodType(inner, Target())

        _assert_refused(
            self,
            module,
            {"part": Holder(build(member))},
            "r14 annotation bound method wf",
        )

    def test_clean_member_in_an_annotation_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        member = R14Member.F

        def read(value: member = None):
            return value

        holder = Holder(read)
        recorded = module.record_promotion(
            "r14 annotation clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, read)
        self.assertIs(
            returned.part.__annotations__["value"], member
        )

    def test_view_in_an_annotation_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}

        def read(value=None):
            return value

        read.__annotations__ = {"value": source.values()}
        recorded = module.record_promotion(
            "r14 annotation view wf", {"part": Holder(read)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, read)
        copied = returned.__annotations__["value"]
        self.assertIs(type(copied), list)
        self.assertEqual(copied, [["v"]])
        source["k"].append("caller mutation")
        found = module.discover("r14 annotation view wf")
        self.assertEqual(
            found["bundle"]["part"].part.__annotations__["value"],
            [["v"]],
        )

    def test_proxy_in_an_annotation_inside_a_holder_copies_apart(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}

        def read(value=None):
            return value

        read.__annotations__ = {"value": MappingProxyType(source)}
        recorded = module.record_promotion(
            "r14 annotation proxy wf", {"part": Holder(read)}
        )
        returned = recorded["bundle"]["part"].part
        self.assertIsNot(returned, read)
        copied = returned.__annotations__["value"]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": ["v"]})
        source["k"].append("caller mutation")
        found = module.discover("r14 annotation proxy wf")
        self.assertEqual(
            found["bundle"]["part"].part.__annotations__["value"],
            {"k": ["v"]},
        )


class TestRuling484ReentrantLock(unittest.TestCase):
    """Ruling 484: a reentrant lock and a condition stand refused."""

    def test_reentrant_lock_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(threading.RLock())},
            "r14 rlock holder wf",
        )

    def test_reentrant_lock_as_a_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": threading.RLock()},
            "r14 rlock direct wf",
        )

    def test_reentrant_lock_nested_in_a_list_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder([threading.RLock()])},
            "r14 rlock nested wf",
        )

    def test_reentrant_lock_as_a_partial_argument_is_refused(self):
        module = require("ontoloop.consumption")
        part = functools.partial(lambda lock: lock, threading.RLock())
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(part)},
            "r14 rlock partial wf",
        )

    def test_reentrant_lock_inside_a_bound_object_is_refused(self):
        module = require("ontoloop.consumption")

        class Bound:
            def __init__(self):
                self.lock = threading.RLock()

            def read(self):
                return self.lock

        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(Bound().read)},
            "r14 rlock bound object wf",
        )

    def test_threading_condition_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(threading.Condition())},
            "r14 condition holder wf",
        )

    def test_plain_lock_and_semaphore_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(threading.Lock())},
            "r14 plain lock control wf",
        )
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(threading.Semaphore())},
            "r14 semaphore control wf",
        )

    def test_plain_list_inside_a_holder_still_records(self):
        module = require("ontoloop.consumption")
        holder = Holder(["plain"])
        recorded = module.record_promotion(
            "r14 rlock plain wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertEqual(returned.part, ["plain"])
        self.assertIsNot(returned.part, holder.part)


class TestRuling485FallbackEscapeForms(unittest.TestCase):
    """Ruling 485: cell, classmethod, staticmethod, module forms."""

    def test_cell_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        cell = types.CellType(["original"])
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(cell)},
            "r14 escape cell wf",
        )

    def test_classmethod_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(classmethod(lambda cls: 1))},
            "r14 escape classmethod wf",
        )

    def test_staticmethod_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(staticmethod(lambda: 1))},
            "r14 escape staticmethod wf",
        )

    def test_module_in_its_escaping_form_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(types)},
            "r14 escape module wf",
        )

    def test_module_in_its_governed_refusal_form_still_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.record_promotion(
                "r14 module governed wf", {"part": Holder(os)}
            )
        found = module.discover("r14 module governed wf")
        self.assertEqual(found["answer"], "no promotion")
        self.assertIsNone(found["bundle"])

    def test_generator_inside_a_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(_generator())},
            "r14 escape generator control wf",
        )

    def test_plain_list_inside_a_holder_still_records(self):
        module = require("ontoloop.consumption")
        holder = Holder(["plain"])
        recorded = module.record_promotion(
            "r14 escape plain wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertEqual(returned.part, ["plain"])


class TestRuling486FunctionCarriedUncopyable(unittest.TestCase):
    """Ruling 486: uncopyable state a function carries stands refused."""

    def test_generator_in_a_positional_default_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")

        def read(value=_generator()):
            return value

        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 function default generator wf",
        )

    def test_lock_in_a_positional_default_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")

        def read(value=threading.Lock()):
            return value

        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 function default lock wf",
        )

    def test_lock_in_a_keyword_default_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")

        def read(*, value=threading.Lock()):
            return value

        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 function kwdefault lock wf",
        )

    def test_generator_in_a_closure_cell_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        captured = _generator()

        def read():
            return captured

        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 function closure generator wf",
        )

    def test_lock_in_a_closure_cell_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        captured = threading.Lock()

        def read():
            return captured

        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 function closure lock wf",
        )

    def test_generator_in_a_property_getter_closure_is_refused(self):
        module = require("ontoloop.consumption")
        captured = _generator()

        def build(value):
            def getter(self):
                return value

            return property(getter)

        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(build(captured))},
            "r14 property closure generator wf",
        )

    def test_generator_in_a_tuple_inside_a_default_is_refused(self):
        module = require("ontoloop.consumption")

        def read(value=(_generator(),)):
            return value

        _assert_uncopyable_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 function default tuple generator wf",
        )

    def test_clean_function_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        member = R14Member.G
        captured = member

        def read(value=member):
            return (value, captured)

        holder = Holder(read)
        recorded = module.record_promotion(
            "r14 function clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, read)
        self.assertIs(returned.part.__defaults__[0], member)


class TestRuling487FunctionGlobals(unittest.TestCase):
    """Ruling 487: the globals mapping a function reads stands read."""

    def _synthetic_function(self, globals_map):
        def template():
            return 1

        return types.FunctionType(
            template.__code__, globals_map, "synthetic"
        )

    def test_member_in_synthetic_globals_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("H")
        func = self._synthetic_function(
            {"__builtins__": {}, "held_member": member}
        )
        _assert_refused(
            self,
            module,
            {"part": Holder(func)},
            "r14 globals synthetic holder wf",
        )

    def test_member_in_synthetic_globals_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("I")
        func = self._synthetic_function(
            {"__builtins__": {}, "held_member": member}
        )
        _assert_refused(
            self,
            module,
            {"part": func},
            "r14 globals synthetic direct wf",
        )

    def test_member_in_module_function_globals_inside_a_holder_is_refused(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("J")
        namespace = types.ModuleType("r14_synthetic_module")
        namespace.__dict__["__builtins__"] = {}
        namespace.__dict__["held_member"] = member
        exec(
            "def module_function():\n    return 1\n",
            namespace.__dict__,
        )
        func = namespace.__dict__["module_function"]
        _assert_refused(
            self,
            module,
            {"part": Holder(func)},
            "r14 globals module function wf",
        )

    def test_clean_globals_function_still_copies_in_standing_form(self):
        module = require("ontoloop.consumption")
        member = R14Member.K
        func = self._synthetic_function(
            {"__builtins__": {}, "held_member": member}
        )
        holder = Holder(func)
        recorded = module.record_promotion(
            "r14 globals clean wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIsNot(returned, holder)
        self.assertIs(returned.part, func)
        self.assertIs(
            returned.part.__globals__["held_member"], member
        )

    def test_member_in_a_default_still_refused_beside_globals(self):
        module = require("ontoloop.consumption")
        member = _member_with_list("L")

        def read(value=member):
            return value

        _assert_refused(
            self,
            module,
            {"part": Holder(read)},
            "r14 globals default control wf",
        )


if __name__ == "__main__":
    unittest.main()
