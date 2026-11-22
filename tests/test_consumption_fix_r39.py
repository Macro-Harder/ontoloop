"""Fix round 39 tests for rulings 2746 to 2784, Region 4.

Written test first against the governing base form of
ontoloop/consumption.py at system head
8ba4e07ebe0b2d89586d8b5a58a0a23b98bb9509. Each ruling stands
pinned at both poles in the form its triage ruling states:
the defective forms stand decided in substance after the
cure, and the standing poles and clean controls its ruling
names stand in their standing forms at both poles.
Copyright (c) J.P. Picard aka Macro-Harder.
"""

import importlib.util
import os
import sys
import types
import unittest

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"

_spec = importlib.util.spec_from_file_location(
    "pin38_r39", os.path.join(os.path.dirname(__file__),
    "test_consume_fix_r38.py"))
pin = importlib.util.module_from_spec(_spec)
sys.modules["pin38_r39"] = pin
_spec.loader.exec_module(pin)

Holder = pin.Holder
_assert_refused = pin._assert_refused
_assert_refused_both = pin._assert_refused_both
_assert_records = pin._assert_records
_make_module = pin._make_module
_chain_home = pin._chain_home
_target_home = pin._target_home
_pair_home = pin._pair_home
_check3 = pin._check3
_records3 = pin._records3
_mods = pin._mods
_HOME_TAIL = pin._HOME_TAIL
_HOME_SRC = pin._HOME_SRC
_GA_SRC = pin._GA_SRC
_GS_SRC = pin._GS_SRC
_CHAIR_GA = pin._CHAIR_GA
_CHAIR_VS = pin._CHAIR_VS
_CHAIR_DS = pin._CHAIR_DS
_CHAIR_EX = pin._CHAIR_EX
_CHAIR_PL = pin._CHAIR_PL
_chair = pin._chair
_hop_home = pin._hop_home


def _sev(kind):
    if kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def seventh():\n        return _n\n"
                "    return seventh\nseventh = _fac()\n")
    elif kind == "string":
        leaf = "STR = 'HELD'\ndef seventh():\n    return STR\n"
    elif kind == "container":
        leaf = "D = {'k': 'HELD'}\ndef seventh():\n    return D['k']\n"
    else:
        leaf = "def seventh(_n='HELD'):\n    return _n\n"
    return (leaf + "def sixth():\n    return seventh()\n"
            "def fifth():\n    return sixth()\n"
            "def fourth():\n    return fifth()\n"
            "def third():\n    return fourth()\n"
            "def inner():\n    return third()\n"
            "def helper():\n    return inner()\n" + _HOME_TAIL)


_POLE6 = {"closure": pin._SIXTH_CLOSURE, "string": pin._SIXTH_STRING,
          "container": pin._SIXTH_CONTAINER,
          "default": pin._SIXTH_DEFAULT}


def _sev_case(case, source, kind, label, plain=False, pole=False):
    module, service = _mods(case)
    body = _POLE6[kind] if pole else _sev(kind)
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _target_home(source, body)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


def _pair4(kind):
    if kind == "string":
        leaf = "STR = 'HELD'\ndef inner4():\n    return STR\n"
    elif kind == "container":
        leaf = "D = {'k': 'HELD'}\ndef inner4():\n    return D['k']\n"
    elif kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def inner4():\n        return _n\n"
                "    return inner4\ninner4 = _fac()\n")
    else:
        leaf = "def inner4(_n='HELD'):\n    return _n\n"
    return (leaf + "def inner3():\n    return inner4()\n"
            "def inner2():\n    return inner3()\n"
            "def inner():\n    return inner2()\n"
            "def pairfn():\n    return inner()\n")


_POLE3 = {"string": pin._PAIR_INNER3_STRING,
          "container": pin._PAIR_INNER3_CONTAINER,
          "closure": pin._PAIR_INNER3_CLOSURE,
          "default": pin._PAIR_INNER3_DEFAULT}
_DEEP_INNER = {"string": pin._PAIR_INNER_STRING,
               "container": pin._PAIR_INNER_CONTAINER,
               "closure": pin._PAIR_INNER_CLOSURE,
               "default": pin._PAIR_INNER_DEFAULT}
_DEEP_SELF = {"string": pin._PAIR_SELF_STRING,
              "container": pin._PAIR_SELF_CONTAINER,
              "closure": pin._PAIR_SELF_CLOSURE,
              "default": pin._PAIR_SELF_DEFAULT}


