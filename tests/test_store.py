"""Slice STORE, list section 2.7, plan section 6.5 plus supplied rows.

Failure and boundary perspective: these tests prize the refusal,
disagreement, and interruption outcomes the rows state: verify in its
three output vocabulary only, named errors for sync, write, founding,
and lock failures, suspect store refusals, and the detection acts at
reopening for the false flush and consumed writeback cases.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.store, with function names taken from the behaviour wording
of each row. Fields a row does not state are not invented. Where a
row names a harness entry, the test drives that entry by its stated
name through the store module fault entry point.
"""

import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.store"

VERIFY_SENTENCE = (
    "Verify proved the journal chain and the manifest agree over "
    "every record checked, and that the journal head and the "
    "manifest head stand signed under the signing key, so no "
    "checked record was altered after it was written except "
    "under that key, at signed strength only."
)

VERIFY_HOLES = (
    "a rewrite signed with the genuine key is not detected",
    "the anchor covers the heads as they stood at the most "
    "recent completed backup archive",
    "whole home deletion is detected only where an anchor for "
    "the store stands in an archive that survives",
)

LOCK_CONTENTION_REFUSAL = "lock contention refusal"
STORE_SUSPECT = "store suspect"


class TestStoreT01(unittest.TestCase):
    """STORE-T01: verify agreement and the verbatim verify sentence."""

    def test_verify_on_fully_checked_store_returns_agreement(self):
        module = require(MODULE)
        result = module.verify(module.golden_record_store())
        self.assertEqual(result["output"], "agreement")

    def test_verify_sentence_stands_in_its_verbatim_form(self):
        module = require(MODULE)
        result = module.verify(module.golden_record_store())
        self.assertEqual(result["sentence"], VERIFY_SENTENCE)


class TestStoreT02(unittest.TestCase):
    """STORE-T02: unverifiable cases and the prefix reading."""

    def test_manifest_lag_returns_unverifiable_naming_that_case(self):
        module = require(MODULE)
        store = module.interrupted_store("manifest lag")
        result = module.verify(store)
        self.assertEqual(result["output"], "unverifiable")
        self.assertEqual(result["case"], "manifest lag")

    def test_non_final_tear_returns_chain_consistent_prefix(self):
        module = require(MODULE)
        store = module.interrupted_store("non final tear")
        result = module.verify(store)
        self.assertEqual(result["reading"], "chain consistent prefix")

    def test_prefix_wording_never_uses_the_verify_sentence(self):
        module = require(MODULE)
        store = module.interrupted_store("non final tear")
        result = module.verify(store)
        self.assertNotIn(VERIFY_SENTENCE, result["wording"])
        self.assertNotEqual(result["wording"], VERIFY_SENTENCE)

    def test_prefix_reading_supports_reads_only(self):
        module = require(MODULE)
        store = module.interrupted_store("non final tear")
        result = module.verify(store)
        self.assertEqual(result["supports"], "reads only")
        self.assertFalse(result["supports_judging_use"])


class TestStoreT03(unittest.TestCase):
    """STORE-T03: torn final line repair order, harness driven."""

    def test_repair_verifies_the_prefix_before_any_truncation(self):
        module = require(MODULE)
        store = module.interrupted_store("torn final line")
        record = module.repair_torn_final_line(store)
        steps = record["steps"]
        self.assertLess(
            steps.index("verify prefix"), steps.index("truncate")
        )

    def test_no_append_follows_repair_until_truncation_verified(self):
        module = require(MODULE)
        store = module.interrupted_store("torn final line")
        module.repair_torn_final_line(store)
        outcome = module.append_before_truncation_verified(store)
        self.assertFalse(outcome["appended"])
        self.assertTrue(outcome["refused"])


