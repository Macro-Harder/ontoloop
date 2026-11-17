"""Fix round 23 tests for Region 5: the isolation copy act.

Written test first for the positions charged at Round 23
triage rulings 969 to 976: a values view of a globals
mapping standing inside slot storage (ISO-R23-1), inside
function attribute storage (ISO-R23-2), inside the
arguments of a partial (ISO-R23-3), inside a closure cell
(ISO-R23-4), and inside the arguments of an exception
(ISO-R23-5), each in that mapping; a governed uncopyable
value standing inside the reduce reach (ISO-R23-6) and
inside the state reach (ISO-R23-7) of a plain custom
carrier; and a governed uncopyable callable standing in
the namespace of a class standing as a bundle value
(Lead Engineer line E-50). Each refused form stands
pinned at the whole bundle, direct bundle value, holder,
and nested list positions beside the standing controls
its ruling names, unless its ruling names fewer
positions.
"""

import functools
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


def _positions(make):
    obj = make()
    yield "whole", obj
    obj = make()
    yield "direct", {"part": obj}
    obj = make()
    yield "holder", {"part": Holder(obj)}
    obj = make()
    yield "nested", {"part": Holder([obj])}


def _check_positions(case, module, make, label):
    for position, bundle in _positions(make):
        _assert_uncopyable_refused(
            case, module, bundle,
            "r23 " + label + " " + position + " wf",
        )


def _template(value):
    return value


def _synthetic_function(globals_map):
    return types.FunctionType(_template.__code__, globals_map, "synthetic")


class _SlotCarrier:
    __slots__ = ("slot",)

    def __init__(self, value):
        self.slot = value


def _make_slot_view_function():
    globals_map = {"__builtins__": {}}
    globals_map["carrier"] = _SlotCarrier(globals_map.values())
    func = _synthetic_function(globals_map)
    globals_map["func"] = func
    return func


class TestRuling969SlotStorageCarrier(unittest.TestCase):
    """Ruling 969 (ISO-R23-1): view inside slot storage."""

    def test_view_in_slot_storage_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_slot_view_function, "969 slot"
        )

    def test_slot_carrier_with_plain_content_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}, "carrier": _SlotCarrier(42)}
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        recorded = module.record_promotion(
            "r23 969 plain slot control wf", {"part": Holder(func)}
        )
        self.assertIn("part", recorded["bundle"])

    def test_function_over_plain_globals_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}, "held": [1, 2]}
        func = _synthetic_function(globals_map)
        recorded = module.record_promotion(
            "r23 969 plain globals control wf", {"part": Holder(func)}
        )
        self.assertIn("part", recorded["bundle"])


def _plain_carrier_function():
    return 0


def _make_function_attribute_view_function():
    globals_map = {"__builtins__": {}}
    carrier = types.FunctionType(
        _plain_carrier_function.__code__, globals_map, "carrier"
    )
    carrier.held_view = globals_map.values()
    globals_map["carrier"] = carrier
    func = _synthetic_function(globals_map)
    globals_map["func"] = func
    return func


class TestRuling970FunctionAttributeCarrier(unittest.TestCase):
    """Ruling 970 (ISO-R23-2): view inside function attributes."""

    def test_view_in_function_attribute_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_function_attribute_view_function,
            "970 funcattr",
        )

    def test_function_with_plain_attribute_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}}
        carrier = types.FunctionType(
            _plain_carrier_function.__code__, globals_map, "carrier"
        )
        carrier.held_view = 42
        globals_map["carrier"] = carrier
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        recorded = module.record_promotion(
            "r23 970 plain attribute control wf", {"part": Holder(func)}
        )
        self.assertIn("part", recorded["bundle"])


def _partial_target(value):
    return value


def _make_partial_view_function():
    globals_map = {"__builtins__": {}}
    globals_map["part"] = functools.partial(
        _partial_target, globals_map.values()
    )
    func = _synthetic_function(globals_map)
    globals_map["func"] = func
    return func


class TestRuling971PartialArgumentCarrier(unittest.TestCase):
    """Ruling 971 (ISO-R23-3): view inside partial arguments."""

    def test_view_in_partial_arguments_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_partial_view_function, "971 partial"
        )

    def test_partial_with_plain_argument_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {
            "__builtins__": {},
            "part": functools.partial(_partial_target, 42),
        }
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        recorded = module.record_promotion(
            "r23 971 plain partial control wf", {"part": Holder(func)}
        )
        self.assertIn("part", recorded["bundle"])


def _make_closure_view_function():
    globals_map = {"__builtins__": {}}
    view = globals_map.values()

    def maker():
        held = view

        def inner():
            return held

        return inner

    globals_map["maker"] = maker()
    func = _synthetic_function(globals_map)
    globals_map["func"] = func
    return func


class TestRuling972ClosureCellCarrier(unittest.TestCase):
    """Ruling 972 (ISO-R23-4): view inside a closure cell."""

    def test_view_in_closure_cell_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_closure_view_function, "972 closure"
        )

    def test_closure_with_plain_content_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}}

        def maker():
            held = 42

            def inner():
                return held

            return inner

        globals_map["maker"] = maker()
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        recorded = module.record_promotion(
            "r23 972 plain closure control wf", {"part": Holder(func)}
        )
        self.assertIn("part", recorded["bundle"])


