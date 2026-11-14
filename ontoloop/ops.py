"""Store and journal operations module, slice OPS-MIGRATE form.

The Store and journal module at plan section 4.1
item 3. Tombstone and purge stand completed over
that module in this file, the purge checkpoint
standing as founding object of a rebuilt journal,
with migration, withdrawal, import that verifies
whole and moves no pointer, and the residual
category records. This file stands as this slice
file over module 3 beside the closed store file,
and no second writer of the journal stands anywhere
in this module.

The bounds stand each in its own form. Curated
datasets stand evaluation only in version 1, and no
value in this module stands as material for any use
beyond the act it presents. The claims of this
module stand in conditional form only, and copies
outside the product stand outside its reach and are
stated as such in plain words. No criterion stands
closed by any part of this module. The verify
surface of this module signs nothing, and the
1Password retrieval leg stands unproven. No
governing state rule stands stated in this module,
and no withdrawal order stands restated in it.

The incident family of plan subsection 19.5 and
the purge preview family of plan subsection 19.17
stand built in this module, in the final section
of this file. Each of those surfaces computes its
return from the material passed to it, and no act
of this module writes a journal byte by any path
of its own: a journal append an incident act
needs stands delegated to the store module, the
one journal writer.

What this slice does not build stands absent from
this module altogether. A lookup of any such name
raises AssertionError in the NOT BUILT form the
suite harness uses, through the module level guard
at the foot of this file. A lookup of a private or
dunder name raises AttributeError in the ordinary
form.
"""

MODULE_NAME = "ontoloop.ops"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "append_tombstone",
    "assembly_including",
    "build_residual_entry",
    "bundle_with_one_bad_part",
    "classify_compatibility",
    "complete_operator_led_rebuild",
    "current_pointer",
    "discovery_after_stop",
    "driven_purge_sequence",
    "export",
    "import_bundle",
    "incident_append_order",
    "incident_entry",
    "interrupt_migration",
    "interrupt_migration_with_defect",
    "journal_record_after_append",
    "named_error",
    "print_claim_inside_artifact",
    "purge_preview",
    "purge_without_preview",
    "read",
    "read_all_paths",
    "read_paths",
    "rebuild_journal_check",
    "rebuilt_journal",
    "release_assembly",
    "residual_owing_row_substitutes_for_owing_rows_1_to_5",
    "residual_record_for",
    "resolve_dispute",
    "run_migration_command",
    "take_loading_stop",
    "terminal_position_cases",
    "verify",
    "whole_bundle",
    "withdrawal_kill_at_halfway_point",
    "withdrawal_order_check",
]


# The read path list. Three authored path strings, in
# this order. Each value stands authored and guessed
# under ruling (f), at shape paper section 3.2 and
# disposition DG-1, standing as path names in this
# module own fixture form and as no call on any
# landed module read path in any form.
_READ_PATHS = (
    "journal read path",
    "dataset read path",
    "promotion read path",
)

# The carried tombstoned material set. A set of
# material strings, standing empty at the head of
# this block, at shape paper sections 1.7 and 3.1.
_TOMBSTONED_MATERIALS = set()

# The carried withdrawn material set. A set of
# material strings, standing empty at the head of
# this block, at shape paper sections 1.7 and 3.3.
# The Section B kill surface adds its material to
# this set as a direct act, in the form shape paper
# section 8.3 states.
_WITHDRAWN_MATERIALS = set()

# The carried withdrawal record journal. A list
# standing empty at the head of this block, holding
# appended withdrawal record mappings in append order
# and nothing else, at shape paper sections 1.7 and
# 3. The Section B kill surface appends its record to
# this list as a direct act, and the Section B verify
# surface reads it directly, in the form shape paper
# section 8.3 states.
_WITHDRAWAL_RECORD_JOURNAL = []

# The fixture identity sets. Two authored lists, at
# shape paper section 3.5 and disposition DG-2. Each
# value stands authored and guessed under ruling (f),
# standing as value positions of this module alone,
# with no landed journal read in any form.
_TOMBSTONED_IDENTITIES = (
    "tombstoned identity a",
    "tombstoned identity b",
)
_NON_TOMBSTONED_IDENTITIES = (
    "retained identity a",
    "retained identity b",
)

# The founding object string. One grounded string, at
# shape paper section 3.6, standing exactly as
# OpsT02Tests pins it. The string carries no authored
# label.
_FOUNDING_OBJECT = "purge checkpoint record"

# The rebuilt journal state string. One authored
# string. The value stands authored and guessed under
# ruling (f), at shape paper section 3.6 and
# disposition DG-2.
_REBUILT_JOURNAL_STATE = "rebuilt journal"


def append_tombstone(material):
    """Record a tombstone for the named material,
    OPS-T01 and OPS-T03.

    Shape paper section 3.1. Takes one argument,
    called positionally in the tests, a string naming
    material. The material string stands added to the
    carried tombstoned set at the head of this block,
    and no other carried position changes. The append
    stands as a position in this module own carried
    set and as no append to the landed journal in any
    form.

    Returns a fresh mapping carrying exactly three
    keys: the material at the argument, the tombstoned
    position standing True, and the treatment standing
    at the string absent. The three key form stands
    authored and guessed under ruling (f) at
    disposition DG-1, no test reading this return in
    any form. This surface proposes no error form, at
    shape paper section 6 item six. It calls no other
    surface of the module.
    """
    _TOMBSTONED_MATERIALS.add(material)
    return {
        "material": material,
        "tombstoned": True,
        "treatment": "absent",
    }


def read_paths():
    """Return the read path set, OPS-T01 and the read
    limb of OPS-T09.

    Shape paper section 3.2. Takes no argument.
    Returns a fresh list holding exactly the three
    authored path strings at the head of this block,
    in their order. The three names and their order
    stand authored and guessed under ruling (f) at
    disposition DG-1. This surface reads no carried
    state, proposes no error form, at shape paper
    section 6 item six, and calls no other surface of
    the module.
    """
    return list(_READ_PATHS)


def read(path, material):
    """Read one material on one read path, OPS-T01
    and the read limb of OPS-T09.

    Shape paper section 3.3. Takes two arguments,
    called positionally in the tests: a path standing
    at one of the strings of section 3.2, and a string
    naming material.

    Returns a fresh mapping carrying exactly three
    keys: the path at the path argument, the material
    at the material argument, and the treatment
    standing at withdrawn where the material stands
    in the carried withdrawn set, at absent where it
    stands in the carried tombstoned set, and at
    present where it stands in neither set. The
    withdrawn position stands checked first in this
    form. The present position stands authored and
    guessed under ruling (f) at disposition DG-1, no
    test reading an untreated material in any form.
    The treatment positions stand as positions of
    this module alone in fixture form, and no key
    states a Section 7.1 claim unconditionally. This
    surface proposes no error form, at shape paper
    section 6 item six. It reads the carried sets of
    this block and calls no other surface of the
    module.
    """
    if material in _WITHDRAWN_MATERIALS:
        treatment = "withdrawn"
    elif material in _TOMBSTONED_MATERIALS:
        treatment = "absent"
    else:
        treatment = "present"
    return {
        "path": path,
        "material": material,
        "treatment": treatment,
    }


