"""Store and journal module, tracer slice Commit 1 and 2 form.

Founding to signed verify path, with the Commit 2 fixture
surfaces. Founding mints the store identity, writes the genesis
record, appends the golden records through the founding sequence
(canonical encoding, hash linking, manifest replacement, signing,
in that order), and verify runs the existing checks and then the
signature check, returning agreement with the signed verify
sentence only where the signature check has run and passed.

Commit 2 adds the varied constructors the verify discrimination
act exercises: interrupted_store for the manifest lag state and
for the non final tear state, and
fully_checked_store_with_disagreement for the signature
disagreement state. Each constructor founds its store whole
through the founding sequence first and applies its variation
only after that founding stands complete. Verify finds each case
from the standing store state: the complete record beyond an
unchanged manifest head as manifest lag, a torn line that is not
the final line as the chain consistent prefix reading, and a
signature value that does not verify on a fully checked store as
disagreement.

Entry points the tracer scope assigns to later STORE rows stand
in NOT BUILT form behind the module level guard at the foot of
this file, and interrupted_store kinds those rows name stand in
the same form inside interrupted_store itself.
"""

import hmac as _hmac

from ontoloop.canonical import encode_canonical as _encode_canonical
from ontoloop.sealing import hash_sha256 as _hash_sha256
from ontoloop.sealing import manifest_hash as _sealing_manifest_hash
from ontoloop.sealing import sign as _sealing_sign

MODULE_NAME = "ontoloop.store"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

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

SIGNING_KEY_UNAVAILABLE = "signing key unavailable"
SIGNATURE_OBJECT_MISSING = "signature object missing"

PREFIX_READING = "chain consistent prefix"
PREFIX_WORDING = (
    "Chain consistency stands over the intact prefix only. "
    "That reading supports reads only and supports no "
    "judging use and no verify conclusion."
)
MANIFEST_LAG = "manifest lag"
NON_FINAL_TEAR = "non final tear"

FIXTURE_KEY = b"ontoloop-fixture-key-tracer-commit-1"

JOURNAL_SCHEMA_VERSION = 1
CANONICAL_FORM_VERSION = 1
HASH_ALGORITHM_IDENTITY = "SHA-256"
_HASH_ALGORITHM = "SHA-256"

_KIND_JOURNAL = "journal record"
_KIND_SIGNATURE = "head signature"
_KIND_ANCHOR = "head anchor"


def _encode(obj, kind_tag):
    return _encode_canonical(obj, kind_tag)


def _hash_domain(kind_tag, content_obj):
    return _hash_sha256(_encode(content_obj, kind_tag))


def _sign(canonical_bytes, key):
    return _sealing_sign(canonical_bytes, key)


def _manifest_hash(manifest):
    return _sealing_manifest_hash(manifest)


def _record_hash(content, predecessor_hash, sequence, record_type):
    fields = {
        "content": content,
        "predecessor_hash": predecessor_hash,
        "store_sequence": sequence,
        "record_type": record_type,
    }
    return _hash_domain(_KIND_JOURNAL, fields), _encode(fields, _KIND_JOURNAL)


def _build_signature_object(store_id, founding_id, head_hash, manifest_hash):
    obj = {
        "store_identity": store_id,
        "founding_object_identity": founding_id,
        "journal_head_hash": head_hash,
        "manifest_hash": manifest_hash,
    }
    return obj


def _sign_heads(store):
    key = store.get("key_slot")
    if key is None:
        return None
    manifest = store["manifest"]
    head_hash = manifest["head_hash"]
    mhash = _manifest_hash(manifest)
    sig_obj = _build_signature_object(
        store["store_identity"], store["founding_object_identity"],
        head_hash, mhash,
    )
    canonical = _encode(sig_obj, _KIND_SIGNATURE)
    signature = _sign(canonical, key)
    signed = dict(sig_obj)
    signed["signature"] = signature
    signed["canonical_bytes"] = canonical
    store["signature_object"] = signed
    anchor_obj = {
        "store_identity": store["store_identity"],
        "founding_object_identity": store["founding_object_identity"],
        "journal_head_hash": head_hash,
        "manifest_hash": mhash,
        "record_count": manifest["record_count"],
        "head_store_sequence": manifest["head_store_sequence"],
        "signature": signature,
    }
    anchor = dict(anchor_obj)
    anchor["canonical_bytes"] = _encode(anchor_obj, _KIND_ANCHOR)
    store["anchor_staging_copy"] = anchor
    return signed


def _replace_manifest(store):
    records = store["records"]
    last = records[-1]
    store["manifest"] = {
        "founding_object_identity": store["founding_object_identity"],
        "head_hash": last["hash"],
        "record_count": len(records),
        "head_store_sequence": last["store_sequence"],
        "journal_schema_version": JOURNAL_SCHEMA_VERSION,
        "canonical_form_version": CANONICAL_FORM_VERSION,
        "hash_algorithm_identity": HASH_ALGORITHM_IDENTITY,
    }


def _make_journal_record(store, content, record_type):
    records = store["records"]
    sequence = len(records) + 1
    predecessor = records[-1]["hash"] if records else ""
    digest, canonical = _record_hash(content, predecessor, sequence, record_type)
    return {
        "content": content,
        "predecessor_hash": predecessor,
        "store_sequence": sequence,
        "record_type": record_type,
        "hash": digest,
        "canonical_bytes": canonical,
    }


def _append_record(store, content, record_type):
    if store.get("key_slot") is None:
        return {
            "error": SIGNING_KEY_UNAVAILABLE,
            "appended": False,
            "reported_appended": False,
        }
    record = _make_journal_record(store, content, record_type)
    store["records"].append(record)
    _replace_manifest(store)
    _sign_heads(store)
    return {"appended": True, "reported_appended": True, "record": record}


