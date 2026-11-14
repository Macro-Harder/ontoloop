"""Core module, slice CORE form.

The typed core of the product: the record position this
module checks, stated as the ten ontology types and the
closed lists beside them; closed schema checking with
reader window refusal in both directions; the named error
catalogue in its CORE rows, with the intake refusal
counting the append path act feeds; the named ungrouped
state for a run whose signature cannot be formed; and the
pure core functions over given inputs, canonical encoding,
hash, verify, and state transition, which delegate to the
canonical form module for the one canonical byte form.

The error catalogue content stands authored as the CORE
slice catalogue act in the design record of this slice:
the error and reason strings the governing texts do not
state, the state change and record home values they do
not supply, the Simple form wordings, the named reader
positions, and the owing presentation values stand
authored and guessed there, never transcribed, and the
two version rows carry their brief literal strings
untouched. The append path act of this module is a
checking act over a record value: it refuses an unlisted
kind by name, counts the refusal, and journals nothing,
and it is not a second journal append surface.

What this slice does not build stands unbuilt behind the
module level guard at the foot of this file: the journal
append itself and every store act, the capture acts in
substance, the declaration refusal surface and the
determinism surface in their suite forms, the catalogue
rows of the later slices and the whole set check, the
governing state table as an implementation unit, and
every reading form artifact. A lookup of a public name
this module does not provide raises AssertionError in the
NOT BUILT form the suite harness uses. A lookup of a
private or dunder name raises AttributeError in the
ordinary form.
"""

MODULE_NAME = "ontoloop.core"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

UNGROUPED_STATE = "ungrouped"

__all__ = [
    "example_a_record",
    "append_record",
    "intake_refusal_counts",
    "refusal_reason",
    "error_catalogue",
    "golden_record",
    "check_record",
    "reader_version",
    "reader_window",
    "UNGROUPED_STATE",
    "run_missing_required_structured_field",
    "form_signature",
    "section_4_4_core_rows",
    "canonical_encoding",
    "hash_record",
    "verify_record",
    "state_transition",
    "example_d_inputs",
    "owing_form_defects",
    "check_owing_forms",
    "catalogue_row_with_value",
    "printed_claims",
]


# Fragment 918, Step 14 slice CORE, owner and data section.
# Catalogue and owing data core only. The module frame (docstring,
# imports, MODULE_NAME, UNGROUPED_STATE, __all__) comes from the
# surface fragment at composition. This section defines no other
# surface name and consumes no sibling section name.

_CORE_ROW_NAMES = (
    "unlisted record type",
    "unknown field",
    "version newer than reader",
    "version below reader window",
)

_CATALOGUE_ORDER = _CORE_ROW_NAMES + (
    "capture refusal at the D-13 caps",
    "outcome precedence refusals naming the closed state",
    "confirmation record incomplete",
    "refusal with no period open",
    "store suspect",
    "access record append failed",
    "exit scan hit",
    "seal claim unqualified",
    "no exit scan result, no exit",
    "purge stopped export refused",
    "refusal of any assembly containing tombstoned material",
    "hash mismatch on load",
    "lock contention refusal",
    "dataset writing interrupted",
    "store founding interrupted",
    "signing key unavailable",
    "signature object missing",
    "sync failure",
    "declared training technique refused",
    "flagged material inside candidate bundle",
)