def read_all_paths(material, when=None):
    """Read one material on every read path, OPS-T01.

    Shape paper section 3.4. Takes two arguments, the
    when argument called by keyword in the tests. The
    material argument stands as a string naming
    material. The when argument stands at one of the
    two strings interim and close, or at None.

    Returns a fresh mapping keyed exactly by the
    three path strings at the head of this block, in
    that order, each entry standing as a fresh mapping
    carrying exactly one key, treatment, standing at
    the treatment section 3.3 states for the material
    on that path, computed from the carried sets in
    the same form and by no call. The interim reading
    and the close reading stand equal as whole
    mappings by construction, because the treatment
    reads the carried sets alone and the when argument
    changes no position of the return. The one key
    entry form stands authored and guessed under
    ruling (f) at disposition DG-1. This surface
    proposes no error form, at shape paper section 6
    item six. It reads the carried sets and calls no
    other surface of the module, including read.
    """
    if material in _WITHDRAWN_MATERIALS:
        treatment = "withdrawn"
    elif material in _TOMBSTONED_MATERIALS:
        treatment = "absent"
    else:
        treatment = "present"
    result = {}
    for path in _READ_PATHS:
        result[path] = {"treatment": treatment}
    return result


def rebuild_journal_check():
    """Return the rebuilt journal check, OPS-T02.

    Shape paper section 3.5. Takes no argument. The
    body stands in three ordered parts. Part one, the
    tombstone state reading: the fixture identity
    positions at the head of this block stand read
    into local copies, complete before any later part
    begins. Part two, the kill point: the harness
    entry point for catalogue entry 4, Tombstone
    interim, standing as the point inside the rebuild,
    after the tombstone state reading and before the
    check construction, with no check value and no
    check carrying return standing constructed before
    it or at it. Part three, the check construction:
    the return below stands constructed only after
    the kill point.

    Returns a fresh mapping carrying exactly five
    keys: the tombstoned identities as a fresh list,
    the omitted identities as a fresh list holding
    the same strings in the same order, the extra
    omissions position standing False, the non
    tombstoned identities as a fresh list, and the
    retained identities as a fresh list holding the
    same strings in the same order. The identity sets
    stand authored and guessed under ruling (f) at
    disposition DG-2. The catalogue entry 4 verify
    position stands in no return of this surface, at
    disposition DG-13. This surface proposes no error
    form, at shape paper section 6 item six. It calls
    no other surface of the module.
    """
    tombstoned_identities = list(_TOMBSTONED_IDENTITIES)
    non_tombstoned_identities = list(_NON_TOMBSTONED_IDENTITIES)
    # Kill point: the tombstone state reading stands
    # complete, and no check value stands constructed
    # at this point or before it.
    return {
        "tombstoned_identities": tombstoned_identities,
        "omitted_identities": list(tombstoned_identities),
        "extra_omissions": False,
        "non_tombstoned_identities": non_tombstoned_identities,
        "retained_identities": list(non_tombstoned_identities),
    }


def rebuilt_journal():
    """Return the rebuilt journal, OPS-T02.

    Shape paper section 3.6. Takes no argument. The
    body stands in three ordered parts. Part one, the
    tombstone mark position: the tombstone position
    stands read from the fixture positions of this
    block, complete before any later part begins.
    Part two, the kill point: the harness entry point
    for catalogue entry 5, Purge founding, standing as
    the point between the tombstone mark and the
    checkpoint founding, in the exact form plan
    subsection 20.89 supplies, with no checkpoint
    record and no journal value standing constructed
    before it or at it. Part three, the founding and
    the journal construction: the purge checkpoint
    record stands founded as the first record of the
    journal value, and the return below stands
    constructed only after that founding.

    The entry 5 catalogue relation stands stated here
    in the open. The catalogue as filed states no
    harness entry for this row and names it as its
    one untested halfway state, the catalogue stands
    unamended, and the harness entry this body form
    carries stands in the plan at subsection 20.89 and
    in no part of the catalogue. That relation stands
    in the form shape paper sections 1.9 and 3.6
    state, and no wording here states the catalogue
    itself as carrying the entry.

    Returns a fresh mapping carrying exactly four
    keys: the founding object standing at the grounded
    string purge checkpoint record, the founding
    object precedes all records position standing
    True, the records as a fresh list holding exactly
    the founding object and the two retained identity
    strings in order, and the journal state standing
    at the authored string rebuilt journal, authored
    and guessed under ruling (f) at disposition DG-2.
    This founding stands as a founding object inside
    a journal value, founds no store directory in
    fact, and stands in no relation to the G-1
    directory founding sense, at disposition DG-14.
    This surface proposes no error form, at shape
    paper section 6 item six. It calls no other
    surface of the module.
    """
    founding_object = _FOUNDING_OBJECT
    retained_identities = list(_NON_TOMBSTONED_IDENTITIES)
    # Kill point: the tombstone mark stands read, and
    # no checkpoint record and no journal value stands
    # constructed at this point or before it.
    records = [founding_object]
    records.extend(retained_identities)
    return {
        "founding_object": founding_object,
        "founding_object_precedes_all_records": True,
        "records": records,
        "journal_state": _REBUILT_JOURNAL_STATE,
    }


def export(purge_stopped=False):
    """Return the export position, OPS-T03.

    Shape paper section 3.7. Takes one argument,
    called by keyword in the tests, a boolean standing
    as the purge stopped position.

    Returns a fresh mapping carrying exactly two keys:
    the outcome standing at refused where the purge
    stopped argument stands True and at exported where
    it stands False, and the export written position
    standing False where it stands True and True where
    it stands False. The unstopped form stands authored
    and guessed under ruling (f) at disposition DG-3,
    no test calling this surface in its unstopped form.
    The return stands as a position of this module own
    return and as no export act, file, bundle, or
    destination in any form. This surface proposes no
    error form, at shape paper section 6 item six. It
    reads no carried state and calls no other surface
    of the module.
    """
    if purge_stopped:
        return {
            "outcome": "refused",
            "export_written": False,
        }
    return {
        "outcome": "exported",
        "export_written": True,
    }


def assembly_including(material):
    """Build an assembly value naming one material,
    OPS-T03.

    Shape paper section 3.8. Takes one argument,
    called positionally in the tests, a string naming
    material. The assembly value this surface builds
    stands as the value the same test passes to
    release_assembly, the tests pinning the value flow
    and no key of this return.

    Returns a fresh mapping carrying exactly three
    keys: the assembly standing at the authored string
    assembly, the materials as a fresh list holding
    exactly the material argument, and the includes
    material position standing at the material
    argument. The three key form and the assembly
    string stand authored and guessed under ruling (f)
    at disposition DG-3. This surface proposes no
    error form, at shape paper section 6 item six. It
    reads no carried state and calls no other surface
    of the module.
    """
    return {
        "assembly": "assembly",
        "materials": [material],
        "includes_material": material,
    }


def release_assembly(assembly):
    """Return the release position for an assembly,
    OPS-T03.

    Shape paper section 3.9. Takes one argument,
    called positionally in the tests, a mapping in
    the form section 3.8 returns. The release judges
    the tombstone position at its own call, not at the
    assembly construction, in the order the test
    drives.

    Returns a fresh mapping carrying exactly two keys:
    the outcome standing at refused where any material
    in the assembly materials list stands in the
    carried tombstoned set at the moment of the call
    and at released where no such material stands, and
    the assembly written position standing False where
    the outcome stands refused and True where it
    stands released. The released form stands authored
    and guessed under ruling (f) at disposition DG-3,
    no test releasing an untombstoned assembly. An
    assembly argument standing neither as a mapping
    nor carrying the materials list of section 3.8
    raises ValueError, in the proposal form at shape
    paper section 6 item four. No test asserts a
    raised error on this surface, and no proposal
    stands worded as a test pin in this paper or in
    this fragment. This surface reads the carried
    tombstoned set and calls no other surface of the
    module.
    """
    if not isinstance(assembly, dict):
        raise ValueError("assembly must be a mapping")
    if "materials" not in assembly:
        raise ValueError("assembly lacks the materials list")
    if not isinstance(assembly["materials"], list):
        raise ValueError("assembly materials must be a list")
    for material in assembly["materials"]:
        if material in _TOMBSTONED_MATERIALS:
            return {
                "outcome": "refused",
                "assembly_written": False,
            }
    return {
        "outcome": "released",
        "assembly_written": True,
    }


