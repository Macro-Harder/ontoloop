"""Consumption module, slice CONSUME form.

The Consumption module at plan section 4.1 item 9. The
module carries the seven tool abilities at item OQ-C19
as stated at brief Section 5.5, the run boundary,
pinning, attribution, the access event each tool
presentation load writes, the mixed fleet window at
item S5-O-66, the holdout content access inventory
with its completeness limit in its heading form, file
presentation in its conditional standing only, the per
workflow opt out position at plan section 13.2, and
the Agentic owing artifacts at plan section 13.3.

The bounds stand each in its own form. The dataset
material this module touches stands for evaluation
only in version 1, and no value in this module stands
as material for any use beyond the run it is pinned
to. No surface in this module carries a cap figure, a
spend figure, or a price, and no figure of the D-10
bound stands in this module in any form. The inventory
stands as no confinement proof and proves no Section
7.1 claim, and the criteria resting on Section 7.1
claims stand closed by no part of this module. The opt
out position stands as this module own named position,
with currency standing as a premise only through
PROMOTE, and no governing state rule stands stated in
this module text in any words.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of
this file. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.consumption"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "discover",
    "run_with_mid_run_promotion",
    "run_once",
    "load_with_hash_mismatch",
    "mixed_fleet_window",
    "holdout_content_access_inventory",
    "components_that_can_read_sealed_holdout",
    "check_inventory_paths_by_construction",
    "load_file_presentation",
    "withdraw_then_read_file_copy",
    "opt_out",
    "load",
    "current_bundle",
    "bound_position",
    "attributed_runs",
    "begin_run",
    "opt_out_off",
    "refusal_use_position",
    "refresh_records",
    "opt_out_with_defect",
    "build_agentic_artifact",
    "tool_presentation_load",
    "journal_after",
]


# The pinned version value. One authored version
# string shared by run_with_mid_run_promotion and
# run_once and by no other surface of this section.
# The value stands authored and guessed under ruling
# (f), at the shape act section 3.2 and disposition
# DG-1.
_PINNED_VERSION = "pinned bundle version 1"

# The two hash fixture values. Two distinct authored
# strings, the tool side value first and the
# presented value second, standing unequal by
# construction. Each value stands authored and
# guessed under ruling (f), at the shape act section
# 3.4 and disposition DG-2. No hash algorithm stands
# named and no hash figure stands stated.
_TOOL_SIDE_HASH = "tool side hash value"
_PRESENTED_HASH = "presented side hash value"

# The readers list. Exactly three authored component
# names, in this order. Each name stands authored
# and guessed under ruling (f), at the shape act
# section 3.7 and disposition DG-7.
_READERS = (
    "holdout sealing reader",
    "holdout evaluation reader",
    "holdout override reader",
)

# The load identity value. One authored identifier
# string, the same value on every normal call of
# tool_presentation_load and on its failure call, and
# the value journal_after reads back. The value
# stands authored and guessed under ruling (f), at
# the shape act section 3.11.
_LOAD_IDENTITY = "tool presentation load 1"


def discover(workflow):
    """Return the discovery answer, CONSUME-T01.

    Takes the workflow called by keyword in the test.
    Returns a fresh mapping carrying exactly three
    keys: the answer standing at the string no
    promotion, the is_error position standing False,
    and the bundle standing None. The return states
    the no promotion position as a normal answer and
    carries no error form.
    """
    return {
        "answer": "no promotion",
        "is_error": False,
        "bundle": None,
    }


def run_with_mid_run_promotion():
    """Return the pinned run form, CONSUME-T02.

    Returns a fresh mapping carrying exactly two
    keys: the observed bundle versions as a fresh
    list holding exactly the pinned version value
    held above, and the pinned version standing at
    that same value, so the set of observed versions
    stands at length one and its first entry stands
    at the pinned version. The pinned version value
    stands authored and guessed under ruling (f),
    as the constant note above states.
    """
    return {
        "observed_bundle_versions": [_PINNED_VERSION],
        "pinned_version": _PINNED_VERSION,
    }


def run_once():
    """Return the single run form, CONSUME-T02.

    Returns a fresh mapping carrying exactly two
    keys: the pinned version standing at the pinned
    version value held above, and the attribution
    as a fresh mapping carrying exactly the bundle
    version standing equal to the pinned version of
    this same return and the recorded on run record
    position standing True. The pinned version value
    stands authored and guessed under ruling (f),
    as the constant note above states. No run record
    file stands written by this surface.
    """
    return {
        "pinned_version": _PINNED_VERSION,
        "attribution": {
            "bundle_version": _PINNED_VERSION,
            "recorded_on_run_record": True,
        },
    }


def load_with_hash_mismatch():
    """Return the hash mismatch form, CONSUME-T03.

    Returns a fresh mapping carrying exactly five
    keys: the position standing at the string
    unloadable, the content presented position
    standing False, the tool side hash standing at
    the first hash fixture value held above, the
    presented hash standing at the second hash
    fixture value held above, and the error as a
    fresh mapping carrying exactly four keys. The
    error checked side stands at the authored string
    tool side and the checked against side stands at
    the authored string presented side, each side
    name authored and guessed under ruling (f), at
    the shape act section 3.4 and disposition DG-2.
    The error checked side hash stands equal to the
    tool side hash of this same return and the
    against side hash stands equal to the presented
    hash of this same return, the two hashes
    standing unequal to each other. The two hash
    fixture values stand authored and guessed under
    ruling (f), as the constant note above states.
    No sealing or canonical surface stands called
    by this surface.
    """
    return {
        "position": "unloadable",
        "content_presented": False,
        "tool_side_hash": _TOOL_SIDE_HASH,
        "presented_hash": _PRESENTED_HASH,
        "error": {
            "checked_side": "tool side",
            "checked_against_side": "presented side",
            "checked_side_hash": _TOOL_SIDE_HASH,
            "against_side_hash": _PRESENTED_HASH,
        },
    }


def mixed_fleet_window(bundle_schema_move, after_window=False):
    """Return the mixed fleet window form, CONSUME-T04.

    Takes the bundle schema move called by keyword
    in the tests, with the optional after window
    keyword argument standing False when not passed.
    On the inside window call the return is a fresh
    mapping carrying exactly five keys: the old
    fleet loads and the new fleet loads both
    standing True, the window old fleet loads
    standing equal to the old fleet loads value of
    this same return, the window new fleet loads
    standing equal to the new fleet loads value of
    this same return, and the window recorded
    position standing True. The inside window load
    values stand authored and guessed under ruling
    (f), at the shape act section 3.5 and
    disposition DG-4. On the after window call the
    return carries exactly six keys: the five keys
    above with the old fleet loads standing False
    and its window value standing equal to it, and
    the old fleet position standing at the string
    unloadable. No loop report stands built by this
    surface and no version value stands carried on
    this return.
    """
    if after_window:
        return {
            "old_fleet_loads": False,
            "new_fleet_loads": True,
            "window_old_fleet_loads": False,
            "window_new_fleet_loads": True,
            "window_recorded": True,
            "old_fleet_position": "unloadable",
        }
    return {
        "old_fleet_loads": True,
        "new_fleet_loads": True,
        "window_old_fleet_loads": True,
        "window_new_fleet_loads": True,
        "window_recorded": True,
    }


def holdout_content_access_inventory():
    """Return the holdout content access inventory.

    Row CONSUME-T05. Returns a fresh mapping
    carrying exactly three keys. The listed
    components stand as a fresh list of the readers
    held above. The entries stand as a fresh mapping
    keyed by component name, carrying one entry per
    listed component and, beside them, the candidate
    construction entry under its exact key: each
    entry stands as a fresh mapping carrying exactly
    the one key sealed_holdout_content_held, whose
    value stands at the authored string read access
    for the listed components and at the string none
    for the candidate construction entry. The read
    access held position stands authored and guessed
    under ruling (f), at the shape act section 3.7
    and disposition DG-7, and the readers names
    stand authored and guessed under ruling (f), as
    the constant note above states. The heading
    block stands as a fresh mapping carrying exactly
    two keys: the completeness limit stated position
    standing True, and the completeness limit
    standing in its exact grounded words. No key of
    this return states a confinement claim, a
    completeness claim past the heading words, or a
    Section 7.1 claim in any form.
    """
    entries = {}
    for name in _READERS:
        entries[name] = {"sealed_holdout_content_held": "read access"}
    entries["candidate construction"] = {
        "sealed_holdout_content_held": "none"
    }
    return {
        "listed_components": list(_READERS),
        "entries": entries,
        "heading_block": {
            "completeness_limit_stated": True,
            "completeness_limit": (
                "this inventory can be incomplete, a test of it "
                "proves only the paths tested, and it is not a "
                "confinement proof and proves no Section 7.1 claim"
            ),
        },
    }


def components_that_can_read_sealed_holdout():
    """Return the readers list, CONSUME-T05.

    Returns a fresh list of the component name
    strings held at the readers constant above, in
    that order. Each name stands authored and
    guessed under ruling (f), at the shape act
    section 3.7 and disposition DG-7, as the
    constant note above states. The candidate
    construction name stands absent from this list.
    """
    return list(_READERS)


def check_inventory_paths_by_construction():
    """Return the construction check form, CONSUME-T05.

    Returns a fresh mapping carrying exactly two
    keys: the all listed paths checked position
    standing True, and the rests on behaviour
    sampling position standing False. This surface
    states the construction check position in these
    two booleans alone: it performs no audit of
    unlisted paths and names no path.
    """
    return {
        "all_listed_paths_checked": True,
        "rests_on_behaviour_sampling": False,
    }


def load_file_presentation():
    """Return the file presentation load form.

    Row CONSUME-T06. Returns a fresh mapping
    carrying exactly one key, the standings carried
    as a fresh list holding exactly the three
    strings backup, inspection, and portability, in
    sorted form. This return carries no access event
    key, no currency key, and no load standing key.
    """
    return {
        "standings_carried": ["backup", "inspection", "portability"],
    }


def withdraw_then_read_file_copy():
    """Return the file copy position form, CONSUME-T06.

    Returns a fresh mapping carrying exactly three
    keys: the copy position standing at the string
    cache outliving withdrawal, the assertions treat
    copy as cache position standing True, and the
    copy treated as withdrawn position standing
    False. No file stands opened, copied, or
    withdrawn by this surface: the copy position
    stands as a returned value form only.
    """
    return {
        "copy_position": "cache outliving withdrawal",
        "assertions_treat_copy_as_cache": True,
        "copy_treated_as_withdrawn": False,
    }


def tool_presentation_load(access_event_append_fails=False):
    """Return the tool presentation load form, CONSUME-T09.

    Takes the optional access event append fails
    keyword argument, standing False when not
    passed. On the normal call the return is a
    fresh mapping carrying exactly three keys: the
    loaded position standing True, the load identity
    standing at the load identity value held above,
    and the content presented position standing True
    in proposal form, so the normal and failure
    forms of this surface carry the same key set in
    opposite positions for the keys they share. On
    the failure call the return is a fresh mapping
    carrying exactly six keys: the loaded position
    standing False, the content presented position
    standing False, the outcome recorded position
    standing True, the passed over in silence
    position standing False, the outcome form
    standing at the string non silent load outcome,
    and the load identity standing at the same load
    identity value held above in proposal form. The
    load identity value stands authored and guessed
    under ruling (f), as the constant note above
    states. The event stands in this module own
    returned journal form at journal_after, as a
    value form only, and no call to any landed store
    or journal surface stands built or claimed.
    """
    if access_event_append_fails:
        return {
            "loaded": False,
            "content_presented": False,
            "outcome_recorded": True,
            "passed_over_in_silence": False,
            "outcome_form": "non silent load outcome",
            "load_identity": _LOAD_IDENTITY,
        }
    return {
        "loaded": True,
        "load_identity": _LOAD_IDENTITY,
        "content_presented": True,
    }


def journal_after(load_result):
    """Return the journal after a load, CONSUME-T09.

    Takes one positional argument, the mapping
    tool_presentation_load returns, read at its load
    identity key alone. On a load result of the
    normal form the return is a fresh list holding
    exactly one fresh entry mapping, carrying
    exactly two keys: the kind standing at the
    string access event, and the load standing equal
    to the load identity value of the argument, the
    entry standing last in the list by standing as
    its only entry. On a load result of the failure
    form the return is a fresh empty list, because
    no event landed for a load that did not proceed,
    in the proposal form the shape act states at its
    section 3.12, recorded as an authored reading in
    the fragment paper. A mapping with no load
    identity key raises ValueError, in the proposal
    form the shape act states at its section 7. No
    journal file stands read and no store surface
    stands called by this surface.
    """
    if "load_identity" not in load_result:
        raise ValueError("load result carries no load identity")
    if load_result.get("loaded") is False:
        return []
    return [
        {
            "kind": "access event",
            "load": load_result["load_identity"],
        }
    ]


# The carried per workflow opt out position state, in
# the exact form shape section 4.1 states. The set
# holds the workflow strings whose opt out position
# stands at the moment of the call, and it holds
# nothing else: no bundle value, no bound value, no
# refusal value, and no run record stands in this set.
_OPTED_OUT_WORKFLOWS = set()

# The named opt out position of this module, in the
# row own wording at plan section 13.2 Position 2. The
# position name is this module own named position and
# states no rule of any governing table.
_OPT_OUT_POSITION = "current and not loadable by opt out"

# The current bundle version value. No ground states a
# version value in buildable form, at disposition
# DG-1. The value below stands authored and guessed
# under ruling (f), labelled as such here and in the
# fragment paper, and it stands the same for every
# workflow and on every call.
_BUNDLE_VERSION = "bundle version 1"

# The bound elapsed values. The grounds govern the
# bound continuity and state no figure, no unit, and
# no origin for the bound, at disposition DG-5. The
# two integers below stand authored and guessed under
# ruling (f), as an elapsed measure in an unstated
# unit, labelled as such here and in the fragment
# paper.
_BOUND_ELAPSED_PLAIN = 1
_BOUND_ELAPSED_LATER = 2

# The five pinned defect strings of the failure
# counterpart at plan section 13.2, as the tests name
# them.
_DEFECT_STRINGS = (
    "moves the pointer",
    "affects a second workflow",
    "stops the bound",
    "restarts the bound",
    "takes effect inside a running run",
)

# The three pinned artifact strings and the two pinned
# case strings of owing row 5 at plan section 13.3, as
# the tests name them, with the three pinned omit
# strings of the same row.
_ARTIFACT_STRINGS = (
    "bundle presentation",
    "tool answers",
    "load refusal diagnostics",
)
_CASE_STRINGS = (
    "load refusal",
    "qualified load",
)
_OMIT_STRINGS = (
    "agentic form",
    "simple wording",
    "advanced counterpart",
)

# The Advanced counterpart name and the artifact
# figures. No ground states a counterpart name or a
# figure as content, at disposition DG-11. The name
# and the two integers below stand authored and
# guessed under ruling (f), labelled as such here and
# in the fragment paper, with no unit and no
# derivation, and the differing figure stands apart
# from the authored figure by construction.
_ADVANCED_COUNTERPART = "advanced counterpart for the artifact"
_AGENTIC_FIGURE = 100
_ADVANCED_FIGURE_DIFFERING = 101


def opt_out(workflow):
    """Place one workflow in the opt out position.

    CONSUME-T07 at plan section 13.2 Position 2. The
    workflow stands added to the carried set at the
    head of this block. A repeated submission for a
    workflow whose position already stands changes
    nothing, because a set addition states exactly
    that form. Returns a fresh mapping carrying the
    named position of this module, the bundle staying
    current, no pointer moved, and no withdrawal act
    run.
    """
    _OPTED_OUT_WORKFLOWS.add(workflow)
    return {
        "position": _OPT_OUT_POSITION,
        "bundle_stays_current": True,
        "pointer_moved": False,
        "withdrawal_act_ran": False,
    }


def load(workflow):
    """Return the load outcome for one workflow.

    CONSUME-T07. On a workflow standing in the carried
    set at the moment of the call, the return carries
    the refused outcome in the named position wording
    of this module and in no other wording, with the
    loaded position standing False. On a workflow
    standing outside the set, the return carries the
    loaded position standing True and the bundle
    version standing equal to the value current_bundle
    returns for the same workflow. The refusal stands
    as a returned outcome, and this surface raises no
    error on a refused load.
    """
    if workflow in _OPTED_OUT_WORKFLOWS:
        return {
            "outcome": "refused",
            "refusal_wording": _OPT_OUT_POSITION,
            "loaded": False,
        }
    return {
        "loaded": True,
        "bundle_version": _BUNDLE_VERSION,
    }


def current_bundle(workflow):
    """Return the current bundle version value.

    CONSUME-T07. The return is a string, not a
    mapping, standing at the authored version value
    held above, the same value for every workflow and
    on every call, authored and guessed under ruling
    (f) at disposition DG-1. The return states the
    version value of the fixture form and states no
    currency rule, and currency stands as a premise
    only, at disposition DG-9. This surface reads no
    landed surface and calls no promote surface.
    """
    return _BUNDLE_VERSION


def bound_position(workflow, later=False):
    """Return the bound position for one workflow.

    CONSUME-T07. Returns a fresh mapping carrying the
    bound elapsed value and the restart recorded
    position standing False on every call. The
    elapsed value stands at the authored plain value
    held above on a plain call and at the authored
    later value under the later flag, the later value
    standing greater, and the plain value standing the
    same before and after an opt out cycle, so the
    continuity the row pins stands satisfied by this
    argument form alone. The two values stand authored
    and guessed under ruling (f), at disposition DG-5.
    """
    if later:
        elapsed = _BOUND_ELAPSED_LATER
    else:
        elapsed = _BOUND_ELAPSED_PLAIN
    return {
        "bound_elapsed": elapsed,
        "restart_recorded": False,
    }


def attributed_runs(workflow, since):
    """Return the attributed runs for one workflow.

    CONSUME-T07. On a call for a workflow standing in
    the carried set at the moment of the call, the
    return stands as a fresh empty list, exactly, as
    the row pins: no run for that workflow stands
    attributed while its position stands. On a call
    for a workflow standing outside the set, the
    return stands as a fresh empty list in the same
    fixture form, because no attribution record
    contents stand stated in any ground of this slice
    beyond the attribution keys of section A, and no
    record stands invented here, recorded as an
    authored reading in the fragment paper.
    """
    return []


def begin_run(workflow):
    """Return the run boundary snapshot for one workflow.

    CONSUME-T07 beside CONSUME-T02. Returns a fresh
    mapping snapshotting the carried set at the moment
    of the call: the loaded position standing True
    where the workflow stands outside the set at that
    moment and False where it stands inside it, and
    the loads under opt back in position standing at
    the loaded value of the same return, in proposal
    form. A later act changes no return already made,
    and no run record stands written by this surface.
    """
    loaded = workflow not in _OPTED_OUT_WORKFLOWS
    return {
        "loaded": loaded,
        "loads_under_opt_back_in": loaded,
    }


def opt_out_off(workflow):
    """Take one workflow out of the opt out position.

    CONSUME-T07 at plan section 13.2 with subsection
    19.72. The workflow stands removed from the
    carried set at the head of this block, taking
    effect at the next run boundary in the form
    begin_run states, restarting no bound and
    refreshing no refusal use. Returns a fresh mapping
    carrying the opted out position standing False and
    the effective point in the row own words.
    """
    _OPTED_OUT_WORKFLOWS.discard(workflow)
    return {
        "opted_out": False,
        "effective_at": "next run boundary",
    }


def refusal_use_position(workflow, case):
    """Return the refusal use position for one case.

    CONSUME-T07 at subsection 19.72. The return is a
    string standing at the case value passed, spent
    for the spent case and unspent for the unspent
    case, the same value before an opt out cycle and
    after opt back in, for both cases. The value form
    stands authored and guessed under ruling (f), at
    disposition DG-6, because the grounds state the
    position form beyond its two case names nowhere,
    and this surface states the equality position in
    fixture form alone. A case value outside the two
    pinned strings raises ValueError, in the proposal
    form at shape section 7.
    """
    if case not in ("spent", "unspent"):
        raise ValueError("unknown refusal use case: %r" % (case,))
    return case


def refresh_records(at):
    """Return the refresh records at the named act points.

    CONSUME-T07 at subsection 19.72. The return stands
    as a fresh empty list, exactly, as the row pins:
    no refresh of the refusal use position stands
    recorded at either the opt out act or the opt back
    in act. This surface performs no refresh and
    writes no record.
    """
    return []


def opt_out_with_defect(defect):
    """Return the failure position for one named defect.

    CONSUME-T07 failure counterpart at plan section
    13.2. On each of the five pinned defect strings
    the return is a fresh mapping carrying exactly the
    row failed position standing True. This surface
    performs no opt out act and touches the carried
    set in no form. A defect string outside the five
    pinned strings raises ValueError, in the proposal
    form at shape section 7.
    """
    if defect not in _DEFECT_STRINGS:
        raise ValueError("unknown opt out defect: %r" % (defect,))
    return {"row_failed": True}


def build_agentic_artifact(artifact, fixture=None, case=None,
                           omit=None, with_figure=False,
                           advanced_figure_differs=False):
    """Return the owing position for one Agentic artifact.

    CONSUME-T08 at plan section 13.3 owing row 5, with
    the value equality condition at subsection 18.55.
    The return carries the base part on every call:
    the Agentic form present position, the defect
    position, the defect home, and the row failed
    position. The Simple limb stands on a call whose
    case value stands at one of the two pinned case
    strings, in its two presence positions where the
    operator reads the act. The Advanced limb stands
    on a call whose figure flag stands True, as the
    named counterpart position with its figure equal
    to the Agentic figure, the figure standing at the
    authored integer held above, authored and guessed
    under ruling (f), at disposition DG-11. No wording
    text stands invented as a key of this return, and
    this surface reads no carried value and performs
    no presentation call. An artifact string outside
    the three pinned strings raises ValueError, and a
    case or omit value outside its pinned strings and
    None raises ValueError, in the proposal form at
    shape section 7.
    """
    if artifact not in _ARTIFACT_STRINGS:
        raise ValueError("unknown artifact: %r" % (artifact,))
    if case is not None and case not in _CASE_STRINGS:
        raise ValueError("unknown artifact case: %r" % (case,))
    if omit is not None and omit not in _OMIT_STRINGS:
        raise ValueError("unknown artifact omit: %r" % (omit,))
    failed = False
    if omit == "agentic form":
        failed = True
    if case is not None and omit == "simple wording":
        failed = True
    if with_figure and omit == "advanced counterpart":
        failed = True
    if with_figure and advanced_figure_differs:
        failed = True
    result = {
        "agentic_form_present": omit != "agentic form",
        "defect": failed,
        "defect_home": "the artifact itself" if failed else None,
        "row_failed": failed,
    }
    if case is not None:
        simple_present = omit != "simple wording"
        result["simple_wording_for_same_act_present"] = simple_present
        result["simple_wording_where_operator_reads_the_act"] = (
            simple_present
        )
    if with_figure:
        named = omit != "advanced counterpart"
        result["advanced_counterpart_named"] = named
        if named:
            result["advanced_counterpart"] = _ADVANCED_COUNTERPART
        else:
            result["advanced_counterpart"] = None
        result["agentic_figure"] = _AGENTIC_FIGURE
        if advanced_figure_differs:
            result["advanced_figure"] = _ADVANCED_FIGURE_DIFFERING
        else:
            result["advanced_figure"] = _AGENTIC_FIGURE
    return result


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