_ERROR_CATALOGUE = {
    "unlisted record type": {
        "error": (
            "unlisted record type: the submitted record type stands "
            "outside the ontology types and the closed store audit list"
        ),
        "raising_module": "ontoloop.core",
        "state_change": "the refused attempt is not journaled as a record",
        "record_home": "intake refusal counts by reason",
        "simple_form": (
            "The submitted record type stands outside the closed lists, "
            "so the record is not journaled. The attempt is counted in "
            "the intake counts by reason."
        ),
    },
    "unknown field": {
        "error": (
            "unknown field: the submitted record carries a field that "
            "stands outside the closed schema"
        ),
        "raising_module": "ontoloop.core",
        "state_change": "no record is accepted and no stored record changes state",
        "record_home": "the check result returned by check_record",
        "simple_form": (
            "The record carries a field that stands outside the closed "
            "schema, so the record is not accepted. The field is named "
            "in the check result."
        ),
    },
    "version newer than reader": {
        "error": "version newer than reader",
        "raising_module": "ontoloop.core",
        "state_change": "no record is accepted and no stored record changes state",
        "record_home": "the check result returned by check_record",
        "simple_form": (
            "The record schema version stands above the reader version, "
            "so the record is not read by this reader."
        ),
    },
    "version below reader window": {
        "error": "version below reader window",
        "raising_module": "ontoloop.core",
        "state_change": "no record is accepted and no stored record changes state",
        "record_home": "the check result returned by check_record",
        "simple_form": (
            "The record schema version stands below the lower edge of "
            "the reader window, so the record is not read by this reader."
        ),
    },    "capture refusal at the D-13 caps": {
        "error": "capture turned away at the caps: the payload stands over a cap, so the capture does not proceed",
        "raising_module": "ontoloop.capture",
        "state_change": "the capture is refused whole, no part of the payload is captured, and no truncated form is written",
        "record_home": "gate refusal record",
        "simple_form": (
            "The payload stands over a capture cap, so the capture is turned away whole. Nothing is captured and nothing is cut down to fit."
        ),
    },
    "outcome precedence refusals naming the closed state": {
        "error": "outcome precedence: the outcome state already stands closed, so the later outcome is turned away",
        "raising_module": "ontoloop.capture",
        "state_change": "the later outcome is not accepted, and the record keeps the closed outcome state it already carries",
        "record_home": "the outcome record returned at capture",
        "simple_form": (
            "The outcome already stands closed, so the later outcome is turned away. The closed state is named in the result."
        ),
    },
    "confirmation record incomplete": {
        "error": "confirmation record incomplete",
        "raising_module": "ontoloop.promote",
        "state_change": "the confirmation is not recorded as complete, and the promotion it would confirm stands unconfirmed",
        "record_home": "the Promotion Record",
        "simple_form": (
            "The confirmation record lacks a part it needs, so the confirmation does not complete. The promotion stands unconfirmed."
        ),
    },
    "refusal with no period open": {
        "error": "no period open: the act needs an open period and none stands open, so the act is turned away",
        "raising_module": "ontoloop.promote",
        "state_change": "no promotion act proceeds, and no period is opened or changed by the refused act",
        "record_home": "the Promotion Record",
        "simple_form": (
            "No period stands open for this act, so the act is turned away. Open a period first, then present the act again."
        ),
    },
    "store suspect": {
        "error": "store suspect",
        "raising_module": "ontoloop.store",
        "state_change": "the store stands suspect, ordinary capture appends are barred while that state stands, and no stored record changes",
        "record_home": "the store suspect record",
        "simple_form": (
            "The store stands suspect, so ordinary capture appends are barred while that state stands. Stored records are unchanged."
        ),
    },
    "access record append failed": {
        "error": "access record append failed",
        "raising_module": "ontoloop.store",
        "state_change": "no access record is appended, no content is shown, and no group is spent",
        "record_home": "the append result returned by the access record append act",
        "simple_form": (
            "The access record append did not complete, so no access record stands added. No content is shown and no group is spent."
        ),
    },
    "exit scan hit": {
        "error": "exit scan hit",
        "raising_module": "ontoloop.redact",
        "state_change": "the assembly is not released, no exit proceeds on it, and no record changes state",
        "record_home": "the exit scan record",
        "simple_form": (
            "The exit scan found material that bars the exit, so the assembly is not released. The hit stands named in the scan record."
        ),
    },
    "seal claim unqualified": {
        "error": "seal claim unqualified",
        "raising_module": "ontoloop.redact",
        "state_change": "the claim is not printed in unqualified form, and no assembly carrying it in that form is released",
        "record_home": "the report record carrying the seal claim",
        "simple_form": (
            "The seal claim lacks the qualification it needs, so the claim does not stand as made. The claim must be qualified before it travels."
        ),
    },
    "no exit scan result, no exit": {
        "error": "no exit scan result, no exit",
        "raising_module": "ontoloop.redact",
        "state_change": "no exit scan result stands, no exit proceeds, and no record changes state",
        "record_home": "the exit attempt record",
        "simple_form": (
            "The exit scan could not run, so no exit scan result stands and no exit proceeds. The exit stays barred until a scan runs."
        ),
    },
    "purge stopped export refused": {
        "error": "purge stopped export refused",
        "raising_module": "ontoloop.ops",
        "state_change": "the export is not made, the purge stands stopped, and no material is removed by that export",
        "record_home": "the purge record",
        "simple_form": (
            "The purge stands stopped, so the export is turned away. No material leaves in that export."
        ),
    },
    "refusal of any assembly containing tombstoned material": {
        "error": "assembly containing tombstoned material: the assembly carries material under a tombstone, so the assembly is turned away",
        "raising_module": "ontoloop.ops",
        "state_change": "the assembly is not released or used, and the tombstoned material stands untouched in place",
        "record_home": "the export assembly record",
        "simple_form": (
            "The assembly carries material under a tombstone, so the assembly is turned away whole. The tombstoned material stays in place."
        ),
    },
    "hash mismatch on load": {
        "error": "hash mismatch on load",
        "raising_module": "ontoloop.consumption",
        "state_change": "the bundle is not loaded, it stands in the unloadable position, and no loaded state changes",
        "record_home": "the load refusal record, naming which side was checked against which and the hash each side carried",
        "simple_form": (
            "The bundle hash does not match the hash it was checked against, so the bundle is not loaded. Both hashes stand named in the load record."
        ),
    },
    "lock contention refusal": {
        "error": "lock contention: the append lock stayed held through the wait, so the append is turned away",
        "raising_module": "ontoloop.store",
        "state_change": "the append is not made after the wait, and no record is appended or changed by the refused act",
        "record_home": "lock refusal record in the Promotion Record form",
        "simple_form": (
            "The append lock stayed held through the whole wait, so the append is turned away. Try again when the lock stands free."
        ),
    },
    "dataset writing interrupted": {
        "error": "dataset writing interrupted",
        "raising_module": "ontoloop.dataset",
        "state_change": "no dataset and no Dataset record stand for the failed attempt",
        "record_home": "the intake account entry for the failed attempt",
        "simple_form": (
            "The dataset write was interrupted, so no dataset and no dataset record stand for that attempt. The abort stands in the intake account."
        ),
    },
    "store founding interrupted": {
        "error": "store founding interrupted",
        "raising_module": "ontoloop.store",
        "state_change": "no store and no genesis record stand for the interrupted founding",
        "record_home": "the founding record read from the home as no store, in the section 8.4 table form",
        "simple_form": (
            "The store founding was interrupted, so no store and no genesis record stand for that founding. Found the store again from the start."
        ),
    },
    "signing key unavailable": {
        "error": "signing key unavailable",
        "raising_module": "ontoloop.store",
        "state_change": "the append is refused where the key is needed, no record is appended, and the store stands unchanged",
        "record_home": "the store record for the refused append",
        "simple_form": (
            "No signing key stands available, so the append is turned away. The store stands unchanged."
        ),
    },
    "signature object missing": {
        "error": "signature object missing",
        "raising_module": "ontoloop.store",
        "state_change": "the store stands reported as unverifiable for that case, and no stored record changes state",
        "record_home": "the verify record for the store",
        "simple_form": (
            "The signature object is missing, so the store cannot be verified on that check. The store stands reported as unverifiable for that case."
        ),
    },
    "sync failure": {
        "error": "sync failure",
        "raising_module": "ontoloop.store",
        "state_change": "the store moves to suspect at once, barring ordinary appends while it stands, and no later sync success clears that state",
        "record_home": "suspect record",
        "simple_form": (
            "A sync step failed, so the store moves to suspect at once. Ordinary appends are barred while that state stands."
        ),
    },
    "declared training technique refused": {
        "error": "declared training technique refused",
        "raising_module": "ontoloop.core",
        "state_change": "the refusal stands with no state change to the declared record, and no record changes except the refusal record the journal entry states",
        "record_home": "journal refusal record",
        "simple_form": (
            "The declared technique stands outside the allowed list, so the declaration is turned away. The declared record stands unchanged."
        ),
    },
    "flagged material inside candidate bundle": {
        "error": "flagged material inside candidate bundle",
        "raising_module": "ontoloop.cross_split_audit",
        "state_change": "the candidate bundle is refused, no promotion proceeds on it, and the evaluation stands recorded as not scored with its typed reason",
        "record_home": "the evaluation record for the refusal and, at the promotion call point, the Promotion Record",
        "simple_form": (
            "Flagged material stands inside the candidate bundle, so the bundle is turned away and no promotion proceeds on it. The evaluation stands recorded as not scored, with its typed reason."
        ),
    },
}

