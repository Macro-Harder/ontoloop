"""Fix round 24 tests for Region 5: the isolation copy act.

Written test first for the positions charged at Round 24
triage rulings 1033 to 1046: a values view of a globals
mapping standing inside the instance attribute storage of
branch matched carriers in that mapping (Consume position
S15-R24-CONSUME-1 and Isolation positions ISO-R24-1 to
ISO-R24-3); a governed uncopyable value standing in the
state element of a reduce form (S15-R24-CONSUME-2 and
ISO-R24-6); a dictionary view standing inside the reduce
arguments of a plain custom carrier (ISO-R24-7) and inside
the state a custom getstate act returns (ISO-R24-8); a
governed uncopyable value and a dictionary view standing
inside the newargs reach (ISO-R24-4) and inside the
newargs ex reach (ISO-R24-5) of a plain custom carrier; a
governed uncopyable value held by a defaultdict factory
at a fallback position (S15-R24-CONSUME-3); a governed
uncopyable value standing inside a function member of the
namespace of a class standing as a bundle value, beside
the Lead Engineer held forms of the skipped members and
the plain function member meeting (ISO-R24-9, lines E-52
and E-53); a governed uncopyable value standing inside
the namespace of a class standing nested in a class
namespace (ISO-R24-10); and a governed uncopyable
callable standing in the namespace of the metaclass of a
class standing as a bundle value (line E-51). Each
refused form stands pinned beside the standing controls
its ruling names, at the positions its papers name.
"""

import collections
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
            "r24 " + label + " " + position + " wf",
        )


def _template(value):
    return value


def _synthetic_function(globals_map):
    return types.FunctionType(
        _template.__code__, globals_map, "synthetic"
    )


def _globals_function_with_carrier(carrier):
    globals_map = {"__builtins__": {}}
    globals_map["carrier"] = carrier
    func = _synthetic_function(globals_map)
    globals_map["func"] = func
    return func


def _view_carrier_function(make_carrier):
    globals_map = {"__builtins__": {}}
    view = globals_map.values()
    globals_map["carrier"] = make_carrier(view)
    func = _synthetic_function(globals_map)
    globals_map["func"] = func
    return func


def _dict_subclass_with_view(view):
    class DictSub(dict):
        pass

    inst = DictSub()
    inst.held_view = view
    return inst


def _list_subclass_with_view(view):
    class ListSub(list):
        pass

    inst = ListSub()
    inst.held_view = view
    return inst


def _tuple_subclass_with_view(view):
    class TupleSub(tuple):
        pass

    inst = TupleSub()
    inst.held_view = view
    return inst


def _set_subclass_with_view(view):
    class SetSub(set):
        pass

    inst = SetSub()
    inst.held_view = view
    return inst


def _frozenset_subclass_with_view(view):
    class FrozenSub(frozenset):
        pass

    inst = FrozenSub()
    inst.held_view = view
    return inst


def _deque_subclass_with_view(view):
    class DequeSub(collections.deque):
        pass

    inst = DequeSub()
    inst.held_view = view
    return inst


def _userdict_with_view(view):
    inst = collections.UserDict()
    inst.held_view = view
    return inst


def _userlist_with_view(view):
    inst = collections.UserList()
    inst.held_view = view
    return inst


def _chainmap_with_view(view):
    inst = collections.ChainMap({})
    inst.held_view = view
    return inst


def _exception_with_view(view):
    inst = ValueError("plain")
    inst.held_view = view
    return inst


def _exception_notes_with_view(view):
    inst = ValueError("plain")
    inst.add_note("a note")
    inst.__notes__ = [view]
    return inst


def _partial_target(value):
    return value


def _partial_with_view(view):
    inst = functools.partial(_partial_target, 1)
    inst.held_view = view
    return inst


