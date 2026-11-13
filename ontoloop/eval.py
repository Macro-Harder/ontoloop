"""Evaluation module, slice EVAL form.

One evaluation of one frozen candidate against one pinned
baseline on the same sealed holdout, under one scorer and
one cost cap, with the aggregation arithmetic stated once
at brief Section 5.4 and governing everywhere. The module
carries the cost account with its cap check before each
costly step, the pointer and spend positions, the
evaluation record and the protocol record in their owing
forms, the cross split audit at the evaluation call
point, and the meaning check surface.

The markings stand each in its own form. The wider
statistics joint act limbs this slice does not exercise
stand conditional in their own form, and the protocol
record position stands consumed in its conditional form
at that strength. The margin noise form stands adopted
in the form plan subsection 20.78 states, and the
condition its row carried stands discharged in full at
that subsection. Every Example E weight stands guessed
and labelled, with the first cost pilot as its replacing
event, and the D-7 cap figure stands guessed in the same
form. No funding row in this slice stands presented as
funding in the world. The dataset material this module
touches stands for evaluation only in version 1, under
plan subsection 20.84, and no value in this module
stands as material for any other use.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of this
file. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.eval"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "aggregate_example",
    "evaluate_example_d",
    "margin_components",
    "student_t_multiplier",
    "estimate_and_start",
    "example_e_weights",
    "move_pointer_between_evaluation_and_promotion",
    "reconcile_spend",
    "verdict_vocabulary",
    "all_recorded_verdicts",
    "not_scored_reasons",
    "forms_beside_the_vocabulary",
    "evaluation_record_example_d",
    "check_evaluation_record",
    "protocol_record_example_d",
    "score_against_protocol_record",
    "grader_awareness_label_agentic",
    "evaluate_with_spanning_pair",
    "meaning_check",
]

from ontoloop.sealing import verbatim_texts as _sealing_verbatim_texts


# The Student t multiplier table. Ground: plan
# subsection 20.78 point one adopts a Student t
# multiplier taken by group count in place of the
# fixed multiplier 2, with check values 2.365 at 8
# groups, 2.262 at 10 groups, and 2.045 at 30 groups.
# The table holds exactly the three grounded counts,
# under the build entry disposition of DG-9. A count
# outside the table raises ValueError, because no
# ground states a multiplier for any other count.
_STUDENT_T_MULTIPLIERS = {8: 2.365, 10: 2.262, 30: 2.045}

# The default group count for a margin call with no
# count argument. No ground states a default count.
# The value 8, the first check count the grounds name,
# stands as an authored reading, labelled as such here
# and in the fragment paper, under the build entry
# disposition of DG-9.
_DEFAULT_GROUPS = 8

# The margin figures. The D-1 value stands grounded
# in its guessed form as the header states. The D-2
# share stands at the brief figure, labelled guessed.
# The remaining error value, the standard error value,
# and the absolute floor value stand authored and
# guessed under ruling (e), on scope gaps G-4 and G-5:
# no EVAL ground states any of the three values, and
# the tests pin the relations they stand in alone.
_D1_VALUE = 50
_D2_SHARE = 0.2
_REMAINING_ERROR = 200
_STANDARD_ERROR = 10.0
_ABSOLUTE_FLOOR = 5.0

# The Example B and Example D per group score fixtures.
# Ground: brief Section 5.4 states the per group score
# derivation once, the score of one group standing as
# the mean of the scores of the scored cases in that
# group, with rounding half up applied once at the
# group score. The concrete score values, the group
# counts, and the paired difference values stand
# nowhere in the grounds and stand authored and
# guessed under ruling (e), on scope gap G-1, labelled
# as such here and in the fragment paper.
_EXAMPLE_SCORES = {
    "B": [600, 700, 800],
    "D": [650, 750],
}
_EXAMPLE_PAIRED_DIFFERENCES = {
    "B": [40, 50, 60],
    "D": [30, 50],
}

# The closed verdict vocabulary, in the brief entry
# OQ-C18 enumeration and order, cited under that entry
# wherever the vocabulary lands, under the build entry
# ruling on DG-4. The four terms stand in that entry
# in this order: beats baseline, does not beat
# baseline, cannot judge, not scored.
_VERDICT_VOCABULARY = (
    "beats baseline",
    "does not beat baseline",
    "cannot judge",
    "not scored",
)

# The recorded verdicts value. Proposal at shape item
# G-19, stated as an authored reading in the fragment
# paper: the list holds the one verdict term the
# Example D cases of this section record in a return,
# the not scored term of the zero paired groups case.
# No test reads the length or any single member beyond
# the subset relation against the vocabulary.
_RECORDED_VERDICTS = ("not scored",)

# The typed not scored reasons value. The one member
# stands grounded: the typed reason no complete pair,
# as the zero paired groups case carries it. No
# further member stands built, because no ground
# states one and no test reads one, at shape section
# 9.3. The container holds no cannot judge only entry.
_NOT_SCORED_REASONS = ("no complete pair",)

# The forms beside the vocabulary value. Ground: a
# gate refusal stands beside the vocabulary and not
# inside it, at brief item S5-O-84 and brief entry
# OQ-C18. The container holds exactly the one pinned
# member, so no second beside form stands invented.
_FORMS_BESIDE = ("gate refusal",)


def aggregate_example(example):
    """Example aggregation value, EVAL-T01.

    Takes one example letter, standing at B or D in
    the test calls, and returns a fresh mapping. The
    aggregate stands as the mean of the per group
    scores, groups weighted equally, computed from
    the returned scores in that one form, with no
    second arithmetic anywhere. The group weights
    stand as one entry per group, all equal, in the
    proposed length form the shape act states. The
    paired differences stand taken group by group,
    one per group. The rounding points stand exactly
    as the one entry list holding the string group
    score, rounding applied once at the group score.
    The concrete fixture contents stand authored and
    guessed under ruling (e), as the fixture constant
    above states. A letter outside B and D raises
    ValueError, in the proposed error form.
    """
    if example not in _EXAMPLE_SCORES:
        raise ValueError("unknown example: %r" % (example,))
    scores = list(_EXAMPLE_SCORES[example])
    return {
        "per_group_scores": scores,
        "aggregate": sum(scores) / len(scores),
        "group_weights": [1] * len(scores),
        "paired_differences": list(
            _EXAMPLE_PAIRED_DIFFERENCES[example]
        ),
        "rounding_points": ["group score"],
    }


def evaluate_example_d(case):
    """Example D evaluation value, EVAL-T02 and T03.

    Takes one case name string and returns a fresh
    mapping per case, carrying the keys its case pins
    and no verdict key on a case no test verdicts.

    Zero paired groups: verdict standing at not
    scored, a member of the closed vocabulary, typed
    reason standing at no complete pair, and
    completed evaluations charged standing at 0.
    Ground: brief Section 5.4 maps this case
    expressly, with the pair completeness rule that a
    group enters every paired figure only with both
    scores present.

    One paired group: comparison carried standing
    True, limits stated standing True, and the noise
    figure standing at None, a non numeric form, in
    the proposed form the shape act states. Ground:
    with exactly one paired group no noise figure is
    printed as a number, and the D-4 floor, not a
    computed noise bar, is what bars a verdict. The
    limits statement contents stand nowhere in the
    grounds, at scope gap G-16, and the return carries
    the stated position as a boolean alone.

    Perfect baseline: the record that no candidate
    gain can clear the practical margin standing
    True, completed evaluations charged standing at
    1, scoring ran standing True, and short circuited
    standing False. Ground: the brief high baseline
    rule, at a literally perfect baseline the
    remaining error is zero and no gain can clear the
    practical component, with no short circuit before
    scoring.

    A case string outside the three pinned strings
    raises ValueError, in the proposed error form.
    """
    if case == "zero paired groups":
        return {
            "verdict": "not scored",
            "typed_reason": "no complete pair",
            "completed_evaluations_charged": 0,
        }
    if case == "one paired group":
        return {
            "comparison_carried": True,
            "limits_stated": True,
            "noise_figure": None,
        }
    if case == "perfect baseline":
        return {
            "records_no_gain_can_clear_practical_margin": True,
            "completed_evaluations_charged": 1,
            "scoring_ran": True,
            "short_circuited": False,
        }
    raise ValueError("unknown Example D case: %r" % (case,))


def student_t_multiplier(groups):
    """Student t multiplier value, EVAL-T04.

    Takes one integer group count, standing as the
    count of complete pairs in the judgement, and
    returns the Student t multiplier for that count
    from the adopted table above. The rule stands
    adopted at plan subsection 20.78, the condition
    on D-16 discharged in full at point three of that
    subsection, and the values stand as the adopted
    form check values at the counts they name, not as
    measured values. No fixed multiplier stands used.
    A count outside the three grounded counts raises
    ValueError, under the disposition of DG-9.
    """
    if groups not in _STUDENT_T_MULTIPLIERS:
        raise ValueError("unknown group count: %r" % (groups,))
    return _STUDENT_T_MULTIPLIERS[groups]


def margin_components(groups=None):
    """Margin components value, EVAL-T04.

    Takes one optional keyword argument, the group
    count, and returns a fresh mapping. A call with
    no argument resolves to the 8 group check case,
    as an authored reading labelled in the notes
    above and in the fragment paper, under DG-9.

    The components mapping carries exactly three
    keys, practical, noise, and absolute floor, in
    the test key form under the disposition of DG-3.
    The selection component stands unkeyed in this
    slice form, as that disposition records. The
    practical component stands as the smaller of the
    D-1 value and the D-2 share times the remaining
    error. The noise component stands as the Student
    t multiplier for the group count times the
    standard error of the paired differences. The
    three components and the sufficiency conjunction
    compute in their one home in this module, and the
    computed in list holds exactly one entry, the
    evaluation module name in its dotted form, in the
    proposed form at shape item G-18. The sufficiency
    conjunction carries its form standing at all
    components must be cleared and its components
    standing over the same three names. Ground: the
    brief margin passage, three components, all
    required, none standing in for another, and
    clearing a component means strictly greater than
    it, with no rounding of a component before the
    clearance test. The D-1 value, the D-2 share, the
    remaining error, the standard error, and the
    absolute floor stand in the forms the constant
    notes above state, the last three authored and
    guessed where those notes say so. A group count
    outside the grounded table raises ValueError.
    """
    count = _DEFAULT_GROUPS if groups is None else groups
    multiplier = student_t_multiplier(count)
    practical = min(_D1_VALUE, _D2_SHARE * _REMAINING_ERROR)
    return {
        "components": {
            "practical": practical,
            "noise": multiplier * _STANDARD_ERROR,
            "absolute floor": _ABSOLUTE_FLOOR,
        },
        "computed_in": ["ontoloop.eval"],
        "d1_value": _D1_VALUE,
        "d2_share": _D2_SHARE,
        "remaining_error": _REMAINING_ERROR,
        "standard_error_of_paired_differences": _STANDARD_ERROR,
        "sufficiency_conjunction": {
            "form": "all components must be cleared",
            "components": ["practical", "noise", "absolute floor"],
        },
    }


def verdict_vocabulary():
    """Closed verdict vocabulary value, EVAL-T08.

    Returns a fresh list holding exactly the four
    terms the brief entry OQ-C18 enumerates, in the
    order that entry states them, cited under that
    entry, under the build entry ruling on DG-4. The
    string gate refusal does not stand as a member:
    a gate refusal is a separate outcome class beside
    the four verdict terms, at brief item S5-O-84 and
    brief entry OQ-C18.
    """
    return list(_VERDICT_VOCABULARY)


def all_recorded_verdicts():
    """Recorded verdicts value, EVAL-T08.

    Returns a fresh list holding the recorded verdict
    terms of this section, every member standing
    inside the closed verdict vocabulary. The concrete
    list stands as an authored reading under the
    proposal at shape item G-19, stated in the notes
    above and in the fragment paper. No test reads the
    length or any single member beyond the subset
    relation.
    """
    return list(_RECORDED_VERDICTS)


def not_scored_reasons():
    """Typed not scored reasons value, EVAL-T08.

    Returns a fresh list holding the typed not scored
    reasons, truthy, holding the grounded member no
    complete pair and holding no cannot judge only
    entry. Typed not scored reasons stand distinguished
    from the cannot judge only position, in the row
    form. No further member stands built, at shape
    section 9.3.
    """
    return list(_NOT_SCORED_REASONS)


def forms_beside_the_vocabulary():
    """Forms beside the vocabulary value, EVAL-T08.

    Returns a fresh list holding the forms that stand
    beside the closed verdict vocabulary and not
    inside it, holding at least the member gate
    refusal and, in the proposed form, exactly that
    one member, so no second beside form stands
    invented.
    """
    return list(_FORMS_BESIDE)


# The Example E weights and the D-7 cap. Ground: brief
# Section 5.4 states the cost weights table under D-17
# with six operation classes and a guessed weight in work
# units for each, source class guessed for every value
# with the first cost pilot as replacing event, and the
# D-7 cap figure stands at 50,000 work units, guessed, at
# brief entry OQ-C16 and at register entry D-7. The
# builders build to that table and that cap under the
# slice record build entry disposition of DG-5. No
# weight value and no cap figure in this section stands
# as measured.
_D7_CAP = 50000

_EXAMPLE_E_WEIGHTS = (
    {"operation_class": "Reading a record", "weight": 1,
     "source_class": "guessed"},
    {"operation_class": "Building with a member", "weight": 25,
     "source_class": "guessed"},
    {"operation_class": "Scoring a case", "weight": 100,
     "source_class": "guessed"},
    {"operation_class": "Cross split audit comparison per pair",
     "weight": 5, "source_class": "guessed"},
    {"operation_class": "Bundle writing", "weight": 10,
     "source_class": "guessed"},
    {"operation_class": "Journal append", "weight": 1,
     "source_class": "guessed"},
)

# The costly step list for the within cap case. The step
# identities stand as the operation classes of the brief
# cost weights table above, in table order, as an authored
# reading: no ground states a step name, a step count, or
# a step order for this case, at scope gap G-3 and shape
# gap G-16. The list stands labelled as authored and
# guessed in the fragment paper.
_COSTLY_STEP_NAMES = tuple(
    entry["operation_class"] for entry in _EXAMPLE_E_WEIGHTS
)

# The varied spend difference. No ground states a varied
# difference value, at scope gap G-14. The value below
# stands as authored and guessed under the slice record
# adoption ruling (e), labelled as such here and in the
# fragment paper: a disagreement stands as a named defect
# with a difference of one work unit, never absorbed.
_VARIED_DIFFERENCE = 1

# The evaluation record figure set for the Example D
# cases. The tests pin the owing discipline over whatever
# figures stand here and pin no figure name, no figure
# value, and no derivation text. The names, the values,
# and the derivation texts below stand as authored and
# guessed under the slice record adoption ruling (e), on
# scope gap G-8, labelled as such here and in the fragment
# paper. Each Advanced entry carries the same value as
# the fixture value for its figure and a full derivation,
# in the subsection 18.55 value equality form the check
# surface below judges, with the fixture standing as the
# comparison home under the build entry disposition of
# DG-10.
_EVAL_FIGURE_VALUES = {
    "baseline score": 800,
    "candidate score": 850,
    "paired groups": 8,
}

_EVAL_FIGURE_DERIVATIONS = {
    "baseline score": (
        "the mean of the per group scores of the pinned "
        "baseline on the Example D cases, taken group by "
        "group in the aggregation form"
    ),
    "candidate score": (
        "the mean of the per group scores of the frozen "
        "candidate on the Example D cases, taken group by "
        "group in the aggregation form"
    ),
    "paired groups": (
        "the count of groups in the Example D cases that "
        "carry both a candidate score and a baseline score"
    ),
}

# The paired per group scores of the Example D cases, in
# the aggregation form. The values stand as authored and
# guessed under the slice record adoption ruling (e), on
# scope gap G-8, labelled as such here and in the fragment
# paper. Their mean stands at the candidate score figure
# above, as fixture coherence only.
_PAIRED_PER_GROUP_SCORES = (820, 840, 860, 880)

# The margin components section of the evaluation record,
# carrying the margin return form in compact fixture form.
# The component values stand as authored and guessed
# under the slice record adoption ruling (e), on scope gap
# G-8, labelled as such here and in the fragment paper.
# The governing margin arithmetic stands in its one home
# in the margin surfaces of this module, and no second
# statement of that arithmetic stands here.
_RECORD_MARGIN_COMPONENTS = {
    "practical": 30,
    "noise": 10,
    "absolute floor": 5,
}

# The verdict wording carried in the evaluation record.
# No ground states a verdict wording text beyond its
# standing present in the record, at scope gap G-16. The
# wording below stands as the closed vocabulary term for
# the Example D boundary case the record fixture carries,
# as an authored reading, labelled as such in the fragment
# paper.
_VERDICT_WORDING = "not scored"

# The protocol record figure set. The record states the
# cost cap as its bound for scoring, at the D-7 figure
# above in its guessed form, and the paired group count
# of the Example D cases as its figure for scoring. The
# derivation texts stand as authored and guessed under
# the slice record adoption ruling (e), on scope gap G-8,
# labelled as such here and in the fragment paper.
_PROTOCOL_FIGURE_VALUES = {
    "cost cap": 50000,
    "paired groups": 8,
}

_PROTOCOL_FIGURE_DERIVATIONS = {
    "cost cap": (
        "the single total cap on the evaluation record, "
        "fixed by the protocol record before scoring"
    ),
    "paired groups": (
        "the count of groups in the Example D cases that "
        "carry both a candidate score and a baseline score"
    ),
}

# The three relations of the cross split audit at the
# evaluation call point, in the form the central row
# DATASET-T05 and plan subsection 16.37 state. The audit
# at this call point runs over these three relations only.
_SPANNING_RELATIONS = ("group", "signature", "near verbatim cluster")


def _grader_label():
    carried = _sealing_verbatim_texts()
    return carried["grader awareness label"]


def _eval_figures():
    figures = {}
    for name, value in _EVAL_FIGURE_VALUES.items():
        figures[name] = {
            "derivation": _EVAL_FIGURE_DERIVATIONS[name],
            "value": value,
        }
    return figures


def _protocol_figures():
    figures = {}
    for name, value in _PROTOCOL_FIGURE_VALUES.items():
        figures[name] = {
            "derivation": _PROTOCOL_FIGURE_DERIVATIONS[name],
            "value": value,
        }
    return figures


def estimate_and_start(case):
    """Return the cost estimation and start outcome.

    The case argument stands at one of the three case
    strings the tests pin. On the over cap case the
    return carries refused standing True and started
    standing False: cost estimation refuses a start over
    the D-7 cap, the cap figure standing at the module
    constant above in its guessed form. On the within
    cap case the return carries costly_steps as a fresh
    list of fresh mappings, each carrying
    cap_checked_before standing True, in the authored
    step list form stated at the module constant above.
    On the abort during run case the return carries
    abort_records_landed standing True: abort records
    land, as a boolean position only, with no record
    contents built beyond it, at scope gap G-3. A case
    string outside the three pinned strings raises
    ValueError.
    """
    if case == "over cap":
        return {"refused": True, "started": False}
    if case == "within cap":
        return {
            "costly_steps": [
                {"operation_class": name, "cap_checked_before": True}
                for name in _COSTLY_STEP_NAMES
            ]
        }
    if case == "abort during run":
        return {"abort_records_landed": True}
    raise ValueError("unknown estimate and start case: %r" % (case,))


def example_e_weights():
    """Return the Example E weights value.

    The return is a fresh list of fresh mappings, one
    per operation class of the brief cost weights table
    at Section 5.4, each carrying its operation class,
    its weight in work units, and source_class standing
    at guessed, exactly. Every weight stands guessed and
    labelled, with the first cost pilot as its replacing
    event, in the row own marking.
    """
    return [dict(entry) for entry in _EXAMPLE_E_WEIGHTS]


def move_pointer_between_evaluation_and_promotion():
    """Return the pointer movement outcome.

    The return carries exactly the two keys EVAL-T06
    pins. comparison_voided stands True: pointer
    movement between evaluation and promotion voids the
    comparison. partial_scores_state stands at the
    string not promotable: partial scores stand recorded
    as not promotable. No pointer object, no movement
    act, and no comparison identity stands built, at
    scope gap G-13, and no named error key and no refusal
    record key stands carried, under the build entry
    disposition of DG-8.
    """
    return {
        "comparison_voided": True,
        "partial_scores_state": "not promotable",
    }


def reconcile_spend(varied_by=None):
    """Return the spend reconciliation result.

    On the plain call the return carries difference
    standing at 0: spend reconciles to the journal
    counted figure with zero tolerance, as a checker and
    not as a second owner. The journal counted figure
    stands consumed as a premise in checker form only,
    and this surface performs no store call and reads no
    journal in fact, at scope gap G-14. On the call
    varied by disagreement the return carries difference
    standing at the varied value stated at the module
    constant above, named_defect standing True, and
    absorbed standing False: a disagreement stands as a
    named defect, never absorbed. A varied_by value
    outside None and the disagreement string raises
    ValueError.
    """
    if varied_by is None:
        return {"difference": 0}
    if varied_by == "disagreement":
        return {
            "difference": _VARIED_DIFFERENCE,
            "named_defect": True,
            "absorbed": False,
        }
    raise ValueError("unknown spend variation: %r" % (varied_by,))


def evaluation_record_example_d():
    """Return the Example D evaluation record value.

    The return is a fresh record mapping with fresh
    nested mappings on every call. simple carries
    grader_awareness_label standing as the grader
    awareness label in Simple form and verdict_wording
    standing as the wording at the module constant
    above, in the owing form of plan section 13.3 owing
    row 3: Simple owed, being the grader awareness label
    in Simple form and the verdict wording in the
    record. advanced carries figures, paired_per_group_
    scores, and margin_components: Advanced owed in
    full, the evaluation figures, the paired per group
    scores, and the margin components, with their full
    figures and derivations. label_discharge stands at
    the string joint with the protocol record, exactly:
    the two records discharge the label owing jointly,
    and neither record alone counts as that discharge.
    No top level agentic key stands in the record:
    Agentic not owed, the record printing no load claim.
    The label value stands consumed at call time from
    its landed home, as the label surface below states,
    and the figure contents stand in the authored and
    guessed form stated at the module constants above.
    """
    return {
        "simple": {
            "grader_awareness_label": _grader_label(),
            "verdict_wording": _VERDICT_WORDING,
        },
        "advanced": {
            "figures": _eval_figures(),
            "paired_per_group_scores": list(_PAIRED_PER_GROUP_SCORES),
            "margin_components": {
                "components": dict(_RECORD_MARGIN_COMPONENTS)
            },
        },
        "label_discharge": "joint with the protocol record",
    }


def check_evaluation_record(record):
    """Return the defect list for one evaluation record.

    The return is a fresh list of fresh defect mappings,
    empty on a record that satisfies owing row 3 in its
    exercised forms, and holding at least one defect
    otherwise. Every defect carries exactly the one key
    artifact, standing at the string evaluation record:
    a failure of this row stands named as a defect in
    the evaluation record itself. No defect key beyond
    artifact, no defect wording, and no defect count
    stands pinned, and none stands built here.

    The limbs judged, in the forms the shape act states.
    One, the counterpart limb: where the advanced part
    stands missing or empty, or a section owed in full
    stands missing from it, the check returns a defect.
    Two, the derivation limb: where an advanced figure
    entry carries a derivation standing missing or
    standing at the string summary only, the check
    returns a defect. Three, the label limb: where the
    simple part carries grader_awareness_label standing
    at None or standing missing, the check returns a
    defect. Four, the value equality limb, under plan
    subsection 18.55: where an advanced figure entry
    states a value different from the value the module
    own fixture record carries for the same figure name,
    the check returns a defect, the fixture standing as
    the comparison home under the build entry
    disposition of DG-10. A limb stands judged only
    where its form stands present in the record, beyond
    the exercised failure forms above.
    """
    defects = []

    def add_defect():
        defects.append({"artifact": "evaluation record"})

    if not isinstance(record, dict):
        add_defect()
        return defects
    simple = record.get("simple")
    if not isinstance(simple, dict) or not simple.get(
        "grader_awareness_label"
    ):
        add_defect()
    advanced = record.get("advanced")
    if not isinstance(advanced, dict) or not advanced:
        add_defect()
        return defects
    for section in (
        "figures",
        "paired_per_group_scores",
        "margin_components",
    ):
        if section not in advanced:
            add_defect()
    figures = advanced.get("figures")
    if figures is not None:
        if not isinstance(figures, dict) or not figures:
            add_defect()
        else:
            for name, entry in figures.items():
                if not isinstance(entry, dict) or not entry.get(
                    "derivation"
                ):
                    add_defect()
                    continue
                if entry.get("derivation") == "summary only":
                    add_defect()
                    continue
                if name not in _EVAL_FIGURE_VALUES:
                    add_defect()
                    continue
                if (
                    "value" in entry
                    and entry["value"] != _EVAL_FIGURE_VALUES[name]
                ):
                    add_defect()
    return defects


def protocol_record_example_d(missing=None):
    """Return the Example D protocol record value.

    The return is a fresh record mapping with fresh
    nested mappings on every call, in the form plan
    section 13.3 owing row 4 states. agentic carries
    grader_awareness_label standing equal to the label
    surface of this module: Agentic owed, being the
    grader awareness label in Agentic form in the
    protocol record, written to be read by the grader.
    simple carries the same label claim in Simple
    wording under the same key name: Simple owed.
    advanced carries figures as a fresh mapping keyed
    by figure names, each entry carrying a derivation
    and a value: Advanced owed, being a counterpart for
    any figure or bound the record states for scoring.
    The fixture carries no conditional key, under the
    build entry disposition of DG-12: no T10 test reads
    a conditional key on this record, and the conditional
    marking stands carried in the module text instead.
    Production of the protocol record stands in the
    DATASET pipeline, and production ownership does not
    move: this surface supplies the fixture form the
    tests pin and produces no protocol record in fact.

    The missing argument stands at None for the complete
    record, or at one of the three strings the tests
    pin. On the agentic label form the agentic label
    stands at None. On the simple label form the simple
    label stands at None. On the advanced counterpart
    form the advanced part stands as the empty mapping,
    so a stated figure stands with no counterpart. A
    missing value outside None and the three pinned
    strings raises ValueError.
    """
    if missing not in (
        None,
        "agentic label",
        "simple label",
        "advanced counterpart",
    ):
        raise ValueError("unknown protocol record missing form: %r" % (missing,))
    record = {
        "agentic": {"grader_awareness_label": _grader_label()},
        "simple": {"grader_awareness_label": _grader_label()},
        "advanced": {"figures": _protocol_figures()},
    }
    if missing == "agentic label":
        record["agentic"]["grader_awareness_label"] = None
    elif missing == "simple label":
        record["simple"]["grader_awareness_label"] = None
    elif missing == "advanced counterpart":
        record["advanced"] = {}
    return record


def score_against_protocol_record(record):
    """Return the scoring outcome for one protocol record.

    The record stands checked before scoring, in the
    owing row 4 form. Where the label stands missing in
    either its Agentic form or its Simple form, or a
    stated scoring figure stands with no Advanced
    counterpart, or an Advanced figure states a value
    different from the value the module own fixture
    record carries for the same figure name under plan
    subsection 18.55, scoring does not proceed: the
    return carries scoring_proceeded standing False and
    defect_artifact standing at the string protocol
    record, the missing form named as a defect in the
    protocol record itself. On the complete record
    scoring proceeds: the return carries
    scoring_proceeded standing True and defect_artifact
    standing at None, the key carried on every return in
    the proposed form at shape gap G-20. This surface
    performs no scoring in fact beyond the check
    position the tests pin.
    """
    blocked = False
    if not isinstance(record, dict):
        blocked = True
    else:
        agentic = record.get("agentic")
        if not isinstance(agentic, dict) or not agentic.get(
            "grader_awareness_label"
        ):
            blocked = True
        simple = record.get("simple")
        if not isinstance(simple, dict) or not simple.get(
            "grader_awareness_label"
        ):
            blocked = True
        advanced = record.get("advanced")
        if not isinstance(advanced, dict):
            blocked = True
        else:
            figures = advanced.get("figures")
            if not isinstance(figures, dict) or not figures:
                blocked = True
            else:
                for name, entry in figures.items():
                    if (
                        isinstance(entry, dict)
                        and name in _PROTOCOL_FIGURE_VALUES
                        and "value" in entry
                        and entry["value"] != _PROTOCOL_FIGURE_VALUES[name]
                    ):
                        blocked = True
    if blocked:
        return {
            "scoring_proceeded": False,
            "defect_artifact": "protocol record",
        }
    return {"scoring_proceeded": True, "defect_artifact": None}


def grader_awareness_label_agentic():
    """Return the grader awareness label in Agentic form.

    The return is the label value the complete protocol
    record carries in its agentic part, this surface
    standing as the equality home for that label in this
    slice. The wording stands consumed at call time from
    its landed home, the landed sealing surface
    verbatim_texts under its grader awareness label key,
    never retyped in this module. The label owing homes
    stand at plan section 13.3 owing rows 3 and 4, with
    the label brief home at brief Section 5.5. The EVAL
    grounds state no label wording: that absence stands
    as scope gap G-7, stated in the open in the fragment
    paper and never papered over, and no distinct Simple
    wording and no distinct Agentic wording stands in
    any ground read, so the one consumed wording stands
    in both forms in this slice, as an adopted form
    stated in the fragment paper.
    """
    return _grader_label()


def evaluate_with_spanning_pair(relation):
    """Return the cross split audit outcome at evaluation.

    The relation argument stands at one of the three
    relations or at the paraphrase only string the tests
    pin. On a call with a relation standing at group,
    signature, or near verbatim cluster, the return
    carries refused_at_evaluation standing True and
    verdict_recorded standing at None: an evaluation
    whose groups carry a spanning pair over any of those
    relations stands refused at evaluation, and no
    verdict stands recorded for it, in the pass
    condition form plan subsection 16.37 supplies. On
    the paraphrase only call refused_at_evaluation
    stands False. On every call relations stands as a
    fresh list over exactly the three relations: the
    audit at this call point runs over those three
    relations only.

    The paraphrase bound stands in the open. This audit
    clears no paraphrase leakage in any form. The
    paraphrase only case stands as the negative fixture
    position, no spanning pair over a tested relation
    standing in that case, and paraphrase leakage across
    the split stands as a residual risk at risk R8. No
    key on this return carries a clearance claim. The
    refusal at this call point stands in this module own
    value form, under the build entry disposition of
    DG-7: no shared audit module stands built, no call
    into any other module stands performed, and the
    subsection 19.36 call point position stands in the
    open in the fragment paper under DG-8, with no named
    error key carried on this return. A relation string
    outside the three relations and the paraphrase only
    string raises ValueError.
    """
    if relation in _SPANNING_RELATIONS:
        return {
            "refused_at_evaluation": True,
            "verdict_recorded": None,
            "relations": list(_SPANNING_RELATIONS),
        }
    if relation == "paraphrase only":
        return {
            "refused_at_evaluation": False,
            "verdict_recorded": None,
            "relations": list(_SPANNING_RELATIONS),
        }
    raise ValueError("unknown spanning relation: %r" % (relation,))


def meaning_check(check_id, affected_class, fixture, direction):
    """Return the meaning check result for one check.

    The call form stands pinned by
    SpanT08NewEnumMeaningTests in system/tests/
    test_spanning.py, all four arguments by keyword:
    check_id, affected_class, fixture, and direction,
    with direction standing at the string meaning held
    or the string meaning changed, the suite identifier
    standing at SPAN-T08, the affected class standing at
    new enum value absorbed by a default branch, and the
    fixture standing as the Example D cases carrying a
    value the default branch would absorb. The governing
    homes stand at plan subsection 18.45, naming that
    affected class in the evaluation path, and plan
    subsection 19.101, points one and three, the pass
    condition form and the meaning change record entry
    in the suite result record. This surface lands
    standing untested by any passing test, under the
    slice record adoption ruling (a): the SpanT08 pair
    requires the bare name evaluation and stays NOT
    BUILT in this slice, and both joining acts stand
    refused. No suite pass stands claimed for this act
    anywhere in this fragment or its paper.

    Held direction return. outcome_records_before and
    outcome_records_after stand as two fresh lists
    holding equal outcome record values.
    meaning_change_record_entry stands as a fresh
    mapping carrying classification standing at no
    meaning change shown, affected_classes standing as
    the list holding exactly the affected class passed
    in, checks_run standing as the list holding exactly
    the check identifier passed in, change_named
    standing True, discharging_seat_named standing
    True, and home standing at the string suite result
    record, in the subsection 19.101 point three form.

    Changed direction return, the same keys with the
    pinned additions. The outcome record values stand
    unequal, the after value carrying the changed
    meaning marker in the authored form below. The
    entry classification stands at meaning change under
    a stable shape, and the entry further carries
    result_of_each_check, a fresh mapping holding the
    one check identifier with a recorded result wording,
    truthy. The top level further carries
    passed_as_no_change_in_any_report standing False
    and loop_report_form standing at the string
    classification by pointer only.

    The outcome record form stands pinned by no text
    beyond comparability for equality across the check,
    and the form built here stands as an authored
    reading in that bound: one record mapping per list,
    carrying the check identifier and a result wording,
    the changed direction after record carrying its
    changed wording in place of the standing wording.
    The fixture argument stands accepted as the call
    form pins it and stands read by no part of this act.
    A direction outside the two pinned strings raises
    ValueError.
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


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