def _helpers_src(n):
    if n == 1:
        return "def helper():\n    return CARRIER.pairfn()\n"
    if n == 2:
        return ("def helper2():\n    return CARRIER.pairfn()\n"
                "def helper():\n    return helper2()\n")
    if n == 3:
        return ("def helper3():\n    return CARRIER.pairfn()\n"
                "def helper2():\n    return helper3()\n"
                "def helper():\n    return helper2()\n")
    return ("def helper4():\n    return CARRIER.pairfn()\n"
            "def helper3():\n    return helper4()\n"
            "def helper2():\n    return helper3()\n"
            "def helper():\n    return helper2()\n")


def _pair_case39(case, source, carrier, label, plain=False, helpers=1):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _pair_home(source, body, _helpers_src(helpers) + _HOME_TAIL,
                      with_target=True)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


def _member_case(case, carrier, act, label, plain=False):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    src = pin._mp_source("CARRIER.pairfn()", act)
    home = _pair_home(src, body, "", with_target=True)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


_CHAIR_D = [
    ("d1_nested_conv_of_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(tuple(_k[0]))[0]]\n"),
    ("d2_conv_of_double_subscript", "def getmod(_k=[[['INNER']]]):\n    return vars(OUTER)[list(_k[0][0])[0]]\n"),
    ("d3_pop_of_nested_conversion", "def getmod(_k=['INNER']):\n    return vars(OUTER)[list(tuple(_k)).pop(0)]\n"),
    ("d4_join_of_conversion", "def getmod(_k=['IN', 'NER']):\n    return vars(OUTER)[''.join(list(_k))]\n"),
    ("d5_comprehension_over_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[[x for x in _k[0]][0]]\n"),
    ("d6_next_iter_conv_of_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[next(iter(list(_k[0])))]\n"),
    ("d7_pop_of_subscript_set", "def getmod(_k=[{'INNER'}]):\n    return vars(OUTER)[_k[0].pop()]\n"),
    ("d8_conversion_inside_sorted", "def getmod(_k=['INNER']):\n    return vars(OUTER)[sorted(list(_k))[0]]\n"),
    ("d9_conversion_of_sorted", "def getmod(_k=['INNER']):\n    return vars(OUTER)[list(sorted(_k))[0]]\n"),
    ("d10_starred_unpack_of_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[(*_k[0],)[0]]\n"),
    ("d11_join_of_subscript", "def getmod(_k=[['IN', 'NER']]):\n    return vars(OUTER)[''.join(_k[0])]\n"),
    ("d12_keys_of_copy_of_subscript", "def getmod(_k=[{'INNER': 1}]):\n    return vars(OUTER)[list(_k[0].copy().keys())[0]]\n"),
    ("d13_conv_of_subscript_of_helper", "def _h():\n    return [['INNER']]\ndef getmod():\n    return vars(OUTER)[list(_h()[0])[0]]\n"),
    ("d14_conv_of_cond_of_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(_k[0] if _k else 'X')[0]]\n"),
    ("d15_conv_of_reversed", "def getmod(_k=['INNER']):\n    return vars(OUTER)[list(reversed(_k))[0]]\n"),
    ("d16_direct_double_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[_k[0][0]]\n"),
    ("d17_tuple_conv_of_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[tuple(_k[0])[0]]\n"),
    ("d18_pop_of_set_conv_of_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[set(_k[0]).pop()]\n"),
    ("d19_comprehension_of_conversion", "def getmod(_k=['INNER']):\n    return vars(OUTER)[[x for x in list(_k)][0]]\n"),
    ("d20_join_of_comprehension", "def getmod(_k=['IN', 'NER']):\n    return vars(OUTER)[''.join([x for x in _k])]\n"),
]


def _mk_chair(name, body, member=_CHAIR_GA):
    def test(self):
        _chair(self, member, body, "r39 2746 " + name)
    test.__name__ = "test_2746_" + name
    return test


