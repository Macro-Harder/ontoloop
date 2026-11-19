"""Fix round 33 tests for rulings 1917 to 1935, Region 5.

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


def _make_module(body, name_hint="r33_region5_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r33_region5_sub")


def _chain_home(source, extra=""):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r33_region5_inner",
    )
    outer = _make_module("", "r33_region5_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(extra + source)
    home.__dict__["OUTER"] = outer
    return home


def _target_home(source, extra=""):
    target = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r33_region5_target",
    )
    home = _make_module(extra + source)
    home.__dict__["MOD"] = target
    return home


def _bytes_home(source, carrier_body, home_extra=""):
    target = _sub_module()
    carrier = _make_module(carrier_body, "r33_region5_carrier")
    home = _make_module(home_extra + source)
    home.__dict__["MOD"] = target
    home.__dict__["CARRIER"] = carrier
    return home


def _bytes2_home(source, inner_body):
    inner = _make_module(inner_body, "r33_region5_inner9")
    carrier = _make_module("", "r33_region5_carrier9")
    carrier.__dict__["INNER9"] = inner
    target = _sub_module()
    home = _make_module(source)
    home.__dict__["MOD"] = target
    home.__dict__["CARRIER"] = carrier
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


class TestConsumptionFixR33Iso1PresentedGatheredName(
    unittest.TestCase
):
    """Ruling 1917: presented modules under a gathered name."""

    def test_1917_getattr_dict_get_class_name(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'),"
            " Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1917 f1")

    def test_1917_vars_subscript_dict_get(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return vars(OUTER.__dict__.get('INNER'))"
            "[Cls.NAME]\n"
        )
        _check3(self, module, service, home, "r33 1917 f2")

    def test_1917_dict_subscript_dict_get(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return OUTER.__dict__.get('INNER')"
            ".__dict__[Cls.NAME]\n"
        )
        _check3(self, module, service, home, "r33 1917 f3")

    def test_1917_getattribute_dict_get(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return object.__getattribute__"
            "(OUTER.__dict__.get('INNER'), Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1917 f4")

    def test_1917_getattr_dict_get_self_name(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    NAME = 'HELD'\n"
            "    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'),"
            " self.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1917 f5")

    def test_1917_getattr_dict_subscript(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.__dict__['INNER'],"
            " Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1917 f6")

    def test_1917_getattr_vars_get(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER).get('INNER'),"
            " Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1917 f7")

    def test_1917_getattribute_chain(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return OUTER.INNER.__getattribute__(Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1917 f8")

    def test_1917_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'PLAIN'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'),"
            " Cls.NAME)\n"
        )
        _records3(self, module, home, "r33 1917 plain")

    def test_1917_literal_name_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'),"
            " 'HELD')\n"
        )
        _check3(self, module, service, home, "r33 1917 literal")

    def test_1917_exec_presentation_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD',"
            " OUTER.__dict__.get('INNER').__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, service, home, "r33 1917 exec pole")


class TestConsumptionFixR33Iso2ChainGatheredName(unittest.TestCase):
    """Ruling 1918: second hop chain under a gathered name."""

    def test_1918_getattr_chain(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.INNER, Cls.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1918 f1")

    def test_1918_dict_subscript_chain(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'HELD'\n"
            "class K:\n    def method(self):\n"
            "        return OUTER.INNER.__dict__[Cls.NAME]\n"
        )
        _check3(self, module, service, home, "r33 1918 f2")

    def test_1918_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class Cls:\n    NAME = 'PLAIN'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.INNER, Cls.NAME)\n"
        )
        _records3(self, module, home, "r33 1918 plain")

    def test_1918_literal_chain_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.INNER, 'HELD')\n"
        )
        _check3(self, module, service, home, "r33 1918 literal")


class TestConsumptionFixR33Iso3VarsGetCarriedKey(unittest.TestCase):
    """Ruling 1919: vars return get under a carried key."""

    def test_1919_getattr_default_key(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return getattr(vars(OUTER).get(k), 'HELD')\n"
        )
        _check3(self, module, service, home, "r33 1919 f1")

    def test_1919_dict_subscript_default_key(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return vars(OUTER).get(k).__dict__['HELD']\n"
        )
        _check3(self, module, service, home, "r33 1919 f2")

    def test_1919_vars_subscript_default_key(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return vars(vars(OUTER).get(k))['HELD']\n"
        )
        _check3(self, module, service, home, "r33 1919 f3")

    def test_1919_exec_default_key(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        loc = {}\n"
            "        exec('x = HELD', vars(OUTER).get(k).__dict__,"
            " loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, service, home, "r33 1919 f4")

    def test_1919_getattr_closure_key(self):
        module, service = _mods(self)
        home = _chain_home(
            "def _fac():\n    k = 'INNER'\n    class K:\n"
            "        def method(self):\n"
            "            return getattr(vars(OUTER).get(k),"
            " 'HELD')\n    return K\nK = _fac()\n"
        )
        _check3(self, module, service, home, "r33 1919 f5")

    def test_1919_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return getattr(vars(OUTER).get(k), 'PLAIN')\n"
        )
        _records3(self, module, home, "r33 1919 plain")

    def test_1919_literal_key_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER).get('INNER'),"
            " 'HELD')\n"
        )
        _check3(self, module, service, home, "r33 1919 literal")


class TestConsumptionFixR33Iso4SecondOrderDefault(unittest.TestCase):
    """Ruling 1920: second order helper default carriage."""

    _EXTRA = (
        "def _helper(_n='HELD'):\n    return _n\n"
        "def mid():\n    return _helper()\n"
        "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
    )

    def test_1920_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1920 f1")

    def test_1920_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1920 f2")

    def test_1920_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[mid()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1920 f3")

    def test_1920_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, mid())\n",
            "def _helper(_n='PLAIN'):\n    return _n\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n",
        )
        _records3(self, module, home, "r33 1920 plain")

    def test_1920_first_order_default_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            "def helper(_n='HELD'):\n    return _n\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1920 fo pole")

    def test_1920_second_order_const_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[mid()]\n",
            "def _helper():\n    return 'HELD'\n"
            "def mid():\n    return _helper()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1920 so pole")


class TestConsumptionFixR33Consume1ClosureHome(unittest.TestCase):
    """Ruling 1921: closure carried name at the home map."""

    _EXTRA = (
        "def _fac():\n    _n = 'HELD'\n    def helper():\n"
        "        return _n\n    return helper\n"
        "helper = _fac()\n"
        "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
    )

    def test_1921_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1921")

    def test_1921_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            "def _fac():\n    _n = 'PLAIN'\n    def helper():\n"
            "        return _n\n    return helper\n"
            "helper = _fac()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r33 1921 plain")

    def test_1921_default_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            "def helper(_n='HELD'):\n    return _n\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1921 pole")


class TestConsumptionFixR33Consume2ClosureForeign(unittest.TestCase):
    """Ruling 1922: closure carried name at a foreign module."""

    _EXTRA = TestConsumptionFixR33Consume1ClosureHome._EXTRA

    def test_1922_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1922 f1")

    def test_1922_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1922 f2")

    def test_1922_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            "def _fac():\n    _n = 'PLAIN'\n    def helper():\n"
            "        return _n\n    return helper\n"
            "helper = _fac()\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r33 1922 plain")

    def test_1922_default_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            "def helper(_n='HELD'):\n    return _n\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1922 pole")


class TestConsumptionFixR33Consume3ModuleStringHome(
    unittest.TestCase
):
    """Ruling 1923: module level string returned, home map."""

    _EXTRA = (
        "NAMESTR = 'HELD'\n"
        "def helper():\n    return NAMESTR\n"
        "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
    )

    def test_1923_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1923")

    def test_1923_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            "NAMESTR = 'PLAIN'\n"
            "def helper():\n    return NAMESTR\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r33 1923 plain")

    def test_1923_const_return_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            "def helper():\n    return 'HELD'\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1923 pole")


class TestConsumptionFixR33Consume4ModuleStringForeign(
    unittest.TestCase
):
    """Ruling 1924: module level string returned, foreign."""

    _EXTRA = TestConsumptionFixR33Consume3ModuleStringHome._EXTRA

    def test_1924_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1924 f1")

    def test_1924_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1924 f2")

    def test_1924_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            "NAMESTR = 'PLAIN'\n"
            "def helper():\n    return NAMESTR\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r33 1924 plain")

    def test_1924_const_return_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            "def helper():\n    return 'HELD'\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1924 pole")


class TestConsumptionFixR33Consume5BaseClassAttr(unittest.TestCase):
    """Ruling 1925: base class attribute value carriage."""

    def test_1925_getattr_class_load(self):
        module, service = _mods(self)
        home = _target_home(
            "class Base:\n    NAME = 'HELD'\n"
            "class K(Base):\n    def method(self):\n"
            "        return getattr(MOD, K.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1925 f1")

    def test_1925_getattr_self_load(self):
        module, service = _mods(self)
        home = _target_home(
            "class Base:\n    NAME = 'HELD'\n"
            "class K(Base):\n    def method(self):\n"
            "        return getattr(MOD, self.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1925 f2")

    def test_1925_dict_subscript_class_load(self):
        module, service = _mods(self)
        home = _target_home(
            "class Base:\n    NAME = 'HELD'\n"
            "class K(Base):\n    def method(self):\n"
            "        return MOD.__dict__[K.NAME]\n"
        )
        _check3(self, module, service, home, "r33 1925 f3")

    def test_1925_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class Base:\n    NAME = 'PLAIN'\n"
            "class K(Base):\n    def method(self):\n"
            "        return getattr(MOD, K.NAME)\n"
        )
        _records3(self, module, home, "r33 1925 plain")

    def test_1925_own_namespace_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    NAME = 'HELD'\n"
            "    def method(self):\n"
            "        return getattr(MOD, K.NAME)\n"
        )
        _check3(self, module, service, home, "r33 1925 pole")


class TestConsumptionFixR33Consume6SetattrInstance(unittest.TestCase):
    """Ruling 1926: instance attribute set through setattr."""

    def test_1926_getattr_setattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        setattr(self, 'nm', 'HELD')\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.nm)\n"
        )
        _check3(self, module, service, home, "r33 1926 f1")

    def test_1926_dict_subscript_setattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        setattr(self, 'nm', 'HELD')\n"
            "    def method(self):\n"
            "        return MOD.__dict__[self.nm]\n"
        )
        _check3(self, module, service, home, "r33 1926 f2")

    def test_1926_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        setattr(self, 'nm', 'PLAIN')\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.nm)\n"
        )
        _records3(self, module, home, "r33 1926 plain")

    def test_1926_direct_assign_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        self.nm = 'HELD'\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.nm)\n"
        )
        _check3(self, module, service, home, "r33 1926 pole")


class TestConsumptionFixR33Consume7BaseInitInstance(
    unittest.TestCase
):
    """Ruling 1927: instance attribute set in a base init."""

    def test_1927_getattr_base_init(self):
        module, service = _mods(self)
        home = _target_home(
            "class Base:\n    def __init__(self):\n"
            "        self.nm = 'HELD'\n"
            "class K(Base):\n    def method(self):\n"
            "        return getattr(MOD, self.nm)\n"
        )
        _check3(self, module, service, home, "r33 1927 f1")

    def test_1927_dict_subscript_base_init(self):
        module, service = _mods(self)
        home = _target_home(
            "class Base:\n    def __init__(self):\n"
            "        self.nm = 'HELD'\n"
            "class K(Base):\n    def method(self):\n"
            "        return MOD.__dict__[self.nm]\n"
        )
        _check3(self, module, service, home, "r33 1927 f2")

    def test_1927_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class Base:\n    def __init__(self):\n"
            "        self.nm = 'PLAIN'\n"
            "class K(Base):\n    def method(self):\n"
            "        return getattr(MOD, self.nm)\n"
        )
        _records3(self, module, home, "r33 1927 plain")

    def test_1927_own_init_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def __init__(self):\n"
            "        self.nm = 'HELD'\n"
            "    def method(self):\n"
            "        return getattr(MOD, self.nm)\n"
        )
        _check3(self, module, service, home, "r33 1927 pole")


class TestConsumptionFixR33Consume8BytesAttrModule(unittest.TestCase):
    """Ruling 1928: decoded bytes attribute of a module."""

    def test_1928_getattr_bytes_attr(self):
        module, service = _mods(self)
        home = _bytes_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, CARRIER.DATA.decode())\n",
            "DATA = b'HELD'\n",
        )
        _check3(self, module, service, home, "r33 1928 f1")

    def test_1928_dict_subscript_bytes_attr(self):
        module, service = _mods(self)
        home = _bytes_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[CARRIER.DATA.decode()]\n",
            "DATA = b'HELD'\n",
        )
        _check3(self, module, service, home, "r33 1928 f2")

    def test_1928_plain_records(self):
        module, service = _mods(self)
        home = _bytes_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, CARRIER.DATA.decode())\n",
            "DATA = b'PLAIN'\n",
        )
        _records3(self, module, home, "r33 1928 plain")

    def test_1928_string_attr_pole(self):
        module, service = _mods(self)
        home = _bytes_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, CARRIER.DATA)\n",
            "DATA = 'HELD'\n",
        )
        _check3(self, module, service, home, "r33 1928 pole")

    def test_1928_home_index_bytes_pole(self):
        module, service = _mods(self)
        home = _bytes_home(
            "class K:\n    def method(self):\n"
            "        return globals()[CARRIER.DATA.decode()]\n",
            "DATA = b'HELD'\n",
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1928 home pole")


class TestConsumptionFixR33Consume9BytesAttrTwoHop(
    unittest.TestCase
):
    """Ruling 1929: decoded bytes attribute at a second hop."""

    def test_1929_getattr_two_hop_bytes(self):
        module, service = _mods(self)
        home = _bytes2_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD,"
            " CARRIER.INNER9.DATA.decode())\n",
            "DATA = b'HELD'\n",
        )
        _check3(self, module, service, home, "r33 1929 f1")

    def test_1929_dict_subscript_two_hop_bytes(self):
        module, service = _mods(self)
        home = _bytes2_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__"
            "[CARRIER.INNER9.DATA.decode()]\n",
            "DATA = b'HELD'\n",
        )
        _check3(self, module, service, home, "r33 1929 f2")

    def test_1929_plain_records(self):
        module, service = _mods(self)
        home = _bytes2_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD,"
            " CARRIER.INNER9.DATA.decode())\n",
            "DATA = b'PLAIN'\n",
        )
        _records3(self, module, home, "r33 1929 plain")

    def test_1929_string_two_hop_pole(self):
        module, service = _mods(self)
        home = _bytes2_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, CARRIER.INNER9.DATA)\n",
            "DATA = 'HELD'\n",
        )
        _check3(self, module, service, home, "r33 1929 pole")


class TestConsumptionFixR33Consume10ContainerHome(
    unittest.TestCase
):
    """Ruling 1930: container element returned, home map."""

    _EXTRA = (
        "BOX = {'k': 'HELD'}\n"
        "def helper():\n    return BOX['k']\n"
        "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
    )

    def test_1930_home_index(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1930")

    def test_1930_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[helper()]\n",
            "BOX = {'k': 'PLAIN'}\n"
            "def helper():\n    return BOX['k']\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r33 1930 plain")

    def test_1930_member_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return globals()[BOX['k']]\n",
            "BOX = {'k': 'HELD'}\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1930 pole")


class TestConsumptionFixR33Consume11ContainerForeign(
    unittest.TestCase
):
    """Ruling 1931: container element returned, foreign."""

    _EXTRA = TestConsumptionFixR33Consume10ContainerHome._EXTRA

    def test_1931_foreign_getattr(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1931 f1")

    def test_1931_foreign_dict_subscript(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return MOD.__dict__[helper()]\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1931 f2")

    def test_1931_plain_records(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, helper())\n",
            "BOX = {'k': 'PLAIN'}\n"
            "def helper():\n    return BOX['k']\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _records3(self, module, home, "r33 1931 plain")

    def test_1931_member_container_pole(self):
        module, service = _mods(self)
        home = _target_home(
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, BOX['k'])\n",
            "BOX = {'k': 'HELD'}\n"
            "import threading\nHELD = threading.Lock()\n"
            "PLAIN = 7\n",
        )
        _check3(self, module, service, home, "r33 1931 pole")


class TestConsumptionFixR33Chair1CallResultModule(unittest.TestCase):
    """Ruling 1932: module standing as a call result."""

    _EXTRA = "def getmod():\n    return OUTER.INNER\n"

    def test_1932_getattr_call_result(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1932 f1")

    def test_1932_vars_subscript_call_result(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return vars(getmod())['HELD']\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1932 f2")

    def test_1932_dict_subscript_call_result(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getmod().__dict__['HELD']\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1932 f3")

    def test_1932_exec_call_result(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', getmod().__dict__, loc)\n"
            "        return loc['x']\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1932 f4")

    def test_1932_second_order_call_result(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod2(), 'HELD')\n",
            "def _inner_fn():\n    return OUTER.INNER\n"
            "def getmod2():\n    return _inner_fn()\n",
        )
        _check3(self, module, service, home, "r33 1932 f5")

    def test_1932_dict_get_inside_helper(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod():\n"
            "    return OUTER.__dict__.get('INNER')\n",
        )
        _check3(self, module, service, home, "r33 1932 f6")

    def test_1932_getattr_inside_helper(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod():\n    return getattr(OUTER, 'INNER')\n",
        )
        _check3(self, module, service, home, "r33 1932 f7")

    def test_1932_vars_get_inside_helper(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod():\n    return vars(OUTER).get('INNER')\n",
        )
        _check3(self, module, service, home, "r33 1932 f8")

    def test_1932_getattribute_inside_helper(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod():\n"
            "    return object.__getattribute__(OUTER, 'INNER')\n",
        )
        _check3(self, module, service, home, "r33 1932 f9")

    def test_1932_module_attr_function(self):
        module, service = _mods(self)
        inner = _sub_module()
        outer = _make_module("", "r33_region5_outer10")
        outer.__dict__["INNER"] = inner
        carrier = _make_module(
            "def getmod():\n    return OUTER.INNER\n",
            "r33_region5_carrier10",
        )
        carrier.__dict__["OUTER"] = outer
        home = _make_module(
            "class K:\n    def method(self):\n"
            "        return getattr(CARRIER.getmod(), 'HELD')\n"
        )
        home.__dict__["OUTER"] = outer
        home.__dict__["CARRIER"] = carrier
        _check3(self, module, service, home, "r33 1932 f10")

    def test_1932_lambda_helper(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "getmod = lambda: OUTER.INNER\n",
        )
        _check3(self, module, service, home, "r33 1932 f11")

    def test_1932_method_of_class(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(Holder2().getmod(), 'HELD')\n",
            "class Holder2:\n    def getmod(self):\n"
            "        return OUTER.INNER\n",
        )
        _check3(self, module, service, home, "r33 1932 f12")

    def test_1932_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'PLAIN')\n",
            self._EXTRA,
        )
        _records3(self, module, home, "r33 1932 plain")

    def test_1932_arg_return_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(passthrough(OUTER.INNER),"
            " 'HELD')\n",
            "def passthrough(m):\n    return m\n",
        )
        _check3(self, module, service, home, "r33 1932 pole")

    def test_1932_accessor_literal_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.__dict__.get('INNER'),"
            " 'HELD')\n"
        )
        _check3(self, module, service, home, "r33 1932 acc pole")


class TestConsumptionFixR33Chair2VarsGetCarriedPresented(
    unittest.TestCase
):
    """Ruling 1933: presented acts on a vars get carried result."""

    def test_1933_getattr_carried(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return getattr(vars(OUTER).get(k), 'HELD')\n"
        )
        _check3(self, module, service, home, "r33 1933 f1")

    def test_1933_vars_subscript_carried(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return vars(vars(OUTER).get(k))['HELD']\n"
        )
        _check3(self, module, service, home, "r33 1933 f2")

    def test_1933_dict_subscript_carried(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return vars(OUTER).get(k).__dict__['HELD']\n"
        )
        _check3(self, module, service, home, "r33 1933 f3")

    def test_1933_getattr_closure_key(self):
        module, service = _mods(self)
        home = _chain_home(
            "def _fac():\n    k = 'INNER'\n    class K:\n"
            "        def method(self):\n"
            "            return getattr(vars(OUTER).get(k),"
            " 'HELD')\n    return K\nK = _fac()\n"
        )
        _check3(self, module, service, home, "r33 1933 f4")

    def test_1933_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return getattr(vars(OUTER).get(k), 'PLAIN')\n"
        )
        _records3(self, module, home, "r33 1933 plain")

    def test_1933_literal_key_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER).get('INNER'),"
            " 'HELD')\n"
        )
        _check3(self, module, service, home, "r33 1933 pole")


class TestConsumptionFixR33Chair3VarsGetCarriedExec(
    unittest.TestCase
):
    """Ruling 1934: exec on a vars get carried result mapping."""

    def test_1934_exec_carried(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        loc = {}\n"
            "        exec('x = HELD', vars(OUTER).get(k).__dict__,"
            " loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, service, home, "r33 1934")

    def test_1934_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        loc = {}\n"
            "        exec('x = PLAIN', vars(OUTER).get(k).__dict__,"
            " loc)\n"
            "        return loc['x']\n"
        )
        _records3(self, module, home, "r33 1934 plain")

    def test_1934_literal_key_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD',"
            " vars(OUTER).get('INNER').__dict__, loc)\n"
            "        return loc['x']\n"
        )
        _check3(self, module, service, home, "r33 1934 pole")

    def test_1934_presented_pole_beside(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self, k='INNER'):\n"
            "        return getattr(vars(OUTER).get(k), 'HELD')\n"
        )
        _check3(self, module, service, home, "r33 1934 beside")


class TestConsumptionFixR33Chair4HomeGlobalsNameBase(
    unittest.TestCase
):
    """Ruling 1935: presented bases under a home globals name."""

    _EXTRA = "KEY = 'INNER'\n"

    def test_1935_getattr_getattr_base(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getattr(OUTER, KEY), 'HELD')\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1935 f1")

    def test_1935_vars_subscript_getattr_base(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return vars(getattr(OUTER, KEY))['HELD']\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1935 f2")

    def test_1935_dict_subscript_getattr_base(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER, KEY).__dict__['HELD']\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1935 f3")

    def test_1935_getattr_vars_subscript_base(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(vars(OUTER)[KEY], 'HELD')\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1935 f4")

    def test_1935_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getattr(OUTER, KEY), 'PLAIN')\n",
            self._EXTRA,
        )
        _records3(self, module, home, "r33 1935 plain")

    def test_1935_exec_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', getattr(OUTER, KEY).__dict__,"
            " loc)\n"
            "        return loc['x']\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1935 exec pole")

    def test_1935_dict_get_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(OUTER.__dict__.get(KEY),"
            " 'HELD')\n",
            self._EXTRA,
        )
        _check3(self, module, service, home, "r33 1935 get pole")


if __name__ == "__main__":
    unittest.main()
