"""Slice CAPTURE, list section 2.10, plan section 6.5.

Failure and boundary perspective: these tests prize the refusal
outcomes the rows state: broken predecessor chains refused or
flagged partial, late and second Outcomes refused naming the closed
state, refusal at the D-13 caps with no truncation written, and
capture refused while the store stands suspect.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.capture, with function names taken from the behaviour
wording of each row. Fields a row does not state are not invented.
The capture price pinned in this slice paragraph, 20 operator
seconds per review for the short correction case, guessed, is
arithmetic only and closes no criterion; no row in this file treats
it as closing criterion 6, which stands stage carried at plan
section 6.3.
"""

import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.capture"


class TestCaptureT01(unittest.TestCase):
    """CAPTURE-T01: outcome change moves none of the three values."""

    def test_same_signature_for_a_different_outcome(self):
        module = require(MODULE)
        base = module.capture_example_a()
        varied = module.capture_example_a(varied_by="outcome only")
        self.assertEqual(base["signature"], varied["signature"])

    def test_same_group_key_for_a_different_outcome(self):
        module = require(MODULE)
        base = module.capture_example_a()
        varied = module.capture_example_a(varied_by="outcome only")
        self.assertEqual(base["group_key"], varied["group_key"])

    def test_same_pool_stamp_for_a_different_outcome(self):
        module = require(MODULE)
        base = module.capture_example_a()
        varied = module.capture_example_a(varied_by="outcome only")
        self.assertEqual(base["pool_stamp"], varied["pool_stamp"])


class TestCaptureT02(unittest.TestCase):
    """CAPTURE-T02: no computation reads outcome or correction."""

    def test_checked_by_construction(self):
        module = require(MODULE)
        for name in ("signature", "group_key", "pool_stamp"):
            inputs = module.computation_inputs(name)
            self.assertNotIn("review outcome", inputs)
            self.assertNotIn("correction", inputs)

    def test_checked_by_the_varied_fixture(self):
        module = require(MODULE)
        base = module.capture_example_a()
        varied = module.capture_example_a(
            varied_by="outcome and correction"
        )
        self.assertEqual(base["signature"], varied["signature"])
        self.assertEqual(base["group_key"], varied["group_key"])
        self.assertEqual(base["pool_stamp"], varied["pool_stamp"])


class TestCaptureT03(unittest.TestCase):
    """CAPTURE-T03: predecessor chains validate in order."""

    def test_chain_validates_in_order(self):
        module = require(MODULE)
        chain = module.example_a_chain()
        result = module.validate_chain(chain)
        self.assertTrue(result["valid"])
        self.assertEqual(result["order"], list(chain["order"]))

    def test_first_step_carries_predecessor_none(self):
        module = require(MODULE)
        chain = module.example_a_chain()
        self.assertIsNone(chain["steps"][0]["predecessor"])

    def test_broken_chain_is_refused_or_flagged_partial(self):
        module = require(MODULE)
        chain = module.example_a_chain(varied_by="chain break")
        result = module.validate_chain(chain)
        self.assertTrue(
            result["refused"] or result["flagged_partial"]
        )
        self.assertFalse(result["valid"])


class TestCaptureT04(unittest.TestCase):
    """CAPTURE-T04: the pending outcome state closes by two routes."""

    def test_pending_state_closes_by_its_two_routes_only(self):
        module = require(MODULE)
        routes = module.pending_outcome_close_routes()
        self.assertEqual(len(routes), 2)

    def test_a_late_outcome_is_refused_naming_the_closed_state(self):
        module = require(MODULE)
        outcome = module.submit_outcome("late")
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["reason"], "closed state")

    def test_a_second_outcome_is_refused_naming_the_closed_state(self):
        module = require(MODULE)
        outcome = module.submit_outcome("second")
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["reason"], "closed state")


class TestCaptureT05(unittest.TestCase):
    """CAPTURE-T05: refusal at the D-13 caps writes no truncation."""

    def test_payload_at_the_cap_is_accepted_whole(self):
        module = require(MODULE)
        outcome = module.capture_payload("at cap")
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["truncated"])

    def test_payload_over_the_cap_is_refused(self):
        module = require(MODULE)
        outcome = module.capture_payload("over cap")
        self.assertTrue(outcome["refused"])

    def test_refusal_at_the_caps_writes_no_truncation(self):
        module = require(MODULE)
        outcome = module.capture_payload("over cap")
        self.assertFalse(outcome["truncation_written"])
        self.assertFalse(outcome["partial_record_written"])

    def test_cap_values_are_labelled_guessed(self):
        module = require(MODULE)
        caps = module.d13_caps()
        for cap in caps:
            self.assertEqual(cap["source_class"], "guessed")


