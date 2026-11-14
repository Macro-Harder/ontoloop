"""Golden record sets and spanning suite module, slice GOLDEN-SPAN form.

The corpus and exercise support module outside the runtime
core: the golden record sets, one real shaped record per
type per schema version, re read under the current schema
version; the spanning group regression suite, running in
the ordinary test run over its fixture contents, covering
external task identity grouping across a signature version
change and no merge of signature based groups across that
change, with pool stamp consequences checked, its suite
result record standing as the counted evidence home under
the one counted row, with the migration occasion record
cited inside it by pointer at each migration run, that
citation demoting nothing and the migration occasion
record remaining an evidence home in its own right;
golden record blessing as a named act, a record re blessed
after STORE closes standing recorded as re blessed by
that act, with automatic regeneration never standing as
evidence; and the meaning change record surface of the
spanning suite, the latest meaning change entry in the
suite result record, the discharge state of the meaning
change bar, and the loop report classification printed
by pointer to that entry only.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of this
file. A lookup of a private or dunder name raises
AttributeError in the ordinary form. The golden records
of this module are fixtures and carry no actor claim.
"""

MODULE_NAME = "ontoloop.golden_span"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "discharge_state",
    "golden_record",
    "golden_record_sets",
    "latest_meaning_change_entry",
    "loop_report_classification",
    "re_bless",
    "re_read",
    "regenerate",
    "run_spanning_suite",
]


def _record_types():
    from ontoloop.dictionary import step7_inventory

    types = []
    for entry in step7_inventory():
        record_type = entry["record_type"]
        if record_type == "Envelope":
            continue
        if record_type not in types:
            types.append(record_type)
    return types


def _schema_versions():
    from ontoloop.core import reader_window

    lower, upper = reader_window()
    return list(range(lower, upper + 1))


def _field_names(record_type):
    from ontoloop.dictionary import step7_inventory

    return [
        entry["field"]
        for entry in step7_inventory()
        if entry["record_type"] == record_type
    ]


def _field_value(record_type, schema_version, field):
    """Return a payload value shaped for one field.

    The value stands formed from the field name, the
    record type, and the schema version of the record
    it stands in, so no two fields of a record carry
    one identical placeholder and a field stands
    answered in a form its name states: a version
    field carries the schema version itself, an
    identity field carries an identity formed from
    the type and the version, and every other field
    carries a value naming its field, its type, and
    its version.
    """
    lowered = field.lower()
    slug = lowered.replace(" ", "-")
    if "version" in lowered:
        return schema_version
    if "identity" in lowered or lowered.endswith(" id"):
        return "golden-" + record_type.lower() + "-" + str(schema_version) + "-" + slug
    return slug + " value for " + record_type + " version " + str(schema_version)


def _set_record(record_type, schema_version):
    payload = {}
    for field in _field_names(record_type):
        payload[field] = _field_value(record_type, schema_version, field)
    return {
        "record_identity": (
            "golden-" + record_type.lower() + "-" + str(schema_version)
        ),
        "record_type": record_type,
        "schema_version": schema_version,
        "payload": payload,
    }


def golden_record_sets():
    """Return the golden record sets mapping.

    The mapping carries exactly the three keys the
    GOLDEN-T01 tests read, in that read order:
    record_types, schema_versions, and records.
    record_types stands as the record type collection
    derived at call time from the landed dictionary
    inventory: the per type rows of step7_inventory() in
    first occurrence order, the Envelope rows standing
    apart as envelope rows and not as a type, which
    yields exactly the ten ontology types the shape act
    derives at its section 3.3. schema_versions stands
    as every schema version inside the reader window the
    landed CORE position presents, lower edge to reader
    version inclusive, derived at call time from
    core.reader_window(): the window frame stands
    grounded in that derivation, and the membership of
    the collection as exactly the window stands authored
    and guessed under entry 89 ruling 3, the shape act
    stating the membership in no text at its DG-2.
    records stands as a mapping from (record type,
    schema version) tuples, type first and version
    second, to one record per pair, covering the whole
    cross product of the two collections. Each record
    carries the four envelope keys record_identity,
    record_type, schema_version, and payload: the record
    type and schema version stand as the pair key states
    them, the record identity stands authored in the
    golden word form in this section, and the payload
    carries the per type field names the landed
    dictionary inventory states for that type, in
    inventory order, each field carrying a value shaped
    for its field from the field name, the record type,
    and the schema version, in the form the field value
    act of this module states, no governing text stating
    a value for any field of any type beyond the CORE
    fixture Run form. The envelope form of a set
    record stands in the shape act DG-4 position as
    ungrounded; this section authored completion carries
    no store sequence, no prior record hash link, no
    workflow identity, and no workflow definition
    version, a set record standing in no journal and
    belonging to no workflow in any text this slice
    reads, and that completion stands recorded as
    authored in this section paper. A fresh mapping,
    with fresh nested mappings and fresh records, stands
    returned on every call.
    """
    record_types = _record_types()
    schema_versions = _schema_versions()
    records = {}
    for record_type in record_types:
        for schema_version in schema_versions:
            records[(record_type, schema_version)] = _set_record(
                record_type, schema_version
            )
    return {
        "record_types": record_types,
        "schema_versions": schema_versions,
        "records": records,
    }


