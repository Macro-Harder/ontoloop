"""Fix round 26 tests for rulings 1202 to 1211, Region 5.

Written test first against the Fix round 25 head form of
ontoloop/consumption.py. Each ruling stands pinned at both
poles: the defective forms its triage ruling names stand
refused with the governed ValueError after the cure and
record before it, and the clean controls and standing poles
its ruling names record at both poles.
"""

import collections
import functools
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
    name = "r26_region5_mod_%d" % _counter[0]
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


class TestRuling1202DynamicNames(unittest.TestCase):
    """Ruling 1202: exec strings and run time built names."""

    def test_1202_exec_form_class_and_instance(self):
        module = require("ontoloop.consumption")
        for tag in ("class", "instance"):
            mod = _make_module(
                "import threading\n"
                "HELD = threading.Lock()\n"
                "class K:\n"
                "    def method(self):\n"
                "        loc = {}\n"
                "        exec('x = HELD', globals(), loc)\n"
                "        return loc['x']\n"
            )
            _assert_refused(
                self, module,
                {"part": mod.K if tag == "class" else mod.K()},
                "r26 1202 exec %s wf" % tag,
            )

    def test_1202_built_name_globals_index(self):
        module = require("ontoloop.consumption")
        for tag in ("class", "holder"):
            mod = _make_module(
                "import threading\n"
                "HELD = threading.Lock()\n"
                "class K:\n"
                "    def method(self):\n"
                "        part = 'HE'\n"
                "        return globals()[part + 'LD']\n"
            )
            bundle = (
                {"part": mod.K} if tag == "class"
                else {"part": Holder(mod.K())}
            )
            _assert_refused(
                self, module, bundle,
                "r26 1202 built index %s wf" % tag,
            )

    def test_1202_built_name_eval(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        part = 'HE'\n"
            "        return eval(part + 'LD')\n"
        )
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1202 built eval wf",
        )

    def test_1202_format_name_globals_index(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()['HE{}D'.format('L')]\n"
        )
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1202 format index wf",
        )

    def test_1202_exec_plain_name_still_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = PLAIN', globals(), loc)\n"
            "        return loc['x']\n"
        )
        recorded = _assert_records(
            self, module, {"part": mod.K},
            "r26 1202 exec plain wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)

    def test_1202_built_plain_name_still_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "PLAIN = 7\n"
            "class K:\n"
            "    def method(self):\n"
            "        part = 'PLA'\n"
            "        return globals()[part + 'IN']\n"
        )
        recorded = _assert_records(
            self, module, {"part": mod.K},
            "r26 1202 built plain wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)

    def test_1202_literal_forms_still_refused(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()['HELD']\n"
        )
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1202 literal index wf",
        )
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return eval('HELD')\n"
        )
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1202 literal eval wf",
        )


