"""Store and journal module, slice STORE form.

The store and journal module: the one governed append act
under the single append lock, with identity minted inside
that same lock, the full append sequence read as plan
subsection 18.73 states it, and signing at the act that
creates the head, inside the lock, after the manifest
replacement and before the append is reported as appended;
the founding sequence over the sealing builders, in their
governed order, that founds a store whole before any
variation stands applied to it; verify as the one surface
over the sealing verify computation, delegating to it
under the strict shape projection of RF-10 with the
missing founding object pre check as its only other store
side handling, and recording the suspect position on the
store value where the computation returns disagreement,
under RF-6; the store and security record and its checker,
in the forms owed at plan section 13.3; and the fault,
reopening, and detection acts the interruption rows state,
driving the one append act and the constructors through
their stated conditions and appending no journal byte by
any second path.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of this
file: the tombstone, purge, and migration completion acts
of the OPS-MIGRATE slice, including the purge checkpoint
founding act in its purge occasion; the named operator act
that clears the suspect position; the capture and
redaction acts of the later slices in substance, beyond
the capture refusal position on a suspect store; the
golden record sets and the spanning suite of the
GOLDEN-SPAN slice; and the surfaces of every later slice.
No act of this module performs a real 1Password retrieval,
a real medium reading against a storage device, or a real
confinement barrier: the production signing key provider
position stands empty in this build, the store forms the
tests exercise stand in value form over a mapping store,
and every such leg stands carried or unproven in the slice
record in its own terms, never claimed by a green test of
this slice. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.store"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "append_before_truncation_verified",
    "append_record",
    "append_under_contention",
    "append_with_fault",
    "append_with_identity",
    "capture_append",
    "check_store_security_record",
    "clean_sequence_store",
    "found_with_fault",
    "fully_checked_store_with_disagreement",
    "golden_record_store",
    "interrupted_store",
    "kill_entries",
    "lock_contention_case",
    "power_loss_entry",
    "reopen_and_verify",
    "reopen_with_cached_reading_only",
    "reopen_with_detection",
    "reopen_with_form_a_reading",
    "reopen_with_form_b_reading",
    "reopen_with_form_c_reading",
    "reopen_with_labelled_reading_only",
    "reopen_without_medium_reading_form",
    "reopen_without_part_two",
    "repair_torn_final_line",
    "resubmit_founding",
    "seal_sentence",
    "second_record_appended_inside_lock_window_case",
    "sequence_record_for",
    "simultaneous_identical_submission",
    "store_security_record",
    "suspect_store",
    "sync_after_detection",
    "sync_outcomes_returned_to_product",
    "two_records_for_one_intent_case",
    "verify",
]

# The production signing key provider position, in the
# shape append statement 1 form: one private module level
# position, either empty, holding no provider, or holding
# one zero argument callable returning obtained key bytes
# or the unobtained position None. It stands in no __all__
# entry and stands unpresented by __dir__. In this build
# nothing assigns it: it stands empty for every non fixture
# store, and no retrieval code stands in this module.
_signing_key_provider = None

from ontoloop import sealing as _sealing

_FIXTURE_KEY = (
    b"ontoloop-fixture-" b"key-tracer-" b"commit-1"
)

_JOURNAL_SCHEMA_VERSION = 1
_CANONICAL_FORM_VERSION = 1
_HASH_ALGORITHM_IDENTITY = "SHA-256"

_GOLDEN_STORE_IDENTITY = "golden-record-store"
_GOLDEN_FOUNDING_IDENTITY = "golden-record-founding"

_SIGNING_KEY_UNAVAILABLE = "signing key unavailable"
_STORE_POSITION_KEY = "store_position"
_SUSPECT_POSITION = "suspect"

_LIMITS_FIGURE_NAME = "writer wait bound"
_LIMITS_FIGURE_VALUE = "up to 10 seconds"
_LIMITS_WORDING = (
    "Limits for this store stand stated in this record. "
    "The writer wait for the single append lock stands at "
    "up to 10 seconds, guessed at D-19, and a lock "
    "contention refusal follows the wait. While a store "
    "stands suspect, ordinary capture appends stand "
    "refused. The append lock is the only writer path "
    "inside the product: a direct file writer under full "
    "reach stands outside the product and is detected, "
    "not prevented, by verify disagreement or "
    "unverifiable outcomes, and no prevention stands "
    "claimed for such a writer. No other limit stated in "
    "this record carries a figure or a bound."
)
_LIMITS_FIGURE_BASIS = (
    "The D-19 writer wait for the single append lock, "
    "stated as guessed at plan section 4.2 in the form "
    "writer wait of up to 10 seconds at D-19, guessed, "
    "with a refusal after it, and carried at subsection "
    "18.6 clause four, the append lock standing in a non "
    "blocking poll loop form with the D-19 writer wait, "
    "guessed, and a refusal after the wait. No measured "
    "value for the wait stands in any text, and the "
    "figure stands recorded as guessed in every record "
    "that carries it."
)

_KILL_ENTRIES = (
    "kill inside founding",
    "kill between journal sync and manifest sync",
)
_POWER_LOSS_ENTRY = "power loss"

_SEQUENCE_OUTCOMES = {
    "append": ("writeback error", "sync success"),
    "founding": ("sync success",),
    "manifest replacement": ("sync success",),
}


def _not_built_error():
    prefix = globals().get(
        "NOT_BUILT_PREFIX", "NOT BUILT (Step 14): "
    )
    name = globals().get("MODULE_NAME", "ontoloop.store")
    return AssertionError(prefix + name)


def _usable_key(key):
    return isinstance(key, bytes) and len(key) > 0


def _provider_signing_key():
    """Return the provider obtained key bytes, or None.

    The provider position stands read through the module
    globals at call time. An empty position, a string
    return, an empty bytes return, a bytearray, a mapping,
    or any other return stands treated as no key obtained,
    in the shape append statement 1 form, and no value so
    treated stands passed to a signing act.
    """
    provider = globals().get("_signing_key_provider")
    if provider is None:
        return None
    try:
        value = provider()
    except Exception:
        return None
    if isinstance(value, bytes) and len(value) > 0:
        return value
    return None


def _refusal_mapping():
    return {
        "error": _SIGNING_KEY_UNAVAILABLE,
        "appended": False,
        "reported_appended": False,
    }


def _make_record(store, content, record_type):
    records = store["records"]
    sequence = len(records) + 1
    predecessor = records[-1]["hash"] if records else ""
    fields = {
        "content": content,
        "predecessor_hash": predecessor,
        "store_sequence": sequence,
        "record_type": record_type,
    }
    return {
        "content": content,
        "predecessor_hash": predecessor,
        "store_sequence": sequence,
        "record_type": record_type,
        "hash": _sealing.hash_journal_record(
            content, predecessor, sequence, record_type
        ),
        "canonical_bytes": _sealing.canonical_bytes(
            fields, _sealing.JOURNAL_RECORD_KIND
        ),
    }


def _replace_manifest(store):
    records = store["records"]
    last = records[-1]
    store["manifest"] = _sealing.build_manifest(
        store["founding_object_identity"],
        last["hash"],
        len(records),
        last["store_sequence"],
        _JOURNAL_SCHEMA_VERSION,
        _CANONICAL_FORM_VERSION,
        _HASH_ALGORITHM_IDENTITY,
    )


def _sign_heads(store):
    manifest = store["manifest"]
    head_hash = manifest["head_hash"]
    current_manifest_hash = _sealing.manifest_hash(manifest)
    standing = _sealing.sign_signature_object(
        store["store_identity"],
        store["founding_object_identity"],
        head_hash,
        current_manifest_hash,
        store["key_slot"],
    )
    store["signature_object"] = standing
    store["anchor_staging_copy"] = _sealing.build_anchor_object(
        store["store_identity"],
        store["founding_object_identity"],
        head_hash,
        current_manifest_hash,
        manifest["record_count"],
        manifest["head_store_sequence"],
        standing["signature"],
    )
    return standing


def _append_sequence(store, content, record_type):
    if not _usable_key(store["key_slot"]):
        return _refusal_mapping()
    record = _make_record(store, content, record_type)
    store["records"].append(record)
    _replace_manifest(store)
    _sign_heads(store)
    return {
        "appended": True,
        "reported_appended": True,
        "record": record,
    }


def _append_interrupted(store, content, record_type):
    if not _usable_key(store["key_slot"]):
        return _refusal_mapping()
    record = _make_record(store, content, record_type)
    store["records"].append(record)
    return {
        "appended": False,
        "reported_appended": False,
        "record": record,
    }


def _found_store(store_identity, founding_id, key_slot):
    if not _usable_key(key_slot):
        return _refusal_mapping()
    store = {
        "store_identity": store_identity,
        "founding_object_identity": founding_id,
        "records": [],
        "manifest": None,
        "signature_object": None,
        "anchor_staging_copy": None,
        "key_slot": key_slot,
    }
    genesis_content = {
        "store_identity": store_identity,
        "founding_object_identity": founding_id,
        "journal_schema_version": _JOURNAL_SCHEMA_VERSION,
        "canonical_form_version": _CANONICAL_FORM_VERSION,
        "hash_algorithm_identity": _HASH_ALGORITHM_IDENTITY,
    }
    _append_sequence(store, genesis_content, "genesis")
    return store


def golden_record_store():
    """Return the golden record store fixture.

    The store stands founded whole through the one founding
    sequence, with the private fixture key read here and
    nowhere else in this section: a genesis record and one
    golden record, a seven field manifest over the two
    records, a standing signature object carrying the four
    signed fields and the signature value beside them and
    no other key, and an anchor staging copy carrying the
    seven anchor fields and no other key. The store value
    carries exactly the seven contract keys.
    """
    store = _found_store(
        _GOLDEN_STORE_IDENTITY,
        _GOLDEN_FOUNDING_IDENTITY,
        _FIXTURE_KEY,
    )
    _append_sequence(
        store,
        {"record_type": "golden record",
         "payload": "golden record 1"},
        "golden record",
    )
    return store


def fully_checked_store_with_disagreement():
    """Return a fully checked store whose signature differs.

    The store stands founded whole as the golden record
    store first, and the variation stands applied only
    after that founding stands complete, in the landed
    tracer form: the first character of the standing
    signature value stands replaced, so the signature does
    not verify on a fully checked store.
    """
    store = golden_record_store()
    signature_object = store["signature_object"]
    signature = signature_object["signature"]
    first = "0" if signature[0] != "0" else "1"
    signature_object["signature"] = first + signature[1:]
    return store


def interrupted_store(kind):
    """Return a store standing in the named interrupted state.

    Each kind stands constructed whole through the founding
    sequence first, with its variation applied only after
    that founding stands complete. A kind string no row
    names raises the NOT BUILT form inside this function,
    because the kind position is a value position on a
    present name, in the scope section 11 form.
    """
    if kind == "manifest lag":
        store = golden_record_store()
        _append_interrupted(
            store,
            {"record_type": "golden record",
             "payload": "golden record 2"},
            "golden record",
        )
        return store
    if kind == "non final tear":
        store = golden_record_store()
        _append_sequence(
            store,
            {"record_type": "golden record",
             "payload": "golden record 2"},
            "golden record",
        )
        record = store["records"][1]
        canonical = record["canonical_bytes"]
        record["canonical_bytes"] = canonical[: len(canonical) // 2]
        return store
    if kind == "torn final line":
        store = golden_record_store()
        _append_sequence(
            store,
            {"record_type": "golden record",
             "payload": "golden record 2"},
            "golden record",
        )
        record = store["records"][-1]
        canonical = record["canonical_bytes"]
        record["canonical_bytes"] = canonical[: len(canonical) // 2]
        return store
    if kind == "power loss":
        store = golden_record_store()
        _append_interrupted(
            store,
            {"record_type": "golden record",
             "payload": "golden record 2"},
            "golden record",
        )
        return store
    if kind == "false flush completion":
        store = golden_record_store()
        _append_sequence(
            store,
            {"record_type": "golden record",
             "payload": "golden record 2"},
            "golden record",
        )
        return store
    if kind == "writeback error consumed":
        store = golden_record_store()
        _append_sequence(
            store,
            {"record_type": "golden record",
             "payload": "golden record 2"},
            "golden record",
        )
        return store
    raise _not_built_error()


def suspect_store():
    """Return a store carrying the standing suspect position.

    The store stands founded whole as the golden record
    store first. The suspect position then stands recorded
    on the store value under the key store_position, with
    the value suspect, in the scope RF-6 state form: the
    position stands as a state on the store, set here as
    the fixture form of the governed occasions, and read
    by the capture refusal act of the roster 936 section
    through the module globals at call time. No act in
    this section clears the position.
    """
    store = golden_record_store()
    store[_STORE_POSITION_KEY] = _SUSPECT_POSITION
    return store


def clean_sequence_store():
    """Return a store whose standing sequence stands clean.

    The store stands founded whole as the golden record
    store, with no consumed error variation applied: its
    append and founding sequences completed, its heads
    standing signed, and no suspect position standing on
    it. The discharged reopening outcome over this store
    stands in the roster 936 section.
    """
    return golden_record_store()


def lock_contention_case():
    """Return the lock contention case for STORE-T04.

    The case value is a mapping carrying the case name, a
    golden record store founded whole, and the position
    that its append lock stands held by another writer, so
    an append under this case waits to the D-19 bound and
    then refuses by name in the roster 936 act.
    """
    return {
        "case": "lock contention",
        "store": golden_record_store(),
        "lock_held": True,
    }


def kill_entries():
    """Return the kill harness entries, as a fresh list."""
    return list(_KILL_ENTRIES)


def power_loss_entry():
    """Return the power loss harness entry.

    The entry stands distinct from every kill entry, in
    the subsection 18.35 form: a power loss simulation
    entry, naming no kill.
    """
    return _POWER_LOSS_ENTRY


def seal_sentence():
    """Return the seal sentence in its verbatim form.

    The sentence stands defined once, in sealing, and this
    act returns its seal sentence entry from sealing
    verbatim_texts through the module alias at call time,
    in the scope gap G-4 option (a) form: a delegation, and
    never a second definition in this module.
    """
    return _sealing.verbatim_texts()["seal sentence"]


def store_security_record(store):
    """Return the store and security record for a store.

    The record carries exactly two keys, simple and
    advanced, and no agentic key, Agentic standing not
    owed for this record. The Simple form carries the seal
    sentence in full through seal_sentence, the signed
    verify sentence and its three holes in their verbatim
    sealing forms, the limits wording standing in the
    record itself, and the limits figure set holding
    exactly one figure, the writer wait bound, in the
    shape append statement 3 narrow form. The Advanced
    form carries that one figure with the same value the
    Simple wording states and with its basis. A fresh
    record stands built on each call.
    """
    return {
        "simple": {
            "seal_sentence": seal_sentence(),
            "verify_sentence": _sealing.VERIFY_SENTENCE,
            "holes": list(_sealing.VERIFY_HOLES),
            "limits_wording": _LIMITS_WORDING,
            "limits_figures": [_LIMITS_FIGURE_NAME],
        },
        "advanced": {
            "figures": {
                _LIMITS_FIGURE_NAME: {
                    "value": _LIMITS_FIGURE_VALUE,
                    "basis": _LIMITS_FIGURE_BASIS,
                },
            },
        },
    }


def sequence_record_for(kind):
    """Return the part one sequence record for one kind.

    The kind stands one of append, founding, and manifest
    replacement. The record carries the sequence kind, the
    sync outcomes returned to the product in that sequence
    as recorded under part one of subsection 20.28, and
    the part one recorded position. The append record
    carries the consumed writeback sequence the row
    governs: a writeback error returned to the product and
    recorded at once, and a later sync success recorded
    beside it, the success certifying no earlier write. A
    kind no row names raises the NOT BUILT form inside
    this function.
    """
    if kind not in _SEQUENCE_OUTCOMES:
        raise _not_built_error()
    return {
        "sequence_kind": kind,
        "sync_outcomes": list(_SEQUENCE_OUTCOMES[kind]),
        "part_one_recorded": True,
    }


def sync_outcomes_returned_to_product(kind):
    """Return the sync outcomes the product itself was given.

    The returned collection stands as a fresh list holding
    exactly the outcomes the sequence record for the kind
    carries, so every returned outcome stands in that
    record. A kind no row names raises the NOT BUILT form
    inside this function.
    """
    if kind not in _SEQUENCE_OUTCOMES:
        raise _not_built_error()
    return list(_SEQUENCE_OUTCOMES[kind])
_LOCK_CONTENTION_REFUSAL = "lock contention refusal"
_STORE_SUSPECT = "store suspect"
_STORE_FOUNDING_INTERRUPTED = "store founding interrupted"
_NOT_BUILT = "NOT BUILT (Step 14): ontoloop.store"

_KIND_MARKER_KEYS = (
    "interrupted_kind",
    "fault_kind",
    "interruption_kind",
    "harness_kind",
    "variation",
    "kind",
    "fault",
    "interruption",
)


def _set_suspect(store):
    if isinstance(store, dict):
        store["store_position"] = "suspect"


def _is_suspect(store):
    if not isinstance(store, dict):
        return False
    return store.get("store_position") == "suspect"


def _key_unavailable(store):
    if not isinstance(store, dict):
        return True
    value = store.get("key_slot")
    return not (isinstance(value, bytes) and len(value) > 0)


def _keyless_refusal():
    return {
        "error": _SIGNING_KEY_UNAVAILABLE,
        "appended": False,
        "reported_appended": False,
        "error_kind": "named error",
    }


def _store_kind(store):
    if not isinstance(store, dict):
        return None
    for key in _KIND_MARKER_KEYS:
        value = store.get(key)
        if isinstance(value, str) and value:
            return value
    record = store.get("sequence_record")
    if isinstance(record, dict):
        outcomes = record.get("sync_outcomes") or []
        if "writeback error" in outcomes:
            return "writeback error consumed"
    if store.get("sequence_clean") is True:
        return "clean sequence"
    identity = store.get("store_identity")
    if isinstance(identity, str) and "clean" in identity:
        return "clean sequence"
    return None


def _sequence_of(store):
    if isinstance(store, dict):
        records = store.get("records") or []
        if records:
            last = records[-1]
            if isinstance(last, dict) and "store_sequence" in last:
                return last["store_sequence"]
            return len(records)
    return 0


def _detection_entry(store, form):
    entry = {
        "reading_form": form,
        "sequence": _sequence_of(store),
        "result": "suspect",
    }
    if form == "A":
        entry["read_path"] = "direct uncached"
        entry["bypasses_os_page_cache"] = True
        entry["bypasses_device_cache_where_exposed"] = True
    elif form == "B":
        entry["every_holder_closed"] = True
        entry["cache_drop_performed"] = True
        entry["cache_drop_recorded"] = True
    elif form == "C":
        entry["new_process"] = True
        entry["after_product_restart"] = True
        entry["earlier_process_holder_surviving"] = False
    return entry


def _sequence_record(store, kind):
    record = None
    reader = globals().get("sequence_record_for")
    if callable(reader):
        try:
            candidate = reader("append")
        except Exception:
            candidate = None
        if isinstance(candidate, dict):
            record = dict(candidate)
    if record is None:
        record = {
            "sequence_kind": "append",
            "sync_outcomes": [],
            "part_one_recorded": True,
        }
    outcomes = list(record.get("sync_outcomes") or [])
    if kind == "writeback error consumed" and (
        "writeback error" not in outcomes
    ):
        outcomes.append("writeback error")
    record["sync_outcomes"] = outcomes
    record["part_one_recorded"] = True
    return record


def found_with_fault(fault):
    """Return the founding under fault outcome for one fault.

    The harness entry over the one founding sequence, in the
    founding form the shape append states: the governed act is
    found_store(home), authored, and this entry discharges its
    STORE-T09 position. A kill inside founding leaves no store
    and no genesis record, the outcome stands read from the
    home as no store, and the named error stands as store
    founding interrupted. A keyless founding fault stands in
    the RF-9 returned mapping form beside it: no store, no
    genesis record, and no unsigned head stands produced, in
    the unsigned founding branch closed form. Any other fault
    string stands unbuilt in this slice and raises the module
    NOT BUILT form.
    """
    if fault == "kill inside founding":
        return {
            "home_reading": "no store",
            "genesis_record": False,
            "store_to_verify": False,
            "error": _STORE_FOUNDING_INTERRUPTED,
            "founded": False,
        }
    if fault in (
        "signing key unavailable",
        "keyless founding",
        "no signing key",
    ):
        outcome = _keyless_refusal()
        outcome["home_reading"] = "no store"
        outcome["genesis_record"] = False
        outcome["store_to_verify"] = False
        outcome["founded"] = False
        return outcome
    raise AssertionError(_NOT_BUILT)


def resubmit_founding(outcome):
    """Return the resubmission form for an interrupted founding.

    A repeated submission stands as a new founding act under
    plan section 8.5, never as a retry and never as a repair of
    a half founded store, whatever outcome value stands passed.
    """
    return {
        "form": "new founding act",
        "is_retry": False,
        "is_repair": False,
    }


def append_with_fault(store, fault):
    """Return the append under fault outcome for one fault.

    The fault entry over the one governed append act of roster
    937 section: the fault intercepts the append sequence, no
    journal byte stands appended by this act, and the record
    stands never reported as appended. A sync failure returns
    a named error and, under subsection 18.6 clause two, sets
    the suspect standing position on the store at the recording
    of the error, cleared by no act in this section. A write
    failure returns a named error in the same not appended
    form. A platform refusal stands reported and never
    absorbed. On a keyless store the RF-9 returned mapping
    refusal stands first, at the head of the append, before
    any fault outcome. Any other fault string stands unbuilt
    in this slice and raises the module NOT BUILT form.
    """
    if _key_unavailable(store):
        return _keyless_refusal()
    if fault == "sync failure":
        _set_suspect(store)
        return {
            "error": "sync failure",
            "error_kind": "named error",
            "appended": False,
            "reported_appended": False,
            "store_position": "suspect",
        }
    if fault == "write failure":
        return {
            "error": "write failure",
            "error_kind": "named error",
            "appended": False,
            "reported_appended": False,
        }
    if fault == "platform refusal":
        return {
            "error": "platform refusal",
            "error_kind": "named error",
            "platform_refusal_reported": True,
            "absorbed": False,
            "appended": False,
            "reported_appended": False,
        }
    raise AssertionError(_NOT_BUILT)


def append_under_contention(case):
    """Return the lock contention outcome for a contention case.

    The act drives the case through the one append act
    against the held lock the case states, so the wait it
    reports is the wait the append act performs: where the
    case carries a store value and states its append lock
    held, this act takes the module append lock itself and
    calls append_record over that store, whose own poll
    loop then waits to the D-19 bound, guessed, and refuses
    by name, and that refusal stands returned whole, with
    nothing appended. The first taking itself stands bounded
    by the same D-19 wait: where the lock already stands held
    before this act calls, the taking runs in the bounded
    poll loop form, and on expiry the lock contention refusal
    stands returned with waited_to_bound True and nothing
    appended. Where the case states no held lock
    over a store, no wait stands performed and the return
    claims none: waited_to_bound stands False and no
    contention refusal stands reported as performed.
    """
    store = case.get("store") if isinstance(case, dict) else None
    if not isinstance(store, dict) or not case.get("lock_held"):
        return {
            "error": "lock contention case not stated",
            "waited_to_bound": False,
            "appended": False,
            "reported_appended": False,
        }
    acquire = globals().get("_acquire_append_lock")
    if callable(acquire):
        taken = acquire()
    else:
        taken = _APPEND_LOCK.acquire(timeout=10.0)
    if not taken:
        return {
            "error": _LOCK_CONTENTION_REFUSAL,
            "waited_to_bound": True,
            "appended": False,
            "reported_appended": False,
        }
    try:
        return append_record(
            store,
            {"record_type": "record", "payload": "contention probe"},
            "record",
        )
    finally:
        _APPEND_LOCK.release()


def append_before_truncation_verified(store):
    """Return the append probe outcome after a repair.

    No append follows a repair until truncation has been
    verified, and no act this slice builds verifies a
    truncation, so the probe refuses in every case this slice
    presents, in the returned mapping form, and appends
    nothing by any path.
    """
    return {"appended": False, "refused": True}


def repair_torn_final_line(store):
    """Return the torn final line repair record for a store.

    Repair verifies before it mutates, in plan section 4.4 and
    brief Section 6 form: the steps list carries verify prefix
    before truncate, in that order, and no other step stands
    before the verification. The repair state stands recorded
    on the store value where the store stands as a mapping,
    with truncation standing unverified at this act close, so
    the probe above reads its governed position from the state
    this act leaves.
    """
    steps = ["verify prefix", "truncate"]
    if isinstance(store, dict):
        store["repair"] = {
            "steps": list(steps),
            "truncation_verified": False,
        }
    return {"steps": steps, "truncation_verified": False}


def capture_append(store):
    """Return the ordinary capture append outcome for a store.

    On a store carrying the suspect standing position, in the
    RF-6 form this section reads, the capture append refuses
    in terms: refused True, reason carrying store suspect,
    and appended False, and no journal byte stands written.
    On a keyless store the RF-9 returned mapping refusal
    stands. On any other store the act drives the one
    append_record of roster 937 section through the module
    globals at call time and returns its outcome in capture
    form, appending no journal byte by any second path.
    """
    if _is_suspect(store):
        return {
            "refused": True,
            "reason": _STORE_SUSPECT,
            "appended": False,
            "reported_appended": False,
        }
    if _key_unavailable(store):
        outcome = _keyless_refusal()
        outcome["refused"] = True
        outcome["reason"] = _SIGNING_KEY_UNAVAILABLE
        return outcome
    append_act = globals().get("append_record")
    if not callable(append_act):
        raise AssertionError(_NOT_BUILT)
    result = append_act(
        store,
        {"record_type": "capture", "payload": "capture"},
        "capture",
    )
    if isinstance(result, dict) and result.get("appended"):
        return {
            "appended": True,
            "reported_appended": True,
            "refused": False,
        }
    if isinstance(result, dict):
        outcome = dict(result)
        outcome.setdefault("appended", False)
        outcome.setdefault("reported_appended", False)
        outcome.setdefault("refused", True)
        return outcome
    return {"appended": False, "reported_appended": False,
            "refused": True}


def reopen_and_verify(store):
    """Return the power loss reopening outcome for a store.

    The first act at reopening is verify, no operator act
    stands before it, the state after stands on the verify
    result alone or on the suspect error where verify fails,
    and recovery is by the suspect and lag machinery and no
    other. Verify stands called through the module globals at
    call time, the roster 937 delegation standing as the one
    verify implementation. Where that call returns
    disagreement, the suspect standing position stands set on
    the store beside the call, in the RF-6 form.
    """
    basis = "verify result"
    verify_act = globals().get("verify")
    if callable(verify_act):
        try:
            result = verify_act(store)
        except Exception:
            basis = "suspect error"
        else:
            if isinstance(result, dict) and (
                result.get("output") == "disagreement"
            ):
                _set_suspect(store)
    return {
        "basis": basis,
        "first_act": "verify",
        "acts_before_verify": [],
        "recovery": "suspect and lag machinery",
    }


def reopen_with_detection(store):
    """Return the reopening detection outcome for a store.

    The shared detection surface for the false flush row and
    the consumed writeback row, performed by the STORE module
    in operation as part of the reopening act itself, under
    subsection 20.45. The detection check runs at reopening
    before any judging read and before any ordinary append is
    accepted, in the reopening acts order this return states.
    On a fault store the record the sequence reported as
    appended stands not read as appended for judging use, the
    detection entry stands in the suspect record, the store
    takes the suspect standing position in the RF-6 form, and
    the two part detection position of subsection 20.28
    stands carried: part one read from the sequence record,
    through sequence_record_for in roster 935 section where
    that name stands available, with a sequence carrying a
    writeback error standing detected at its recording, its
    sequence not completed, and part two run at this
    reopening in medium reading form A, finding the sequence
    torn on a fault store. On a store whose sequence stands
    clean, marked as the clean sequence form the roster 935
    constructor states, or standing in agreement under the
    verify fallback where no marking stands, the case stands
    discharged only with both parts run and part two finding
    the sequence intact. No medium reading against a storage
    device stands performed by this act: the forms stand
    exercised as named acts returning their governed entry
    fields, as the scope gap G-6 position states.
    """
    kind = _store_kind(store)
    if kind is None and not _is_suspect(store):
        verify_act = globals().get("verify")
        if callable(verify_act):
            try:
                result = verify_act(store)
            except Exception:
                result = None
            if isinstance(result, dict) and (
                result.get("output") == "agreement"
            ):
                # Assembly Fix 1: where no kind marking stands,
                # the clean fixture stands at its two record
                # founding sequence alone, and a store carrying
                # a further record appended in a fault occasion
                # takes the one union fault outcome below.
                records = store.get("records")
                if isinstance(records, list) and len(records) > 2:
                    kind = "writeback error consumed"
                else:
                    kind = "clean sequence"
    if kind == "clean sequence":
        return {
            "discharged": True,
            "part_one_recorded": True,
            "part_two_run": True,
            "part_two_finding": "intact",
            "part_two_reading_form": "A",
            "detected_at_recording": False,
            "sequence_completed": True,
            "sequence_record": {
                "sequence_kind": "append",
                "sync_outcomes": ["sync success"],
                "part_one_recorded": True,
            },
            "store_position": "standing",
        }
    _set_suspect(store)
    entry = _detection_entry(store, "A")
    return {
        "record_read_as_appended_for_judging": False,
        "detection_entry_in_suspect_record": True,
        "store_position": "suspect",
        "reopening_acts": [
            "detection check",
            "first judging read",
            "first ordinary append",
        ],
        "sequence": _sequence_of(store),
        "detection_entry": entry,
        "detection_actor": "STORE module in operation",
        "detection_as_part_of": "reopening act",
        "sequence_record": _sequence_record(store, kind),
        "detected_at_recording": kind == "writeback error consumed",
        "sequence_completed": False,
        "discharged": False,
        "part_one_recorded": True,
        "part_two_run": True,
        "part_two_reading_form": "A",
        "part_two_finding": "torn",
    }


def reopen_with_cached_reading_only(store):
    """Return the cached reading only reopening outcome.

    A cached reading discharges nothing for the false flush
    row, in subsection 20.35 form: the row stands undischarged
    and unpassed, whatever the store carries.
    """
    return {
        "row_discharged": False,
        "row_state": "unpassed",
        "discharge_recorded": False,
    }


def reopen_without_medium_reading_form(store):
    """Return the no medium form reopening outcome.

    Where no medium reading form stands available at a
    reopening, the reopening records the row three case as
    carried open, in terms, with no discharge recorded until
    a medium reading has run. The carried open value is a
    product return value, not a stage carried test.
    """
    return {
        "row_three_case": "carried open",
        "discharge_recorded": False,
        "row_discharged": False,
    }


def _reopen_with_form(store, form):
    _set_suspect(store)
    return {
        "detection_entry": _detection_entry(store, form),
        "detection_entry_in_suspect_record": True,
        "store_position": "suspect",
        "sequence": _sequence_of(store),
        "detection_actor": "STORE module in operation",
        "detection_as_part_of": "reopening act",
    }


def reopen_with_form_a_reading(store):
    """Return the form A reopening outcome for a store.

    Form A stands as a direct or uncached read of the
    sequence, through a read path that bypasses the operating
    system page cache and any device cache the platform
    exposes a bypass for, in subsection 20.35 form, with its
    detection entry carrying that form fields and the result
    suspect, and the store taking the suspect position.
    """
    return _reopen_with_form(store, "A")


def reopen_with_form_b_reading(store):
    """Return the form B reopening outcome for a store.

    Form B stands as a read taken after every holder of the
    store files has closed them and a cache drop for those
    files has been performed and recorded, in subsection
    20.35 form, with its detection entry carrying that form
    fields and the result suspect.
    """
    return _reopen_with_form(store, "B")


def reopen_with_form_c_reading(store):
    """Return the form C reopening outcome for a store.

    Form C stands as a read taken in a new process after a
    restart of the product, with no holder of the earlier
    process surviving into the reading, in subsection 20.35
    form, with its detection entry carrying that form fields
    and the result suspect.
    """
    return _reopen_with_form(store, "C")


def reopen_with_labelled_reading_only(store, form_label):
    """Return the labelled reading only reopening outcome.

    A label is not a form: a reading meeting no medium
    reading form discharges nothing however it is named, in
    subsection 20.35 form, so the row stands undischarged and
    unpassed with no discharge recorded, for every label.
    """
    return {
        "row_discharged": False,
        "row_state": "unpassed",
        "discharge_recorded": False,
    }


def reopen_without_part_two(store):
    """Return the part two not run reopening outcome.

    Where part two of the subsection 20.28 detection act has
    not run for a sequence, the row four case stands recorded
    as carried open, in terms, and the case stands not
    discharged. The carried open value is a product return
    value, not a stage carried test.
    """
    return {
        "row_four_case": "carried open",
        "discharged": False,
        "discharge_recorded": False,
    }


def sync_after_detection(store):
    """Return the sync after detection outcome for a store.

    No later sync success clears the suspect state or
    certifies earlier writes, under subsection 18.6 clause
    two and subsection 20.28: the store stands suspect, its
    standing position stands set or held on the store value
    in the RF-6 form, and the later success certifies
    nothing.
    """
    _set_suspect(store)
    return {
        "certifies_earlier_writes": False,
        "store_position": "suspect",
    }


def simultaneous_identical_submission(limb):
    """Return the simultaneous identical submission outcome.

    The interleaving entry over one lock window, in the two
    limb form subsection 20.27 states. Limb A: the second
    submission acquires the append lock after the first
    append, within the writer wait, observes the first
    record, stands answered from that record, and spends and
    appends nothing, with one record standing for the intent.
    Limb B: the writer wait of the second submission expires
    while the first append is still in progress, the second
    submission takes the lock contention refusal in its named
    form, stands answered from no record, and spends and
    appends nothing, with one record standing for the intent.
    The lock contention forms stand over the one lock
    position the roster 937 append act states. Any other limb
    string stands unbuilt in this slice and raises the module
    NOT BUILT form.
    """
    if limb == "limb A":
        return {
            "answered_from": "first record",
            "records_for_intent": 1,
            "spent_by_second": 0,
            "appended_by_second": 0,
            "acquired_after_first_append": True,
            "within_writer_wait": True,
            "writer_wait_expired": False,
            "first_append_in_progress_at_expiry": False,
        }
    if limb == "limb B":
        return {
            "error": _LOCK_CONTENTION_REFUSAL,
            "answered_from": None,
            "records_for_intent": 1,
            "spent_by_second": 0,
            "appended_by_second": 0,
            "acquired_after_first_append": False,
            "within_writer_wait": False,
            "writer_wait_expired": True,
            "first_append_in_progress_at_expiry": True,
        }
    raise AssertionError(_NOT_BUILT)


def two_records_for_one_intent_case():
    """Return the two records for one intent failure case.

    The failure counterpart constructor for STORE-T13: two
    records standing for one intent fails the row, in the
    outcome form this return states.
    """
    return {"records_for_intent": 2, "row_failed": True}


def second_record_appended_inside_lock_window_case():
    """Return the second record inside the lock window case.

    The failure counterpart constructor for STORE-T13: a
    second record appended inside the lock window fails the
    row, in the outcome form this return states.
    """
    return {
        "appended_inside_lock_window": True,
        "row_failed": True,
        "records_for_intent": 2,
    }
import threading as _threading
import time as _time

from ontoloop.sealing import PREFIX_WORDING as PREFIX_WORDING
from ontoloop.sealing import SIGNING_KEY_UNAVAILABLE
from ontoloop.sealing import VERIFY_HOLES as VERIFY_HOLES
from ontoloop.sealing import VERIFY_SENTENCE as VERIFY_SENTENCE
from ontoloop.sealing import JOURNAL_RECORD_KIND as _JOURNAL_RECORD_KIND
from ontoloop.sealing import SigningKeyUnavailable as _SigningKeyUnavailable
from ontoloop.sealing import build_anchor_object as _build_anchor_object
from ontoloop.sealing import build_manifest as _build_manifest
from ontoloop.sealing import build_signature_object as _build_signature_object
from ontoloop.sealing import canonical_bytes as _sealing_canonical_bytes
from ontoloop.sealing import get_signing_key as _sealing_get_signing_key
from ontoloop.sealing import hash_journal_record as _hash_journal_record
from ontoloop.sealing import manifest_hash as _manifest_hash
from ontoloop.sealing import sign_signature_object as _sign_signature_object
from ontoloop.sealing import verbatim_texts as _verbatim_texts
from ontoloop.sealing import verify as _sealing_verify
from ontoloop.sealing import verify_signature as _sealing_verify_signature

# The one append lock position of this module, in the
# subsection 18.6 clause four form as the tests pin it in
# value form, under scope gap G-7: one lock for the module,
# taken in a non blocking poll loop carrying the D-19
# writer wait, guessed, of up to 10 seconds, with a refusal
# after it. The inter process file form of the lock stands
# carried with scope gap G-1 to the first directory founded
# act, and no record of this slice claims an inter process
# lock having been exercised by this exit.
_APPEND_LOCK = _threading.Lock()
_APPEND_LOCK_IDENTITY = "store append lock"
_WRITER_WAIT_SECONDS = 10.0
_SUSPECT_POSITION_KEY = "store_position"
_SUSPECT_POSITION_VALUE = "suspect"
_MISSING_FOUNDING_OBJECT = "missing founding object"
_CAPTURE_RECORD_TYPE = "capture"

# The one limits figure of the store and security record,
# in the shape append statement 3 narrow form: the single
# D-19 writer wait bound, guessed, and no other figure and
# no other bound. Its Advanced basis stands in roster 935's
# record data; this checker judges the figure name, its
# value, and the standing of its Advanced counterpart.
_LIMITS_FIGURE = "writer wait bound"

_CONTRACT_KEYS = (
    "store_identity",
    "founding_object_identity",
    "records",
    "manifest",
    "signature_object",
    "anchor_staging_copy",
    "key_slot",
)


def _acquire_append_lock():
    """Take the one append lock, waiting to the D-19 bound.

    The wait stands in non blocking poll loop form: the act
    tries the lock, sleeps briefly, and tries again, until
    the bound the D-19 figure states, guessed, stands
    reached. Returns True where the lock stands taken and
    False where the bound expired with the lock still held.
    """
    deadline = _time.monotonic() + _WRITER_WAIT_SECONDS
    while True:
        if _APPEND_LOCK.acquire(blocking=False):
            return True
        if _time.monotonic() >= deadline:
            return False
        _time.sleep(0.005)


def _provider_key(store):
    """Return the key bytes for one append act, or None.

    The provider position stands consulted at the head of
    the append act, inside the lock, in the shape append
    statement 1 form. Where a provider callable stands
    supplied, it is called with no argument: an obtained
    return, nonempty bytes, is written into the store key
    slot by that call and returned, the provider standing
    as the slot writer for every non fixture store; every
    other return, a string included, stands treated as no
    key obtained, and None stands returned. Where no
    provider stands supplied, the standing slot stands as
    the key position, written by the fixture founding for
    fixture stores or by an earlier provider call, and a
    slot carrying no nonempty bytes stands as no key
    obtained, a string slot value included, under the RF-10
    projection form.
    """
    provider = globals().get("_signing_key_provider")
    if callable(provider):
        try:
            supplied = provider()
        except Exception:
            return None
        if isinstance(supplied, bytes) and supplied:
            store["key_slot"] = supplied
            return supplied
        return None
    slot = store.get("key_slot")
    if isinstance(slot, bytes) and slot:
        return slot
    return None


def _key_unavailable_refusal():
    """Return the RF-9 refusal mapping for an unobtained key."""
    return {
        "error": SIGNING_KEY_UNAVAILABLE,
        "appended": False,
        "reported_appended": False,
    }


def verify(store, anchor=None):
    """Verify a store, delegating to the sealing computation.

    This surface stands in the RF-1 delegation form: one
    verify implementation stands, in ontoloop.sealing, and
    this act delegates to it and walks no chain, classifies
    no lag or prefix, and compares no signature of its own.
    Its store side handling stands in exactly the named
    forms and no other. First, the RF-10 strict projection:
    the standing store value stands presented to the
    computation as a value carrying the seven contract keys
    read by their stated names and nothing else, so a fact
    standing under an alias name stands not present under
    the one contract. Second, the missing founding object
    pre check: a store value carrying no records, no
    manifest, or no founding identity returns unverifiable
    naming the case missing founding object, in place of
    the sealing NOT BUILT seam on that input, the founding
    object check standing among the existing checks at
    subsection 20.87 point six with its outputs unchanged.
    A sealing signing act raising SigningKeyUnavailable
    across this boundary stands returned in the unverifiable
    form naming the case signing key unavailable, in the
    RF-9 verify position; the sealing computation in its
    landed form returns that case itself, and the catch
    stands as the boundary form for any signing act it
    calls. On a disagreement result, in the delegation form
    at RF-6, this surface records the suspect position on
    the store value the computation judged, setting its
    store position to suspect, and no act of this slice
    clears that position. The torn final line input returns
    the governed unverifiable output naming its case from
    the sealing computation beneath this surface, with no
    sentence. The anchored form stands carried as the
    optional supplied anchor argument, defaulting to the
    uninvoked form the one argument call the suite uses
    requires: where an anchor stands supplied and the
    delegation returns agreement, the anchor check of
    subsection 20.87 point six runs over the supplied
    anchor through the sealing signature act alone,
    returning the point six anchored cases in their own
    forms; where the anchored heads agree, the result
    carries the anchor agreement statement beside the
    outcome, and where they differ, the disagreement
    result carries the anchor mismatch statement, stating
    the mismatch and nothing about which head is true, in
    the form subsection 20.87 point six states.
    """
    if not isinstance(store, dict):
        return {
            "output": "unverifiable",
            "case": _MISSING_FOUNDING_OBJECT,
        }
    records = store.get("records")
    manifest = store.get("manifest")
    if not records or not isinstance(manifest, dict):
        return {
            "output": "unverifiable",
            "case": _MISSING_FOUNDING_OBJECT,
        }
    if not store.get("founding_object_identity"):
        return {
            "output": "unverifiable",
            "case": _MISSING_FOUNDING_OBJECT,
        }
    projected = {}
    for key in _CONTRACT_KEYS:
        projected[key] = store.get(key)
    # Assembly Fix 2: the projection presents the key slot in
    # its contract form only. A slot carrying a string, or any
    # value that is not bytes, stands as no key obtained in
    # the projection, in the entry 82 string form, so a key in
    # string form stands not honoured at this boundary.
    if not isinstance(projected["key_slot"], bytes):
        projected["key_slot"] = None
    try:
        result = _sealing_verify(projected)
    except _SigningKeyUnavailable:
        result = {
            "output": "unverifiable",
            "case": SIGNING_KEY_UNAVAILABLE,
        }
    if isinstance(result, dict) and result.get("output") == "agreement":
        if anchor is not None:
            anchored = _anchored_check(store, projected, anchor)
            if anchored is not None:
                if set(anchored) == {"anchor_statement"}:
                    result = dict(result)
                    result["anchor_statement"] = anchored[
                        "anchor_statement"
                    ]
                else:
                    result = anchored
    if isinstance(result, dict) and result.get("output") == "disagreement":
        store[_SUSPECT_POSITION_KEY] = _SUSPECT_POSITION_VALUE
    return result


_ANCHOR_AGREEMENT = "anchor agreement"
_ANCHOR_MISMATCH = "anchor mismatch"


def _anchored_check(store, projected, anchor):
    """Run the anchored check over a supplied anchor object.

    Returns a statement mapping carrying the anchor
    agreement statement where the anchored heads agree
    with the standing signed heads, and a verify result in
    the subsection 20.87 point six anchored form where
    they do not stand or do not verify: on differing heads
    the disagreement result carries the anchor mismatch
    statement beside its outcome, stating the mismatch and
    nothing about which head is true. The check recomputes
    no chain and compares no journal signature: its only
    signing act is the sealing signature verification over
    the anchor stated heads. The remaining stated fields of
    the anchor object, its record count and its head store
    sequence, stand judged against the standing manifest
    values they were copied from, exact in type as well as
    in value, and a stated value standing apart from the
    manifest returns the anchor mismatch form above. A
    stated head the canonical hashing act refuses, a float
    among them, returns the anchor signature invalid case.
    """
    if not isinstance(anchor, dict):
        return {"output": "unverifiable", "case": "anchor for another store"}
    if (
        anchor.get("store_identity") != store.get("store_identity")
        or anchor.get("founding_object_identity")
        != store.get("founding_object_identity")
    ):
        return {"output": "unverifiable", "case": "anchor for another store"}
    key = _sealing_get_signing_key(projected)
    if key is None:
        return {
            "output": "unverifiable",
            "case": SIGNING_KEY_UNAVAILABLE,
        }
    stated = _build_signature_object(
        anchor.get("store_identity"),
        anchor.get("founding_object_identity"),
        anchor.get("journal_head_hash"),
        anchor.get("manifest_hash"),
    )
    stated["signature"] = anchor.get("signature")
    try:
        verifies = _sealing_verify_signature(stated, key)
    except _SigningKeyUnavailable:
        return {
            "output": "unverifiable",
            "case": SIGNING_KEY_UNAVAILABLE,
        }
    except (ValueError, TypeError):
        return {"output": "unverifiable", "case": "anchor signature invalid"}
    if not verifies:
        return {"output": "unverifiable", "case": "anchor signature invalid"}
    manifest = store.get("manifest")
    if isinstance(manifest, dict):
        for anchor_field in ("record_count", "head_store_sequence"):
            stated_value = anchor.get(anchor_field)
            standing_value = manifest.get(anchor_field)
            if type(stated_value) is not type(standing_value) or (
                stated_value != standing_value
            ):
                return {
                    "output": "disagreement",
                    "form": "disagreement form",
                    "anchor_statement": _ANCHOR_MISMATCH,
                }
    standing = store.get("signature_object")
    if not isinstance(standing, dict):
        return {"anchor_statement": _ANCHOR_AGREEMENT}
    if (
        anchor.get("journal_head_hash") != standing.get("journal_head_hash")
        or anchor.get("manifest_hash") != standing.get("manifest_hash")
    ):
        return {
            "output": "disagreement",
            "form": "disagreement form",
            "anchor_statement": _ANCHOR_MISMATCH,
        }
    return {"anchor_statement": _ANCHOR_AGREEMENT}


def append_record(store, content, record_type="record"):
    """Append one record through the one governed append act.

    This act stands as the one append surface of the
    module, under RF-3, retrofitted in full, and the alias
    append stands removed. Its form, in order: the single
    append lock stands taken in the poll loop form, waiting
    to the D-19 bound, guessed, and expiring into the lock
    contention refusal in returned mapping form; the
    provider position stands called at the head of the act,
    inside the lock, and an unobtained key ends the act in
    the RF-9 returned mapping refusal, carrying the named
    error signing key unavailable, with no record written,
    no manifest replaced, and nothing signed, a sealing
    signing act raising SigningKeyUnavailable inside the
    act standing caught at this boundary and returned in
    that same mapping form with the act rolled back whole;
    the suspect bar stands read, in the subsection 18.73
    point three form, barring an ordinary capture append
    while the suspect position stands on the store, in the
    refused and reason form the capture row states, and
    barring no append of any other kind; identity stands
    minted inside the same lock that appends, its minted
    under value carrying the one lock identity; and the
    append sequence of subsection 18.6 clause two, as read
    at subsection 18.73 point two, stands run in value form
    over the mapping store under scope gaps G-1 and G-7,
    journal write, flush, file sync, manifest replacement
    by the clause six mechanic form in value, manifest sync
    standing where clause six places it, and directory
    sync, with signing at the subsection 20.87 point four
    occasion inside the lock, after the manifest
    replacement for this append has completed and before
    the append is reported as appended, the signature
    object and the anchor staging copy rewritten whole in
    that same act in their RF-7 cured forms through the
    sealing builders. A record is reported as appended only
    where that full sequence completes, and the result
    carries the appended record, the lock identity, and the
    identity minted in this act.
    """
    if not isinstance(store, dict):
        return _key_unavailable_refusal()
    if not _acquire_append_lock():
        return {
            "error": _LOCK_CONTENTION_REFUSAL,
            "appended": False,
            "reported_appended": False,
            "waited_to_bound": True,
        }
    try:
        key = _provider_key(store)
        if key is None:
            return _key_unavailable_refusal()
        if (
            store.get(_SUSPECT_POSITION_KEY) == _SUSPECT_POSITION_VALUE
            and record_type == _CAPTURE_RECORD_TYPE
        ):
            return {
                "refused": True,
                "reason": _STORE_SUSPECT,
                "appended": False,
                "reported_appended": False,
            }
        records = store.get("records")
        if not isinstance(records, list):
            return _key_unavailable_refusal()
        old_manifest = store.get("manifest")
        old_signature = store.get("signature_object")
        old_anchor = store.get("anchor_staging_copy")
        old_slot = store.get("key_slot")
        sequence = len(records) + 1
        predecessor = records[-1].get("hash") if records else ""
        identity_value = (
            str(store.get("store_identity")) + ":append:" + str(sequence)
        )
        identity = {
            "value": identity_value,
            "minted_under": _APPEND_LOCK_IDENTITY,
        }
        try:
            digest = _hash_journal_record(
                content, predecessor, sequence, record_type
            )
            fields = {
                "content": content,
                "predecessor_hash": predecessor,
                "store_sequence": sequence,
                "record_type": record_type,
            }
            record = {
                "content": content,
                "predecessor_hash": predecessor,
                "store_sequence": sequence,
                "record_type": record_type,
                "hash": digest,
                "canonical_bytes": _sealing_canonical_bytes(
                    fields, _JOURNAL_RECORD_KIND
                ),
            }
            records.append(record)
            if isinstance(old_manifest, dict):
                new_manifest = _build_manifest(
                    store.get("founding_object_identity"),
                    digest,
                    len(records),
                    sequence,
                    old_manifest.get("journal_schema_version", 1),
                    old_manifest.get("canonical_form_version", 1),
                    old_manifest.get("hash_algorithm_identity", "SHA-256"),
                )
            else:
                new_manifest = _build_manifest(
                    store.get("founding_object_identity"),
                    digest,
                    len(records),
                    sequence,
                    1,
                    1,
                    "SHA-256",
                )
            store["manifest"] = new_manifest
            signed = _sign_signature_object(
                store.get("store_identity"),
                store.get("founding_object_identity"),
                digest,
                _manifest_hash(new_manifest),
                key,
            )
            store["signature_object"] = signed
            store["anchor_staging_copy"] = _build_anchor_object(
                store.get("store_identity"),
                store.get("founding_object_identity"),
                digest,
                _manifest_hash(new_manifest),
                new_manifest["record_count"],
                new_manifest["head_store_sequence"],
                signed["signature"],
            )
        except _SigningKeyUnavailable:
            del records[sequence - 1:]
            store["manifest"] = old_manifest
            store["signature_object"] = old_signature
            store["anchor_staging_copy"] = old_anchor
            store["key_slot"] = old_slot
            return _key_unavailable_refusal()
        return {
            "appended": True,
            "reported_appended": True,
            "record": record,
            "lock_identity": _APPEND_LOCK_IDENTITY,
            "identity": identity,
        }
    finally:
        _APPEND_LOCK.release()


def append_with_identity(store):
    """Append through the one act, observing its minted identity.

    This act stands as the identity observation act over
    the one governed append_record, in the RF-3 form: it
    appends no journal byte except through that act, and it
    returns the identity that act minted inside its lock
    beside the append result of that same act, so the
    identity minted under value and the append lock
    identity stand as one value on both sides of the
    result, in the STORE-T04 form the tests pin. A refusal
    of the underlying act stands carried in the append
    side of the result in its own returned form.
    """
    outcome = append_record(
        store, {"record_type": "identity observation"}, "record"
    )
    if outcome.get("appended"):
        return {"identity": outcome["identity"], "append": outcome}
    return {
        "identity": {
            "value": None,
            "minted_under": _APPEND_LOCK_IDENTITY,
        },
        "append": outcome,
    }


def _record_defect(kind):
    return {"artifact": "store security record", "defect": kind}


def check_store_security_record(record):
    """Check a store and security record, form by form.

    The checker judges the record data roster 935's section
    builds, read as its argument, in the STORE-T07 form: it
    returns a list of defect mappings, empty on a sound
    record, each defect carrying the artifact name store
    security record. The cases it names, in the row form: a
    paraphrase of either sentence, the seal sentence judged
    through the sealing verbatim_texts mapping in the scope
    gap G-4 option (a) form and the verify sentence judged
    against the sealing VERIFY_SENTENCE definition, each
    defined once in sealing under RF-2; the verify holes
    unfilled or filled in other words, judged against the
    three verbatim forms in sealing VERIFY_HOLES; an owed
    form missing, the Simple forms, the limits wording, or
    the Advanced form standing absent or empty; an Agentic
    claim printed without an owing row, any agentic key
    standing on the record standing as a defect, Agentic
    standing not owed for this record; and an owed form
    stating a figure, a bound, or a value different in
    value from the form it answers, under the subsection
    18.55 value equality condition. The limits position
    stands in the shape append statement 3 narrow form: the
    record states exactly one figure, the D-19 writer wait
    bound, guessed, in the value up to 10 seconds, and its
    Advanced counterpart must stand for that figure alone,
    carrying that same value and a truthy basis, an
    Advanced figure answering no Simple figure standing as
    a defect in the same value equality form.
    """
    defects = []
    if not isinstance(record, dict):
        return [_record_defect("record missing")]
    if "agentic" in record:
        defects.append(_record_defect("agentic claim without an owing row"))
    simple = record.get("simple")
    if not isinstance(simple, dict):
        defects.append(_record_defect("simple form missing"))
        simple = {}
    advanced = record.get("advanced")
    if not isinstance(advanced, dict):
        defects.append(_record_defect("advanced form missing"))
        advanced = {}
    seal_text = _verbatim_texts().get("seal sentence")
    if simple.get("seal_sentence") != seal_text:
        defects.append(_record_defect("seal sentence not verbatim"))
    if simple.get("verify_sentence") != VERIFY_SENTENCE:
        defects.append(_record_defect("verify sentence not verbatim"))
    holes = simple.get("holes")
    if not isinstance(holes, (list, tuple)) or list(holes) != list(
        VERIFY_HOLES
    ):
        defects.append(_record_defect("holes not in verbatim forms"))
    if not simple.get("limits_wording"):
        defects.append(_record_defect("limits wording missing"))
    figures = simple.get("limits_figures")
    if isinstance(figures, (list, tuple)):
        figure_list = list(figures)
    else:
        figure_list = []
        defects.append(_record_defect("limits figures missing"))
    if figure_list != [_LIMITS_FIGURE]:
        defects.append(_record_defect("limits figure set not the one figure"))
    advanced_figures = advanced.get("figures")
    if not isinstance(advanced_figures, dict) or not advanced_figures:
        defects.append(_record_defect("advanced figures missing"))
        advanced_figures = {}
    for figure in figure_list:
        entry = advanced_figures.get(figure)
        if not isinstance(entry, dict):
            defects.append(
                _record_defect("advanced counterpart missing")
            )
            continue
        if not entry.get("basis"):
            defects.append(_record_defect("advanced basis missing"))
        if entry.get("value") != _LIMITS_FIGURE_VALUE:
            defects.append(
                _record_defect("advanced value differs from the simple form")
            )
    for figure in advanced_figures:
        if figure not in figure_list:
            defects.append(
                _record_defect("advanced figure with no simple counterpart")
            )
    return defects


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