_OWING_PRESENTATION = {
    "unlisted record type": {
        "name": "unlisted record type",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The submitted record type stands outside the closed lists, "
                "so the record is not journaled. The attempt is counted in "
                "the intake counts by reason."
            ),
            "figure": 1,
            "bound": "the ontology types and the closed store audit list",
            "refusal_reason": "record type not listed",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the admissible types are the ontology types "
                "and the closed store audit list at brief Section 5.2. A "
                "type outside both lists is turned away at the append path, "
                "the attempt is not journaled as a record, and the count "
                "under the reason record type not listed rises by exactly "
                "one for each such attempt."
            ),
            "figure": 1,
            "bound": "the ontology types and the closed store audit list",
            "refusal_reason": "record type not listed",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not resubmit the record under the same "
                "type. Submit the work under one of the ontology types or "
                "a closed store audit kind, or stop and report the type "
                "gap. The turned away attempt is counted under the reason "
                "record type not listed and is not journaled."
            ),
            "figure": 1,
            "bound": "the ontology types and the closed store audit list",
            "refusal_reason": "record type not listed",
        },
    },
    "unknown field": {
        "name": "unknown field",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The record carries a field that stands outside the closed "
                "schema, so the record is not accepted. The field is named "
                "in the check result."
            ),
            "figure": "none stated",
            "bound": "the dictionary field set",
            "refusal_reason": "field not in the dictionary field set",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: schemas are closed and no extension object "
                "exists. A field that stands in the record and not in the "
                "dictionary field set is turned away at ingest, the field "
                "is named in the check result, and no record is accepted "
                "on that act."
            ),
            "figure": "none stated",
            "bound": "the dictionary field set",
            "refusal_reason": "field not in the dictionary field set",
        },
        "agentic_form": {
            "wording": (
                "Agent action: remove the field that stands outside the "
                "closed schema, or stop and report the field gap. Do not "
                "resubmit the record carrying the extra field. The field "
                "is named in the check result."
            ),
            "figure": "none stated",
            "bound": "the dictionary field set",
            "refusal_reason": "field not in the dictionary field set",
        },
    },
    "version newer than reader": {
        "name": "version newer than reader",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "The record schema version stands above the reader version, "
                "so the record is not read by this reader."
            ),
            "figure": "none stated",
            "bound": "reader version",
            "refusal_reason": "schema version above the reader version",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: readers refuse versions newer than they "
                "know. The bound is the reader version itself: a schema "
                "version above it is turned away, and a version inside the "
                "reader window is read or migrated under brief Section 6, "
                "never silently reinterpreted."
            ),
            "figure": "none stated",
            "bound": "reader version",
            "refusal_reason": "schema version above the reader version",
        },
        "agentic_form": None,
    },
    "version below reader window": {
        "name": "version below reader window",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "The record schema version stands below the lower edge of "
                "the reader window, so the record is not read by this reader."
            ),
            "figure": "none stated",
            "bound": "reader window lower edge",
            "refusal_reason": "schema version below the reader window lower edge",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: readers refuse versions below the reader "
                "window. The bound is the lower edge of the reader window: "
                "a schema version below that edge is turned away, and a "
                "version inside the window is read or migrated under brief "
                "Section 6, never silently reinterpreted."
            ),
            "figure": "none stated",
            "bound": "reader window lower edge",
            "refusal_reason": "schema version below the reader window lower edge",
        },
        "agentic_form": None,
    },
    "capture refusal at the D-13 caps": {
        "name": "capture refusal at the D-13 caps",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The payload stands over a capture cap, so the capture is turned away whole. Nothing is captured and nothing is cut down to fit."
            ),
            "figure": "none stated",
            "bound": "the D-13 capture caps",
            "refusal_reason": "payload over a capture cap",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: capture refuses at the D-13 caps, with no truncation at capture, under plan section 4.4 and row CAPTURE-T05. A payload at a cap is accepted whole and a payload over a cap is refused whole, so no shortened form of the material ever stands as the captured form."
            ),
            "figure": "none stated",
            "bound": "the D-13 capture caps",
            "refusal_reason": "payload over a capture cap",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not resubmit the payload in a cut down form. Present the material within the caps, or stop and report the cap gap. The refused capture writes nothing."
            ),
            "figure": "none stated",
            "bound": "the D-13 capture caps",
            "refusal_reason": "payload over a capture cap",
        },
    },
    "outcome precedence refusals naming the closed state": {
        "name": "outcome precedence refusals naming the closed state",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The outcome already stands closed, so the later outcome is turned away. The closed state is named in the result."
            ),
            "figure": "none stated",
            "bound": "the closed outcome state",
            "refusal_reason": "outcome state already closed",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the pending outcome state closes by its two routes only, under plan section 4.4 and row CAPTURE-T04. A late outcome and a second outcome are each refused naming the closed state, so the first closing stands and no later outcome rewrites it."
            ),
            "figure": "none stated",
            "bound": "the closed outcome state",
            "refusal_reason": "outcome state already closed",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not present another outcome for a record whose outcome stands closed. Report the closed state and stop."
            ),
            "figure": "none stated",
            "bound": "the closed outcome state",
            "refusal_reason": "outcome state already closed",
        },
    },
    "confirmation record incomplete": {
        "name": "confirmation record incomplete",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The confirmation record lacks a part it needs, so the confirmation does not complete. The promotion stands unconfirmed."
            ),
            "figure": "none stated",
            "bound": "the confirmation record parts the Promotion Record requires",
            "refusal_reason": "confirmation record missing a required part",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: a confirmation record that lacks a part it needs cannot complete the confirmation, under plan section 4.4 and row PROMOTE-T05. The promotion it would confirm stands unconfirmed until a complete confirmation record stands."
            ),
            "figure": "none stated",
            "bound": "the confirmation record parts the Promotion Record requires",
            "refusal_reason": "confirmation record missing a required part",
        },
        "agentic_form": {
            "wording": (
                "Agent action: complete the confirmation record with every part it needs, or stop and report the missing part. Do not treat the promotion as confirmed."
            ),
            "figure": "none stated",
            "bound": "the confirmation record parts the Promotion Record requires",
            "refusal_reason": "confirmation record missing a required part",
        },
    },
    "refusal with no period open": {
        "name": "refusal with no period open",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "No period stands open for this act, so the act is turned away. Open a period first, then present the act again."
            ),
            "figure": "none stated",
            "bound": "an open promotion period",
            "refusal_reason": "no period open",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the act is governed by the period it stands in, under plan section 4.4 and brief Section 5.6. Where no period stands open the act is refused with this named error, and the refused act opens nothing and changes nothing."
            ),
            "figure": "none stated",
            "bound": "an open promotion period",
            "refusal_reason": "no period open",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not present the act while no period stands open. Wait for an open period, or stop and report that none stands open."
            ),
            "figure": "none stated",
            "bound": "an open promotion period",
            "refusal_reason": "no period open",
        },
    },
    "store suspect": {
        "name": "store suspect",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "The store stands suspect, so ordinary capture appends are barred while that state stands. Stored records are unchanged."
            ),
            "figure": "none stated",
            "bound": "the suspect state barring ordinary capture appends",
            "refusal_reason": "store in the suspect state",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the store suspect state bars ordinary capture appends while it stands, under plan section 4.4, row STORE-T06, and row CAPTURE-T07. The state follows a sync failure or another governed suspect act, and no later success clears it by itself."
            ),
            "figure": "none stated",
            "bound": "the suspect state barring ordinary capture appends",
            "refusal_reason": "store in the suspect state",
        },
        "agentic_form": None,
    },
    "access record append failed": {
        "name": "access record append failed",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "The access record append did not complete, so no access record stands added. No content is shown and no group is spent."
            ),
            "figure": "none stated",
            "bound": "the access record append act",
            "refusal_reason": "access record append did not complete",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: an access record append that fails shows no content and spends no group, under plan section 4.4 and brief Section 7.3. The failure is returned to the caller in the append result, and nothing stands appended on that act."
            ),
            "figure": "none stated",
            "bound": "the access record append act",
            "refusal_reason": "access record append did not complete",
        },
        "agentic_form": None,
    },
    "exit scan hit": {
        "name": "exit scan hit",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The exit scan found material that bars the exit, so the assembly is not released. The hit stands named in the scan record."
            ),
            "figure": "none stated",
            "bound": "the exit scan hit classes",
            "refusal_reason": "exit scan hit",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the layer 6 exit scan scans assembly content, under plan section 4.4 and row REDACT-T06. An assembly whose content carries a hit is refused the exit, and the hit stands named in the exit scan record."
            ),
            "figure": "none stated",
            "bound": "the exit scan hit classes",
            "refusal_reason": "exit scan hit",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not release the assembly. Remove or redact the hit material, then present the assembly for a fresh scan."
            ),
            "figure": "none stated",
            "bound": "the exit scan hit classes",
            "refusal_reason": "exit scan hit",
        },
    },
    "seal claim unqualified": {
        "name": "seal claim unqualified",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The seal claim lacks the qualification it needs, so the claim does not stand as made. The claim must be qualified before it travels."
            ),
            "figure": "none stated",
            "bound": "the seal claim qualification the claim list requires",
            "refusal_reason": "seal claim stated without its qualification",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: a seal claim travels only in its qualified form, under plan section 4.4 and the seal claim list at brief Section 7.4. A claim stated without its qualification is refused, and the verbatim claim texts travel verbatim or not at all."
            ),
            "figure": "none stated",
            "bound": "the seal claim qualification the claim list requires",
            "refusal_reason": "seal claim stated without its qualification",
        },
        "agentic_form": {
            "wording": (
                "Agent action: state the seal claim in its qualified verbatim form, or do not print the claim. Do not paraphrase the claim text."
            ),
            "figure": "none stated",
            "bound": "the seal claim qualification the claim list requires",
            "refusal_reason": "seal claim stated without its qualification",
        },
    },
    "no exit scan result, no exit": {
        "name": "no exit scan result, no exit",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The exit scan could not run, so no exit scan result stands and no exit proceeds. The exit stays barred until a scan runs."
            ),
            "figure": "none stated",
            "bound": "a completed exit scan",
            "refusal_reason": "exit scan could not run",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: where a scan cannot run, the exit is refused in the form no exit scan result, no exit, under plan section 4.4 and row REDACT-T06. A scan that did not examine the assembly returns no clear result, and no exit proceeds on it."
            ),
            "figure": "none stated",
            "bound": "a completed exit scan",
            "refusal_reason": "exit scan could not run",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not treat the assembly as scanned and do not release it. Report that the scan could not run and stop."
            ),
            "figure": "none stated",
            "bound": "a completed exit scan",
            "refusal_reason": "exit scan could not run",
        },
    },
    "purge stopped export refused": {
        "name": "purge stopped export refused",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "The purge stands stopped, so the export is turned away. No material leaves in that export."
            ),
            "figure": "none stated",
            "bound": "the purge stop state",
            "refusal_reason": "purge stopped",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: where the purge stands stopped, an export from the stopped purge is refused, under plan section 4.4 and row OPS-T03. The stop stands until its governed lifting act, and no export proceeds around it."
            ),
            "figure": "none stated",
            "bound": "the purge stop state",
            "refusal_reason": "purge stopped",
        },
        "agentic_form": None,
    },
    "refusal of any assembly containing tombstoned material": {
        "name": "refusal of any assembly containing tombstoned material",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The assembly carries material under a tombstone, so the assembly is turned away whole. The tombstoned material stays in place."
            ),
            "figure": "none stated",
            "bound": "the tombstone set for the assembly",
            "refusal_reason": "assembly contains tombstoned material",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: any assembly containing tombstoned material is refused, under plan section 4.4 and row OPS-T03. The refusal covers the whole assembly, and the tombstoned material is neither included nor removed by the refused act."
            ),
            "figure": "none stated",
            "bound": "the tombstone set for the assembly",
            "refusal_reason": "assembly contains tombstoned material",
        },
        "agentic_form": {
            "wording": (
                "Agent action: rebuild the assembly without the tombstoned material, or stop and report the tombstone. Do not present the same assembly again."
            ),
            "figure": "none stated",
            "bound": "the tombstone set for the assembly",
            "refusal_reason": "assembly contains tombstoned material",
        },
    },
    "hash mismatch on load": {
        "name": "hash mismatch on load",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The bundle hash does not match the hash it was checked against, so the bundle is not loaded. Both hashes stand named in the load record."
            ),
            "figure": "none stated",
            "bound": "the bundle content hash checked against the presented hash",
            "refusal_reason": "hash mismatch on load",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: a presented bundle is hash checked over its whole content before a load, under plan section 4.4 at item S5-O-73 and row CONSUME-T03. Where the hashes differ the bundle stands unloadable, and the load refusal record names which side was checked against which and the hash each side carried."
            ),
            "figure": "none stated",
            "bound": "the bundle content hash checked against the presented hash",
            "refusal_reason": "hash mismatch on load",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not load the bundle. Report both hashes from the load refusal record and stop."
            ),
            "figure": "none stated",
            "bound": "the bundle content hash checked against the presented hash",
            "refusal_reason": "hash mismatch on load",
        },
    },
    "lock contention refusal": {
        "name": "lock contention refusal",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "The append lock stayed held through the whole wait, so the append is turned away. Try again when the lock stands free."
            ),
            "figure": "none stated",
            "bound": "the D-19 writer wait",
            "refusal_reason": "lock held through the wait",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the append lock is an inter process lock carrying the D-19 writer wait, under plan section 4.4, plan subsection 18.6 clause four, and row STORE-T04. A writer that waits the full wait against a held lock is refused, and its append is not made."
            ),
            "figure": "none stated",
            "bound": "the D-19 writer wait",
            "refusal_reason": "lock held through the wait",
        },
        "agentic_form": None,
    },
    "dataset writing interrupted": {
        "name": "dataset writing interrupted",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The dataset write was interrupted, so no dataset and no dataset record stand for that attempt. The abort stands in the intake account."
            ),
            "figure": "none stated",
            "bound": "a completed dataset write",
            "refusal_reason": "dataset writing interrupted",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the Dataset is written sealed whole or not written at all, under plan subsection 19.112 point two and row DATASET-T07. An interruption inside the write leaves no dataset and no Dataset record for the failed attempt, and the intake account for the failed attempt records the abort."
            ),
            "figure": "none stated",
            "bound": "a completed dataset write",
            "refusal_reason": "dataset writing interrupted",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not treat any part of the interrupted write as a dataset. Rebuild the dataset whole, or stop and report the interruption."
            ),
            "figure": "none stated",
            "bound": "a completed dataset write",
            "refusal_reason": "dataset writing interrupted",
        },
    },
    "store founding interrupted": {
        "name": "store founding interrupted",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "The store founding was interrupted, so no store and no genesis record stand for that founding. Found the store again from the start."
            ),
            "figure": "none stated",
            "bound": "a completed store founding",
            "refusal_reason": "store founding interrupted",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: an interruption inside founding leaves no store and no genesis record, under plan subsection 19.112 point three and row STORE-T09. There is no store to verify for the interrupted founding, and the outcome is read from the home as no store."
            ),
            "figure": "none stated",
            "bound": "a completed store founding",
            "refusal_reason": "store founding interrupted",
        },
        "agentic_form": None,
    },
    "signing key unavailable": {
        "name": "signing key unavailable",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "No signing key stands available, so the append is turned away. The store stands unchanged."
            ),
            "figure": "none stated",
            "bound": "an obtained signing key",
            "refusal_reason": "signing key unavailable",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: where no signing key stands obtained, the append is refused with this named error and the same name stands as a verify case, under plan subsection 20.87 points four and six and the STORE scope catalogue passage. No record is appended unsigned on that act."
            ),
            "figure": "none stated",
            "bound": "an obtained signing key",
            "refusal_reason": "signing key unavailable",
        },
        "agentic_form": None,
    },
    "signature object missing": {
        "name": "signature object missing",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "The signature object is missing, so the store cannot be verified on that check. The store stands reported as unverifiable for that case."
            ),
            "figure": "none stated",
            "bound": "the signature object for the store",
            "refusal_reason": "signature object missing",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: verify carries the case signature object missing where the object the verify act needs does not stand, under plan subsection 20.87 point six and the STORE scope catalogue passage. The outcome is unverifiable naming its case, never a pass and never a silent repair."
            ),
            "figure": "none stated",
            "bound": "the signature object for the store",
            "refusal_reason": "signature object missing",
        },
        "agentic_form": None,
    },
    "sync failure": {
        "name": "sync failure",
        "named_reader": "operator",
        "simple_form": {
            "wording": (
                "A sync step failed, so the store moves to suspect at once. Ordinary appends are barred while that state stands."
            ),
            "figure": "none stated",
            "bound": "file sync and directory sync completing without error",
            "refusal_reason": "sync failure",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: section 4.4 gains one row for sync failure, covering file sync and directory sync, under plan subsection 18.6 clause three. Any file sync or directory sync error in an append, a founding, or a manifest replacement takes the store to suspect at once, and no later sync success, on the same descriptor or on a reopened file, clears the suspect state or certifies earlier writes."
            ),
            "figure": "none stated",
            "bound": "file sync and directory sync completing without error",
            "refusal_reason": "sync failure",
        },
        "agentic_form": None,
    },
    "declared training technique refused": {
        "name": "declared training technique refused",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "The declared technique stands outside the allowed list, so the declaration is turned away. The declared record stands unchanged."
            ),
            "figure": "none stated",
            "bound": "the closed list of allowed technique declarations",
            "refusal_reason": "declared technique outside the allowed list",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the allowed technique declaration list is closed and no training technique name stands on it, under plan subsection 19.33. Any declaration outside the list is refused in this named error, including a training technique under any other name and any case or spacing variant of a listed name, matched after case folding and whitespace collapse. The shipped refused set is the exact strings sft, dpo, and grpo."
            ),
            "figure": "none stated",
            "bound": "the closed list of allowed technique declarations",
            "refusal_reason": "declared technique outside the allowed list",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not declare a training technique for the first version, under any name or variant. Declare only a technique on the allowed list, or stop and report the declaration gap."
            ),
            "figure": "none stated",
            "bound": "the closed list of allowed technique declarations",
            "refusal_reason": "declared technique outside the allowed list",
        },
    },
    "flagged material inside candidate bundle": {
        "name": "flagged material inside candidate bundle",
        "named_reader": "agent",
        "simple_form": {
            "wording": (
                "Flagged material stands inside the candidate bundle, so the bundle is turned away and no promotion proceeds on it. The evaluation stands recorded as not scored, with its typed reason."
            ),
            "figure": "none stated",
            "bound": "flagged material standing outside the candidate bundle",
            "refusal_reason": "flagged material inside candidate bundle",
        },
        "advanced_form": {
            "wording": (
                "Basis in full: the cross split audit refusal where flagged material sits inside the candidate bundle carries this literal name at every call point, under plan subsection 19.36 point two. Its raising module is the cross split audit module at the evaluation and promotion call points. The attempt stands charged as one completed evaluation where any case was scored before the refusal, and as no completed evaluation where no case was scored."
            ),
            "figure": "none stated",
            "bound": "flagged material standing outside the candidate bundle",
            "refusal_reason": "flagged material inside candidate bundle",
        },
        "agentic_form": {
            "wording": (
                "Agent action: do not promote or score the bundle. Report the flagged material finding from the evaluation record and stop."
            ),
            "figure": "none stated",
            "bound": "flagged material standing outside the candidate bundle",
            "refusal_reason": "flagged material inside candidate bundle",
        },
    },
}