class TestRuling1033BranchMatchedCarriers(unittest.TestCase):
    """Ruling 1033 (S15-R24-CONSUME-1): branch matched carriers."""

    def test_exception_attribute_view_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            lambda: _view_carrier_function(_exception_with_view),
            "1033 exception",
        )

    def test_remaining_consume_carriers_refused_at_holder(self):
        module = require("ontoloop.consumption")
        makers = (
            _tuple_subclass_with_view,
            _set_subclass_with_view,
            _deque_subclass_with_view,
            _userlist_with_view,
            _chainmap_with_view,
        )
        for index, maker in enumerate(makers):
            func = _view_carrier_function(maker)
            _assert_uncopyable_refused(
                self, module, {"part": Holder(func)},
                "r24 1033 carrier " + str(index) + " wf",
            )

    def test_exception_with_plain_attribute_still_records(self):
        module = require("ontoloop.consumption")
        carrier = ValueError("plain")
        carrier.held_view = 42
        func = _globals_function_with_carrier(carrier)
        recorded = module.record_promotion(
            "r24 1033 plain exception control wf",
            {"part": Holder(func)},
        )
        self.assertIn("part", recorded["bundle"])


class TestRuling1034ContainerAttributeStorage(unittest.TestCase):
    """Ruling 1034 (ISO-R24-1): container instance attribute storage."""

    def test_dict_subclass_view_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            lambda: _view_carrier_function(_dict_subclass_with_view),
            "1034 dict",
        )

    def test_list_subclass_view_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            lambda: _view_carrier_function(_list_subclass_with_view),
            "1034 list",
        )

    def test_other_containers_view_refused_at_direct(self):
        module = require("ontoloop.consumption")
        makers = (
            _tuple_subclass_with_view,
            _set_subclass_with_view,
            _frozenset_subclass_with_view,
            _deque_subclass_with_view,
            _userdict_with_view,
            _userlist_with_view,
            _chainmap_with_view,
        )
        for index, maker in enumerate(makers):
            func = _view_carrier_function(maker)
            _assert_uncopyable_refused(
                self, module, {"part": func},
                "r24 1034 container " + str(index) + " wf",
            )

    def test_container_with_plain_attribute_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _dict_subclass_with_view(42)
        func = _globals_function_with_carrier(carrier)
        recorded = module.record_promotion(
            "r24 1034 plain container control wf",
            {"part": Holder(func)},
        )
        self.assertIn("part", recorded["bundle"])


class TestRuling1035ExceptionAttributeStorage(unittest.TestCase):
    """Ruling 1035 (ISO-R24-2): exception attribute storage."""

    def test_exception_attribute_view_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            lambda: _view_carrier_function(_exception_with_view),
            "1035 exception",
        )

    def test_exception_notes_view_refused_at_direct(self):
        module = require("ontoloop.consumption")
        func = _view_carrier_function(_exception_notes_with_view)
        _assert_uncopyable_refused(
            self, module, {"part": func},
            "r24 1035 notes wf",
        )

    def test_exception_with_plain_attribute_still_records(self):
        module = require("ontoloop.consumption")
        carrier = ValueError("plain")
        carrier.held_view = 42
        func = _globals_function_with_carrier(carrier)
        recorded = module.record_promotion(
            "r24 1035 plain exception control wf",
            {"part": Holder(func)},
        )
        self.assertIn("part", recorded["bundle"])


class TestRuling1036PartialAttributeStorage(unittest.TestCase):
    """Ruling 1036 (ISO-R24-3): partial attribute storage."""

    def test_partial_attribute_view_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            lambda: _view_carrier_function(_partial_with_view),
            "1036 partial",
        )

    def test_partial_with_plain_attribute_still_records(self):
        module = require("ontoloop.consumption")
        carrier = functools.partial(_partial_target, 1)
        carrier.held_view = 42
        func = _globals_function_with_carrier(carrier)
        recorded = module.record_promotion(
            "r24 1036 plain partial control wf",
            {"part": Holder(func)},
        )
        self.assertIn("part", recorded["bundle"])


def _rebuild_from_reduce(value):
    return ("rebuilt", value)


def _blank_instance(cls):
    return object.__new__(cls)


def _make_reduce_state_lock_carrier():
    lock = threading.Lock()

    class ReduceStateCarrier:
        __slots__ = ("state",)

        def __reduce_ex__(self, protocol):
            return (
                _blank_instance, (ReduceStateCarrier,),
                {"held": lock},
            )

        def __setstate__(self, state):
            self.state = state

    return ReduceStateCarrier()