class TestRuling1203CacheConduit(unittest.TestCase):
    """Ruling 1203: a cache wrapper over a helper stands followed."""

    def _conduit_module(self):
        return _make_module(
            "import functools, threading\n"
            "HELD = threading.Lock()\n"
            "def helper():\n"
            "    return HELD\n"
            "wrapped = functools.lru_cache(maxsize=None)(helper)\n"
            "class K:\n"
            "    def method(self):\n"
            "        return wrapped()\n"
        )

    def test_1203_wrapper_conduit_class_and_instance(self):
        module = require("ontoloop.consumption")
        mod = self._conduit_module()
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1203 conduit class wf",
        )
        mod = self._conduit_module()
        _assert_refused(
            self, module, {"part": mod.K()},
            "r26 1203 conduit instance wf",
        )

    def test_1203_helper_direct_still_refused(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "def helper():\n"
            "    return HELD\n"
            "class K:\n"
            "    def method(self):\n"
            "        return helper()\n"
        )
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1203 helper direct wf",
        )

    def test_1203_wrapper_alone_still_records(self):
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
            "r26 1203 wrapper alone wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)

    def test_1203_wrapper_over_plain_helper_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import functools\n"
            "def helper():\n"
            "    return 7\n"
            "wrapped = functools.lru_cache(maxsize=None)(helper)\n"
            "class K:\n"
            "    def method(self):\n"
            "        return wrapped()\n"
        )
        recorded = _assert_records(
            self, module, {"part": mod.K},
            "r26 1203 plain conduit wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)


def _template(value):
    return value


def _view_bundle(carrier_kind):
    globals_map = {"__builtins__": {}}
    view = globals_map.values()
    if carrier_kind == "instance":
        class InstClass:
            pass

        InstClass.held = view
        globals_map["carrier"] = InstClass()
    elif carrier_kind == "class":
        class InstClass:
            pass

        InstClass.held = view
        globals_map["carrier"] = InstClass
    elif carrier_kind == "plain":
        class InstClass:
            pass

        InstClass.held = [1, 2]
        globals_map["carrier"] = InstClass()
    func = types.FunctionType(
        _template.__code__, globals_map, "over_globals"
    )
    return func


class TestRuling1204ViewInstanceClass(unittest.TestCase):
    """Ruling 1204: a view in the class namespace of an instance."""

    def test_1204_view_in_instance_class_namespace(self):
        module = require("ontoloop.consumption")
        func = _view_bundle("instance")
        _assert_refused(
            self, module, {"part": Holder(func)},
            "r26 1204 view instance class wf",
        )
        func = _view_bundle("instance")
        _assert_refused(
            self, module, {"part": func},
            "r26 1204 view instance class direct wf",
        )

    def test_1204_view_in_class_namespace_still_refused(self):
        module = require("ontoloop.consumption")
        func = _view_bundle("class")
        _assert_refused(
            self, module, {"part": Holder(func)},
            "r26 1204 view class standing wf",
        )

    def test_1204_plain_instance_class_still_records(self):
        module = require("ontoloop.consumption")
        func = _view_bundle("plain")
        _assert_records(
            self, module, {"part": Holder(func)},
            "r26 1204 plain instance class wf",
        )


def _rebuild_branch_list(*args):
    return BranchList()


def _rebuild_branch_dict(*args):
    return BranchDict()


def _rebuild_branch_deque(*args):
    return BranchDeque()


class BranchList(list):
    """List subclass whose reduce act creates its values."""

    mode = "args_lock"

    def __reduce__(self):
        if self.mode == "args_lock":
            return (_rebuild_branch_list, (threading.Lock(),))
        if self.mode == "tail_lock":
            return (
                _rebuild_branch_list, (), None,
                iter([threading.Lock()]), iter([]),
            )
        if self.mode == "tail_view":
            return (
                _rebuild_branch_list, (), None,
                iter([{"a": 1}.values()]), iter([]),
            )
        return (
            _rebuild_branch_list, (), None,
            iter([10, 20]), iter([]),
        )


class BranchDict(dict):
    def __reduce__(self):
        return (
            _rebuild_branch_dict, (), None,
            iter([]), iter([("k", threading.Lock())]),
        )


class BranchTuple(tuple):
    def __reduce__(self):
        return (_rebuild_branch_list, (threading.Lock(),))


class BranchDeque(collections.deque):
    def __reduce__(self):
        return (
            _rebuild_branch_deque, (), None,
            iter([threading.Lock()]), iter([]),
        )


def _branch_list(mode):
    carrier = BranchList()
    carrier.mode = mode
    return carrier


def _rebuild_plain_list():
    return []


class _PlainTailCarrier:
    def __reduce__(self):
        return (
            _rebuild_plain_list, (), None,
            iter([threading.Lock()]), iter([]),
        )


class TestRuling1205BranchReduce(unittest.TestCase):
    """Ruling 1205: reduce readings of branch matched carriers."""

    def test_1205_lock_in_reduce_args_list_subclass(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(_branch_list("args_lock"))},
            "r26 1205 list args wf",
        )

    def test_1205_lock_in_reduce_args_tuple_subclass(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": Holder(BranchTuple())},
            "r26 1205 tuple args wf",
        )

    def test_1205_lock_in_list_items_element(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(_branch_list("tail_lock"))},
            "r26 1205 list items wf",
        )

    def test_1205_lock_in_dict_items_element(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": Holder(BranchDict())},
            "r26 1205 dict items wf",
        )

    def test_1205_lock_in_deque_tail_element(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": Holder(BranchDeque())},
            "r26 1205 deque tail wf",
        )

    def test_1205_view_in_list_tail_element(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(_branch_list("tail_view"))},
            "r26 1205 list tail view wf",
        )

    def test_1205_branch_carrier_direct_still_records(self):
        module = require("ontoloop.consumption")
        recorded = _assert_records(
            self, module, {"part": _branch_list("tail_lock")},
            "r26 1205 direct walked wf",
        )
        self.assertEqual(list(recorded["bundle"]["part"]), [])

    def test_1205_branch_tail_plain_still_records(self):
        module = require("ontoloop.consumption")
        recorded = _assert_records(
            self, module,
            {"part": Holder(_branch_list("plain"))},
            "r26 1205 branch plain tail wf",
        )
        self.assertEqual(list(recorded["bundle"]["part"].part), [10, 20])

    def test_1205_plain_carrier_tail_still_refused(self):
        module = require("ontoloop.consumption")
        carrier = _PlainTailCarrier()
        _assert_refused(
            self, module, {"part": Holder(carrier)},
            "r26 1205 plain tail standing wf",
        )