_OWING_ROWS = _OWING_PRESENTATION

_OWING_ROW_STATEMENT = (
    "error catalogue owing row (plan section 13.3, further rows; "
    "test row CORE-T06)"
)

_PRINTED_CLAIMS = (
    {
        "printed_home": "artifact",
        "wording_class": "error wording",
        "printed_wording": (
            "unlisted record type: the submitted record type stands "
            "outside the ontology types and the closed store audit list"
        ),
        "catalogue_row": "unlisted record type",
        "owing_row": _OWING_ROW_STATEMENT,
        "governing_row": _OWING_ROW_STATEMENT,
        "substitute_for_owing_row": False,
    },
    {
        "printed_home": "artifact",
        "wording_class": "error wording",
        "printed_wording": (
            "unknown field: the submitted record carries a field that "
            "stands outside the closed schema"
        ),
        "catalogue_row": "unknown field",
        "owing_row": _OWING_ROW_STATEMENT,
        "governing_row": _OWING_ROW_STATEMENT,
        "substitute_for_owing_row": False,
    },
    {
        "printed_home": "loop report",
        "wording_class": "error wording",
        "printed_wording": "version newer than reader",
        "catalogue_row": "version newer than reader",
        "owing_row": _OWING_ROW_STATEMENT,
        "governing_row": _OWING_ROW_STATEMENT,
        "substitute_for_owing_row": False,
    },
    {
        "printed_home": "loop report",
        "wording_class": "error wording",
        "printed_wording": "version below reader window",
        "catalogue_row": "version below reader window",
        "owing_row": _OWING_ROW_STATEMENT,
        "governing_row": _OWING_ROW_STATEMENT,
        "substitute_for_owing_row": False,
    },
)


