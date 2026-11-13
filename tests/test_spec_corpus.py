"""Slice SPEC-CORPUS, list section 2.5, plan section 6.5.

Data structures perspective: these tests pin the exact three
hard negative shapes, the decoding round field on every decoded
candidate, the per shape rate report with no aggregate key, and
the pair count commitment form: a minimum of 30 labelled pairs
of each kind, stated as a completeness condition only.

Rows dependent on this specification are mapped in form only
until it closes, as the slice paragraph states; no completeness
beyond form is claimed here for redaction or cluster rows.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.corpus_spec.
"""

import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.corpus_spec"

HARD_NEGATIVE_SHAPES = (
    "hash heavy",
    "identifier heavy",
    "configuration heavy",
)


class TestSpecCorpusT01(unittest.TestCase):
    """SPEC-CORPUS-T01: hard negatives in the specification."""

    def test_hard_negative_shape_set_shape(self):
        # Suite fixture shape only; no product surface is touched.
        self.assertEqual(
            HARD_NEGATIVE_SHAPES,
            ("hash heavy", "identifier heavy", "configuration heavy"),
        )

    def test_decoding_round_field_on_every_decoded_candidate(self):
        module = require(MODULE)
        spec = module.corpus_specification()
        self.assertEqual(
            set(spec["hard_negatives"].keys()), set(HARD_NEGATIVE_SHAPES)
        )
        for shape in HARD_NEGATIVE_SHAPES:
            entry = spec["hard_negatives"][shape]
            self.assertEqual(entry["label"], "secret bearing shape")
            self.assertTrue(entry["negative_cases"])
            self.assertTrue(entry["decoded_candidates"])
            for candidate in entry["decoded_candidates"]:
                self.assertIn("decoding_round", candidate)
                self.assertIsInstance(candidate["decoding_round"], int)

    def test_per_shape_rate_reporting_with_no_single_aggregate(self):
        module = require(MODULE)
        report = module.rate_report()
        self.assertEqual(set(report.keys()), set(HARD_NEGATIVE_SHAPES))
        self.assertNotIn("aggregate", report)
        self.assertNotIn("total", report)
        for shape in HARD_NEGATIVE_SHAPES:
            self.assertEqual(set(report[shape].keys()), {"rate"})


class TestSpecCorpusT02(unittest.TestCase):
    """SPEC-CORPUS-T02: pair part in commitment form only."""

    def test_pair_counts_state_a_minimum_of_30_pairs_of_each_kind(self):
        module = require(MODULE)
        pair_part = module.pair_part()
        self.assertTrue(pair_part["kinds"])
        for kind in pair_part["kinds"]:
            commitment = pair_part["commitments"][kind]
            self.assertEqual(commitment["form"], "minimum")
            self.assertEqual(commitment["count"], 30)
            labelled = pair_part["labelled_pairs"][kind]
            self.assertGreaterEqual(len(labelled), commitment["count"])
            for pair in labelled:
                self.assertTrue(pair["label"])

    def test_no_production_count_cited_as_specification_evidence(self):
        module = require(MODULE)
        pair_part = module.pair_part()
        self.assertEqual(pair_part["evidence"], "specification commitment")
        self.assertNotIn("production_count", pair_part)


class TestSpecCorpusT03(unittest.TestCase):
    """SPEC-CORPUS-T03: labeller, act, and protocol, stage record."""

    def test_labeller_is_the_operator(self):
        stage_carried(
            "SPEC-CORPUS-T03 evidence home is stage record evidence: "
            "the labeller being the operator is a stage record fact "
            "about the labelling act, not a fixture result."
        )

    def test_labelling_act_and_protocol_are_named(self):
        stage_carried(
            "SPEC-CORPUS-T03 evidence home is stage record evidence: "
            "the naming of the labelling act and protocol in the "
            "specification is checked on the stage record for this "
            "specification slice."
        )


if __name__ == "__main__":
    unittest.main()
