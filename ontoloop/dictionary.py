"""Dictionary and schema module, slice SPEC-DICT form.

The field dictionary artifact, built from one machine readable
source: the source and its validator, the Step 7 field inventory,
the EVAL minimum materialised as the trace target, the field
level audit against that minimum with the registered disposition
words at DQ-SPEC-7 and its closure check, the example code shapes
and the dictionary check over them, and the relation catalogue
with the never reuse register kept with the dictionary. The
reader window width stands as content inside the artifact the
source serves, in the form the source states.

What this slice does not build stands unbuilt behind the module
level guard at the foot of this file: the reader window checking
implementation and the closed schema refusal implementation,
rendered views of the dictionary, and the dictionary version
move acts. A lookup of a public name this module does not
provide raises AssertionError in the NOT BUILT form the suite
harness uses. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

_DICTIONARY_VERSION = 1

_READER_WINDOW_WIDTH_VERSIONS = 3

_INVENTORY_ROWS = (
    ('Record identity', 'Envelope'),
    ('Record type', 'Envelope'),
    ('Schema version', 'Envelope'),
    ('Workflow identity', 'Envelope'),
    ('Workflow definition version', 'Envelope'),
    ('Store sequence', 'Envelope'),
    ('Capture or append timestamp', 'Envelope'),
    ('Provenance stamp, arrival channel', 'Envelope'),
    ('Claimed source kind', 'Envelope'),
    ('Redaction result', 'Envelope'),
    ('Payload', 'Envelope'),
    ('Prior record hash link', 'Envelope'),
    ('Workflow identity', 'Workflow'),
    ('Display name', 'Workflow'),
    ('Definition version', 'Workflow'),
    ('Signature field list', 'Workflow'),
    ('Task kind set', 'Workflow'),
    ('Review form statement', 'Workflow'),
    ('Provisional loadability opt out state', 'Workflow'),
    ('Current bundle pointer', 'Workflow'),
    ('Run identity', 'Run'),
    ('Workflow identity and definition version', 'Run'),
    ('Task verbatim', 'Run'),
    ('Work product identity and reference', 'Run'),
    ('Task signature', 'Run'),
    ('Signature version', 'Run'),
    ('Group key', 'Run'),
    ('External task identity', 'Run'),
    ('Pool stamp, inherited', 'Run'),
    ('Promoted bundle identity in use', 'Run'),
    ('Steps completeness flag', 'Run'),
    ('Reasoning summary, where captured', 'Run'),
    ('Redaction uncertain state', 'Run'),
    ('Outcome state', 'Run'),
    ('Step identity', 'Step'),
    ('Run reference', 'Step'),
    ('Predecessor reference', 'Step'),
    ('No parent reference', 'Step'),
    ('Step content', 'Step'),
    ('Step kind', 'Step'),
    ('Outcome identity', 'Outcome'),
    ('Run reference', 'Outcome'),
    ('Review outcome', 'Outcome'),
    ('Operator grade band', 'Outcome'),
    ('System grade points', 'Outcome'),
    ('Grade source stamp', 'Outcome'),
    ('Correction verbatim', 'Outcome'),
    ('Success position', 'Outcome'),
    ('Signal identity', 'Signal'),
    ('Run reference', 'Signal'),
    ('Signal kind', 'Signal'),
    ('Channel stamp', 'Signal'),
    ('Signal value', 'Signal'),
    ('Build effect position', 'Signal'),
    ('Bundle reference, where attributed', 'Signal'),
    ('Dataset identity and version', 'Dataset'),
    ('Workflow reference', 'Dataset'),
    ('Build target statement', 'Dataset'),
    ('Precedence rule statement', 'Dataset'),
    ('Member group list', 'Dataset'),
    ('Intake account, runs seen', 'Dataset'),
    ('Intake account, runs with outcomes', 'Dataset'),
    ('Intake account, runs dropped per reason', 'Dataset'),
    ('Intake account, pool counts', 'Dataset'),
    ('Intake account, per workflow shortfalls', 'Dataset'),
    ('Intake account, self reported share with its two counts', 'Dataset'),
    ('Intake account, redaction volume', 'Dataset'),
    ('Intake account, refusal counts by reason', 'Dataset'),
    ('Intake account, quarantined share with counts by layer and class', 'Dataset'),
    ('Intake account, cluster size distribution and largest clusters', 'Dataset'),
    ('Intake account, group key join rate', 'Dataset'),
    ('Intake account, final membership restatement', 'Dataset'),
    ('Intake stamps', 'Dataset'),
    ('Curation input versions', 'Dataset'),
    ('Seal position', 'Dataset'),
    ('Operator attestation', 'Dataset'),
    ('Candidate identity', 'Candidate'),
    ('Workflow reference', 'Candidate'),
    ('Author position', 'Candidate'),
    ('Lineage, building runs', 'Candidate'),
    ('Candidate content', 'Candidate'),
    ('Frozen position', 'Candidate'),
    ('Source Dataset reference', 'Candidate'),
    ('Evaluation identity', 'Evaluation'),
    ('Candidate reference and content hash', 'Evaluation'),
    ('Baseline reference and content hash', 'Evaluation'),
    ('Dataset version reference', 'Evaluation'),
    ('Scorer identity and version', 'Evaluation'),
    ('Holdout group count', 'Evaluation'),
    ('Per group scores, candidate and baseline', 'Evaluation'),
    ('Groups with a non zero paired difference', 'Evaluation'),
    ('Headline scores', 'Evaluation'),
    ('Margin, practical component', 'Evaluation'),
    ('Margin, noise component', 'Evaluation'),
    ('Margin, selection component', 'Evaluation'),
    ('Expected selection bias', 'Evaluation'),
    ('Verdict', 'Evaluation'),
    ('Not scored reasons, where the verdict is not scored', 'Evaluation'),
    ('Claim label', 'Evaluation'),
    ('Low confidence stamp position', 'Evaluation'),
    ('Cost cap and recipe identity', 'Evaluation'),
    ('Cost table version', 'Evaluation'),
    ('Estimate and start outcome', 'Evaluation'),
    ('Spend by operation class', 'Evaluation'),
    ('Journal counted operations and priced journal total', 'Evaluation'),
    ('Cap headroom and abort point', 'Evaluation'),
    ('Selection ledger charge', 'Evaluation'),
    ('Drop counts at evaluation', 'Evaluation'),
    ('Pre scoring protocol reference', 'Evaluation'),
    ('Artifact identity, bundle hash', 'Artifact'),
    ('Provenance block', 'Artifact'),
    ('Workflow reference', 'Artifact'),
    ('Bundle version', 'Artifact'),
    ('Instruction items', 'Artifact'),
    ('Bundle content token count', 'Artifact'),
    ('Applicability markers', 'Artifact'),
    ('Caveats block', 'Artifact'),
    ('Claim label, bundle form', 'Artifact'),
    ('Null artifact marker', 'Artifact'),
    ('File presentation hash', 'Artifact'),
    ('PromotionEvent identity', 'PromotionEvent'),
    ('Act kind', 'PromotionEvent'),
    ('Bundle reference and digest', 'PromotionEvent'),
    ('Workflow reference', 'PromotionEvent'),
    ('Evaluation reference', 'PromotionEvent'),
    ('Lineage, judging runs', 'PromotionEvent'),
    ('Margin and confidence facts', 'PromotionEvent'),
    ('Stamps that apply', 'PromotionEvent'),
    ('Instrument versions', 'PromotionEvent'),
    ('State position after the act', 'PromotionEvent'),
    ('Review bound position, on a provisional record', 'PromotionEvent'),
    ('Outcome coverage, provisional period', 'PromotionEvent'),
    ('Signal coverage, provisional period', 'PromotionEvent'),
    ('Production evidence label position', 'PromotionEvent'),
    ('Production evidence weight position', 'PromotionEvent'),
    ('Reason, on a rollback record', 'PromotionEvent'),
    ('Reason, on other operator acts', 'PromotionEvent'),
    ('Acknowledgement position, where a stamp blocks a pass', 'PromotionEvent'),
    ('Demotion flag and its age', 'PromotionEvent'),
    ('Refusal use position', 'PromotionEvent'),
    ('Purge caveat position', 'PromotionEvent'),
    ('Withdrawn dataset mark position', 'PromotionEvent'),
    ('Displaced bundle reference, on a rollback act', 'PromotionEvent'),
)

_FIELDS = tuple(
    dict.fromkeys(field for field, record_type in _INVENTORY_ROWS)
)

_DISPOSITIONS = (
    "traced",
    "traced conditional",
    "missing",
    "contradicted",
)


def _inventory_entries():
    return [
        {"field": field, "record_type": record_type}
        for field, record_type in _INVENTORY_ROWS
    ]


def dictionary_source():
    """Return the machine readable dictionary source.

    The mapping carries exactly the keys version, fields, and
    reader_window. The version is the first version identity.
    The fields value is a tuple of the distinct field names
    from the Step 7 inventory rows, in first occurrence order,
    with duplicates across record types collapsed. The
    reader_window value is a nested mapping carrying the
    schema version reader window width in number form, beside
    its check basis and the direction it protects.
    """
    return {
        "version": _DICTIONARY_VERSION,
        "fields": _FIELDS,
        "reader_window": {
            "width_versions": _READER_WINDOW_WIDTH_VERSIONS,
            "check_basis": (
                "every version inside the window, "
                "not only the latest"
            ),
            "direction": "both directions",
        },
    }


def step7_inventory():
    """Return the Step 7 field inventory entries.

    The list carries one entry per inventory row, in inventory
    order, envelope rows first. Each entry is a mapping with
    the keys field and record_type: field carries the row
    field name exactly as the inventory states it, and
    record_type carries the type the row belongs to, with the
    envelope rows carrying Envelope. A fresh list of fresh
    entries is returned on each call.
    """
    return _inventory_entries()


def eval_minimum():
    """Return the EVAL minimum as the trace target.

    The list carries the same entries, in the same order and
    the same form, as the Step 7 inventory, so its field set
    equals the inventory field set exactly. A fresh list of
    fresh entries is returned on each call.
    """
    return _inventory_entries()


def dq_spec_7_dispositions():
    """Return the registered DQ-SPEC-7 disposition words.

    The set holds exactly the four words the plan names at
    DQ-SPEC-7. A fresh set is returned on each call.
    """
    return set(_DISPOSITIONS)

# Section: failure and boundary, roster 877.
# Functions: validate_dictionary_source, dictionary_check,
# audit_closure, register_name.
# Cross section names are read from the module globals at call
# time, because the assembled module carries them in other
# sections: dictionary_source and step7_inventory from the data
# section, retired_names from the surface section. No name in
# this section is defined by any other section.

_AUDIT_DIRECTIONS = (
    "dictionary_to_minimum",
    "minimum_to_dictionary",
)

_BLOCKING_DISPOSITIONS = ("missing", "contradicted")


def _listed_fields():
    source = globals().get("dictionary_source")
    if not callable(source):
        return set()
    return set(source()["fields"])


def _retired_names():
    retired = globals().get("retired_names")
    if not callable(retired):
        return set()
    return set(retired())


def _expected_audit_pairs():
    inventory = globals().get("step7_inventory")
    if not callable(inventory):
        return set()
    pairs = set()
    for entry in inventory():
        for direction in _AUDIT_DIRECTIONS:
            pairs.add((entry["field"], direction))
    return pairs


def validate_dictionary_source(source):
    """Validate a dictionary source against the listed fields.

    Returns exactly the keys accepted, version, and
    refused_fields. The source is accepted at its own version
    when every field it carries stands in the listed field set
    of the dictionary source this module serves. A field that
    does not stand in that set is refused, named in
    refused_fields in the order it appears in the source.
    """
    listed = _listed_fields()
    refused = [
        field for field in source["fields"] if field not in listed
    ]
    return {
        "accepted": not refused,
        "version": source["version"],
        "refused_fields": refused,
    }


def dictionary_check(fields):
    """Check a field set against the dictionary.

    Returns the keys accepted and refused_fields. The check is
    accepted when every given field stands in the dictionary.
    Where any field stands outside the dictionary, accepted is
    False and refused_fields names exactly the outside fields,
    in the order they were given, no more and no less.
    """
    listed = _listed_fields()
    refused = [field for field in fields if field not in listed]
    return {
        "accepted": not refused,
        "refused_fields": refused,
    }


def audit_closure(rows):
    """Judge whether an audit row set closes.

    Returns the keys closed and blocking_rows. A row whose
    disposition is missing or contradicted blocks closure and
    its field is named in blocking_rows. A missing row also
    blocks closure: missingness is judged both against the
    expected trace, derived from the Step 7 inventory this
    module serves where that name stands in the module, and
    against the directions present for each field in the rows
    given, so a field left with only one direction stands
    named. blocking_rows carries field name strings, each
    blocking field named once, in first blocking order. Where
    nothing blocks, closed is True and blocking_rows is empty.
    """
    rows = list(rows)
    blocking = []

    def _block(field):
        if field not in blocking:
            blocking.append(field)

    present = set()
    directions_by_field = {}
    for row in rows:
        field = row["field"]
        direction = row["direction"]
        present.add((field, direction))
        directions_by_field.setdefault(field, set()).add(direction)
        if row["disposition"] in _BLOCKING_DISPOSITIONS:
            _block(field)

    for field, direction in sorted(_expected_audit_pairs()):
        if (field, direction) not in present:
            _block(field)

    for field in directions_by_field:
        for direction in _AUDIT_DIRECTIONS:
            if direction not in directions_by_field[field]:
                _block(field)

    return {
        "closed": not blocking,
        "blocking_rows": blocking,
    }


def register_name(name):
    """Register a name against the never reuse register.

    Returns the keys accepted and name, with the name echoed
    back. A retired name is refused, with accepted False. A
    name that does not stand in the retired set is accepted.
    The retired set is read from retired_names in the module
    globals at call time.
    """
    if name in _retired_names():
        return {"accepted": False, "name": name}
    return {"accepted": True, "name": name}

# Section: surface and fixed text, roster 878.
# Functions: field_level_audit, relation_catalogue,
# registered_cross_types, retired_names, example_code_shapes,
# and the guard foot. No cross section call stands in this
# section. The guard foot at the end is the scope's unified
# form, copied character for character.

_TRACE_DIRECTIONS = (
    "dictionary_to_minimum",
    "minimum_to_dictionary",
)

_TRACED = "traced"

_REGISTERED_CROSS_TYPES = ("step_predecessor_reference",)

_TOMBSTONE_BEHAVIOUR = (
    "If the target record is tombstoned, the reference "
    "resolves to the tombstone itself and never to content."
)

_SUPERSESSION_BEHAVIOUR = (
    "If the target record is superseded, the reference "
    "follows the supersession to the successor identity "
    "and never to the superseded content."
)

_RETIRED_NAMES = ("former_field_name",)

_EXAMPLE_A_FIELDS = (
    "run identity",
    "workflow identity",
    "workflow definition version",
    "schema version",
    "task verbatim",
    "steps",
    "outcome record",
    "signal records",
)

_UNLISTED_EXAMPLE_FIELD = "unlisted_example_field"


def field_level_audit(inventory):
    """Return the field level audit rows for an inventory.

    Returns one row per field per direction, for the
    directions dictionary_to_minimum and minimum_to_dictionary,
    in that order per field. Each row carries exactly the keys
    field, direction, and disposition, and every row carries
    the disposition traced.
    """
    rows = []
    for entry in inventory:
        for direction in _TRACE_DIRECTIONS:
            rows.append(
                {
                    "field": entry["field"],
                    "direction": direction,
                    "disposition": _TRACED,
                }
            )
    return rows


def relation_catalogue():
    """Return the relation catalogue rows.

    Returns one row per registered cross type reference. Each
    row carries exactly the keys cross_type_reference,
    tombstone_behaviour, and supersession_behaviour. The rows
    are built from the same registered set that
    registered_cross_types returns, so the stated set equals
    the registered set by construction.
    """
    return [
        {
            "cross_type_reference": reference,
            "tombstone_behaviour": _TOMBSTONE_BEHAVIOUR,
            "supersession_behaviour": _SUPERSESSION_BEHAVIOUR,
        }
        for reference in _REGISTERED_CROSS_TYPES
    ]


def registered_cross_types():
    """Return the registered cross type reference set."""
    return _REGISTERED_CROSS_TYPES


def retired_names():
    """Return the never reuse register's retired names."""
    return _RETIRED_NAMES


def example_code_shapes():
    """Return the example code shapes.

    Returns a non empty sequence of shapes, each carrying only
    the key fields, whose value is a tuple of field name
    strings. The first shape carries the Example A field set
    in its stated order. The second shape carries one field
    that stands outside the dictionary on purpose, so the
    dictionary check refusal can be exercised on it.
    """
    return [
        {"fields": _EXAMPLE_A_FIELDS},
        {"fields": (_UNLISTED_EXAMPLE_FIELD,)},
    ]


MODULE_NAME = "ontoloop.dictionary"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "audit_closure",
    "dictionary_check",
    "dictionary_source",
    "dq_spec_7_dispositions",
    "eval_minimum",
    "example_code_shapes",
    "field_level_audit",
    "register_name",
    "registered_cross_types",
    "relation_catalogue",
    "retired_names",
    "step7_inventory",
    "validate_dictionary_source",
]


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