def re_read(record):
    """Return the re reading result for one record.

    The record stands checked under the current schema
    version on every call, in four limbs. The record
    must stand as a mapping carrying the four envelope
    keys, record identity, record type, schema version,
    and payload. Its record type must stand among the
    record types the dictionary inventory states. Its
    schema version must stand inside the reader window
    the landed CORE position presents, lower edge to
    reader version inclusive. Its payload must stand
    as a mapping whose keys stand exactly as the field
    names the inventory states for its record type.
    A record passing every limb returns read True with
    the record itself. A record failing any limb
    returns read False with the record and a refusal
    naming the limb that refused it, in the case names
    this act states: not a record mapping, envelope key
    missing, record type unlisted, schema version
    outside the reader window, and payload keys not
    the fields of the record type. No record stands
    reported as read on a limb this act did not run.
    """
    def refusal(case):
        return {
            "read": False,
            "record": record,
            "refusal": {"case": case},
        }

    if not isinstance(record, dict):
        return refusal("not a record mapping")
    for key in ("record_identity", "record_type",
                "schema_version", "payload"):
        if key not in record:
            return refusal("envelope key missing: " + key)
    if record["record_type"] not in _record_types():
        return refusal("record type unlisted")
    if record["schema_version"] not in _schema_versions():
        return refusal("schema version outside the reader window")
    payload = record["payload"]
    if not isinstance(payload, dict):
        return refusal("payload keys not the fields of the record type")
    if sorted(payload.keys()) != sorted(_field_names(record["record_type"])):
        return refusal("payload keys not the fields of the record type")
    return {"read": True, "record": record}


def golden_record():
    """Return a fresh golden shaped record mapping.

    The record stands as the CORE fixture consumed by
    reference: this act returns core.golden_record()
    whole, at call time, in the scope section 10 G-4
    proposed form the adoption at entry 89 answers, a
    fresh envelope formed Run record at the lower edge
    of the reader window, with fresh nested mappings on
    every call because the CORE act returns fresh. The
    shape act at its DG-10 states that no text states
    whether this module singular name is that fixture
    consumed, a set record, or a form of its own; the
    consumption form stands taken here on the scope
    proposal and the entry 89 ruling, and stands recorded
    in this section paper in the open as a position taken
    on that ground, not as a transcribed identity. The
    record is the input form the GOLDEN-T03 blessing acts
    of section B consume; this section states no blessing
    position on it.
    """
    from ontoloop.core import golden_record as _core_golden_record

    return _core_golden_record()


# The eight affected classes the meaning change trigger
# names, in the order the spanning test file states them
# at its head, grounded in plan subsection 18.45 as that
# file transcribes it. The discharge computation reads
# its required coverage from this tuple where the caller
# passes no affected classes of its own.
_AFFECTED_CLASSES = (
    "deduplication parameter or rule",
    "clustering parameter or rule",
    "normalisation parameter or rule",
    "filtering parameter or rule",
    "redaction parameter or rule",
    "truncation parameter or rule",
    "type mapping change",
    "new enum value absorbed by a default branch",
)

# The eight spanning suite check identifiers, in order.
_CHECKS_RUN = (
    "SPAN-T01",
    "SPAN-T02",
    "SPAN-T03",
    "SPAN-T04",
    "SPAN-T05",
    "SPAN-T06",
    "SPAN-T07",
    "SPAN-T08",
)

# The result wording each check carries in the standing
# entry. This wording stands authored and guessed under
# entry 89 ruling 3, in the form the spanning tests
# themselves supply for their varied entries.
_CHECK_RESULT = "meaning check result recorded"

# The classification the standing entry carries, one of
# the two forms plan subsection 19.101 point three and
# subsection 18.45 state. The choice of this one of the
# two for the standing fixture facing entry stands
# authored and guessed under entry 89 ruling 3.
_CLASSIFICATION = "no meaning change shown"

# The standing entry change wording and its identity.
# Both stand authored and guessed under entry 89 ruling 3:
# no governing text states the change wording of the
# standing entry, and no governing text states the entry
# identity form, the tests pinning only that the loop
# report pointer equals it.
_ENTRY_CHANGE = "definition of the spanning suite meaning checks"
_ENTRY_IDENTITY = "meaning change entry 1"