def _make_reduce_state_lock_carrier_dict_form():
    lock = threading.Lock()

    class ReduceStateDictCarrier:
        def __reduce_ex__(self, protocol):
            return (
                _blank_instance, (ReduceStateDictCarrier,),
                {"held": lock},
            )

        def __setstate__(self, state):
            self.state = state

    return ReduceStateDictCarrier()


def _make_reduce_state_view_carrier():
    plain = {"a": 1}

    class ReduceStateViewCarrier:
        __slots__ = ("state",)

        def __reduce_ex__(self, protocol):
            return (
                _blank_instance, (ReduceStateViewCarrier,),
                {"held": plain.values()},
            )

        def __setstate__(self, state):
            self.state = state

    return ReduceStateViewCarrier()


class _ReduceStatePlainCarrier:
    __slots__ = ("state",)

    def __reduce_ex__(self, protocol):
        return (
            _blank_instance, (_ReduceStatePlainCarrier,),
            {"v": [1, 2]},
        )

    def __setstate__(self, state):
        self.state = state["v"]


def _make_consume_reduce_state_lock_carrier():
    lock = threading.Lock()

    class ConsumeReduceCarrier:
        def __reduce__(self):
            return (ConsumeReduceCarrier, (), {"held": lock})

    return ConsumeReduceCarrier()


