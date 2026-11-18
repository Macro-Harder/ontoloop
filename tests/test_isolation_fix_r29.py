"""Fix round 29 tests for rulings 1483 to 1497, Region 5.

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


def _make_module(body, name_hint="r29_region5_mod"):
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
    return _make_module(body, "r29_region5_sub")


def _chain_home(method_body, extra=""):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r29_region5_inner",
    )
    outer = _make_module("", "r29_region5_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(
        extra
        + "class K:\n"
        "    def method(self):\n"
        "        return %s\n" % method_body
    )
    home.__dict__["OUTER"] = outer
    return home


def _stdlib_file(filename):
    return os.path.join(os.path.dirname(os.__file__), filename)


class TestRuling1483GateGenuineModuleStanding(unittest.TestCase):
    """Ruling 1483: a file claim whose genuine module stands unloaded."""

    def _fake_module(self, dotted_name, file_value, genuine_name):
        saved = sys.modules.pop(genuine_name, None)
        if saved is not None:
            self.addCleanup(
                sys.modules.__setitem__, genuine_name, saved
            )
        module = types.ModuleType(dotted_name)
        module.__file__ = file_value
        sys.modules[dotted_name] = module
        self.addCleanup(sys.modules.pop, dotted_name, None)
        exec(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n",
            module.__dict__,
        )
        return module

    def test_1483_dotted_colorsys_claim_refused(self):
        module = require("ontoloop.consumption")
        fake = self._fake_module(
            "r29fakepkg.colorsys",
            _stdlib_file("colorsys.py"),
            "colorsys",
        )
        _assert_refused(
            self, module, {"part": Holder(fake.K)},
            "r29 1483 dotted colorsys wf",
        )

    def test_1483_dotted_antigravity_claim_refused(self):
        module = require("ontoloop.consumption")
        fake = self._fake_module(
            "r29fakepkg.antigravity",
            _stdlib_file("antigravity.py"),
            "antigravity",
        )
        _assert_refused(
            self, module, {"part": Holder(fake.K)},
            "r29 1483 dotted antigravity wf",
        )

    def test_1483_fake_claim_on_os_file_still_refused(self):
        module = require("ontoloop.consumption")
        _counter[0] += 1
        name = "r29_region5_fake_%d" % _counter[0]
        fake = types.ModuleType(name)
        fake.__file__ = os.__file__
        sys.modules[name] = fake
        self.addCleanup(sys.modules.pop, name, None)
        exec(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n",
            fake.__dict__,
        )
        _assert_refused(
            self, module, {"part": Holder(fake.K)},
            "r29 1483 fake os file wf",
        )

    def test_1483_fake_claim_no_file_still_refused(self):
        module = require("ontoloop.consumption")
        _counter[0] += 1
        name = "r29_region5_fake_%d" % _counter[0]
        fake = types.ModuleType(name)
        fake.__file__ = _stdlib_file("no_such_file_r29_region5.py")
        sys.modules[name] = fake
        self.addCleanup(sys.modules.pop, name, None)
        exec(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n",
            fake.__dict__,
        )
        _assert_refused(
            self, module, {"part": Holder(fake.K)},
            "r29 1483 fake no file wf",
        )

    def test_1483_genuine_stdlib_function_still_records(self):
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
            "r29 1483 stdlib function wf",
        )

    def test_1483_null_handler_still_records_apart(self):
        module = require("ontoloop.consumption")
        recorded = _assert_records(
            self, module,
            {"part": Holder(logging.NullHandler())},
            "r29 1483 null handler wf",
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsInstance(copied, logging.NullHandler)


class TestRuling1484DictSubscriptSecondHop(unittest.TestCase):
    """Ruling 1484: a dictionary subscript at a second hop."""

    def test_1484_second_hop_literal_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home("OUTER.INNER.__dict__['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1484 second hop literal wf",
        )

    def test_1484_second_hop_variable_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "OUTER.INNER.__dict__[KEY]", "KEY = 'HELD'\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1484 second hop variable wf",
        )

    def test_1484_direct_dict_literal_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return SUB.__dict__['HELD']\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1484 direct dict wf",
        )

    def test_1484_second_hop_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home("OUTER.INNER.__dict__['PLAIN']")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r29 1484 second hop plain wf",
        )


class TestRuling1485DefaultNameForeignModule(unittest.TestCase):
    """Ruling 1485: a default carried name applied to a foreign module."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1485_getattr_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, n)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1485 getattr default wf",
        )

    def test_1485_dict_subscript_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[n]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1485 dict default wf",
        )

    def test_1485_globals_index_default_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return globals()[n]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1485 index default wf",
        )

    def test_1485_getattr_default_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='PLAIN'):\n"
            "        return getattr(SUB, n)\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r29 1485 getattr plain wf",
        )