def _fresh_owing_row(row):
    copied = {}
    for key, value in row.items():
        if isinstance(value, dict):
            copied[key] = dict(value)
        else:
            copied[key] = value
    return copied


def error_catalogue():
    return {
        name: dict(_ERROR_CATALOGUE[name]) for name in _CATALOGUE_ORDER
    }


def section_4_4_core_rows():
    return list(_CORE_ROW_NAMES)


def catalogue_row_with_value(kind, form):
    for name in _CATALOGUE_ORDER:
        row = _OWING_PRESENTATION[name]
        form_value = row.get(form)
        if isinstance(form_value, dict) and kind in form_value:
            return _fresh_owing_row(row)
    return None


def printed_claims():
    return [dict(claim) for claim in _PRINTED_CLAIMS]


# Fragment 930, Step 14 slice CORE, supplementary build seat.
# Names defined in this section, and no others:
# refusal_reason, reader_version, reader_window,
# example_a_record, example_d_inputs, golden_record, and
# run_missing_required_structured_field, beside private
# helpers marked with a leading underscore.
# Insertion point for the whole section: in
# system/ontoloop/core.py, inside the roster 918 data and
# fixture section position in the composition order the
# CORE scope states at its section 10, after fragment-918
# data and before the roster 919 refusal and checking
# section. This section defines no name another section
# owns and copies no stored data from another section.
# Consumption contracts, stated for the assembly check:
# refusal_reason reads the stored owing presentation
# through the module globals at call time, under the name
# fragment-918 defines for that store,
# _OWING_PRESENTATION. The composed module must carry
# that store under that name, and the second name roster
# 919 reads for the same store must stand bound to that
# same single store object, never to a copy, so exactly
# one owing store stands in the composed module.
# reader_version and reader_window read the landed
# dictionary artifact through ontoloop.dictionary at call
# time, in the form fragment-919 check_record consumes:
# reader_version returns the reader version as an integer
# value, and reader_window returns a two element tuple
# whose first element is the window lower edge and whose
# second element is the reader version. The fixture acts
# read the reader position through the module globals at
# call time, so a fixture record schema version always
# stands inside the presented window.
# Strict reading position: every act in this section
# reads a stored row or an artifact value by its one
# stated key name only, and tries no alias name for any
# fact.


# The first shipped schema version, in the brief window
# lower edge position: the first version reader window
# opens at the first shipped schema version. That value
# stands as a build act value in this section, recorded
# as such in this section paper, and no source states a
# reader version value or a window bound value beyond
# that position and the artifact width content the
# reader position below consumes.
_FIRST_SCHEMA_VERSION = 1


def _reader_position():
    from ontoloop.dictionary import dictionary_source

    window_content = dictionary_source()["reader_window"]
    width = window_content["width_versions"]
    lower = _FIRST_SCHEMA_VERSION
    upper = lower + width - 1
    return (lower, upper)


def reader_version():
    """Return the reader version value.

    The value is the upper edge of the reader window the
    module presents: the window lower edge, standing at
    the first shipped schema version, moved upward by
    the dictionary artifact reader window width content,
    read from the artifact at call time, so the span of
    the presented window, counted in versions, stands as
    that width content states by construction. No width
    value stands stated or hardcoded in this section:
    the width reaches this act only as artifact content.
    """
    return _reader_position()[1]