class TestConsumptionFixR39Chair1(unittest.TestCase):
    """Ruling 2746: produced name forms two operations beyond
    the produced name patterns of ruling 2594."""

    def test_2746_d1_vars_member(self):
        _chair(self, _CHAIR_VS, _CHAIR_D[0][1], "r39 2746 d1 vs")

    def test_2746_d1_dict_member(self):
        _chair(self, _CHAIR_DS, _CHAIR_D[0][1], "r39 2746 d1 ds")

    def test_2746_d1_exec_member(self):
        _chair(self, _CHAIR_EX, _CHAIR_D[0][1], "r39 2746 d1 ex")

    def test_2746_d11_vars_member(self):
        _chair(self, _CHAIR_VS, _CHAIR_D[10][1], "r39 2746 d11 vs")

    def test_2746_plain_via_d1(self):
        _chair(self, _CHAIR_PL, _CHAIR_D[0][1], "r39 2746 plain d1",
               plain=True)

    def test_2746_plain_via_d16(self):
        _chair(self, _CHAIR_PL, _CHAIR_D[15][1], "r39 2746 plain d16",
               plain=True)

    def test_2746_r2594_c1_pole(self):
        _chair(self, _CHAIR_GA,
               "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(_k[0])[0]]\n",
               "r39 2746 pole 2594")

    def test_2746_r2444_pole(self):
        _chair(self, _CHAIR_GA,
               "def getmod(_k={'INNER'}):\n    return vars(OUTER)[list(_k)[0]]\n",
               "r39 2746 pole 2444")

    def test_2746_direct_element_pole(self):
        _chair(self, _CHAIR_GA,
               "def getmod(_k=('INNER',)):\n    return vars(OUTER)[_k[0]]\n",
               "r39 2746 pole direct")


for _nm, _bd in _CHAIR_D:
    setattr(TestConsumptionFixR39Chair1, "test_2746_" + _nm,
            _mk_chair(_nm, _bd))


class TestConsumptionFixR39Consume1SeventhClosureHome(unittest.TestCase):
    """Ruling 2747: seventh order closure at the home map."""

    def test_2747_home_index(self):
        _sev_case(self, _HOME_SRC, "closure", "r39 2747 home")

    def test_2747_plain_records(self):
        _sev_case(self, _HOME_SRC, "closure", "r39 2747 plain", plain=True)

    def test_2747_sixth_pole(self):
        _sev_case(self, _HOME_SRC, "closure", "r39 2747 pole", pole=True)


class TestConsumptionFixR39Consume2SeventhClosureForeign(unittest.TestCase):
    """Ruling 2748: seventh order closure at a foreign module."""

    def test_2748_foreign_getattr(self):
        _sev_case(self, _GA_SRC, "closure", "r39 2748 ga")

    def test_2748_foreign_dict_subscript(self):
        _sev_case(self, _GS_SRC, "closure", "r39 2748 gs")

    def test_2748_plain_records(self):
        _sev_case(self, _GA_SRC, "closure", "r39 2748 plain", plain=True)


class TestConsumptionFixR39Consume3SeventhStringHome(unittest.TestCase):
    """Ruling 2749: seventh order string at the home map."""

    def test_2749_home_index(self):
        _sev_case(self, _HOME_SRC, "string", "r39 2749 home")

    def test_2749_plain_records(self):
        _sev_case(self, _HOME_SRC, "string", "r39 2749 plain", plain=True)

    def test_2749_sixth_pole(self):
        _sev_case(self, _HOME_SRC, "string", "r39 2749 pole", pole=True)


class TestConsumptionFixR39Consume4SeventhStringForeign(unittest.TestCase):
    """Ruling 2750: seventh order string at a foreign module."""

    def test_2750_foreign_getattr(self):
        _sev_case(self, _GA_SRC, "string", "r39 2750 ga")

    def test_2750_foreign_dict_subscript(self):
        _sev_case(self, _GS_SRC, "string", "r39 2750 gs")

    def test_2750_plain_records(self):
        _sev_case(self, _GA_SRC, "string", "r39 2750 plain", plain=True)


class TestConsumptionFixR39Consume5SeventhContainerHome(unittest.TestCase):
    """Ruling 2751: seventh order container at the home map."""

    def test_2751_home_index(self):
        _sev_case(self, _HOME_SRC, "container", "r39 2751 home")

    def test_2751_plain_records(self):
        _sev_case(self, _HOME_SRC, "container", "r39 2751 plain", plain=True)

    def test_2751_sixth_pole(self):
        _sev_case(self, _HOME_SRC, "container", "r39 2751 pole", pole=True)