# The discharging seat of the standing entry, in the form
# plan subsection 19.101 point two grounds: the discharge
# act stands owned by the GOLDEN-SPAN slice owner seat.
_DISCHARGING_SEAT = "GOLDEN-SPAN slice owner seat"


def _spanning_rows():
    """Return a fresh copy of the spanning fixture rows.

    The rows stand as the GOLDEN-T02 fixture store contents
    in result facing form: each row names a group identity,
    a signature version, a pool stamp, and an outcome, in
    the merged list fixture field form. Every concrete
    value stands authored and guessed under entry 89
    ruling 3, recorded as such in the fragment paper: the
    group identities, the signature version values 1 and
    2, the pool stamp values, the outcome wordings, the
    row count of four, and the key spellings group_identity
    and signature_version, which no test pins. In substance
    the four rows exercise the grounded shapes: the first
    two rows share one external task identity group across
    the signature version change and carry that group one
    permanent pool stamp, in the brief Section 5.3 pool
    consequence form; the last two rows stand as signature
    based groups on either side of the change, standing
    separate with their own pool stamps, merged in no way.
    A fresh list of fresh mappings stands returned on
    every call, so a caller variation reaches no later
    result.
    """
    return [
        {
            "group_identity": "external task group 1",
            "signature_version": 1,
            "pool_stamp": "pool stamp 1",
            "outcome": "accepted, group formed",
        },
        {
            "group_identity": "external task group 1",
            "signature_version": 2,
            "pool_stamp": "pool stamp 1",
            "outcome": "joined existing group, carries group pool stamp",
        },
        {
            "group_identity": "signature group A",
            "signature_version": 1,
            "pool_stamp": "pool stamp 2",
            "outcome": "stands separate",
        },
        {
            "group_identity": "signature group B",
            "signature_version": 2,
            "pool_stamp": "pool stamp 3",
            "outcome": "stands separate, no merge across the change",
        },
    ]


def run_spanning_suite(rows=None):
    """Return the spanning group regression suite result.

    The result stands computed from the fixture rows at
    every call. Where the caller passes rows, those rows
    stand grouped in place of the standing fixture rows,
    and every result value below stands derived from the
    rows in hand, so rows contradicting a shape change
    the result for that shape. The grouping act groups
    the rows by group identity. External task identity
    grouping across the signature version change stands
    where one group identity spans more than one
    signature version and carries one pool stamp across
    all of its rows. Signature based groups stand merged
    across the change where two distinct group identities
    on opposite sides of the change share one pool stamp,
    the shared stamp standing as the merge sign. The pool
    stamp consequences stand checked where every row
    carries a pool stamp and an outcome and every group
    spanning the change carries exactly one pool stamp
    across its rows. The evidence home and migration run
    positions stand in the forms the shape act states.
    A fresh result, with fresh nested values, stands
    returned on every call.
    """
    if rows is None:
        rows = _spanning_rows()
    else:
        rows = [dict(row) for row in rows]
    by_identity = {}
    for row in rows:
        by_identity.setdefault(row.get("group_identity"), []).append(row)
    grouped_across = False
    for identity, group in by_identity.items():
        versions = {row.get("signature_version") for row in group}
        stamps = {row.get("pool_stamp") for row in group}
        if len(versions) > 1 and len(stamps) == 1:
            grouped_across = True
    merged_across = False
    identities = list(by_identity.keys())
    for first_index in range(len(identities)):
        for second_index in range(first_index + 1, len(identities)):
            first = by_identity[identities[first_index]]
            second = by_identity[identities[second_index]]
            first_versions = {row.get("signature_version") for row in first}
            second_versions = {row.get("signature_version") for row in second}
            first_stamps = {row.get("pool_stamp") for row in first}
            second_stamps = {row.get("pool_stamp") for row in second}
            if first_stamps & second_stamps and first_versions != second_versions:
                merged_across = True
    pool_checked = True
    for row in rows:
        if "pool_stamp" not in row or "outcome" not in row:
            pool_checked = False
    for identity, group in by_identity.items():
        versions = {row.get("signature_version") for row in group}
        stamps = {row.get("pool_stamp") for row in group}
        if len(versions) > 1 and len(stamps) != 1:
            pool_checked = False
    return {
        "ran_in_ordinary_run": True,
        "shapes": {
            "external task identity grouping": {
                "grouped_across_signature_version_change": grouped_across,
            },
            "signature based groups": {
                "merged_across_signature_version_change": merged_across,
            },
        },
        "pool_stamp_consequences_checked": pool_checked,
        "rows": rows,
        "evidence_home": {
            "counted_record": "suite result record",
            "stands_under_one_counted_row": True,
            "citation_demotes_migration_record": False,
            "migration_occasion_record_remains_evidence_home": True,
        },
        "migration_runs": [
            {"migration_occasion_record_citation": "by pointer"},
        ],
    }