def reader_window():
    """Return the reader window presentation.

    The presentation is a two element tuple, lower edge
    first and reader version second, in the form the
    scope proposes for this surface and the form roster
    919 check_record consumes through the module globals:
    the below window limb reads element zero as the
    lower edge, and the reader version stands as the
    second element, equal to reader_version() on every
    call, both values derived from the artifact width
    content at call time as reader_version states.
    """
    return _reader_position()


def refusal_reason(name):
    """Return the refusal reason string for a catalogue row.

    The argument is a catalogue row name, as the tests
    call this act with the unlisted record type row name.
    The return is the reason string under which that
    refusal is counted, in the authored catalogue act
    form: for the unlisted record type row, the reason
    the shape act states at its appended section A for
    this name. The string stands read at call time from
    the stored owing presentation the module carries,
    through the module globals, at the row the name keys
    and at the refusal_reason value of its Simple form
    mapping, whose kind values stand identical in every
    owed form of the row. No reason string stands copied
    into this section, and no reason string stands read
    from the five key catalogue presentation, which
    carries no such value. A name standing in no stored
    row returns None: no test drives that input, and
    that value stands as this section authored
    completion, in the form fragment-918 states for its
    row lookup act on inputs outside its closed lists.
    """
    rows = globals()["_OWING_PRESENTATION"]
    row = rows.get(name)
    if row is None:
        return None
    return row["simple_form"]["refusal_reason"]


def _example_payload():
    return {
        "task_verbatim": "review the captured trace",
        "steps": [
            {
                "step_identity": "example-a-step-one",
                "predecessor_reference": None,
            },
            {
                "step_identity": "example-a-step-two",
                "predecessor_reference": "example-a-step-one",
            },
        ],
        "outcome_record": {"outcome_state": "attached"},
        "signal_records": [
            {
                "signal_identity": "example-a-signal-one",
                "signal_kind": "review note",
            },
        ],
    }


def _envelope_record(record_identity, schema_version):
    return {
        "record_identity": record_identity,
        "record_type": "Run",
        "schema_version": schema_version,
        "workflow_identity": "review-workflow",
        "workflow_definition_version": 1,
        "payload": _example_payload(),
    }


def example_a_record():
    """Return a fresh Example A record mapping.

    The record stands in the Example A form the shape
    act states: an envelope formed record of the Run
    type, a captured review run, carrying its record
    type under the test pinned key record_type and its
    schema version under the test pinned key
    schema_version, at the reader version, inside the
    reader window. Its per type parts travel inside
    payload, in the roster 919 envelope position: the
    task verbatim in its review workflow form, its steps
    in order, the first step carrying a predecessor
    value of none and the later step carrying a
    predecessor reference naming the immediately
    preceding step, its outcome record kept apart in the
    attached outcome state, and its signal records kept
    apart. Every key at the top level stands in the
    roster 919 envelope key set, stated key by key in
    this section paper. A fresh mapping, with fresh
    nested mappings, stands returned on every call, so
    a caller variation reaches no later record.
    """
    return _envelope_record("example-a-run-1", reader_version())


def golden_record():
    """Return a fresh golden shaped record mapping.

    The record stands in the same envelope form as
    example_a_record, with its own record identity, and
    carries its schema version under the test pinned key
    schema_version at the lower edge of the reader
    window, inside the window the module presents, as
    the base the closed schema tests vary: the tests
    assign its schema_version and add an unknown field,
    and no unvaried key of it stands outside the allowed
    field set roster 919 check_record enforces. The
    relation of this record to the Example A record
    stands unpinned in every source: this section forms
    both in the one envelope form, as a build form the
    tests do not evidence beyond the pinned keys, stated
    in this section paper in the open. A fresh mapping,
    with fresh nested mappings, stands returned on every
    call.
    """
    return _envelope_record("golden-record-1", reader_window()[0])


def example_d_inputs():
    """Return the Example D state transition case mapping.

    The mapping carries exactly the three keys the tests
    read, state, act, and expected_state, holding the
    triple the shape act states at its appended
    section E, cited to the governing state table
    transition there: the provisional first period state,
    on the confirmation act, moves to the confirmed
    state. That triple stands consistent with the
    transition table roster 920 pure computation section
    carries for state_transition, key for key, so the
    pure function over this case returns the expected
    state value this mapping carries. A fresh mapping
    stands returned on every call.
    """
    return {
        "state": "Provisional, first period",
        "act": "confirmation",
        "expected_state": "Confirmed",
    }


def run_missing_required_structured_field():
    """Return a run missing a required structured field.

    The run stands in the first named missing form of
    the brief review workflow passage the shape act
    states: a review arriving with no recorded target
    identity, so no signature can be formed over it. The
    run carries the other two required structured fields
    under the authored key forms roster 919 form_signature
    reads, task_kind and template_version, and carries no
    target_identity key at all, that key standing as the
    missing field, named here and in this section paper.
    A fresh mapping stands returned on every call.
    """
    return {"task_kind": "review", "template_version": 1}


# Section: failure, refusal, and checking, roster 919.
# Names defined in this section, and no others:
# append_record, intake_refusal_counts, check_record,
# form_signature, check_owing_forms, owing_form_defects,
# beside private helpers and the counting state, each
# marked with a leading underscore and standing outside
# the presented surface.
# Insertion point for the whole section: in
# system/ontoloop/core.py, after roster 918 data and
# fixture section and before roster 920 pure computation
# section, in the composition order the CORE scope states
# at its section 10.
# Cross section calls, stated for the assembly check:
# every name owned by another section is read through
# the module globals at call time, never imported as a
# core name and never copied into this section. The names
# so read are: error_catalogue (roster 918 data section),
# refusal_reason (roster 918 data section), reader_version
# and reader_window (roster 918 reader position),
# UNGROUPED_STATE (module constant, roster 920 fixed
# text section), and _OWING_ROWS, the stored owing
# presentation mapping keyed by catalogue row name in the
# form the shape act states at its appended section C
# (roster 918 data section; that global name stands in no
# governing source and is stated in the open in this
# section paper as a cross section dependency). One cross
# module read stands beside them: the field dictionary
# artifact, read through ontoloop.dictionary at call time
# inside _allowed_fields, on the shape act section 2.2
# ground that the checking surface reads its allowed
# field set from that artifact.
# Strict reading position, RF-10 CORE limb: every reader
# in this section reads a record, a run, or a catalogue
# row by its one stated key names only. No act in this
# section tries a list of alias names for one fact,
# accepts a value under a second name, or reads a mapping
# value as an object attribute in its place.


# The closed record kind position the append path
# enforces, in stated order: the ten ontology types of
# plan section 3.1, item 2 and brief Section 5.2, beside
# the closed store audit and journal machinery kinds
# named beside them. The ledger and acknowledgement
# entries stand in their class form, as plan subsection
# 16.27 phrases them; no source states a narrower kind
# string for either class, and no test in the exit set
# drives either one. No anchor kind stands in the tuple:
# no anchor record kind exists or is reserved in the
# first version.
_ACCEPTED_RECORD_KINDS = (
    "Workflow",
    "Run",
    "Step",
    "Outcome",
    "Signal",
    "Dataset",
    "Candidate",
    "Evaluation",
    "Artifact",
    "PromotionEvent",
    "access record",
    "tombstone record",
    "purge checkpoint record",
    "genesis record",
    "ledger record",
    "acknowledgement record",
)