class TestConsumptionFixR39Consume6SeventhContainerForeign(unittest.TestCase):
    """Ruling 2752: seventh order container at a foreign module."""

    def test_2752_foreign_getattr(self):
        _sev_case(self, _GA_SRC, "container", "r39 2752 ga")

    def test_2752_foreign_dict_subscript(self):
        _sev_case(self, _GS_SRC, "container", "r39 2752 gs")

    def test_2752_plain_records(self):
        _sev_case(self, _GA_SRC, "container", "r39 2752 plain", plain=True)


class TestConsumptionFixR39Consume7SeventhDefaultHome(unittest.TestCase):
    """Ruling 2753: seventh order default at the home map."""

    def test_2753_home_index(self):
        _sev_case(self, _HOME_SRC, "default", "r39 2753 home")

    def test_2753_plain_records(self):
        _sev_case(self, _HOME_SRC, "default", "r39 2753 plain", plain=True)

    def test_2753_sixth_pole(self):
        _sev_case(self, _HOME_SRC, "default", "r39 2753 pole", pole=True)


class TestConsumptionFixR39Consume8SeventhDefaultForeign(unittest.TestCase):
    """Ruling 2754: seventh order default at a foreign module."""

    def test_2754_foreign_getattr(self):
        _sev_case(self, _GA_SRC, "default", "r39 2754 ga")

    def test_2754_foreign_dict_subscript(self):
        _sev_case(self, _GS_SRC, "default", "r39 2754 gs")

    def test_2754_plain_records(self):
        _sev_case(self, _GA_SRC, "default", "r39 2754 plain", plain=True)


class TestConsumptionFixR39Consume9Pair4StringHome(unittest.TestCase):
    """Ruling 2755: pair inner inner inner inner string home."""

    def test_2755_home_index(self):
        _pair_case39(self, _HOME_SRC, _pair4("string"), "r39 2755 home", helpers=1)

    def test_2755_plain_records(self):
        _pair_case39(self, _HOME_SRC, _pair4("string"), "r39 2755 plain", plain=True, helpers=1)

    def test_2755_inner3_pole(self):
        _pair_case39(self, _HOME_SRC, _POLE3["string"], "r39 2755 pole", helpers=1)


class TestConsumptionFixR39Consume10Pair4StringForeign(unittest.TestCase):
    """Ruling 2756: pair inner inner inner inner string foreign."""

    def test_2756_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _pair4("string"), "r39 2756 ga", helpers=1)

    def test_2756_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _pair4("string"), "r39 2756 gs", helpers=1)

    def test_2756_plain_records(self):
        _pair_case39(self, _GA_SRC, _pair4("string"), "r39 2756 plain", plain=True, helpers=1)


class TestConsumptionFixR39Consume11Pair4ContainerHome(unittest.TestCase):
    """Ruling 2757: pair inner inner inner inner container home."""

    def test_2757_home_index(self):
        _pair_case39(self, _HOME_SRC, _pair4("container"), "r39 2757 home", helpers=1)

    def test_2757_plain_records(self):
        _pair_case39(self, _HOME_SRC, _pair4("container"), "r39 2757 plain", plain=True, helpers=1)

    def test_2757_inner3_pole(self):
        _pair_case39(self, _HOME_SRC, _POLE3["container"], "r39 2757 pole", helpers=1)


class TestConsumptionFixR39Consume12Pair4ContainerForeign(unittest.TestCase):
    """Ruling 2758: pair inner inner inner inner container foreign."""

    def test_2758_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _pair4("container"), "r39 2758 ga", helpers=1)

    def test_2758_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _pair4("container"), "r39 2758 gs", helpers=1)

    def test_2758_plain_records(self):
        _pair_case39(self, _GA_SRC, _pair4("container"), "r39 2758 plain", plain=True, helpers=1)


class TestConsumptionFixR39Consume13Pair4ClosureHome(unittest.TestCase):
    """Ruling 2759: pair inner inner inner inner closure home."""

    def test_2759_home_index(self):
        _pair_case39(self, _HOME_SRC, _pair4("closure"), "r39 2759 home", helpers=1)

    def test_2759_plain_records(self):
        _pair_case39(self, _HOME_SRC, _pair4("closure"), "r39 2759 plain", plain=True, helpers=1)

    def test_2759_inner3_pole(self):
        _pair_case39(self, _HOME_SRC, _POLE3["closure"], "r39 2759 pole", helpers=1)