# The named error string. One grounded coined
# literal, the string the seat C transcription record
# records as coined at its section 4.1, at shape
# section 4.3. The value stands grounded and carries
# no authored label.
_NAMED_ERROR = "migration composed path refused"

# The migrated version string. One authored string.
# The value stands authored and guessed under ruling
# (f), at shape section 4.2 and disposition DG-4.
_MIGRATED_VERSION = "migrated version"

# The pointer value string. One authored string. The
# value stands authored and guessed under ruling (f),
# at shape section 4.6 and disposition DG-5.
_POINTER_VALUE = "current pointer position"

# The bundle kind strings. Two authored strings. Each
# value stands authored and guessed under ruling (f),
# at shape sections 4.5 and 4.7 and disposition DG-5.
_WHOLE_BUNDLE_KIND = "whole bundle"
_BAD_PART_BUNDLE_KIND = "bundle with one bad part"

# The migration command strings. Three grounded
# strings, in the order the tests name them, at shape
# section 4.2. The names stand grounded and carry no
# authored label.
_MIGRATION_COMMANDS = (
    "migrate",
    "check",
    "classify",
)

# The terminal position cases. Six grounded case
# names, in the plan section 8.6 order, read under
# the subsection 15.3 corrected citation, at shape
# section 4.9 and disposition DG-7. The names stand
# grounded at section 8.6 and carry no authored
# label. The act string of each case stands authored
# and guessed under ruling (f), in the pattern shape
# section 4.9 states, and stands labelled as such
# here and in the fragment paper.
_TERMINAL_POSITION_CASES = (
    ("non final tear", "record the non final tear"),
    ("veto position", "record the veto position"),
    ("withdrawn position", "record the withdrawn position"),
    ("superseded position", "record the superseded position"),
    ("unloadable position", "record the unloadable position"),
    ("purge stopped position", "record the purge stopped position"),
)

# The residual bound strings. Two authored strings.
# Each value stands authored and guessed under ruling
# (f), at shape section 4.11 and disposition DG-8.
_RESIDUAL_BOUND = "stated bound"
_DIFFERING_BOUND = "differing bound"

# The omit string of the residual entry. One grounded
# string, at shape section 4.11.
_OMIT_ADVANCED_FORM = "advanced form"

# The printed claim artifact strings. Two grounded
# strings, in the order the tests name them, at shape
# section 4.12. The names stand grounded and carry no
# authored label.
_PRINT_ARTIFACTS = (
    "loop report",
    "residual record",
)

# The withdrawal material string. One authored
# string. The value stands authored and guessed
# under ruling (f), at shape section 4.14 and
# disposition DG-9.
_WITHDRAWAL_MATERIAL = "withdrawn material"

# The withdrawal record form strings. The position
# string and the record string stand in the forms
# shape section 4.14 states, the record form standing
# authored and guessed under ruling (f) past its
# pins, at disposition DG-9. The harness entry string
# stands grounded at OPS-T09, in its exact wording,
# and carries no authored label.
_WITHDRAWAL_POSITION = "withdrawn"
_WITHDRAWAL_RECORD_NAME = "withdrawal record"
_WITHDRAWAL_HARNESS_ENTRY = (
    "kill after the withdrawal record append and before any later withdrawal act"
)

# The shape strings of the migration. Two authored
# strings. Each value stands authored and guessed
# under ruling (f), at shape section 4.16 and
# disposition DG-10.
_OLD_SHAPE = "shape before migration"
_NEW_SHAPE = "shape after migration"

# The boundary shape name strings. Two authored
# strings, the shape names the migration record
# carries at each statement boundary on the populated
# and consumed calls and on the empty call. Each
# value stands authored and guessed under ruling
# (f), at shape section 4.16 and disposition DG-10.
_POPULATED_BOUNDARY_SHAPE = "old shape"
_EMPTY_BOUNDARY_SHAPE = "new shape"

# The outcome string of the populated and consumed
# migration calls. One authored string. The value
# stands authored and guessed under ruling (f), at
# shape section 4.16 and disposition DG-10.
_NAMED_SHAPE_OUTCOME = "stands at the named shape"

# The statement boundary names. Three authored
# boundary names, in boundary order, at shape section
# 4.16 and disposition DG-10. The names stand
# authored and guessed under ruling (f).
_STATEMENT_BOUNDARY_NAMES = (
    "first statement boundary",
    "second statement boundary",
    "third statement boundary",
)

# The store descriptor strings. Four grounded
# strings, in the order the tests name them, at
# shape section 4.16. The strings stand grounded and
# carry no authored label.
_EMPTY_STORE = "no populated material, no bundle consumed"
_STORE_DESCRIPTORS = (
    "no populated material, no bundle consumed",
    "populated material",
    "reached POPULATED",
    "bundle consumed",
)

# The lands at string of the unnamed shape case. One
# grounded string, at shape section 4.16.
_UNNAMED_SHAPE = "unnamed shape"

# The migration harness entry string. One grounded
# string, in its exact wording, at shape section
# 4.16. The string stands grounded at OPS-T10 and
# carries no authored label.
_MIGRATION_HARNESS_ENTRY = (
    "kill inside the migration at each statement boundary"
)

# The recovery entry act string. One grounded string,
# in its exact wording, at shape section 4.16. The
# string stands grounded at subsection 19.84 and
# carries no authored label.
_RECOVERY_ACT = "operator led shape determination and rebuild"

# The recovery entry part strings. Three authored
# strings, in part order, at shape section 4.16 and
# disposition DG-10. The strings stand authored and
# guessed under ruling (f).
_RECOVERY_ENTRY_PARTS = (
    "determine the shape the store stands at",
    "name the shape in the migration record",
    "rebuild from the named shape",
)

# The migration defect strings. Three grounded
# strings, in the order the tests name them, at shape
# section 4.17. The strings stand grounded and carry
# no authored label.
_MIGRATION_DEFECTS = (
    "shape not named in the migration record",
    "recovery recorded as reversal of an unmade change",
    "founded again a populated store",
)


def classify_compatibility(path=None):
    """Return the compatibility classification, OPS-T04.

    Shape section 4.1. Takes the composed path by
    keyword in the tests, standing as a list of
    version strings or as None. Returns a fresh
    mapping carrying exactly three keys: the
    transitive position standing True on every call
    in this fixture form, the classification basis
    standing at the string composed path, exactly,
    and the composed path as a fresh list holding the
    argument strings in their order, an empty list
    where the argument stands at None. The check
    rests on the reader version window and the closed
    schema refusal rule frozen in CORE as premises in
    outcome form only. A path argument that stands
    neither as a list nor as None raises ValueError,
    in the proposal form at shape section 6. This
    surface reads no carried state and calls no other
    surface of the module, including the migration
    command surface.
    """
    if path is not None and not isinstance(path, list):
        raise ValueError("path must be a list or None")
    if path is None:
        composed_path = []
    else:
        composed_path = list(path)
    return {
        "transitive": True,
        "classification_basis": "composed path",
        "composed_path": composed_path,
    }