def _append_record_interrupted(store, content, record_type):
    if store.get("key_slot") is None:
        return {
            "error": SIGNING_KEY_UNAVAILABLE,
            "appended": False,
            "reported_appended": False,
        }
    record = _make_journal_record(store, content, record_type)
    store["records"].append(record)
    return {"appended": False, "reported_appended": False, "record": record}


def append_record(store, content, record_type="record"):
    return _append_record(store, content, record_type)


append = append_record


def _found_store(store_identity, founding_id, key_slot):
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
        "journal_schema_version": JOURNAL_SCHEMA_VERSION,
        "canonical_form_version": CANONICAL_FORM_VERSION,
        "hash_algorithm_identity": HASH_ALGORITHM_IDENTITY,
    }
    if key_slot is None:
        sequence = 1
        digest, canonical = _record_hash(genesis_content, "", sequence, "genesis")
        store["records"].append({
            "content": genesis_content,
            "predecessor_hash": "",
            "store_sequence": sequence,
            "record_type": "genesis",
            "hash": digest,
            "canonical_bytes": canonical,
        })
        _replace_manifest(store)
        return store
    _append_record(store, genesis_content, "genesis")
    return store


def golden_record_store():
    store = _found_store(
        "golden-record-store", "golden-record-founding", FIXTURE_KEY
    )
    _append_record(
        store,
        {"record_type": "golden record", "payload": "golden record 1"},
        "golden record",
    )
    return store


def interrupted_store(kind):
    if kind == MANIFEST_LAG:
        store = golden_record_store()
        _append_record_interrupted(
            store,
            {"record_type": "golden record", "payload": "golden record 2"},
            "golden record",
        )
        return store
    if kind == NON_FINAL_TEAR:
        store = golden_record_store()
        _append_record(
            store,
            {"record_type": "golden record", "payload": "golden record 2"},
            "golden record",
        )
        record = store["records"][1]
        canonical = record["canonical_bytes"]
        record["canonical_bytes"] = canonical[: len(canonical) // 2]
        return store
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def fully_checked_store_with_disagreement():
    store = golden_record_store()
    signature_object = store["signature_object"]
    signature = signature_object["signature"]
    first = "0" if signature[0] != "0" else "1"
    signature_object["signature"] = first + signature[1:]
    return store


def verify(store):
    if not isinstance(store, dict):
        return {"output": "unverifiable", "case": "store missing"}
    records = store.get("records") or []
    manifest = store.get("manifest")
    if not records or manifest is None:
        return {"output": "unverifiable", "case": "founding object missing"}
    if records[0].get("record_type") != "genesis":
        return {"output": "unverifiable", "case": "founding object missing"}
    if manifest.get("founding_object_identity") != store.get(
        "founding_object_identity"
    ):
        return {"output": "disagreement", "form": "disagreement form"}
    predecessor = ""
    for index, record in enumerate(records, start=1):
        if record.get("store_sequence") != index:
            return {"output": "disagreement", "form": "disagreement form"}
        if record.get("predecessor_hash") != predecessor:
            return {"output": "disagreement", "form": "disagreement form"}
        canonical_bytes = record.get("canonical_bytes")
        if canonical_bytes is not None and (
            _hash_sha256(canonical_bytes) != record.get("hash")
        ):
            if index < len(records):
                return {
                    "reading": PREFIX_READING,
                    "wording": PREFIX_WORDING,
                    "supports": "reads only",
                    "supports_judging_use": False,
                }
            raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)
        digest, _canon = _record_hash(
            record.get("content"), predecessor, index, record.get("record_type")
        )
        if digest != record.get("hash"):
            return {"output": "disagreement", "form": "disagreement form"}
        predecessor = record["hash"]
    head_hash = records[-1]["hash"]
    if manifest.get("record_count") != len(records):
        count = manifest.get("record_count") or 0
        if (
            0 < count < len(records)
            and manifest.get("head_hash") == records[count - 1]["hash"]
            and manifest.get("head_store_sequence")
            == records[count - 1]["store_sequence"]
        ):
            return {"output": "unverifiable", "case": MANIFEST_LAG}
        return {"output": "disagreement", "form": "disagreement form"}
    if manifest.get("head_hash") != head_hash:
        return {"output": "disagreement", "form": "disagreement form"}
    if manifest.get("head_store_sequence") != records[-1]["store_sequence"]:
        return {"output": "disagreement", "form": "disagreement form"}
    sig_obj = store.get("signature_object")
    if sig_obj is None:
        return {"output": "unverifiable", "case": SIGNATURE_OBJECT_MISSING}
    key = store.get("key_slot")
    if key is None:
        return {"output": "unverifiable", "case": SIGNING_KEY_UNAVAILABLE}
    mhash = _manifest_hash(manifest)
    expected_obj = _build_signature_object(
        store.get("store_identity"),
        store.get("founding_object_identity"),
        head_hash,
        mhash,
    )
    for field in (
        "store_identity",
        "founding_object_identity",
        "journal_head_hash",
        "manifest_hash",
    ):
        if sig_obj.get(field) != expected_obj[field]:
            return {"output": "disagreement", "form": "disagreement form"}
    canonical = _encode(expected_obj, _KIND_SIGNATURE)
    expected_sig = _sign(canonical, key)
    if not _hmac.compare_digest(expected_sig, str(sig_obj.get("signature", ""))):
        return {"output": "disagreement", "form": "disagreement form"}
    return {
        "output": "agreement",
        "sentence": VERIFY_SENTENCE,
        "holes": list(VERIFY_HOLES),
    }


def __getattr__(name):
    if name.startswith("_") or (name.startswith("__") and name.endswith("__")):
        raise AttributeError(name)
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(list(globals().keys()))
