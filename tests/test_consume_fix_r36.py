"""Fix round 36 tests for rulings 2308 to 2333, Regions 5 and 6.

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


def _make_module(body, name_hint="r36_region56_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r36_region56_sub")


def _chain_home(source, extra=""):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r36_region56_inner",
    )
    outer = _make_module("", "r36_region56_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(extra + source)
    home.__dict__["OUTER"] = outer
    return home


def _target_home(source, extra=""):
    target = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r36_region56_target",
    )
    home = _make_module(extra + source)
    home.__dict__["MOD"] = target
    return home


def _pair_home(source, carrier_body, extra="", with_target=False):
    carrier = _make_module(carrier_body, "r36_region56_carrier")
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

_HOME_SRC = (
    "class K:\n    def method(self):\n"
    "        return globals()[helper()]\n"
)
_GA_SRC = (
    "class K:\n    def method(self):\n"
    "        return getattr(MOD, helper())\n"
)
_GS_SRC = (
    "class K:\n    def method(self):\n"
    "        return MOD.__dict__[helper()]\n"
)


class TestConsumeFixR36Chair1VarsSubscriptContainer(
    unittest.TestCase
):
    """Ruling 2308: vars subscript return under a container name."""

    def test_2308_getattr_tuple_default(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod(_k=('INNER',)):\n"
            "    return vars(OUTER)[_k[0]]\n",
        )
        _check3(self, module, service, home, "r36 2308 f1")

    def test_2308_vars_subscript_list_default(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return vars(getmod())['HELD']\n",
            "def getmod(_k=['INNER']):\n"
            "    return vars(OUTER)[_k[0]]\n",
        )
        _check3(self, module, service, home, "r36 2308 f2")

    def test_2308_dict_subscript_dict_default(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getmod().__dict__['HELD']\n",
            "def getmod(_k={'k': 'INNER'}):\n"
            "    return vars(OUTER)[_k['k']]\n",
        )
        _check3(self, module, service, home, "r36 2308 f3")

    def test_2308_exec_tuple_default(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec('x = HELD', getmod().__dict__, loc)\n"
            "        return loc['x']\n",
            "def getmod(_k=('INNER',)):\n"
            "    return vars(OUTER)[_k[0]]\n",
        )
        _check3(self, module, service, home, "r36 2308 f4")

    def test_2308_getattr_globals_list(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "KEYS = ['INNER']\n"
            "def getmod():\n    return vars(OUTER)[KEYS[0]]\n",
        )
        _check3(self, module, service, home, "r36 2308 f5")

    def test_2308_getattr_closure_list(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def _fac():\n    _k = ['INNER']\n    def getmod():\n"
            "        return vars(OUTER)[_k[0]]\n"
            "    return getmod\n"
            "getmod = _fac()\n",
        )
        _check3(self, module, service, home, "r36 2308 f6")

    def test_2308_direct_string_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "def getmod(key='INNER'):\n"
            "    return vars(OUTER)[key]\n",
        )
        _check3(self, module, service, home, "r36 2308 pole1")

    def test_2308_globals_string_pole(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'HELD')\n",
            "KEY = 'INNER'\n"
            "def getmod():\n    return vars(OUTER)[KEY]\n",
        )
        _check3(self, module, service, home, "r36 2308 pole2")

    def test_2308_plain_records(self):
        module, service = _mods(self)
        home = _chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'PLAIN')\n",
            "def getmod(_k=('INNER',)):\n"
            "    return vars(OUTER)[_k[0]]\n",
        )
        _records3(self, module, home, "r36 2308 plain")


_FOURTH_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def fourth():\n"
    "        return _n\n    return fourth\n"
    "fourth = _fac()\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FOURTH_STRING = (
    "STR = 'HELD'\n"
    "def fourth():\n    return STR\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FOURTH_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def fourth():\n    return D['k']\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FOURTH_DEFAULT = (
    "def fourth(_n='HELD'):\n    return _n\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_THIRD_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def third():\n"
    "        return _n\n    return third\n"
    "third = _fac()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL


def _fourth_home(case, source, body, label):
    module, service = _mods(case)
    home = _target_home(source, body)
    _check3(case, module, service, home, label)


def _fourth_plain(case, source, body, label):
    module, service = _mods(case)
    home = _target_home(source, body.replace("'HELD'", "'PLAIN'"))
    _records3(case, module, home, label)


class TestConsumeFixR36Consume1FourthClosureHome(
    unittest.TestCase
):
    """Ruling 2309: fourth order closure name at the home map."""

    def test_2309_home_index(self):
        _fourth_home(
            self, _HOME_SRC, _FOURTH_CLOSURE, "r36 2309 home"
        )

    def test_2309_plain_records(self):
        _fourth_plain(
            self, _HOME_SRC, _FOURTH_CLOSURE, "r36 2309 plain"
        )

    def test_2309_third_order_pole(self):
        _fourth_home(
            self, _HOME_SRC, _THIRD_CLOSURE, "r36 2309 pole"
        )


class TestConsumeFixR36Consume2FourthClosureForeign(
    unittest.TestCase
):
    """Ruling 2310: fourth order closure name at a foreign module."""

    def test_2310_foreign_getattr(self):
        _fourth_home(
            self, _GA_SRC, _FOURTH_CLOSURE, "r36 2310 ga"
        )

    def test_2310_foreign_dict_subscript(self):
        _fourth_home(
            self, _GS_SRC, _FOURTH_CLOSURE, "r36 2310 gs"
        )

    def test_2310_plain_records(self):
        _fourth_plain(
            self, _GA_SRC, _FOURTH_CLOSURE, "r36 2310 plain"
        )

    def test_2310_third_order_pole(self):
        _fourth_home(
            self, _GA_SRC, _THIRD_CLOSURE, "r36 2310 pole"
        )


class TestConsumeFixR36Consume3FourthStringHome(
    unittest.TestCase
):
    """Ruling 2311: fourth order module string at the home map."""

    def test_2311_home_index(self):
        _fourth_home(
            self, _HOME_SRC, _FOURTH_STRING, "r36 2311 home"
        )

    def test_2311_plain_records(self):
        _fourth_plain(
            self, _HOME_SRC, _FOURTH_STRING, "r36 2311 plain"
        )


class TestConsumeFixR36Consume4FourthStringForeign(
    unittest.TestCase
):
    """Ruling 2312: fourth order module string, foreign module."""

    def test_2312_foreign_getattr(self):
        _fourth_home(
            self, _GA_SRC, _FOURTH_STRING, "r36 2312 ga"
        )

    def test_2312_foreign_dict_subscript(self):
        _fourth_home(
            self, _GS_SRC, _FOURTH_STRING, "r36 2312 gs"
        )

    def test_2312_plain_records(self):
        _fourth_plain(
            self, _GA_SRC, _FOURTH_STRING, "r36 2312 plain"
        )


class TestConsumeFixR36Consume5FourthContainerHome(
    unittest.TestCase
):
    """Ruling 2313: fourth order container element, home map."""

    def test_2313_home_index(self):
        _fourth_home(
            self, _HOME_SRC, _FOURTH_CONTAINER, "r36 2313 home"
        )

    def test_2313_plain_records(self):
        _fourth_plain(
            self, _HOME_SRC, _FOURTH_CONTAINER, "r36 2313 plain"
        )


class TestConsumeFixR36Consume6FourthContainerForeign(
    unittest.TestCase
):
    """Ruling 2314: fourth order container element, foreign."""

    def test_2314_foreign_getattr(self):
        _fourth_home(
            self, _GA_SRC, _FOURTH_CONTAINER, "r36 2314 ga"
        )

    def test_2314_foreign_dict_subscript(self):
        _fourth_home(
            self, _GS_SRC, _FOURTH_CONTAINER, "r36 2314 gs"
        )

    def test_2314_plain_records(self):
        _fourth_plain(
            self, _GA_SRC, _FOURTH_CONTAINER, "r36 2314 plain"
        )


class TestConsumeFixR36Consume7FourthDefaultHome(
    unittest.TestCase
):
    """Ruling 2315: fourth order default name at the home map."""

    def test_2315_home_index(self):
        _fourth_home(
            self, _HOME_SRC, _FOURTH_DEFAULT, "r36 2315 home"
        )

    def test_2315_plain_records(self):
        _fourth_plain(
            self, _HOME_SRC, _FOURTH_DEFAULT, "r36 2315 plain"
        )


class TestConsumeFixR36Consume8FourthDefaultForeign(
    unittest.TestCase
):
    """Ruling 2316: fourth order default name, foreign module."""

    def test_2316_foreign_getattr(self):
        _fourth_home(
            self, _GA_SRC, _FOURTH_DEFAULT, "r36 2316 ga"
        )

    def test_2316_foreign_dict_subscript(self):
        _fourth_home(
            self, _GS_SRC, _FOURTH_DEFAULT, "r36 2316 gs"
        )

    def test_2316_plain_records(self):
        _fourth_plain(
            self, _GA_SRC, _FOURTH_DEFAULT, "r36 2316 plain"
        )


_PAIR_INNER = (
    "STR = 'HELD'\n"
    "D = {'k': 'HELD'}\n"
    "def qstr():\n    return STR\n"
    "def pstr2():\n    return qstr()\n"
    "def qbox():\n    return D['k']\n"
    "def pbox2():\n    return qbox()\n"
    "def _fac():\n    _n = 'HELD'\n    def qclos():\n"
    "        return _n\n    return qclos\n"
    "qclos = _fac()\n"
    "def pclos2():\n    return qclos()\n"
    "def qdef(_n='HELD'):\n    return _n\n"
    "def pdef2():\n    return qdef()\n"
    "def pstr():\n    return STR\n"
)

_PAIR_DIRECT = (
    "STR = 'HELD'\n"
    "D = {'k': 'HELD'}\n"
    "def pstr():\n    return STR\n"
    "def pbox():\n    return D['k']\n"
)


def _pair_inner_home(case, source, px, label, plain=False):
    module, service = _mods(case)
    carrier = _PAIR_INNER
    if plain:
        carrier = carrier.replace("'HELD'", "'PLAIN'")
    home = _pair_home(
        source, carrier,
        "def helper():\n    return CARRIER.%s()\n" % px
        + _HOME_TAIL,
        with_target=True,
    )
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR36Consume9PairInnerStringHome(
    unittest.TestCase
):
    """Ruling 2317: pair inner module string at the home map."""

    def test_2317_home_index(self):
        _pair_inner_home(
            self, _HOME_SRC, "pstr2", "r36 2317 home"
        )

    def test_2317_plain_records(self):
        _pair_inner_home(
            self, _HOME_SRC, "pstr2", "r36 2317 plain",
            plain=True,
        )

    def test_2317_pair_direct_pole(self):
        module, service = _mods(self)
        home = _pair_home(
            _HOME_SRC, _PAIR_INNER,
            "def helper():\n    return CARRIER.pstr()\n"
            + _HOME_TAIL,
            with_target=True,
        )
        _check3(self, module, service, home, "r36 2317 pole")


class TestConsumeFixR36Consume10PairInnerStringForeign(
    unittest.TestCase
):
    """Ruling 2318: pair inner module string, foreign module."""

    def test_2318_foreign_getattr(self):
        _pair_inner_home(
            self, _GA_SRC, "pstr2", "r36 2318 ga"
        )

    def test_2318_foreign_dict_subscript(self):
        _pair_inner_home(
            self, _GS_SRC, "pstr2", "r36 2318 gs"
        )

    def test_2318_plain_records(self):
        _pair_inner_home(
            self, _GA_SRC, "pstr2", "r36 2318 plain",
            plain=True,
        )


class TestConsumeFixR36Consume11PairInnerContainerHome(
    unittest.TestCase
):
    """Ruling 2319: pair inner container element, home map."""

    def test_2319_home_index(self):
        _pair_inner_home(
            self, _HOME_SRC, "pbox2", "r36 2319 home"
        )

    def test_2319_plain_records(self):
        _pair_inner_home(
            self, _HOME_SRC, "pbox2", "r36 2319 plain",
            plain=True,
        )


class TestConsumeFixR36Consume12PairInnerContainerForeign(
    unittest.TestCase
):
    """Ruling 2320: pair inner container element, foreign."""

    def test_2320_foreign_getattr(self):
        _pair_inner_home(
            self, _GA_SRC, "pbox2", "r36 2320 ga"
        )

    def test_2320_foreign_dict_subscript(self):
        _pair_inner_home(
            self, _GS_SRC, "pbox2", "r36 2320 gs"
        )

    def test_2320_plain_records(self):
        _pair_inner_home(
            self, _GA_SRC, "pbox2", "r36 2320 plain",
            plain=True,
        )


class TestConsumeFixR36Consume13PairInnerClosureHome(
    unittest.TestCase
):
    """Ruling 2321: pair inner closure name at the home map."""

    def test_2321_home_index(self):
        _pair_inner_home(
            self, _HOME_SRC, "pclos2", "r36 2321 home"
        )

    def test_2321_plain_records(self):
        _pair_inner_home(
            self, _HOME_SRC, "pclos2", "r36 2321 plain",
            plain=True,
        )


class TestConsumeFixR36Consume14PairInnerClosureForeign(
    unittest.TestCase
):
    """Ruling 2322: pair inner closure name, foreign module."""

    def test_2322_foreign_getattr(self):
        _pair_inner_home(
            self, _GA_SRC, "pclos2", "r36 2322 ga"
        )

    def test_2322_foreign_dict_subscript(self):
        _pair_inner_home(
            self, _GS_SRC, "pclos2", "r36 2322 gs"
        )

    def test_2322_plain_records(self):
        _pair_inner_home(
            self, _GA_SRC, "pclos2", "r36 2322 plain",
            plain=True,
        )


class TestConsumeFixR36Consume15PairInnerDefaultHome(
    unittest.TestCase
):
    """Ruling 2323: pair inner default name at the home map."""

    def test_2323_home_index(self):
        _pair_inner_home(
            self, _HOME_SRC, "pdef2", "r36 2323 home"
        )

    def test_2323_plain_records(self):
        _pair_inner_home(
            self, _HOME_SRC, "pdef2", "r36 2323 plain",
            plain=True,
        )


class TestConsumeFixR36Consume16PairInnerDefaultForeign(
    unittest.TestCase
):
    """Ruling 2324: pair inner default name, foreign module."""

    def test_2324_foreign_getattr(self):
        _pair_inner_home(
            self, _GA_SRC, "pdef2", "r36 2324 ga"
        )

    def test_2324_foreign_dict_subscript(self):
        _pair_inner_home(
            self, _GS_SRC, "pdef2", "r36 2324 gs"
        )

    def test_2324_plain_records(self):
        _pair_inner_home(
            self, _GA_SRC, "pdef2", "r36 2324 plain",
            plain=True,
        )


def _member_pair(case, source, carrier, call, label, plain=False):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _pair_home(source, body, "", with_target=True)
    home.__dict__["_call"] = call
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


def _mp_source(call, act):
    if act == "ga":
        return (
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, %s)\n" % call
        )
    return (
        "class K:\n    def method(self):\n"
        "        return MOD.__dict__[%s]\n" % call
    )


class TestConsumeFixR36Consume17MemberPairStringDirect(
    unittest.TestCase
):
    """Ruling 2325: member direct pair module string, foreign."""

    def test_2325_foreign_getattr(self):
        _member_pair(
            self, _mp_source("CARRIER.pstr()", "ga"),
            _PAIR_DIRECT, "CARRIER.pstr()", "r36 2325 ga",
        )

    def test_2325_foreign_dict_subscript(self):
        _member_pair(
            self, _mp_source("CARRIER.pstr()", "gs"),
            _PAIR_DIRECT, "CARRIER.pstr()", "r36 2325 gs",
        )

    def test_2325_plain_records(self):
        _member_pair(
            self, _mp_source("CARRIER.pstr()", "ga"),
            _PAIR_DIRECT, "CARRIER.pstr()", "r36 2325 plain",
            plain=True,
        )


class TestConsumeFixR36Consume18MemberPairContainerDirect(
    unittest.TestCase
):
    """Ruling 2326: member direct pair container, foreign."""

    def test_2326_foreign_getattr(self):
        _member_pair(
            self, _mp_source("CARRIER.pbox()", "ga"),
            _PAIR_DIRECT, "CARRIER.pbox()", "r36 2326 ga",
        )

    def test_2326_foreign_dict_subscript(self):
        _member_pair(
            self, _mp_source("CARRIER.pbox()", "gs"),
            _PAIR_DIRECT, "CARRIER.pbox()", "r36 2326 gs",
        )

    def test_2326_plain_records(self):
        _member_pair(
            self, _mp_source("CARRIER.pbox()", "ga"),
            _PAIR_DIRECT, "CARRIER.pbox()", "r36 2326 plain",
            plain=True,
        )


class TestConsumeFixR36Consume19MemberPairInnerString(
    unittest.TestCase
):
    """Ruling 2327: member direct pair inner string, foreign."""

    def test_2327_foreign_getattr(self):
        _member_pair(
            self, _mp_source("CARRIER.pstr2()", "ga"),
            _PAIR_INNER, "CARRIER.pstr2()", "r36 2327 ga",
        )

    def test_2327_foreign_dict_subscript(self):
        _member_pair(
            self, _mp_source("CARRIER.pstr2()", "gs"),
            _PAIR_INNER, "CARRIER.pstr2()", "r36 2327 gs",
        )

    def test_2327_plain_records(self):
        _member_pair(
            self, _mp_source("CARRIER.pstr2()", "ga"),
            _PAIR_INNER, "CARRIER.pstr2()", "r36 2327 plain",
            plain=True,
        )


class TestConsumeFixR36Consume20MemberPairInnerContainer(
    unittest.TestCase
):
    """Ruling 2328: member direct pair inner container."""

    def test_2328_foreign_getattr(self):
        _member_pair(
            self, _mp_source("CARRIER.pbox2()", "ga"),
            _PAIR_INNER, "CARRIER.pbox2()", "r36 2328 ga",
        )

    def test_2328_foreign_dict_subscript(self):
        _member_pair(
            self, _mp_source("CARRIER.pbox2()", "gs"),
            _PAIR_INNER, "CARRIER.pbox2()", "r36 2328 gs",
        )

    def test_2328_plain_records(self):
        _member_pair(
            self, _mp_source("CARRIER.pbox2()", "ga"),
            _PAIR_INNER, "CARRIER.pbox2()", "r36 2328 plain",
            plain=True,
        )


class TestConsumeFixR36Consume21MemberPairInnerClosure(
    unittest.TestCase
):
    """Ruling 2329: member direct pair inner closure, foreign."""

    def test_2329_foreign_getattr(self):
        _member_pair(
            self, _mp_source("CARRIER.pclos2()", "ga"),
            _PAIR_INNER, "CARRIER.pclos2()", "r36 2329 ga",
        )

    def test_2329_foreign_dict_subscript(self):
        _member_pair(
            self, _mp_source("CARRIER.pclos2()", "gs"),
            _PAIR_INNER, "CARRIER.pclos2()", "r36 2329 gs",
        )

    def test_2329_plain_records(self):
        _member_pair(
            self, _mp_source("CARRIER.pclos2()", "ga"),
            _PAIR_INNER, "CARRIER.pclos2()", "r36 2329 plain",
            plain=True,
        )


class TestConsumeFixR36Consume22MemberPairInnerDefault(
    unittest.TestCase
):
    """Ruling 2330: member direct pair inner default, foreign."""

    def test_2330_foreign_getattr(self):
        _member_pair(
            self, _mp_source("CARRIER.pdef2()", "ga"),
            _PAIR_INNER, "CARRIER.pdef2()", "r36 2330 ga",
        )

    def test_2330_foreign_dict_subscript(self):
        _member_pair(
            self, _mp_source("CARRIER.pdef2()", "gs"),
            _PAIR_INNER, "CARRIER.pdef2()", "r36 2330 gs",
        )

    def test_2330_plain_records(self):
        _member_pair(
            self, _mp_source("CARRIER.pdef2()", "ga"),
            _PAIR_INNER, "CARRIER.pdef2()", "r36 2330 plain",
            plain=True,
        )


def _deep_chain_home(source, cls_name="HELD", leaf_extra=""):
    leaf = _make_module(
        "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
        + leaf_extra,
        "r36_region56_leaf",
    )
    l3 = _make_module("", "r36_region56_l3")
    l3.__dict__["LEAF"] = leaf
    l2 = _make_module("", "r36_region56_l2")
    l2.__dict__["L3"] = l3
    l1 = _make_module("", "r36_region56_l1")
    l1.__dict__["L2"] = l2
    outer = _make_module("", "r36_region56_outer")
    outer.__dict__["L1"] = l1
    home = _make_module(source)
    home.__dict__["OUTER"] = outer
    cls = _make_module("", "r36_region56_clsmod")
    home.__dict__["Cls"] = type(
        "Cls", (), {"NAME": cls_name}
    )
    return home


class TestConsumeFixR36Iso1FifthHopChain(unittest.TestCase):
    """Ruling 2331: governed value at the fifth hop of a chain."""

    def test_2331_getattr_gathered(self):
        module, service = _mods(self)
        home = _deep_chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(\n"
            "            OUTER.L1.L2.L3.LEAF, Cls.NAME\n"
            "        )\n"
        )
        _check3(self, module, service, home, "r36 2331 ga")

    def test_2331_dict_subscript_literal(self):
        module, service = _mods(self)
        home = _deep_chain_home(
            "class K:\n    def method(self):\n"
            "        return OUTER.L1.L2.L3.LEAF.__dict__[\n"
            "            'HELD'\n"
            "        ]\n"
        )
        _check3(self, module, service, home, "r36 2331 ds")

    def test_2331_vars_subscript_gathered(self):
        module, service = _mods(self)
        home = _deep_chain_home(
            "class K:\n    def method(self):\n"
            "        return vars(OUTER.L1.L2.L3.LEAF)[\n"
            "            Cls.NAME\n"
            "        ]\n"
        )
        _check3(self, module, service, home, "r36 2331 vs")

    def test_2331_exec_dict_form(self):
        module, service = _mods(self)
        home = _deep_chain_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec(\n"
            "            'x = HELD',\n"
            "            OUTER.L1.L2.L3.LEAF.__dict__, loc,\n"
            "        )\n"
            "        return loc['x']\n"
        )
        _check3(self, module, service, home, "r36 2331 ex")

    def test_2331_plain_records(self):
        module, service = _mods(self)
        home = _deep_chain_home(
            "class K:\n    def method(self):\n"
            "        return getattr(\n"
            "            OUTER.L1.L2.L3.LEAF, Cls.NAME\n"
            "        )\n",
            cls_name="PLAIN",
        )
        _records3(self, module, home, "r36 2331 plain")

    def test_2331_fourth_hop_pole(self):
        module, service = _mods(self)
        leaf = _make_module(
            "import threading\n"
            "PLAIN = 7\nHELD = threading.Lock()\n",
            "r36_region56_leaf4",
        )
        l2 = _make_module("", "r36_region56_l2b")
        l2.__dict__["LEAF"] = leaf
        l1 = _make_module("", "r36_region56_l1b")
        l1.__dict__["L2"] = l2
        outer = _make_module("", "r36_region56_outerb")
        outer.__dict__["L1"] = l1
        home = _make_module(
            "class K:\n    def method(self):\n"
            "        return getattr(\n"
            "            OUTER.L1.L2.LEAF, Cls.NAME\n"
            "        )\n"
        )
        home.__dict__["OUTER"] = outer
        home.__dict__["Cls"] = type("Cls", (), {"NAME": "HELD"})
        _check3(self, module, service, home, "r36 2331 pole")


def _iso2_home(source, with_obj=False):
    inner = _make_module(
        "import threading\nPLAIN = 7\nHELD = threading.Lock()\n",
        "r36_region56_inner2",
    )
    outer = _make_module("", "r36_region56_outer2")
    outer.__dict__["INNER"] = inner
    home = _make_module(source)
    home.__dict__["OUTER"] = outer
    if with_obj:
        obj_cls = _make_module(
            "class Obj:\n"
            "    def __init__(self):\n"
            "        self.KEY = 'INNER'\n",
            "r36_region56_objmod",
        )
        home.__dict__["OBJ"] = obj_cls.Obj()
    return home


_ISO2_K = (
    "class K:\n"
    "    def __init__(self):\n"
    "        self.KEY = 'INNER'\n"
    "    def method(self):\n"
    "        return %s\n"
)


class TestConsumeFixR36Iso2SubscriptInstanceKey(
    unittest.TestCase
):
    """Ruling 2332: subscript presentation under an instance key."""

    def test_2332_vars_subscript_self_key(self):
        module, service = _mods(self)
        home = _iso2_home(
            _ISO2_K % "getattr(vars(OUTER)[self.KEY], 'HELD')"
        )
        _check3(self, module, service, home, "r36 2332 vs")

    def test_2332_dict_subscript_self_key(self):
        module, service = _mods(self)
        home = _iso2_home(
            _ISO2_K % "getattr(OUTER.__dict__[self.KEY], 'HELD')"
        )
        _check3(self, module, service, home, "r36 2332 ds")

    def test_2332_vars_subscript_home_instance_key(self):
        module, service = _mods(self)
        home = _iso2_home(
            "class K:\n    def method(self):\n"
            "        return getattr(\n"
            "            vars(OUTER)[OBJ.KEY], 'HELD'\n"
            "        )\n",
            with_obj=True,
        )
        _check3(self, module, service, home, "r36 2332 obj")

    def test_2332_plain_records(self):
        module, service = _mods(self)
        home = _iso2_home(
            _ISO2_K % "getattr(vars(OUTER)[self.KEY], 'PLAIN')"
        )
        _records3(self, module, home, "r36 2332 plain")

    def test_2332_class_key_pole(self):
        module, service = _mods(self)
        home = _iso2_home(
            "class Cls:\n    KEY = 'INNER'\n"
            "class K:\n    def method(self):\n"
            "        return getattr(\n"
            "            vars(OUTER)[Cls.KEY], 'HELD'\n"
            "        )\n"
        )
        _check3(self, module, service, home, "r36 2332 pole")


_ISO3_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def fourth():\n"
    "        return _n\n    return fourth\n"
    "fourth = _fac()\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)
_ISO3_STRING = (
    "STR = 'HELD'\n"
    "def fourth():\n    return STR\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)
_ISO3_CONTAINER = (
    "D = ['HELD']\n"
    "def fourth():\n    return D[0]\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)
_ISO3_DEFAULT = (
    "def fourth(_n='HELD'):\n    return _n\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)
_ISO3_THIRD_POLE = (
    "def _fac():\n    _n = 'HELD'\n    def third():\n"
    "        return _n\n    return third\n"
    "third = _fac()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)

_ISO3_HOME = (
    "class K:\n    def method(self):\n"
    "        return globals()[mid()]\n"
)
_ISO3_GA = (
    "class K:\n    def method(self):\n"
    "        return getattr(MOD, mid())\n"
)


def _iso3_home(case, source, body, label, plain=False):
    module, service = _mods(case)
    text = body
    if plain:
        text = text.replace("'HELD'", "'PLAIN'")
    home = _target_home(source, text + _HOME_TAIL)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR36Iso3FourthOrderClass(unittest.TestCase):
    """Ruling 2333: fourth order carried name of a class member."""

    def test_2333_home_closure(self):
        _iso3_home(self, _ISO3_HOME, _ISO3_CLOSURE, "r36 2333 hc")

    def test_2333_foreign_closure(self):
        _iso3_home(self, _ISO3_GA, _ISO3_CLOSURE, "r36 2333 fc")

    def test_2333_home_string(self):
        _iso3_home(self, _ISO3_HOME, _ISO3_STRING, "r36 2333 hs")

    def test_2333_foreign_string(self):
        _iso3_home(self, _ISO3_GA, _ISO3_STRING, "r36 2333 fs")

    def test_2333_home_container(self):
        _iso3_home(
            self, _ISO3_HOME, _ISO3_CONTAINER, "r36 2333 hb"
        )

    def test_2333_foreign_container(self):
        _iso3_home(self, _ISO3_GA, _ISO3_CONTAINER, "r36 2333 fb")

    def test_2333_home_default(self):
        _iso3_home(self, _ISO3_HOME, _ISO3_DEFAULT, "r36 2333 hd")

    def test_2333_foreign_default(self):
        _iso3_home(self, _ISO3_GA, _ISO3_DEFAULT, "r36 2333 fd")

    def test_2333_plain_records(self):
        _iso3_home(
            self, _ISO3_GA, _ISO3_CLOSURE, "r36 2333 plain",
            plain=True,
        )

    def test_2333_third_order_pole(self):
        _iso3_home(
            self, _ISO3_HOME, _ISO3_THIRD_POLE, "r36 2333 pole"
        )
