"""Fix round 22 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 22 triage
rulings 918, 919, and 920: a bound builtin method of a governed
uncopyable object standing as a bundle value in its own right
(ruling 918, Consume Finding 8), a governed uncopyable callable
standing wrapped in a functools.partial (ruling 919, ISO-R22-1),
and a values view of a globals mapping standing inside object
attribute storage in that mapping (ruling 920, ISO-R22-2). Each
refused form stands pinned at the whole bundle, direct bundle
value, holder, and nested list positions beside the standing
controls its ruling names, unless its ruling names the direct
bundle value position alone.
"""

import functools
import itertools
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
    obj, cleanup = make()
    yield "whole", obj, cleanup
    obj, cleanup = make()
    yield "direct", {"part": obj}, cleanup
    obj, cleanup = make()
    yield "holder", {"part": Holder(obj)}, cleanup
    obj, cleanup = make()
    yield "nested", {"part": Holder([obj])}, cleanup


def _check_positions(case, module, make, label):
    for position, bundle, cleanup in _positions(make):
        try:
            _assert_uncopyable_refused(
                case, module, bundle,
                "r22 " + label + " " + position + " wf",
            )
        finally:
            if cleanup is not None:
                cleanup()


def _lock():
    return threading.Lock()


def _make_lock_acquire():
    lock = _lock()
    return lock.acquire, None


class _PlainLockHolder:
    """A plain object carrying a lock, with a Python method."""

    def __init__(self):
        self.lock = _lock()

    def fetch(self):
        return self.lock


def _plain_function(value):
    return value + 1


def _plain_callable():
    return 42


class TestRuling918BoundBuiltinMethod(unittest.TestCase):
    """Ruling 918 (Consume Finding 8): bound builtin method."""

    def test_lock_acquire_value_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_lock_acquire, "918 acquire"
        )

    def test_lock_acquire_in_list_tuple_and_mapping_is_refused(self):
        module = require("ontoloop.consumption")
        lock = _lock()
        _assert_uncopyable_refused(
            self, module, {"part": [lock.acquire]},
            "r22 918 list wf",
        )
        lock = _lock()
        _assert_uncopyable_refused(
            self, module, {"part": (lock.acquire,)},
            "r22 918 tuple wf",
        )
        lock = _lock()
        _assert_uncopyable_refused(
            self, module, {"part": {"inner": lock.acquire}},
            "r22 918 mapping value wf",
        )

    def test_lock_acquire_inside_cycle_is_refused(self):
        module = require("ontoloop.consumption")
        lock = _lock()
        _assert_uncopyable_refused(
            self, module,
            {"part": itertools.cycle([lock.acquire])},
            "r22 918 cycle wf",
        )

    def test_python_bound_method_of_lock_holder_still_refused(self):
        module = require("ontoloop.consumption")
        holder = _PlainLockHolder()
        _assert_uncopyable_refused(
            self, module, {"part": Holder(holder.fetch)},
            "r22 918 methodtype control wf",
        )

    def test_plain_content_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r22 918 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(_lock())},
            "r22 918 lock control wf",
        )

    def test_builtin_method_bound_to_plain_list_still_records(self):
        module = require("ontoloop.consumption")
        caller = [1, 2]
        recorded = module.record_promotion(
            "r22 918 plain append control wf",
            {"part": caller.append},
        )
        self.assertTrue(callable(recorded["bundle"]["part"]))

    def test_plain_builtin_function_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r22 918 len control wf", {"part": len}
        )
        self.assertIs(recorded["bundle"]["part"], len)


def _make_partial_lock_acquire():
    lock = _lock()
    return functools.partial(lock.acquire), None


def _make_map_partial_lock_acquire():
    lock = _lock()
    return map(functools.partial(lock.acquire), [1]), None


def _make_filter_partial_lock_acquire():
    lock = _lock()
    return filter(functools.partial(lock.acquire), [1]), None