class TestConsumptionFixR39Consume14Pair4ClosureForeign(unittest.TestCase):
    """Ruling 2760: pair inner inner inner inner closure foreign."""

    def test_2760_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _pair4("closure"), "r39 2760 ga", helpers=1)

    def test_2760_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _pair4("closure"), "r39 2760 gs", helpers=1)

    def test_2760_plain_records(self):
        _pair_case39(self, _GA_SRC, _pair4("closure"), "r39 2760 plain", plain=True, helpers=1)


class TestConsumptionFixR39Consume15Pair4DefaultHome(unittest.TestCase):
    """Ruling 2761: pair inner inner inner inner default home."""

    def test_2761_home_index(self):
        _pair_case39(self, _HOME_SRC, _pair4("default"), "r39 2761 home", helpers=1)

    def test_2761_plain_records(self):
        _pair_case39(self, _HOME_SRC, _pair4("default"), "r39 2761 plain", plain=True, helpers=1)

    def test_2761_inner3_pole(self):
        _pair_case39(self, _HOME_SRC, _POLE3["default"], "r39 2761 pole", helpers=1)


class TestConsumptionFixR39Consume16Pair4DefaultForeign(unittest.TestCase):
    """Ruling 2762: pair inner inner inner inner default foreign."""

    def test_2762_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _pair4("default"), "r39 2762 ga", helpers=1)

    def test_2762_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _pair4("default"), "r39 2762 gs", helpers=1)

    def test_2762_plain_records(self):
        _pair_case39(self, _GA_SRC, _pair4("default"), "r39 2762 plain", plain=True, helpers=1)


class TestConsumptionFixR39Consume17MemberPair4String(unittest.TestCase):
    """Ruling 2763: member level pair inner inner inner inner string."""

    def test_2763_getattr(self):
        _member_case(self, _pair4("string"), "ga", "r39 2763 ga")

    def test_2763_dict_subscript(self):
        _member_case(self, _pair4("string"), "gs", "r39 2763 gs")

    def test_2763_plain_records(self):
        _member_case(self, _pair4("string"), "ga", "r39 2763 plain", plain=True)

    def test_2763_inner3_pole(self):
        _member_case(self, _POLE3["string"], "ga", "r39 2763 pole")


class TestConsumptionFixR39Consume18MemberPair4Container(unittest.TestCase):
    """Ruling 2764: member level pair inner inner inner inner container."""

    def test_2764_getattr(self):
        _member_case(self, _pair4("container"), "ga", "r39 2764 ga")

    def test_2764_dict_subscript(self):
        _member_case(self, _pair4("container"), "gs", "r39 2764 gs")

    def test_2764_plain_records(self):
        _member_case(self, _pair4("container"), "ga", "r39 2764 plain", plain=True)

    def test_2764_inner3_pole(self):
        _member_case(self, _POLE3["container"], "ga", "r39 2764 pole")


class TestConsumptionFixR39Consume19MemberPair4Closure(unittest.TestCase):
    """Ruling 2765: member level pair inner inner inner inner closure."""

    def test_2765_getattr(self):
        _member_case(self, _pair4("closure"), "ga", "r39 2765 ga")

    def test_2765_dict_subscript(self):
        _member_case(self, _pair4("closure"), "gs", "r39 2765 gs")

    def test_2765_plain_records(self):
        _member_case(self, _pair4("closure"), "ga", "r39 2765 plain", plain=True)

    def test_2765_inner3_pole(self):
        _member_case(self, _POLE3["closure"], "ga", "r39 2765 pole")


class TestConsumptionFixR39Consume20MemberPair4Default(unittest.TestCase):
    """Ruling 2766: member level pair inner inner inner inner default."""

    def test_2766_getattr(self):
        _member_case(self, _pair4("default"), "ga", "r39 2766 ga")

    def test_2766_dict_subscript(self):
        _member_case(self, _pair4("default"), "gs", "r39 2766 gs")

    def test_2766_plain_records(self):
        _member_case(self, _pair4("default"), "ga", "r39 2766 plain", plain=True)

    def test_2766_inner3_pole(self):
        _member_case(self, _POLE3["default"], "ga", "r39 2766 pole")


