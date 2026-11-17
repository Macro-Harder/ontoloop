"""Fix round 27 tests for rulings 1294 to 1305, Region 5.

Written test first against the governing base form of
ontoloop/consumption.py. Each ruling stands pinned at both
poles in the form its triage ruling states: the defective
forms stand decided in substance after the cure, and the
standing poles and clean controls its ruling names stand
in their standing forms at both poles.
"""

import array
import logging
import os
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


def _make_module(body, name_hint="r27_region5_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(held=True):
    body = "import threading\nPLAIN = 7\n"
    if held:
        body += "HELD = threading.Lock()\n"
    return _make_module(body, "r27_region5_sub")


class TestRuling1294TransitiveGate(unittest.TestCase):
    """Ruling 1294: the standard library gate at every position."""

    def test_1294_stdlib_function_by_name_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import logging\n"
            "_addHandlerRef = logging._addHandlerRef\n"
            "class K:\n"
            "    def method(self):\n"
            "        return _addHandlerRef\n"
        )
        _assert_records(
            self, module, {"part": Holder(mod.K)},
            "r27 1294 by name wf",
        )

    def test_1294_stdlib_function_by_module_attribute_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import logging\n"
            "class K:\n"
            "    def method(self):\n"
            "        return logging._addHandlerRef\n"
        )
        _assert_records(
            self, module, {"part": Holder(mod.K)},
            "r27 1294 by attribute wf",
        )

    def test_1294_plain_stdlib_function_by_name_records(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import string\n"
            "capwords = string.capwords\n"
            "class K:\n"
            "    def method(self):\n"
            "        return capwords\n"
        )
        _assert_records(
            self, module, {"part": Holder(mod.K)},
            "r27 1294 capwords wf",
        )

    def test_1294_governed_value_by_name_still_refused(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n"
        )
        _assert_refused(
            self, module, {"part": Holder(mod.K)},
            "r27 1294 governed by name wf",
        )

    def test_1294_null_handler_still_records_apart(self):
        module = require("ontoloop.consumption")
        recorded = _assert_records(
            self, module,
            {"part": Holder(logging.NullHandler())},
            "r27 1294 null handler wf",
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsInstance(copied, logging.NullHandler)

    def test_1294_plain_handler_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(logging.Handler())},
            "r27 1294 plain handler wf",
        )

    def test_1294_logger_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(logging.getLogger("r27_1294_probe"))},
            "r27 1294 logger wf",
        )


class TestRuling1295GateBasis(unittest.TestCase):
    """Ruling 1295: the gate decided on facts not supplied."""

    def _fake_stdlib_module(self):
        _counter[0] += 1
        name = "r27_region5_fake_%d" % _counter[0]
        module = types.ModuleType(name)
        stdlib_dir = os.path.dirname(os.__file__)
        module.__file__ = os.path.join(
            stdlib_dir, "no_such_file_r27_region5.py"
        )
        sys.modules[name] = module
        self.addCleanup(sys.modules.pop, name, None)
        exec(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n",
            module.__dict__,
        )
        return module

    def test_1295_fake_stdlib_claim_refused(self):
        module = require("ontoloop.consumption")
        fake = self._fake_stdlib_module()
        _assert_refused(
            self, module, {"part": Holder(fake.K)},
            "r27 1295 fake claim wf",
        )

    def test_1295_no_file_claim_refused(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n"
        )
        _assert_refused(
            self, module, {"part": Holder(mod.K)},
            "r27 1295 no claim wf",
        )

    def test_1295_genuine_null_handler_still_records(self):
        module = require("ontoloop.consumption")
        _assert_records(
            self, module,
            {"part": Holder(logging.NullHandler())},
            "r27 1295 null handler wf",
        )

    def test_1295_genuine_handler_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(logging.Handler())},
            "r27 1295 handler wf",
        )


