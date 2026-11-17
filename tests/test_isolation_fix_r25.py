"""Fix round 25 tests for rulings 1110 to 1118, Region 5.

Written test first against the Fix round 24 head form of
ontoloop/consumption.py. Each ruling stands pinned at both
poles: the defective forms its triage ruling names stand
refused with the governed ValueError after the cure and
record before it, and the clean controls its ruling names
record at both poles.
"""

import bz2
import collections
import contextvars
import functools
import json
import logging
import lzma
import operator
import struct
import sys
import threading
import types
import unittest

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


def _assert_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), UNCOPYABLE_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _assert_records(case, module, bundle, workflow):
    recorded = module.record_promotion(workflow, bundle)
    case.assertTrue(recorded["recorded"])
    return recorded


_counter = [0]


def _make_module(body):
    _counter[0] += 1
    name = "r25_region5_mod_%d" % _counter[0]
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


_EXTRA_FORMS = {
    "logger": "logging.getLogger('r25probe')",
    "contextvar": "contextvars.ContextVar('r25v')",
    "struct": "struct.Struct('i')",
    "decoder": "json.JSONDecoder()",
    "bz2": "bz2.BZ2Compressor()",
    "lzma": "lzma.LZMACompressor()",
}

_EXTRA_PREAMBLE = (
    "import logging, contextvars, struct, json, bz2, lzma\n"
)


def _extra_module(kind, carrier="function"):
    body = _EXTRA_PREAMBLE + "HELD = %s\n" % _EXTRA_FORMS[kind]
    if carrier == "function":
        body += (
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n"
        )
    elif carrier == "property":
        body += (
            "class K:\n"
            "    @property\n"
            "    def method(self):\n"
            "        return HELD\n"
        )
    elif carrier == "classmethod":
        body += (
            "class K:\n"
            "    @classmethod\n"
            "    def method(cls):\n"
            "        return HELD\n"
        )
    elif carrier == "staticmethod":
        body += (
            "class K:\n"
            "    @staticmethod\n"
            "    def method():\n"
            "        return HELD\n"
        )
    elif carrier == "nested":
        body += (
            "class K:\n"
            "    def method(self):\n"
            "        def inner():\n"
            "            return HELD\n"
            "        return inner()\n"
        )
    elif carrier == "lambda":
        body += (
            "class K:\n"
            "    method = lambda self: HELD\n"
        )
    return _make_module(body)


