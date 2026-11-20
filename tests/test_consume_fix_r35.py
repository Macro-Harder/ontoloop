"""Fix round 35 tests for rulings 2174 to 2192, Regions 5 and 6.

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


def _make_module(body, name_hint="r35_region56_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r35_region56_sub")


def _chain_home(source, extra=""):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r35_region56_inner",
    )
    outer = _make_module("", "r35_region56_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(extra + source)
    home.__dict__["OUTER"] = outer
    return home


def _target_home(source, extra=""):
    target = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r35_region56_target",
    )
    home = _make_module(extra + source)
    home.__dict__["MOD"] = target
    return home


def _pair_home(source, carrier_body, extra="", with_target=False):
    carrier = _make_module(carrier_body, "r35_region56_carrier")
    home = _make_module(extra + source)
    home.__dict__["CARRIER"] = carrier
    if with_target:
        home.__dict__["MOD"] = _sub_module()
    return home


def _check3(case, module, service, home, label):
    _assert_refused_both(
        case, module, service, {"part": home.K}, label + " class wf"
    )
    _assert_refused_both(
        case, module, service, {"part": home.K()},
        label + " instance wf",
    )
    _assert_refused_both(
        case, module, service, {"part": Holder(home.K)},
        label + " holder wf",
    )


def _records3(case, module, home, label):
    _assert_records(
        case, module, {"part": home.K}, label + " class wf"
    )
    _assert_records(
        case, module, {"part": home.K()}, label + " instance wf"
    )
    _assert_records(
        case, module, {"part": Holder(home.K)}, label + " holder wf"
    )


def _mods(case):
    return require("ontoloop.consumption"), require(
        "ontoloop.service_layer"
    )


_HOME_TAIL = (
    "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
)


class TestConsumeFixR35Chair1ContainerCarried(unittest.TestCase):
    """Ruling 2174: container element inside the called function."""

    def test_2174_getattr_default_tuple(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod(_k=('INNER',)):\n"
            "    return getattr(OUTER, _k[0])\n",
        )
        _check3(self, module, service, home, "r35 2174 f1")

    def test_2174_vars_subscript_default_list(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return vars(getmod())['HELD']\n",
            "def getmod(_k=['INNER']):\n"
            "    return getattr(OUTER, _k[0])\n",
        )
        _check3(self, module, service, home, "r35 2174 f2")

    def test_2174_dict_subscript_default_dict(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getmod().__dict__['HELD']\n",
            "def getmod(_k={'k': 'INNER'}):\n"
            "    return getattr(OUTER, _k['k'])\n",
        )
        _check3(self, module, service, home, "r35 2174 f3")

    def test_2174_exec_vars_get_tuple(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', getmod().__dict__, loc)\n"
            "        return loc['x']\n",
            "def getmod(_k=('INNER',)):\n"
            "    return vars(OUTER).get(_k[0])\n",
        )
        _check3(self, module, service, home, "r35 2174 f4")

    def test_2174_getattr_closure_list(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def _fac():\n    _k = ['INNER']\n    def getmod():\n"
            "        return getattr(OUTER, _k[0])\n"
            "    return getmod\n"
            "getmod = _fac()\n",
        )
        _check3(self, module, service, home, "r35 2174 f5")

    def test_2174_getattr_globals_list(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "KEYS = ['INNER']\n"
            "def getmod():\n    return getattr(OUTER, KEYS[0])\n",
        )
        _check3(self, module, service, home, "r35 2174 f6")

    def test_2174_dict_subscript_globals_tuple(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getmod().__dict__['HELD']\n",
            "KEYS = ('INNER',)\n"
            "def getmod():\n    return getattr(OUTER, KEYS[0])\n",
        )
        _check3(self, module, service, home, "r35 2174 f7")

    def test_2174_vars_subscript_globals_dict(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return vars(getmod())['HELD']\n",
            "KEYS = {'k': 'INNER'}\n"
            "def getmod():\n    return getattr(OUTER, KEYS['k'])\n",
        )
        _check3(self, module, service, home, "r35 2174 f8")

    def test_2174_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'PLAIN')\n",
            "def getmod(_k=('INNER',)):\n"
            "    return getattr(OUTER, _k[0])\n",
        )
        _records3(self, module, home, "r35 2174 plain")

    def test_2174_direct_string_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod(key='INNER'):\n"
            "    return getattr(OUTER, key)\n",
        )
        _check3(self, module, service, home, "r35 2174 pole")


_THIRD_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def third():\n"
    "        return _n\n    return third\n"
    "third = _fac()\n"
    "def further():\n    return third()\n"
    "def helper():\n    return further()\n"
) + _HOME_TAIL

_THIRD_STRING = (
    "STR = 'HELD'\n"
    "def third():\n    return STR\n"
    "def further():\n    return third()\n"
    "def helper():\n    return further()\n"
) + _HOME_TAIL

_THIRD_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def third():\n    return D['k']\n"
    "def further():\n    return third()\n"
    "def helper():\n    return further()\n"
) + _HOME_TAIL

_THIRD_DEFAULT = (
    "def third(_n='HELD'):\n    return _n\n"
    "def further():\n    return third()\n"
    "def helper():\n    return further()\n"
) + _HOME_TAIL


class TestConsumeFixR35Consume1ThirdClosureHome(unittest.TestCase):
    """Ruling 2175: third order closure name at the home map."""

    def test_2175_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _THIRD_CLOSURE,
        )
        _check3(self, module, service, home, "r35 2175")

    def test_2175_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _THIRD_CLOSURE.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2175 plain")

    def test_2175_second_order_closure_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _fac():\n    _n = 'HELD'\n    def _h():\n"
            "        return _n\n    return _h\n"
            "_h = _fac()\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2175 pole")

    def test_2175_first_order_closure_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[third()]\n",
            _THIRD_CLOSURE,
        )
        _check3(self, module, service, home, "r35 2175 fo pole")


class TestConsumeFixR35Consume2ThirdClosureForeign(unittest.TestCase):
    """Ruling 2176: third order closure name, foreign module."""

    def test_2176_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _THIRD_CLOSURE,
        )
        _check3(self, module, service, home, "r35 2176 f1")

    def test_2176_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            _THIRD_CLOSURE,
        )
        _check3(self, module, service, home, "r35 2176 f2")

    def test_2176_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _THIRD_CLOSURE.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2176 plain")

    def test_2176_second_order_closure_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def _fac():\n    _n = 'HELD'\n    def _h():\n"
            "        return _n\n    return _h\n"
            "_h = _fac()\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2176 pole")


class TestConsumeFixR35Consume3ThirdStringHome(unittest.TestCase):
    """Ruling 2177: third order module level string, home map."""

    def test_2177_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _THIRD_STRING,
        )
        _check3(self, module, service, home, "r35 2177")

    def test_2177_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _THIRD_STRING.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2177 plain")

    def test_2177_second_order_string_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "STR = 'HELD'\n"
            "def _h():\n    return STR\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2177 pole")


class TestConsumeFixR35Consume4ThirdStringForeign(unittest.TestCase):
    """Ruling 2178: third order module level string, foreign."""

    def test_2178_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _THIRD_STRING,
        )
        _check3(self, module, service, home, "r35 2178 f1")

    def test_2178_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            _THIRD_STRING,
        )
        _check3(self, module, service, home, "r35 2178 f2")

    def test_2178_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _THIRD_STRING.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2178 plain")

    def test_2178_second_order_string_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "STR = 'HELD'\n"
            "def _h():\n    return STR\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2178 pole")


class TestConsumeFixR35Consume5ThirdContainerHome(unittest.TestCase):
    """Ruling 2179: third order container element, home map."""

    def test_2179_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _THIRD_CONTAINER,
        )
        _check3(self, module, service, home, "r35 2179")

    def test_2179_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _THIRD_CONTAINER.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2179 plain")

    def test_2179_second_order_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "D = {'k': 'HELD'}\n"
            "def _h():\n    return D['k']\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2179 pole")


class TestConsumeFixR35Consume6ThirdContainerForeign(unittest.TestCase):
    """Ruling 2180: third order container element, foreign."""

    def test_2180_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _THIRD_CONTAINER,
        )
        _check3(self, module, service, home, "r35 2180 f1")

    def test_2180_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            _THIRD_CONTAINER,
        )
        _check3(self, module, service, home, "r35 2180 f2")

    def test_2180_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _THIRD_CONTAINER.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2180 plain")

    def test_2180_second_order_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "D = {'k': 'HELD'}\n"
            "def _h():\n    return D['k']\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2180 pole")


class TestConsumeFixR35Consume7ThirdDefaultHome(unittest.TestCase):
    """Ruling 2181: third order default argument name, home."""

    def test_2181_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _THIRD_DEFAULT,
        )
        _check3(self, module, service, home, "r35 2181")

    def test_2181_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _THIRD_DEFAULT.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2181 plain")

    def test_2181_second_order_default_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _h(_n='HELD'):\n    return _n\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2181 pole")


class TestConsumeFixR35Consume8ThirdDefaultForeign(unittest.TestCase):
    """Ruling 2182: third order default argument name, foreign."""

    def test_2182_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _THIRD_DEFAULT,
        )
        _check3(self, module, service, home, "r35 2182 f1")

    def test_2182_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            _THIRD_DEFAULT,
        )
        _check3(self, module, service, home, "r35 2182 f2")

    def test_2182_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _THIRD_DEFAULT.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2182 plain")

    def test_2182_second_order_default_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def _h(_n='HELD'):\n    return _n\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2182 pole")


_PAIR_STRING_CARRIER = (
    "STR = 'HELD'\n"
    "def pairfn():\n    return STR\n"
)

_PAIR_CONTAINER_CARRIER = (
    "D = {'k': 'HELD'}\n"
    "def pairfn():\n    return D['k']\n"
)

_PAIR_HELPER = (
    "def helper():\n    return CARRIER.pairfn()\n"
) + _HOME_TAIL


class TestConsumeFixR35Consume9PairStringHome(unittest.TestCase):
    """Ruling 2183: pair function module level string, home."""

    def test_2183_home_index(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _PAIR_STRING_CARRIER,
            _PAIR_HELPER,
        )
        _check3(self, module, service, home, "r35 2183")

    def test_2183_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _PAIR_STRING_CARRIER.replace("'HELD'", "'PLAIN'"),
            _PAIR_HELPER,
        )
        _records3(self, module, home, "r35 2183 plain")

    def test_2183_pair_closure_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            "def _fac():\n    _n = 'HELD'\n    def pairfn():\n"
            "        return _n\n    return pairfn\n"
            "pairfn = _fac()\n",
            _PAIR_HELPER,
        )
        _check3(self, module, service, home, "r35 2183 pole")


class TestConsumeFixR35Consume10PairStringForeign(unittest.TestCase):
    """Ruling 2184: pair function module level string, foreign."""

    def test_2184_foreign_getattr(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _PAIR_STRING_CARRIER,
            _PAIR_HELPER,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2184 f1")

    def test_2184_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            _PAIR_STRING_CARRIER,
            _PAIR_HELPER,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2184 f2")

    def test_2184_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _PAIR_STRING_CARRIER.replace("'HELD'", "'PLAIN'"),
            _PAIR_HELPER,
            with_target=True,
        )
        _records3(self, module, home, "r35 2184 plain")

    def test_2184_pair_closure_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            "def _fac():\n    _n = 'HELD'\n    def pairfn():\n"
            "        return _n\n    return pairfn\n"
            "pairfn = _fac()\n",
            _PAIR_HELPER,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2184 pole")


class TestConsumeFixR35Consume11PairContainerHome(unittest.TestCase):
    """Ruling 2185: pair function container element, home."""

    def test_2185_home_index(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _PAIR_CONTAINER_CARRIER,
            _PAIR_HELPER,
        )
        _check3(self, module, service, home, "r35 2185")

    def test_2185_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            _PAIR_CONTAINER_CARRIER.replace("'HELD'", "'PLAIN'"),
            _PAIR_HELPER,
        )
        _records3(self, module, home, "r35 2185 plain")

    def test_2185_second_order_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "D = {'k': 'HELD'}\n"
            "def _h():\n    return D['k']\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2185 pole")


class TestConsumeFixR35Consume12PairContainerForeign(unittest.TestCase):
    """Ruling 2186: pair function container element, foreign."""

    def test_2186_foreign_getattr(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _PAIR_CONTAINER_CARRIER,
            _PAIR_HELPER,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2186 f1")

    def test_2186_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            _PAIR_CONTAINER_CARRIER,
            _PAIR_HELPER,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2186 f2")

    def test_2186_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _PAIR_CONTAINER_CARRIER.replace("'HELD'", "'PLAIN'"),
            _PAIR_HELPER,
            with_target=True,
        )
        _records3(self, module, home, "r35 2186 plain")

    def test_2186_second_order_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "D = {'k': 'HELD'}\n"
            "def _h():\n    return D['k']\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2186 pole")


_PAIR_CLOSURE_CARRIER = (
    "def _fac():\n    _n = 'HELD'\n    def pairfn():\n"
    "        return _n\n    return pairfn\n"
    "pairfn = _fac()\n"
)

_PAIR_DEFAULT_CARRIER = (
    "def pairfn(_n='HELD'):\n    return _n\n"
)


class TestConsumeFixR35Consume13MemberPairClosureAct(unittest.TestCase):
    """Ruling 2187: member level pair closure, act routes."""

    def test_2187_foreign_getattr(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, CARRIER.pairfn())\n",
            _PAIR_CLOSURE_CARRIER,
            _HOME_TAIL,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2187 f1")

    def test_2187_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[CARRIER.pairfn()]\n",
            _PAIR_CLOSURE_CARRIER,
            _HOME_TAIL,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2187 f2")

    def test_2187_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, CARRIER.pairfn())\n",
            _PAIR_CLOSURE_CARRIER.replace("'HELD'", "'PLAIN'"),
            _HOME_TAIL,
            with_target=True,
        )
        _records3(self, module, home, "r35 2187 plain")

    def test_2187_home_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[CARRIER.pairfn()]\n",
            _PAIR_CLOSURE_CARRIER,
            _HOME_TAIL,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2187 home pole")

    def test_2187_helper_pair_closure_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _PAIR_CLOSURE_CARRIER,
            _PAIR_HELPER,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2187 pole")


class TestConsumeFixR35Consume14MemberPairDefaultAct(unittest.TestCase):
    """Ruling 2188: member level pair default, act routes."""

    def test_2188_foreign_getattr(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, CARRIER.pairfn())\n",
            _PAIR_DEFAULT_CARRIER,
            _HOME_TAIL,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2188 f1")

    def test_2188_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[CARRIER.pairfn()]\n",
            _PAIR_DEFAULT_CARRIER,
            _HOME_TAIL,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2188 f2")

    def test_2188_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, CARRIER.pairfn())\n",
            _PAIR_DEFAULT_CARRIER.replace("'HELD'", "'PLAIN'"),
            _HOME_TAIL,
            with_target=True,
        )
        _records3(self, module, home, "r35 2188 plain")

    def test_2188_home_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[CARRIER.pairfn()]\n",
            _PAIR_DEFAULT_CARRIER,
            _HOME_TAIL,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2188 home pole")

    def test_2188_helper_pair_default_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            _PAIR_DEFAULT_CARRIER,
            _PAIR_HELPER,
            with_target=True,
        )
        _check3(self, module, service, home, "r35 2188 pole")


_CLS_DEF = (
    "class Cls:\n    NAME = 'HELD'\n    PNAME = 'PLAIN'\n"
    "    KEY = 'INNER'\n    KEYP = 'INNERP'\n"
)


def _deep_home(source):
    leaf = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r35_region56_leaf",
    )
    inner = _make_module("", "r35_region56_deep_inner")
    inner.__dict__["LEAF"] = leaf
    mid = _make_module("", "r35_region56_deep_mid")
    mid.__dict__["INNER"] = inner
    outer = _make_module("", "r35_region56_deep_outer")
    outer.__dict__["MID"] = mid
    home = _make_module(_CLS_DEF + source)
    home.__dict__["OUTER"] = outer
    return home


class TestConsumeFixR35Iso1FourthHopChain(unittest.TestCase):
    """Ruling 2189: governed value at the fourth hop of a chain."""

    def test_2189_getattr_gathered(self):
        module, service = _mods(self)
        home = _deep_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.MID.INNER.LEAF, Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r35 2189 f1")

    def test_2189_dict_subscript_literal(self):
        module, service = _mods(self)
        home = _deep_home(
            "class K:\n    def method(self):\n"
            "        return OUTER.MID.INNER.LEAF.__dict__['HELD']\n"
        )
        _check3(self, module, service, home, "r35 2189 f2")

    def test_2189_vars_subscript_gathered(self):
        module, service = _mods(self)
        home = _deep_home(
            "class K:\n    def method(self):\n"
            "        return vars(OUTER.MID.INNER.LEAF)[Cls.NAME]\n"
        )
        _check3(self, module, service, home, "r35 2189 f3")

    def test_2189_plain_records(self):
        module, service = _mods(self)
        home = _deep_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.MID.INNER.LEAF, Cls.PNAME)\n"
        )
        _records3(self, module, home, "r35 2189 plain")

    def test_2189_third_hop_pole(self):
        module, service = _mods(self)
        leaf = _make_module(
            "import threading\n"
            "PLAIN = 7\n"
            "HELD = threading.Lock()\n",
            "r35_region56_pole_leaf",
        )
        mid = _make_module("", "r35_region56_pole_mid")
        mid.__dict__["LEAF"] = leaf
        outer = _make_module("", "r35_region56_pole_outer")
        outer.__dict__["MID"] = mid
        home = _make_module(
            _CLS_DEF
            + "class K:\n    def method(self):\n"
            "        return getattr(OUTER.MID.LEAF, Cls.NAME)\n"
        )
        home.__dict__["OUTER"] = outer
        _check3(self, module, service, home, "r35 2189 pole")


def _iso2_home(source):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r35_region56_iso2_inner",
    )
    innerp = _make_module("PLAIN = 7\n", "r35_region56_iso2_innerp")
    outer = _make_module("", "r35_region56_iso2_outer")
    outer.__dict__["INNER"] = inner
    outer.__dict__["INNERP"] = innerp
    home = _make_module(_CLS_DEF + source)
    home.__dict__["OUTER"] = outer
    return home


class TestConsumeFixR35Iso2SubscriptAttrKey(unittest.TestCase):
    """Ruling 2190: subscript presentation under an attribute key."""

    def test_2190_vars_subscript_attr_key(self):
        module, service = _mods(self)
        home = _iso2_home(
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER)[Cls.KEY], 'HELD')\n"
        )
        _check3(self, module, service, home, "r35 2190 f1")

    def test_2190_dict_subscript_attr_key(self):
        module, service = _mods(self)
        home = _iso2_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.__dict__[Cls.KEY], 'HELD')\n"
        )
        _check3(self, module, service, home, "r35 2190 f2")

    def test_2190_plain_records(self):
        module, service = _mods(self)
        home = _iso2_home(
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER)[Cls.KEYP], 'PLAIN')\n"
        )
        _records3(self, module, home, "r35 2190 plain")

    def test_2190_get_form_pole(self):
        module, service = _mods(self)
        home = _iso2_home(
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER).get(Cls.KEY), 'HELD')\n"
        )
        _check3(self, module, service, home, "r35 2190 pole")


_ISO3_CHAIN = (
    "def _fac():\n    _n = 'HELD'\n    def third():\n"
    "        return _n\n    return third\n"
    "third = _fac()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
) + _HOME_TAIL

_ISO4_CHAIN = (
    "L = ['HELD']\n"
    "def third():\n    return L[0]\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
) + _HOME_TAIL


class TestConsumeFixR35Iso3ThirdClosureClass(unittest.TestCase):
    """Ruling 2191: third order closure name of a class member."""

    def test_2191_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            _ISO3_CHAIN,
        )
        _check3(self, module, service, home, "r35 2191 f1")

    def test_2191_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            _ISO3_CHAIN,
        )
        _check3(self, module, service, home, "r35 2191 f2")

    def test_2191_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            _ISO3_CHAIN.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2191 plain")

    def test_2191_second_order_closure_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _fac():\n    _n = 'HELD'\n    def _h():\n"
            "        return _n\n    return _h\n"
            "_h = _fac()\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2191 pole")


class TestConsumeFixR35Iso4ThirdContainerClass(unittest.TestCase):
    """Ruling 2192: third order container element, class member."""

    def test_2192_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            _ISO4_CHAIN,
        )
        _check3(self, module, service, home, "r35 2192 f1")

    def test_2192_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            _ISO4_CHAIN,
        )
        _check3(self, module, service, home, "r35 2192 f2")

    def test_2192_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            _ISO4_CHAIN.replace("'HELD'", "'PLAIN'"),
        )
        _records3(self, module, home, "r35 2192 plain")

    def test_2192_second_order_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "D = {'k': 'HELD'}\n"
            "def _h():\n    return D['k']\n"
            "def mid():\n    return _h()\n" + _HOME_TAIL,
        )
        _check3(self, module, service, home, "r35 2192 pole")