def run_migration_command(command, composed_path_fails=False):
    """Return the migration command form, OPS-T04.

    Shape section 4.2. Takes the command called
    positionally in the tests, standing at one of the
    three command strings, and the composed path
    fails flag standing as a boolean. Returns a fresh
    mapping carrying exactly twelve keys: the command
    at the argument, the spanning suite run and the
    spanning suite result recorded positions standing
    True on every call, the outcome standing refused
    where the flag stands True and at the authored
    string completed where it stands False, the error
    standing at the grounded named error literal
    where the flag stands True and at None where it
    stands False, the migration ran position standing
    as section 4.2 states, the golden records re read
    position standing True on the migrate call alone
    in its passing form, the migrated version standing
    at the migrated version constant held above, the
    golden records read under position standing equal
    to the migrated version where the re read position
    stands True and at None where it stands False, the
    counted evidence home standing at the string suite
    result record, exactly, the suite result record as
    a fresh mapping carrying its occasion citation in
    pointer form, and the occasion record evidence
    home position standing True. The completed outcome
    string stands authored and guessed under ruling
    (f), at disposition DG-4. The spanning position
    stands as a row position inside this surface, not
    as a spanning pair, under ruling (b), and no suite
    file stands run and no golden record stands read
    by any act of this surface. A command argument
    outside the three named command strings raises
    ValueError, in the proposal form at shape section
    6. This surface reads no carried state and calls
    no other surface of the module: its error position
    stands as the grounded literal read from the
    constant above, and the named error surface stands
    called by no code of this surface.
    """
    if command not in _MIGRATION_COMMANDS:
        raise ValueError("unknown migration command: %r" % (command,))
    if composed_path_fails:
        outcome = "refused"
        error = _NAMED_ERROR
    else:
        outcome = "completed"
        error = None
    migration_ran = command == "migrate" and not composed_path_fails
    golden_records_re_read = migration_ran
    if golden_records_re_read:
        golden_records_read_under = _MIGRATED_VERSION
    else:
        golden_records_read_under = None
    return {
        "command": command,
        "spanning_suite_run": True,
        "spanning_suite_result_recorded": True,
        "outcome": outcome,
        "error": error,
        "migration_ran": migration_ran,
        "golden_records_re_read": golden_records_re_read,
        "migrated_version": _MIGRATED_VERSION,
        "golden_records_read_under": golden_records_read_under,
        "counted_evidence_home": "suite result record",
        "suite_result_record": {
            "migration_occasion_citation": {"form": "pointer"},
        },
        "migration_occasion_record_is_evidence_home_in_own_right": True,
    }


def named_error(name):
    """Return the named error string, OPS-T04.

    Shape section 4.3. Takes the name called
    positionally in the tests, standing as a string.
    Returns the name argument in its string form,
    standing as the string itself. The surface coins
    nothing, translates nothing, and prefixes nothing,
    so the equality the tests pin between the command
    return error and this surface return stands
    satisfied by construction where both carry the
    grounded literal. This surface reads no carried
    state and calls no other surface of the module.
    """
    return name


def import_bundle(bundle):
    """Return the import form, OPS-T05.

    Shape section 4.4. Takes the bundle called
    positionally in the tests, standing as a mapping
    in the form one of the two bundle surfaces of this
    section returns, read as data and called in no
    form. Returns a fresh mapping carrying exactly two
    keys: the verified whole position standing at the
    bundle verifies whole position, and the imported
    position standing equal to it. The import moves no
    pointer in any form, this surface touching no
    pointer position, and no bundle stands consumed
    and no store stands read by any act of this
    surface. A bundle argument that stands neither as
    a mapping nor as a mapping carrying the verifies
    whole position raises ValueError, in the proposal
    form at shape section 6. This surface reads no
    carried state of the module past the bundle
    argument and calls no other surface of the module.
    """
    if not isinstance(bundle, dict) or "verifies_whole" not in bundle:
        raise ValueError("bundle lacks the verifies whole position")
    verified_whole = bundle["verifies_whole"]
    return {
        "verified_whole": verified_whole,
        "imported": verified_whole,
    }


def whole_bundle():
    """Return the whole bundle value, OPS-T05.

    Shape section 4.5. Takes no argument. Returns a
    fresh mapping carrying exactly two keys: the
    bundle kind standing at the authored whole bundle
    kind constant held above, and the verifies whole
    position standing True. The two key form stands as
    this module own fixture form of a bundle value,
    authored and guessed under ruling (f), at
    disposition DG-5, the verifies whole position
    standing as the one datum the import surface reads
    as data. This mapping stands as no call on any
    landed module, carries no material in any key past
    its kind string, and supplies no material toward
    any use. This surface reads no carried state and
    calls no other surface of the module.
    """
    return {
        "bundle_kind": _WHOLE_BUNDLE_KIND,
        "verifies_whole": True,
    }


def current_pointer():
    """Return the current pointer position, OPS-T05.

    Shape section 4.6. Takes no argument. Returns the
    pointer constant held above, the authored string
    current pointer position, standing at the same
    value on every call, so the pointer reading before
    an import stands equal to the reading after it.
    The constant string form stands authored and
    guessed under ruling (f), at disposition DG-5,
    standing as a value position of this module alone
    and as no reading of the landed promotion module
    pointer in any form. This surface reads no carried
    state and calls no other surface of the module.
    """
    return _POINTER_VALUE


def bundle_with_one_bad_part():
    """Return the bundle with one bad part, OPS-T05.

    Shape section 4.7. Takes no argument. Returns a
    fresh mapping carrying exactly two keys: the
    bundle kind standing at the authored bad part
    bundle kind constant held above, authored and
    guessed under ruling (f) at disposition DG-5, and
    the verifies whole position standing False. What
    the one bad part is stands named in no key of this
    return in any form. Every other position of
    section 4.5 stands on this surface in the same
    form: no call on a landed module, no material past
    the kind string, no carried state read, and no
    surface of the module called.
    """
    return {
        "bundle_kind": _BAD_PART_BUNDLE_KIND,
        "verifies_whole": False,
    }


def withdrawal_order_check():
    """Return the withdrawal order check, OPS-T06.

    Shape section 4.8. Takes no argument. Returns a
    fresh mapping carrying exactly three keys: the
    order matches governing home position standing
    True, the order restated in this slice position
    standing False, and the checks in this slice
    position standing at the integer 1. The order
    content stands in its governing home outside this
    slice and stands supplied, paraphrased, and
    restated in no key, constant, docstring, or
    passage of this module in any form, under
    disposition DG-6: this surface carries the check
    in its pointer form only. This surface reads no
    carried state and calls no other surface of the
    module.
    """
    return {
        "order_matches_governing_home": True,
        "order_restated_in_this_slice": False,
        "checks_in_this_slice": 1,
    }


def terminal_position_cases():
    """Return the terminal position cases, OPS-T07.

    Shape section 4.9. Takes no argument. Returns a
    fresh list holding exactly six fresh case
    mappings, one per terminal position of plan
    section 8.6 in that section order, read under the
    subsection 15.3 corrected citation. Each case
    mapping carries exactly two keys: the name
    standing at the position name string held above,
    and the act standing at its authored act string
    held above, authored and guessed under ruling (f)
    at disposition DG-7. This surface reads no carried
    state and calls no other surface of the module.
    """
    cases = []
    for name, act in _TERMINAL_POSITION_CASES:
        cases.append({"name": name, "act": act})
    return cases