class TestStoreT04(unittest.TestCase):
    """STORE-T04: identity minted in the append lock, D-19 refusal."""

    def test_identity_is_minted_inside_the_same_lock_that_appends(self):
        module = require(MODULE)
        result = module.append_with_identity(module.golden_record_store())
        self.assertEqual(
            result["identity"]["minted_under"],
            result["append"]["lock_identity"],
        )

    def test_lock_contention_waits_to_the_bound_then_refuses_by_name(self):
        module = require(MODULE)
        outcome = module.append_under_contention(
            module.lock_contention_case()
        )
        self.assertEqual(outcome["error"], LOCK_CONTENTION_REFUSAL)
        self.assertTrue(outcome["waited_to_bound"])
        self.assertFalse(outcome["appended"])


class TestStoreFixR1(unittest.TestCase):
    """Fix round 1 STORE cures, written test first.

    Covers S15-R1-007 (torn final line verify output),
    S15-R1-010 (the contention evidence surface performing
    the real wait), S15-R1-011 (the sealing level string
    key refusal), S15-R1-105 (the limits wording detected,
    not prevented, statement), and S15-R1-106 (the anchored
    verify anchor agreement and anchor mismatch statements).
    """

    def test_verify_over_a_torn_final_line_returns_a_governed_output(self):
        module = require(MODULE)
        store = module.interrupted_store("torn final line")
        result = module.verify(store)
        self.assertEqual(result["output"], "unverifiable")
        self.assertEqual(result["case"], "torn final line")
        self.assertNotIn("sentence", result)

    def test_append_under_contention_performs_the_wait_it_reports(self):
        import time

        module = require(MODULE)
        started = time.monotonic()
        outcome = module.append_under_contention(
            module.lock_contention_case()
        )
        elapsed = time.monotonic() - started
        self.assertEqual(outcome["error"], LOCK_CONTENTION_REFUSAL)
        self.assertTrue(outcome["waited_to_bound"])
        self.assertFalse(outcome["appended"])
        self.assertGreaterEqual(elapsed, 9.0)

    def test_append_under_contention_without_a_case_claims_no_wait(self):
        module = require(MODULE)
        outcome = module.append_under_contention({"unrelated": True})
        self.assertFalse(outcome["waited_to_bound"])
        self.assertFalse(outcome["appended"])

    def test_limits_wording_states_detected_not_prevented(self):
        module = require(MODULE)
        record = module.store_security_record(
            module.golden_record_store()
        )
        wording = record["simple"]["limits_wording"]
        self.assertIn("detected, not prevented", wording)
        self.assertEqual(module.check_store_security_record(record), [])

    def test_anchored_verify_states_anchor_agreement(self):
        module = require(MODULE)
        store = module.golden_record_store()
        anchor = dict(store["anchor_staging_copy"])
        result = module.verify(store, anchor=anchor)
        self.assertEqual(result["output"], "agreement")
        self.assertEqual(result["anchor_statement"], "anchor agreement")

    def test_anchored_verify_states_anchor_mismatch(self):
        module = require(MODULE)
        store = module.golden_record_store()
        anchor = dict(store["anchor_staging_copy"])
        module.append_record(
            store,
            {"record_type": "golden record", "payload": "golden record 2"},
            "golden record",
        )
        result = module.verify(store, anchor=anchor)
        self.assertEqual(result["output"], "disagreement")
        self.assertEqual(result["anchor_statement"], "anchor mismatch")
        self.assertNotIn("which head is true", str(result))

    def test_sealing_treats_a_string_key_as_no_key_obtained(self):
        sealing = require("ontoloop.sealing")
        self.assertIsNone(sealing.get_signing_key({"key_slot": "a key"}))
        with self.assertRaises(Exception) as caught:
            sealing.sign(b"data", "a key")
        self.assertEqual(
            type(caught.exception).__name__, "SigningKeyUnavailable"
        )

    def test_sealing_verify_refuses_a_string_key_store(self):
        module = require(MODULE)
        sealing = require("ontoloop.sealing")
        store = module.golden_record_store()
        store["key_slot"] = "a string key"
        result = sealing.verify(store)
        self.assertEqual(result["output"], "unverifiable")
        self.assertEqual(result["case"], "signing key unavailable")