def _make_exception_view_function():
    globals_map = {"__builtins__": {}}
    globals_map["error"] = ValueError(globals_map.values())
    func = _synthetic_function(globals_map)
    globals_map["func"] = func
    return func


class TestRuling973ExceptionArgumentCarrier(unittest.TestCase):
    """Ruling 973 (ISO-R23-5): view inside exception arguments."""

    def test_view_in_exception_arguments_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_exception_view_function, "973 exc"
        )

    def test_exception_with_plain_argument_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}, "error": ValueError(42)}
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        recorded = module.record_promotion(
            "r23 973 plain exception control wf", {"part": Holder(func)}
        )
        self.assertIn("part", recorded["bundle"])


def _rebuild_from_reduce(value):
    return ("rebuilt", value)


class _ReducePlainCarrier:
    __slots__ = ()

    def __reduce_ex__(self, protocol):
        return (_rebuild_from_reduce, (7,))


def _make_reduce_lock_carrier():
    lock = threading.Lock()

    class ReduceLockCarrier:
        __slots__ = ()

        def __reduce_ex__(self, protocol):
            return (_rebuild_from_reduce, (lock,))

    return ReduceLockCarrier()


class TestRuling974ReduceReachCarrier(unittest.TestCase):
    """Ruling 974 (ISO-R23-6): uncopyable in the reduce reach."""

    def test_lock_in_reduce_reach_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_reduce_lock_carrier, "974 reduce"
        )

    def test_reduce_with_plain_content_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _ReducePlainCarrier()
        recorded = module.record_promotion(
            "r23 974 plain reduce control wf", {"part": Holder(carrier)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, carrier)
        self.assertEqual(copied, ("rebuilt", 7))

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(threading.Lock())},
            "r23 974 lock control wf",
        )


class _StatePlainCarrier:
    __slots__ = ("state",)

    def __getstate__(self):
        return {"v": [1, 2]}

    def __setstate__(self, state):
        self.state = state["v"]


def _make_state_lock_carrier():
    lock = threading.Lock()

    class StateLockCarrier:
        __slots__ = ()

        def __getstate__(self):
            return {"lock": lock}

        def __setstate__(self, state):
            pass

    return StateLockCarrier()


def _make_state_holder_lock_carrier():
    lock = threading.Lock()

    class StateHolderLockCarrier:
        __slots__ = ()

        def __getstate__(self):
            return {"holder": Holder(lock)}

        def __setstate__(self, state):
            pass

    return StateHolderLockCarrier()


class TestRuling975StateReachCarrier(unittest.TestCase):
    """Ruling 975 (ISO-R23-7): uncopyable in the state reach."""

    def test_lock_in_state_reach_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_state_lock_carrier, "975 state"
        )

    def test_holder_with_lock_in_state_reach_is_refused(self):
        module = require("ontoloop.consumption")
        carrier = _make_state_holder_lock_carrier()
        _assert_uncopyable_refused(
            self, module, {"part": carrier},
            "r23 975 state holder wf",
        )

    def test_getstate_with_plain_content_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _StatePlainCarrier()
        recorded = module.record_promotion(
            "r23 975 plain state control wf", {"part": Holder(carrier)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, carrier)
        self.assertEqual(copied.state, [1, 2])

    def test_lock_in_dict_of_plain_object_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(threading.Lock())},
            "r23 975 lock control wf",
        )


def _make_acquire_class():
    lock = threading.Lock()

    class AcquireClass:
        acquire = lock.acquire
        name = "plain"

    return AcquireClass


def _make_lock_class():
    lock = threading.Lock()

    class LockClass:
        held = lock
        name = "plain"

    return LockClass


class _PlainClass:
    name = "plain"


class TestRuling976ClassNamespaceCarrier(unittest.TestCase):
    """Ruling 976 (E-50): uncopyable callable in a class namespace."""

    def test_acquire_in_class_namespace_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_acquire_class, "976 acquire class"
        )

    def test_lock_in_class_namespace_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": _make_lock_class()},
            "r23 976 lock class direct wf",
        )
        _assert_uncopyable_refused(
            self, module, _make_lock_class(),
            "r23 976 lock class whole wf",
        )

    def test_instance_of_acquire_class_is_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": _make_acquire_class()()},
            "r23 976 instance direct wf",
        )
        _assert_uncopyable_refused(
            self, module, {"part": Holder(_make_acquire_class()())},
            "r23 976 instance holder wf",
        )

    def test_direct_acquire_value_still_refused(self):
        module = require("ontoloop.consumption")
        lock = threading.Lock()
        _assert_uncopyable_refused(
            self, module, {"part": lock.acquire},
            "r23 976 direct acquire wf",
        )
        self.assertFalse(lock.locked())

    def test_plain_class_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r23 976 plain class control wf", {"part": _PlainClass}
        )
        self.assertIs(recorded["bundle"]["part"], _PlainClass)


if __name__ == "__main__":
    unittest.main()