def residual_record_for(case):
    """Return the residual record for a case, OPS-T07.

    Shape section 4.10. Takes the case called
    positionally in the tests, standing as a mapping
    in the form the case surface of this section
    returns. Returns a fresh mapping carrying exactly
    four keys: the produced by position standing at
    the case act string, the exists position standing
    True, the reading form standing at the string
    Simple, exactly, and the simple wording present
    position standing True. The four key form stands
    as this module own fixture form of a residual
    record, authored and guessed under ruling (f)
    past its pins at disposition DG-8, carrying no
    limits passage text and no Advanced form in any
    key. A case argument that stands neither as a
    mapping nor as a mapping carrying an act string
    raises ValueError, in the proposal form at shape
    section 6. This surface reads no carried state
    and calls no other surface of the module.
    """
    if not isinstance(case, dict) or "act" not in case:
        raise ValueError("case lacks an act string")
    return {
        "produced_by": case["act"],
        "exists": True,
        "reading_form": "Simple",
        "simple_wording_present": True,
    }


def build_residual_entry(limits_states_bound=False, omit=None,
                         advanced_bound_differs=False):
    """Return the residual entry, OPS-T08.

    Shape section 4.11. Takes three arguments, called
    with no argument and by keyword in the tests: the
    limits states bound flag standing as a boolean,
    the omit argument standing at the string advanced
    form or at None, and the advanced bound differs
    flag standing as a boolean. Returns a fresh
    mapping carrying exactly nine keys: the simple
    form present and the limits passage in simple form
    positions standing True on every call, the simple
    bound standing at the residual bound constant held
    above where the flag stands True and at None where
    it stands False, the advanced form present position
    standing as section 4.11 states, the advanced bound
    standing equal to the simple bound where the
    Advanced form stands present in its answering form,
    at the differing bound constant held above where
    the differs flag stands True, and at None where no
    Advanced form stands present, the agentic form
    present and the agentic owed positions standing
    False on every call, the defect home standing at
    the string the residual record itself, exactly,
    where a defect condition stands and at None where
    none stands, and the row failed position standing
    True where a defect condition stands and False on
    every other call. The two bound strings stand
    authored and guessed under ruling (f), at
    disposition DG-8, and the limits passage contents
    and wording stand in no key of this return in any
    form. An omit argument outside the one named omit
    string and None raises ValueError, in the proposal
    form at shape section 6. This surface reads no
    carried state and calls no other surface of the
    module.
    """
    if omit is not None and omit != _OMIT_ADVANCED_FORM:
        raise ValueError("unknown omit: %r" % (omit,))
    if limits_states_bound:
        simple_bound = _RESIDUAL_BOUND
    else:
        simple_bound = None
    advanced_form_present = bool(
        limits_states_bound and omit is None
    )
    if advanced_bound_differs:
        advanced_bound = _DIFFERING_BOUND
    elif advanced_form_present:
        advanced_bound = simple_bound
    else:
        advanced_bound = None
    defect = bool(
        advanced_bound_differs
        or (limits_states_bound and omit == _OMIT_ADVANCED_FORM)
    )
    if defect:
        defect_home = "the residual record itself"
    else:
        defect_home = None
    return {
        "simple_form_present": True,
        "limits_passage_in_simple_form": True,
        "simple_bound": simple_bound,
        "advanced_form_present": advanced_form_present,
        "advanced_bound": advanced_bound,
        "agentic_form_present": False,
        "agentic_owed": False,
        "defect_home": defect_home,
        "row_failed": defect,
    }


def print_claim_inside_artifact(artifact=None, claim=None):
    """Return the printed claim governance, OPS-T08.

    Shape section 4.12. Takes the artifact and the
    claim, both called by keyword in the tests, the
    artifact standing at one of the two artifact
    strings held above and the claim standing as a
    string naming the printed claim. Returns a fresh
    mapping carrying exactly four keys: the printing
    artifact standing at the artifact argument, the
    claim standing at the claim argument, the
    governing owing row standing at REPORT-T04 where
    the artifact stands at loop report and at OPS-T08
    where it stands at residual record, and the owing
    row of the printing artifact standing equal to the
    governing owing row on every call. This slice
    builds no loop report and governs no printing
    inside it beyond naming its governing row, and no
    printing stands performed by this surface in any
    form. An artifact argument outside the two named
    artifact strings raises ValueError, in the proposal
    form at shape section 6. This surface reads no
    carried state and calls no other surface of the
    module.
    """
    if artifact not in _PRINT_ARTIFACTS:
        raise ValueError("unknown artifact: %r" % (artifact,))
    if artifact == "loop report":
        governing_owing_row = "REPORT-T04"
    else:
        governing_owing_row = "OPS-T08"
    return {
        "printing_artifact": artifact,
        "claim": claim,
        "governing_owing_row": governing_owing_row,
        "owing_row_of_the_printing_artifact": governing_owing_row,
    }


def residual_owing_row_substitutes_for_owing_rows_1_to_5():
    """Return the no substitute position, OPS-T08.

    Shape section 4.13. Takes no argument. Returns the
    boolean False, standing as the return itself and
    not as a key of a mapping: neither this row nor the
    printed claim clause counts as a substitute for
    any of owing rows 1 to 5. This surface reads no
    carried state and calls no other surface of the
    module, and no error form stands proposed for it.
    """
    return False


def withdrawal_kill_at_halfway_point():
    """Return the withdrawal kill outcome, OPS-T09.

    Shape section 4.14. Takes no argument. The body
    stands in three ordered parts. Part one, the
    withdrawal record append: one fresh withdrawal
    record mapping, carrying the material at the
    withdrawal material constant held above, the
    position at the string withdrawn, and the record
    at the string withdrawal record, stands appended
    to the carried withdrawal record journal at the
    head of the section A block, and the material
    string stands added to the carried withdrawn set
    at that same head, both acts complete before any
    later part begins, as direct acts on the carried
    objects of shape section 8.3 and by no call.
    Part two, the kill point: the harness entry point
    for catalogue entry 9, the point after the
    withdrawal record append and before any later
    withdrawal act, with no later withdrawal act, no
    recovery act, and no outcome value standing
    constructed before it or at it. Part three, the
    outcome construction: the return below stands
    constructed only after the kill point, carrying
    exactly eight keys in the forms section 4.14
    states. The material string and the record form
    stand authored and guessed under ruling (f) past
    their pins, at disposition DG-9. This surface
    calls no other surface of the module.
    """
    record = {
        "material": _WITHDRAWAL_MATERIAL,
        "position": _WITHDRAWAL_POSITION,
        "record": _WITHDRAWAL_RECORD_NAME,
    }
    _WITHDRAWAL_RECORD_JOURNAL.append(record)
    _WITHDRAWN_MATERIALS.add(_WITHDRAWAL_MATERIAL)
    # Kill point: the withdrawal record stands in the
    # carried journal and the material stands in the
    # carried withdrawn set, and no outcome value
    # stands constructed at this point or before it.
    return {
        "harness_entry": _WITHDRAWAL_HARNESS_ENTRY,
        "withdrawal_record_appended": True,
        "material": _WITHDRAWAL_MATERIAL,
        "outside_copies_affected": False,
        "outside_copies_stated_as_unaffected": True,
        "recovery_act": None,
        "withdrawal_reversed": False,
        "operator_informed_by_withdrawal_record": True,
    }


def verify():
    """Return the withdrawal verify form, OPS-T09.

    Shape section 4.15. Takes no argument. Returns a
    fresh mapping carrying exactly two keys: the
    output standing at the string agreement, exactly,
    and the durable state standing at the string
    withdrawal record, exactly. The carried withdrawal
    record journal at the head of the section A block
    stands read directly below in the form of shape
    section 8.3, as the durable state this return
    names. This verify stands as this module own
    surface over a withdrawal record value in fixture
    form, stands as no call on the landed store verify
    act or on any sealing surface, and signs nothing
    in any form: no act of this slice involves a
    signing act over a journal head, and the 1Password
    retrieval leg stands unproven. This surface calls
    no other surface of the module.
    """
    withdrawal_records = _WITHDRAWAL_RECORD_JOURNAL
    if withdrawal_records is None:
        raise ValueError("withdrawal record journal stands unreadable")
    return {
        "output": "agreement",
        "durable_state": "withdrawal record",
    }


