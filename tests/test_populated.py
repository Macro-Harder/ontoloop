"""Slice POPULATED tests, list section 2.18.

Rows transcribed from design/steps/step-09-merged-test-list.md section 2.18.
The plan states for this slice: no fixture result closes any row in this
slice. Every row is a real target row, written in the stage carried form of
plan section 6.3: each test states the part a Step 13 test may pin, names
the owning stage and the record that will close it, and calls
harness.stage_carried with that reason, never skipped and never passed.
"""

import unittest

from tests import harness

REASON = (
    "stage carried: POPULATED rows are real target rows on the first "
    "populated store, no fixture result closes any row in this slice, "
    "and the closing records are the stage records named in each test"
)


class PopT01Tests(unittest.TestCase):
    """POP-T01: replacing events land on the records the brief names."""

    def test_replacing_events_land_on_their_named_records(self):
        harness.stage_carried(
            REASON + "; POP-T01 closes only when each replacing event, "
            "rerun, and timed act lands its replacement figure, or its "
            "recorded standing open form, on its named record, with the "
            "event register at plan section 7.4 as its evidence home."
        )


class PopT02Tests(unittest.TestCase):
    """POP-T02: corpus production counts, beside the specification commitment."""

    def test_corpus_production_counts_beside_the_commitment(self):
        harness.stage_carried(
            REASON + "; POP-T02 closes only on real material labelled by "
            "the operator in POPULATED corpus production, reporting counts "
            "actually produced per shape and per family in the production "
            "report form, beside the specification commitment and never "
            "merged into it."
        )


class PopT03Tests(unittest.TestCase):
    """POP-T03: the second implementation verification exercise."""

    def test_second_implementation_verifies_store_and_bundle(self):
        harness.stage_carried(
            REASON + "; POP-T03 closes only on the exercise record in the "
            "rehearsal register, verifying a store and a bundle produced "
            "by the first implementation against SPEC-CANON and SPEC-SEAL "
            "in the bounded form at plan section 4.7, with no cross "
            "implementation claim beyond that form."
        )


class PopT04Tests(unittest.TestCase):
    """POP-T04: the calibration record and the three pilot reruns."""

    def test_calibration_record_lands(self):
        harness.stage_carried(
            REASON + "; POP-T04 calibration limb closes only when the "
            "calibration record lands, or its unjudged form with reasons, "
            "on real traces."
        )

    def test_cluster_pilot_rerun_lands(self):
        harness.stage_carried(
            REASON + "; POP-T04 cluster limb closes only when the D-15 "
            "cluster pilot rerun lands its record, or its unjudged form "
            "with reasons, on real traces."
        )

    def test_redaction_pilot_rerun_lands(self):
        harness.stage_carried(
            REASON + "; POP-T04 redaction limb closes only when the "
            "redaction pilot rerun lands its record, or its unjudged "
            "form with reasons, on real traces."
        )

    def test_cost_pilot_lands(self):
        harness.stage_carried(
            REASON + "; POP-T04 cost limb closes only when the cost pilot "
            "over the first 10 completed evaluations on real traces lands "
            "its record, or its unjudged form with reasons."
        )


class PopT05Tests(unittest.TestCase):
    """POP-T05: the volume only fallback at 200 captured runs."""

    def test_unfired_event_recorded_at_the_next_loop_report(self):
        harness.stage_carried(
            REASON + "; POP-T05 closes only on real target evidence: at "
            "200 captured runs with no build attempted, the event is "
            "recorded as unfired at the next loop report of a real store."
        )


if __name__ == "__main__":
    unittest.main()
