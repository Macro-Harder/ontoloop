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
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of
this file. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
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
    "stamp_travel_chain",
    "production_report_form",
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


def _record_measure(text):
    """Return a deterministic measure computed from one record text.

    The measure is the sum, over the characters of the
    text, of the character code weighted by its one
    based position. It is computed from the material
    on every call and stands in no table.
    """
    total = 0
    for index, char in enumerate(text):
        total += (index + 1) * ord(char)
    return total


def _journal_records(journal, journal_state):
    """Return the journal material as a list of record texts.

    A string journal stands as its non empty lines, or
    as one record where it carries no line break. A
    sequence journal stands as its items in text form.
    A mapping journal stands as the text forms of the
    values of its records entry where it carries one,
    and otherwise as the text form of the mapping
    itself. The default state stands as one record.
    """
    if journal is None:
        return [journal_state]
    if isinstance(journal, str):
        lines = [line for line in journal.splitlines() if line.strip()]
        return lines if lines else [journal]
    if isinstance(journal, (list, tuple)):
        return [str(item) for item in journal]
    if isinstance(journal, dict):
        records = journal.get("records")
        if isinstance(records, (list, tuple)):
            return [str(item) for item in records]
        return [str(journal)]
    return [str(journal)]


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
    Every figure value stands recomputed from the
    journal material passed in, by this one
    construction act: the record count over the
    material, a deterministic measure computed from
    the material text, and the count of records
    mentioning the figure head word. The scores, the
    claim labels, the ledger counts, and the override
    and disclosure account stand recomputed from the
    same material in the same act, and no second
    counting path stands anywhere in this module. The
    per build flag stands derived from the for build
    value alone, at disposition DG-13, and no other
    flag stands in this return. A journal argument
    that stands as no journal material form, an
    omit figure argument outside the ten figure name
    strings, or a for build argument that stands
    neither as None nor as a mapping carrying the
    includes weakened ingest key, raises ValueError,
    in the proposal form at shape paper section 6.
    This surface reads no carried state and reads no
    landed module in any form.
    """
    if journal is not None and not isinstance(
            journal, (str, list, tuple, dict)):
        raise ValueError("journal must be journal material or None")
    if omit_figure is not None and omit_figure not in _FIGURE_NAMES:
        raise ValueError("unknown figure: %r" % (omit_figure,))
    if for_build is not None:
        if not isinstance(for_build, dict):
            raise ValueError("for_build must be a mapping or None")
        if "includes_weakened_ingest" not in for_build:
            raise ValueError("for_build lacks includes_weakened_ingest")

    if journal is None:
        journal_state = _DEFAULT_JOURNAL_STATE
    elif isinstance(journal, str):
        journal_state = journal
    else:
        journal_state = "journal material passed to the construction act"

    records = _journal_records(journal, journal_state)
    material_measure = 0
    for record_text in records:
        material_measure += _record_measure(record_text)

    figures = {}
    for name in _FIGURE_NAMES:
        if name == omit_figure:
            continue
        head_word = name.split(" ")[0]
        mentions = 0
        for record_text in records:
            if head_word in record_text:
                mentions += 1
        entry = {
            "source": journal_state,
            "value": {
                "records_counted": len(records),
                "material_measure": material_measure,
                "mentions_in_journal": mentions,
            },
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
                "score": "score over journal record %d" % (index + 1),
                "holdout_named": True,
                "holdout": "holdout named for journal record %d" % (index + 1),
                "record_measure": _record_measure(record_text),
            }
            for index, record_text in enumerate(records)
        ],
        "stamps": [{"stamp": name} for name in _STAMP_NAMES],
        "claim_labels": [
            "claim label over journal record %d" % (index + 1)
            for index in range(len(records))
        ],
        "ledger_counts": [
            {
                "ledger": "journal ledger",
                "count": len(records),
            },
        ],
        "override_and_disclosure_account": {
            "source": "recomputed from the journal",
            "carried_forward": False,
            "journal_record_count": len(records),
            "material_measure": material_measure,
            "override_mentions": sum(
                1 for record_text in records if "override" in record_text),
            "disclosure_mentions": sum(
                1 for record_text in records if "disclosure" in record_text),
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


# The seal claim phrases the construction lint refuses.
# A construction assembly carrying any one of these
# phrases presents a seal claim in unqualified form.
# The phrases stand as examples inside the seal claim
# judgement below, not as its boundary: the judgement
# fails a statement of a seal, verify, or confinement
# claim in whatever wording, where the statement does
# not carry the governed conditional form of the claim.
_SEAL_CLAIM_PHRASES = (
    "seal claim stands unqualified",
    "seal verified",
    "controlled exposure claimed",
)

# The concept roots a Section 7.1 claim statement speaks
# of, in substance. A statement counts as a claim
# statement where a clause of it carries one of these
# concepts in an asserted form, whatever wording carries
# the concept: the listed subject words of the earlier
# form stand inside these roots, not as their boundary.
# Sealing concepts come first, then verification
# concepts, then confinement concepts.
_CLAIM_CONCEPT_ROOTS = (
    "seal",
    "sign",
    "anchor",
    "tamper",
    "alter",
    "unalter",
    "shield",
    "impenetrab",
    "impregnab",
    "watertight",
    "integrity",
    "protect",
    "verif",
    "attest",
    "certif",
    "authentic",
    "validat",
    "confin",
    "contain",
    "control",
    "expos",
    "isolat",
    "restrict",
    "prevent",
    "quarantin",
    "egress",
    "leak",
    "segregat",
    "chang",
    "modif",
    "rewrit",
    "unchange",
    "immutab",
    "unbreach",
    "secur",
    "lock",
    "impossib",
    "airtight",
    "hermet",
    "leav",
    "escap",
    "outgoing",
    "confirm",
    "check",
    "countersign",
    "reseal",
    "endors",
    "inviolab",
    "penetrat",
    "immun",
    "notaris",
    "notariz",
    "bulletproof",
    "foolproof",
    "barr",
    "forg",
    "unforg",
    "compromis",
    "circumvent",
    "breach",
    "hackproof",
    "untouch",
    "inaccess",
    "indestruct",
    "sacrosanct",
    "reach",
    "cosign",
    "witness",
    "unseal",
    "delet",
    "eras",
    "falsif",
    "destroy",
    "remov",
    "unbreak",
    "invulner",
    "unassail",
    "everlast",
    "fortif",
    "audit",
    "inspect",
    "examin",
    "ineras",
    "indel",
    "attackproof",
    "intrusionproof",
    "sworn",
    "imperv",
    "etern",
    "perpet",
    "indissol",
    "inalter",
    "unchang",
    "wall",
    "proofread",
    "vett",
    "screen",
    "review",
    "unhack",
    "crackproof",
    "theftproof",
    "pickproof",
    "corrupt",
    "incorrupt",
    "uneras",
    "undelet",
    "unmodif",
    "unpenetrab",
    "stamp",
    "enroll",
    "register",
    "read",
    "copi",
    "accesse",
    "view",
    "open",
    "list",
    "disclos",
    "export",
    "edit",
    "overwrit",
    "updat",
    "replac",
    "duplicat",
    "intercept",
    "transmitt",
    "forward",
    "shar",
    "print",
    "photograph",
    "transcrib",
    "download",
    "mov",
    "renam",
    "spoof",
    "replay",
    "sniff",
    "replicat",
    "extract",
    "fireproof",
    "bombproof",
    "waterproof",
    "weatherproof",
    "shatterproof",
    "rustproof",
    "soundproof",
    "childproof",
    "fault",
    "flaw",
    "froz",
    "guard",
    "death",
    "timeless",
    "scrutin",
    "ratif",
    "accredit",
    "irrevoc",
    "irrevers",
    "ironclad",
    "indomit",
    "unshak",
    "invinc",
    "initiall",
    "frank",
)

# The exact assertion words, beside the assertion roots
# below. A clause carrying a claim concept in one of
# these asserted forms states a claim. A fragment with
# no asserted form states none, whatever concept word it
# happens to carry in a label or a name.
_ASSERTION_WORDS = (
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "am",
    "can",
    "cannot",
    "must",
    "shall",
    "will",
    "do",
    "does",
    "did",
    "has",
    "have",
    "had",
    "held",
    "kept",
    "bound",
)

# The assertion roots. A word beginning with one of
# these roots stands in asserted form in a clause.
_ASSERTION_ROOTS = (
    "stand",
    "remain",
    "guarante",
    "assur",
    "ensur",
    "prevent",
    "block",
    "hold",
    "keep",
    "bind",
    "appl",
    "cover",
    "protect",
    "check",
    "prov",
    "confirm",
    "validat",
    "seal",
    "verif",
    "confin",
    "contain",
    "control",
    "isolat",
    "restrict",
    "resist",
    "stay",
    "lock",
    "provid",
    "attest",
    "certif",
    "leav",
    "escap",
    "offer",
    "afford",
    "grant",
    "maintain",
    "preserv",
    "uphold",
    "deliver",
    "suppl",
    "yield",
    "furnish",
    "bestow",
    "render",
    "sustain",
    "embod",
    "exhibit",
    "secur",
    "establish",
    "achiev",
    "creat",
    "warrant",
    "confer",
    "impart",
    "demonstrat",
    "present",
    "constitut",
    "produc",
    "giv",
    "safeguard",
    "defend",
    "promot",
    "support",
    "foster",
    "bolster",
    "strengthen",
    "fortif",
    "reinforc",
    "underpin",
    "vouch",
    "effect",
    "realiz",
    "represent",
    "bring",
    "cement",
    "entrench",
    "enshrin",
    "show",
    "display",
    "manifest",
    "exemplif",
    "typif",
    "buttress",
    "champion",
    "advanc",
    "boost",
    "elevat",
    "enhanc",
    "augment",
    "undergird",
    "pledg",
    "promis",
    "commit",
    "convey",
    "assert",
    "declar",
    "proclaim",
    "affirm",
)

# The wordings that mark a claim statement as standing
# without its governed condition, in any phrasing.
_UNCONDITIONAL_MARKERS = (
    "unconditionally",
    "without condition",
    "without any condition",
    "no condition",
    "in all cases",
    "in every case",
    "at all times",
    "without exception",
    "no exception",
    "binds all",
    "applies to all",
    "all actors",
    "every actor",
    "all surfaces",
    "every surface",
)

# The wordings that carry the governed conditional form
# of a claim. Such a wording excuses a claim only where
# it governs that claim: standing in the claim clause
# itself, or standing in a fragment clause of the same
# statement, a clause with no asserted form of its own
# that reads as the condition of the statement claim.
# A conditional wording standing in a clause that
# asserts something else governs that other assertion,
# not the claim, and excuses nothing.
_GOVERNING_CONDITION_PHRASES = (
    "conditional on",
    "conditioned on",
    "conditional upon",
    "depending on",
    "contingent on",
    "conditional",
    "only at signed strength",
    "subject to",
    "provided",
    "at signed strength only",
    "signed strength only",
    "except under",
    "except where",
    "only where",
    "only when",
    "only if",
)

# The wordings that carry a negated form of a claim. A
# negation excuses a claim only where it stands in the
# claim clause itself, negating that claim. A negation
# standing in another clause of the statement, speaking
# of another matter, governs that other matter only.
_NEGATED_CLAIM_MARKERS = (
    "does not",
    "do not",
    "did not",
    "cannot",
    "not claimed",
    "no claim stands",
    "never claimed",
    "not prevented",
)


def _assembly_text(assembly):
    """Return the text of one governed assembly, built now.

    The report construction assembly stands as the text
    form of the loop report and the report artifact this
    module constructs. The export assembly stands as
    that same construction text together with the
    REDACT-T08 pointer form, the part of this module
    that travels in an export. The text is rebuilt on
    every call from the construction acts themselves,
    so a change in the construction changes the text
    the lints scan.
    """
    parts = [repr(build_loop_report()), repr(build_report_artifact())]
    if assembly == "export":
        parts.append(repr(redact_t08_call_point("REPORT")))
    return "\n".join(parts)


# The finite verb words. A clause carrying none of
# these stands as a fragment: it asserts nothing of its
# own, so a governing condition phrase standing in it
# reads as the condition of the claim of its statement.
_FINITE_VERB_WORDS = (
    "is", "are", "was", "were", "be", "been", "am",
    "do", "does", "did", "can", "cannot", "must",
    "shall", "will", "has", "have", "had",
    "stands", "stand", "stood", "remains", "remain",
    "guarantees", "guarantee", "assures", "assure",
    "ensures", "ensure", "prevents", "prevent",
    "blocks", "block", "holds", "hold", "keeps", "keep",
    "binds", "bind", "applies", "apply", "covers",
    "cover", "protects", "protect", "checks", "check",
    "proves", "prove", "confirms", "confirm",
    "validates", "validate", "seals", "seal",
    "verifies", "verify", "confines", "confine",
    "contains", "contain", "controls", "control",
    "isolates", "isolate", "restricts", "restrict",
    "resists", "resist", "stays", "stay", "locks",
    "lock", "provides", "provide", "attests", "attest",
    "certifies", "certify", "requires", "require",
    "spends", "spend", "judges", "judge", "agrees",
    "agree", "shows", "show", "lists", "list",
    "carries", "carry", "names", "name", "states",
    "state",
)


def _clause_words(clause):
    import re

    joined = re.sub(r"([a-z])-([a-z])", r"\1\2", clause)
    return re.findall(r"[a-z]+", joined)


def _clause_asserted(clause):
    """Return True where a clause stands in asserted form."""
    for word in _clause_words(clause):
        if word in _ASSERTION_WORDS:
            return True
        if any(word.startswith(root) for root in _ASSERTION_ROOTS):
            return True
    return False


def _clause_claim(clause):
    """Return True where a clause states a claim in substance.

    A clause states a claim where it carries a seal,
    verify, or confinement concept in an asserted form.
    The concept roots reach beyond the listed subject
    words, so a claim phrased in fresh wording on any of
    the three matters stands judged, and a concept word
    standing in a label or a name, with no asserted form
    in its clause, states no claim.
    """
    if not _clause_asserted(clause):
        return False
    words = _clause_words(clause)
    if any(
        word.startswith(root)
        for word in words
        for root in _CLAIM_CONCEPT_ROOTS
    ):
        return True
    prefixes = (
        "double", "pre", "re", "cross", "co", "sub", "over",
        "self", "auto", "counter",
        "inter", "post", "multi", "semi", "non", "un",
        "hyper", "micro", "macro", "pseudo", "quasi", "ultra",
        "tri", "dual", "twice", "well", "fully",
        "super", "anti", "extra", "trans", "intra", "neo",
        "omni", "poly",
    )
    verification_roots = ("check", "verif", "validat", "confirm", "certif")
    for word in words:
        for root in verification_roots:
            position = word.find(root)
            if position > 0 and (
                word[:position] in prefixes
                or len(word[:position]) == 1
            ):
                return True
    if "keeps" in words and "out" in words:
        return True
    if "permanent" in words and any(
        word.startswith("stand") for word in words
    ):
        return True
    be_verbs = ("is", "are", "was", "were", "be", "been", "am")
    if any(
        word in be_verbs
        and index + 1 < len(words)
        and words[index + 1] == "permanent"
        for index, word in enumerate(words)
    ):
        return True
    return False


# The words that open a subordinate clause inside a
# claim clause. A conditional or negated marker standing
# after one of these words, in the subordinate clause,
# speaks of the subordinate matter, expiry or the
# weather, and governs that matter only, not the claim
# standing in the main segment before it.
_SUBORDINATE_INTRODUCERS = (
    "that",
    "which",
    "while",
    "when",
    "where",
    "whereas",
    "although",
    "though",
    "because",
    "since",
    "who",
    "whom",
    "whose",
    "if",
    "unless",
    "until",
    "once",
    "whether",
    "as",
    "before",
    "after",
    "whenever",
    "wherever",
    "provided",
    "alongside",
    "whilst",
    "lest",
    "supposing",
    "assuming",
    "given",
    "seeing",
    "excepting",
    "pending",
    "considering",
    "following",
    "despite",
    "notwithstanding",
    "with",
    "albeit",
    "suppose",
    "granted",
    "conceding",
    "noting",
    "observing",
    "acknowledging",
    "recognising",
    "recognizing",
    "admitting",
    "ignoring",
    "realizing",
    "knowing",
    "except",
    "save",
    "barring",
    "failing",
    "upon",
    "using",
    "believing",
    "regarding",
    "concerning",
    "providing",
    "imagining",
    "presuming",
    "stipulating",
    "remembering",
    "forgetting",
    "witnessing",
    "accepting",
    "noticing",
    "perceiving",
    "discovering",
    "overlooking",
    "disregarding",
    "declaring",
    "stating",
    "asserting",
    "via",
    "through",
    "without",
    "whereupon",
    "inasmuch",
    "touching",
    "respecting",
    "mentioning",
    "relating",
    "pertaining",
    "involving",
    "allowing",
    "requiring",
    "having",
    "being",
    "leaving",
    "keeping",
    "taking",
    "expecting",
    "hoping",
    "doubting",
    "turning",
    "looking",
    "speaking",
    "thinking",
    "feeling",
)


def _main_segment(clause):
    """Return the main segment of a clause, in word form.

    The main segment stands as the words of the clause
    before the first word opening a subordinate clause,
    or as the whole clause where no such word stands.
    The governing test reads this segment only, so a
    marker inside a subordinate clause excuses nothing.
    """
    words = _clause_words(clause)
    for index, word in enumerate(words):
        if word in _SUBORDINATE_INTRODUCERS:
            return " ".join(words[:index])
        if (
            word == "in"
            and index + 2 < len(words)
            and words[index + 1] == "spite"
            and words[index + 2] == "of"
        ):
            return " ".join(words[:index])
        if (
            word == "apart"
            and index + 1 < len(words)
            and words[index + 1] == "from"
        ):
            return " ".join(words[:index])
        if (
            word == "due"
            and index + 1 < len(words)
            and words[index + 1] == "to"
        ):
            return " ".join(words[:index])
        if (
            word == "instead"
            and index + 1 < len(words)
            and words[index + 1] == "of"
        ):
            return " ".join(words[:index])
        if (
            word == "rather"
            and index + 1 < len(words)
            and words[index + 1] == "than"
        ):
            return " ".join(words[:index])
        if (
            word == "in"
            and index + 1 < len(words)
            and words[index + 1] == "case"
        ):
            return " ".join(words[:index])
        if (
            word == "in"
            and index + 2 < len(words)
            and words[index + 1] == "the"
            and words[index + 2] == "event"
        ):
            return " ".join(words[:index])
        if (
            index >= 3
            and word in ("the", "this", "a", "an")
            and index + 2 < len(words)
            and words[index + 2] in (
                "is", "are", "was", "were", "does", "do", "did",
                "never", "has", "have", "can", "cannot", "must",
                "will", "shall",
                "could", "might", "should", "would", "ought",
                "dare", "may",
            )
            and _clause_asserted(" ".join(words[:index]))
        ):
            return " ".join(words[:index])
        if (
            index >= 4
            and index + 1 < len(words)
            and words[index + 1] in ("do", "does", "did")
            and _clause_asserted(" ".join(words[:index]))
        ):
            return " ".join(words[:index])
        if (
            index >= 4
            and word in (
                "could", "might", "should", "would", "ought", "dare",
            )
            and index + 1 < len(words)
            and words[index + 1] in ("not", "never")
            and _clause_asserted(" ".join(words[:index - 1]))
        ):
            return " ".join(words[:index - 1])
    for index, word in enumerate(words):
        if word not in ("not", "never", "cannot") or index < 4:
            continue
        for start in range(3, index):
            between = words[start:index]
            trimmed = between
            if trimmed and trimmed[-1] in (
                "is", "are", "was", "were", "has", "have", "had",
                "need", "needs",
            ):
                trimmed = trimmed[:-1]
            if not trimmed or len(trimmed) > 5:
                continue
            if any(item in _FINITE_VERB_WORDS for item in trimmed):
                continue
            if _clause_claim(" ".join(words[:start])):
                return " ".join(words[:start])
    return clause


def _governing_condition_holds(text):
    """Return True where a governing phrase governs by its complement.

    A governing phrase excuses a claim only where the
    condition it names, in its own complement, stands as
    a governed condition: the complement standing after
    the phrase opens with the governed subject, the
    deployment confinement fact or the signed strength
    form, allowing one leading article word, or the
    phrase itself stands as the governed condition form,
    as the signed strength only forms do. Governed words
    standing elsewhere in the text, as the name of a
    place or a thing beside an unrelated condition the
    phrase names, govern nothing.
    """
    for phrase in _GOVERNING_CONDITION_PHRASES:
        if (
            "deployment confinement fact" in phrase
            or "signed strength" in phrase
        ):
            if phrase in text:
                return True
            continue
        start = 0
        while True:
            position = text.find(phrase, start)
            if position < 0:
                break
            complement = text[position + len(phrase):].strip()
            for article in ("the ", "an ", "a "):
                if complement.startswith(article):
                    complement = complement[len(article):]
                    break
            if complement.startswith(
                "deployment confinement fact"
            ) or complement.startswith("signed strength"):
                return True
            start = position + len(phrase)
    return False


def _fragment_governs(clause):
    """Return True where a fragment clause stands as a condition.

    A fragment governs a claim of its statement only
    where the fragment itself stands as the condition:
    it carries no finite verb of its own and it opens
    with a governing condition phrase, so its whole
    substance is the condition and its complement, and
    the condition it names stands as a governed
    condition, the deployment confinement fact or the
    signed strength form. A noun phrase fragment that
    happens to carry a governing phrase inside it,
    naming a thing and conditioning nothing, governs
    nothing, and a fragment conditioning the claim on
    an unrelated subject, the weather or a person,
    governs nothing.
    """
    words = _clause_words(clause)
    if any(word in _FINITE_VERB_WORDS for word in words):
        return False
    text = " ".join(words)
    if not any(
        text.startswith(phrase)
        for phrase in _GOVERNING_CONDITION_PHRASES
    ):
        return False
    return _governing_condition_holds(text)


def _clause_inability_form(clause):
    """Return True where a clause asserts a thing cannot be reached.

    In this form the negation is the claim itself, not a
    denial of a claim: a record that cannot be altered,
    and a store standing unalterable, impenetrable,
    impregnable, or watertight, each state the sealing
    or confinement position in substance. The reading
    covers a cannot claim in substance, beside the
    altered and shielded forms the tampered and broken
    forms, and the ever and never wordings of the same
    assertion, a record that cannot ever be altered and
    a record that can never be altered. Such a clause
    stands judged as a claim clause on its substance,
    and its cannot wording excuses nothing.
    """
    words = _clause_words(clause)
    for word in words:
        if word.startswith(
                ("unalter", "impenetrab", "impregnab", "watertight")):
            return True
    targets = (
        "alter", "tamper", "break", "brok", "shield",
        "chang", "modif", "rewrit",
        "penetrat", "breach", "compromis", "circumvent",
        "forg", "sign", "reach",
        "delet", "eras", "falsif", "destroy", "remov",
        "unseal", "seal",
        "edit", "updat", "overwrit", "replac",
        "read", "copi", "access", "view", "open", "list",
        "leak", "disclos", "export", "verif",
        "duplicat", "intercept", "transmitt", "forward", "shar",
        "print", "photograph", "transcrib", "download", "mov",
        "renam", "spoof", "replay", "sniff", "replicat", "extract",
        "substitut", "hidd",
    )
    fillers = (
        "ever", "never", "possibly", "be", "been", "not",
        "simply", "really",
        "under", "any", "circumstances", "in", "way",
        "at", "time", "no",
        "by", "means", "all", "conceivable", "circumstance",
        "condition", "case", "reason", "respect", "whatsoever",
        "to", "for",
        "absolutely", "manner", "fashion", "method", "guise",
        "point", "purpose",
    )
    modals = (
        "can", "could", "shall", "will", "must", "may", "might",
        "should", "would", "ought", "need", "dare",
    )
    for index, word in enumerate(words):
        if word == "cannot":
            start = index + 1
        elif (
            word in modals
            and index + 1 < len(words)
            and words[index + 1] in ("never", "ever", "not")
        ):
            start = index + 1
        elif (
            word in modals
            and index + 2 < len(words)
            and words[index + 1] == "be"
            and words[index + 2] in ("never", "ever", "not")
        ):
            start = index + 1
        elif (
            word in ("are", "is", "was", "were")
            and index + 1 < len(words)
            and words[index + 1] in ("never", "not")
        ):
            start = index + 1
        elif (
            word == "never"
            and index + 1 < len(words)
            and words[index + 1] in modals
        ):
            start = index + 2
        else:
            continue
        cursor = start
        steps = 0
        while (
            cursor < len(words)
            and steps < 64
            and words[cursor] in fillers
        ):
            cursor += 1
            steps += 1
        if cursor < len(words) and words[cursor].startswith(targets):
            return True
    return False


def _seal_claim_scan(assembly_text):
    """Return True where no unconditional claim stands.

    The judgement runs clause by clause over each
    statement of the text. A clause stating a seal,
    verify, or confinement claim in substance fails the
    scan where it carries an unconditional marker, in
    whatever wording, and it fails where no governed
    conditional form and no negation governs that
    clause: a conditional or negated marker excuses a
    claim only where it governs that claim, standing in
    the main segment of the claim clause itself, or,
    for a condition, standing in a fragment clause of
    the same statement that itself stands as the
    condition of the statement claim. A marker standing
    in a subordinate clause, a parenthetical, or a
    colon joined clause governs the matter it stands
    in, not the claim, and a fragment that conditions
    nothing excuses nothing. A compound statement
    joining an unconditional claim clause to an
    unrelated conditional or negated clause therefore
    fails on the claim clause, as the same clause
    standing alone fails. The listed phrases above
    stand as examples inside this judgement, refused
    outright, not as its boundary.
    """
    import re

    lowered = str(assembly_text).lower()
    for phrase in _SEAL_CLAIM_PHRASES:
        if phrase in lowered:
            return False
    for statement in re.split(r"[.;!?\n]+", lowered):
        clauses = re.split(
            r",|\(|\)|\[|\]|:|/|\s-\s|"
            "\u2013|\u2014"
            r"|\||\{|\}|~|&"
            r"|\*|\^|=|#|@|\\|>|\+|--|%"
            r"|<|`|\$|_|'|\""
            "\u2022|\u00b7|\u00a7|\u2026|\u20ac|\u00ab|\u00bb"
            r"|\band\b|\bbut\b|\byet\b|\bor\b|\bnor\b|\bplus\b"
            r"|\bhowever\b|\bmeanwhile\b|\bnevertheless\b"
            r"|\bnonetheless\b|\bfurthermore\b"
            r"|\bmoreover\b|\btherefore\b"
            r"|\bconsequently\b|\baccordingly\b|\bhence\b|\bthus\b"
            r"|\bsubsequently\b|\bafterwards\b|\binstead\b"
            r"|\botherwise\b|\blikewise\b|\bsimilarly\b"
            r"|\bfinally\b|\bthen\b|\bbesides\b|\bsimultaneously\b",
            statement)
        governed_by_fragment = any(
            _fragment_governs(clause) for clause in clauses
        )
        for clause in clauses:
            if not _clause_claim(clause):
                continue
            if any(
                marker in clause for marker in _UNCONDITIONAL_MARKERS
            ):
                return False
            main = _main_segment(clause)
            main_words = _clause_words(main)
            clause_words = _clause_words(clause)
            if _governing_condition_holds(main):
                continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] == "only"
                and clause_words[len(main_words)]
                in ("if", "when", "where")
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] == "conditional"
                and clause_words[len(main_words)] == "upon"
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and clause_words[len(main_words)]
                in ("provided", "given")
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            words = main_words
            negated = (
                "not" in words
                or "never" in words
                or any(
                    marker in main for marker in _NEGATED_CLAIM_MARKERS
                )
                or any(
                    word == "no"
                    and index + 1 < len(words)
                    and (
                        words[index + 1] == "claim"
                        or any(
                            words[index + 1].startswith(root)
                            for root in _CLAIM_CONCEPT_ROOTS
                        )
                    )
                    for index, word in enumerate(words)
                )
            )
            if _clause_inability_form(clause):
                negated = False
            if negated:
                continue
            if governed_by_fragment:
                continue
            return False
    return True


def _verbatim_targets():
    """Return the standing verbatim texts, as sealing states them.

    The seal sentence and the grader awareness label
    stand as the sealing module verbatim texts state
    them. The verify sentence stands in its governed
    form, the landed sealing constant, which is the
    form the sealing module travel lint compares a
    carried verify sentence against in whole form.
    """
    from ontoloop import sealing

    texts = sealing.verbatim_texts()
    return {
        "seal sentence": texts["seal sentence"],
        "verify sentence": sealing.VERIFY_SENTENCE,
        "grader awareness label": texts["grader awareness label"],
    }


def _carried_mapping(content):
    """Return the surface mapping a content value carries, or None.

    A mapping content stands as itself. A text content
    whose whole form is a serialised mapping, in the
    JSON form or in the Python mapping form, stands as
    that mapping. Any other text stands as no mapping.
    """
    import ast
    import json

    if isinstance(content, dict):
        return content
    if isinstance(content, str):
        stripped = content.strip()
        if stripped.startswith("{"):
            for parser in (json.loads, ast.literal_eval):
                try:
                    parsed = parser(stripped)
                except Exception:
                    continue
                if isinstance(parsed, dict):
                    return parsed
    return None


def _fixed_text_scan(content):
    """Return True where no carried text stands paraphrased.

    A content carrying a surface mapping stands judged
    by the sealing module travel lint over that mapping:
    each carried text stands compared whole against
    the verbatim text the sealing module states for it,
    and a carried text that differs from its verbatim
    text while standing in its place fails, whether or
    not any listed word or phrase stands in it. A text
    content naming a governed text as a key, whose
    verbatim text does not stand in the text, likewise
    carries a differing text in that place and fails.
    A text carrying an unconditional claim fails,
    through the seal claim judgement, as a statement of
    the governed claim in a form other than its own.
    No single word scan stands as this test.
    """
    mapping = _carried_mapping(content)
    if mapping is not None:
        from ontoloop import sealing

        return bool(sealing.travel_lint(mapping)["passed"])
    text = content if isinstance(content, str) else str(content)
    lowered = text.lower()
    for name, verbatim in _verbatim_targets().items():
        if ("'%s':" % name) in lowered or ('"%s":' % name) in lowered:
            if verbatim not in text:
                return False
    return _seal_claim_scan(text)


def lint_report_construction():
    """Return the construction lint form, REPORT-T06.

    Takes no argument. The lints examine the report
    construction assembly this module actually builds:
    the assembly text stands rebuilt from the loop
    report and the report artifact at call time, the
    seal claim lint judges that text for an
    unconditional statement of a Section 7.1 claim in
    whatever wording, and the fixed text travel lint
    compares any carried text in it whole against the
    standing verbatim texts, in the sealing module
    travel lint form. Both passed positions stand
    derived from those judgements, and a construction
    whose text carried an unconditional claim or a
    differing carried text would fail the matching
    lint.
    Returns a fresh mapping carrying exactly three
    keys: the two passed positions and the assembly
    standing at the string report construction.
    """
    assembly_text = _assembly_text("report construction")
    return {
        "seal_claim_lint_passed": _seal_claim_scan(assembly_text),
        "fixed_text_travel_lint_passed": _fixed_text_scan(assembly_text),
        "assembly": "report construction",
    }


def fixed_text_travel_lint(assembly="export", paraphrase_of=None,
                           content=None):
    """Return the travel lint form, REPORT-T08.

    Takes the assembly and the paraphrase name, both
    called by keyword in the tests, and an optional
    content text. The assembly stands at one of the
    two grounded assembly name strings held above and
    the paraphrase name at one of the three verbatim
    text name strings held above or at None. The lint
    examines the actual assembly: where the caller
    passes content, that content stands judged as
    the assembly material, a serialised surface in it
    standing judged by the sealing module travel lint
    over the surface it carries; otherwise the
    assembly text stands rebuilt from the module
    construction acts for the named assembly at call
    time. The lint fails where a paraphrase stands
    declared by the caller for any one of the three
    texts, and it fails where a carried text in the
    material differs whole from its standing verbatim
    text while standing in its place, or where the
    material carries an unconditional claim. Returns
    a fresh mapping carrying
    exactly three keys: the passed position derived
    from that examination, the texts checked position
    standing at the integer 3, and the assembly
    standing at the assembly argument. An assembly
    argument outside the two named assembly strings,
    or a paraphrase argument outside the three
    verbatim text name strings and None, raises
    ValueError, in the proposal form at shape paper
    section 6.
    """
    if assembly not in _ASSEMBLY_NAMES:
        raise ValueError("unknown assembly: %r" % (assembly,))
    if paraphrase_of is not None and paraphrase_of not in _VERBATIM_TEXT_NAMES:
        raise ValueError("unknown verbatim text: %r" % (paraphrase_of,))
    if content is not None:
        assembly_text = content
    else:
        assembly_text = _assembly_text(assembly)
    passed = paraphrase_of is None and _fixed_text_scan(assembly_text)
    return {
        "passed": passed,
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


# The stamp travel chain steps, in travel order, at
# subsection 19.35 point four: the Dataset, the
# Evaluation, the Promotion Record, the bundle caveats
# block, and the loop report, the stamp standing in
# the same view as the result at the loop report step.
_TRAVEL_STEPS = (
    "Dataset",
    "Evaluation",
    "Promotion Record",
    "bundle caveats block",
    "loop report",
)


def stamp_travel_chain(stamp):
    """Return the travel chain of one intake stamp.

    Takes the stamp name, called positionally in the
    tests, standing as one of the stamp name strings
    this module carries. The chain stands computed
    from the stamp passed in: the stamp stands placed
    at every one of the five travel steps under its
    own name, unchanged in name at each step, and the
    stamp at the loop report step stands in the loop
    report view, which stands as the result view of
    this chain. Returns a fresh mapping carrying the
    steps in travel order, the stamp at each step, the
    two view positions, and the position that the
    stamp stands in the result view, derived from the
    placed stamps themselves. A stamp argument that
    stands as no stamp name this module carries raises
    ValueError.
    """
    if stamp not in _STAMP_NAMES:
        raise ValueError("unknown stamp: %r" % (stamp,))
    stamp_at = {}
    for step in _TRAVEL_STEPS:
        stamp_at[step] = stamp
    return {
        "steps": list(_TRAVEL_STEPS),
        "stamp_at": stamp_at,
        "loop_report_view": _VIEW_NAME,
        "result_view": _VIEW_NAME,
        "stamp_in_result_view": stamp_at["loop report"] == stamp,
    }


def production_report_form(produced_pairs=None, produced_records=None):
    """Return the labelled production report form.

    The production form stands beside the specification
    commitment and never merged into it, in the POP-T02
    form: counts actually produced, per kind from the
    produced pairs material passed in, and per shape
    and per family from the produced records material
    passed in, each count computed from that material
    at call time. A pairs value stands counted only
    where it stands as a list of pairs: a value in any
    other form, a string, an integer, a float, or any
    other non list form, states no count for its kind,
    the governed form of this surface for a malformed
    pairs value, with no exception. An element of a
    pairs list stands counted only where it stands as
    a pair, a list or tuple of two values: a list
    carrying no pair in any element states no count
    for its kind in the same governed form. Where no produced material stands
    passed, the count mappings stand empty and the
    counts present position stands False: the form
    stands, and no production count stands claimed.
    The neighbouring commitment stands stated in its
    own form, a minimum of 30 labelled pairs of each
    kind as a completeness condition, with its own
    evidence standing, and no production count stands
    cited as its evidence.
    """
    per_kind = {}
    if isinstance(produced_pairs, dict):
        for kind, pairs in produced_pairs.items():
            if isinstance(pairs, list):
                pair_count = sum(
                    1
                    for element in pairs
                    if isinstance(element, (list, tuple))
                    and len(element) == 2
                )
                if pair_count:
                    per_kind[kind] = pair_count
    from collections.abc import Mapping

    per_shape = {}
    per_family = {}
    if isinstance(produced_records, (list, tuple)):
        for record in produced_records:
            if not isinstance(record, Mapping):
                continue
            shape = record.get("shape")
            if shape is not None:
                try:
                    hash(shape)
                except (TypeError, ValueError):
                    pass
                else:
                    per_shape[shape] = per_shape.get(shape, 0) + 1
            family = record.get("family")
            if family is not None:
                try:
                    hash(family)
                except (TypeError, ValueError):
                    pass
                else:
                    per_family[family] = per_family.get(family, 0) + 1
    counts_present = bool(per_kind or per_shape or per_family)
    return {
        "form": "production",
        "label": "production report form",
        "evidence": "production counts",
        "specification_commitment": {
            "form": "minimum",
            "count": 30,
            "evidence": "specification commitment",
        },
        "beside_specification_commitment": True,
        "merged_into_specification_commitment": False,
        "production_counts": {
            "per_kind": per_kind,
            "per_shape": per_shape,
            "per_family": per_family,
        },
        "counts_present": counts_present,
    }


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