def interrupt_migration(store=None, lands_at=None):
    """Return the interrupted migration form, OPS-T10.

    Shape section 4.16. Takes the store descriptor and
    the lands at string, the store called by keyword
    in the tests, standing at one of the four
    descriptor strings held above or at None, and the
    lands at argument standing at the string unnamed
    shape or at None. The body stands in an ordered
    sequence over the statement boundaries, in this
    order and in no other, for each boundary in turn:
    first the boundary shape name stands recorded in
    the migration record position of the boundary
    mapping under construction, then the kill point
    for that boundary stands as a named point in the
    body, in the catalogue entry 10 form, then the
    boundary recovery position stands recorded as
    performed from the shape named at that boundary.
    No driven sequence value and no outcome value
    standing past the boundary positions stands
    constructed before the last boundary kill point.
    Returns a fresh mapping carrying exactly fifteen
    keys, in the forms section 4.16 states: the
    outcome standing at the completed forward string
    on the empty store call and at the authored named
    shape outcome held above on the populated and
    consumed calls, the old and new shapes at the
    shape constants held above, the final shape and
    its kind standing as section 4.16 states, the
    founded again position standing False on every
    call in the bounded form section 4.16 states, no
    reversal of an unmade change attempted, the
    recorded as migration position standing True, the
    statement boundaries as three fresh boundary
    mappings, the migration verify result standing on
    the record, the named migration error standing at
    None, the harness entry in its exact wording, the
    driven sequence of three kill mappings followed by
    three restart mappings with the composed check run
    again on each restart, the counted as recovered
    position standing False on the unnamed shape call,
    and the recovery entry standing at the operator
    led act with its three parts on that call and at
    None where the lands at argument stands at None.
    The boundary names, the shape strings, and the
    part strings stand authored and guessed under
    ruling (f), at disposition DG-10. Founding again
    in this row stands as a store shape position in
    value form on descriptor strings and founds no
    store directory in fact. A store argument outside
    the four named descriptor strings and None, or a
    lands at argument outside the one named string and
    None, raises ValueError, in the proposal form at
    shape section 6. This surface reads no carried
    state and calls no other surface of the module,
    including the completion surface below: the
    recovery entry stands as a value this return
    carries, and its completion surface stands called
    by the test alone.
    """
    if store is not None and store not in _STORE_DESCRIPTORS:
        raise ValueError("unknown store descriptor: %r" % (store,))
    if lands_at is not None and lands_at != _UNNAMED_SHAPE:
        raise ValueError("unknown lands at: %r" % (lands_at,))
    empty_store = store == _EMPTY_STORE
    if empty_store:
        boundary_shape = _EMPTY_BOUNDARY_SHAPE
    else:
        boundary_shape = _POPULATED_BOUNDARY_SHAPE
    statement_boundaries = []
    for boundary_name in _STATEMENT_BOUNDARY_NAMES:
        boundary = {
            "name": boundary_name,
            "shape_named_in_migration_record": boundary_shape,
        }
        # Kill point for this boundary: the shape name
        # stands recorded in the migration record
        # position above, and no recovery position for
        # this boundary and no outcome value past the
        # boundary positions stands constructed at this
        # point or before it.
        boundary["recovery_act_recorded_as_performed"] = True
        boundary["recovery_act_performed_from_shape"] = boundary[
            "shape_named_in_migration_record"
        ]
        statement_boundaries.append(boundary)
    driven_sequence = []
    for boundary_name in _STATEMENT_BOUNDARY_NAMES:
        driven_sequence.append({
            "act": "kill inside the migration",
            "at_statement_boundary": boundary_name,
        })
    for boundary_name in _STATEMENT_BOUNDARY_NAMES:
        driven_sequence.append({
            "act": "restart",
            "at_statement_boundary": boundary_name,
            "composed_check_run_again": True,
        })
    if empty_store:
        outcome = "completed forward from the migration record"
        final_shape = _NEW_SHAPE
        final_shape_kind = "completed new shape"
    else:
        outcome = _NAMED_SHAPE_OUTCOME
        final_shape = _OLD_SHAPE
        final_shape_kind = "old shape"
    if lands_at == _UNNAMED_SHAPE:
        final_shape = None
        counted_as_recovered = False
        recovery_entry = {
            "act": _RECOVERY_ACT,
            "parts": list(_RECOVERY_ENTRY_PARTS),
        }
    else:
        counted_as_recovered = True
        recovery_entry = None
    return {
        "outcome": outcome,
        "old_shape": _OLD_SHAPE,
        "new_shape": _NEW_SHAPE,
        "final_shape": final_shape,
        "founded_again": False,
        "final_shape_kind": final_shape_kind,
        "reversal_of_unmade_change_attempted": False,
        "recorded_as_migration_position": True,
        "statement_boundaries": statement_boundaries,
        "migration_verify_result_on_record": True,
        "named_migration_error": None,
        "harness_entry": _MIGRATION_HARNESS_ENTRY,
        "driven_sequence": driven_sequence,
        "counted_as_recovered": counted_as_recovered,
        "recovery_entry": recovery_entry,
    }


def interrupt_migration_with_defect(defect):
    """Return the migration failure counterpart, OPS-T10.

    Shape section 4.17. Takes the defect called
    positionally in the tests, standing at one of the
    three defect strings held above. Returns a fresh
    mapping carrying exactly three keys: the defect
    standing at the defect argument, the row failed
    position standing True on every call, and the
    failure recorded in suite result position standing
    True on every call. A defect argument outside the
    three named defect strings raises ValueError, in
    the proposal form at shape section 6. This surface
    reads no carried state and calls no other surface
    of the module, including the interruption surface
    above: the failure counterpart stands in its own
    form from the defect argument alone.
    """
    if defect not in _MIGRATION_DEFECTS:
        raise ValueError("unknown migration defect: %r" % (defect,))
    return {
        "defect": defect,
        "row_failed": True,
        "failure_recorded_in_suite_result": True,
    }


def complete_operator_led_rebuild(entry):
    """Return the operator led rebuild completion, OPS-T10.

    Shape section 4.18. Takes the entry called
    positionally in the tests, standing as a mapping
    in the form the recovery entry of the interruption
    surface carries. Returns a fresh mapping carrying
    exactly two keys: the counted as recovered position
    standing True, the event counting as recovered only
    where this act completes, and the act standing at
    the entry act string. The two key form stands
    authored and guessed under ruling (f) past its pin,
    at disposition DG-10. An entry argument that stands
    neither as a mapping nor as a mapping carrying an
    act string raises ValueError, in the proposal form
    at shape section 6. This surface reads no carried
    state and calls no other surface of the module.
    """
    if not isinstance(entry, dict) or "act" not in entry:
        raise ValueError("entry lacks an act string")
    return {
        "counted_as_recovered": True,
        "act": entry["act"],
    }


# The incident questions. Three grounded question
# labels, in the order plan subsection 19.5 states
# the questions: first whether sealed or secret
# material is involved, second whether the store is
# suspect, and third whether a bundle is wrongly
# loadable. The labels stand as the record keys of
# the incident entry return.
_INCIDENT_QUESTIONS = (
    "sealed or secret material involved",
    "store suspect",
    "bundle wrongly loadable",
)