class TestConsumptionFixR39Consume21Deep4InnerStringHome(unittest.TestCase):
    """Ruling 2767: deep pair one helper past, inner string home."""

    def test_2767_home_index(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["string"], "r39 2767 home", helpers=4)

    def test_2767_plain_records(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["string"], "r39 2767 plain", plain=True, helpers=4)

    def test_2767_triple_helper_pole(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["string"], "r39 2767 pole", helpers=3)


class TestConsumptionFixR39Consume22Deep4InnerStringForeign(unittest.TestCase):
    """Ruling 2768: deep pair one helper past, inner string foreign."""

    def test_2768_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _DEEP_INNER["string"], "r39 2768 ga", helpers=4)

    def test_2768_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _DEEP_INNER["string"], "r39 2768 gs", helpers=4)

    def test_2768_plain_records(self):
        _pair_case39(self, _GA_SRC, _DEEP_INNER["string"], "r39 2768 plain", plain=True, helpers=4)


class TestConsumptionFixR39Consume23Deep4InnerContainerHome(unittest.TestCase):
    """Ruling 2769: deep pair one helper past, inner container home."""

    def test_2769_home_index(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["container"], "r39 2769 home", helpers=4)

    def test_2769_plain_records(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["container"], "r39 2769 plain", plain=True, helpers=4)

    def test_2769_triple_helper_pole(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["container"], "r39 2769 pole", helpers=3)


class TestConsumptionFixR39Consume24Deep4InnerContainerForeign(unittest.TestCase):
    """Ruling 2770: deep pair one helper past, inner container foreign."""

    def test_2770_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _DEEP_INNER["container"], "r39 2770 ga", helpers=4)

    def test_2770_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _DEEP_INNER["container"], "r39 2770 gs", helpers=4)

    def test_2770_plain_records(self):
        _pair_case39(self, _GA_SRC, _DEEP_INNER["container"], "r39 2770 plain", plain=True, helpers=4)


class TestConsumptionFixR39Consume25Deep4InnerClosureHome(unittest.TestCase):
    """Ruling 2771: deep pair one helper past, inner closure home."""

    def test_2771_home_index(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["closure"], "r39 2771 home", helpers=4)

    def test_2771_plain_records(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["closure"], "r39 2771 plain", plain=True, helpers=4)

    def test_2771_triple_helper_pole(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["closure"], "r39 2771 pole", helpers=3)


class TestConsumptionFixR39Consume26Deep4InnerClosureForeign(unittest.TestCase):
    """Ruling 2772: deep pair one helper past, inner closure foreign."""

    def test_2772_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _DEEP_INNER["closure"], "r39 2772 ga", helpers=4)

    def test_2772_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _DEEP_INNER["closure"], "r39 2772 gs", helpers=4)

    def test_2772_plain_records(self):
        _pair_case39(self, _GA_SRC, _DEEP_INNER["closure"], "r39 2772 plain", plain=True, helpers=4)


class TestConsumptionFixR39Consume27Deep4InnerDefaultHome(unittest.TestCase):
    """Ruling 2773: deep pair one helper past, inner default home."""

    def test_2773_home_index(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["default"], "r39 2773 home", helpers=4)

    def test_2773_plain_records(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["default"], "r39 2773 plain", plain=True, helpers=4)

    def test_2773_triple_helper_pole(self):
        _pair_case39(self, _HOME_SRC, _DEEP_INNER["default"], "r39 2773 pole", helpers=3)


class TestConsumptionFixR39Consume28Deep4InnerDefaultForeign(unittest.TestCase):
    """Ruling 2774: deep pair one helper past, inner default foreign."""

    def test_2774_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _DEEP_INNER["default"], "r39 2774 ga", helpers=4)

    def test_2774_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _DEEP_INNER["default"], "r39 2774 gs", helpers=4)

    def test_2774_plain_records(self):
        _pair_case39(self, _GA_SRC, _DEEP_INNER["default"], "r39 2774 plain", plain=True, helpers=4)


class TestConsumptionFixR39Consume29Deep4SelfStringHome(unittest.TestCase):
    """Ruling 2775: deep pair one helper past, self string home."""

    def test_2775_home_index(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["string"], "r39 2775 home", helpers=4)

    def test_2775_plain_records(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["string"], "r39 2775 plain", plain=True, helpers=4)

    def test_2775_triple_helper_pole(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["string"], "r39 2775 pole", helpers=3)


