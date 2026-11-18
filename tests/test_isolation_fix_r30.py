"""Fix round 30 tests for rulings 1582 to 1595, Region 5.

Written test first against the governing base form of
ontoloop/consumption.py. Each ruling stands pinned at both
poles in the form its triage ruling states: the defective
forms stand decided in substance after the cure, and the
standing poles and clean controls its ruling names stand
in their standing forms at both poles.
"""

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


def _assert_refused_both(case, module, service, bundle, workflow):
    _assert_refused(case, module, bundle, workflow)
    found = service.discover_tool(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _assert_records(case, module, bundle, workflow):
    recorded = module.record_promotion(workflow, bundle)
    case.assertTrue(recorded["recorded"])
    return recorded


_counter = [0]


def _make_module(body, name_hint="r30_region5_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r30_region5_sub")


def _chain_home(source):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r30_region5_inner",
    )
    outer = _make_module("", "r30_region5_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(source)
    home.__dict__["OUTER"] = outer
    return home


def _exec_chain_home(code_expr, globals_expr, extra=""):
    source = (
        extra
        + "class K:\n"
        "    def method(self):\n"
        "        loc = {}\n"
        "        exec(%s, %s, loc)\n"
        "        return loc['x']\n" % (code_expr, globals_expr)
    )
    return _chain_home(source)


class TestRuling1582ExecSecondHopChair(unittest.TestCase):
    """Ruling 1582: the exec act at a second hop, Chair scope."""

    def test_1582_chain_constant_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _exec_chain_home("'x = HELD'", "OUTER.INNER.__dict__")
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r30 1582 chain constant wf",
        )

    def test_1582_chain_variable_refused(self):
        module = require("ontoloop.consumption")
        home = _exec_chain_home(
            "CODE", "OUTER.INNER.__dict__", "CODE = 'x = HELD'\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1582 chain variable wf",
        )

    def test_1582_chain_default_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, code='x = HELD'):\n"
            "        loc = {}\n"
            "        exec(code, OUTER.INNER.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1582 chain default wf",
        )

    def test_1582_chain_closure_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "def _factory(code):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            loc = {}\n"
            "            exec(code, OUTER.INNER.__dict__, loc)\n"
            "            return loc['x']\n"
            "    return K\n"
            "K = _factory('x = HELD')\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1582 chain closure wf",
        )

    def test_1582_chain_builtins_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "import builtins\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        builtins.exec('x = HELD', OUTER.INNER.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1582 chain builtins wf",
        )

    def test_1582_subscript_constant_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _exec_chain_home(
            "'x = HELD'", "OUTER.__dict__['INNER'].__dict__"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r30 1582 subscript constant wf",
        )

    def test_1582_first_hop_constant_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1582 first hop wf",
        )

    def test_1582_chain_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _exec_chain_home("'x = PLAIN'", "OUTER.INNER.__dict__")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1582 chain plain wf",
        )


class TestRuling1583DictSubscriptTargetChair(unittest.TestCase):
    """Ruling 1583: acts on a module reached by a dict subscript."""

    def _home(self, method_body):
        return _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def test_1583_getattr_subscript_target_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home("getattr(OUTER.__dict__['INNER'], 'HELD')")
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r30 1583 getattr wf",
        )

    def test_1583_vars_subscript_target_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(OUTER.__dict__['INNER'])['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1583 vars wf",
        )

    def test_1583_dict_subscript_target_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("OUTER.__dict__['INNER'].__dict__['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1583 dict wf",
        )

    def test_1583_chain_getattr_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.INNER, 'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1583 chain getattr wf",
        )

    def test_1583_getattr_subscript_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.__dict__['INNER'], 'PLAIN')")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1583 plain wf",
        )