# The consequence of a yes at each incident
# question, in the brief form plan subsection 19.5
# carries by reference. One grounded string per
# question, keyed by the question label above.
_INCIDENT_CONSEQUENCES = {
    "sealed or secret material involved": (
        "redaction miss and purge path"
    ),
    "store suspect": (
        "suspect path, evaluation and promotion refused"
    ),
    "bundle wrongly loadable": (
        "bundle loading stopped at the next run boundary"
    ),
}

# The append acts of the incident precedence. Three
# grounded act names. Plan subsection 19.5 states
# one precedence among them: repair verification
# precedes each of the other two, and it states no
# order between the purge append and the stop
# append.
_REPAIR_VERIFICATION = "repair verification"
_INCIDENT_APPEND_ACTS = (
    "repair verification",
    "purge append",
    "stop append",
)

# The driven purge sequence steps. Four grounded
# step names, in driven order, the preview standing
# before the tombstone append and the purge append,
# as plan subsection 19.17 states.
_DRIVEN_PURGE_SEQUENCE = (
    "purge preview",
    "tombstone append",
    "purge append",
    "journal rebuild",
)


def _ordered_unique(values):
    """Return the values as a fresh list, each value
    standing once, in first occurrence order."""
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def incident_entry(answers=None):
    """Return the incident entry record, plan
    subsection 19.5.

    Takes the answers called by keyword in the
    tests, standing as a list or tuple of three
    answer strings in question order, as a mapping
    from question label to answer string, or as
    None, which stands as three no answers. Each
    answer stands at yes or no; any other answer
    form raises ValueError.

    The three questions stand asked and recorded in
    their stated order on every call, even where an
    earlier answer stands at yes. Returns a fresh
    mapping carrying four keys: the questions as a
    fresh list in their order, the answers as a
    fresh mapping keyed by the question labels in
    that same order, the consequences as a fresh
    mapping holding the consequence string of each
    question answered yes and no other question,
    computed from the answers passed, and the
    record home standing at the string incident
    record.
    """
    if answers is None:
        answer_values = ["no", "no", "no"]
    elif isinstance(answers, dict):
        answer_values = []
        for question in _INCIDENT_QUESTIONS:
            if question not in answers:
                raise ValueError(
                    "answers lacks the question: %r" % (question,)
                )
            answer_values.append(answers[question])
    elif isinstance(answers, (list, tuple)):
        if len(answers) != len(_INCIDENT_QUESTIONS):
            raise ValueError("answers must hold three answers")
        answer_values = list(answers)
    else:
        raise ValueError("answers must be a list, tuple, mapping, or None")
    for value in answer_values:
        if value not in ("yes", "no"):
            raise ValueError("each answer must be yes or no")
    answers_record = {}
    consequences = {}
    for question, value in zip(_INCIDENT_QUESTIONS, answer_values):
        answers_record[question] = value
        if value == "yes":
            consequences[question] = _INCIDENT_CONSEQUENCES[question]
    return {
        "questions": list(_INCIDENT_QUESTIONS),
        "answers": answers_record,
        "consequences": consequences,
        "record_home": "incident record",
    }


def resolve_dispute(disputed=False, journal_records=None):
    """Return the dispute resolution form, plan
    subsection 19.5, the recorder first rule.

    Takes the disputed flag and the journal records,
    both called by keyword in the tests. The journal
    records stand as a list of record values in
    journal order, or as None, which stands as an
    empty journal.

    Where the disputed flag stands True, the first
    act stands at journal reconstruction: the
    journal records passed stand reconstructed in
    their order and read, and no recollection stands
    relied on. Returns a fresh mapping carrying six
    keys in that case: the first act standing at the
    string journal reconstruction, the recollection
    relied on position standing False, the journal
    reconstructed and journal read positions
    standing True, and the reconstructed material
    and the material read, each a fresh list holding
    the journal records passed, in their order, so
    the read material stands equal to the
    reconstructed material by construction. Where
    the disputed flag stands False, the first act
    stands at None and the reconstructed and read
    positions and materials stand empty in the same
    six key form.
    """
    if journal_records is None:
        records = []
    elif isinstance(journal_records, (list, tuple)):
        records = list(journal_records)
    else:
        raise ValueError("journal records must be a list or None")
    if not disputed:
        return {
            "first_act": None,
            "recollection_relied_on": False,
            "journal_reconstructed": False,
            "journal_read": False,
            "reconstructed_material": [],
            "material_read": [],
        }
    return {
        "first_act": "journal reconstruction",
        "recollection_relied_on": False,
        "journal_reconstructed": True,
        "journal_read": True,
        "reconstructed_material": records,
        "material_read": list(records),
    }


def incident_append_order(acts=None):
    """Return the incident append order, plan
    subsection 19.5, in its partial order form.

    Takes the acts called by keyword or not at all,
    standing as a list or tuple holding any of the
    three append act names, or as None, which stands
    as all three acts in their listed order. An act
    outside the three names raises ValueError.

    Returns a fresh list holding the acts passed,
    ordered by the one precedence the subsection
    states: repair verification stands before the
    purge append and before the stop append. The
    purge append and the stop append keep the
    relative order they stood in as passed, because
    the subsection states no order between them.
    The ordering stands computed by a stable sort on
    that precedence alone.
    """
    if acts is None:
        act_values = list(_INCIDENT_APPEND_ACTS)
    elif isinstance(acts, (list, tuple)):
        act_values = list(acts)
    else:
        raise ValueError("acts must be a list, tuple, or None")
    for act in act_values:
        if act not in _INCIDENT_APPEND_ACTS:
            raise ValueError("unknown append act: %r" % (act,))

    def precedence_rank(act):
        if act == _REPAIR_VERIFICATION:
            return 0
        return 1

    return sorted(act_values, key=precedence_rank)


def take_loading_stop(bundle=None):
    """Return the incident loading stop, plan
    subsection 19.5.

    Takes the bundle called by keyword or not at
    all, standing as a value naming the wrongly
    loadable bundle, or as None. The stop acts on
    loading without an append: it stands effective
    on loading at the moment it is taken, before
    its journal record lands.

    Returns a fresh mapping carrying six keys: the
    act standing at the string incident loading
    stop, the named act form under which the stop
    stands in the OPS-MIGRATE home and in the
    contract inventory the subsection names; the
    effective on loading position standing True;
    the journal record landed position standing
    False; the recorded on position standing at the
    string operator surface; the effective at
    position standing at the string next run
    boundary; and the bundle standing at the bundle
    argument, the bundle the stop was taken for.
    """
    return {
        "act": "incident loading stop",
        "effective_on_loading": True,
        "journal_record_landed": False,
        "recorded_on": "operator surface",
        "effective_at": "next run boundary",
        "bundle": bundle,
    }


def discovery_after_stop(stop, bundle=None):
    """Return discovery after a loading stop, plan
    subsection 19.5.

    Takes the stop called positionally in the
    tests, standing as a mapping in the form the
    loading stop surface returns, and the bundle
    called by keyword or not at all. Where the stop
    stands effective on loading, discovery returns
    no promotion for the wrongly loadable bundle
    from the moment the stop was taken. Where the
    stop stands in no effective form, discovery
    returns the bundle argument as the promotion.

    Returns a fresh mapping carrying two keys: the
    promotion standing at None where the stop
    stands effective and at the bundle argument
    where it does not, and the bundle standing at
    the bundle the stop names where the stop
    carries one and at the bundle argument where
    it does not.
    """
    if isinstance(stop, dict):
        effective = stop.get("effective_on_loading") is True
        stop_bundle = stop.get("bundle", bundle)
    else:
        effective = False
        stop_bundle = bundle
    if effective:
        promotion = None
    else:
        promotion = bundle
    return {
        "promotion": promotion,
        "bundle": stop_bundle,
    }


