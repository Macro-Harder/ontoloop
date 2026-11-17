"""Fix round 24 supplement tests for ruling 1044: the globals limb.

Written test first for the one limb of ruling 1044 (ISO-R24-9,
absorbing Lead Engineer lines E-52 and E-53) that the Fix round 24
trace graded PARTIAL: a governed uncopyable value standing as a
bare direct value in the globals mapping of a function member of
the namespace of a class standing as a bundle value, where the
landed reading reaches the globals of a member function only for
a value standing as a bound builtin callable or a bound method.
Each refused form below stands pinned beside the nearest controls
its narrowing history names: a member function whose module
globals carry a governed value the member never reaches into
still records, a member function over a globals mapping holding
only plain values still records, and the bound callable globals
form the landed reading already refuses still refuses.
"""

import threading
import types
import unittest

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


def _assert_uncopyable_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), UNCOPYABLE_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _template(value):
    return value


def _synthetic_member_class(globals_map, member_kind):
    carried = types.FunctionType(
        _template.__code__, globals_map, "carried"
    )

    class MemberClass:
        pass

    if member_kind == "function":
        MemberClass.carried = carried
    elif member_kind == "property":
        MemberClass.carried = property(carried)
    elif member_kind == "classmethod":
        MemberClass.carried = classmethod(carried)
    elif member_kind == "staticmethod":
        MemberClass.carried = staticmethod(carried)
    return MemberClass


def _make_synthetic_lock_class(member_kind="function"):
    lock = threading.Lock()
    globals_map = {"__builtins__": {}, "held": lock}
    return _synthetic_member_class(globals_map, member_kind)


def _make_synthetic_rlock_class():
    lock = threading.RLock()
    globals_map = {"__builtins__": {}, "held": lock}
    return _synthetic_member_class(globals_map, "function")


def _make_synthetic_lock_in_list_class():
    lock = threading.Lock()
    globals_map = {"__builtins__": {}, "held": [lock]}
    return _synthetic_member_class(globals_map, "function")


def _make_exec_lock_class():
    lock = threading.Lock()
    globals_map = {"__name__": "r24b_glob"}
    exec("def gf():\n    return HELD\n", globals_map)
    globals_map["HELD"] = lock

    class MemberClass:
        pass

    MemberClass.carried = globals_map["gf"]
    return MemberClass


def _make_synthetic_acquire_class():
    lock = threading.Lock()
    globals_map = {"__builtins__": {}, "held": lock.acquire}
    return _synthetic_member_class(globals_map, "function")


def _make_synthetic_plain_class():
    globals_map = {"__builtins__": {}, "held": 7, "name": "plain"}
    return _synthetic_member_class(globals_map, "function")


def _make_synthetic_plain_function_class():
    inner_map = {"__builtins__": {}, "held": 7}
    inner = types.FunctionType(
        _template.__code__, inner_map, "inner"
    )
    globals_map = {"__builtins__": {}, "held": inner}
    return _synthetic_member_class(globals_map, "function")


HOME_HELD_LOCK = threading.Lock()
HOME_PLAIN_CONSTANT = 7


class _HomeReferencedLockClass:
    def method(self):
        return HOME_HELD_LOCK


class _HomeUnreferencedClass:
    def method(self, held=7):
        return held


class _HomePlainReferenceClass:
    def method(self):
        return HOME_PLAIN_CONSTANT


class _PlainMethodClass:
    def method(self, held=7):
        return held


class TestRuling1044GlobalsLimbRefusals(unittest.TestCase):
    """The bare globals value limb of ruling 1044, refused."""

    def test_synthetic_globals_bare_lock_function_member(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24b 1044 synthetic lock class wf",
        )
        cls = _make_synthetic_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls()},
            "r24b 1044 synthetic lock instance wf",
        )

    def test_synthetic_globals_bare_lock_holder_positions(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": Holder(cls)},
            "r24b 1044 synthetic lock holder wf",
        )
        cls = _make_synthetic_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": [cls]},
            "r24b 1044 synthetic lock nested wf",
        )

    def test_exec_globals_referenced_bare_lock(self):
        module = require("ontoloop.consumption")
        cls = _make_exec_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24b 1044 exec lock class wf",
        )
        cls = _make_exec_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls()},
            "r24b 1044 exec lock instance wf",
        )

    def test_property_getter_synthetic_globals_bare_lock(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_lock_class("property")
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24b 1044 property lock class wf",
        )
        cls = _make_synthetic_lock_class("property")
        _assert_uncopyable_refused(
            self, module, {"part": cls()},
            "r24b 1044 property lock instance wf",
        )

    def test_classmethod_carried_synthetic_globals_bare_lock(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_lock_class("classmethod")
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24b 1044 classmethod lock wf",
        )

    def test_staticmethod_carried_synthetic_globals_bare_lock(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_lock_class("staticmethod")
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24b 1044 staticmethod lock wf",
        )

    def test_synthetic_globals_bare_rlock(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_rlock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24b 1044 synthetic rlock wf",
        )

    def test_synthetic_globals_lock_inside_a_list(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_lock_in_list_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24b 1044 synthetic lock in list wf",
        )

    def test_home_globals_referenced_bare_lock(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": _HomeReferencedLockClass},
            "r24b 1044 home referenced class wf",
        )
        _assert_uncopyable_refused(
            self, module, {"part": _HomeReferencedLockClass()},
            "r24b 1044 home referenced instance wf",
        )


class TestRuling1044GlobalsLimbControls(unittest.TestCase):
    """Nearest controls: standing forms that still record."""

    def test_synthetic_globals_plain_values_still_record(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_plain_class()
        recorded = module.record_promotion(
            "r24b 1044 synthetic plain wf", {"part": cls}
        )
        self.assertIs(recorded["bundle"]["part"], cls)

    def test_synthetic_globals_plain_function_still_records(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_plain_function_class()
        recorded = module.record_promotion(
            "r24b 1044 synthetic plain function wf", {"part": cls}
        )
        self.assertIs(recorded["bundle"]["part"], cls)

    def test_home_globals_unreferenced_lock_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r24b 1044 home unreferenced wf",
            {"part": _HomeUnreferencedClass},
        )
        self.assertIs(
            recorded["bundle"]["part"], _HomeUnreferencedClass
        )
        recorded = module.record_promotion(
            "r24b 1044 home unreferenced instance wf",
            {"part": _HomeUnreferencedClass()},
        )
        self.assertIn("part", recorded["bundle"])

    def test_home_globals_plain_reference_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r24b 1044 home plain reference wf",
            {"part": _HomePlainReferenceClass},
        )
        self.assertIs(
            recorded["bundle"]["part"], _HomePlainReferenceClass
        )

    def test_plain_method_class_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r24b 1044 plain method control wf",
            {"part": _PlainMethodClass},
        )
        self.assertIs(recorded["bundle"]["part"], _PlainMethodClass)

    def test_bound_callable_globals_form_still_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_synthetic_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24b 1044 globals acquire control wf",
        )

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(threading.Lock())},
            "r24b 1044 lock control wf",
        )


if __name__ == "__main__":
    unittest.main()
