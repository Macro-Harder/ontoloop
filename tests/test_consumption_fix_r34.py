"""Fix round 34 tests for rulings 2048 to 2065, Region 5.

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


def _make_module(body, name_hint="r34_region5_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r34_region5_sub")


def _chain_home(source, extra=""):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r34_region5_inner",
    )
    outer = _make_module("", "r34_region5_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(extra + source)
    home.__dict__["OUTER"] = outer
    return home


def _target_home(source, extra=""):
    target = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r34_region5_target",
    )
    home = _make_module(extra + source)
    home.__dict__["MOD"] = target
    return home


def _pair_home(source, carrier_body, extra="", with_target=False):
    carrier = _make_module(carrier_body, "r34_region5_carrier")
    home = _make_module(extra + source)
    home.__dict__["CARRIER"] = carrier
    if with_target:
        home.__dict__["MOD"] = _sub_module()
    return home


def _deep_home(source, extra=""):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r34_region5_deep_inner",
    )
    mid = _make_module("", "r34_region5_deep_mid")
    mid.__dict__["INNER"] = inner
    outer = _make_module("", "r34_region5_deep_outer")
    outer.__dict__["MID"] = mid
    outer.__dict__["INNER"] = inner
    home = _make_module(extra + source)
    home.__dict__["OUTER"] = outer
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


class TestConsumptionFixR34Chair1CallResultCarried(
    unittest.TestCase
):
    """Ruling 2048: carried name inside the called function."""

    def test_2048_getattr_default_carriage(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod(key='INNER'):\n"
            "    return getattr(OUTER, key)\n",
        )
        _check3(self, module, service, home, "r34 2048 f1")

    def test_2048_vars_subscript_default_carriage(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return vars(getmod())['HELD']\n",
            "def getmod(key='INNER'):\n"
            "    return getattr(OUTER, key)\n",
        )
        _check3(self, module, service, home, "r34 2048 f2")

    def test_2048_dict_subscript_vars_get_carriage(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getmod().__dict__['HELD']\n",
            "def getmod(key='INNER'):\n"
            "    return vars(OUTER).get(key)\n",
        )
        _check3(self, module, service, home, "r34 2048 f3")

    def test_2048_exec_dict_get_carriage(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', getmod().__dict__, loc)\n"
            "        return loc['x']\n",
            "def getmod(key='INNER'):\n"
            "    return OUTER.__dict__.get(key)\n",
        )
        _check3(self, module, service, home, "r34 2048 f4")

    def test_2048_home_string_carriage(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "KEY = 'INNER'\n"
            "def getmod():\n    return getattr(OUTER, KEY)\n",
        )
        _check3(self, module, service, home, "r34 2048 f5")

    def test_2048_closure_carriage(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def _fac():\n    k = 'INNER'\n    def getmod():\n"
            "        return getattr(OUTER, k)\n"
            "    return getmod\n"
            "getmod = _fac()\n",
        )
        _check3(self, module, service, home, "r34 2048 f6")

    def test_2048_vars_subscript_inside_carriage(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod(key='INNER'):\n"
            "    return vars(OUTER)[key]\n",
        )
        _check3(self, module, service, home, "r34 2048 f7")

    def test_2048_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'PLAIN')\n",
            "def getmod(key='INNER'):\n"
            "    return getattr(OUTER, key)\n",
        )
        _records3(self, module, home, "r34 2048 plain")

    def test_2048_literal_accessor_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod():\n    return getattr(OUTER, 'INNER')\n",
        )
        _check3(self, module, service, home, "r34 2048 pole")


class TestConsumptionFixR34Consume1SecondClosureHome(
    unittest.TestCase
):
    """Ruling 2049: second order closure name at the home map."""

    _EXTRA = (
        "def _fac():\n    _n = 'HELD'\n    def _helper():\n"
        "        return _n\n    return _helper\n"
        "_helper = _fac()\n"
        "def mid():\n    return _helper()\n"
        "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
    )

    def test_2049_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2049")

    def test_2049_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _fac():\n    _n = 'PLAIN'\n    def _helper():\n"
            "        return _n\n    return _helper\n"
            "_helper = _fac()\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r34 2049 plain")

    def test_2049_first_order_closure_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[_helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2049 fo pole")

    def test_2049_second_order_default_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _helper(_n='HELD'):\n    return _n\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r34 2049 so pole")


class TestConsumptionFixR34Consume2SecondClosureForeign(
    unittest.TestCase
):
    """Ruling 2050: second order closure name, foreign module."""

    _EXTRA = TestConsumptionFixR34Consume1SecondClosureHome._EXTRA

    def test_2050_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2050 f1")

    def test_2050_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2050 f2")

    def test_2050_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def _fac():\n    _n = 'PLAIN'\n    def _helper():\n"
            "        return _n\n    return _helper\n"
            "_helper = _fac()\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r34 2050 plain")

    def test_2050_first_order_closure_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, _helper())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2050 fo pole")


class TestConsumptionFixR34Consume3SecondStringHome(
    unittest.TestCase
):
    """Ruling 2051: second order module string at home map."""

    _EXTRA = (
        "NAMESTR = 'HELD'\n"
        "def _helper():\n    return NAMESTR\n"
        "def mid():\n    return _helper()\n"
        "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
    )

    def test_2051_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2051")

    def test_2051_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "NAMESTR = 'PLAIN'\n"
            "def _helper():\n    return NAMESTR\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r34 2051 plain")

    def test_2051_first_order_string_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[_helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2051 fo pole")

    def test_2051_second_order_const_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _helper():\n    return 'HELD'\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r34 2051 so pole")


class TestConsumptionFixR34Consume4SecondStringForeign(
    unittest.TestCase
):
    """Ruling 2052: second order module string, foreign."""

    _EXTRA = TestConsumptionFixR34Consume3SecondStringHome._EXTRA

    def test_2052_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2052 f1")

    def test_2052_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2052 f2")

    def test_2052_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "NAMESTR = 'PLAIN'\n"
            "def _helper():\n    return NAMESTR\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r34 2052 plain")

    def test_2052_first_order_string_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, _helper())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2052 fo pole")


class TestConsumptionFixR34Consume5SecondContainerHome(
    unittest.TestCase
):
    """Ruling 2053: second order container element, home."""

    _EXTRA = (
        "BOX = {'k': 'HELD'}\n"
        "def _helper():\n    return BOX['k']\n"
        "def mid():\n    return _helper()\n"
        "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
    )

    def test_2053_home_index_dict(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2053 f1")

    def test_2053_home_index_list(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "BOX = ['HELD']\n"
            "def _helper():\n    return BOX[0]\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r34 2053 f2")

    def test_2053_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "BOX = {'k': 'PLAIN'}\n"
            "def _helper():\n    return BOX['k']\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r34 2053 plain")

    def test_2053_first_order_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[_helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2053 fo pole")


class TestConsumptionFixR34Consume6SecondContainerForeign(
    unittest.TestCase
):
    """Ruling 2054: second order container element, foreign."""

    _EXTRA = TestConsumptionFixR34Consume5SecondContainerHome._EXTRA

    def test_2054_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2054 f1")

    def test_2054_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2054 f2")

    def test_2054_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "BOX = {'k': 'PLAIN'}\n"
            "def _helper():\n    return BOX['k']\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r34 2054 plain")

    def test_2054_first_order_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, _helper())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2054 fo pole")


class TestConsumptionFixR34Consume7PairClosureHome(
    unittest.TestCase
):
    """Ruling 2055: pair function closure name at home map."""

    _CARRIER = (
        "def _fac():\n    _n = 'HELD'\n    def pf():\n"
        "        return _n\n    return pf\n"
        "pf = _fac()\n"
    )
    _EXTRA = (
        "def mid():\n    return CARRIER.pf()\n"
        "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
    )

    def test_2055_home_index(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            self._CARRIER,
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2055")

    def test_2055_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _fac():\n    _n = 'PLAIN'\n    def pf():\n"
            "        return _n\n    return pf\n"
            "pf = _fac()\n",
            self._EXTRA,
        )
        _records3(self, module, home, "r34 2055 plain")

    def test_2055_pair_const_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def pf():\n    return 'HELD'\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2055 pole")


class TestConsumptionFixR34Consume8PairClosureForeign(
    unittest.TestCase
):
    """Ruling 2056: pair function closure name, foreign."""

    _CARRIER = TestConsumptionFixR34Consume7PairClosureHome._CARRIER
    _EXTRA = TestConsumptionFixR34Consume7PairClosureHome._EXTRA

    def test_2056_foreign_getattr(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            self._CARRIER,
            self._EXTRA,
            with_target=True,
        )
        _check3(self, module, service, home, "r34 2056 f1")

    def test_2056_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[mid()]\n",
            self._CARRIER,
            self._EXTRA,
            with_target=True,
        )
        _check3(self, module, service, home, "r34 2056 f2")

    def test_2056_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def _fac():\n    _n = 'PLAIN'\n    def pf():\n"
            "        return _n\n    return pf\n"
            "pf = _fac()\n",
            self._EXTRA,
            with_target=True,
        )
        _records3(self, module, home, "r34 2056 plain")

    def test_2056_pair_const_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def pf():\n    return 'HELD'\n",
            self._EXTRA,
            with_target=True,
        )
        _check3(self, module, service, home, "r34 2056 pole")


class TestConsumptionFixR34Consume9PairDefaultHome(
    unittest.TestCase
):
    """Ruling 2057: pair function default name at home map."""

    _CARRIER = "def pf(_n='HELD'):\n    return _n\n"
    _EXTRA = TestConsumptionFixR34Consume7PairClosureHome._EXTRA

    def test_2057_home_index(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            self._CARRIER,
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2057")

    def test_2057_home_index_kwdefault(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def pf(*, _n='HELD'):\n    return _n\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2057 kw")

    def test_2057_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def pf(_n='PLAIN'):\n    return _n\n",
            self._EXTRA,
        )
        _records3(self, module, home, "r34 2057 plain")

    def test_2057_pair_const_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def pf():\n    return 'HELD'\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2057 pole")


class TestConsumptionFixR34Consume10PairDefaultForeign(
    unittest.TestCase
):
    """Ruling 2058: pair function default name, foreign."""

    _CARRIER = TestConsumptionFixR34Consume9PairDefaultHome._CARRIER
    _EXTRA = TestConsumptionFixR34Consume7PairClosureHome._EXTRA

    def test_2058_foreign_getattr(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            self._CARRIER,
            self._EXTRA,
            with_target=True,
        )
        _check3(self, module, service, home, "r34 2058 f1")

    def test_2058_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[mid()]\n",
            self._CARRIER,
            self._EXTRA,
            with_target=True,
        )
        _check3(self, module, service, home, "r34 2058 f2")

    def test_2058_plain_records(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def pf(_n='PLAIN'):\n    return _n\n",
            self._EXTRA,
            with_target=True,
        )
        _records3(self, module, home, "r34 2058 plain")

    def test_2058_pair_const_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def pf():\n    return 'HELD'\n",
            self._EXTRA,
            with_target=True,
        )
        _check3(self, module, service, home, "r34 2058 pole")


class TestConsumptionFixR34Consume11BytesClassAttr(
    unittest.TestCase
):
    """Ruling 2059: bytes attribute value of the member class."""

    def test_2059_self_bytes_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    NB = b'HELD'\n    def method(self):\n"
            "        return getattr(MOD, self.NB.decode())\n"
        )
        _check3(self, module, service, home, "r34 2059 f1")

    def test_2059_class_bytes_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    NB = b'HELD'\n    def method(self):\n"
            "        return getattr(MOD, K.NB.decode())\n"
        )
        _check3(self, module, service, home, "r34 2059 f2")

    def test_2059_self_bytes_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    NB = b'HELD'\n    def method(self):\n"
            "        return MOD.__dict__[self.NB.decode()]\n"
        )
        _check3(self, module, service, home, "r34 2059 f3")

    def test_2059_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    NB = b'PLAIN'\n    def method(self):\n"
            "        return getattr(MOD, self.NB.decode())\n"
        )
        _records3(self, module, home, "r34 2059 plain")

    def test_2059_string_attr_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    NB = 'HELD'\n    def method(self):\n"
            "        return getattr(MOD, self.NB)\n"
        )
        _check3(self, module, service, home, "r34 2059 pole")


class TestConsumptionFixR34Consume12BytesInstanceAssign(
    unittest.TestCase
):
    """Ruling 2060: bytes instance value by direct assignment."""

    def test_2060_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        self.NB = b'HELD'\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.NB.decode())\n"
        )
        _check3(self, module, service, home, "r34 2060 f1")

    def test_2060_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        self.NB = b'HELD'\n"
            "    def method(self):\n"
            "        return MOD.__dict__[self.NB.decode()]\n"
        )
        _check3(self, module, service, home, "r34 2060 f2")

    def test_2060_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        self.NB = b'PLAIN'\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.NB.decode())\n"
        )
        _records3(self, module, home, "r34 2060 plain")

    def test_2060_string_assign_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        self.NB = 'HELD'\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.NB)\n"
        )
        _check3(self, module, service, home, "r34 2060 pole")


class TestConsumptionFixR34Consume13BytesInstanceSetattr(
    unittest.TestCase
):
    """Ruling 2061: bytes instance value through setattr."""

    def test_2061_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        setattr(self, 'NB', b'HELD')\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.NB.decode())\n"
        )
        _check3(self, module, service, home, "r34 2061 f1")

    def test_2061_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        setattr(self, 'NB', b'HELD')\n"
            "    def method(self):\n"
            "        return MOD.__dict__[self.NB.decode()]\n"
        )
        _check3(self, module, service, home, "r34 2061 f2")

    def test_2061_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        setattr(self, 'NB', b'PLAIN')\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.NB.decode())\n"
        )
        _records3(self, module, home, "r34 2061 plain")

    def test_2061_string_setattr_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        setattr(self, 'NB', 'HELD')\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.NB)\n"
        )
        _check3(self, module, service, home, "r34 2061 pole")


class TestConsumptionFixR34Iso1PresentedAttrKey(
    unittest.TestCase
):
    """Ruling 2062: presentation key standing as attribute load."""

    def test_2062_vars_get_class_key_getattr(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    KEY = 'INNER'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER).get(Cls.KEY),"
            " 'HELD')\n"
        )
        _check3(self, module, service, home, "r34 2062 f1")

    def test_2062_vars_get_class_key_dict(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    KEY = 'INNER'\n"
            "class K:\n    def method(self):\n"
            "        return vars(OUTER).get(Cls.KEY)"
            ".__dict__['HELD']\n"
        )
        _check3(self, module, service, home, "r34 2062 f2")

    def test_2062_vars_get_self_key_getattr(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    KEY = 'INNER'\n"
            "    def method(self):\n"
            "        return getattr(vars(OUTER).get(self.KEY),"
            " 'HELD')\n"
        )
        _check3(self, module, service, home, "r34 2062 f3")

    def test_2062_dict_get_class_key_getattr(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    KEY = 'INNER'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.__dict__.get(Cls.KEY),"
            " 'HELD')\n"
        )
        _check3(self, module, service, home, "r34 2062 f4")

    def test_2062_exec_dict_get_self_key(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    KEY = 'INNER'\n"
            "    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD',"
            " OUTER.__dict__.get(self.KEY).__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, service, home, "r34 2062 f5")

    def test_2062_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    KEY = 'INNER'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER).get(Cls.KEY),"
            " 'PLAIN')\n"
        )
        _records3(self, module, home, "r34 2062 plain")

    def test_2062_literal_key_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER).get('INNER'),"
            " 'HELD')\n"
        )
        _check3(self, module, service, home, "r34 2062 lit pole")

    def test_2062_carried_key_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return getattr(vars(OUTER).get(k), 'HELD')\n"
        )
        _check3(self, module, service, home, "r34 2062 car pole")


class TestConsumptionFixR34Iso2ThirdHopChain(unittest.TestCase):
    """Ruling 2063: governed value at the third hop of a chain."""

    def test_2063_getattr_gathered(self):
        module, service = _mods(self)
        home = _deep_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.MID.INNER, Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r34 2063 f1")

    def test_2063_dict_subscript_gathered(self):
        module, service = _mods(self)
        home = _deep_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return OUTER.MID.INNER.__dict__[Cls.NAME]\n"
        )
        _check3(self, module, service, home, "r34 2063 f2")

    def test_2063_vars_subscript_gathered(self):
        module, service = _mods(self)
        home = _deep_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return vars(OUTER.MID.INNER)[Cls.NAME]\n"
        )
        _check3(self, module, service, home, "r34 2063 f3")

    def test_2063_getattr_literal(self):
        module, service = _mods(self)
        home = _deep_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.MID.INNER, 'HELD')\n"
        )
        _check3(self, module, service, home, "r34 2063 f4")

    def test_2063_dict_subscript_literal(self):
        module, service = _mods(self)
        home = _deep_home(
            "class K:\n    def method(self):\n"
            "        return OUTER.MID.INNER.__dict__['HELD']\n"
        )
        _check3(self, module, service, home, "r34 2063 f5")

    def test_2063_plain_records(self):
        module, service = _mods(self)
        home = _deep_home(
            "class Cls:\n    NAME = 'PLAIN'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.MID.INNER, Cls.NAME)\n"
        )
        _records3(self, module, home, "r34 2063 plain")

    def test_2063_second_hop_pole(self):
        module, service = _mods(self)
        home = _deep_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.INNER, Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r34 2063 hop2 pole")


class TestConsumptionFixR34Iso3SecondClosureClass(
    unittest.TestCase
):
    """Ruling 2064: second order closure name, class member."""

    _EXTRA = TestConsumptionFixR34Consume1SecondClosureHome._EXTRA

    def test_2064_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2064 f1")

    def test_2064_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2064 f2")

    def test_2064_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2064 f3")

    def test_2064_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def _fac():\n    _n = 'PLAIN'\n    def _helper():\n"
            "        return _n\n    return _helper\n"
            "_helper = _fac()\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r34 2064 plain")

    def test_2064_second_order_default_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _helper(_n='HELD'):\n    return _n\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r34 2064 so pole")


class TestConsumptionFixR34Iso4SecondContainerClass(
    unittest.TestCase
):
    """Ruling 2065: second order container element, class."""

    _EXTRA = TestConsumptionFixR34Consume5SecondContainerHome._EXTRA

    def test_2065_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2065 f1")

    def test_2065_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2065 f2")

    def test_2065_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "BOX = {'k': 'PLAIN'}\n"
            "def _helper():\n    return BOX['k']\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r34 2065 plain")

    def test_2065_first_order_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[_helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r34 2065 fo pole")