class ByteStateCarrier(bytearray):
    def __getstate__(self):
        return {"held": threading.Lock()}


class BytePlainCarrier(bytearray):
    def __getstate__(self):
        return {"held": 5}


class TestRuling1206BytearrayGetstate(unittest.TestCase):
    """Ruling 1206: bytearray getstate at walked positions."""

    def test_1206_bytearray_state_walked_positions(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": [ByteStateCarrier(b"ab")]},
            "r26 1206 bytearray in list wf",
        )
        _assert_refused(
            self, module, {"part": ByteStateCarrier(b"ab")},
            "r26 1206 bytearray direct wf",
        )

    def test_1206_bytearray_state_fallback_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(ByteStateCarrier(b"ab"))},
            "r26 1206 bytearray holder wf",
        )

    def test_1206_bytearray_plain_state_still_records(self):
        module = require("ontoloop.consumption")
        recorded = _assert_records(
            self, module, {"part": [BytePlainCarrier(b"ab")]},
            "r26 1206 bytearray plain wf",
        )
        self.assertEqual(bytes(recorded["bundle"]["part"][0]), b"ab")


class TestRuling1207FunctionGlobalsAttribute(unittest.TestCase):
    """Ruling 1207: a reach through a function globals attribute."""

    def _attr_module(self, held_line):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def helper():\n"
            "    return 0\n"
            "class K:\n"
            "    def method(self):\n"
            "        return helper.__globals__['%s']\n" % held_line
        )

    def test_1207_globals_attribute_class_and_instance(self):
        module = require("ontoloop.consumption")
        mod = self._attr_module("HELD")
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1207 globals attr class wf",
        )
        mod = self._attr_module("HELD")
        _assert_refused(
            self, module, {"part": mod.K()},
            "r26 1207 globals attr instance wf",
        )

    def test_1207_globals_attribute_plain_still_records(self):
        module = require("ontoloop.consumption")
        mod = self._attr_module("PLAIN")
        recorded = _assert_records(
            self, module, {"part": mod.K},
            "r26 1207 globals attr plain wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)


class TestRuling1208RegistryModuleReach(unittest.TestCase):
    """Ruling 1208: vars and getattr reaches through the registry."""

    def test_1208_vars_registry_form(self):
        module = require("ontoloop.consumption")
        for tag in ("class", "instance"):
            mod = _make_module(
                "import sys, threading\n"
                "HELD = threading.Lock()\n"
                "class K:\n"
                "    def method(self):\n"
                "        return vars(sys.modules[__name__])['HELD']\n"
            )
            _assert_refused(
                self, module,
                {"part": mod.K if tag == "class" else mod.K()},
                "r26 1208 vars %s wf" % tag,
            )

    def test_1208_getattr_registry_form(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import sys, threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(sys.modules[__name__], 'HELD')\n"
        )
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1208 getattr wf",
        )

    def test_1208_vars_plain_still_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import sys\n"
            "PLAIN = 7\n"
            "class K:\n"
            "    def method(self):\n"
            "        return vars(sys.modules[__name__])['PLAIN']\n"
        )
        recorded = _assert_records(
            self, module, {"part": mod.K},
            "r26 1208 vars plain wf",
        )
        self.assertIs(recorded["bundle"]["part"], mod.K)