class TestStoreFixR3(unittest.TestCase):
    """Fix round 3 STORE and sealing cures, written test first.

    Covers S15-R3-001 (a record whose content field differs
    from the content its canonical bytes encode stands
    detected by verify, with a content_mismatch item among
    the failed checks), S15-R3-002 (the first lock taking in
    append_under_contention stands bounded by the D-19 wait
    of up to 10 seconds), and S15-R3-015 (the chain
    consistent prefix reading stands returned only where an
    intact prefix of at least one record stands; a store
    with no intact record returns the unverifiable form
    naming the case no intact record).
    """

    def test_verify_detects_a_content_field_swapped_from_its_canonical_bytes(self):
        module = require(MODULE)
        sealing = require("ontoloop.sealing")
        store = module.golden_record_store()
        record = store["records"][-1]
        record["content"] = {
            "record_type": "golden record",
            "payload": "a different valid record body",
        }
        result = module.verify(store)
        self.assertNotEqual(result.get("output"), "agreement")
        self.assertIn("content_mismatch", result.get("failed_checks", []))
        direct = sealing.verify(store)
        self.assertIn("content_mismatch", direct.get("failed_checks", []))

    def test_verify_still_agrees_where_the_body_stands_as_recorded(self):
        module = require(MODULE)
        result = module.verify(module.golden_record_store())
        self.assertEqual(result["output"], "agreement")

    def test_append_under_contention_first_taking_stands_bounded(self):
        import threading
        import time

        module = require(MODULE)
        case = module.lock_contention_case()
        lock = module._APPEND_LOCK
        lock.acquire()
        outcome = {}

        def run():
            outcome["result"] = module.append_under_contention(case)

        thread = threading.Thread(target=run)
        started = time.monotonic()
        thread.start()
        thread.join(14)
        alive_after_bound = thread.is_alive()
        if alive_after_bound:
            lock.release()
            thread.join(20)
        else:
            lock.release()
        elapsed = time.monotonic() - started
        self.assertFalse(alive_after_bound)
        self.assertLess(elapsed, 14)
        self.assertGreaterEqual(elapsed, 9.0)
        result = outcome["result"]
        self.assertEqual(result["error"], LOCK_CONTENTION_REFUSAL)
        self.assertTrue(result["waited_to_bound"])
        self.assertFalse(result["appended"])

    def test_verify_with_no_intact_record_returns_unverifiable(self):
        module = require(MODULE)
        for records in ([1, 2], [None, None], [{}, {}], "junk"):
            store = module.golden_record_store()
            store["records"] = records
            result = module.verify(store)
            self.assertEqual(result.get("output"), "unverifiable")
            self.assertEqual(result.get("case"), "no intact record")
            self.assertNotIn("reading", result)

    def test_verify_genuine_prefix_case_still_returns_the_prefix_reading(self):
        module = require(MODULE)
        store = module.interrupted_store("non final tear")
        result = module.verify(store)
        self.assertEqual(result["reading"], "chain consistent prefix")
        self.assertFalse(result["supports_judging_use"])


class TestStoreT05(unittest.TestCase):
    """STORE-T05: sync and write failures, platform refusal kept."""

    def test_sync_failure_returns_a_named_error(self):
        module = require(MODULE)
        outcome = module.append_with_fault(
            module.golden_record_store(), "sync failure"
        )
        self.assertTrue(outcome["error"])
        self.assertEqual(outcome["error_kind"], "named error")

    def test_sync_failure_record_not_reported_as_appended(self):
        module = require(MODULE)
        outcome = module.append_with_fault(
            module.golden_record_store(), "sync failure"
        )
        self.assertFalse(outcome["reported_appended"])

    def test_write_failure_returns_a_named_error_not_appended(self):
        module = require(MODULE)
        outcome = module.append_with_fault(
            module.golden_record_store(), "write failure"
        )
        self.assertTrue(outcome["error"])
        self.assertFalse(outcome["reported_appended"])

    def test_platform_refusal_is_reported_and_never_absorbed(self):
        module = require(MODULE)
        outcome = module.append_with_fault(
            module.golden_record_store(), "platform refusal"
        )
        self.assertTrue(outcome["platform_refusal_reported"])
        self.assertFalse(outcome["absorbed"])
        self.assertFalse(outcome["reported_appended"])