class TestRuling1110ExtraTypes(unittest.TestCase):
    """Ruling 1110: extra types referenced by name stand refused."""

    def _check_kind(self, kind):
        module = require("ontoloop.consumption")
        mod = _extra_module(kind)
        _assert_refused(
            self, module, {"part": mod.K},
            "r25 1110 %s class wf" % kind,
        )
        mod = _extra_module(kind)
        _assert_refused(
            self, module, {"part": mod.K()},
            "r25 1110 %s instance wf" % kind,
        )

    def test_1110_logger(self):
        self._check_kind("logger")

    def test_1110_contextvar(self):
        self._check_kind("contextvar")

    def test_1110_struct(self):
        self._check_kind("struct")

    def test_1110_decoder(self):
        self._check_kind("decoder")

    def test_1110_bz2(self):
        self._check_kind("bz2")

    def test_1110_lzma(self):
        self._check_kind("lzma")

    def test_1110_logger_holder_position(self):
        module = require("ontoloop.consumption")
        mod = _extra_module("logger")
        _assert_refused(
            self, module, {"part": Holder(mod.K)},
            "r25 1110 logger holder wf",
        )
        mod = _extra_module("struct")
        _assert_refused(
            self, module, {"part": Holder(mod.K())},
            "r25 1110 struct holder instance wf",
        )

    def test_1110_logger_accessors_and_carried(self):
        module = require("ontoloop.consumption")
        for carrier in (
            "property", "classmethod", "staticmethod",
            "nested", "lambda",
        ):
            mod = _extra_module("logger", carrier)
            _assert_refused(
                self, module, {"part": mod.K},
                "r25 1110 logger %s wf" % carrier,
            )

    def test_1110_cache_wrapper_still_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import functools\n"
            "def _plain(x):\n"
            "    return x\n"
            "HELD = functools.lru_cache(maxsize=None)(_plain)\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n"
        )
        recorded = _assert_records(
            self, module, {"part": mod.K},
            "r25 1110 cache wrapper wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)

    def test_1110_referenced_lock_still_refused(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n"
        )
        _assert_refused(
            self, module, {"part": mod.K},
            "r25 1110 referenced lock wf",
        )

    def test_1110_plain_class_still_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "HELD = 7\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n"
        )
        recorded = _assert_records(
            self, module, {"part": mod.K},
            "r25 1110 plain reference wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)


class TestRuling1111SecondHop(unittest.TestCase):
    """Ruling 1111: the second hop of the referenced reading."""

    def _hop_module(self, held_expr):
        return _make_module(
            "import threading\n"
            "HELD = %s\n"
            "def helper():\n"
            "    return HELD\n"
            "class K:\n"
            "    def method(self):\n"
            "        return helper()\n" % held_expr
        )

    def test_1111_second_hop_class_and_instance(self):
        module = require("ontoloop.consumption")
        mod = self._hop_module("threading.Lock()")
        _assert_refused(
            self, module, {"part": mod.K},
            "r25 1111 hop class wf",
        )
        mod = self._hop_module("threading.Lock()")
        _assert_refused(
            self, module, {"part": mod.K()},
            "r25 1111 hop instance wf",
        )

    def test_1111_second_hop_holder(self):
        module = require("ontoloop.consumption")
        mod = self._hop_module("threading.Lock()")
        _assert_refused(
            self, module, {"part": Holder(mod.K)},
            "r25 1111 hop holder wf",
        )

    def test_1111_helper_alone_still_refused(self):
        module = require("ontoloop.consumption")
        mod = self._hop_module("threading.Lock()")
        _assert_refused(
            self, module, {"part": Holder(mod.helper)},
            "r25 1111 helper alone wf",
        )

    def test_1111_plain_helper_still_records(self):
        module = require("ontoloop.consumption")
        mod = self._hop_module("7")
        recorded = _assert_records(
            self, module, {"part": mod.K},
            "r25 1111 plain helper wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)


class TestRuling1112DynamicGlobals(unittest.TestCase):
    """Ruling 1112: dynamic globals access forms stand refused."""

    def test_1112_globals_index_class_and_instance(self):
        module = require("ontoloop.consumption")
        for bundle_part, tag in (("K", "class"), ("K()", "instance")):
            mod = _make_module(
                "import threading\n"
                "HELD = threading.Lock()\n"
                "class K:\n"
                "    def method(self):\n"
                "        return globals()['HELD']\n"
            )
            _assert_refused(
                self, module,
                {"part": getattr(mod, "K") if tag == "class"
                 else mod.K()},
                "r25 1112 index %s wf" % tag,
            )

    def test_1112_eval_form(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return eval('HELD')\n"
        )
        _assert_refused(
            self, module, {"part": mod.K},
            "r25 1112 eval class wf",
        )
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return eval('HELD')\n"
        )
        _assert_refused(
            self, module, {"part": Holder(mod.K)},
            "r25 1112 eval holder wf",
        )


def _template(value):
    return value


def _view_globals_bundle(carrier_kind):
    globals_map = {"__builtins__": {}}
    view = globals_map.values()
    if carrier_kind == "class":
        class ViewClass:
            pass

        ViewClass.held = view
        globals_map["carrier"] = ViewClass
    elif carrier_kind == "factory":
        class Factory:
            def __call__(self):
                return None

        factory = Factory()
        factory.held = view
        globals_map["carrier"] = collections.defaultdict(factory)
    elif carrier_kind == "methodcaller":
        globals_map["carrier"] = operator.methodcaller(
            "keys", view
        )
    elif carrier_kind == "itemgetter":
        globals_map["carrier"] = operator.itemgetter(view)
    func = types.FunctionType(
        _template.__code__, globals_map, "over_globals"
    )
    return func


class TestRuling1113ViewWalk(unittest.TestCase):
    """Ruling 1113: the view walk type, factory, operator limbs."""

    def test_1113_view_in_class_namespace(self):
        module = require("ontoloop.consumption")
        func = _view_globals_bundle("class")
        _assert_refused(
            self, module, {"part": Holder(func)},
            "r25 1113 view class wf",
        )
        func = _view_globals_bundle("class")
        _assert_refused(
            self, module, {"part": func},
            "r25 1113 view class direct wf",
        )

    def test_1113_view_in_defaultdict_factory(self):
        module = require("ontoloop.consumption")
        func = _view_globals_bundle("factory")
        _assert_refused(
            self, module, {"part": Holder(func)},
            "r25 1113 view factory wf",
        )

    def test_1113_view_in_methodcaller(self):
        module = require("ontoloop.consumption")
        func = _view_globals_bundle("methodcaller")
        _assert_refused(
            self, module, {"part": Holder(func)},
            "r25 1113 view methodcaller wf",
        )

    def test_1113_view_in_itemgetter(self):
        module = require("ontoloop.consumption")
        func = _view_globals_bundle("itemgetter")
        _assert_refused(
            self, module, {"part": Holder(func)},
            "r25 1113 view itemgetter wf",
        )

    def test_1113_plain_carriers_still_record(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}, "held": 7}

        class PlainClass:
            held = 3

        globals_map["carrier"] = PlainClass
        globals_map["dd"] = collections.defaultdict(list)
        globals_map["mc"] = operator.methodcaller("keys", 1)
        func = types.FunctionType(
            _template.__code__, globals_map, "over_globals"
        )
        _assert_records(
            self, module, {"part": Holder(func)},
            "r25 1113 plain carriers wf",
        )