class TestRuling1584GetattrTargetChair(unittest.TestCase):
    """Ruling 1584: acts on a module reached by a getattr act."""

    def _home(self, method_body):
        return _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def test_1584_getattr_result_getattr_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home("getattr(getattr(OUTER, 'INNER'), 'HELD')")
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r30 1584 getattr wf",
        )

    def test_1584_getattr_result_dict_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER, 'INNER').__dict__['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1584 dict wf",
        )

    def test_1584_direct_getattr_still_refused(self):
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
            "r30 1584 direct wf",
        )

    def test_1584_getattr_result_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(getattr(OUTER, 'INNER'), 'PLAIN')")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1584 plain wf",
        )


class TestRuling1585ReturnedNameCodeHome(unittest.TestCase):
    """Ruling 1585: a name or code string returned by a called function."""

    def _home(self, method_source):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _name():\n"
            "    return 'HELD'\n"
            "def _code():\n"
            "    return 'x = HELD'\n"
            "def _plain_name():\n"
            "    return 'PLAIN'\n"
            "class K:\n"
            + method_source
        )

    def test_1585_globals_index_returned_name_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return globals()[_name()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1585 returned name wf",
        )

    def test_1585_exec_returned_code_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(_code(), globals(), loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1585 returned code wf",
        )

    def test_1585_default_name_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self, n='HELD'):\n"
            "        return globals()[n]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1585 default name wf",
        )

    def test_1585_constant_code_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', globals(), loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1585 constant code wf",
        )

    def test_1585_returned_plain_name_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return globals()[_plain_name()]\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1585 returned plain wf",
        )