def re_bless(record):
    """Return a record recorded as re blessed by this act.

    The blessing stands recorded on the record itself, in
    the GOLDEN-T03 test pinned form: a blessing mapping
    carrying act equal to re blessed and named_act standing
    True, the named act position grounded at plan sections
    2.3 and 11.2 in the shape act section 6 form. The
    return stands as a fresh mapping carrying every key of
    the record passed in, with the blessing mapping set
    beside them: that input preservation form stands
    authored and guessed under entry 89 ruling 3, no text
    pinning it, recorded as such in the fragment paper.
    The record passed in stands unmutated.
    """
    blessed = dict(record)
    blessed["blessing"] = {"act": "re blessed", "named_act": True}
    return blessed


def regenerate(record):
    """Return the automatic regeneration result for a record.

    Automatic regeneration is never evidence, in the
    GOLDEN-T03 rule form grounded at plan section 6.5 and
    the ANA2-03 adoption: the return carries
    counts_as_evidence standing False, and no other key,
    no field beyond that one standing pinned by any test
    or stated in any text for this result. The record
    passed in stands unread by this act beyond its
    standing as the act input, and stands unmutated.
    """
    return {"counts_as_evidence": False}


def latest_meaning_change_entry():
    """Return the latest meaning change record entry.

    The entry stands in the form MeaningChangeRecordTests
    pins and plan subsection 19.101 point three states,
    field for field: the change, the affected classes, the
    checks run by their suite identifiers, the result of
    each check as a mapping over those identifiers, the
    classification in one of its two governed forms, and
    the discharging seat, beside entry_identity, which the
    loop report pointer reads and which stands as a test
    form field with no prose counterpart, at shape act
    DG-14. The concrete values stand as the constants of
    this section state them, each recorded grounded or
    authored and guessed in the fragment paper in its own
    terms. The standing entry covers every affected class
    and every check, in the fixture facing position shape
    act DG-15 records: no change stands entered into this
    module by any act, and the entry stands as the suite
    result record standing entry in that position. A fresh
    entry, with fresh nested values, stands returned on
    every call.
    """
    return {
        "change": _ENTRY_CHANGE,
        "affected_classes": list(_AFFECTED_CLASSES),
        "checks_run": list(_CHECKS_RUN),
        "result_of_each_check": {
            check: _CHECK_RESULT for check in _CHECKS_RUN
        },
        "classification": _CLASSIFICATION,
        "discharging_seat": _DISCHARGING_SEAT,
        "entry_identity": _ENTRY_IDENTITY,
    }


def discharge_state(entry=None, affected_classes=None):
    """Return the discharge state of the meaning change bar.

    The state stands in the form MeaningChangeRecordTests
    pins and plan subsection 19.101 point four states. With
    no entry standing, the bar stands: discharged False,
    bar_stands True, and change_passed_as_no_change False,
    a change of that kind standing passed as no change in
    no report. With an entry standing, the reading set of
    this computation stands as this section states it in
    the open, at shape act DG-15, as an authored completion
    under entry 89 ruling 3 where the texts leave it
    unpinned: the entry discharges the bar where every
    affected class in the required set stands named in the
    entry affected classes, the required set standing as
    the affected classes the caller passes or, where the
    caller passes none, the eight classes of this section
    tuple, and where the entry checks run stand non empty
    with a result standing for each check run, the result
    collection length equal to the checks run length and
    every result truthy. In every other case the bar
    stands in the same three key form, with
    change_passed_as_no_change standing False in every
    return of this act.
    """
    if not isinstance(entry, dict):
        return {
            "discharged": False,
            "bar_stands": True,
            "change_passed_as_no_change": False,
        }
    if affected_classes is None:
        required = list(_AFFECTED_CLASSES)
    else:
        required = list(affected_classes)
    covered = entry.get("affected_classes") or []
    checks = entry.get("checks_run") or []
    results = entry.get("result_of_each_check") or []
    try:
        result_values = list(results.values())
    except AttributeError:
        result_values = list(results)
    discharged = (
        all(name in covered for name in required)
        and len(checks) > 0
        and len(results) == len(checks)
        and all(result_values)
    )
    return {
        "discharged": discharged,
        "bar_stands": not discharged,
        "change_passed_as_no_change": False,
    }


def loop_report_classification(entry):
    """Return the loop report printed form for an entry.

    The printed form stands by pointer only, in the form
    MeaningChangeRecordTests pins and plan subsection
    19.101 point three closes with: a mapping carrying
    form equal to pointer and points_to equal to the entry
    identity it is passed, and no classification text of
    its own, the classification standing in the entry, in
    the suite result record, and nowhere in this printed
    form as its home. The entry stands read by its one
    stated key, entry_identity, and no other key of it
    stands read by this act.
    """
    return {"form": "pointer", "points_to": entry["entry_identity"]}


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