class TestConsumptionFixR39Consume30Deep4SelfStringForeign(unittest.TestCase):
    """Ruling 2776: deep pair one helper past, self string foreign."""

    def test_2776_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _DEEP_SELF["string"], "r39 2776 ga", helpers=4)

    def test_2776_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _DEEP_SELF["string"], "r39 2776 gs", helpers=4)

    def test_2776_plain_records(self):
        _pair_case39(self, _GA_SRC, _DEEP_SELF["string"], "r39 2776 plain", plain=True, helpers=4)


class TestConsumptionFixR39Consume31Deep4SelfContainerHome(unittest.TestCase):
    """Ruling 2777: deep pair one helper past, self container home."""

    def test_2777_home_index(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["container"], "r39 2777 home", helpers=4)

    def test_2777_plain_records(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["container"], "r39 2777 plain", plain=True, helpers=4)

    def test_2777_triple_helper_pole(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["container"], "r39 2777 pole", helpers=3)


class TestConsumptionFixR39Consume32Deep4SelfContainerForeign(unittest.TestCase):
    """Ruling 2778: deep pair one helper past, self container foreign."""

    def test_2778_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _DEEP_SELF["container"], "r39 2778 ga", helpers=4)

    def test_2778_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _DEEP_SELF["container"], "r39 2778 gs", helpers=4)

    def test_2778_plain_records(self):
        _pair_case39(self, _GA_SRC, _DEEP_SELF["container"], "r39 2778 plain", plain=True, helpers=4)


class TestConsumptionFixR39Consume33Deep4SelfClosureHome(unittest.TestCase):
    """Ruling 2779: deep pair one helper past, self closure home."""

    def test_2779_home_index(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["closure"], "r39 2779 home", helpers=4)

    def test_2779_plain_records(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["closure"], "r39 2779 plain", plain=True, helpers=4)

    def test_2779_triple_helper_pole(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["closure"], "r39 2779 pole", helpers=3)


class TestConsumptionFixR39Consume34Deep4SelfClosureForeign(unittest.TestCase):
    """Ruling 2780: deep pair one helper past, self closure foreign."""

    def test_2780_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _DEEP_SELF["closure"], "r39 2780 ga", helpers=4)

    def test_2780_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _DEEP_SELF["closure"], "r39 2780 gs", helpers=4)

    def test_2780_plain_records(self):
        _pair_case39(self, _GA_SRC, _DEEP_SELF["closure"], "r39 2780 plain", plain=True, helpers=4)


class TestConsumptionFixR39Consume35Deep4SelfDefaultHome(unittest.TestCase):
    """Ruling 2781: deep pair one helper past, self default home."""

    def test_2781_home_index(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["default"], "r39 2781 home", helpers=4)

    def test_2781_plain_records(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["default"], "r39 2781 plain", plain=True, helpers=4)

    def test_2781_triple_helper_pole(self):
        _pair_case39(self, _HOME_SRC, _DEEP_SELF["default"], "r39 2781 pole", helpers=3)


class TestConsumptionFixR39Consume36Deep4SelfDefaultForeign(unittest.TestCase):
    """Ruling 2782: deep pair one helper past, self default foreign."""

    def test_2782_foreign_getattr(self):
        _pair_case39(self, _GA_SRC, _DEEP_SELF["default"], "r39 2782 ga", helpers=4)

    def test_2782_foreign_dict_subscript(self):
        _pair_case39(self, _GS_SRC, _DEEP_SELF["default"], "r39 2782 gs", helpers=4)

    def test_2782_plain_records(self):
        _pair_case39(self, _GA_SRC, _DEEP_SELF["default"], "r39 2782 plain", plain=True, helpers=4)


_EIGHT = ["L1", "L2", "L3", "L4", "L5", "L6"]
_SEVENH = ["L1", "L2", "L3", "L4", "L5"]
_CHAIN8 = "OUTER.L1.L2.L3.L4.L5.L6.LEAF"
_CHAIN7H = "OUTER.L1.L2.L3.L4.L5.LEAF"