class TestRuling1296ModuleDictSubscript(unittest.TestCase):
    """Ruling 1296: a subscript of a module dictionary attribute."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1296_dict_subscript_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1296 dict subscript wf",
        )

    def test_1296_attribute_load_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.HELD")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1296 attribute load wf",
        )

    def test_1296_module_value_itself_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r27 1296 module itself wf",
        )


class TestRuling1297SecondHop(unittest.TestCase):
    """Ruling 1297: a module attribute at a second hop."""

    def _home(self, method_body):
        inner = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "def helper():\n"
            "    return HELD\n",
            "r27_region5_inner",
        )
        outer = _make_module("", "r27_region5_outer")
        outer.__dict__["INNER"] = inner
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["OUTER"] = outer
        return home

    def test_1297_chained_attribute_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("OUTER.INNER.HELD")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1297 chained wf",
        )

    def test_1297_helper_call_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("OUTER.INNER.helper()")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1297 helper call wf",
        )

    def test_1297_first_module_itself_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("OUTER")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r27 1297 first module wf",
        )


class TestRuling1298ContainerModuleAttribute(unittest.TestCase):
    """Ruling 1298: contents of a container module attribute."""

    def _home(self, method_body, sub_body):
        sub = _make_module(sub_body, "r27_region5_contsub")
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1298_list_attribute_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "SUB.BOXLIST",
            "import threading\n"
            "BOXLIST = [threading.Lock()]\n",
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1298 list attribute wf",
        )

    def test_1298_mapping_attribute_subscript_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "SUB.BOX['x']",
            "import threading\n"
            "BOX = {'x': threading.Lock()}\n",
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1298 mapping attribute wf",
        )

    def test_1298_plain_container_attribute_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "SUB.PLAINLIST",
            "PLAINLIST = [1, 2, 3]\n",
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r27 1298 plain container wf",
        )


class TestRuling1299GetattrForeignModule(unittest.TestCase):
    """Ruling 1299: the getattr act on a module in home globals."""

    def _home(self, method_body, own_held=False):
        sub = _sub_module()
        body = ""
        if own_held:
            body = (
                "import threading\n"
                "HELD = threading.Lock()\n"
            )
        home = _make_module(
            body
            + "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1299_getattr_literal_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, 'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1299 getattr literal wf",
        )

    def test_1299_getattr_built_name_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, 'HE' + 'LD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1299 getattr built wf",
        )

    def test_1299_registry_form_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(sys.modules[__name__], 'HELD')",
            own_held=True,
        )
        home.__dict__["sys"] = sys
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1299 registry form wf",
        )

    def test_1299_plain_value_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, 'PLAIN')")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r27 1299 plain value wf",
        )


class TestRuling1300VarsForeignModule(unittest.TestCase):
    """Ruling 1300: the vars act on a module in home globals."""

    def _home(self, method_body, own_held=False):
        sub = _sub_module()
        body = ""
        if own_held:
            body = (
                "import threading\n"
                "HELD = threading.Lock()\n"
            )
        home = _make_module(
            body
            + "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1300_vars_plain_call_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1300 vars plain wf",
        )

    def test_1300_vars_starred_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(*[SUB])['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1300 vars starred wf",
        )

    def test_1300_registry_form_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "vars(sys.modules[__name__])['HELD']",
            own_held=True,
        )
        home.__dict__["sys"] = sys
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r27 1300 registry form wf",
        )

    def test_1300_plain_value_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)['PLAIN']")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r27 1300 plain value wf",
        )


class TestRuling1301PresentationWhole(unittest.TestCase):
    """Ruling 1301: the refusal decided on the whole bundle."""

    def _attr_name_module(self, key):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "class K:\n"
            "    def __init__(self):\n"
            "        self.k = '%s'\n"
            "    def method(self):\n"
            "        return globals()[self.k]\n" % key
        )

    def test_1301_class_and_instance_plain_name_records(self):
        module = require("ontoloop.consumption")
        mod = self._attr_name_module("PLAIN")
        bundle = {
            "first": Holder(mod.K),
            "second": Holder(mod.K()),
        }
        _assert_records(
            self, module, bundle,
            "r27 1301 class and instance wf",
        )

    def test_1301_class_and_instance_governed_name_refused(self):
        module = require("ontoloop.consumption")
        mod = self._attr_name_module("HELD")
        bundle = {
            "first": Holder(mod.K),
            "second": Holder(mod.K()),
        }
        _assert_refused(
            self, module, bundle,
            "r27 1301 governed name wf",
        )

    def test_1301_class_alone_still_refused(self):
        module = require("ontoloop.consumption")
        mod = self._attr_name_module("PLAIN")
        _assert_refused(
            self, module, {"part": Holder(mod.K)},
            "r27 1301 class alone wf",
        )

    def test_1301_instance_alone_still_records(self):
        module = require("ontoloop.consumption")
        mod = self._attr_name_module("PLAIN")
        _assert_records(
            self, module, {"part": Holder(mod.K())},
            "r27 1301 instance alone wf",
        )


class CapResult:
    def __init__(self, held):
        self.held = held


class CapCarrier:
    def __init__(self, flag):
        self.flag = flag

    def __deepcopy__(self, memo):
        if self.flag:
            return CapResult(threading.Lock())
        return CapResult(7)


class TestRuling1302CapEdge(unittest.TestCase):
    """Ruling 1302: the per type act cap at exactly its count."""

    def test_1302_exact_count_lock_first_refused(self):
        module = require("ontoloop.consumption")
        instances = [CapCarrier(True)] + [
            CapCarrier(False) for _ in range(31)
        ]
        _assert_refused(
            self, module, {"part": Holder(instances)},
            "r27 1302 exact count lock first wf",
        )

    def test_1302_exact_count_lock_last_refused(self):
        module = require("ontoloop.consumption")
        instances = [
            CapCarrier(False) for _ in range(31)
        ] + [CapCarrier(True)]
        _assert_refused(
            self, module, {"part": Holder(instances)},
            "r27 1302 exact count lock last wf",
        )

    def test_1302_past_count_lock_first_records(self):
        module = require("ontoloop.consumption")
        instances = [CapCarrier(True)] + [
            CapCarrier(False) for _ in range(32)
        ]
        _assert_records(
            self, module, {"part": Holder(instances)},
            "r27 1302 past count lock first wf",
        )


class ArrayCarrier(array.array):
    def __new__(cls):
        return super().__new__(cls, "i", [1, 2])

    def __getstate__(self):
        return {"held": threading.Lock()}


class PlainStateArrayCarrier(array.array):
    def __new__(cls):
        return super().__new__(cls, "i", [1, 2])

    def __getstate__(self):
        return {"plain": 1}


class TestRuling1303ArrayGetstate(unittest.TestCase):
    """Ruling 1303: the array subclass carrier at walked positions."""

    def test_1303_array_getstate_walked_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": [ArrayCarrier()]},
            "r27 1303 walked wf",
        )

    def test_1303_array_getstate_fallback_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module, {"part": Holder(ArrayCarrier())},
            "r27 1303 fallback wf",
        )

    def test_1303_array_plain_state_still_records(self):
        module = require("ontoloop.consumption")
        _assert_records(
            self, module, {"part": [PlainStateArrayCarrier()]},
            "r27 1303 plain state wf",
        )


class TestRuling1304VariableCarriedName(unittest.TestCase):
    """Ruling 1304: a name or code string carried in a variable."""

    def _home(self, method_body, extra=""):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            + extra
            + "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def test_1304_exec_variable_code_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "CODE = 'x = HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(CODE, globals(), loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r27 1304 exec variable class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r27 1304 exec variable instance wf",
        )

    def test_1304_eval_variable_name_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("eval(NAME)", "NAME = 'HELD'\n")
        _assert_refused(
            self, module, {"part": home.K},
            "r27 1304 eval variable wf",
        )

    def test_1304_globals_index_variable_name_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[NAME]", "NAME = 'HELD'\n")
        _assert_refused(
            self, module, {"part": home.K},
            "r27 1304 index variable wf",
        )

    def test_1304_constant_exec_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', globals(), loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r27 1304 constant exec wf",
        )

    def test_1304_variable_plain_code_still_records(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "PLAIN = 7\n"
            "CODE = 'x = PLAIN'\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(CODE, globals(), loc)\n"
            "        return loc['x']\n"
        )
        _assert_records(
            self, module, {"part": home.K},
            "r27 1304 variable plain wf",
        )


class TestRuling1305DynamicActsForeignModule(unittest.TestCase):
    """Ruling 1305: vars and getattr on a foreign module, isolation."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1305_vars_foreign_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)['HELD']")
        _assert_refused(
            self, module, {"part": home.K},
            "r27 1305 vars class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r27 1305 vars instance wf",
        )

    def test_1305_getattr_foreign_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, 'HELD')")
        _assert_refused(
            self, module, {"part": home.K},
            "r27 1305 getattr class wf",
        )
        _assert_refused(
            self, module, {"part": Holder(home.K())},
            "r27 1305 getattr holder wf",
        )

    def test_1305_attribute_form_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.HELD")
        _assert_refused(
            self, module, {"part": home.K},
            "r27 1305 attribute form wf",
        )

    def test_1305_vars_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)['PLAIN']")
        _assert_records(
            self, module, {"part": home.K},
            "r27 1305 vars plain wf",
        )