def _rebuild_list():
    return []


def _rebuild_dict():
    return {}


class _ReduceTailCarrier:
    """Reduce carrier creating its tail values inside its body."""

    kind = "plain_list"

    def __reduce__(self):
        if self.kind == "lock_list":
            return (
                _rebuild_list, (), None,
                iter([threading.Lock()]), iter([]),
            )
        if self.kind == "view_list":
            return (
                _rebuild_list, (), None,
                iter([{"a": 1}.values()]), iter([]),
            )
        if self.kind == "lock_dict":
            return (
                _rebuild_dict, (), None,
                iter([]), iter([("k", threading.Lock())]),
            )
        return (
            _rebuild_list, (), None,
            iter([1, 2]), iter([]),
        )


def _tail_carrier(kind):
    return type(
        "TailCarrier_%s" % kind, (_ReduceTailCarrier,),
        {"kind": kind},
    )()


class TestRuling1114ReduceTail(unittest.TestCase):
    """Ruling 1114: reduce fourth and fifth elements stand read."""

    def test_1114_lock_in_list_items_holder(self):
        module = require("ontoloop.consumption")
        carrier = _tail_carrier("lock_list")
        _assert_refused(
            self, module, {"part": Holder(carrier)},
            "r25 1114 list items holder wf",
        )

    def test_1114_lock_in_list_items_direct_and_nested(self):
        module = require("ontoloop.consumption")
        carrier = _tail_carrier("lock_list")
        _assert_refused(
            self, module, {"part": carrier},
            "r25 1114 list items direct wf",
        )
        carrier = _tail_carrier("lock_list")
        _assert_refused(
            self, module, {"part": [carrier]},
            "r25 1114 list items nested wf",
        )

    def test_1114_view_in_list_items_holder(self):
        module = require("ontoloop.consumption")
        carrier = _tail_carrier("view_list")
        _assert_refused(
            self, module, {"part": Holder(carrier)},
            "r25 1114 view list items wf",
        )

    def test_1114_lock_in_dict_items_holder(self):
        module = require("ontoloop.consumption")
        carrier = _tail_carrier("lock_dict")
        _assert_refused(
            self, module, {"part": Holder(carrier)},
            "r25 1114 dict items holder wf",
        )

    def test_1114_plain_reduce_tail_still_records(self):
        module = require("ontoloop.consumption")
        carrier = _tail_carrier("plain_list")
        recorded = _assert_records(
            self, module, {"part": Holder(carrier)},
            "r25 1114 plain tail wf",
        )
        self.assertEqual(
            recorded["bundle"]["part"].part, [1, 2]
        )