class TestCaptureT06(unittest.TestCase):
    """CAPTURE-T06: a run with no outcome counts in runs seen only."""

    def test_counted_in_runs_seen(self):
        module = require(MODULE)
        counts = module.membership_counts("none will follow")
        self.assertEqual(counts["runs_seen_delta"], 1)

    def test_counted_in_no_membership_figure(self):
        module = require(MODULE)
        counts = module.membership_counts("none will follow")
        for figure in counts["membership_figures"]:
            self.assertEqual(counts["membership_figures"][figure], 0)


class TestCaptureT07(unittest.TestCase):
    """CAPTURE-T07: capture refuses while the store stands suspect."""

    def test_capture_refused_while_store_suspect(self):
        module = require(MODULE)
        outcome = module.capture_into_store("suspect")
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["reason"], "store suspect")
        self.assertFalse(outcome["captured"])


class TestCaptureFixR1(unittest.TestCase):
    """Fix round 1: real payload measurement and widened forms.

    Written test first for the COR cure of S15-R1-059 and
    S15-R1-064: capture_payload measures the payload it is
    given against both D-13 caps, the pool stamp act reads
    the rotation position it is given, chain validation
    detects a cross run predecessor where the chain carries
    run identity, and the outcome, membership, and capture
    into store acts accept the material forms their rows
    state beyond their exact case strings.
    """

    def test_real_payload_at_the_text_field_cap_is_accepted_whole(self):
        module = require(MODULE)
        outcome = module.capture_payload("x" * 32768)
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["refused"])
        self.assertFalse(outcome["truncated"])

    def test_real_payload_over_the_text_field_cap_is_refused(self):
        module = require(MODULE)
        outcome = module.capture_payload("x" * 32769)
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["accepted"])
        self.assertFalse(outcome["truncation_written"])
        self.assertFalse(outcome["partial_record_written"])

    def test_real_payload_well_under_the_caps_is_accepted(self):
        module = require(MODULE)
        outcome = module.capture_payload(b"a small real payload")
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["refused"])

    def test_mapping_payload_at_the_journal_line_cap_is_accepted(self):
        module = require(MODULE)
        payload = {"first": "a" * 32768, "second": "b" * 32767}
        outcome = module.capture_payload(payload)
        self.assertTrue(outcome["accepted"])
        self.assertFalse(outcome["refused"])

    def test_mapping_payload_over_the_journal_line_cap_is_refused(self):
        module = require(MODULE)
        payload = {"first": "a" * 32768, "second": "b" * 32768}
        outcome = module.capture_payload(payload)
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["accepted"])

    def test_mapping_payload_with_a_field_over_the_field_cap_is_refused(self):
        module = require(MODULE)
        payload = {"only": "a" * 40000}
        outcome = module.capture_payload(payload)
        self.assertTrue(outcome["refused"])

    def test_pool_stamp_reads_the_rotation_position_given(self):
        module = require(MODULE)
        self.assertEqual(module.pool_stamp(3), "holdout eligible")
        self.assertEqual(module.pool_stamp(6), "holdout eligible")
        self.assertEqual(module.pool_stamp(1), "not holdout eligible")
        self.assertEqual(module.pool_stamp(2), "not holdout eligible")
        self.assertEqual(
            module.capture_example_a()["pool_stamp"], module.pool_stamp(1)
        )

    def test_chain_validation_detects_a_cross_run_predecessor(self):
        module = require(MODULE)
        chain = module.example_a_chain()
        chain["steps"][1]["predecessor_run"] = "another run"
        result = module.validate_chain(chain)
        self.assertFalse(result["valid"])
        self.assertTrue(result["refused"] or result["flagged_partial"])

    def test_submit_outcome_accepts_a_pending_run_form(self):
        module = require(MODULE)
        outcome = module.submit_outcome("pending")
        self.assertFalse(outcome["refused"])
        outcome = module.submit_outcome({"state": "attached"})
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["reason"], "closed state")

    def test_membership_counts_accepts_the_pending_state_form(self):
        module = require(MODULE)
        counts = module.membership_counts({"state": "pending"})
        self.assertEqual(counts["runs_seen_delta"], 1)
        for figure in counts["membership_figures"]:
            self.assertEqual(counts["membership_figures"][figure], 0)

    def test_capture_into_store_over_a_real_store_value(self):
        module = require(MODULE)
        store_module = require("ontoloop.store")
        clean = module.capture_into_store(store_module.golden_record_store())
        self.assertTrue(clean["captured"])
        self.assertFalse(clean["refused"])
        suspect = module.capture_into_store(store_module.suspect_store())
        self.assertTrue(suspect["refused"])
        self.assertEqual(suspect["reason"], "store suspect")
        self.assertFalse(suspect["captured"])