class TestRuling1209ModuleAttributeReach(unittest.TestCase):
    """Ruling 1209: reaches through a module standing in home globals."""

    def _home_module(self, method_line, sub_body=None):
        if sub_body is None:
            sub_body = (
                "import threading\n"
                "HELD = threading.Lock()\n"
                "PLAIN = 7\n"
                "def helper():\n"
                "    return HELD\n"
                "def phelper():\n"
                "    return PLAIN\n"
            )
        sub = _make_module(sub_body)
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_line
        )
        home.SUB = sub
        return home

    def test_1209_module_helper_call(self):
        module = require("ontoloop.consumption")
        for tag in ("class", "instance"):
            home = self._home_module("SUB.helper()")
            _assert_refused(
                self, module,
                {"part": home.K if tag == "class" else home.K()},
                "r26 1209 helper call %s wf" % tag,
            )

    def test_1209_module_value_attribute(self):
        module = require("ontoloop.consumption")
        home = self._home_module("SUB.HELD")
        _assert_refused(
            self, module, {"part": home.K},
            "r26 1209 value attr wf",
        )

    def test_1209_module_alone_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home_module("SUB")
        recorded = _assert_records(
            self, module, {"part": home.K},
            "r26 1209 module alone wf",
        )
        self.assertIs(recorded["bundle"]["part"], home.K)

    def test_1209_module_plain_reaches_still_record(self):
        module = require("ontoloop.consumption")
        home = self._home_module("SUB.phelper()")
        recorded = _assert_records(
            self, module, {"part": home.K},
            "r26 1209 plain helper wf",
        )
        self.assertIs(recorded["bundle"]["part"], home.K)
        home = self._home_module("SUB.PLAIN")
        recorded = _assert_records(
            self, module, {"part": home.K},
            "r26 1209 plain value wf",
        )
        self.assertIs(recorded["bundle"]["part"], home.K)


class TestRuling1210InstanceAttributeName(unittest.TestCase):
    """Ruling 1210: a name carried in an instance attribute."""

    def _attr_name_module(self, act_line, key="HELD"):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "class K:\n"
            "    def __init__(self):\n"
            "        self.k = '%s'\n"
            "    def method(self):\n"
            "        return %s\n" % (key, act_line)
        )

    def test_1210_globals_index_attribute_name(self):
        module = require("ontoloop.consumption")
        mod = self._attr_name_module("globals()[self.k]")
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1210 globals index class wf",
        )
        mod = self._attr_name_module("globals()[self.k]")
        _assert_refused(
            self, module, {"part": mod.K()},
            "r26 1210 globals index instance wf",
        )

    def test_1210_eval_attribute_name(self):
        module = require("ontoloop.consumption")
        mod = self._attr_name_module("eval(self.k)")
        _assert_refused(
            self, module, {"part": mod.K},
            "r26 1210 eval class wf",
        )
        mod = self._attr_name_module("eval(self.k)")
        _assert_refused(
            self, module, {"part": mod.K()},
            "r26 1210 eval instance wf",
        )

    def test_1210_plain_attribute_name_still_records(self):
        module = require("ontoloop.consumption")
        mod = self._attr_name_module(
            "globals()[self.k]", key="PLAIN"
        )
        recorded = _assert_records(
            self, module, {"part": mod.K()},
            "r26 1210 plain attr name wf",
        )
        self.assertIsNot(recorded["bundle"]["part"], mod.K)


class DeepResult:
    def __init__(self, held):
        self.held = held


class DeepCarrier:
    def __init__(self, flag):
        self.flag = flag

    def __deepcopy__(self, memo):
        if self.flag:
            return DeepResult(threading.Lock())
        return DeepResult(7)


class TestRuling1211DeepcopyPerInstance(unittest.TestCase):
    """Ruling 1211: a custom deepcopy return decided per instance."""

    def test_1211_second_instance_return_decided(self):
        module = require("ontoloop.consumption")
        bundle = {
            "part": Holder([DeepCarrier(True), DeepCarrier(False)])
        }
        _assert_refused(
            self, module, bundle,
            "r26 1211 plain decided first wf",
        )

    def test_1211_lock_decided_first_still_refused(self):
        module = require("ontoloop.consumption")
        bundle = {
            "part": Holder([DeepCarrier(False), DeepCarrier(True)])
        }
        _assert_refused(
            self, module, bundle,
            "r26 1211 lock decided first wf",
        )

    def test_1211_single_lock_instance_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": Holder(DeepCarrier(True))},
            "r26 1211 single lock wf",
        )

    def test_1211_two_plain_instances_still_record(self):
        module = require("ontoloop.consumption")
        recorded = _assert_records(
            self, module,
            {"part": Holder([DeepCarrier(False), DeepCarrier(False)])},
            "r26 1211 two plain wf",
        )
        held = [
            item.held
            for item in recorded["bundle"]["part"].part
        ]
        self.assertEqual(held, [7, 7])


if __name__ == "__main__":
    unittest.main()