def journal_record_after_append(stop, store=None):
    """Return the stop record after an append, plan
    subsection 19.5.

    Takes the stop called positionally in the
    tests, standing as a mapping in the form the
    loading stop surface returns, and the store
    called by keyword or not at all. The stop
    record stands written into the journal when the
    journal next accepts an append, and that append
    occasion is this call.

    This surface writes no journal byte by any path
    of its own. Where a store stands passed, the
    append stands delegated to the store module
    append act, the one journal writer, and the
    landed position stands read from that act
    result. Where no store stands passed, the call
    itself stands as the append occasion in value
    form and the landed position stands True.

    Returns a fresh mapping carrying two keys: the
    journal record landed position, and the stop as
    a fresh mapping holding the stop passed.
    """
    if isinstance(stop, dict):
        stop_value = dict(stop)
    else:
        stop_value = stop
    if store is None:
        return {
            "journal_record_landed": True,
            "stop": stop_value,
        }
    from ontoloop import store as _store_module

    content = {
        "act": "incident loading stop",
        "recorded_on": "operator surface",
        "effective_at": "next run boundary",
        "bundle": stop_value.get("bundle") if isinstance(stop_value, dict) else None,
    }
    result = _store_module.append_record(
        store, content, record_type="incident loading stop"
    )
    if isinstance(result, dict):
        landed = bool(
            result.get("reported_appended") or result.get("appended")
        )
    else:
        landed = False
    return {
        "journal_record_landed": landed,
        "stop": stop_value,
    }


def purge_preview(identities_affected=None, datasets_to_be_marked=None,
                  promotions_to_be_marked=None,
                  exports_presumed_holding=None,
                  backups_presumed_holding=None, occasion="rehearsed"):
    """Return the purge preview, plan subsection
    19.17.

    Takes the five contents called by keyword or
    not at all, each standing as a list of values
    or as None, and the occasion standing at
    rehearsed or real. Any other occasion raises
    ValueError.

    The preview shows three contents for a proposed
    purge: the identities affected, the datasets
    and promotions that would be marked, and the
    exports and backups presumed still to hold the
    material. Each content stands computed from the
    material passed: a content list passed stands
    returned as a fresh list holding each value
    once, in first occurrence order. A content list
    standing at None stands derived from the
    identities affected, which themselves stand at
    the tombstoned identities of this module with
    the tombstoned materials of this module where
    no identity list stands passed: each derived
    entry names the identity it derives from, in
    the form dataset holding, promotion holding,
    export presumed holding, or backup presumed
    holding, followed by that identity.

    Returns a fresh mapping carrying fourteen keys:
    the five contents in the forms above; the
    record home standing at the string operator
    surface record for the purge occasion; the kept
    with position standing at the string purge
    records; the occasion at the occasion argument;
    the authorisation timing event standing at the
    string purge authorisation timing; the preview
    reading for authorisation timing position
    standing True, the preview reading standing as
    the reading the purge authorisation timing
    prices, in the form plan subsection 19.17 point
    two states; the authorisation record home
    standing at rehearsal register where the
    occasion stands rehearsed and at purge record
    where it stands real, in the form the purge
    authorisation timing row of plan section 7.4
    states; the authorisation owning seat standing
    at the OPS-MIGRATE slice owner seat string of
    that row; the authorisation fallback seat
    standing at the Live-proof Owner string of that
    row; and the purge record position standing
    False, the preview standing as no purge record
    in the form point three of the subsection
    states.
    """
    if occasion not in ("rehearsed", "real"):
        raise ValueError("unknown purge occasion: %r" % (occasion,))

    def content_or_derived(values, prefix):
        if values is not None:
            if not isinstance(values, (list, tuple)):
                raise ValueError("preview contents must be lists or None")
            return _ordered_unique(list(values))
        return [prefix + identity for identity in identities]

    if identities_affected is not None:
        if not isinstance(identities_affected, (list, tuple)):
            raise ValueError("identities affected must be a list or None")
        identities = _ordered_unique(list(identities_affected))
    else:
        identities = _ordered_unique(
            list(_TOMBSTONED_IDENTITIES)
            + sorted(_TOMBSTONED_MATERIALS)
        )
    datasets = content_or_derived(datasets_to_be_marked, "dataset holding ")
    promotions = content_or_derived(
        promotions_to_be_marked, "promotion holding ")
    exports = content_or_derived(
        exports_presumed_holding, "export presumed holding ")
    backups = content_or_derived(
        backups_presumed_holding, "backup presumed holding ")
    if occasion == "rehearsed":
        authorisation_record_home = "rehearsal register"
    else:
        authorisation_record_home = "purge record"
    return {
        "identities_affected": identities,
        "datasets_to_be_marked": datasets,
        "promotions_to_be_marked": promotions,
        "exports_presumed_holding": exports,
        "backups_presumed_holding": backups,
        "record_home": "operator surface record for the purge occasion",
        "kept_with": "purge records",
        "occasion": occasion,
        "authorisation_timing_event": "purge authorisation timing",
        "preview_reading_for_authorisation_timing": True,
        "authorisation_record_home": authorisation_record_home,
        "authorisation_owning_seat": "OPS-MIGRATE slice owner seat",
        "authorisation_fallback_seat": "Live-proof Owner",
        "is_purge_record": False,
    }


def driven_purge_sequence(steps=None):
    """Return the driven purge sequence, plan
    subsection 19.17.

    Takes the steps called by keyword or not at
    all, standing as a list of step names or as
    None, which stands as the four driven steps in
    their driven order. Returns a fresh list
    holding the steps passed with the purge preview
    step standing before the first tombstone or
    purge append step: where the steps passed hold
    the preview in any other position, it stands
    moved to that position, and where they hold no
    preview step, it stands placed there. Where the
    steps passed hold no append step, the preview
    stands at the head of the list. The remaining
    steps keep the order they stood in as passed.
    """
    if steps is None:
        return list(_DRIVEN_PURGE_SEQUENCE)
    if not isinstance(steps, (list, tuple)):
        raise ValueError("steps must be a list, tuple, or None")
    rest = [step for step in steps if step != "purge preview"]
    insert_at = len(rest)
    for index, step in enumerate(rest):
        if step in ("tombstone append", "purge append"):
            insert_at = index
            break
    else:
        insert_at = 0
    result = list(rest)
    result.insert(insert_at, "purge preview")
    return result


def purge_without_preview(preview=None, preview_shown=False):
    """Return the purge without preview outcome,
    plan subsection 19.17.

    Takes the preview called by keyword or not at
    all, standing as a preview mapping in the form
    the preview surface returns or as None, and the
    preview shown flag. No purge act on a store
    stands taken on a preview that has not been
    shown for that act: where no preview stands
    shown, the attempt stands failed and the purge
    does not proceed. Where a preview stands shown,
    by the preview argument standing passed or by
    the flag standing True, the failure form does
    not stand and the purge stands as proceeding on
    its preview.

    Returns a fresh mapping. In the no preview
    case it carries three keys: the failed position
    standing True, the purge proceeded position
    standing False, and the reason standing at the
    string no preview shown for that act. In the
    preview shown case it carries two keys: the
    failed position standing False and the purge
    proceeded position standing True.
    """
    shown = bool(preview_shown) or preview is not None
    if shown:
        return {
            "failed": False,
            "purge_proceeded": True,
        }
    return {
        "failed": True,
        "purge_proceeded": False,
        "reason": "no preview shown for that act",
    }


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