class _TupleNewargs(tuple):
    def __getnewargs__(self):
        return (threading.Lock(),)


class _ListNewargs(list):
    def __getnewargs__(self):
        return (threading.Lock(),)


class _DictNewargs(dict):
    def __getnewargs__(self):
        return (threading.Lock(),)


class _TupleNewargsEx(tuple):
    def __getnewargs_ex__(self):
        return ((threading.Lock(),), {})


class _TuplePlainNewargs(tuple):
    def __getnewargs__(self):
        return ((1, 2),)


class TestRuling1115BranchNewargs(unittest.TestCase):
    """Ruling 1115: branch matched newargs reach stands read."""

    def test_1115_tuple_newargs_lock(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(_TupleNewargs((1,)))},
            "r25 1115 tuple newargs wf",
        )

    def test_1115_list_newargs_lock(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(_ListNewargs([1]))},
            "r25 1115 list newargs wf",
        )

    def test_1115_dict_newargs_lock(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(_DictNewargs({"a": 1}))},
            "r25 1115 dict newargs wf",
        )

    def test_1115_tuple_newargs_ex_lock(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(_TupleNewargsEx((1,)))},
            "r25 1115 tuple newargs ex wf",
        )

    def test_1115_plain_newargs_still_records(self):
        module = require("ontoloop.consumption")
        _assert_records(
            self, module,
            {"part": Holder(_TuplePlainNewargs((1, 2)))},
            "r25 1115 plain newargs wf",
        )


def _state_carrier(base, plain=False):
    held = 7 if plain else threading.Lock()

    class Carrier(base):
        def __getstate__(self):
            return {"held": held}

    return Carrier


class TestRuling1116BranchGetstate(unittest.TestCase):
    """Ruling 1116: branch matched getstate at walked positions."""

    def test_1116_list_carrier_walked_positions(self):
        module = require("ontoloop.consumption")
        carrier_cls = _state_carrier(list)
        positions = [
            ({"part": carrier_cls([1])}, "direct"),
            ({"part": [carrier_cls([1])]}, "nested list"),
            ({"part": {"k": carrier_cls([1])}}, "mapping value"),
            ({"part": (carrier_cls([1]),)}, "tuple element"),
        ]
        for bundle, tag in positions:
            _assert_refused(
                self, module, bundle,
                "r25 1116 list %s wf" % tag,
            )

    def test_1116_other_branch_carriers_direct(self):
        module = require("ontoloop.consumption")
        forms = [
            (_state_carrier(dict)({"a": 1}), "dict"),
            (_state_carrier(set)({1}), "set"),
            (_state_carrier(collections.deque)(
                collections.deque([1])), "deque"),
            (_state_carrier(collections.UserList)(
                collections.UserList([1])), "userlist"),
        ]
        for carrier, tag in forms:
            _assert_refused(
                self, module, {"part": carrier},
                "r25 1116 %s direct wf" % tag,
            )

    def test_1116_fallback_position_still_refused(self):
        module = require("ontoloop.consumption")
        carrier_cls = _state_carrier(list)
        _assert_refused(
            self, module, {"part": Holder(carrier_cls([1]))},
            "r25 1116 fallback holder wf",
        )

    def test_1116_plain_state_still_records(self):
        module = require("ontoloop.consumption")
        carrier_cls = _state_carrier(list, plain=True)
        _assert_records(
            self, module, {"part": carrier_cls([1])},
            "r25 1116 plain walked wf",
        )
        _assert_records(
            self, module, {"part": Holder(carrier_cls([1]))},
            "r25 1116 plain holder wf",
        )


class _DeepcopyLockCarrier:
    def __deepcopy__(self, memo):
        built = object.__new__(_DeepcopyLockCarrier)
        built.held = threading.Lock()
        return built


class _DeepcopyPlainCarrier:
    def __deepcopy__(self, memo):
        built = object.__new__(_DeepcopyPlainCarrier)
        built.held = 7
        return built


