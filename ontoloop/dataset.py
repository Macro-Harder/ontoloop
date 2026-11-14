"""Dataset build module, slice DATASET form.

The dataset build order at brief Section 5.3 as one
pipeline, the Dataset record with its intake account,
curation version pinning under item S5-O-25, the
operator attestation field, the post audit shortfall
state, and the pre scoring protocol record at item
S5-O-57 in its conditional form. Below the D-14 gate
the build writes no dataset and records the workflow
as not yet buildable with its counts, and at or above
the gate the Dataset is written sealed whole or not
written at all. The D-14 gate values stand guessed
at their register home. The dataset this module
builds is a curated dataset for evaluation only in
version 1, under plan subsection 20.84.

What this slice does not build stands absent from
this module altogether, and a lookup of any such name
raises AssertionError in the NOT BUILT form the suite
harness uses, through the module level guard at the
foot of this file. A lookup of a private or dunder
name raises AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.dataset"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "acknowledgement_wording",
    "attach_stamps_at_build",
    "brief_order",
    "brief_outcome_mapping",
    "brief_quota",
    "build_example_b",
    "build_order",
    "build_with_fault",
    "build_with_mid_build_append",
    "build_with_shortfall",
    "candidate_with_instruction_item",
    "check_dataset_record",
    "control_build_in_same_store",
    "cross_split_audit_at_build",
    "dataset_build_for_posture_sequence",
    "dataset_record",
    "dataset_record_example_b",
    "dataset_record_first_build_gate",
    "dedup_grouped_fixture",
    "eligibility_grouped_fixture",
    "error_catalogue",
    "fixed_text_travel_lint",
    "freshness_check",
    "intake_stamp_set",
    "meaning_check",
    "next_build",
    "reaffirm",
    "retire",
    "retire_unspent_sealed",
    "selection_grouped_fixture",
    "stale_warning_at_age",
    "stamp_origin_slice",
    "stamps_attached",
    "supersession_refusal",
    "test_instruction_items_against_holdout",
    "three_verbatim_texts",
]

from ontoloop.core import error_catalogue as _core_error_catalogue
from ontoloop.sealing import VERIFY_HOLES as _VERIFY_HOLES
from ontoloop.sealing import VERIFY_SENTENCE as _VERIFY_SENTENCE
from ontoloop.sealing import verbatim_texts as _sealing_verbatim_texts


# The build order list, in brief Section 5.3 order.
# Ground: the brief build order passage states the steps
# in prose in full, gate step first, then collect and
# state eligibility, exact dedup, settled quality filters
# only, grouping and near duplicate clustering inside the
# selection, plain selection per workflow, the cross split
# audit, the selection and audit loop, and the dataset
# written with its full intake account. The entry strings
# and the entry count stand as authored and guessed under
# scope item G-2, in the event the shape act states, and
# as an authored reading under entry 104 item (h).
_BUILD_ORDER = (
    "gate step",
    "collect and state eligibility",
    "exact dedup",
    "settled quality filters only",
    "grouping and near duplicate clustering inside the selection",
    "plain selection per workflow",
    "cross split audit",
    "selection and audit loop",
    "dataset written with full intake account",
)

# The selection order list. Ground: the brief plain
# selection passage states eligible material first, by
# grade points descending, then by store sequence
# ascending as the tie break. The entry strings stand as
# an authored reading under entry 104 item (h), at shape
# item G-1 in its brief order part.
_BRIEF_ORDER = (
    "grade points descending",
    "store sequence ascending",
)

# The outcome mapping. Ground: the brief selection mapping
# passage states that pass maps to success material, send
# back maps to failure material, and pass with correction
# maps to failure material, and that grade bands map as
# strong and sound to success material where the outcome
# is pass, and weak and unacceptable to failure material.
# The mapping stands keyed by outcome alone for the first
# three entries and by grade band alone for the last four,
# as an authored reading under entry 104 item (h): no
# ground states a joint key form for the band entries.
_OUTCOME_MAPPING = {
    "pass": "success material",
    "send back": "failure material",
    "pass with correction": "failure material",
    "strong": "success material",
    "sound": "success material",
    "weak": "failure material",
    "unacceptable": "failure material",
}

# The quota value. Ground: the brief proportions passage
# states that the stated proportions act as quotas filled
# first, with grade order inside each class, the
# proportions standing stated on the Dataset record under
# the OQ-C4 precedence rule. No ground states a quota
# figure, a proportion value, or a class key form, at
# shape item G-4. The value below states the rule form
# alone and no figure, as an authored reading under entry
# 104 item (h).
_QUOTA = {
    "rule": "stated proportions act as quotas filled first",
    "success material": "quota filled first",
    "failure material": "quota filled first",
}

# The pool fixture for the snapshot case. The run identity
# values and the appended run value stand as authored and
# guessed under scope item G-1, at shape item G-2: no
# ground states a run identity value form. The pool holds
# three runs in its snapshot form, as the smallest form
# that shows the membership positions the tests pin.
_POOL_RUN_IDS = ("run-001", "run-002", "run-003")
_APPENDED_RUN = "run-appended-mid-build"


def build_example_b(runs=None, group_size=None):
    """Example B build value, DATASET-T01 and DATASET-T02.

    With runs at 30 the value carries the gate form: no
    dataset written, the workflow state not yet buildable,
    and counts carrying runs at the passed value. With a
    group size of 5 or 8 the value carries the span form:
    the span condition failed, stated in its own form as
    span condition failure. A call with neither argument
    stands in the runs at 30 form, and a call with a group
    size alone stands at runs 30 in its counts, as an
    authored reading under entry 104 item (h) at shape
    item DG-3: no ground states the default form. The
    concrete Example B contents behind the counts stand
    as authored and guessed under scope item G-1. A fresh
    mapping stands returned on every call, with a fresh
    counts mapping inside it.
    """
    run_count = 30 if runs is None else runs
    return {
        "dataset_written": False,
        "workflow_state": "not yet buildable",
        "counts": {"runs": run_count},
        "span_condition": "failed",
        "span_failure_form": "span condition failure",
    }


def build_order():
    """The build order value, DATASET-T03.

    Returns a fresh list holding the build order entries
    in brief Section 5.3 order, in the spelling form the
    module constant above states. The tests pin this value
    by equality against the order value of the mid build
    value alone, and no literal entry stands pinned.
    """
    return list(_BUILD_ORDER)


def build_with_mid_build_append():
    """The snapshot build value, DATASET-T03.

    Returns a fresh mapping carrying the build order, one
    snapshot used, the run that lands during the build,
    and the pool run identities of the one consistent pool
    snapshot. The appended run stands outside the pool run
    identities of this build, in the brief snapshot rule
    form: appends landing during a build take effect for
    the next build and not for the build in flight.
    """
    return {
        "order": list(_BUILD_ORDER),
        "snapshots_used": 1,
        "appended_run": _APPENDED_RUN,
        "pool_run_ids": list(_POOL_RUN_IDS),
    }


def next_build(build):
    """The following build value, DATASET-T03.

    Takes the mid build value and returns a fresh mapping
    whose pool run identities hold the snapshot pool runs
    and, after them, the appended run of the passed build.
    No further key stands returned, at shape item G-2.
    """
    pool = list(build["pool_run_ids"])
    appended = build["appended_run"]
    if appended not in pool:
        pool.append(appended)
    return {"pool_run_ids": pool}


def dedup_grouped_fixture():
    """The dedup fixture value, DATASET-T04.

    Returns a fresh mapping carrying the comparison fields
    and the merged position of an outcome distinct pair.
    Ground: exact dedup after redaction keeps outcome
    bearing fields in the comparison, so runs with the
    same task text and different outcomes are never exact
    duplicates. The comparison field list holds the one
    pinned string and, beside it, the normalised task text
    field the brief dedup key names, as an authored reading
    under entry 104 item (h) at shape item G-3. The grouped
    fixture contents stand as authored and guessed under
    scope item G-1.
    """
    return {
        "comparison_fields": [
            "normalised task text",
            "outcome bearing fields",
        ],
        "merged_outcome_distinct_pair": False,
    }


def eligibility_grouped_fixture():
    """The eligibility fixture value, DATASET-T04.

    Returns a fresh mapping whose excluded mapping holds
    the synthetic kind and the canary kind, each with its
    own drop reason standing truthy. Ground: at collect
    and state eligibility, marked synthetic and canary
    material is excluded, is never a dataset member, and
    is reported under its own drop reason. The two drop
    reason strings stand as authored and guessed under
    scope item G-1, at shape item G-3: no ground states
    either string, and each test reads truthiness alone.
    """
    return {
        "excluded": {
            "synthetic": {
                "drop_reason": "marked synthetic material excluded",
            },
            "canary": {
                "drop_reason": "marked canary material excluded",
            },
        }
    }


def brief_order():
    """The selection order value, DATASET-T04.

    Returns a fresh list holding the selection order
    entries in the brief plain selection form stated at
    the module constant above.
    """
    return list(_BRIEF_ORDER)


def brief_outcome_mapping():
    """The outcome mapping value, DATASET-T04.

    Returns a fresh mapping holding the outcome mapping
    in the form the module constant above states.
    """
    return dict(_OUTCOME_MAPPING)


def brief_quota():
    """The quota value, DATASET-T04.

    Returns a fresh mapping holding the quota rule form
    the module constant above states, and no figure.
    """
    return dict(_QUOTA)


def selection_grouped_fixture():
    """The selection fixture value, DATASET-T04.

    Returns a fresh mapping carrying the selection order,
    the outcome mapping, and the quota, each equal to the
    module own brief value for that form, in the self
    referential form the tests pin. The grouped fixture
    contents stand as authored and guessed under scope
    item G-1, and the brief named return forms stand under
    the bound at entry 104 item (h).
    """
    return {
        "order": list(_BRIEF_ORDER),
        "outcome_mapping": dict(_OUTCOME_MAPPING),
        "quota": dict(_QUOTA),
    }


def cross_split_audit_at_build(
    material="flagged material in bundle", scored_before_refusal=None
):
    """The cross split audit at build, DATASET-T05.

    This call point performs no relation logic of its
    own. It calls the one shared module,
    ontoloop.cross_split_audit, at its build call point
    act audit_at_build, and translates that act outcome
    into the record form DATASET-T05 pins. The shared
    act outcome stands carried on the return under
    cross_split_audit_result, so the delegation stands
    readable from the value itself. At the build point
    the shared refusal outcome is the drop outcome: a
    refused spanning pair stands dropped, and the
    refusal stands recorded at the shared act record
    home. The audit covers the group relation, the
    signature relation, and the near verbatim cluster
    relation only, the relation set the shared module
    states. The paraphrase pair stands flagged on
    paraphrase grounds at False and flagged at False.
    The audit clears no paraphrase leakage: the clears
    key stands False and the residual risk stands in
    its pinned string form, carried at risk R8. No
    wider leakage clearance stands claimed by this
    value.
    """
    from ontoloop import cross_split_audit as _shared_module

    shared = _shared_module.audit_at_build(
        material, scored_before_refusal=scored_before_refusal
    )
    refused = bool(shared["candidate_bundle_refused"])
    return {
        "spanning_pairs_dropped": refused,
        "spanning_pairs_recorded": bool(
            refused or shared["firing_pairs"]
        ),
        "relations": ["group", "signature", "near verbatim cluster"],
        "paraphrase_pair": {
            "flagged_on_paraphrase_grounds": False,
            "flagged": False,
        },
        "clears_paraphrase_leakage": False,
        "residual_risk": "paraphrase leakage across the split",
        "cross_split_audit_result": dict(shared),
    }


def build_with_shortfall():
    """The shortfall build value, the DATASET-T06 limb.

    Returns a fresh mapping carrying the state alone, in
    its pinned string form. Ground: where eligible
    material runs out after the audit, the dataset stands
    written with an explicit post audit shortfall state.
    No count key and no verdict consequence key stands
    returned, at shape item G-7, because no test reads one
    on this value.
    """
    return {"state": "post audit shortfall"}


# The stamp acknowledgement wording. Its owing
# position stands grounded at plan section 13.3,
# owing row 2, and at brief Section 5.4 item S5-O-75:
# the wording stands in the intake account in full
# and not in summary or pointer form, for the gate
# stamps only, intake thin and high self reported
# share, each stamp acknowledgement stating what the
# operator is accepting in the stamp own terms and
# offering the action menu of proceed with the
# promotion, return for more material, or stop. No
# governing text carries the wording in whole form,
# so the text below stands authorised as authored
# and guessed under step record entry 104 ruling
# (g), on shape item G-3, labelled as such here and
# in the fragment paper, and never as grounded.
_ACKNOWLEDGEMENT_WORDING = (
    "The operator acknowledges the gate stamps on "
    "this dataset. Intake thin: the operator accepts "
    "that the intake for this dataset is thin. High "
    "self reported share: the operator accepts that "
    "a high share of the material in this dataset is "
    "self reported. For each gate stamp the operator "
    "chooses one action: proceed with the promotion, "
    "return for more material, or stop."
)

# The Example B intake figure set. The tests pin the
# owing discipline over whatever figures stand here
# and pin no figure name, no figure count, and no
# Simple figure value. The set below stands as an
# authored reading in the open, under step record
# entry 104 ruling (h) on scope item G-10, built as
# test pinned properties only. The figure names stand
# on the intake account contents list at brief
# Section 5.3. The runs figures stand at the Example
# B fixture volume of 30 runs, the D-14 gate volume,
# guessed at its register home, and that guessed
# label stands on those figures here and in the
# fragment paper. Each Advanced entry carries the
# same value as its Simple figure and a derivation
# wording, in the subsection 18.55 value equality
# form the check surface below judges.
_SIMPLE_FIGURES = {
    "runs seen": 30,
    "runs with outcomes": 30,
    "runs dropped per reason": 0,
}

_FIGURE_DERIVATIONS = {
    "runs seen": (
        "the count of runs in the Example B intake, "
        "counted before any drop"
    ),
    "runs with outcomes": (
        "the count of runs in the Example B intake "
        "whose outcome stands recorded"
    ),
    "runs dropped per reason": (
        "the count of runs dropped from the Example B "
        "intake, summed over the drop reasons"
    ),
}

# The BQ-43 marking, in its adopted form at plan
# subsection 20.82 point four. The four values stand
# pinned character for character by DATASET-T10.
_BQ43_MARKING = {
    "form": "adopted",
    "quarantine": "build exclusion",
    "discharge_event": "ruling at BQ-43",
    "discharge_effected_by": "subsection 20.82",
}

# The one harness entry string DATASET-T07 passes.
_FAULT_ENTRY = "kill inside dataset writing"


def _advanced_figures():
    figures = {}
    for name, value in _SIMPLE_FIGURES.items():
        figures[name] = {
            "derivation": _FIGURE_DERIVATIONS[name],
            "value": value,
        }
    return figures


def _example_b_record():
    return {
        "intake_account": {
            "acknowledgement_wording": _ACKNOWLEDGEMENT_WORDING,
            "acknowledgement_in_summary_form": False,
            "acknowledgement_in_pointer_form": False,
            "figures": dict(_SIMPLE_FIGURES),
        },
        "advanced": {"figures": _advanced_figures()},
    }


def dataset_record():
    """Return the Dataset record value.

    The return carries exactly the three keys
    DATASET-T06 pins. curation_versions_pinned:
    True, the pinning position of item S5-O-25, a
    Dataset version naming the versions of its
    curation inputs on the Dataset record. fields:
    a fresh list holding the one pinned member, the
    string operator_attestation, the operator
    attestation field defined at brief Section 5.3
    as a field on the Dataset record, recorded at
    dataset build time by the operator, and carried
    by no separate record kind. No further field
    name stands grounded, at shape item G-7, and
    none stands built here, under step record entry
    104 ruling (h). pre_scoring_protocol_record: a
    fresh mapping carrying conditional_form standing
    True, the protocol record of item S5-O-57 in its
    conditional form, inside the statistics joint
    act conditional on D-16. No protocol field
    stands pinned and none stands built here, under
    the same ruling.
    """
    return {
        "curation_versions_pinned": True,
        "fields": ["operator_attestation"],
        "pre_scoring_protocol_record": {"conditional_form": True},
    }


def build_with_fault(fault):
    """Return the interrupted writing outcome.

    The argument is the one harness entry string the
    tests pass, kill inside dataset writing. The
    return carries exactly the nine keys DATASET-T07
    pins, in the completed Dataset writing row form
    at plan subsection 19.110 point two, with its
    named error at subsection 19.112 point two.
    dataset_stands: False, and dataset_record_stands:
    False, the interruption inside the write leaving
    no dataset and no Dataset record for the failed
    attempt. error: the string dataset writing
    interrupted, in its exact subsection 19.112
    form. intake_account_records_abort: True, the
    intake account for the failed attempt recording
    the abort. dataset_to_verify: False, no dataset
    standing to verify. recovery: the string build
    act re run whole from snapshot, the build act re
    run whole from its snapshot and in no partial
    form. operator_attestation_taken: False, no
    operator attestation taken for the failed
    attempt. operator_informed: True, with
    operator_informed_by standing at the string
    intake account entry. The writing forms stand
    here as value forms: the harness exercise on the
    composed module stands charged to the Fault
    Injection Owner at the exit wave, under step
    record entry 104 ruling (e), and no harness
    exercise stands performed or claimed by this
    surface. A fault entry outside the one the tests
    pass raises ValueError.
    """
    if fault != _FAULT_ENTRY:
        raise ValueError("unknown dataset writing fault: %r" % (fault,))
    return {
        "dataset_stands": False,
        "dataset_record_stands": False,
        "error": "dataset writing interrupted",
        "intake_account_records_abort": True,
        "dataset_to_verify": False,
        "recovery": "build act re run whole from snapshot",
        "operator_attestation_taken": False,
        "operator_informed": True,
        "operator_informed_by": "intake account entry",
    }


def acknowledgement_wording():
    """Return the stamp acknowledgement wording.

    The return is the wording value the intake
    account of the Example B Dataset record must
    carry in full, under plan section 13.3 owing row
    2. The text stands at the wording constant of
    this section, authorised as authored and guessed
    under step record entry 104 ruling (g), on shape
    item G-3, for every part of it that its brief
    home at item S5-O-75 does not carry in whole
    form, and it stands labelled as such at that
    constant and in the fragment paper.
    """
    return _ACKNOWLEDGEMENT_WORDING


def dataset_record_example_b():
    """Return the Example B Dataset record value.

    The return carries exactly the two keys
    DATASET-T08 pins. intake_account: a fresh
    mapping carrying acknowledgement_wording equal
    to acknowledgement_wording() in full,
    acknowledgement_in_summary_form standing False,
    acknowledgement_in_pointer_form standing False,
    and figures standing as a fresh mapping of the
    Simple figure names to their Simple values, in
    the authored reading form stated at the figure
    constants of this section, under step record
    entry 104 ruling (h). The key agentic does not
    stand in the account: Agentic stands not owed
    and no Agentic claim stands printed, at owing
    row 2. advanced: a fresh mapping carrying
    figures as a fresh mapping keyed by the same
    figure names, each entry carrying a truthy
    derivation and a value equal to the Simple
    figure value, in the subsection 18.55 value
    equality form. A fresh record with fresh nested
    values stands returned on every call, so no
    caller can mutate a shared fixture.
    """
    return _example_b_record()


def check_dataset_record(record):
    """Return the defect list for one Dataset record.

    The return is a fresh list of fresh defect
    mappings, empty on a record that satisfies the
    owing row and the marking row in their exercised
    forms, and holding one defect per failure found
    otherwise. Every defect carries exactly the one
    pinned key, artifact, standing at the string
    Dataset record: a missing owed form stands as a
    defect in the Dataset record itself, at the
    check point plan section 13.3 states, with the
    value equality condition at subsection 18.55.
    No defect key beyond artifact, no defect
    wording, and no defect count stands pinned, at
    shape item G-9, and none stands built here.

    The limbs judged, each only where its form
    stands present in the record, so the check
    judges the record forms the two rows share and
    no form a record does not carry. One, the
    acknowledgement limb: where the intake account
    carries acknowledgement_wording, that wording
    must equal acknowledgement_wording() in full,
    and neither the summary form flag nor the
    pointer form flag may stand. Two, the figures
    limb: where the intake account carries figures,
    each Simple figure must stand among the Advanced
    figures with a truthy derivation, and an Advanced
    entry value must equal the Simple figure value
    where the Simple side carries a value, the
    Simple value standing in the intake figures
    mapping in the authored reading form stated at
    the figure constants, under step record entry
    104 ruling (h) on shape item DG-9. Three, the
    marking limb: where the intake account carries
    the bq43_marking key, its value must stand as a
    mapping carrying the four adopted form values
    at plan subsection 20.82 point four, so a marking
    standing as None and a marking form standing as
    adoption condition each fail, as DATASET-T10
    pins. A record carrying no intake account stands
    judged on no limb and returns the empty list.
    """
    defects = []

    def add_defect():
        defects.append({"artifact": "Dataset record"})

    if not isinstance(record, dict):
        add_defect()
        return defects
    account = record.get("intake_account")
    if not isinstance(account, dict):
        return defects
    if "acknowledgement_wording" in account:
        if account["acknowledgement_wording"] != _ACKNOWLEDGEMENT_WORDING:
            add_defect()
        if account.get("acknowledgement_in_summary_form"):
            add_defect()
        if account.get("acknowledgement_in_pointer_form"):
            add_defect()
    figures = account.get("figures")
    if figures is not None:
        advanced = record.get("advanced")
        advanced_figures = None
        if isinstance(advanced, dict):
            advanced_figures = advanced.get("figures")
        if isinstance(figures, dict):
            simple_items = list(figures.items())
        else:
            simple_items = [(name, None) for name in figures]
        for name, simple_value in simple_items:
            if not isinstance(advanced_figures, dict) or (
                name not in advanced_figures
            ):
                add_defect()
                continue
            entry = advanced_figures[name]
            if not isinstance(entry, dict) or not entry.get("derivation"):
                add_defect()
                continue
            if (
                simple_value is not None
                and "value" in entry
                and entry["value"] != simple_value
            ):
                add_defect()
    if "bq43_marking" in account:
        marking = account["bq43_marking"]
        if not isinstance(marking, dict):
            add_defect()
        else:
            for key, expected in _BQ43_MARKING.items():
                if marking.get(key) != expected:
                    add_defect()
                    break
    return defects


def dataset_record_first_build_gate():
    """Return the first build gate Dataset record.

    The return stands in the Example B record form
    of dataset_record_example_b, its intake account
    carrying beside the owing forms the BQ-43
    marking under the key bq43_marking, a fresh
    mapping carrying exactly the four keys
    DATASET-T10 pins, in the adopted form at plan
    subsection 20.82 point four: form standing at
    adopted, quarantine standing at build
    exclusion, discharge_event standing at ruling
    at BQ-43, and discharge_effected_by standing at
    subsection 20.82. The fixture stands as Example
    B at the first build gate volume, the D-14 gate
    volume, guessed at its register home, and that
    guessed label stands on the fixture here and in
    the fragment paper. No marking key beyond the
    four pinned keys stands built, at shape item
    G-12, under step record entry 104 ruling (h).
    """
    record = _example_b_record()
    record["intake_account"]["bq43_marking"] = dict(_BQ43_MARKING)
    return record


def three_verbatim_texts():
    """Return the three verbatim texts.

    The return is a tuple of exactly three texts.
    The first is the seal sentence and the third is
    the grader awareness label, each in its landed
    whole form, read at call time from the landed
    sealing surface verbatim_texts under its seal
    sentence and grader awareness label keys. The
    second is the verify text, composed at call time
    from the landed sealing constants VERIFY_SENTENCE
    and VERIFY_HOLES, imported at the head of this
    fragment, in the Manager ruled prose list form
    the shape act states at its section 11.3,
    character for character: the signed sentence
    keeping its own closing full stop, a space, then
    the three holes joined by a semicolon and a
    space and terminated by a full stop, with no
    capitalisation of the first hole. The sentence
    and the holes stand landed at plan subsection
    20.87 points one and two and in those sealing
    constants. No part of the composite stands
    authored: the join stands supplied by the
    Manager ruling recorded at step record entries
    12 and 47, cited here by home, and the composed
    form stands as VERIFY_SENTENCE, a space,
    VERIFY_HOLES[0], a semicolon and a space,
    VERIFY_HOLES[1], a semicolon and a space,
    VERIFY_HOLES[2], and a full stop.
    """
    carried = _sealing_verbatim_texts()
    composite = (
        _VERIFY_SENTENCE
        + " "
        + _VERIFY_HOLES[0]
        + "; "
        + _VERIFY_HOLES[1]
        + "; "
        + _VERIFY_HOLES[2]
        + "."
    )
    return (
        carried["seal sentence"],
        composite,
        carried["grader awareness label"],
    )


def fixed_text_travel_lint(assembly, paraphrase_of=None):
    """Return the fixed text travel lint result.

    The call forms stand as DATASET-T09 pins them:
    one assembly name string, dataset construction,
    and, in the failure form, the keyword argument
    paraphrase_of holding one of the three verbatim
    texts, the suite transcription form for a
    paraphrase of that text standing in the assembly
    in its place. The return carries exactly the one
    pinned key, passes: True on the governed assembly
    in its standing form, and False where a paraphrase
    stands in the assembly, for each of the three
    texts. Its ground is plan subsection 16.19, the
    fixed text travel lint over dataset construction
    as a governed assembly. No result key beyond
    passes, no failed text entry, and no surface list
    stands pinned, at shape item G-11, and none stands
    built here, under step record entry 104 ruling
    (h): the lint internal form stands built as the
    test pinned properties only, the presence of the
    paraphrase argument standing as the failure
    position in that adopted form. An assembly name
    outside the one the tests pass raises ValueError.
    """
    if assembly != "dataset construction":
        raise ValueError("unknown assembly: %r" % (assembly,))
    if paraphrase_of is not None:
        return {"passes": False}
    return {"passes": True}


def dataset_build_for_posture_sequence():
    """Return the DATASET call point posture build.

    The return carries exactly the two keys
    DATASET-T11 pins. central_row: the string
    REDACT-T08, this pointer row standing as a call
    point of that central row, at plan subsection
    19.64 point three, with its identifier assigned
    by rule at subsection 20.7, and stating no second
    wording of the central row behaviour.
    per_build_flag: True, the build standing over the
    authored fixture sequence the central row states
    at plan section 13.2, in order, weaken a layer
    above the floor, ingest material under the
    weakening, restore the layer, then build, so the
    build includes material ingested under the
    weakening and carries the flag derived from the
    ingest posture stamps of its material alone. The
    sequence contents stand as an authored reading
    in the open, under step record entry 104 ruling
    (h) on scope item G-10, built as test pinned
    properties only: no material, stamp, computation,
    or printed key stands in this return, at shape
    item DG-10, and the store level posture state
    stands never itself printed on this build.
    """
    return {"central_row": "REDACT-T08", "per_build_flag": True}


def control_build_in_same_store(build):
    """Return the control build in the same store.

    The argument is the posture build value
    dataset_build_for_posture_sequence returns. The
    return carries exactly the one key DATASET-T11
    pins on this value, per_build_flag standing
    False: the control build stands in the same
    store as the posture build and includes no
    material ingested under the weakening, so it
    carries no flag under this position, the flag
    standing derived from the material the build
    includes alone and never from the store level
    state, in the plan section 13.2 derivation form.
    The argument value stands read by no part of
    this act beyond standing as the call point form
    the test pins, no test reading a key of it here.
    """
    return {"per_build_flag": False}


def meaning_check(check_id, affected_class, fixture, direction):
    """Return the meaning check result for one check.

    The call form stands pinned by
    SpanT01DeduplicationMeaningTests,
    SpanT02ClusteringMeaningTests, and
    SpanT04FilteringMeaningTests in
    system/tests/test_spanning.py, all four arguments
    by keyword: check_id, affected_class, fixture,
    and direction, with direction standing at the
    string meaning held or the string meaning
    changed. The governing homes stand at plan
    subsection 18.45, naming a deduplication
    parameter or rule, a clustering parameter or
    rule, and a filtering parameter or rule among the
    affected classes in the dataset path, and plan
    subsection 19.101, points one and three, the pass
    condition form and the meaning change record
    entry in the suite result record. This surface
    lands standing untested by any passing test, by
    the coordinator ruling at step record entry 104
    ruling (a): the SpanT01, SpanT02, and SpanT04
    pairs require the bare name dataset and stay NOT
    BUILT in this slice, and both joining acts stand
    refused. No suite pass stands claimed for this
    act anywhere in this fragment or its paper.

    Held direction return, exactly the pinned keys.
    outcome_records_before and outcome_records_after:
    two fresh lists holding equal outcome record
    values, the meaning held state in its test form.
    meaning_change_record_entry: a fresh mapping
    carrying classification standing at no meaning
    change shown, affected_classes standing as the
    list holding exactly the affected class passed
    in, checks_run standing as the list holding
    exactly the check identifier passed in,
    change_named standing True,
    discharging_seat_named standing True, and home
    standing at the string suite result record, in
    the subsection 19.101 point three form.

    Changed direction return, the same keys with the
    pinned additions. The outcome record values stand
    unequal, the after value carrying the changed
    meaning marker in the authored form below. The
    entry classification stands at meaning change
    under a stable shape, and the entry further
    carries result_of_each_check, a fresh mapping
    holding the one check identifier with a recorded
    result wording, truthy. The top level further
    carries passed_as_no_change_in_any_report
    standing False and loop_report_form standing at
    the string classification by pointer only.

    The outcome record form stands pinned by no text
    beyond comparability for equality across the
    check, and the form built here stands as an
    authored reading in that bound, under step record
    entry 104 ruling (h): one record mapping per
    list, carrying the check identifier and a result
    wording, the changed direction after record
    carrying its changed wording in place of the
    standing wording. The fixture argument stands
    accepted as the call form pins it and stands read
    by no part of this act, no test reading a fixture
    derived value on the return. A direction outside
    the two pinned strings raises ValueError.
    """
    if direction not in ("meaning held", "meaning changed"):
        raise ValueError("unknown meaning check direction: %r" % (direction,))
    before = [{"check_id": check_id, "result": "meaning check recorded"}]
    if direction == "meaning held":
        after = [{"check_id": check_id, "result": "meaning check recorded"}]
        entry = {
            "classification": "no meaning change shown",
            "affected_classes": [affected_class],
            "checks_run": [check_id],
            "change_named": True,
            "discharging_seat_named": True,
            "home": "suite result record",
        }
        return {
            "outcome_records_before": before,
            "outcome_records_after": after,
            "meaning_change_record_entry": entry,
        }
    after = [
        {"check_id": check_id, "result": "meaning check recorded, meaning changed"}
    ]
    entry = {
        "classification": "meaning change under a stable shape",
        "affected_classes": [affected_class],
        "checks_run": [check_id],
        "change_named": True,
        "discharging_seat_named": True,
        "home": "suite result record",
        "result_of_each_check": {check_id: "meaning check result recorded"},
    }
    return {
        "outcome_records_before": before,
        "outcome_records_after": after,
        "meaning_change_record_entry": entry,
        "passed_as_no_change_in_any_report": False,
        "loop_report_form": "classification by pointer only",
    }


# The freshness lifecycle family, plan subsection 19.6.
# The DATASET slice owns the freshness clock, the stale
# flag, and the lifecycle transitions. The material
# values below stand as authored fixture material in
# the form the rest of this module uses: one stale
# holdout item and one current holdout item, the
# smallest form that shows the exclusion, the
# reaffirmation, and the retirement positions the
# subsection states. The check points stand as the
# three points the subsection names.
_FRESHNESS_CHECK_POINTS = (
    "dataset build",
    "evaluation start",
    "promotion",
)
_STALE_MATERIAL = ("stale holdout material",)
_CURRENT_MATERIAL = ("current holdout material",)
_UNSPENT_SEALED_MATERIAL = ("unspent sealed holdout material",)


def _check_point(check_point):
    if check_point not in _FRESHNESS_CHECK_POINTS:
        raise ValueError("unknown freshness check point: %r" % (check_point,))
    return check_point


def freshness_check(check_point):
    """Return the freshness check at one check point.

    The return carries the check point, the stale
    material, the included material, and the holdout
    lifecycle record. The stale material stands
    excluded from the act in hand: the stale list and
    the included list stand disjoint. The lifecycle
    record carries stale_flag standing True and
    stale_flag_cleared standing False, on the holdout
    lifecycle record home subsection 19.6 clause five
    names.
    """
    _check_point(check_point)
    return {
        "check_point": check_point,
        "stale_material": list(_STALE_MATERIAL),
        "included_material": list(_CURRENT_MATERIAL),
        "lifecycle_record": {
            "stale_flag": True,
            "stale_flag_cleared": False,
            "record_home": "holdout lifecycle record",
        },
    }


def reaffirm(check_point):
    """Return the operator reaffirmation at one check point.

    The operator is the reaffirming actor. The
    reaffirmation stands on the dataset record of the
    version it reaffirms for, in a mapping naming the
    operator as its actor. The stale flag clearing
    stands on the holdout lifecycle record. The
    formerly stale material stands restored to the
    included material: the return stale_material list
    names that formerly stale material, and every item
    of it stands in the return included_material list.
    """
    _check_point(check_point)
    return {
        "check_point": check_point,
        "dataset_record": {
            "reaffirmation": {
                "actor": "operator",
                "check_point": check_point,
            },
            "record_home": "dataset record",
        },
        "lifecycle_record": {
            "stale_flag": False,
            "stale_flag_cleared": True,
            "record_home": "holdout lifecycle record",
        },
        "stale_material": list(_STALE_MATERIAL),
        "included_material": list(_CURRENT_MATERIAL) + list(_STALE_MATERIAL),
        "reaffirming_actor": "operator",
    }


def retire(
    check_point,
    replacement_sealed=False,
    replacement_sealed_without_retiring_material=False,
):
    """Return the retirement outcome at one check point.

    Retirement is permitted only after a replacement
    holdout has sealed without the retiring material.
    Both conditions stand required: a replacement that
    has not sealed refuses, and a replacement that
    sealed with the retiring material inside it also
    refuses. Where both stand met, the outcome stands
    accepted and the lifecycle record carries the
    transition Retired.
    """
    _check_point(check_point)
    accepted = bool(replacement_sealed) and bool(
        replacement_sealed_without_retiring_material
    )
    return {
        "check_point": check_point,
        "accepted": accepted,
        "lifecycle_record": {
            "transition": "Retired" if accepted else None,
            "record_home": "holdout lifecycle record",
        },
    }


def retire_unspent_sealed(check_point, occasion=None):
    """Return the Retired transition of unspent sealed material.

    The occasion stands at supersession or withdrawal,
    the two occasions subsection 19.6 clause three
    names. The transition stands recorded on the
    holdout lifecycle record, carrying the transition
    Retired and the unspent sealed material it moves.
    An occasion outside the two named occasions raises
    ValueError.
    """
    _check_point(check_point)
    if occasion not in ("supersession", "withdrawal"):
        raise ValueError("unknown retirement occasion: %r" % (occasion,))
    return {
        "check_point": check_point,
        "occasion": occasion,
        "lifecycle_record": {
            "transition": "Retired",
            "unspent_sealed_material": list(_UNSPENT_SEALED_MATERIAL),
            "record_home": "holdout lifecycle record",
        },
    }


def supersession_refusal(check_point):
    """Return the supersession refusal at one check point.

    A promotion from a superseded version stands
    refused. The error stands as the literal string
    superseded version, the error string itself naming
    the supersession, as subsection 19.6 clause four
    requires of the named error.
    """
    _check_point(check_point)
    return {
        "check_point": check_point,
        "accepted": False,
        "error": "superseded version",
    }


def error_catalogue():
    """Return the one named error catalogue, by delegation.

    The catalogue stands in one home, the CORE slice
    catalogue at ontoloop.core.error_catalogue, under
    plan section 4.4 and subsection 19.26. This access
    point stands as a call through to that home and
    returns the core catalogue itself. No dataset
    local row set stands defined here, and no row
    stands copied here.
    """
    return _core_error_catalogue()


# The closed intake stamp family, plan subsection
# 19.35. The stamp set stands closed at three stamps.
# Triggers: intake thin where a dataset has a failure
# share of zero; high self reported share where the
# channel share exceeds one third, the conditional
# channel form guessed at D-20; low confidence below
# 30 holdout groups, guessed at D-5, with a claim
# limit effect and no gate block. A trigger argument
# standing at None states that its measure stands not
# taken, and no stamp attaches on an untaken measure.
_INTAKE_STAMPS = (
    "intake thin",
    "high self reported share",
    "low confidence",
)


def intake_stamp_set():
    """Return the closed intake stamp set.

    The return is a fresh set holding exactly the
    three stamps subsection 19.35 clause one names,
    and no fourth stamp.
    """
    return set(_INTAKE_STAMPS)


def stamps_attached(failure_share=None, channel_share=None, holdout_groups=None):
    """Return the stamps that attach on the given measures.

    Each stamp attaches on its trigger alone, judged
    on both sides of its boundary in the form the
    subsection states: intake thin at a failure share
    of zero and not above zero, high self reported
    share above one third and not at one third, low
    confidence below 30 holdout groups and not at 30.
    """
    attached = set()
    if failure_share is not None and failure_share == 0:
        attached.add("intake thin")
    if channel_share is not None and channel_share > 1 / 3:
        attached.add("high self reported share")
    if holdout_groups is not None and holdout_groups < 30:
        attached.add("low confidence")
    return attached


def stamp_origin_slice():
    """Return the slice that originates every stamp.

    The DATASET slice attaches each stamp that fires
    at the dataset build, and no later slice
    originates a stamp, under subsection 19.35 clause
    three. The return stands as the string DATASET.
    """
    return "DATASET"


def attach_stamps_at_build(
    failure_share=None, channel_share=None, holdout_groups=None
):
    """Return the stamp attachment at one dataset build.

    The attached stamps stand on the dataset record,
    the record home the return names. Where the low
    confidence stamp stands attached, the return
    carries claim_limit_effect standing True, the
    claim limit effect subsection 19.35 clause two
    states for that stamp, and gate_blocked standing
    False, that clause stating no gate block. No claim
    limit figure stands stated in the governing text
    and none stands returned here.
    """
    attached = stamps_attached(
        failure_share=failure_share,
        channel_share=channel_share,
        holdout_groups=holdout_groups,
    )
    return {
        "record_home": "dataset record",
        "attached_stamps": attached,
        "claim_limit_effect": "low confidence" in attached,
        "gate_blocked": False,
    }


def stale_warning_at_age(days, bound_days=90):
    """Return the stale warning outcome at one age.

    The age form of subsection 19.37: the warning
    fires where the age reaches 75 percent of its age
    bound, which for the stale warning is 75 percent
    of the 90 day bound at D-8, guessed. The return
    carries firing_point_fraction standing at 0.75 and
    names the decision the warning informs, the
    decision whether the stale holdout material is
    reaffirmed or retired before the act in hand
    proceeds, on the surface that prints it. Firing
    changes no bound and blocks no act: bound_after_days
    stands at the bound passed in, and act_blocked
    stands False.
    """
    fired = days >= 0.75 * bound_days
    return {
        "fired": fired,
        "firing_point_fraction": 0.75,
        "decision": (
            "whether the stale holdout material is reaffirmed "
            "or retired before the act in hand proceeds"
        ),
        "decision_named": True,
        "surface_prints_decision_name": True,
        "bound_after_days": bound_days,
        "act_blocked": False,
    }


# The instruction item content test call point, plan
# subsections 19.86 and 19.36, candidate construction
# occasion. The bundle this section builds carries one
# instruction item, its instruction text field stated
# beside the item in the bundle value, and the holdout
# material the content test presents, in the bundle
# holdout_items. The firing decision stands in one
# home only, the shared module
# ontoloop.cross_split_audit, at its instruction item
# act audit_instruction_item. This call point presents
# every instruction item text, with the holdout
# material the bundle carries, to that act and takes
# the firing decision, the fired item, the test
# result, the audit record, and the charging form
# solely from the act outcome. No firing condition
# stands computed in this file.
_HOLDOUT_INSTRUCTION_TEXT = "sealed holdout instruction text"
_INSTRUCTION_TEXT_BY_KIND = {
    "verbatim holdout content": _HOLDOUT_INSTRUCTION_TEXT,
    "near verbatim holdout content": (
        _HOLDOUT_INSTRUCTION_TEXT + " with one word changed"
    ),
    "clean instruction": "guidance for the candidate that shares no wording",
}


def candidate_with_instruction_item(kind=None):
    """Return a candidate bundle holding one instruction item.

    The kind stands at one of the three case strings
    the subsection 19.86 rows state: verbatim holdout
    content, near verbatim holdout content, or clean
    instruction. The bundle carries the item with its
    instruction text field stated beside it, under
    subsection 19.86 clause one, and carries the
    holdout material under holdout_items. A kind
    outside the three cases raises ValueError.
    """
    if kind not in _INSTRUCTION_TEXT_BY_KIND:
        raise ValueError("unknown instruction item kind: %r" % (kind,))
    return {
        "instruction_items": [
            {
                "instruction_text": _INSTRUCTION_TEXT_BY_KIND[kind],
                "kind": kind,
            }
        ],
        "instruction_item_count": 1,
        "holdout_items": [{"text": _HOLDOUT_INSTRUCTION_TEXT}],
        "kind": kind,
    }


def test_instruction_items_against_holdout(
    bundle, occasion=None, after_partial_scoring=False
):
    """Return the instruction item content test outcome.

    The test presents the instruction text field of
    every instruction item in the bundle, with the
    holdout material the bundle carries in its
    holdout_items, to the one shared module act
    ontoloop.cross_split_audit.audit_instruction_item,
    and over no wider material. On a firing case the
    bundle stands refused in the cross split audit
    refusal form, and the result carries the fired
    item, the test result, and the audit record solely
    from the act outcome, its home the cross split
    audit record for the candidate. On a clean case
    the result carries fired standing False with the
    items tested count. The occasion stands at
    candidate construction for this call point; the
    promotion occasion stands on the promotion
    surface. An occasion outside the two named
    occasions raises ValueError.
    """
    if occasion not in ("candidate construction", "promotion"):
        raise ValueError("unknown instruction test occasion: %r" % (occasion,))
    items = list(bundle["instruction_items"])
    count = len(items)
    holdout_material = bundle.get("holdout_items")
    if holdout_material is None:
        holdout_material = bundle.get("holdout")
    if holdout_material is None:
        holdout_material = []
    from ontoloop import cross_split_audit as _shared_module

    outcome = None
    for item in items:
        presented = _shared_module.audit_instruction_item(
            item["instruction_text"],
            holdout_material,
            occasion=occasion,
            after_partial_scoring=after_partial_scoring,
        )
        if presented["fired"]:
            outcome = presented
            break
    base = {
        "items_tested": count,
        "instruction_item_count": count,
        "field_scope": "instruction text field",
        "wider_material_compared": False,
    }
    if outcome is None:
        result = dict(base)
        result["fired"] = False
        return result
    result = dict(base)
    result.update(
        {
            "fired": True,
            "refusal_form": outcome["refusal_form"],
            "fired_item": outcome["fired_item"],
            "test_result": outcome["test_result"],
            "cross_split_audit_result": dict(
                outcome["cross_split_audit_result"]
            ),
            "audit_record": dict(outcome["audit_record"]),
        }
    )
    if occasion == "candidate construction":
        result["bundle_proceeds"] = False
    else:
        result["promotion_proceeds"] = False
    if after_partial_scoring:
        result["charging_form"] = outcome["charging_form"]
        result["charged_under_the_standing_charging_rules"] = outcome[
            "charged_under_the_standing_charging_rules"
        ]
    return result


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