class TestRuling1037ConsumeReduceState(unittest.TestCase):
    """Ruling 1037 (S15-R24-CONSUME-2): reduce state element."""

    def test_lock_in_reduce_state_refused_at_holder_and_nested(self):
        module = require("ontoloop.consumption")
        carrier = _make_consume_reduce_state_lock_carrier()
        _assert_uncopyable_refused(
            self, module, {"part": Holder(carrier)},
            "r24 1037 holder wf",
        )
        carrier = _make_consume_reduce_state_lock_carrier()
        _assert_uncopyable_refused(
            self, module, {"part": Holder([carrier])},
            "r24 1037 nested wf",
        )

    def test_plain_reduce_state_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _ReduceStatePlainCarrier()
        recorded = module.record_promotion(
            "r24 1037 plain state control wf",
            {"part": Holder(carrier)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, carrier)


class TestRuling1038ReduceStateElement(unittest.TestCase):
    """Ruling 1038 (ISO-R24-6): state element of the reduce tuple."""

    def test_lock_in_reduce_state_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_reduce_state_lock_carrier,
            "1038 state lock",
        )

    def test_lock_in_reduce_state_dict_form_refused_at_direct(self):
        module = require("ontoloop.consumption")
        carrier = _make_reduce_state_lock_carrier_dict_form()
        _assert_uncopyable_refused(
            self, module, {"part": carrier},
            "r24 1038 dict form wf",
        )

    def test_view_in_reduce_state_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_reduce_state_view_carrier,
            "1038 state view",
        )

    def test_plain_reduce_state_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _ReduceStatePlainCarrier()
        recorded = module.record_promotion(
            "r24 1038 plain state control wf",
            {"part": Holder(carrier)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, carrier)
        self.assertEqual(copied.state, [1, 2])


def _make_reduce_args_view_carrier():
    plain = {"a": 1}

    class ReduceArgsViewCarrier:
        __slots__ = ()

        def __reduce_ex__(self, protocol):
            return (_rebuild_from_reduce, (plain.values(),))

    return ReduceArgsViewCarrier()


def _make_reduce_args_lock_carrier():
    lock = threading.Lock()

    class ReduceArgsLockCarrier:
        __slots__ = ()

        def __reduce_ex__(self, protocol):
            return (_rebuild_from_reduce, (lock,))

    return ReduceArgsLockCarrier()


class _ReducePlainCarrier:
    __slots__ = ()

    def __reduce_ex__(self, protocol):
        return (_rebuild_from_reduce, (7,))


class TestRuling1039ReduceArgumentsView(unittest.TestCase):
    """Ruling 1039 (ISO-R24-7): view in the reduce arguments."""

    def test_view_in_reduce_arguments_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_reduce_args_view_carrier,
            "1039 args view",
        )

    def test_lock_in_reduce_arguments_still_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_reduce_args_lock_carrier,
            "1039 args lock control",
        )

    def test_plain_reduce_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _ReducePlainCarrier()
        recorded = module.record_promotion(
            "r24 1039 plain reduce control wf",
            {"part": Holder(carrier)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, carrier)
        self.assertEqual(copied, ("rebuilt", 7))


def _make_getstate_view_carrier():
    plain = {"a": 1}

    class GetstateViewCarrier:
        __slots__ = ("state",)

        def __getstate__(self):
            return {"held": plain.values()}

        def __setstate__(self, state):
            self.state = state

    return GetstateViewCarrier()


def _make_getstate_lock_carrier():
    lock = threading.Lock()

    class GetstateLockCarrier:
        __slots__ = ()

        def __getstate__(self):
            return {"held": lock}

        def __setstate__(self, state):
            pass

    return GetstateLockCarrier()


class _GetstatePlainCarrier:
    __slots__ = ("state",)

    def __getstate__(self):
        return {"v": [1, 2]}

    def __setstate__(self, state):
        self.state = state["v"]


class TestRuling1040GetstateStateView(unittest.TestCase):
    """Ruling 1040 (ISO-R24-8): view in the getstate state."""

    def test_view_in_getstate_state_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_getstate_view_carrier,
            "1040 state view",
        )

    def test_lock_in_getstate_state_still_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_getstate_lock_carrier,
            "1040 state lock control",
        )

    def test_plain_getstate_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _GetstatePlainCarrier()
        recorded = module.record_promotion(
            "r24 1040 plain state control wf",
            {"part": Holder(carrier)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, carrier)
        self.assertEqual(copied.state, [1, 2])


def _make_newargs_lock_carrier():
    lock = threading.Lock()

    class NewargsLockCarrier:
        __slots__ = ()

        def __init__(self, *args, **kwargs):
            pass

        def __getnewargs__(self):
            return (lock,)

    return NewargsLockCarrier()


def _make_newargs_view_carrier():
    plain = {"a": 1}

    class NewargsViewCarrier:
        __slots__ = ()

        def __init__(self, *args, **kwargs):
            pass

        def __getnewargs__(self):
            return (plain.values(),)

    return NewargsViewCarrier()


class _NewargsPlainCarrier:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    def __getnewargs__(self):
        return (7,)


class TestRuling1041NewargsReach(unittest.TestCase):
    """Ruling 1041 (ISO-R24-4): the newargs reach."""

    def test_lock_in_newargs_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_newargs_lock_carrier,
            "1041 newargs lock",
        )

    def test_view_in_newargs_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_newargs_view_carrier,
            "1041 newargs view",
        )

    def test_plain_newargs_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _NewargsPlainCarrier()
        recorded = module.record_promotion(
            "r24 1041 plain newargs control wf",
            {"part": Holder(carrier)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, carrier)


def _make_newargs_ex_kwargs_lock_carrier():
    lock = threading.Lock()

    class NewargsExCarrier:
        __slots__ = ()

        def __init__(self, *args, **kwargs):
            pass

        def __getnewargs_ex__(self):
            return ((), {"held": lock})

    return NewargsExCarrier()


def _make_newargs_ex_args_lock_carrier():
    lock = threading.Lock()

    class NewargsExArgsCarrier:
        __slots__ = ()

        def __init__(self, *args, **kwargs):
            pass

        def __getnewargs_ex__(self):
            return ((lock,), {})

    return NewargsExArgsCarrier()


class _NewargsExPlainCarrier:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    def __getnewargs_ex__(self):
        return ((7,), {"k": 8})


class TestRuling1042NewargsExReach(unittest.TestCase):
    """Ruling 1042 (ISO-R24-5): the newargs ex reach."""

    def test_lock_in_newargs_ex_kwargs_refused_all_positions(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_newargs_ex_kwargs_lock_carrier,
            "1042 newargs ex kwargs",
        )

    def test_lock_in_newargs_ex_args_refused_at_direct(self):
        module = require("ontoloop.consumption")
        carrier = _make_newargs_ex_args_lock_carrier()
        _assert_uncopyable_refused(
            self, module, {"part": carrier},
            "r24 1042 newargs ex args wf",
        )

    def test_plain_newargs_ex_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _NewargsExPlainCarrier()
        recorded = module.record_promotion(
            "r24 1042 plain newargs ex control wf",
            {"part": Holder(carrier)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, carrier)


class _LockFactory:
    def __init__(self, lock):
        self.lock = lock

    def __call__(self):
        return 0


class _PlainFactory:
    def __call__(self):
        return 0


def _make_fallback_defaultdict():
    lock = threading.Lock()
    return collections.defaultdict(_LockFactory(lock))


class TestRuling1043DefaultdictFactory(unittest.TestCase):
    """Ruling 1043 (S15-R24-CONSUME-3): defaultdict factory."""

    def test_factory_lock_refused_at_holder_and_nested(self):
        module = require("ontoloop.consumption")
        dd = _make_fallback_defaultdict()
        _assert_uncopyable_refused(
            self, module, {"part": Holder(dd)},
            "r24 1043 holder wf",
        )
        dd = _make_fallback_defaultdict()
        _assert_uncopyable_refused(
            self, module, {"part": Holder([dd])},
            "r24 1043 nested wf",
        )

    def test_same_defaultdict_at_walked_position_still_records(self):
        module = require("ontoloop.consumption")
        dd = _make_fallback_defaultdict()
        recorded = module.record_promotion(
            "r24 1043 walked control wf", {"part": dd}
        )
        self.assertIn("part", recorded["bundle"])

    def test_plain_factory_defaultdict_in_holder_still_records(self):
        module = require("ontoloop.consumption")
        dd = collections.defaultdict(_PlainFactory())
        recorded = module.record_promotion(
            "r24 1043 plain factory control wf",
            {"part": Holder(dd)},
        )
        self.assertIn("part", recorded["bundle"])


def _make_method_default_lock_class():
    lock = threading.Lock()

    class MethodDefaultClass:
        def method(self, held=lock):
            return held

    return MethodDefaultClass


def _make_property_default_lock_class():
    lock = threading.Lock()

    class PropertyDefaultClass:
        def getter(self, held=lock):
            return held

        prop = property(getter)

    return PropertyDefaultClass


def _make_classmethod_default_lock_class():
    lock = threading.Lock()

    class ClassmethodDefaultClass:
        def carried(cls, held=lock):
            return held

        cm = classmethod(carried)

    return ClassmethodDefaultClass


def _make_staticmethod_closure_lock_class():
    lock = threading.Lock()

    def maker():
        held = lock

        def carried():
            return held

        return carried

    class StaticmethodClosureClass:
        sm = staticmethod(maker())

    return StaticmethodClosureClass


def _make_property_acquire_class():
    lock = threading.Lock()

    class PropertyAcquireClass:
        pass

    PropertyAcquireClass.prop = property(lock.acquire)
    return PropertyAcquireClass


def _make_classmethod_acquire_class():
    lock = threading.Lock()

    class ClassmethodAcquireClass:
        pass

    ClassmethodAcquireClass.cm = classmethod(lock.acquire)
    return ClassmethodAcquireClass


def _make_staticmethod_acquire_class():
    lock = threading.Lock()

    class StaticmethodAcquireClass:
        pass

    StaticmethodAcquireClass.sm = staticmethod(lock.acquire)
    return StaticmethodAcquireClass


def _make_function_closure_acquire_class():
    lock = threading.Lock()
    acquire = lock.acquire

    def maker():
        held = acquire

        def carried():
            return held

        return carried

    class FunctionClosureClass:
        pass

    FunctionClosureClass.carried = maker()
    return FunctionClosureClass


def _make_function_globals_acquire_class():
    lock = threading.Lock()
    globals_map = {"__builtins__": {}, "held": lock.acquire}
    carried = types.FunctionType(
        _template.__code__, globals_map, "carried"
    )

    class FunctionGlobalsClass:
        pass

    FunctionGlobalsClass.carried = carried
    return FunctionGlobalsClass


class _PlainMethodClass:
    def method(self, held=7):
        return held


class TestRuling1044FunctionMembers(unittest.TestCase):
    """Ruling 1044 (ISO-R24-9, E-52, E-53): function members."""

    def test_method_default_lock_refused_class_and_instance(self):
        module = require("ontoloop.consumption")
        cls = _make_method_default_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls}, "r24 1044 method class wf"
        )
        cls = _make_method_default_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls()},
            "r24 1044 method instance wf",
        )

    def test_property_getter_default_lock_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_property_default_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1044 property class wf",
        )
        cls = _make_property_default_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls()},
            "r24 1044 property instance wf",
        )

    def test_classmethod_carried_default_lock_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_classmethod_default_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1044 classmethod wf",
        )

    def test_staticmethod_carried_closure_lock_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_staticmethod_closure_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1044 staticmethod wf",
        )

    def test_property_accessor_itself_acquire_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_property_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1044 property acquire class wf",
        )
        cls = _make_property_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls()},
            "r24 1044 property acquire instance wf",
        )

    def test_classmethod_carried_itself_acquire_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_classmethod_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1044 classmethod acquire wf",
        )

    def test_staticmethod_carried_itself_acquire_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_staticmethod_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1044 staticmethod acquire wf",
        )

    def test_function_member_closure_acquire_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_function_closure_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1044 function closure wf",
        )

    def test_function_member_globals_acquire_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_function_globals_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1044 function globals wf",
        )

    def test_plain_method_class_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r24 1044 plain method control wf",
            {"part": _PlainMethodClass},
        )
        self.assertIs(recorded["bundle"]["part"], _PlainMethodClass)
        recorded = module.record_promotion(
            "r24 1044 plain method instance control wf",
            {"part": _PlainMethodClass()},
        )
        self.assertIn("part", recorded["bundle"])