class TestRuling1117DeepcopyReturn(unittest.TestCase):
    """Ruling 1117: the custom deepcopy return stands decided."""

    def test_1117_deepcopy_lock_return_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(_DeepcopyLockCarrier())},
            "r25 1117 deepcopy lock wf",
        )

    def test_1117_plain_deepcopy_return_records(self):
        module = require("ontoloop.consumption")
        recorded = _assert_records(
            self, module,
            {"part": Holder(_DeepcopyPlainCarrier())},
            "r25 1117 deepcopy plain wf",
        )
        found = module.discover("r25 1117 deepcopy plain wf")
        self.assertEqual(found["answer"], "promotion")
        self.assertEqual(
            found["bundle"]["part"].part.held, 7
        )


_LOCK = threading.Lock()


class _ServiceWithLockDefault:
    def method(self, held=_LOCK):
        return held


class _OuterInstanceNamespace:
    member = _ServiceWithLockDefault()


class _InnerLockNamespace:
    held = _LOCK


class _OuterContainerNamespace:
    member = [_InnerLockNamespace]


class _OuterMappingNamespace:
    member = {"k": _InnerLockNamespace}


class _OuterDefaultClassNamespace:
    def method(self, held=_InnerLockNamespace):
        return held


def _synthetic_globals_function():
    globals_map = {"__builtins__": {}, "held": threading.Lock()}
    return types.FunctionType(
        _template.__code__, globals_map, "carried_fn"
    )


_CARRIED_FN = _synthetic_globals_function()


class _OuterDefaultFunctionNamespace:
    def method(self, held=_CARRIED_FN):
        return held


def _closure_outer():
    carried = _CARRIED_FN

    class Outer:
        def method(self):
            return carried

    return Outer


class _PlainNamespaceClass:
    held = 3

    def method(self, plain=7):
        return plain


class _OuterPlainInstanceNamespace:
    member = _PlainNamespaceClass()


class TestRuling1118NamespaceMarking(unittest.TestCase):
    """Ruling 1118: namespace marking suppresses no expansion."""

    def test_1118_instance_in_namespace(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": _OuterInstanceNamespace},
            "r25 1118 instance namespace class wf",
        )
        _assert_refused(
            self, module, {"part": _OuterInstanceNamespace()},
            "r25 1118 instance namespace instance wf",
        )

    def test_1118_class_in_container_in_namespace(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": _OuterContainerNamespace},
            "r25 1118 container class wf",
        )
        _assert_refused(
            self, module, {"part": _OuterContainerNamespace()},
            "r25 1118 container instance wf",
        )
        _assert_refused(
            self, module, {"part": _OuterMappingNamespace},
            "r25 1118 mapping class wf",
        )

    def test_1118_class_in_member_defaults(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": _OuterDefaultClassNamespace},
            "r25 1118 default class wf",
        )
        _assert_refused(
            self, module,
            {"part": _OuterDefaultClassNamespace()},
            "r25 1118 default class instance wf",
        )

    def test_1118_function_in_member_defaults(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": _OuterDefaultFunctionNamespace},
            "r25 1118 default function wf",
        )
        _assert_refused(
            self, module,
            {"part": _OuterDefaultFunctionNamespace()},
            "r25 1118 default function instance wf",
        )

    def test_1118_function_in_member_closure(self):
        module = require("ontoloop.consumption")
        outer = _closure_outer()
        _assert_refused(
            self, module, {"part": outer},
            "r25 1118 closure function wf",
        )

    def test_1118_plain_namespace_still_records(self):
        module = require("ontoloop.consumption")
        _assert_records(
            self, module, {"part": _OuterPlainInstanceNamespace},
            "r25 1118 plain instance namespace wf",
        )
        _assert_records(
            self, module, {"part": _PlainNamespaceClass},
            "r25 1118 plain class wf",
        )

    def test_1118_bare_nested_class_still_refused(self):
        module = require("ontoloop.consumption")

        class OuterBare:
            inner = _InnerLockNamespace

        _assert_refused(
            self, module, {"part": OuterBare},
            "r25 1118 bare nested wf",
        )


if __name__ == "__main__":
    unittest.main()