class TestCaptureFixR3(unittest.TestCase):
    """Fix round 3, ruling 9: validate_chain governed refusal.

    Written test first for S15-R3-009. Malformed chain
    inputs stand refused in one stated governed form,
    the ValueError form the sibling surfaces of this
    module use on an input in no stated form, beside
    the standing well formed cases, whose flagged
    partial form for a broken chain stands unchanged.
    """

    def test_validate_chain_integer_chain_raises_value_error(self):
        module = require(MODULE)
        with self.assertRaises(ValueError) as caught:
            module.validate_chain(123)
        self.assertEqual(str(caught.exception), "unknown chain form: 123")
        with self.assertRaises(ValueError) as caught:
            module.validate_chain([1, 2, 3])
        self.assertEqual(
            str(caught.exception), "unknown chain form: [1, 2, 3]")
        chain = module.example_a_chain()
        chain["steps"] = [1, 2]
        with self.assertRaises(ValueError) as caught:
            module.validate_chain(chain)
        self.assertEqual(
            str(caught.exception), "unknown chain step form: 1")

    def test_validate_chain_missing_kind_entry_raises_value_error(self):
        module = require(MODULE)
        chain = module.example_a_chain()
        chain["steps"] = [{}]
        chain["order"] = [chain["order"][0]]
        with self.assertRaises(ValueError) as caught:
            module.validate_chain(chain)
        self.assertEqual(
            str(caught.exception), "unknown chain step form: {}")
        chain = module.example_a_chain()
        del chain["steps"][0]["predecessor"]
        with self.assertRaises(ValueError) as caught:
            module.validate_chain(chain)
        self.assertEqual(
            str(caught.exception),
            "unknown chain step form: %r" % (chain["steps"][0],))
        with self.assertRaises(ValueError) as caught:
            module.validate_chain({})
        self.assertEqual(str(caught.exception), "unknown chain form: {}")

    def test_validate_chain_none_entry_raises_value_error(self):
        module = require(MODULE)
        chain = module.example_a_chain()
        chain["steps"] = [None, None]
        with self.assertRaises(ValueError) as caught:
            module.validate_chain(chain)
        self.assertEqual(
            str(caught.exception), "unknown chain step form: None")

    def test_validate_chain_none_chain_raises_value_error(self):
        module = require(MODULE)
        with self.assertRaises(ValueError) as caught:
            module.validate_chain(None)
        self.assertEqual(str(caught.exception), "unknown chain form: None")

    def test_validate_chain_string_forms_raise_value_error(self):
        module = require(MODULE)
        chain = module.example_a_chain()
        chain["steps"] = "a string steps value"
        with self.assertRaises(ValueError) as caught:
            module.validate_chain(chain)
        self.assertEqual(
            str(caught.exception), "unknown chain form: %r" % (chain,))
        chain = module.example_a_chain()
        chain["steps"] = ["a string step", "another string step"]
        with self.assertRaises(ValueError) as caught:
            module.validate_chain(chain)
        self.assertEqual(
            str(caught.exception),
            "unknown chain step form: 'a string step'")
        with self.assertRaises(ValueError) as caught:
            module.validate_chain("a string chain")
        self.assertEqual(
            str(caught.exception), "unknown chain form: 'a string chain'")

    def test_validate_chain_well_formed_cases_stand(self):
        module = require(MODULE)
        chain = module.example_a_chain()
        result = module.validate_chain(chain)
        self.assertTrue(result["valid"])
        self.assertFalse(result["flagged_partial"])
        broken = module.example_a_chain(varied_by="chain break")
        result = module.validate_chain(broken)
        self.assertFalse(result["valid"])
        self.assertTrue(result["flagged_partial"])
        empty = {"order": [], "steps": []}
        result = module.validate_chain(empty)
        self.assertFalse(result["valid"])
        self.assertTrue(result["flagged_partial"])


if __name__ == "__main__":
    unittest.main()