class TestRuling1586ReturnedNameForeignActs(unittest.TestCase):
    """Ruling 1586: a returned name at a foreign module act."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "def _name():\n"
            "    return 'HELD'\n"
            "def _plain_name():\n"
            "    return 'PLAIN'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1586_getattr_returned_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, _name())")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1586 getattr wf",
        )

    def test_1586_vars_returned_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)[_name()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1586 vars wf",
        )

    def test_1586_dict_returned_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[_name()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1586 dict wf",
        )

    def test_1586_getattr_variable_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "NAME = 'HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(SUB, NAME)\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1586 variable wf",
        )

    def test_1586_getattr_returned_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, _plain_name())")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1586 plain wf",
        )


class TestRuling1587ReturnedCodeForeignExec(unittest.TestCase):
    """Ruling 1587: a returned code string at a foreign exec act."""

    def _home(self, method_source, extra=""):
        sub = _sub_module()
        home = _make_module(
            extra
            + "def _code():\n"
            "    return 'x = HELD'\n"
            "def _plain_code():\n"
            "    return 'x = PLAIN'\n"
            "class K:\n"
            + method_source
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1587_exec_returned_code_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(_code(), SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1587 returned code wf",
        )

    def test_1587_exec_carried_code_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(CODE, SUB.__dict__, loc)\n"
            "        return loc['x']\n",
            "CODE = 'x = HELD'\n",
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1587 carried code wf",
        )

    def test_1587_exec_returned_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(_plain_code(), SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1587 plain code wf",
        )


class TestRuling1588BytesDefaultGetattr(unittest.TestCase):
    """Ruling 1588: a bytes carried name in a default argument."""

    def test_1588_getattr_bytes_default_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, raw=b'HELD'):\n"
            "        return getattr(SUB, raw.decode())\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1588 bytes default wf",
        )

    def test_1588_getattr_string_default_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return getattr(SUB, n)\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1588 string default wf",
        )

    def test_1588_globals_bytes_default_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self, raw=b'HELD'):\n"
            "        return globals()[raw.decode()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1588 globals bytes wf",
        )

    def test_1588_getattr_bytes_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, raw=b'PLAIN'):\n"
            "        return getattr(SUB, raw.decode())\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1588 bytes plain wf",
        )


class TestRuling1589BytesClosureGetattr(unittest.TestCase):
    """Ruling 1589: a bytes carried name in a closure cell."""

    def _home(self, factory_arg):
        sub = _sub_module()
        home = _make_module(
            "def _factory(raw):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            return getattr(SUB, raw.decode())\n"
            "    return K\n"
            "K = _factory(%s)\n" % factory_arg
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1589_getattr_bytes_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("b'HELD'")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1589 bytes closure wf",
        )

    def test_1589_getattr_string_closure_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("'HELD'")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1589 string closure wf",
        )

    def test_1589_getattr_bytes_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("b'PLAIN'")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1589 bytes plain wf",
        )


class TestRuling1590ModuleAttributeName(unittest.TestCase):
    """Ruling 1590: a name standing as an attribute of the target module."""

    def _sub(self):
        return _sub_module(
            "import threading\n"
            "PLAIN = 7\n"
            "HELD = threading.Lock()\n"
            "NAMEKEY = 'HELD'\n"
            "PLAINKEY = 'PLAIN'\n"
        )

    def _home(self, method_body, extra=""):
        sub = self._sub()
        home = _make_module(
            extra
            + "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1590_getattr_module_attribute_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, SUB.NAMEKEY)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1590 getattr wf",
        )

    def test_1590_dict_module_attribute_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[SUB.NAMEKEY]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1590 dict wf",
        )

    def test_1590_getattr_variable_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(SUB, NAME)", "NAME = 'HELD'\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r30 1590 variable wf",
        )

    def test_1590_getattr_module_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, SUB.PLAINKEY)")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r30 1590 plain wf",
        )


class TestRuling1591IsolationExecSecondHop(unittest.TestCase):
    """Ruling 1591: the exec act at a second hop, isolation scope."""

    def _check(self, module, home, label):
        _assert_refused(
            self, module, {"part": home.K}, label + " class wf"
        )
        _assert_refused(
            self, module, {"part": home.K()}, label + " instance wf"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            label + " holder wf",
        )

    def test_1591_chain_constant_refused(self):
        module = require("ontoloop.consumption")
        home = _exec_chain_home("'x = HELD'", "OUTER.INNER.__dict__")
        self._check(module, home, "r30 1591 constant")

    def test_1591_chain_variable_refused(self):
        module = require("ontoloop.consumption")
        home = _exec_chain_home(
            "CODE", "OUTER.INNER.__dict__", "CODE = 'x = HELD'\n"
        )
        self._check(module, home, "r30 1591 variable")

    def test_1591_chain_default_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, code='x = HELD'):\n"
            "        loc = {}\n"
            "        exec(code, OUTER.INNER.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        self._check(module, home, "r30 1591 default")

    def test_1591_chain_closure_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "def _factory(code):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            loc = {}\n"
            "            exec(code, OUTER.INNER.__dict__, loc)\n"
            "            return loc['x']\n"
            "    return K\n"
            "K = _factory('x = HELD')\n"
        )
        self._check(module, home, "r30 1591 closure")

    def test_1591_subscript_constant_refused(self):
        module = require("ontoloop.consumption")
        home = _exec_chain_home(
            "'x = HELD'", "OUTER.__dict__['INNER'].__dict__"
        )
        self._check(module, home, "r30 1591 subscript")

    def test_1591_first_hop_constant_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K},
            "r30 1591 first hop wf",
        )

    def test_1591_chain_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _exec_chain_home("'x = PLAIN'", "OUTER.INNER.__dict__")
        _assert_records(
            self, module, {"part": home.K},
            "r30 1591 plain wf",
        )


class TestRuling1592IsolationSubscriptTarget(unittest.TestCase):
    """Ruling 1592: acts on a subscript reached module, isolation."""

    def _home(self, method_body):
        return _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def _check(self, module, home, label):
        _assert_refused(
            self, module, {"part": home.K}, label + " class wf"
        )
        _assert_refused(
            self, module, {"part": home.K()}, label + " instance wf"
        )

    def test_1592_getattr_subscript_target_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.__dict__['INNER'], 'HELD')")
        self._check(module, home, "r30 1592 getattr")

    def test_1592_vars_subscript_target_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(OUTER.__dict__['INNER'])['HELD']")
        self._check(module, home, "r30 1592 vars")

    def test_1592_dict_subscript_target_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("OUTER.__dict__['INNER'].__dict__['HELD']")
        self._check(module, home, "r30 1592 dict")

    def test_1592_chain_getattr_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.INNER, 'HELD')")
        _assert_refused(
            self, module, {"part": home.K},
            "r30 1592 chain getattr wf",
        )

    def test_1592_getattr_subscript_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.__dict__['INNER'], 'PLAIN')")
        _assert_records(
            self, module, {"part": home.K},
            "r30 1592 plain wf",
        )


class TestRuling1593IsolationGetattrTarget(unittest.TestCase):
    """Ruling 1593: acts on a getattr reached module, isolation."""

    def _home(self, method_body):
        return _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def _check(self, module, home, label):
        _assert_refused(
            self, module, {"part": home.K}, label + " class wf"
        )
        _assert_refused(
            self, module, {"part": home.K()}, label + " instance wf"
        )

    def test_1593_getattr_result_getattr_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(getattr(OUTER, 'INNER'), 'HELD')")
        self._check(module, home, "r30 1593 getattr")

    def test_1593_getattr_result_dict_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER, 'INNER').__dict__['HELD']")
        self._check(module, home, "r30 1593 dict")

    def test_1593_chain_getattr_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.INNER, 'HELD')")
        _assert_refused(
            self, module, {"part": home.K},
            "r30 1593 chain getattr wf",
        )

    def test_1593_getattr_result_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(getattr(OUTER, 'INNER'), 'PLAIN')")
        _assert_records(
            self, module, {"part": home.K},
            "r30 1593 plain wf",
        )


class TestRuling1594IsolationVarsSubscriptTarget(unittest.TestCase):
    """Ruling 1594: acts on a vars subscript reached module."""

    def _home(self, method_body):
        return _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def _check(self, module, home, label):
        _assert_refused(
            self, module, {"part": home.K}, label + " class wf"
        )
        _assert_refused(
            self, module, {"part": home.K()}, label + " instance wf"
        )

    def test_1594_getattr_vars_target_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(vars(OUTER)['INNER'], 'HELD')")
        self._check(module, home, "r30 1594 getattr")

    def test_1594_vars_vars_target_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(vars(OUTER)['INNER'])['HELD']")
        self._check(module, home, "r30 1594 vars")

    def test_1594_dict_vars_target_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(OUTER)['INNER'].__dict__['HELD']")
        self._check(module, home, "r30 1594 dict")

    def test_1594_direct_getattr_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(SUB, 'HELD')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K},
            "r30 1594 direct wf",
        )

    def test_1594_getattr_vars_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(vars(OUTER)['INNER'], 'PLAIN')")
        _assert_records(
            self, module, {"part": home.K},
            "r30 1594 plain wf",
        )


class TestRuling1595IsolationGetattribute(unittest.TestCase):
    """Ruling 1595: the getattribute act of a class namespace member."""

    def _check(self, module, home, label):
        _assert_refused(
            self, module, {"part": home.K}, label + " class wf"
        )
        _assert_refused(
            self, module, {"part": home.K()}, label + " instance wf"
        )

    def test_1595_getattribute_literal_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return SUB.__getattribute__('HELD')\n"
        )
        home.__dict__["SUB"] = sub
        self._check(module, home, "r30 1595 literal")

    def test_1595_getattribute_default_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return SUB.__getattribute__(n)\n"
        )
        home.__dict__["SUB"] = sub
        self._check(module, home, "r30 1595 default")

    def test_1595_getattribute_second_hop_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return OUTER.INNER.__getattribute__('HELD')\n"
        )
        self._check(module, home, "r30 1595 second hop")

    def test_1595_getattr_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(SUB, 'HELD')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K},
            "r30 1595 getattr wf",
        )

    def test_1595_getattribute_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return SUB.__getattribute__('PLAIN')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": home.K},
            "r30 1595 plain wf",
        )