class TestRuling1486GetattrDefaultHomeModule(unittest.TestCase):
    """Ruling 1486: the getattr act under a default carried name."""

    def _home(self, signature, method_body):
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, %s):\n"
            "        return %s\n" % (signature, method_body)
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1486_getattr_positional_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("n='HELD'", "getattr(SUB, n)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1486 getattr positional wf",
        )

    def test_1486_getattr_kwonly_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("*, n='HELD'", "getattr(SUB, n)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1486 getattr kwonly wf",
        )

    def test_1486_getattr_second_hop_default_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "getattr(OUTER.INNER, n)",
        )
        home2 = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return getattr(OUTER.INNER, n)\n"
        )
        home2.__dict__["OUTER"] = home.__dict__["OUTER"]
        _assert_refused(
            self, module, {"part": Holder(home2.K)},
            "r29 1486 getattr second hop wf",
        )


class TestRuling1487VarsDefaultHomeModule(unittest.TestCase):
    """Ruling 1487: the vars act under a default carried name."""

    def test_1487_vars_default_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return vars(SUB)[n]\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1487 vars default wf",
        )

    def test_1487_vars_direct_literal_still_refused(self):
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
            "r29 1487 vars literal wf",
        )

    def test_1487_vars_default_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='PLAIN'):\n"
            "        return vars(SUB)[n]\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r29 1487 vars plain wf",
        )


class TestRuling1488DictDefaultHomeModule(unittest.TestCase):
    """Ruling 1488: a dictionary subscript under a default carried name."""

    def test_1488_dict_default_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return SUB.__dict__[n]\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1488 dict default wf",
        )

    def test_1488_dict_variable_key_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "KEY = 'HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return SUB.__dict__[KEY]\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1488 dict variable wf",
        )

    def test_1488_dict_default_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='PLAIN'):\n"
            "        return SUB.__dict__[n]\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r29 1488 dict plain wf",
        )


class TestRuling1489ClosureCarriedHome(unittest.TestCase):
    """Ruling 1489: a name or code string carried in a closure cell."""

    def test_1489_closure_code_exec_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "def _factory(code):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            loc = {}\n"
            "            exec(code, globals(), loc)\n"
            "            return loc['x']\n"
            "    return K\n"
            "K = _factory('x = HELD')\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1489 closure code wf",
        )

    def test_1489_closure_name_globals_index_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "def _factory(nm):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            return globals()[nm]\n"
            "    return K\n"
            "K = _factory('HELD')\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1489 closure name wf",
        )

    def test_1489_closure_code_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "PLAIN = 7\n"
            "def _factory(code):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            loc = {}\n"
            "            exec(code, globals(), loc)\n"
            "            return loc['x']\n"
            "    return K\n"
            "K = _factory('x = PLAIN')\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r29 1489 closure plain wf",
        )

    def test_1489_default_name_index_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return globals()[n]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1489 default index wf",
        )

    def test_1489_constant_exec_still_refused(self):
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
            "r29 1489 constant exec wf",
        )


class TestRuling1490ClosureNameForeignActs(unittest.TestCase):
    """Ruling 1490: dynamic acts on a foreign module, closure name."""

    def _home(self, method_body, held_name="HELD"):
        sub = _sub_module()
        home = _make_module(
            "def _factory(nm):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            return %s\n"
            "    return K\n"
            "K = _factory('%s')\n" % (method_body, held_name)
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1490_getattr_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, nm)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1490 getattr closure wf",
        )

    def test_1490_vars_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)[nm]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1490 vars closure wf",
        )

    def test_1490_dict_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[nm]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1490 dict closure wf",
        )

    def test_1490_getattr_closure_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, nm)", "PLAIN")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r29 1490 getattr plain wf",
        )


class TestRuling1491ExecForeignClosureCode(unittest.TestCase):
    """Ruling 1491: the exec act, foreign globals, closure code string."""

    def test_1491_exec_foreign_closure_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "def _factory(code):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            loc = {}\n"
            "            exec(code, SUB.__dict__, loc)\n"
            "            return loc['x']\n"
            "    return K\n"
            "K = _factory('x = HELD')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1491 exec closure wf",
        )

    def test_1491_exec_foreign_carried_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "CODE = 'x = HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(CODE, SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r29 1491 exec carried wf",
        )

    def test_1491_exec_foreign_closure_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "def _factory(code):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            loc = {}\n"
            "            exec(code, SUB.__dict__, loc)\n"
            "            return loc['x']\n"
            "    return K\n"
            "K = _factory('x = PLAIN')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r29 1491 exec plain wf",
        )


class TestRuling1492IsolationSecondHopDict(unittest.TestCase):
    """Ruling 1492: a dictionary subscript at a second hop, isolation."""

    def test_1492_second_hop_literal_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home("OUTER.INNER.__dict__['HELD']")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1492 literal class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r29 1492 literal instance wf",
        )

    def test_1492_second_hop_variable_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "OUTER.INNER.__dict__[KEY]", "KEY = 'HELD'\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1492 variable class wf",
        )

    def test_1492_direct_dict_literal_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return SUB.__dict__['HELD']\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1492 direct dict wf",
        )

    def test_1492_second_hop_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home("OUTER.INNER.__dict__['PLAIN']")
        _assert_records(
            self, module, {"part": home.K},
            "r29 1492 second hop plain wf",
        )


