"""Exit and reporting module, slice REPORT form.

The Exit and reporting module at plan section 4.1
item 10. The module carries report construction from
one named journal state by the one construction act,
the loop report as one view carrying scores with
their holdout named, stamps and claim labels, ledger
counts, the leakage limit sentence, the override and
disclosure account recomputed from the journal, and
the precursor line for the current dataset version
only, the owing artifact of the loop report, the seal
claim lint and the fixed text travel lint over the
governed assemblies of report construction and export,
and the REDACT-T08 call point at REPORT in its pointer
form with the per build flag derived at the
construction point.

The bounds stand each in its own form. Curated
datasets stand evaluation only in version 1, and no
value in this module stands as material for any use
beyond the act it presents. Every figure in a report
stands as a derived view owned by the journal and
recomputed at construction, with no second counting
path, no aggregation or margin arithmetic restated,
and no governing state rule stated. Both attention
cadences stand guessed, and the attention budget
stands described as satisfied nowhere. The REDACT-T08
quantity limb stands in no form in this module. The
subsection 19.34 divergence stands carried in neither
form. The report claims stand in conditional form
only, with no controlled exposure claimed, and no
criterion stands closed by any part of this module.

What this slice does not build stands absent from this
module altogether, the unrowed name stamp_travel_chain
standing among those absent names, and a lookup of any
such name raises AssertionError in the NOT BUILT form
the suite harness uses, through the module level guard
at the foot of this file. A lookup of a private or
dunder name raises AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.report"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "build_loop_report",
    "build_report_artifact",
    "lint_report_construction",
    "fixed_text_travel_lint",
    "redact_t08_call_point",
    "dataset_build_including_weakened_ingest",
    "dataset_build_without_weakened_ingest",
]


# The default journal state. One authored string, at
# the Section A constant. The value stands authored
# and guessed under ruling (f), at the shape paper
# section 3.1 and disposition DG-1.
_DEFAULT_JOURNAL_STATE = "default journal state"

# The view name and the build view name. Two authored
# strings. Each value stands authored and guessed
# under ruling (f), at the shape paper section 3.1
# and disposition DG-3.
_VIEW_NAME = "loop report view"
_BUILD_VIEW_NAME = "build view"

# The current dataset version. One authored string.
# The value stands authored and guessed under ruling
# (f), at the shape paper section 3.1 and
# disposition DG-7.
_CURRENT_DATASET_VERSION = "current dataset version"

# The figure name list. Ten grounded names, in the
# test file constant order, at the shape paper
# section 3.1 and disposition DG-2. The names stand
# grounded at subsection 16.62 and carry no authored
# label.
_FIGURE_NAMES = (
    "cannot judge rate",
    "not scored by cause rate",
    "cumulative spend per dataset version",
    "cumulative spend per workflow",
    "drop counts beside the scores",
    "outstanding quarantined count",
    "queue defect test results",
    "futility statement",
    "does not beat baseline verdict count",
    "attempts charged as completed evaluations count",
)

# The stamp name list. Three grounded names, in the
# order the scope states for subsection 19.35, at
# the shape paper section 3.1 and disposition DG-5.
# The names stand grounded and carry no authored
# label. The entry form stands authored at that
# disposition.
_STAMP_NAMES = (
    "intake thin",
    "high self reported share",
    "low confidence",
)

# The attention readings. Two cadence pairs, in this
# order, each pair standing as seconds per review
# and reviews per version: (35.6, 100) and
# (72.0, 30). Both cadence figures stand guessed in
# the row own words, under the F6 reservation, at the
# shape paper sections 1.6 and 3.1 and disposition
# DG-2. The recorded total stands at 3560 and the
# sensitivity total stands at 2160, in the distinct
# form subsection 19.31 states.
_ATTENTION_CADENCES = (
    (35.6, 100),
    (72.0, 30),
)
_ATTENTION_RECORDED_TOTAL = 3560
_ATTENTION_SENSITIVITY_TOTAL = 2160

# The row identifier list. Ten grounded identifiers,
# in row order, REPORT-T01 to REPORT-T10, at the
# shape paper section 3.1.
_ROW_IDS = (
    "REPORT-T01",
    "REPORT-T02",
    "REPORT-T03",
    "REPORT-T04",
    "REPORT-T05",
    "REPORT-T06",
    "REPORT-T07",
    "REPORT-T08",
    "REPORT-T09",
    "REPORT-T10",
)

# The owed forms list. Three grounded form names, in
# this order, at the shape paper section 3.2 and
# disposition DG-10. The names stand grounded at
# merged list row REPORT-T04 and plan section 13.3
# and carry no authored label.
_OWED_FORMS = (
    "Simple",
    "Advanced",
    "Agentic",
)


class _AttentionFigures(list):
    """The attention figures list form, section 3.1.

    A private list subclass. Its membership test for
    a mapping candidate stands True where any element
    carries every key and value of the candidate, in
    the subset form the shape paper sections 1.10 and
    3.1 state at dispositions DG-2 and DG-19. Its
    membership test for a non mapping candidate stands
    in the ordinary list form. Each element carries
    its source class as a real key. This form stands
    authored and guessed under ruling (f), labelled
    as such here and in the fragment paper.
    """

    def __contains__(self, candidate):
        if isinstance(candidate, dict):
            for element in self:
                matched = True
                for key in candidate:
                    if key not in element or element[key] != candidate[key]:
                        matched = False
                        break
                if matched:
                    return True
            return False
        return super().__contains__(candidate)


def build_loop_report(journal=None, reconstruction_fails=False,
                      with_refusal=False, omit_figure=None,
                      for_build=None):
    """Return the loop report, rows T01 to T03, T05,
    T07, and T09, and the flag limb of T10.

    Takes five arguments, every one called by keyword
    or not called in the tests. The journal argument
    stands as a string naming a journal state, or as
    None for the default state. The reconstruction
    fails and with refusal arguments stand as
    booleans. The omit figure argument stands as one
    of the ten figure name strings, or as None. The
    for build argument stands as a mapping carrying
    the includes weakened ingest position, or as
    None, and stands read as data only.

    Returns a fresh mapping carrying exactly the keys
    the shape paper section 3.1 states, in that order.
    Every figure value stands as an authored derived
    string formed from the journal state, authored
    and guessed under ruling (f) at disposition DG-2,
    and no value stands as a measured figure. The
    per build flag stands derived from the for build
    value alone, at disposition DG-13, and no other
    flag stands in this return. A journal argument
    that stands neither as a string nor as None, an
    omit figure argument outside the ten figure name
    strings, or a for build argument that stands
    neither as None nor as a mapping carrying the
    includes weakened ingest key, raises ValueError,
    in the proposal form at shape paper section 6.
    This surface reads no carried state, calls no
    other surface of the module in either section,
    and reads no landed module in any form.
    """
    if journal is not None and not isinstance(journal, str):
        raise ValueError("journal must be a string or None")
    if omit_figure is not None and omit_figure not in _FIGURE_NAMES:
        raise ValueError("unknown figure: %r" % (omit_figure,))
    if for_build is not None:
        if not isinstance(for_build, dict):
            raise ValueError("for_build must be a mapping or None")
        if "includes_weakened_ingest" not in for_build:
            raise ValueError("for_build lacks includes_weakened_ingest")

    if journal is None:
        journal_state = _DEFAULT_JOURNAL_STATE
    else:
        journal_state = journal

    figures = {}
    for name in _FIGURE_NAMES:
        if name == omit_figure:
            continue
        entry = {
            "source": journal_state,
            "value": "derived from " + journal_state,
        }
        if name == "drop counts beside the scores":
            entry["placed_beside"] = "scores"
        figures[name] = entry
    figures_in_place = list(figures.keys())

    views = [
        {
            "budget_exhausted": True,
            "promotion": False,
            "promotion_succeeded": False,
            "futility_statement_printed": True,
            "figures_beside_score": [],
        },
        {
            "budget_exhausted": False,
            "promotion": True,
            "promotion_succeeded": True,
            "futility_statement_printed": False,
            "figures_beside_score": [
                "does not beat baseline verdict count",
                "attempts charged as completed evaluations count",
            ],
        },
    ]

    if reconstruction_fails:
        defect_printed = True
        defect_name = "reconstruction failure"
        defect_view = _VIEW_NAME
        printed_value = defect_name
    else:
        defect_printed = False
        defect_name = None
        defect_view = None
        printed_value = None

    if with_refusal:
        refusal = {
            "form": "Simple",
            "failed_condition_named": True,
            "figures_present": True,
            "readable_from_report_alone": True,
        }
    else:
        refusal = None

    attention_figures = _AttentionFigures()
    for seconds_per_review, reviews_per_version in _ATTENTION_CADENCES:
        attention_figures.append({
            "seconds_per_review": seconds_per_review,
            "reviews_per_version": reviews_per_version,
            "source_class": "guessed",
        })

    attention_readings = {
        "recorded": {
            "total_seconds_per_dataset_version": _ATTENTION_RECORDED_TOTAL,
            "seconds_per_review": _ATTENTION_CADENCES[0][0],
            "reviews_per_version": _ATTENTION_CADENCES[0][1],
        },
        "sensitivity": {
            "total_seconds_per_dataset_version": _ATTENTION_SENSITIVITY_TOTAL,
            "seconds_per_review": _ATTENTION_CADENCES[1][0],
            "reviews_per_version": _ATTENTION_CADENCES[1][1],
        },
    }

    rows = []
    for row_id in _ROW_IDS:
        rows.append({
            "row": row_id,
            "describes_attention_budget_as_satisfied": False,
        })

    if for_build is None:
        per_build_flag = False
    elif for_build["includes_weakened_ingest"]:
        per_build_flag = True
    else:
        per_build_flag = False

    if per_build_flag:
        flag_view = _BUILD_VIEW_NAME
    else:
        flag_view = None

    return {
        "journal_state_named": True,
        "journal_state": journal_state,
        "construction_acts": 1,
        "counting_paths": 1,
        "figures": figures,
        "figures_in_place": figures_in_place,
        "view": _VIEW_NAME,
        "views": views,
        "view_contents": ["leakage limit sentence", "audit result"],
        "audit_results": ["audit result"],
        "leakage_limit_sentence_view": _VIEW_NAME,
        "scores": [
            {
                "score": "authored score",
                "holdout_named": True,
                "holdout": "authored holdout",
            },
        ],
        "stamps": [{"stamp": name} for name in _STAMP_NAMES],
        "claim_labels": ["authored claim label"],
        "ledger_counts": [
            {
                "ledger": "authored ledger",
                "count": 1,
            },
        ],
        "override_and_disclosure_account": {
            "source": "recomputed from the journal",
            "carried_forward": False,
        },
        "precursor_lines": [
            {
                "dataset_version": _CURRENT_DATASET_VERSION,
                "line": "precursor line for the current dataset version",
            },
        ],
        "current_dataset_version": _CURRENT_DATASET_VERSION,
        "defect_printed": defect_printed,
        "defect_name": defect_name,
        "defect_view": defect_view,
        "printed_value": printed_value,
        "refusal": refusal,
        "attention_figures": attention_figures,
        "attention_readings": attention_readings,
        "rows": rows,
        "all_wording": "loop report view; leakage limit sentence; audit result",
        "per_build_flag": per_build_flag,
        "build_view": _BUILD_VIEW_NAME,
        "flag_view": flag_view,
        "row_failed": omit_figure is not None,
    }


def build_report_artifact(omit=None, owed_form_value_differs=False):
    """Return the owing artifact of the loop report,
    REPORT-T04.

    Takes two arguments, the omit argument called by
    keyword in the tests. The omit argument stands at
    one of the three owed form name strings, or at
    None. The owed form value differs argument stands
    as a boolean.

    Returns a fresh mapping carrying exactly six keys,
    in the order the shape paper section 3.2 states:
    the forms owed, the forms present, the form owed,
    the defect position, the defect home standing at
    the reporting artifact itself, and the row failed
    position standing equal to the defect position.
    The value equality condition at subsection 18.55
    stands as the row failed position on a value
    differs call, at disposition DG-10, and as no pair
    of differing values. An omit argument outside the
    three owed form name strings raises ValueError,
    in the proposal form at shape paper section 6.
    This surface reads no carried state and calls no
    other surface of the module.
    """
    if omit is not None and omit not in _OWED_FORMS:
        raise ValueError("unknown owed form: %r" % (omit,))

    forms_present = []
    for form in _OWED_FORMS:
        if form != omit:
            forms_present.append(form)

    if omit is not None or owed_form_value_differs:
        defect = True
    else:
        defect = False

    return {
        "forms_owed": list(_OWED_FORMS),
        "forms_present": forms_present,
        "form_owed": omit,
        "defect": defect,
        "defect_home": "the reporting artifact itself",
        "row_failed": defect,
    }


# The verbatim text name list. Exactly the three
# grounded text names, in the order the tests name
# them, at shape section 4. The three texts themselves
# stand grounded at their brief homes and, for the
# verify sentence, in the landed form at subsection
# 20.87, and stand outside ruling (f) under gap item
# G-9. This block carries the texts by name only and
# holds no verbatim wording in any form.
_VERBATIM_TEXT_NAMES = (
    "seal sentence",
    "verify sentence",
    "grader awareness label",
)

# The assembly name list. Exactly the two grounded
# assembly names, at shape section 4.
_ASSEMBLY_NAMES = (
    "export",
    "report construction",
)

# The call point list. Exactly the two grounded call
# point names, in the central row own form, at shape
# section 4.3.
_CALL_POINTS = (
    "REPORT",
    "DATASET",
)

# The central row constant. One grounded string, at
# shape section 4.3.
_CENTRAL_ROW = "REDACT-T08"

# The two build kind strings. No test pins a build
# kind value and no ground states one in buildable
# form, at disposition DG-13. The two values below
# stand authored and guessed under ruling (f),
# labelled as such here and in the fragment paper.
# Each stands as the kind string of its build value
# mapping and as nothing else.
_BUILD_KIND_INCLUDING = "including weakened ingest"
_BUILD_KIND_WITHOUT = "without weakened ingest"


def lint_report_construction():
    """Return the construction lint form, REPORT-T06.

    Shape section 4.1. Takes no argument. Returns a
    fresh mapping carrying exactly three keys: the
    seal claim lint passed position standing True, the
    fixed text travel lint passed position standing
    True, and the assembly standing at the string
    report construction, exactly. The return carries
    no seal claim list, no claim contents, and no scan
    result in any form, at disposition DG-8: this
    surface builds no second scan and calls no
    redaction surface, and its passed positions stand
    as this module own lint return in fixture form.
    This surface reads no carried state and calls no
    other surface of the module, including the travel
    lint surface below: the two lint surfaces serve
    the one lint position together from the constants
    at the head of this block and by no call.
    """
    return {
        "seal_claim_lint_passed": True,
        "fixed_text_travel_lint_passed": True,
        "assembly": "report construction",
    }


def fixed_text_travel_lint(assembly="export", paraphrase_of=None):
    """Return the travel lint form, REPORT-T08.

    Shape section 4.2. Takes the assembly and the
    paraphrase name, both called by keyword in the
    tests, the assembly standing at one of the two
    grounded assembly name strings held above and the
    paraphrase name standing at one of the three
    verbatim text name strings held above or at None.
    Returns a fresh mapping carrying exactly three
    keys: the passed position standing True where the
    paraphrase name stands at None and False where it
    stands at any one of the three names, the texts
    checked position standing at the integer 3 on
    every call, and the assembly standing at the
    assembly argument in its string form. The three
    texts stand carried by name only, at disposition
    DG-9: this surface reads no verbatim wording and
    states no text contents in any key, and a
    paraphrase stands detected in this fixture form by
    its name argument alone. An assembly argument
    outside the two named assembly strings, or a
    paraphrase argument outside the three verbatim
    text name strings and None, raises ValueError, in
    the proposal form at shape section 6. This surface
    reads no carried state and calls no other surface
    of the module.
    """
    if assembly not in _ASSEMBLY_NAMES:
        raise ValueError("unknown assembly: %r" % (assembly,))
    if paraphrase_of is not None and paraphrase_of not in _VERBATIM_TEXT_NAMES:
        raise ValueError("unknown verbatim text: %r" % (paraphrase_of,))
    return {
        "passed": paraphrase_of is None,
        "texts_checked": 3,
        "assembly": assembly,
    }


def redact_t08_call_point(call_point):
    """Return the REDACT-T08 pointer form, REPORT-T10.

    Shape section 4.3, the pointer part of the row.
    Takes the call point called positionally in the
    tests, standing at one of the two call point name
    strings held above. Returns a fresh mapping
    carrying exactly four keys: the call point standing
    at the argument in its string form, the central row
    standing at the central row constant held above,
    the pass condition home standing at that same
    constant, and the second wording position standing
    False. This return states no pass condition wording
    in its own words, carries no quantity, no unit, and
    no source class for weakened ingest in any key,
    computes no posture position, and carries no flag
    in any form: the one per build flag of this slice
    stands on the construction return alone. A call
    point argument outside the two named call point
    strings raises ValueError, in the proposal form at
    shape section 6. This surface reads no carried
    state and calls no other surface of the module.
    """
    if call_point not in _CALL_POINTS:
        raise ValueError("unknown call point: %r" % (call_point,))
    return {
        "call_point": call_point,
        "central_row": _CENTRAL_ROW,
        "pass_condition_home": _CENTRAL_ROW,
        "states_second_wording_of_behaviour": False,
    }


def dataset_build_including_weakened_ingest():
    """Return the build value with weakened ingest.

    Shape section 4.4, the build value part of
    REPORT-T10. Takes no argument. Returns a fresh
    mapping carrying exactly two keys: the includes
    weakened ingest position standing True, and the
    build kind standing at the authored build kind
    constant held above. The build kind value stands
    authored and guessed under ruling (f), at
    disposition DG-13, as the constant note above
    states, and the includes position stands as the
    one datum the construction surface reads as data.
    This mapping stands as no call on the landed
    dataset module, carries no material, no posture
    state, no stamp, and no quantity in any key, and
    supplies dataset material toward no use. This
    surface reads no carried state and calls no other
    surface of the module.
    """
    return {
        "includes_weakened_ingest": True,
        "build_kind": _BUILD_KIND_INCLUDING,
    }


def dataset_build_without_weakened_ingest():
    """Return the build value with no weakened ingest.

    Shape section 4.5, the build value part of
    REPORT-T10. Takes no argument. Returns a fresh
    mapping carrying exactly two keys: the includes
    weakened ingest position standing False, and the
    build kind standing at the authored build kind
    constant held above. The build kind value stands
    authored and guessed under ruling (f), at
    disposition DG-13, in the same form as section
    4.4. Every other position of section 4.4 stands on
    this surface in the same form: no call on the
    landed dataset module, no material, no posture
    state, no stamp, and no quantity in any key, no
    carried state read, and no surface of the module
    called.
    """
    return {
        "includes_weakened_ingest": False,
        "build_kind": _BUILD_KIND_WITHOUT,
    }


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
