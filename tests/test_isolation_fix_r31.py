"""Fix round 31 tests for rulings 1689 to 1711, Region 5.

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


def _make_module(body, name_hint="r31_region5_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r31_region5_sub")


def _chain_home(source):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r31_region5_inner",
    )
    outer = _make_module("", "r31_region5_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(source)
    home.__dict__["OUTER"] = outer
    return home


def _home_with_sub(method_body, extra=""):
    sub = _sub_module()
    home = _make_module(
        extra
        + "class K:\n"
        "    def method(self):\n"
        "        return %s\n" % method_body
    )
    home.__dict__["SUB"] = sub
    return home


def _check3(case, module, home, label):
    _assert_refused(
        case, module, {"part": home.K}, label + " class wf"
    )
    _assert_refused(
        case, module, {"part": home.K()}, label + " instance wf"
    )
    _assert_refused(
        case, module, {"part": Holder(home.K)},
        label + " holder wf",
    )


class TestRuling1689ExecCallResultChair(unittest.TestCase):
    """Ruling 1689: exec with a foreign mapping standing as a call result."""

    def _home(self, globals_expr, code_expr="'x = HELD'", extra=""):
        return _chain_home(
            extra
            + "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(%s, %s, loc)\n"
            "        return loc['x']\n" % (code_expr, globals_expr)
        )

    def test_1689_getattr_result_constant_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home("getattr(OUTER, 'INNER').__dict__")
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r31 1689 getattr result wf",
        )

    def test_1689_vars_subscript_result_constant_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home("vars(OUTER)['INNER'].__dict__")
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r31 1689 vars result wf",
        )

    def test_1689_dict_get_result_constant_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home("OUTER.__dict__.get('INNER').__dict__")
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r31 1689 dict get result wf",
        )

    def test_1689_getattr_result_variable_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(OUTER, 'INNER').__dict__", "CODE",
            "CODE = 'x = HELD'\n",
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1689 getattr variable wf",
        )

    def test_1689_chain_constant_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("OUTER.INNER.__dict__")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1689 chain wf",
        )

    def test_1689_getattr_result_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(OUTER, 'INNER').__dict__", "'x = PLAIN'"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1689 plain wf",
        )


class TestRuling1690DictGetTargetChair(unittest.TestCase):
    """Ruling 1690: acts on a module standing as a dict get result."""

    def _home(self, method_body):
        return _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def test_1690_getattr_dict_get_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home(
            "getattr(OUTER.__dict__.get('INNER'), 'HELD')"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r31 1690 getattr wf",
        )

    def test_1690_vars_dict_get_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(OUTER.__dict__.get('INNER'))['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1690 vars wf",
        )

    def test_1690_dict_dict_get_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "OUTER.__dict__.get('INNER').__dict__['HELD']"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1690 dict wf",
        )

    def test_1690_subscript_target_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.__dict__['INNER'], 'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1690 subscript wf",
        )

    def test_1690_getattr_dict_get_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(OUTER.__dict__.get('INNER'), 'PLAIN')"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1690 plain wf",
        )


class TestRuling1691BytearrayDefault(unittest.TestCase):
    """Ruling 1691: a bytearray carried name in a default argument."""

    def _home(self, method_source):
        sub = _sub_module()
        home = _make_module(
            "class K:\n" + method_source
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1691_getattr_bytearray_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self, raw=bytearray(b'HELD')):\n"
            "        return getattr(SUB, raw.decode())\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1691 getattr wf",
        )

    def test_1691_vars_bytearray_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self, raw=bytearray(b'HELD')):\n"
            "        return vars(SUB)[raw.decode()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1691 vars wf",
        )

    def test_1691_dict_bytearray_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self, raw=bytearray(b'HELD')):\n"
            "        return SUB.__dict__[raw.decode()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1691 dict wf",
        )

    def test_1691_getattr_bytes_default_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self, raw=b'HELD'):\n"
            "        return getattr(SUB, raw.decode())\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1691 bytes wf",
        )

    def test_1691_getattr_bytearray_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self, raw=bytearray(b'PLAIN')):\n"
            "        return getattr(SUB, raw.decode())\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1691 plain wf",
        )


class TestRuling1692BytearrayClosure(unittest.TestCase):
    """Ruling 1692: a bytearray carried name in a closure cell."""

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

    def test_1692_getattr_bytearray_closure_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("bytearray(b'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1692 bytearray closure wf",
        )

    def test_1692_getattr_bytes_closure_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("b'HELD'")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1692 bytes closure wf",
        )

    def test_1692_getattr_bytearray_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("bytearray(b'PLAIN')")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1692 plain wf",
        )


class TestRuling1693BytesConstantName(unittest.TestCase):
    """Ruling 1693: a name in a bytes constant of the member code."""

    def test_1693_getattr_bytes_constant_refused(self):
        module = require("ontoloop.consumption")
        home = _home_with_sub("getattr(SUB, b'HELD'.decode())")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1693 getattr wf",
        )

    def test_1693_vars_bytes_constant_refused(self):
        module = require("ontoloop.consumption")
        home = _home_with_sub("vars(SUB)[b'HELD'.decode()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1693 vars wf",
        )

    def test_1693_getattr_string_constant_still_refused(self):
        module = require("ontoloop.consumption")
        home = _home_with_sub("getattr(SUB, 'HELD')")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1693 string wf",
        )

    def test_1693_globals_bytes_constant_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()[b'HELD'.decode()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1693 globals wf",
        )

    def test_1693_getattr_bytes_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _home_with_sub("getattr(SUB, b'PLAIN'.decode())")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1693 plain wf",
        )


class TestRuling1694BytesMapValueName(unittest.TestCase):
    """Ruling 1694: a name in a bytes value of the map under decision."""

    def _home(self, method_body):
        return _home_with_sub(method_body, "KEYB = b'HELD'\n")

    def test_1694_getattr_bytes_map_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, KEYB.decode())")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1694 getattr wf",
        )

    def test_1694_vars_bytes_map_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(SUB)[KEYB.decode()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1694 vars wf",
        )

    def test_1694_getattr_string_map_still_refused(self):
        module = require("ontoloop.consumption")
        home = _home_with_sub(
            "getattr(SUB, KEY)", "KEY = 'HELD'\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1694 string wf",
        )

    def test_1694_getattr_bytes_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _home_with_sub(
            "getattr(SUB, KEYB.decode())", "KEYB = b'PLAIN'\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1694 plain wf",
        )


class TestRuling1695BytesConstantCodeHome(unittest.TestCase):
    """Ruling 1695: bytes constant code at the home exec act."""

    def _home(self, code_expr):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(%s, globals(), loc)\n"
            "        return loc['x']\n" % code_expr
        )

    def test_1695_exec_bytes_constant_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("b'x = HELD'")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1695 bytes code wf",
        )

    def test_1695_exec_string_constant_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("'x = HELD'")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1695 string code wf",
        )

    def test_1695_exec_bytes_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("b'x = PLAIN'")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1695 plain wf",
        )


class TestRuling1696BytesConstantCodeForeign(unittest.TestCase):
    """Ruling 1696: bytes constant code at the foreign exec act."""

    def _home(self, code_expr):
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(%s, SUB.__dict__, loc)\n"
            "        return loc['x']\n" % code_expr
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1696_exec_bytes_constant_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("b'x = HELD'")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1696 bytes code wf",
        )

    def test_1696_exec_string_constant_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("'x = HELD'")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1696 string code wf",
        )

    def test_1696_exec_bytes_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("b'x = PLAIN'")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1696 plain wf",
        )


class TestRuling1697ContainerNameHome(unittest.TestCase):
    """Ruling 1697: a container carried name at the home map."""

    def test_1697_globals_container_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "BOX = {'k': 'HELD'}\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()[BOX['k']]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1697 container wf",
        )

    def test_1697_globals_string_value_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "KEY = 'HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()[KEY]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1697 string wf",
        )

    def test_1697_globals_container_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "PLAIN = 7\n"
            "BOX = {'k': 'PLAIN'}\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()[BOX['k']]\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1697 plain wf",
        )


class TestRuling1698ContainerNameForeign(unittest.TestCase):
    """Ruling 1698: a container carried name at a foreign act."""

    def _home(self, method_body, box):
        return _home_with_sub(method_body, "BOX = %s\n" % box)

    def test_1698_getattr_dict_container_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(SUB, BOX['k'])", "{'k': 'HELD'}"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1698 dict wf",
        )

    def test_1698_getattr_list_container_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, BOX[0])", "['HELD']")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1698 list wf",
        )

    def test_1698_dict_dict_container_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "SUB.__dict__[BOX['k']]", "{'k': 'HELD'}"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1698 dict dict wf",
        )

    def test_1698_getattr_string_value_still_refused(self):
        module = require("ontoloop.consumption")
        home = _home_with_sub(
            "getattr(SUB, KEY)", "KEY = 'HELD'\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1698 string wf",
        )

    def test_1698_getattr_container_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(SUB, BOX['k'])", "{'k': 'PLAIN'}"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1698 plain wf",
        )


class TestRuling1699ContainerCodeHome(unittest.TestCase):
    """Ruling 1699: container carried code at the home exec act."""

    def _home(self, box, code_expr="BOX['k']"):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "BOX = %s\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(%s, globals(), loc)\n"
            "        return loc['x']\n" % (box, code_expr)
        )

    def test_1699_exec_container_code_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("{'k': 'x = HELD'}")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1699 container code wf",
        )

    def test_1699_exec_constant_code_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("{'k': 'x = PLAIN'}", "'x = HELD'")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1699 constant wf",
        )

    def test_1699_exec_container_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("{'k': 'x = PLAIN'}")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1699 plain wf",
        )


class TestRuling1700ContainerCodeForeign(unittest.TestCase):
    """Ruling 1700: container carried code at the foreign exec act."""

    def _home(self, extra, code_expr):
        sub = _sub_module()
        home = _make_module(
            extra
            + "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(%s, SUB.__dict__, loc)\n"
            "        return loc['x']\n" % code_expr
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1700_exec_container_code_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "BOX = {'k': 'x = HELD'}\n", "BOX['k']"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1700 container code wf",
        )

    def test_1700_exec_carried_code_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("CODE = 'x = HELD'\n", "CODE")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1700 carried wf",
        )

    def test_1700_exec_container_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "BOX = {'k': 'x = PLAIN'}\n", "BOX['k']"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1700 plain wf",
        )


class TestRuling1701SecondOrderNameHome(unittest.TestCase):
    """Ruling 1701: a second order returned name at the home map."""

    def _home(self, method_source, inner_return="'HELD'"):
        return _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _inner():\n"
            "    return " + inner_return + "\n"
            "def _outer():\n"
            "    return _inner()\n"
            "def _first():\n"
            "    return 'HELD'\n"
            "class K:\n"
            + method_source
        )

    def test_1701_globals_second_order_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return globals()[_outer()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1701 second order wf",
        )

    def test_1701_globals_first_order_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return globals()[_first()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1701 first order wf",
        )

    def test_1701_globals_second_order_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return globals()[_outer()]\n",
            "'PLAIN'",
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1701 plain wf",
        )


class TestRuling1702SecondOrderNameForeign(unittest.TestCase):
    """Ruling 1702: a second order returned name at a foreign act."""

    def _home(self, method_body, inner_return="'HELD'"):
        sub = _sub_module()
        home = _make_module(
            "def _inner():\n"
            "    return " + inner_return + "\n"
            "def _outer():\n"
            "    return _inner()\n"
            "def _first():\n"
            "    return 'HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1702_getattr_second_order_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, _outer())")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1702 getattr wf",
        )

    def test_1702_dict_second_order_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[_outer()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1702 dict wf",
        )

    def test_1702_getattr_first_order_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, _first())")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1702 first order wf",
        )

    def test_1702_getattr_second_order_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, _outer())", "'PLAIN'")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1702 plain wf",
        )


class TestRuling1703ThirdModuleAttributeName(unittest.TestCase):
    """Ruling 1703: a name standing as an attribute of a third module."""

    def _home(self, method_body, third_body=None):
        if third_body is None:
            third_body = "NAMEKEY = 'HELD'\nPLAINKEY = 'PLAIN'\n"
        sub = _sub_module()
        third = _make_module(third_body, "r31_region5_third")
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["SUB"] = sub
        home.__dict__["THIRD"] = third
        return home

    def test_1703_getattr_third_module_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, THIRD.NAMEKEY)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1703 getattr wf",
        )

    def test_1703_dict_third_module_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("SUB.__dict__[THIRD.NAMEKEY]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1703 dict wf",
        )

    def test_1703_getattr_target_attribute_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module(
            "import threading\n"
            "PLAIN = 7\n"
            "HELD = threading.Lock()\n"
            "NAMEKEY = 'HELD'\n"
        )
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(SUB, SUB.NAMEKEY)\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r31 1703 target attr wf",
        )

    def test_1703_getattr_third_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(SUB, THIRD.PLAINKEY)")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r31 1703 plain wf",
        )


class TestRuling1704IsolationDictGetTarget(unittest.TestCase):
    """Ruling 1704: acts on a dict get reached module, isolation."""

    def _home(self, method_body):
        return _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def test_1704_getattr_dict_get_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(OUTER.__dict__.get('INNER'), 'HELD')"
        )
        _check3(self, module, home, "r31 1704 getattr")

    def test_1704_vars_dict_get_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(OUTER.__dict__.get('INNER'))['HELD']")
        _check3(self, module, home, "r31 1704 vars")

    def test_1704_dict_dict_get_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "OUTER.__dict__.get('INNER').__dict__['HELD']"
        )
        _check3(self, module, home, "r31 1704 dict")

    def test_1704_subscript_target_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.__dict__['INNER'], 'HELD')")
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1704 subscript wf",
        )

    def test_1704_getattr_dict_get_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(OUTER.__dict__.get('INNER'), 'PLAIN')"
        )
        _assert_records(
            self, module, {"part": home.K},
            "r31 1704 plain wf",
        )


class TestRuling1705IsolationReturnedBytes(unittest.TestCase):
    """Ruling 1705: a name decoded from a returned bytes value."""

    def _home(self, method_source, name_return="b'HELD'",
              code_return="b'x = HELD'"):
        sub = _sub_module()
        home = _make_module(
            "def get_name():\n"
            "    return " + name_return + "\n"
            "def get_code():\n"
            "    return " + code_return + "\n"
            "def get_str():\n"
            "    return 'HELD'\n"
            "class K:\n"
            + method_source
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1705_getattr_returned_bytes_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, get_name().decode())\n"
        )
        _check3(self, module, home, "r31 1705 getattr")

    def test_1705_dict_returned_bytes_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return SUB.__dict__[get_name().decode()]\n"
        )
        _check3(self, module, home, "r31 1705 dict")

    def test_1705_exec_returned_bytes_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(get_code(), SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, home, "r31 1705 exec")

    def test_1705_getattr_returned_string_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, get_str())\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1705 string wf",
        )

    def test_1705_getattr_returned_bytes_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, get_name().decode())\n",
            "b'PLAIN'",
        )
        _assert_records(
            self, module, {"part": home.K},
            "r31 1705 plain wf",
        )


class TestRuling1706IsolationSecondOrder(unittest.TestCase):
    """Ruling 1706: a name returned at second order, isolation."""

    def _home(self, method_source, inner_return="'HELD'",
              inner_code="'x = HELD'"):
        sub = _sub_module()
        home = _make_module(
            "def inner_name():\n"
            "    return " + inner_return + "\n"
            "def outer_name():\n"
            "    return inner_name()\n"
            "def inner_code():\n"
            "    return " + inner_code + "\n"
            "def outer_code():\n"
            "    return inner_code()\n"
            "class K:\n"
            + method_source
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1706_getattr_second_order_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, outer_name())\n"
        )
        _check3(self, module, home, "r31 1706 getattr")

    def test_1706_dict_second_order_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return SUB.__dict__[outer_name()]\n"
        )
        _check3(self, module, home, "r31 1706 dict")

    def test_1706_exec_second_order_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(outer_code(), SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, home, "r31 1706 exec")

    def test_1706_getattr_first_order_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, inner_name())\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1706 first order wf",
        )

    def test_1706_getattr_second_order_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, outer_name())\n",
            "'PLAIN'",
        )
        _assert_records(
            self, module, {"part": home.K},
            "r31 1706 plain wf",
        )


class TestRuling1707IsolationAttributeFunction(unittest.TestCase):
    """Ruling 1707: a name returned by a function standing as an attribute."""

    def _home(self, method_source):
        sub = _sub_module(
            "import threading\n"
            "PLAIN = 7\n"
            "HELD = threading.Lock()\n"
            "def name_fn():\n"
            "    return 'HELD'\n"
            "def plain_fn():\n"
            "    return 'PLAIN'\n"
            "def code_fn():\n"
            "    return 'x = HELD'\n"
        )
        home = _make_module(
            "def local_name():\n"
            "    return 'HELD'\n"
            "class K:\n"
            + method_source
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1707_getattr_attribute_function_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, SUB.name_fn())\n"
        )
        _check3(self, module, home, "r31 1707 getattr")

    def test_1707_dict_attribute_function_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return SUB.__dict__[SUB.name_fn()]\n"
        )
        _check3(self, module, home, "r31 1707 dict")

    def test_1707_exec_attribute_function_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(SUB.code_fn(), SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, home, "r31 1707 exec")

    def test_1707_getattr_loaded_function_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, local_name())\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1707 loaded wf",
        )

    def test_1707_getattr_attribute_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, SUB.plain_fn())\n"
        )
        _assert_records(
            self, module, {"part": home.K},
            "r31 1707 plain wf",
        )


class TestRuling1708IsolationBytesGlobals(unittest.TestCase):
    """Ruling 1708: a name decoded from a bytes value in the home globals."""

    def _home(self, method_source, keyb="b'HELD'",
              codeb="b'x = HELD'"):
        sub = _sub_module()
        home = _make_module(
            "KEYB = " + keyb + "\n"
            "CODEB = " + codeb + "\n"
            "class K:\n"
            + method_source
        )
        home.__dict__["SUB"] = sub
        return home

    def test_1708_getattr_bytes_globals_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, KEYB.decode())\n"
        )
        _check3(self, module, home, "r31 1708 getattr")

    def test_1708_dict_bytes_globals_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return SUB.__dict__[KEYB.decode()]\n"
        )
        _check3(self, module, home, "r31 1708 dict")

    def test_1708_exec_bytes_globals_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(CODEB, SUB.__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, home, "r31 1708 exec")

    def test_1708_getattr_bytes_default_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, raw=b'HELD'):\n"
            "        return getattr(SUB, raw.decode())\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1708 default wf",
        )

    def test_1708_getattr_bytes_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return getattr(SUB, KEYB.decode())\n",
            "b'PLAIN'",
        )
        _assert_records(
            self, module, {"part": home.K},
            "r31 1708 plain wf",
        )


class TestRuling1709IsolationObjectGetattribute(unittest.TestCase):
    """Ruling 1709: the getattribute act of the object type."""

    def _home(self, method_source, chain=False):
        if chain:
            return _chain_home(
                "class K:\n" + method_source
            )
        sub = _sub_module()
        home = _make_module("class K:\n" + method_source)
        home.__dict__["SUB"] = sub
        return home

    def test_1709_object_getattribute_literal_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return object.__getattribute__(SUB, 'HELD')\n"
        )
        _check3(self, module, home, "r31 1709 direct")

    def test_1709_object_getattribute_chain_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return object.__getattribute__(\n"
            "            OUTER.INNER, 'HELD')\n",
            chain=True,
        )
        _check3(self, module, home, "r31 1709 chain")

    def test_1709_object_getattribute_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self, n='HELD'):\n"
            "        return object.__getattribute__(SUB, n)\n"
        )
        _check3(self, module, home, "r31 1709 default")

    def test_1709_direct_getattribute_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return SUB.__getattribute__('HELD')\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1709 direct form wf",
        )

    def test_1709_object_getattribute_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "    def method(self):\n"
            "        return object.__getattribute__(SUB, 'PLAIN')\n"
        )
        _assert_records(
            self, module, {"part": home.K},
            "r31 1709 plain wf",
        )


class TestRuling1710IsolationChainBaseAttributeName(unittest.TestCase):
    """Ruling 1710: acts at a chain hop under a base attribute name."""

    def _home(self, method_body, outer_extra="NAME = 'HELD'\n"):
        inner = _make_module(
            "import threading\n"
            "PLAIN = 7\n"
            "HELD = threading.Lock()\n",
            "r31_region5_inner7",
        )
        outer = _make_module(outer_extra, "r31_region5_outer7")
        outer.__dict__["INNER"] = inner
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["OUTER"] = outer
        return home

    def test_1710_getattr_chain_base_name_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.INNER, OUTER.NAME)")
        _check3(self, module, home, "r31 1710 getattr")

    def test_1710_dict_chain_base_name_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("OUTER.INNER.__dict__[OUTER.NAME]")
        _check3(self, module, home, "r31 1710 dict")

    def test_1710_vars_chain_base_name_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("vars(OUTER.INNER)[OUTER.NAME]")
        _check3(self, module, home, "r31 1710 vars")

    def test_1710_target_attribute_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module(
            "import threading\n"
            "PLAIN = 7\n"
            "HELD = threading.Lock()\n"
            "NAMEKEY = 'HELD'\n"
        )
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(SUB, SUB.NAMEKEY)\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1710 target attr wf",
        )

    def test_1710_chain_literal_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER.INNER, 'HELD')")
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1710 chain literal wf",
        )

    def test_1710_getattr_chain_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(OUTER.INNER, OUTER.NAME)",
            "NAME = 'PLAIN'\n",
        )
        _assert_records(
            self, module, {"part": home.K},
            "r31 1710 plain wf",
        )


class TestRuling1711IsolationCarriedKeyPresentation(unittest.TestCase):
    """Ruling 1711: presented modules under a carried key."""

    def test_1711_dict_subscript_default_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return getattr(OUTER.__dict__[k], 'HELD')\n"
        )
        _check3(self, module, home, "r31 1711 dict default")

    def test_1711_getattr_result_default_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return getattr(getattr(OUTER, k), 'HELD')\n"
        )
        _check3(self, module, home, "r31 1711 getattr default")

    def test_1711_vars_subscript_default_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return vars(OUTER)[k].__dict__['HELD']\n"
        )
        _check3(self, module, home, "r31 1711 vars default")

    def test_1711_dict_subscript_closure_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "def _factory(k):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            return OUTER.__dict__[k].__dict__['HELD']\n"
            "    return K\n"
            "K = _factory('INNER')\n"
        )
        _check3(self, module, home, "r31 1711 dict closure")

    def test_1711_literal_key_still_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(OUTER.__dict__['INNER'], 'HELD')\n"
        )
        _assert_refused(
            self, module, {"part": home.K},
            "r31 1711 literal wf",
        )

    def test_1711_carried_key_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return getattr(OUTER.__dict__[k], 'PLAIN')\n"
        )
        _assert_records(
            self, module, {"part": home.K},
            "r31 1711 plain wf",
        )