class TestStoreT06(unittest.TestCase):
    """STORE-T06: a suspect store refuses ordinary capture appends."""

    def test_suspect_store_refuses_ordinary_capture_append_in_terms(self):
        module = require(MODULE)
        outcome = module.capture_append(module.suspect_store())
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["reason"], STORE_SUSPECT)
        self.assertFalse(outcome["appended"])


class TestStoreT07(unittest.TestCase):
    """STORE-T07, Amendment 1: forms owed in the security record."""

    def test_record_carries_the_seal_sentence_in_full(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        self.assertEqual(record["simple"]["seal_sentence"],
                         module.seal_sentence())

    def test_verify_sentence_holes_completed_in_verbatim_forms(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        self.assertEqual(record["simple"]["verify_sentence"],
                         VERIFY_SENTENCE)
        self.assertEqual(record["simple"]["holes"],
                         list(VERIFY_HOLES))

    def test_limits_wording_stands_in_the_record_itself(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        self.assertTrue(record["simple"]["limits_wording"])

    def test_each_limits_figure_has_an_advanced_counterpart(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        self.assertEqual(module.check_store_security_record(record), [])
        for figure in record["simple"]["limits_figures"]:
            self.assertIn(figure, record["advanced"]["figures"])
            self.assertTrue(record["advanced"]["figures"][figure]["basis"])

    def test_paraphrase_of_either_sentence_is_a_named_defect(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        varied = dict(record)
        varied_simple = dict(record["simple"])
        varied_simple["seal_sentence"] = "a paraphrase of the seal sentence"
        varied["simple"] = varied_simple
        defects = module.check_store_security_record(varied)
        self.assertTrue(defects)
        self.assertTrue(all(d["artifact"] == "store security record"
                            for d in defects))

    def test_hole_unfilled_or_in_other_words_is_a_named_defect(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        varied = dict(record)
        varied_simple = dict(record["simple"])
        varied_simple["holes"] = ["filled in other words", ""]
        varied["simple"] = varied_simple
        self.assertTrue(module.check_store_security_record(varied))

    def test_missing_owed_form_is_a_named_defect(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        varied = dict(record)
        varied["advanced"] = {}
        self.assertTrue(module.check_store_security_record(varied))

    def test_agentic_claim_without_an_owing_row_is_a_defect(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        self.assertNotIn("agentic", record)
        varied = dict(record)
        varied["agentic"] = {"claim": "an unowed agentic claim"}
        self.assertTrue(module.check_store_security_record(varied))

    def test_owed_form_with_a_different_value_fails_the_row(self):
        module = require(MODULE)
        record = module.store_security_record(module.golden_record_store())
        varied = dict(record)
        advanced = dict(record["advanced"])
        figures = dict(advanced["figures"])
        first = sorted(figures)[0]
        entry = dict(figures[first])
        entry["value"] = "a different value"
        figures[first] = entry
        advanced["figures"] = figures
        varied["advanced"] = advanced
        self.assertTrue(module.check_store_security_record(varied))


class TestStoreT08(unittest.TestCase):
    """STORE-T08: disagreement output in its own reserved form."""

    def test_disagreement_returned_for_chain_manifest_disagreement(self):
        module = require(MODULE)
        store = module.fully_checked_store_with_disagreement()
        result = module.verify(store)
        self.assertEqual(result["output"], "disagreement")

    def test_disagreement_is_neither_agreement_nor_unverifiable(self):
        module = require(MODULE)
        store = module.fully_checked_store_with_disagreement()
        result = module.verify(store)
        self.assertNotEqual(result["output"], "agreement")
        self.assertNotEqual(result["output"], "unverifiable")
        self.assertEqual(result["form"], "disagreement form")


class TestStoreT09(unittest.TestCase):
    """STORE-T09: kill inside founding leaves no store at all."""

    def test_interruption_inside_founding_leaves_no_store(self):
        module = require(MODULE)
        outcome = module.found_with_fault("kill inside founding")
        self.assertEqual(outcome["home_reading"], "no store")

    def test_no_genesis_record_stands_after_interrupted_founding(self):
        module = require(MODULE)
        outcome = module.found_with_fault("kill inside founding")
        self.assertFalse(outcome["genesis_record"])

    def test_there_is_no_store_to_verify(self):
        module = require(MODULE)
        outcome = module.found_with_fault("kill inside founding")
        self.assertFalse(outcome["store_to_verify"])

    def test_named_error_is_store_founding_interrupted(self):
        module = require(MODULE)
        outcome = module.found_with_fault("kill inside founding")
        self.assertEqual(outcome["error"], "store founding interrupted")

    def test_repeated_submission_is_a_new_founding_not_a_retry(self):
        module = require(MODULE)
        outcome = module.found_with_fault("kill inside founding")
        resubmission = module.resubmit_founding(outcome)
        self.assertEqual(resubmission["form"], "new founding act")
        self.assertFalse(resubmission["is_retry"])
        self.assertFalse(resubmission["is_repair"])


class TestStoreT10(unittest.TestCase):
    """STORE-T10: power loss, recovery by the suspect machinery only."""

    def test_power_loss_entry_is_distinct_from_every_kill_entry(self):
        module = require(MODULE)
        entry = module.power_loss_entry()
        self.assertNotIn(entry, module.kill_entries())

    def test_state_after_stands_on_the_next_verify_alone(self):
        module = require(MODULE)
        store = module.interrupted_store("power loss")
        outcome = module.reopen_and_verify(store)
        self.assertIn(outcome["basis"], ("verify result", "suspect error"))
        self.assertEqual(outcome["first_act"], "verify")

    def test_no_operator_act_stands_before_the_reopening_verify(self):
        module = require(MODULE)
        store = module.interrupted_store("power loss")
        outcome = module.reopen_and_verify(store)
        self.assertEqual(outcome["acts_before_verify"], [])

    def test_recovery_is_by_that_machinery_and_no_other(self):
        module = require(MODULE)
        store = module.interrupted_store("power loss")
        outcome = module.reopen_and_verify(store)
        self.assertEqual(outcome["recovery"], "suspect and lag machinery")


class TestStoreT11(unittest.TestCase):
    """STORE-T11: false flush completion, detection at reopening."""

    def test_record_not_read_as_appended_for_judging_use(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_detection(store)
        self.assertFalse(outcome["record_read_as_appended_for_judging"])

    def test_detection_entry_stands_in_the_suspect_record(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_detection(store)
        self.assertTrue(outcome["detection_entry_in_suspect_record"])
        self.assertEqual(outcome["store_position"], "suspect")

    def test_detection_runs_at_reopening_before_judging_read(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_detection(store)
        acts = outcome["reopening_acts"]
        self.assertLess(acts.index("detection check"),
                        acts.index("first judging read"))

    def test_detection_runs_before_any_ordinary_append_is_accepted(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_detection(store)
        acts = outcome["reopening_acts"]
        self.assertLess(acts.index("detection check"),
                        acts.index("first ordinary append"))

    def test_detection_entry_names_a_medium_reading_form(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_detection(store)
        entry = outcome["detection_entry"]
        self.assertIn(entry["reading_form"], ("A", "B", "C"))
        self.assertEqual(entry["sequence"], outcome["sequence"])
        self.assertEqual(entry["result"], "suspect")

    def test_a_cached_reading_discharges_nothing_for_this_row(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_cached_reading_only(store)
        self.assertFalse(outcome["row_discharged"])
        self.assertEqual(outcome["row_state"], "unpassed")

    def test_no_medium_form_available_records_the_case_carried_open(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_without_medium_reading_form(store)
        self.assertEqual(outcome["row_three_case"], "carried open")
        self.assertFalse(outcome["discharge_recorded"])

    def test_form_a_reading_bypasses_the_caches_it_can_bypass(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_form_a_reading(store)
        entry = outcome["detection_entry"]
        self.assertEqual(entry["reading_form"], "A")
        self.assertEqual(entry["read_path"], "direct uncached")
        self.assertTrue(entry["bypasses_os_page_cache"])
        self.assertTrue(entry["bypasses_device_cache_where_exposed"])
        self.assertEqual(entry["result"], "suspect")

    def test_form_b_reading_follows_holder_close_and_cache_drop(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_form_b_reading(store)
        entry = outcome["detection_entry"]
        self.assertEqual(entry["reading_form"], "B")
        self.assertTrue(entry["every_holder_closed"])
        self.assertTrue(entry["cache_drop_performed"])
        self.assertTrue(entry["cache_drop_recorded"])
        self.assertEqual(entry["result"], "suspect")

    def test_form_c_reading_is_in_a_new_process_after_restart(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_form_c_reading(store)
        entry = outcome["detection_entry"]
        self.assertEqual(entry["reading_form"], "C")
        self.assertTrue(entry["new_process"])
        self.assertTrue(entry["after_product_restart"])
        self.assertFalse(entry["earlier_process_holder_surviving"])
        self.assertEqual(entry["result"], "suspect")

    def test_labelled_reading_meeting_no_form_discharges_nothing(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_labelled_reading_only(store, "A")
        self.assertFalse(outcome["row_discharged"])
        self.assertEqual(outcome["row_state"], "unpassed")
        self.assertFalse(outcome["discharge_recorded"])

    def test_detection_is_by_the_store_module_in_the_reopening_act(self):
        module = require(MODULE)
        store = module.interrupted_store("false flush completion")
        outcome = module.reopen_with_detection(store)
        self.assertEqual(
            outcome["detection_actor"], "STORE module in operation"
        )
        self.assertEqual(outcome["detection_as_part_of"], "reopening act")


class TestStoreT12(unittest.TestCase):
    """STORE-T12: sync success after a consumed writeback failure."""

    def test_sequence_record_carries_every_sync_outcome(self):
        module = require(MODULE)
        store = module.interrupted_store("writeback error consumed")
        outcome = module.reopen_with_detection(store)
        record = outcome["sequence_record"]
        self.assertIn("writeback error", record["sync_outcomes"])

    def test_a_sequence_carrying_an_error_stands_detected_at_once(self):
        module = require(MODULE)
        store = module.interrupted_store("writeback error consumed")
        outcome = module.reopen_with_detection(store)
        self.assertTrue(outcome["detected_at_recording"])
        self.assertFalse(outcome["sequence_completed"])
        self.assertEqual(outcome["store_position"], "suspect")

    def test_later_success_certifies_no_earlier_writes(self):
        module = require(MODULE)
        store = module.interrupted_store("writeback error consumed")
        outcome = module.sync_after_detection(store)
        self.assertFalse(outcome["certifies_earlier_writes"])
        self.assertEqual(outcome["store_position"], "suspect")

    def test_case_discharged_only_with_both_detection_parts_run(self):
        module = require(MODULE)
        store = module.clean_sequence_store()
        outcome = module.reopen_with_detection(store)
        self.assertTrue(outcome["discharged"])
        self.assertTrue(outcome["part_one_recorded"])
        self.assertTrue(outcome["part_two_run"])
        self.assertEqual(outcome["part_two_finding"], "intact")

    def test_part_one_records_outcomes_across_the_three_sequences(self):
        module = require(MODULE)
        kinds = ("append", "founding", "manifest replacement")
        for kind in kinds:
            record = module.sequence_record_for(kind)
            self.assertEqual(record["sequence_kind"], kind)
            self.assertTrue(record["part_one_recorded"])
            returned = module.sync_outcomes_returned_to_product(kind)
            self.assertTrue(returned)
            for sync_outcome in returned:
                self.assertIn(sync_outcome, record["sync_outcomes"])

    def test_part_two_reading_takes_a_medium_reading_form(self):
        module = require(MODULE)
        store = module.interrupted_store("writeback error consumed")
        outcome = module.reopen_with_detection(store)
        self.assertTrue(outcome["part_two_run"])
        self.assertIn(outcome["part_two_reading_form"], ("A", "B", "C"))

    def test_part_two_not_run_stands_recorded_as_carried_open(self):
        module = require(MODULE)
        store = module.interrupted_store("writeback error consumed")
        outcome = module.reopen_without_part_two(store)
        self.assertEqual(outcome["row_four_case"], "carried open")
        self.assertFalse(outcome["discharged"])

    def test_medium_reading_finds_the_sequence_state_at_reopening(self):
        module = require(MODULE)
        store = module.interrupted_store("writeback error consumed")
        outcome = module.reopen_with_detection(store)
        self.assertIn(outcome["part_two_finding"],
                      ("intact", "absent", "torn", "failing check"))


class TestStoreT13(unittest.TestCase):
    """STORE-T13: simultaneous identical submission, two limbs.

    Each test below names the limb it exercises in its docstring
    line, as the row requires of the test record.
    """

    def test_limb_a_answered_from_the_first_record(self):
        """Limb exercised: A."""
        module = require(MODULE)
        outcome = module.simultaneous_identical_submission("limb A")
        self.assertEqual(outcome["answered_from"], "first record")
        self.assertEqual(outcome["records_for_intent"], 1)

    def test_limb_a_spends_and_appends_nothing(self):
        """Limb exercised: A."""
        module = require(MODULE)
        outcome = module.simultaneous_identical_submission("limb A")
        self.assertEqual(outcome["spent_by_second"], 0)
        self.assertEqual(outcome["appended_by_second"], 0)

    def test_limb_b_takes_the_lock_contention_refusal(self):
        """Limb exercised: B."""
        module = require(MODULE)
        outcome = module.simultaneous_identical_submission("limb B")
        self.assertEqual(outcome["error"], LOCK_CONTENTION_REFUSAL)
        self.assertIsNone(outcome["answered_from"])

    def test_limb_b_spends_and_appends_nothing(self):
        """Limb exercised: B."""
        module = require(MODULE)
        outcome = module.simultaneous_identical_submission("limb B")
        self.assertEqual(outcome["spent_by_second"], 0)
        self.assertEqual(outcome["appended_by_second"], 0)
        self.assertEqual(outcome["records_for_intent"], 1)

    def test_limb_a_acquires_the_lock_within_the_writer_wait(self):
        """Limb exercised: A."""
        module = require(MODULE)
        outcome = module.simultaneous_identical_submission("limb A")
        self.assertTrue(outcome["acquired_after_first_append"])
        self.assertTrue(outcome["within_writer_wait"])
        self.assertFalse(outcome["writer_wait_expired"])

    def test_limb_b_wait_expires_while_first_append_in_progress(self):
        """Limb exercised: B."""
        module = require(MODULE)
        outcome = module.simultaneous_identical_submission("limb B")
        self.assertTrue(outcome["writer_wait_expired"])
        self.assertTrue(outcome["first_append_in_progress_at_expiry"])

    def test_two_records_for_one_intent_fails_the_row(self):
        """Limb exercised: failure counterpart."""
        module = require(MODULE)
        outcome = module.two_records_for_one_intent_case()
        self.assertEqual(outcome["records_for_intent"], 2)
        self.assertTrue(outcome["row_failed"])
        second = module.second_record_appended_inside_lock_window_case()
        self.assertTrue(second["appended_inside_lock_window"])
        self.assertTrue(second["row_failed"])


if __name__ == "__main__":
    unittest.main()