def _make_nested_lock_class():
    lock = threading.Lock()

    class Inner:
        held = lock

    class Outer:
        inner = Inner

    return Outer


def _make_deep_nested_lock_class():
    lock = threading.Lock()

    class Innermost:
        held = lock

    class Middle:
        inner = Innermost

    class Outer:
        middle = Middle

    return Outer


class _PlainNestedClass:
    class Inner:
        held = 7


class TestRuling1045NestedClassNamespace(unittest.TestCase):
    """Ruling 1045 (ISO-R24-10): nested class namespace."""

    def test_nested_namespace_lock_refused_class_and_instance(self):
        module = require("ontoloop.consumption")
        cls = _make_nested_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls}, "r24 1045 nested class wf"
        )
        cls = _make_nested_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls()},
            "r24 1045 nested instance wf",
        )

    def test_deep_nested_namespace_lock_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_deep_nested_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls}, "r24 1045 deep nested wf"
        )

    def test_plain_nested_class_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r24 1045 plain nested control wf",
            {"part": _PlainNestedClass},
        )
        self.assertIs(
            recorded["bundle"]["part"], _PlainNestedClass
        )


def _make_metaclass_acquire_class():
    lock = threading.Lock()

    class Meta(type):
        pass

    Meta.held = lock.acquire

    class ViaMeta(metaclass=Meta):
        pass

    return ViaMeta


def _make_metaclass_lock_class():
    lock = threading.Lock()

    class Meta(type):
        pass

    Meta.held = lock

    class ViaMeta(metaclass=Meta):
        pass

    return ViaMeta


class _PlainMetaclassClass:
    pass


class TestRuling1046MetaclassNamespace(unittest.TestCase):
    """Ruling 1046 (E-51): metaclass namespace."""

    def test_metaclass_acquire_refused_class_and_instance(self):
        module = require("ontoloop.consumption")
        cls = _make_metaclass_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1046 metaclass class wf",
        )
        cls = _make_metaclass_acquire_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls()},
            "r24 1046 metaclass instance wf",
        )

    def test_metaclass_lock_value_refused(self):
        module = require("ontoloop.consumption")
        cls = _make_metaclass_lock_class()
        _assert_uncopyable_refused(
            self, module, {"part": cls},
            "r24 1046 metaclass lock wf",
        )

    def test_plain_class_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r24 1046 plain class control wf",
            {"part": _PlainMetaclassClass},
        )
        self.assertIs(
            recorded["bundle"]["part"], _PlainMetaclassClass
        )

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(threading.Lock())},
            "r24 1046 lock control wf",
        )


if __name__ == "__main__":
    unittest.main()
