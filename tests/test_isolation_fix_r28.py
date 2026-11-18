"""Fix round 28 tests for rulings 1388 to 1398, Region 5.

Written test first against the governing base form of
ontoloop/consumption.py. Each ruling stands pinned at both
poles in the form its triage ruling states: the defective
forms stand decided in substance after the cure, and the
standing poles and clean controls its ruling names stand
in their standing forms at both poles.
"""

import logging
import os
import sys
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


def _make_module(body, name_hint="r28_region5_mod"):
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
    return _make_module(body, "r28_region5_sub")


def _chain_home(method_body):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r28_region5_inner",
    )
    outer = _make_module("", "r28_region5_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(
        "class K:\n"
        "    def method(self):\n"
        "        return %s\n" % method_body
    )
    home.__dict__["OUTER"] = outer
    return home


class TestRuling1388GateOwnership(unittest.TestCase):
    """Ruling 1388: a file claim naming a genuine file of another."""

    def _fake_module(self, file_value):
        _counter[0] += 1
        name = "r28_region5_fake_%d" % _counter[0]
        module = types.ModuleType(name)
        module.__file__ = file_value
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

    def test_1388_fake_claim_on_os_file_refused(self):
        module = require("ontoloop.consumption")
        fake = self._fake_module(os.__file__)
        _assert_refused(
            self, module, {"part": Holder(fake.K)},
            "r28 1388 fake os file wf",
        )

    def test_1388_fake_claim_no_file_still_refused(self):
        module = require("ontoloop.consumption")
        stdlib_dir = os.path.dirname(os.__file__)
        fake = self._fake_module(os.path.join(
            stdlib_dir, "no_such_file_r28_region5.py"
        ))
        _assert_refused(
            self, module, {"part": Holder(fake.K)},
            "r28 1388 fake no file wf",
        )

    def test_1388_genuine_stdlib_function_still_records(self):
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
            "r28 1388 stdlib function wf",
        )

    def test_1388_null_handler_still_records_apart(self):
        module = require("ontoloop.consumption")
        recorded = _assert_records(
            self, module,
            {"part": Holder(logging.NullHandler())},
            "r28 1388 null handler wf",
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsInstance(copied, logging.NullHandler)

    def test_1388_plain_handler_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(logging.Handler())},
            "r28 1388 plain handler wf",
        )


class TestRuling1389DictSubscriptVariableKey(unittest.TestCase):
    """Ruling 1389: a module dictionary subscript, key in a variable."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "KEY = 'HELD'\n"
            "PKEY = 'PLAIN'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1389_variable_key_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[KEY]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1389 variable key wf",
        )

    def test_1389_literal_key_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1389 literal key wf",
        )

    def test_1389_variable_plain_key_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[PKEY]")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r28 1389 plain key wf",
        )


class TestRuling1390GetattrVariableName(unittest.TestCase):
    """Ruling 1390: the getattr act, name carried in a variable."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "NM = 'HELD'\n"
            "PNM = 'PLAIN'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1390_getattr_variable_name_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, NM)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1390 getattr variable wf",
        )

    def test_1390_getattr_literal_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, 'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1390 getattr literal wf",
        )

    def test_1390_getattr_variable_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, PNM)")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r28 1390 getattr plain wf",
        )