class TestRuling1493IsolationDefaultForeignActs(unittest.TestCase):
    """Ruling 1493: class namespace acts under a default carried name."""

    def _home(self, method_body):
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1493_getattr_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, n)")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1493 getattr class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r29 1493 getattr instance wf",
        )

    def test_1493_vars_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)[n]")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1493 vars class wf",
        )

    def test_1493_dict_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[n]")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1493 dict class wf",
        )

    def test_1493_getattr_variable_still_refused(self):
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
            self, module, {"part": home.K},
            "r29 1493 getattr variable wf",
        )

    def test_1493_getattr_default_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='PLAIN'):\n"
            "        return getattr(SUB, n)\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": home.K},
            "r29 1493 getattr plain wf",
        )


class TestRuling1494IsolationClosureForeignActs(unittest.TestCase):
    """Ruling 1494: class namespace acts under a closure carried name."""

    def _home(self, method_body, held_name="HELD"):
        sub = _sub_module()
        home = _make_module(
            "def _factory(nm):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            return %s\n"
            "    return K\n"
            "K = _factory('%s')\n" % (method_body, held_name)
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1494_getattr_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, nm)")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1494 getattr class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r29 1494 getattr instance wf",
        )

    def test_1494_dict_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[nm]")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1494 dict class wf",
        )

    def test_1494_getattr_variable_still_refused(self):
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
            self, module, {"part": home.K},
            "r29 1494 getattr variable wf",
        )

    def test_1494_getattr_closure_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, nm)", "PLAIN")
        _assert_records(
            self, module, {"part": home.K},
            "r29 1494 getattr plain wf",
        )


class TestRuling1495IsolationExecClosureForeign(unittest.TestCase):
    """Ruling 1495: class namespace exec, foreign globals, closure code."""

    def test_1495_exec_closure_foreign_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "def _factory(code):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            loc = {}\n"
            "            exec(code, SUB.__dict__, loc)\n"
            "            return loc['x']\n"
            "    return K\n"
            "K = _factory('x = HELD')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1495 exec class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r29 1495 exec instance wf",
        )

    def test_1495_exec_default_foreign_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, code='x = HELD'):\n"
            "        loc = {}\n"
            "        exec(code, SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1495 exec default wf",
        )

    def test_1495_exec_closure_foreign_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "def _factory(code):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            loc = {}\n"
            "            exec(code, SUB.__dict__, loc)\n"
            "            return loc['x']\n"
            "    return K\n"
            "K = _factory('x = PLAIN')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": home.K},
            "r29 1495 exec plain wf",
        )


class TestRuling1496IsolationClosureHomeActs(unittest.TestCase):
    """Ruling 1496: globals index and eval under a closure carried name."""

    def _home(self, method_body, held_name="HELD"):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _factory(nm):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            return %s\n"
            "    return K\n"
            "K = _factory('%s')\n" % (method_body, held_name)
        )

    def test_1496_globals_index_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[nm]")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1496 index class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r29 1496 index instance wf",
        )

    def test_1496_eval_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("eval(nm)")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1496 eval class wf",
        )

    def test_1496_eval_variable_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "NAME = 'HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return eval(NAME)\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1496 eval variable wf",
        )

    def test_1496_globals_index_closure_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[nm]", "PLAIN")
        _assert_records(
            self, module, {"part": home.K},
            "r29 1496 index plain wf",
        )


class TestRuling1497IsolationSecondHopDefault(unittest.TestCase):
    """Ruling 1497: the getattr act at a second hop, default carried name."""

    def test_1497_second_hop_getattr_default_refused(self):
        module = require("ontoloop.consumption")
        inner_home = _chain_home("getattr(OUTER.INNER, 'HELD')")
        home = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return getattr(OUTER.INNER, n)\n"
        )
        home.__dict__["OUTER"] = inner_home.__dict__["OUTER"]
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1497 chain class wf",
        )
        _assert_refused(
            self, module, {"part": home.K()},
            "r29 1497 chain instance wf",
        )

    def test_1497_second_hop_getattr_literal_still_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home("getattr(OUTER.INNER, 'HELD')")
        _assert_refused(
            self, module, {"part": home.K},
            "r29 1497 chain literal wf",
        )

    def test_1497_second_hop_getattr_default_plain_records(self):
        module = require("ontoloop.consumption")
        inner_home = _chain_home("getattr(OUTER.INNER, 'PLAIN')")
        home = _make_module(
            "class K:\n"
            "    def method(self, n='PLAIN'):\n"
            "        return getattr(OUTER.INNER, n)\n"
        )
        home.__dict__["OUTER"] = inner_home.__dict__["OUTER"]
        _assert_records(
            self, module, {"part": home.K},
            "r29 1497 chain plain wf",
        )