class TestConsumptionFixR39Iso1EighthHop(unittest.TestCase):
    """Ruling 2783: governed value at the eighth hop of a chain."""

    def test_2783_getattr_gathered(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return getattr(%s, Cls.NAME)\n"
                         % _CHAIN8, _EIGHT)
        _check3(self, module, service, home, "r39 2783 ga")

    def test_2783_dict_subscript_literal(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return %s.__dict__['HELD']\n"
                         % _CHAIN8, _EIGHT)
        _check3(self, module, service, home, "r39 2783 ds")

    def test_2783_vars_subscript_gathered(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return vars(%s)[Cls.NAME]\n"
                         % _CHAIN8, _EIGHT)
        _check3(self, module, service, home, "r39 2783 vs")

    def test_2783_exec_dict_form(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        loc = {}\n"
                         "        exec('x = HELD', %s.__dict__, loc)\n"
                         "        return loc['x']\n" % _CHAIN8, _EIGHT)
        _check3(self, module, service, home, "r39 2783 ex")

    def test_2783_plain_records(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return getattr(%s, Cls.NAME)\n"
                         % _CHAIN8, _EIGHT, cls_name="PLAIN")
        _records3(self, module, home, "r39 2783 plain")

    def test_2783_seventh_hop_pole(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return getattr(%s, Cls.NAME)\n"
                         % _CHAIN7H, _SEVENH)
        _check3(self, module, service, home, "r39 2783 pole")


_ISO_HOME_G = ("class K:\n    def method(self):\n"
               "        return globals()[mid()]\n")
_ISO_GA_G = ("class K:\n    def method(self):\n"
             "        return getattr(MOD, mid())\n")


def _iso7(kind):
    if kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def seventh():\n        return _n\n"
                "    return seventh\nseventh = _fac()\n")
    elif kind == "string":
        leaf = "S = 'HELD'\ndef seventh():\n    return S\n"
    elif kind == "container":
        leaf = "L = ['HELD']\ndef seventh():\n    return L[0]\n"
    else:
        leaf = "def seventh(_n='HELD'):\n    return _n\n"
    return (leaf + "def sixth():\n    return seventh()\n"
            "def fifth():\n    return sixth()\n"
            "def fourth():\n    return fifth()\n"
            "def third():\n    return fourth()\n"
            "def second():\n    return third()\n"
            "def mid():\n    return second()\n" + _HOME_TAIL)


def _iso6(kind):
    if kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def sixth():\n        return _n\n"
                "    return sixth\nsixth = _fac()\n")
    elif kind == "string":
        leaf = "S = 'HELD'\ndef sixth():\n    return S\n"
    elif kind == "container":
        leaf = "L = ['HELD']\ndef sixth():\n    return L[0]\n"
    else:
        leaf = "def sixth(_n='HELD'):\n    return _n\n"
    return (leaf + "def fifth():\n    return sixth()\n"
            "def fourth():\n    return fifth()\n"
            "def third():\n    return fourth()\n"
            "def second():\n    return third()\n"
            "def mid():\n    return second()\n" + _HOME_TAIL)


def _iso_case(case, source, kind, label, plain=False, pole=False):
    module, service = _mods(case)
    body = _iso6(kind) if pole else _iso7(kind)
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _target_home(source, body)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumptionFixR39Iso2SeventhOrder(unittest.TestCase):
    """Ruling 2784: name carried at a seventh order step, severed
    from the Consume seventh order family, on the bundle copy act
    at the class, instance, and holder positions."""

    def test_2784_closure_home(self):
        _iso_case(self, _ISO_HOME_G, "closure", "r39 2784 closure home")

    def test_2784_closure_foreign(self):
        _iso_case(self, _ISO_GA_G, "closure", "r39 2784 closure ga")

    def test_2784_container_home(self):
        _iso_case(self, _ISO_HOME_G, "container", "r39 2784 container home")

    def test_2784_container_foreign(self):
        _iso_case(self, _ISO_GA_G, "container", "r39 2784 container ga")

    def test_2784_string_home(self):
        _iso_case(self, _ISO_HOME_G, "string", "r39 2784 string home")

    def test_2784_string_foreign(self):
        _iso_case(self, _ISO_GA_G, "string", "r39 2784 string ga")

    def test_2784_default_home(self):
        _iso_case(self, _ISO_HOME_G, "default", "r39 2784 default home")

    def test_2784_default_foreign(self):
        _iso_case(self, _ISO_GA_G, "default", "r39 2784 default ga")

    def test_2784_plain_records(self):
        _iso_case(self, _ISO_GA_G, "closure", "r39 2784 plain",
                  plain=True)

    def test_2784_sixth_pole(self):
        _iso_case(self, _ISO_HOME_G, "closure", "r39 2784 pole",
                  pole=True)


if __name__ == "__main__":
    unittest.main()
