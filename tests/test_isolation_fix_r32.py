"""Fix round 32 tests for rulings 1795 to 1811, Region 4.

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


def _make_module(body, name_hint="r32_region4_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r32_region4_sub")


def _chain_home(source):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r32_region4_inner",
    )
    outer = _make_module("", "r32_region4_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(source)
    home.__dict__["OUTER"] = outer
    return home


def _target_home(source, extra=""):
    target = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r32_region4_target",
    )
    home = _make_module(extra + source)
    home.__dict__["MOD"] = target
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


class TestRuling1795IsolationVarsGetResult(unittest.TestCase):
    """Ruling 1795: acts on the get form of the vars return."""

    def test_1795_getattr_vars_get_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(vars(OUTER).get('INNER'), 'HELD')\n"
        )
        _check3(self, module, home, "r32 1795 getattr")

    def test_1795_dict_subscript_vars_get_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return vars(OUTER).get('INNER').__dict__['HELD']\n"
        )
        _check3(self, module, home, "r32 1795 dictsub")

    def test_1795_vars_subscript_vars_get_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return vars(vars(OUTER).get('INNER'))['HELD']\n"
        )
        _check3(self, module, home, "r32 1795 varssub")

    def test_1795_exec_vars_get_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', vars(OUTER).get('INNER').__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, home, "r32 1795 exec")

    def test_1795_getattribute_vars_get_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return vars(OUTER).get('INNER').__getattribute__('HELD')\n"
        )
        _check3(self, module, home, "r32 1795 getattribute")

    def test_1795_dict_get_literal_still_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'), 'HELD')\n"
        )
        _assert_refused(
            self, module, {"part": home.K}, "r32 1795 literal wf"
        )

    def test_1795_vars_get_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(vars(OUTER).get('INNER'), 'PLAIN')\n"
        )
        _assert_records(
            self, module, {"part": home.K}, "r32 1795 plain wf"
        )


class TestRuling1796IsolationDictGetCarriedKey(unittest.TestCase):
    """Ruling 1796: the dictionary get form under a carried key."""

    def test_1796_getattr_default_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return getattr(OUTER.__dict__.get(k), 'HELD')\n"
        )
        _check3(self, module, home, "r32 1796 getattr default")

    def test_1796_dict_subscript_default_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return OUTER.__dict__.get(k).__dict__['HELD']\n"
        )
        _check3(self, module, home, "r32 1796 dictsub default")

    def test_1796_exec_default_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        loc = {}\n"
            "        exec('x = HELD', OUTER.__dict__.get(k).__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, home, "r32 1796 exec default")

    def test_1796_getattr_closure_key_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "def _factory(k):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            return getattr(OUTER.__dict__.get(k), 'HELD')\n"
            "    return K\n"
            "K = _factory('INNER')\n"
        )
        _check3(self, module, home, "r32 1796 getattr closure")

    def test_1796_literal_key_still_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'), 'HELD')\n"
        )
        _assert_refused(
            self, module, {"part": home.K}, "r32 1796 literal wf"
        )

    def test_1796_carried_key_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return getattr(OUTER.__dict__.get(k), 'PLAIN')\n"
        )
        _assert_records(
            self, module, {"part": home.K}, "r32 1796 plain wf"
        )


class TestRuling1797IsolationTypeGetattribute(unittest.TestCase):
    """Ruling 1797: the getattribute act of the type of a module."""

    def test_1797_type_getattribute_direct_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return type(SUB).__getattribute__(SUB, 'HELD')\n"
        )
        home.__dict__["SUB"] = sub
        _check3(self, module, home, "r32 1797 direct")

    def test_1797_type_getattribute_chain_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return type(OUTER.INNER).__getattribute__(OUTER.INNER, 'HELD')\n"
        )
        _check3(self, module, home, "r32 1797 chain")

    def test_1797_type_getattribute_default_name_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self, n='HELD'):\n"
            "        return type(SUB).__getattribute__(SUB, n)\n"
        )
        home.__dict__["SUB"] = sub
        _check3(self, module, home, "r32 1797 default")

    def test_1797_object_getattribute_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return object.__getattribute__(SUB, 'HELD')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K}, "r32 1797 object wf"
        )

    def test_1797_type_getattribute_plain_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return type(SUB).__getattribute__(SUB, 'PLAIN')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": home.K}, "r32 1797 plain wf"
        )


class TestRuling1798ConsumeClassAttributeName(unittest.TestCase):
    """Ruling 1798: a name standing as a class attribute value."""

    def _home(self, method_body, extra=""):
        return _target_home(
            "class K:\n"
            "    held_name = 'HELD'\n"
            "    plain_name = 'PLAIN'\n"
            "    def method(self):\n"
            "        return %s\n" % method_body,
            extra,
        )

    def test_1798_getattr_class_load_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, K.held_name)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1798 class load wf",
        )

    def test_1798_getattr_self_load_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, self.held_name)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1798 self load wf",
        )

    def test_1798_dict_subscript_class_load_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("MOD.__dict__[K.held_name]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1798 dictsub wf",
        )

    def test_1798_class_attribute_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, K.plain_name)")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1798 plain wf",
        )

    def test_1798_home_index_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[K.held_name]")
        home.__dict__["HELD"] = home.__dict__["MOD"].__dict__["HELD"]
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1798 home wf",
        )


class TestRuling1799ConsumeInstanceAttributeName(unittest.TestCase):
    """Ruling 1799: a name standing as an instance attribute value."""

    def _home(self, method_body):
        return _target_home(
            "class K:\n"
            "    def __init__(self):\n"
            "        self.held_name = 'HELD'\n"
            "        self.plain_name = 'PLAIN'\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )

    def test_1799_getattr_self_load_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, self.held_name)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1799 getattr wf",
        )

    def test_1799_dict_subscript_self_load_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("MOD.__dict__[self.held_name]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1799 dictsub wf",
        )

    def test_1799_instance_attribute_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, self.plain_name)")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1799 plain wf",
        )

    def test_1799_home_index_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[self.held_name]")
        home.__dict__["HELD"] = home.__dict__["MOD"].__dict__["HELD"]
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1799 home wf",
        )


class TestRuling1800ConsumeTwoHopAttributeName(unittest.TestCase):
    """Ruling 1800: a name at a two hop attribute load."""

    def _home(self, method_body, attr_value="'HELD'"):
        further = _make_module("", "r32_region4_further")
        inner = _make_module("", "r32_region4_innerattr")
        inner.__dict__["held_name"] = (
            "HELD" if attr_value == "'HELD'" else "PLAIN"
        )
        further.__dict__["INNER"] = inner
        home = _target_home(
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["FURTHER"] = further
        return home

    def test_1800_getattr_two_hop_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, FURTHER.INNER.held_name)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1800 getattr wf",
        )

    def test_1800_dict_subscript_two_hop_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("MOD.__dict__[FURTHER.INNER.held_name]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1800 dictsub wf",
        )

    def test_1800_two_hop_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home(
            "getattr(MOD, FURTHER.INNER.held_name)", "'PLAIN'"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1800 plain wf",
        )

    def test_1800_home_index_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[FURTHER.INNER.held_name]")
        home.__dict__["HELD"] = home.__dict__["MOD"].__dict__["HELD"]
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1800 home wf",
        )


class TestRuling1801ConsumeHelperDefaultHome(unittest.TestCase):
    """Ruling 1801: a name returned from a helper default, home map."""

    def test_1801_home_index_helper_default_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _helper(n='HELD'):\n"
            "    return n\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()[_helper()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1801 home wf",
        )

    def test_1801_home_index_helper_default_plain_records(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _helper(n='PLAIN'):\n"
            "    return n\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()[_helper()]\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1801 plain wf",
        )

    def test_1801_first_order_return_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _helper():\n"
            "    return 'HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()[_helper()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1801 first order wf",
        )


class TestRuling1802ConsumeHelperDefaultForeign(unittest.TestCase):
    """Ruling 1802: a name returned from a helper default, foreign act."""

    def _home(self, method_body, default="'HELD'"):
        return _target_home(
            "def _helper(n=%s):\n"
            "    return n\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % (default, method_body)
        )

    def test_1802_getattr_helper_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, _helper())")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1802 getattr wf",
        )

    def test_1802_dict_subscript_helper_default_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("MOD.__dict__[_helper()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1802 dictsub wf",
        )

    def test_1802_helper_default_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, _helper())", "'PLAIN'")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1802 plain wf",
        )

    def test_1802_first_order_return_still_refused(self):
        module = require("ontoloop.consumption")
        home = _target_home(
            "def _helper():\n"
            "    return 'HELD'\n"
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(MOD, _helper())\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1802 first order wf",
        )


class TestRuling1803ConsumeSecondOrderAttrCallHome(unittest.TestCase):
    """Ruling 1803: a second order name through an attribute call."""

    def _home(self, method_body, returned="'HELD'"):
        further = _make_module(
            "def _named():\n    return %s\n" % returned,
            "r32_region4_furtherfn",
        )
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _mid():\n"
            "    return FURTHER._named()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["FURTHER"] = further
        return home

    def test_1803_home_index_second_order_attr_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[_mid()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1803 home wf",
        )

    def test_1803_second_order_attr_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[_mid()]", "'PLAIN'")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1803 plain wf",
        )

    def test_1803_second_order_by_name_still_refused(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _inner():\n"
            "    return 'HELD'\n"
            "def _mid():\n"
            "    return _inner()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return globals()[_mid()]\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1803 by name wf",
        )


class TestRuling1804ConsumeSecondOrderAttrCallForeign(unittest.TestCase):
    """Ruling 1804: ruling 1803 carriage at a foreign act."""

    def _home(self, method_body, returned="'HELD'"):
        further = _make_module(
            "def _named():\n    return %s\n" % returned,
            "r32_region4_furtherfn",
        )
        home = _target_home(
            "def _mid():\n"
            "    return FURTHER._named()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["FURTHER"] = further
        return home

    def test_1804_getattr_second_order_attr_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, _mid())")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1804 getattr wf",
        )

    def test_1804_dict_subscript_second_order_attr_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("MOD.__dict__[_mid()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1804 dictsub wf",
        )

    def test_1804_second_order_attr_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, _mid())", "'PLAIN'")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1804 plain wf",
        )

    def test_1804_second_order_by_name_still_refused(self):
        module = require("ontoloop.consumption")
        home = _target_home(
            "def _inner():\n"
            "    return 'HELD'\n"
            "def _mid():\n"
            "    return _inner()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(MOD, _mid())\n"
        )
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1804 by name wf",
        )


class TestRuling1805ConsumeSecondOrderAttrValueHome(unittest.TestCase):
    """Ruling 1805: a second order name through an attribute return."""

    def _home(self, method_body, attr_value="HELD"):
        further = _make_module("", "r32_region4_furtherval")
        further.__dict__["held_name"] = attr_value
        home = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "PLAIN = 7\n"
            "def _mid():\n"
            "    return FURTHER.held_name\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["FURTHER"] = further
        return home

    def test_1805_home_index_second_order_value_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[_mid()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1805 home wf",
        )

    def test_1805_second_order_value_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("globals()[_mid()]", "PLAIN")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1805 plain wf",
        )

    def test_1805_direct_attribute_still_refused(self):
        module = require("ontoloop.consumption")
        home = _target_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(MOD, FURTHER.held_name)\n"
        )
        further = _make_module("", "r32_region4_furtherval")
        further.__dict__["held_name"] = "HELD"
        home.__dict__["FURTHER"] = further
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1805 direct wf",
        )


class TestRuling1806ConsumeSecondOrderAttrValueForeign(unittest.TestCase):
    """Ruling 1806: ruling 1805 carriage at a foreign act."""

    def _home(self, method_body, attr_value="HELD"):
        further = _make_module("", "r32_region4_furtherval")
        further.__dict__["held_name"] = attr_value
        home = _target_home(
            "def _mid():\n"
            "    return FURTHER.held_name\n"
            "class K:\n"
            "    def method(self):\n"
            "        return %s\n" % method_body
        )
        home.__dict__["FURTHER"] = further
        return home

    def test_1806_getattr_second_order_value_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, _mid())")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1806 getattr wf",
        )

    def test_1806_dict_subscript_second_order_value_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("MOD.__dict__[_mid()]")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1806 dictsub wf",
        )

    def test_1806_second_order_value_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, _mid())", "PLAIN")
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1806 plain wf",
        )

    def test_1806_direct_attribute_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(MOD, FURTHER.held_name)")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1806 direct wf",
        )


class TestRuling1807ChairExecCarriedCallResult(unittest.TestCase):
    """Ruling 1807: exec with a call result mapping under carried forms."""

    def _home(self, globals_expr, code_expr="'x = HELD'", extra=""):
        return _chain_home(
            extra
            + "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec(%s, %s, loc)\n"
            "        return loc['x']\n" % (code_expr, globals_expr)
        )

    def test_1807_exec_getattr_result_carried_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self, n='INNER'):\n"
            "        loc = {}\n"
            "        exec('x = HELD', getattr(OUTER, n).__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1807 getattr carried wf",
        )

    def test_1807_exec_vars_result_carried_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        loc = {}\n"
            "        exec('x = HELD', vars(OUTER)[k].__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1807 vars carried wf",
        )

    def test_1807_exec_dict_get_carried_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        loc = {}\n"
            "        exec('x = HELD', OUTER.__dict__.get(k).__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1807 dict get carried wf",
        )

    def test_1807_exec_dict_get_global_key_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "KEYNAME = 'INNER'\n"
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', OUTER.__dict__.get(KEYNAME).__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1807 dict get global key wf",
        )

    def test_1807_exec_getattr_result_variable_code_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "CODE = 'x = HELD'\n"
            "class K:\n"
            "    def method(self, n='INNER'):\n"
            "        loc = {}\n"
            "        exec(CODE, getattr(OUTER, n).__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1807 variable code wf",
        )

    def test_1807_exec_vars_get_result_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home("vars(OUTER).get('INNER').__dict__")
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1807 vars get wf",
        )

    def test_1807_exec_literal_call_result_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER, 'INNER').__dict__")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1807 literal wf",
        )

    def test_1807_exec_dict_get_carried_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        loc = {}\n"
            "        exec('x = PLAIN', OUTER.__dict__.get(k).__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1807 plain wf",
        )


class TestRuling1808ChairDictGetCarriedTarget(unittest.TestCase):
    """Ruling 1808: acts on a dictionary get result under a carried key."""

    def test_1808_getattr_dict_get_default_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return getattr(OUTER.__dict__.get(k), 'HELD')\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1808 getattr wf",
        )

    def test_1808_vars_subscript_dict_get_default_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return vars(OUTER.__dict__.get(k))['HELD']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1808 vars wf",
        )

    def test_1808_dict_subscript_dict_get_default_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return OUTER.__dict__.get(k).__dict__['HELD']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1808 dictsub wf",
        )

    def test_1808_getattr_dict_get_closure_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "def _factory(k):\n"
            "    class K:\n"
            "        def method(self):\n"
            "            return getattr(OUTER.__dict__.get(k), 'HELD')\n"
            "    return K\n"
            "K = _factory('INNER')\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1808 closure wf",
        )

    def test_1808_literal_dict_get_still_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'), 'HELD')\n"
        )
        _assert_refused(
            self, module, {"part": home.K}, "r32 1808 literal wf"
        )

    def test_1808_dict_get_carried_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self, k='INNER'):\n"
            "        return getattr(OUTER.__dict__.get(k), 'PLAIN')\n"
        )
        _assert_records(
            self, module, {"part": home.K}, "r32 1808 plain wf"
        )


class TestRuling1809ChairVarsGetTarget(unittest.TestCase):
    """Ruling 1809: acts on the get form of the vars return."""

    def test_1809_getattr_vars_get_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(vars(OUTER).get('INNER'), 'HELD')\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1809 getattr wf",
        )

    def test_1809_vars_subscript_vars_get_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return vars(vars(OUTER).get('INNER'))['HELD']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1809 vars wf",
        )

    def test_1809_dict_subscript_vars_get_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return vars(OUTER).get('INNER').__dict__['HELD']\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1809 dictsub wf",
        )

    def test_1809_dict_get_literal_still_refused(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'), 'HELD')\n"
        )
        _assert_refused(
            self, module, {"part": home.K}, "r32 1809 literal wf"
        )

    def test_1809_vars_get_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(vars(OUTER).get('INNER'), 'PLAIN')\n"
        )
        _assert_records(
            self, module, {"part": home.K}, "r32 1809 plain wf"
        )


class TestRuling1810ChairGetattributeResultTarget(unittest.TestCase):
    """Ruling 1810: acts on a module standing as a getattribute result."""

    def test_1810_getattr_attr_result_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(OUTER.__getattribute__('INNER'), 'HELD')\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1810 attr result wf",
        )

    def test_1810_getattr_object_result_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(object.__getattribute__(OUTER, 'INNER'), 'HELD')\n"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1810 object result wf",
        )

    def test_1810_direct_getattribute_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return SUB.__getattribute__('HELD')\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K}, "r32 1810 direct wf"
        )

    def test_1810_getattribute_result_plain_still_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        return getattr(OUTER.__getattribute__('INNER'), 'PLAIN')\n"
        )
        _assert_records(
            self, module, {"part": home.K}, "r32 1810 plain wf"
        )


class TestRuling1811ChairExecGetattributeResult(unittest.TestCase):
    """Ruling 1811: exec with a getattribute result mapping."""

    def _home(self, globals_expr):
        return _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', %s, loc)\n"
            "        return loc['x']\n" % globals_expr
        )

    def test_1811_exec_attr_result_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home("OUTER.__getattribute__('INNER').__dict__")
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1811 attr result wf",
        )

    def test_1811_exec_object_result_refused(self):
        module = require("ontoloop.consumption")
        service = require("ontoloop.service_layer")
        home = self._home(
            "object.__getattribute__(OUTER, 'INNER').__dict__"
        )
        _assert_refused_both(
            self, module, service, {"part": Holder(home.K)},
            "r32 1811 object result wf",
        )

    def test_1811_exec_literal_call_result_still_refused(self):
        module = require("ontoloop.consumption")
        home = self._home("getattr(OUTER, 'INNER').__dict__")
        _assert_refused(
            self, module, {"part": Holder(home.K)},
            "r32 1811 literal wf",
        )

    def test_1811_exec_getattribute_result_plain_records(self):
        module = require("ontoloop.consumption")
        home = _chain_home(
            "class K:\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = PLAIN', OUTER.__getattribute__('INNER').__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _assert_records(
            self, module, {"part": Holder(home.K)},
            "r32 1811 plain wf",
        )


class TestRuling1044BoundedFormStanding(unittest.TestCase):
    """Ruling 1044 bounded form: standing poles at both poles."""

    def test_1044_direct_lock_still_refused(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return SUB.HELD\n"
        )
        home.__dict__["SUB"] = sub
        _assert_refused(
            self, module, {"part": home.K}, "r32 1044 direct wf"
        )

    def test_1044_module_value_still_records(self):
        module = require("ontoloop.consumption")
        sub = _sub_module()
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return SUB\n"
        )
        home.__dict__["SUB"] = sub
        _assert_records(
            self, module, {"part": home.K}, "r32 1044 module wf"
        )

    def test_1044_plain_class_still_records(self):
        module = require("ontoloop.consumption")
        home = _make_module(
            "class K:\n"
            "    def method(self):\n"
            "        return 7\n"
        )
        _assert_records(
            self, module, {"part": home.K}, "r32 1044 plain wf"
        )