class TestRuling1391IsolationVariableName(unittest.TestCase):
    """Ruling 1391: dynamic acts on a foreign module, variable name."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "NAME = 'HELD'\n"
            "PNAME = 'PLAIN'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1391_getattr_variable_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, NAME)")
        _assert_refused(
            self, module, {"part": home.K},
            "r28 1391 getattr class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r28 1391 getattr instance wf",
        )

    def test_1391_vars_variable_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)[NAME]")
        _assert_refused(
            self, module, {"part": home.K},
            "r28 1391 vars class wf",
        )

    def test_1391_dict_subscript_variable_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[NAME]")
        _assert_refused(
            self, module, {"part": home.K},
            "r28 1391 dict subscript class wf",
        )

    def test_1391_getattr_variable_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, PNAME)")
        _assert_records(
            self, module, {"part": home.K},
            "r28 1391 getattr plain wf",
        )


class TestRuling1392ExecForeignGlobals(unittest.TestCase):
    """Ruling 1392: the exec act with a foreign globals argument."""

    def _home(self, method_body, extra=""):
        sub = _sub_module()
        home = _make_module(
            extra
            + "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        %s\n"
            "        return loc['x']\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1392_exec_constant_foreign_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("exec('x = HELD', SUB.__dict__, loc)")
        _assert_refused(
            self, module, {"part": home.K},
            "r28 1392 exec constant class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r28 1392 exec constant instance wf",
        )

    def test_1392_exec_carried_foreign_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "exec(CODE, SUB.__dict__, loc)",
            "CODE = 'x = HELD'\n",
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r28 1392 exec carried class wf",
        )

    def test_1392_exec_home_constant_still_refused(self):
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
            "r28 1392 exec home wf",
        )

    def test_1392_exec_foreign_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("exec('x = PLAIN', SUB.__dict__, loc)")
        _assert_records(
            self, module, {"part": home.K},
            "r28 1392 exec foreign plain wf",
        )


class TestRuling1393GetattrSecondHop(unittest.TestCase):
    """Ruling 1393: the getattr act at a second hop target."""

    def test_1393_getattr_second_hop_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home("getattr(OUTER.INNER, 'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1393 getattr second hop wf",
        )

    def test_1393_getattr_direct_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(SUB, 'HELD')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1393 getattr direct wf",
        )

    def test_1393_getattr_second_hop_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home("getattr(OUTER.INNER, 'PLAIN')")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r28 1393 getattr plain wf",
        )


class TestRuling1394VarsSecondHop(unittest.TestCase):
    """Ruling 1394: the vars act at a second hop target."""

    def test_1394_vars_second_hop_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home("vars(OUTER.INNER)['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1394 vars second hop wf",
        )

    def test_1394_vars_direct_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return vars(SUB)['HELD']\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1394 vars direct wf",
        )

    def test_1394_vars_second_hop_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home("vars(OUTER.INNER)['PLAIN']")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r28 1394 vars plain wf",
        )


class TestRuling1395GetattrBuiltinsForm(unittest.TestCase):
    """Ruling 1395: the getattr act in builtins attribute form."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "import builtins\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1395_builtins_getattr_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("builtins.getattr(SUB, 'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1395 builtins getattr wf",
        )

    def test_1395_plain_getattr_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, 'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1395 plain getattr wf",
        )

    def test_1395_builtins_getattr_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("builtins.getattr(SUB, 'PLAIN')")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r28 1395 builtins plain wf",
        )


class TestRuling1396VarsBuiltinsForm(unittest.TestCase):
    """Ruling 1396: the vars act in builtins attribute form."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "import builtins\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1396_builtins_vars_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("builtins.vars(SUB)['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1396 builtins vars wf",
        )

    def test_1396_plain_vars_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1396 plain vars wf",
        )

    def test_1396_builtins_vars_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("builtins.vars(SUB)['PLAIN']")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r28 1396 builtins plain wf",
        )


class TestRuling1397DefaultArgumentCarried(unittest.TestCase):
    """Ruling 1397: a name or code string in a default argument."""

    def test_1397_exec_default_code_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self, code='x = HELD'):\n"
            "        loc = {}\n"
            "        exec(code, globals(), loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1397 exec default wf",
        )

    def test_1397_globals_index_default_name_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self, name='HELD'):\n"
            "        return globals()[name]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1397 index default wf",
        )

    def test_1397_exec_default_plain_code_still_records(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "PLAIN = 7\n"
            "class K:\n"
            "    def method(self, code='x = PLAIN'):\n"
            "        loc = {}\n"
            "        exec(code, globals(), loc)\n"
            "        return loc['x']\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r28 1397 exec plain default wf",
        )

    def test_1397_constant_exec_still_refused(self):
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
            self, module, {"part": Holder(home.K)},
            "r28 1397 constant exec wf",
        )


class TestRuling1398ExecBuiltinsForm(unittest.TestCase):
    """Ruling 1398: the exec act in builtins attribute form."""

    def _home(self, method_body, extra=""):
        return _make_module(
            "import builtins\n"
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            + extra
            + "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        %s\n"
            "        return loc['x']\n" % method_body
        )

    def test_1398_builtins_exec_carried_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "builtins.exec(CODE, globals(), loc)",
            "CODE = 'x = HELD'\n",
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1398 builtins exec wf",
        )

    def test_1398_plain_exec_carried_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "exec(CODE, globals(), loc)",
            "CODE = 'x = HELD'\n",
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r28 1398 plain exec wf",
        )

    def test_1398_builtins_exec_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "builtins.exec(PCODE, globals(), loc)",
            "PCODE = 'x = PLAIN'\n",
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r28 1398 builtins plain wf",
        )
