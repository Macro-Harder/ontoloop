"""Fix round 10 pins for the PROMOTE scope, Region 3.

Written test first for triage rulings 314, 315, and 316 at
design/steps/step-15-r10-triage.md. Ruling 314 counts
R10-PRO-1. Ruling 315 counts R10-PRO-2. Ruling 316 counts
R10-PRO-3. Each ruling stands counted in its own act here
and nowhere else in this region.
"""

import unittest
from collections import ChainMap, OrderedDict, UserDict
from collections.abc import Mapping
from types import MappingProxyType

from tests import harness


class _CustomMapping(Mapping):
    """A Mapping subclass standing as no dict instance."""

    def __init__(self, values):
        self._values = dict(values)

    def __getitem__(self, key):
        return self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)


def _mapping_forms(values):
    return (
        UserDict(values),
        MappingProxyType(dict(values)),
        ChainMap(dict(values)),
        _CustomMapping(values),
    )


class SubmitConfirmationMappingFormTests(unittest.TestCase):
    """Ruling 314: submit_confirmation reads its record as a mapping."""

    def test_complete_record_in_each_mapping_form_accepted(self):
        mod = harness.require("ontoloop.promote")
        record = mod.complete_confirmation_record()
        self.assertEqual(
            mod.submit_confirmation(dict(record))["outcome"], "accepted")
        self.assertEqual(
            mod.submit_confirmation(OrderedDict(record))["outcome"],
            "accepted")
        for form in _mapping_forms(record):
            result = mod.submit_confirmation(form)
            self.assertEqual(result["outcome"], "accepted",
                             type(form).__name__)
            self.assertNotIn("reason", result)

    def test_incomplete_and_disallowed_mapping_forms_still_refused(self):
        mod = harness.require("ontoloop.promote")
        record = mod.complete_confirmation_record()
        label_field = "production_evidence_label_position"
        weight_field = "production_evidence_weight_position"
        for missing in (label_field, weight_field):
            incomplete = dict(record)
            del incomplete[missing]
            for form in _mapping_forms(incomplete):
                result = mod.submit_confirmation(form)
                self.assertEqual(result["outcome"], "refused",
                                 (missing, type(form).__name__))
                self.assertEqual(result["reason"],
                                 "confirmation record incomplete")
        disallowed = dict(record)
        disallowed[weight_field] = "outside the allowed values"
        for form in _mapping_forms(disallowed):
            result = mod.submit_confirmation(form)
            self.assertEqual(result["outcome"], "refused",
                             type(form).__name__)

    def test_non_mapping_records_still_refused_incomplete(self):
        mod = harness.require("ontoloop.promote")
        for record in (bytearray(b"record"), frozenset({"record"}),
                       ["record"], None, "record"):
            result = mod.submit_confirmation(record)
            self.assertEqual(result["outcome"], "refused", repr(record))
            self.assertEqual(result["reason"],
                             "confirmation record incomplete")


class WriteBundleMappingFormTests(unittest.TestCase):
    """Ruling 315: write_bundle reads its candidate as a mapping."""

    def test_over_bound_candidate_in_each_mapping_form_refused(self):
        mod = harness.require("ontoloop.promote")
        candidate = mod.candidate_over_bound()
        control = mod.write_bundle(dict(candidate))
        self.assertEqual(control["outcome"], "refused")
        self.assertEqual(control["check_point"], "bundle writing")
        self.assertEqual(control["bundle_size_after"], candidate["size"])
        self.assertFalse(control["trimmed"])
        for form in _mapping_forms(candidate):
            result = mod.write_bundle(form)
            self.assertEqual(result["outcome"], "refused",
                             type(form).__name__)
            self.assertEqual(result["check_point"], "bundle writing")
            self.assertEqual(result["bundle_size_after"], candidate["size"],
                             type(form).__name__)
            self.assertFalse(result["trimmed"])

    def test_standing_bundle_writing_forms_preserved(self):
        mod = harness.require("ontoloop.promote")
        result = mod.write_bundle(bundle_size="over D-10 bound")
        self.assertEqual(result["outcome"], "refused")
        self.assertEqual(result["check_point"], "bundle writing")
        self.assertEqual(result["bundle_size_after"], "over D-10 bound")
        self.assertFalse(result["trimmed"])
        candidate = mod.candidate_over_bound()
        governed = mod.write_bundle(candidate, bundle_size="other size")
        self.assertEqual(governed["outcome"], "refused")
        self.assertEqual(governed["bundle_size_after"], candidate["size"])
        within = {"size": "within bound"}
        for form in (dict(within),) + _mapping_forms(within):
            result = mod.write_bundle(form)
            self.assertEqual(result["outcome"], "written",
                             type(form).__name__)
            self.assertEqual(result["bundle_size_after"], "within bound")
            self.assertFalse(result["trimmed"])
        standing = mod.write_bundle(["not a mapping"])
        self.assertEqual(standing["outcome"], "written")
        self.assertIsNone(standing["bundle_size_after"])


class RaiseDemotionFlagMappingFormTests(unittest.TestCase):
    """Ruling 316: raise_demotion_flag reads its bundle as a mapping."""

    def test_present_identity_in_each_mapping_form_carried(self):
        mod = harness.require("ontoloop.promote")
        for identity in ("", 0, False):
            bundle = {"bundle_identity": identity}
            control = mod.raise_demotion_flag(dict(bundle))
            self.assertEqual(control["bundle_identity"], identity)
            self.assertEqual(
                type(control["bundle_identity"]), type(identity))
            for form in _mapping_forms(bundle):
                flag = mod.raise_demotion_flag(form)
                self.assertEqual(flag["bundle_identity"], identity,
                                 (repr(identity), type(form).__name__))
                self.assertEqual(
                    type(flag["bundle_identity"]), type(identity))

    def test_missing_key_and_non_mapping_forms_still_fixture(self):
        mod = harness.require("ontoloop.promote")
        for form in _mapping_forms({}):
            flag = mod.raise_demotion_flag(form)
            self.assertEqual(flag["bundle_identity"], "confirmed bundle 1",
                             type(form).__name__)
        for bundle in ({}, "not a mapping", ["not a mapping"]):
            flag = mod.raise_demotion_flag(bundle)
            self.assertEqual(flag["bundle_identity"], "confirmed bundle 1",
                             repr(bundle))


if __name__ == "__main__":
    unittest.main()