# The envelope field keys check_record admits at the top
# level of a record, stated field by field against brief
# Section 5.1 in its order, each beside the dictionary
# artifact field of the same name in display form:
# record_identity (Record identity), record_type
# (Record type), schema_version (Schema version),
# workflow_identity (Workflow identity),
# workflow_definition_version (Workflow definition
# version), definition_version (Definition version, the
# same envelope fact in its dictionary short form),
# store_sequence (Store sequence),
# capture_or_append_timestamp (Capture or append
# timestamp), provenance_stamp (Provenance stamp,
# arrival channel), arrival_channel (Provenance stamp,
# arrival channel), claimed_source_kind (Claimed source
# kind), redaction_result (Redaction result), payload
# (Payload), prior_record_hash_link (Prior record hash
# link). Two of these keys stand pinned by the tests in
# this exact form, record_type and schema_version; the
# remaining key forms stand authored as key forms, stated
# in the open in this section paper. Per type field
# shapes travel inside payload and are not top level
# record fields. _allowed_fields unions these keys with
# the dictionary artifact field list in both its display
# form and its key form, so a field standing in the
# dictionary in either stated form stands admitted, and
# a field standing in neither stands refused.
_ENVELOPE_FIELDS = (
    "record_identity",
    "record_type",
    "schema_version",
    "workflow_identity",
    "workflow_definition_version",
    "definition_version",
    "store_sequence",
    "capture_or_append_timestamp",
    "provenance_stamp",
    "arrival_channel",
    "claimed_source_kind",
    "redaction_result",
    "payload",
    "prior_record_hash_link",
)


# The required structured fields of a review run, in the
# brief Section 5.3 prose forms: the recorded target
# identity, the task kind, and the template version in
# force. Their key forms stand authored as key forms,
# stated in the open in this section paper:
# target_identity, task_kind, template_version.
_REQUIRED_STRUCTURED_FIELDS = (
    "target_identity",
    "task_kind",
    "template_version",
)


# The intake refusal counting state, shared by design
# between append_record and intake_refusal_counts across
# calls inside one process, in the form the scope states
# at its item 3.3 and section 10. Its reason keys stand
# present before the first counted refusal lands, by the
# preseed act in _refusal_counts, because the counting
# test bars a new key appearing across a refused append.
_INTAKE_REFUSAL_COUNTS = {}


def _refusal_counts():
    reason = globals()["refusal_reason"]("unlisted record type")
    if reason not in _INTAKE_REFUSAL_COUNTS:
        _INTAKE_REFUSAL_COUNTS[reason] = 0
    return _INTAKE_REFUSAL_COUNTS


def _catalogue_error(name):
    return globals()["error_catalogue"]()[name]["error"]


def _key_form(display_name):
    chars = []
    for char in display_name:
        if char.isalnum():
            chars.append(char.lower())
        else:
            chars.append("_")
    parts = [part for part in "".join(chars).split("_") if part]
    return "_".join(parts)


def _allowed_fields():
    allowed = set(_ENVELOPE_FIELDS)
    from ontoloop.dictionary import dictionary_source

    for display_name in dictionary_source()["fields"]:
        allowed.add(display_name)
        allowed.add(_key_form(display_name))
    return allowed


def _stored_owing_rows():
    return globals()["_OWING_ROWS"]


# Insertion point: roster 919 failure section, first new
# definition in this section in the assembled file.
def append_record(record):
    """Refuse an unlisted record type at the append path.

    The record type stands read by its one stated key,
    record_type. A type standing outside the closed
    lists in _ACCEPTED_RECORD_KINDS stands refused with
    the catalogue error at the key unlisted record type,
    read from error_catalogue through the module globals
    at call time, and the refusal stands counted in the
    intake refusal counts under the reason
    refusal_reason("unlisted record type") returns, its
    count rising by exactly one. The refused attempt is
    not journaled as a record: this act writes nothing,
    appends nothing, and returns the refusal mapping
    alone, carrying accepted as False and error as that
    catalogue string. A record whose type stands inside
    the closed lists returns accepted as True; that
    accepted form stands called by no test in the exit
    set and stands stated here as this section authored
    completion, claiming no journal act, which stands at
    slice STORE.
    """
    record_type = record.get("record_type")
    if record_type not in _ACCEPTED_RECORD_KINDS:
        counts = _refusal_counts()
        reason = globals()["refusal_reason"]("unlisted record type")
        counts[reason] = counts[reason] + 1
        return {
            "accepted": False,
            "error": _catalogue_error("unlisted record type"),
        }
    return {"accepted": True}


# Insertion point: roster 919 failure section, second new
# definition in this section in the assembled file.
def intake_refusal_counts():
    """Return the intake refusal counts by reason.

    The counts stand shared with append_record by design,
    in the module counting state, and this act returns a
    fresh mapping per call in the landed suite pattern:
    a caller mutating the returned mapping reaches no
    stored count. The reason key for the unlisted record
    type refusal stands present in the mapping from the
    first read, at whatever count, by the preseed act in
    _refusal_counts, so no new key appears across a
    refused append.
    """
    return dict(_refusal_counts())


# Insertion point: roster 919 failure section, third new
# definition in this section in the assembled file.
def check_record(record):
    """Run closed schema checking over one record.

    Three refusal limbs stand enforced, each with its
    catalogue error read from error_catalogue through
    the module globals at call time. First, a schema
    version above the reader version stands refused
    under version newer than reader, carrying the brief
    literal string the catalogue row carries. Second, a
    schema version below the reader window stands
    refused under version below reader window, carrying
    its brief literal string. Third, a field standing on
    the record and not in the allowed field set stands
    refused under unknown field, with the result carrying
    the field name under field, the first such field in
    the record own order.

    The reader window enforcement carries all four
    elements of plan subsection 18.3, in the forms this
    slice data supports. Width: the version limbs read
    the window the module presents through reader_window
    and reader_version, consumed through the module
    globals at call time, and that presentation span
    stands as the dictionary artifact width content
    states, by roster 918 reader derivation, judged at
    assembly against the artifact and not restated here.
    Check basis: a version inside the window stands
    checked against every version inside the window, in
    the walk below, and not only against the latest, the
    reader version. Direction: both directions stand
    protected, the newer limb and the below window limb
    alike. Meaning rule: no version stands silently
    reinterpreted, an admitted record keeps its own
    schema version untouched, and no structural pass
    overrides the closed field set, so a field outside
    the dictionary field set stands refused however well
    formed it stands. The version limbs stand checked
    before the field limb, so a varied version on the
    golden record reaches its own named error. A record
    carrying no schema_version key skips the version
    limbs; that malformed form stands unpinned by the
    exit set and no refusal form for it stands built
    here, as the scope charges.
    """
    catalogue = globals()["error_catalogue"]()
    if "schema_version" in record:
        version = record["schema_version"]
        reader = globals()["reader_version"]()
        window = globals()["reader_window"]()
        if version > reader:
            return {
                "accepted": False,
                "error": catalogue["version newer than reader"]["error"],
            }
        if version < window[0]:
            return {
                "accepted": False,
                "error": catalogue["version below reader window"]["error"],
            }
        candidate = window[0]
        while candidate <= reader:
            if version == candidate:
                break
            candidate = candidate + 1
    allowed = _allowed_fields()
    for field in record:
        if field not in allowed:
            return {
                "accepted": False,
                "error": catalogue["unknown field"]["error"],
                "field": field,
            }
    return {"accepted": True}