class TestRuling919PartialWrappedCallable(unittest.TestCase):
    """Ruling 919 (ISO-R22-1): partial wrapped uncopyable callable."""

    def test_partial_over_lock_acquire_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_partial_lock_acquire, "919 partial"
        )

    def test_map_over_partial_lock_acquire_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_map_partial_lock_acquire, "919 map"
        )

    def test_filter_over_partial_lock_acquire_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_filter_partial_lock_acquire,
            "919 filter",
        )

    def test_wider_carriers_over_partial_at_direct_are_refused(self):
        module = require("ontoloop.consumption")
        makers = [
            ("calliter", lambda lock: iter(
                functools.partial(lock.acquire), None
            )),
            ("takewhile", lambda lock: itertools.takewhile(
                functools.partial(lock.acquire), [1]
            )),
            ("dropwhile", lambda lock: itertools.dropwhile(
                functools.partial(lock.acquire), [1]
            )),
            ("filterfalse", lambda lock: itertools.filterfalse(
                functools.partial(lock.acquire), [1]
            )),
            ("starmap", lambda lock: itertools.starmap(
                functools.partial(lock.acquire), [()]
            )),
            ("groupby", lambda lock: itertools.groupby(
                [1], key=functools.partial(lock.acquire)
            )),
            ("accumulate", lambda lock: itertools.accumulate(
                [1, 2], functools.partial(lock.acquire)
            )),
        ]
        for label, make in makers:
            lock = _lock()
            _assert_uncopyable_refused(
                self, module, {"part": make(lock)},
                "r22 919 " + label + " wf",
            )

    def test_refusal_exercises_no_callable(self):
        module = require("ontoloop.consumption")
        lock = _lock()
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(functools.partial(lock.acquire))},
            "r22 919 no exercise partial wf",
        )
        self.assertFalse(lock.locked())
        lock = _lock()
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(map(
                functools.partial(lock.acquire), [1]
            ))},
            "r22 919 no exercise map wf",
        )
        self.assertFalse(lock.locked())

    def test_partial_over_plain_function_still_records(self):
        module = require("ontoloop.consumption")
        original = functools.partial(_plain_function, 1)
        recorded = module.record_promotion(
            "r22 919 plain partial control wf",
            {"part": Holder(original)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertEqual(copied(), 2)

    def test_partial_carrying_lock_as_argument_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": functools.partial(_plain_function, _lock())},
            "r22 919 partial argument control wf",
        )

    def test_partial_carrying_lock_as_keyword_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": functools.partial(
                _plain_function, value=_lock()
            )},
            "r22 919 partial keyword control wf",
        )

    def test_callable_iterator_plain_function_still_records(self):
        module = require("ontoloop.consumption")
        caller = iter(_plain_callable, 999)
        recorded = module.record_promotion(
            "r22 919 plain calliter control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(next(copied), 42)

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(_lock())},
            "r22 919 lock control wf",
        )


def _template(value):
    return value


def _synthetic_function(globals_map):
    return types.FunctionType(
        _template.__code__, globals_map, "synthetic"
    )


class _AttributeHolder:
    """A plain custom instance carrying values in its attributes."""


def _make_view_function(storage_kind):
    def make():
        globals_map = {"__builtins__": {}}
        view = globals_map.values()
        if storage_kind == "namespace":
            globals_map["held"] = types.SimpleNamespace(held=view)
        elif storage_kind == "instance":
            holder = _AttributeHolder()
            holder.held = view
            globals_map["held"] = holder
        elif storage_kind == "instance_mapping":
            holder = _AttributeHolder()
            holder.held = {"inner": view}
            globals_map["held"] = holder
        else:
            globals_map["held"] = types.SimpleNamespace(
                held=[view]
            )
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        return func, None

    return make


class TestRuling920GlobalsViewInAttributeStorage(unittest.TestCase):
    """Ruling 920 (ISO-R22-2): self view in attribute storage."""

    def test_view_inside_namespace_in_globals_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            _make_view_function("namespace"), "920 namespace",
        )

    def test_view_inside_instance_in_globals_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            _make_view_function("instance"), "920 instance",
        )

    def test_view_inside_mapping_inside_instance_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            _make_view_function("instance_mapping"),
            "920 instance mapping",
        )

    def test_view_inside_list_inside_namespace_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            _make_view_function("namespace_list"),
            "920 namespace list",
        )

    def test_function_over_plain_globals_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}, "held": [1, 2]}
        func = _synthetic_function(globals_map)
        recorded = module.record_promotion(
            "r22 920 plain globals control wf",
            {"part": Holder(func)},
        )
        self.assertIn("part", recorded["bundle"])

    def test_view_inside_list_in_globals_still_refused(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}}
        globals_map["held"] = [globals_map.values()]
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r22 920 ruling 862 control wf",
        )

    def test_direct_self_view_still_refused(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}}
        globals_map["view"] = globals_map.values()
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r22 920 ruling 798 control wf",
        )

    def test_ruling_622_view_of_another_mapping_still_records(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        shared = {"__builtins__": {}, "held": source.values()}
        first = _synthetic_function(shared)
        second = _synthetic_function(shared)
        recorded = module.record_promotion(
            "r22 920 ruling 622 control wf",
            {"first": first, "second": second},
        )
        bundle = recorded["bundle"]
        self.assertIs(
            bundle["first"].__globals__,
            bundle["second"].__globals__,
        )
        self.assertIsNot(bundle["first"].__globals__, shared)
        self.assertEqual(
            bundle["first"].__globals__["held"], [[1]]
        )

    def test_class_and_instance_in_globals_still_record(self):
        module = require("ontoloop.consumption")
        holder = _AttributeHolder()
        holder.held = [1, 2]
        globals_map = {
            "__builtins__": {},
            "held_class": _AttributeHolder,
            "held_instance": holder,
        }
        func = _synthetic_function(globals_map)
        recorded = module.record_promotion(
            "r22 920 class instance control wf",
            {"part": Holder(func)},
        )
        self.assertIn("part", recorded["bundle"])


if __name__ == "__main__":
    unittest.main()