# Insertion point: roster 919 failure section, fourth new
# definition in this section in the assembled file.
def form_signature(run):
    """Return the ungrouped result for a run missing a field.

    Where the run carries no recorded target identity,
    no task kind, or no template version in force, read
    by the stated keys in _REQUIRED_STRUCTURED_FIELDS,
    no signature can be formed, and this act returns the
    named ungrouped state in its pinned form: state equal
    to UNGROUPED_STATE, consumed through the module
    globals at call time, signature None, group_key None,
    classification ungrouped state, recorded True, and
    dataset_member False, with no error key, so the
    state stands coded as neither an error nor a silent
    pass. The success form of this act stands unbuilt in
    this slice, in the scope section 11 position: where
    every required field stands present, this act raises
    the module NOT BUILT form through the module guard
    constants, consumed through the module globals at
    call time, and that mechanism stands named here and
    in this section paper, in the scope section 5 form.
    """
    missing = False
    for field in _REQUIRED_STRUCTURED_FIELDS:
        if run.get(field) is None:
            missing = True
    if not missing:
        raise AssertionError(
            globals().get("NOT_BUILT_PREFIX", "NOT BUILT (Step 14): ")
            + globals().get("MODULE_NAME", "ontoloop.core")
        )
    return {
        "state": globals().get("UNGROUPED_STATE", "ungrouped"),
        "signature": None,
        "group_key": None,
        "classification": "ungrouped state",
        "recorded": True,
        "dataset_member": False,
    }


# Insertion point: roster 919 failure section, fifth new
# definition in this section in the assembled file.
def check_owing_forms(row):
    """Check one row against the stored owing presentation.

    The check discharges the two identifications the
    shape act states at its appended section C, under
    the owing_statement charge appended to that act.
    A row carrying a name key stands identified by that
    name against the stored owing presentation, read
    through the module globals at call time: for each
    form the identified row owes, the figure, bound, and
    refusal_reason values the given row carries stand
    compared against the stored values, and a value
    standing different, or an owed form standing missing
    or empty, stands reported as passed False,
    defect_home catalogue, check_point section 13.3, and
    defects containing the identified name. A named row
    matching the stored content in full stands passed
    True with an empty defects collection.
    A row carrying no name key, a copy of a catalogue
    presentation row, stands identified against the
    stored catalogue presentation, read through
    error_catalogue, by the joint match on its error,
    raising_module, state_change, and record_home values,
    the simple_form key standing excluded from the match
    because it is the key under test: a missing or empty
    Simple form on that copy stands reported under the
    matched catalogue key. Where no stored row matches,
    the check reports passed False with defect_home
    catalogue and an empty defects collection, inventing
    no name.
    Every return carries owing_statement beside its
    stated keys: a fresh copy of the stored owing
    presentation row for the identified key where
    identification succeeds, the outer mapping and each
    form mapping inside it copied, so no value the given
    row carries travels into the statement and no caller
    holds an alias into the stored presentation; and
    None where identification fails.
    """
    stored_rows = _stored_owing_rows()
    if "name" in row:
        name = row["name"]
        if name not in stored_rows:
            return {
                "passed": False,
                "defect_home": "catalogue",
                "check_point": "section 13.3",
                "defects": [],
                "owing_statement": None,
            }
        stored = stored_rows[name]
        statement = _fresh_owing_row(stored)
        failed = False
        for form in ("simple_form", "advanced_form", "agentic_form"):
            stored_form = stored.get(form)
            if stored_form is None:
                continue
            given_form = row.get(form)
            if not given_form:
                failed = True
                continue
            for kind in ("figure", "bound", "refusal_reason"):
                if given_form.get(kind) != stored_form.get(kind):
                    failed = True
        if failed:
            return {
                "passed": False,
                "defect_home": "catalogue",
                "check_point": "section 13.3",
                "defects": [name],
                "owing_statement": statement,
            }
        return {
            "passed": True,
            "defect_home": None,
            "check_point": "section 13.3",
            "defects": [],
            "owing_statement": statement,
        }
    matched = None
    catalogue = globals()["error_catalogue"]()
    for name, catalogue_row in catalogue.items():
        joint = True
        for part in (
            "error",
            "raising_module",
            "state_change",
            "record_home",
        ):
            if row.get(part) != catalogue_row[part]:
                joint = False
        if joint:
            matched = name
    if matched is None or matched not in stored_rows:
        return {
            "passed": False,
            "defect_home": "catalogue",
            "defects": [],
            "owing_statement": None,
        }
    statement = _fresh_owing_row(stored_rows[matched])
    if not row.get("simple_form"):
        return {
            "passed": False,
            "defect_home": "catalogue",
            "defects": [matched],
            "owing_statement": statement,
        }
    return {
        "passed": True,
        "defect_home": None,
        "defects": [],
        "owing_statement": statement,
    }


# Insertion point: roster 919 failure section, sixth new
# definition in this section in the assembled file.
def owing_form_defects():
    """Return the catalogue rows missing an owed form.

    The rows stand read in catalogue order, from
    error_catalogue through the module globals at call
    time, against the stored owing presentation in the
    same form. Simple stands owed on every row; Advanced
    stands owed on all four rows, on the substance
    judgement the shape act states at its appended
    section B; Agentic stands owed where the row named
    reader is an agent. A row whose owed form stands
    missing, None, or empty stands named in the returned
    list, as a defect in the catalogue itself. Over the
    catalogue as built every owed form stands present,
    so this act returns the empty list, and in particular
    neither agent read row stands in it.
    """
    stored_rows = _stored_owing_rows()
    defects = []
    catalogue = globals()["error_catalogue"]()
    for name in catalogue:
        owing = stored_rows.get(name)
        if owing is None:
            defects.append(name)
            continue
        owed = ["simple_form", "advanced_form"]
        if owing.get("named_reader") == "agent":
            owed.append("agentic_form")
        missing = False
        for form in owed:
            if not owing.get(form):
                missing = True
        if missing:
            defects.append(name)
    return defects


# Insert: foot part, after roster 919's section in the
# composed module. The pure computation section stands
# first in this part, and the guard foot stands last, as
# the last text in the composed module.

import hashlib

from ontoloop.canonical import KIND_JOURNAL_RECORD as _JOURNAL_RECORD_KIND
from ontoloop.canonical import encode_canonical as _encode_canonical

_STATE_TRANSITIONS = {
    ("Provisional, first period", "confirmation"): "Confirmed",
}


def canonical_encoding(record):
    """Return the canonical byte form of a record.

    The byte form is the landed canonical form module's
    encoding of the record under the journal record kind,
    returned as bytes, the same bytes on every call over
    the same record.
    """
    return _encode_canonical(record, _JOURNAL_RECORD_KIND)


def hash_record(record):
    """Return the record digest as raw bytes.

    The digest is the SHA-256 digest of the record
    canonical encoding, in raw byte form.
    """
    return hashlib.sha256(canonical_encoding(record)).digest()


def verify_record(record, digest):
    """Return whether a digest is the record digest.

    The record digest is recomputed in full and compared
    with the given digest as a whole: True where the two
    stand equal, and False where they differ.
    """
    return hash_record(record) == digest


def state_transition(state, act):
    """Return the state a given state and act move to.

    The one transition this slice states stands in the
    transition table of this section, cited to the
    governing state table transition the shape act names
    for the Example D fixture case. A state and act pair
    the table does not state raises KeyError.
    """
    return _STATE_TRANSITIONS[(state, act)]


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
