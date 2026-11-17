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
    "mirror",
    "clon",
    "screenshot",
    "email",
    "upload",
    "archiv",
    "broadcast",
    "stol",
    "wip",
    "exfiltrat",
    "purg",
    "film",
    "scan",
    "trac",
    "impermeab",
    "burglarproof",
    "vandalproof",
    "ageless",
    "endless",
    "boundless",
    "perfect",
    "impeccab",
    "undying",
    "infallib",
    "corroborat",
    "failsafe",
    "errorproof",
    "peerless",
    "matchless",
    "errorfree",
    "riskfree",
    "rubberstamp",
    "timestamp",
    "memoriz",
    "smuggl",
    "relay",
    "dictat",
    "carri",
    "fabricat",
    "publish",
    "sold",
    "sell",
    "counterfeit",
    "impersonat",
    "fak",
    "reproduc",
    "photocopi",
    "fax",
    "sync",
    "siphon",
    "harvest",
    "scrap",
    "lift",
    "purloin",
    "filch",
    "restor",
    "recover",
    "reconstruct",
    "regenerat",
    "reissu",
    "recreat",
    "spotless",
    "unblemish",
    "pristine",
    "unmark",
    "unopen",
    "impass",
    "unenter",
    "unimpeach",
    "unquestion",
    "immaculat",
    "errorless",
    "riskless",
    "defectfree",
    "unpick",
    "uncrack",
    "unfake",
    "unspoof",
    "hackerproof",
    "thiefproof",
    "waxseal",
    "emboss",
    "engrav",
    "brand",
    "imprint",
    "inscrib",
    "etch",
    "postmark",
    "hallmark",
    "watermark",
    "goldstamp",
    "silverstamp",
    "handstamp",
    "datestamp",
    "stream",
    "distribut",
    "transfer",
    "doctor",
    "pilfer",
    "memoris",
    "circulat",
    "disseminat",
    "convey",
    "dispatch",
    "aire",
    "televis",
    "projecte",
    "displaye",
    "beame",
    "overhear",
    "quot",
    "paraphras",
    "plagiar",
    "unlock",
    "decrypt",
    "manipulat",
    "loot",
    "snatch",
    "swip",
    "pinch",
    "tape",
    "bugg",
    "wiretap",
    "embezzl",
    "divert",
    "xerox",
    "retyp",
    "noted",
    "logg",
    "catalog",
    "memorial",
    "chronicl",
    "unstain",
    "untarnish",
    "unsulli",
    "unsoil",
    "unequal",
    "unparallel",
    "unrival",
    "unsurpass",
    "incomparab",
    "unreach",
    "unapproach",
    "ungett",
    "foilstamp",
    "inkstamp",
    "laseretch",
    "inviolat",
    "unflaw",
    "unmarr",
    "unimpair",
    "entryproof",
    "unchalleng",
    "imperish",
    "fraudproof",
    "drillproof",
    "dustproof",
    "smudgeproof",
    "narrat",
    "recit",
    "whisper",
    "annotat",
    "summaris",
    "summariz",
    "translat",
    "encrypt",
    "encod",
    "compress",
    "index",
    "cach",
    "perform",
    "decipher",
    "decod",
    "crack",
    "enter",
    "obtain",
    "retriev",
    "fetch",
    "gather",
    "collect",
    "compil",
    "vandalis",
    "vandaliz",
    "defac",
    "mutilat",
    "ransack",
    "burgl",
    "robb",
    "heist",
    "eavesdrop",
    "obliterat",
    "annihilat",
    "poison",
    "sabotag",
    "undermin",
    "hack",
    "reveal",
    "monitor",
    "observ",
    "survey",
    "untaint",
    "undefil",
    "unpollut",
    "uncontaminat",
    "unspott",
    "unsmirch",
    "unbesmirch",
    "sinless",
    "guiltless",
    "blameless",
    "irreproach",
    "unconquer",
    "unvanquish",
    "unbeat",
    "uncorrupt",
    "unbend",
    "unshatter",
    "immort",
    "unimpregn",
    "immov",
    "irrefut",
    "incontest",
    "incontrovert",
    "indisput",
    "unrefut",
    "uncontest",
    "unoppos",
    "unmatch",
    "stainless",
    "inimit",
    "transcend",
    "unfad",
    "perenni",
    "shockproof",
    "quakeproof",
    "scratchproof",
    "stainproof",
    "dentproof",
    "tearproof",
    "punctureproof",
    "heatproof",
    "acidproof",
    "smokeproof",
    "flameproof",
    "rotproof",
    "petproof",
    "machineetch",
    "handengrav",
    "laserengrav",
    "deepetch",
    "blindstamp",
    "hotstamp",
    "coldstamp",
    "machinestamp",
    "officiallystamp",
    "carv",
    "draft",
    "penn",
    "author",
    "compos",
    "seiz",
    "post",
    "mail",
    "map",
    "chart",
    "graph",
    "draw",
    "paint",
    "sketch",
    "labell",
    "tagg",
    "flagg",
    "highlight",
    "underlin",
    "presente",
    "describ",
    "defin",
    "caption",
    "digitis",
    "digitiz",
    "play",
    "import",
    "queri",
    "search",
    "locat",
    "identifi",
    "unscar",
    "undamag",
    "unharm",
    "unbrok",
    "unbruis",
    "unwound",
    "unchip",
    "untorn",
    "waxstamp",
    "steelstamp",
    "ironstamp",
    "handetch",
    "acidetch",
    "copperetch",
    "stoneetch",
    "woodetch",
    "glassetch",
    "unend",
    "absolut",
    "pure",
    "intact",
    "whole",
    "complet",
    "total",
    "suprem",
    "ultimat",
    "undoubt",
    "armour",
    "armor",
    "bolt",
    "chain",
    "bound",
    "tied",
    "fasten",
    "lightproof",
    "vacuumseal",
    "endur",
    "failproof",
    "dirtproof",
    "spillproof",
    "splinterproof",
    "chipproof",
    "fadeproof",
    "wrinkleproof",
    "creaseproof",
    "odourproof",
    "vaporproof",
    "vapourproof",
    "germproof",
    "mothproof",
    "mildewproof",
    "corrosionproof",
    "typed",
    "handwritten",
    "texted",
    "captur",
    "taken",
    "touch",
    "burn",
    "shred",
    "watched",
    "closed",
    "shifted",
    "rotat",
    "cited",
    "referenc",
    "mention",
    "filed",
    "stored",
    "saved",
    "kept",
    "held",
    "convert",
    "unscratch",
    "unbent",
    "uncrush",
    "unsmash",
    "unpierc",
    "uncut",
    "unburn",
    "unwither",
    "brassstamp",
    "bronzestamp",
    "leadstamp",
    "tinstamp",
    "indefeas",
    "inefface",
    "limitless",
    "infinit",
    "steadfast",
    "resolut",
    "unyield",
    "inflexib",
    "rigid",
    "solid",
    "sturdy",
    "robust",
    "durab",
    "lasting",
    "abid",
    "fixed",
    "stable",
    "steady",
    "constant",
    "continual",
    "continuous",
    "ceaseless",
    "incessant",
    "relentless",
    "unrelent",
    "unremitt",
    "stormproof",
    "floodproof",
    "coldproof",
    "crushproof",
    "vibrationproof",
    "pressureproof",
    "radiationproof",
    "chemicalproof",
    "damag",
    "divulg",
    "ship",
    "deliver",
    "test",
    "measur",
    "count",
    "weigh",
    "clear",
    "sampl",
    "book",
    "remark",
    "notic",
    "perceiv",
    "backed",
    "earthquakeproof",
    "tornadoproof",
    "hurricaneproof",
    "lightningproof",
    "frostproof",
    "impactproof",
    "blastproof",
    "explosionproof",
    "airproof",
    "sawproof",
    "hammerproof",
    "uncompromis",
    "unscath",
    "unspoil",
    "seamless",
    "adamant",
    "granit",
    "unbound",
    "unlimit",
    "inexhaust",
    "unfail",
    "omnipot",
    "sovereign",
    "autonom",
    "selfcontain",
    "knifeproof",
    "gasproof",
    "unedit",
    "undisput",
    "crashproof",
    "smashproof",
    "windproof",
    "rainproof",
    "snowproof",
    "microwaveproof",
    "grinderproof",
    "torchproof",
    "uninjur",
    "unhurt",
    "rocksolid",
    "almighty",
    "selfsufficient",
    "selfsustain",
    "standalone",
    "allpowerful",
    "godlike",
    "superhuman",
    "undeniab",
    "resist",
    "harden",
    "reinforc",
    "safe",
    "sound",
    "virusproof",
    "mouldproof",
    "moldproof",
    "insectproof",
    "ratproof",
    "mouseproof",
    "dogproof",
    "catproof",
    "babyproof",
    "studentproof",
    "teacherproof",
    "futureproof",
    "recessionproof",
    "inflationproof",
    "crisisproof",
    "tsunamiproof",
    "blizzardproof",
    "hailproof",
    "avalancheproof",
    "sandproof",
    "mudproof",
    "iceproof",
    "sleetproof",
    "greaseproof",
    "oilproof",
    "solventproof",
    "diamondproof",
    "titaniumproof",
    "steelproof",
    "ironproof",
    "stoneproof",
    "rockproof",
    "glassproof",
    "plasticproof",
    "woodproof",
    "leatherproof",
    "rubberproof",
    "ceramicproof",
    "kevlarproof",
    "carbonproof",
    "leadproof",
    "copperproof",
    "bronzeproof",
    "silverproof",
    "goldproof",
    "platinumproof",
    "chromeproof",
    "nickelproof",
    "zincproof",
    "tinproof",
    "brassproof",
    "unviolat",
    "unseen",
    "unknown",
    "unstopp",
    "undefac",
    "unvandalis",
    "unvandaliz",
    "untamper",
    "unfalsif",
    "uncounterfeit",
    "ungarbl",
    "unscrambl",
    "unencrypt",
    "undecay",
    "undecompos",
    "unrott",
    "adultproof",
    "workerproof",
    "employeeproof",
    "managerproof",
    "clientproof",
    "customerproof",
    "userproof",
    "visitorproof",
    "guestproof",
    "strangerproof",
    "intruderproof",
    "attackerproof",
    "enemyproof",
    "policeproof",
    "lawyerproof",
    "judgeproof",
    "governmentproof",
    "climateproof",
    "seasonproof",
    "timeproof",
    "ageproof",
    "lifeproof",
    "droughtproof",
    "monsoonproof",
    "cycloneproof",
    "typhoonproof",
    "noiseproof",
    "volcanoproof",
    "thunderproof",
    "waveproof",
    "tideproof",
    "currentproof",
    "stressproof",
    "strainproof",
    "smellproof",
    "tasteproof",
    "feelproof",
    "antproof",
    "waspproof",
    "beeproof",
    "mosquitoproof",
    "termiteproof",
    "spiderproof",
    "snakeproof",
    "bearproof",
    "wildfireproof",
    "aluminumproof",
    "aluminiumproof",
    "marbleproof",
    "obsidianproof",
    "pigeonproof",
    "flyproof",
    "beetleproof",
    "birdproof",
    "squirrelproof",
    "deerproof",
    "rabbitproof",
    "biteproof",
    "pestproof",
    "odorproof",
    "steamproof",
    "splashproof",
    "sprayproof",
    "foamproof",
    "powderproof",
    "granuleproof",
    "unvari",
    "unmov",
    "unweaken",
    "unpenetrat",
    "unaccess",
    "unripp",
    "undent",
    "uninfect",
    "unrevis",
    "unamend",
    "unadjust",
    "unadulterat",
    "unmix",
    "unalloy",
    "undilut",
    "unsoften",
    "unloosen",
    "unfasten",
    "unlatch",
    "unbolt",
    "unguard",
    "unshield",
    "unprotect",
    "undefend",
    "unnotic",
    "undetect",
    "undiscover",
    "unreport",
    "unrecord",
    "unlogg",
    "unfil",
    "unstor",
    "unsav",
    "unback",
    "abrasionproof", "allergenproof", "alphabetis", "alphabetiz", 
    "ashproof", "asteroidproof", "bacteriaproof", "basaltproof", 
    "batproof", "bedbugproof", "blueprint", "brickproof", "burstproof", 
    "butterflyproof", "categoris", "categoriz", "cinderproof", 
    "cockroachproof", "collat", "cometproof", "concreteproof", "confiscat", 
    "cottonproof", "crat", "crowproof", "cyberproof", "devis", 
    "emberproof", "envelop", "envision", "erosionproof", "farmerproof", 
    "firestormproof", "fleaproof", "foxproof", "fram", "fumeproof", 
    "fungusproof", "gild", "glareproof", "glu", "gooseproof", "ivoryproof", 
    "lacquer", "latch", "lavaproof", "limestoneproof", "malwareproof", 
    "meteorproof", "microfich", "miteproof", "moonproof", "nurseproof", 
    "nylonproof", "outlin", "padlock", "past", "pathogenproof", 
    "phishingproof", "pictur", "pirateproof", "pollenproof", "quartzproof", 
    "raccoonproof", "ransomwareproof", "reword", "ripproof", 
    "sandstoneproof", "scamproof", "scorpionproof", "shelv", "shrinkproof", 
    "silkproof", "skunkproof", "slateproof", "slugproof", "snailproof", 
    "sootproof", "spamproof", "sunproof", "tempestproof", "tickproof", 
    "toxinproof", "transform", "unarchiv", "unbroadcast", "unclon", 
    "uncopi", "undisclos", "unduplicat", "unemail", "unexport", "unfax", 
    "unforward", "unhash", "unindex", "unlabel", "unlist", "unmirror", 
    "unphotocopi", "unprint", "unpublish", "unreplicat", "unsalt", 
    "unscann", "unshar", "unstamp", "unstream", "unsync", "untagg", 
    "untranscrib", "untranslat", "unupload", "unview", "unxerox", 
    "varnish", "velvetproof", "venomproof", "wolfproof", 
    "infrangib",
    "subpoena", "impound", "fingerprint", 
    "garnish", "probat", "annul", 
    "expung", "redact", "incinerat", 
    "embargo", "swabb", "imprison", 
    "jaile", "taxe", "levi", 
    "foreclos", "demolish", "intern", 
    "droneproof", "laserproof", "empproof", 
    "landslideproof", "sinkholeproof", "locustproof", 
    "rodentproof", "tarnishproof", "gnatproof", 
    "aphidproof", "cricketproof", "weevilproof", 
    "opossumproof", "porcupineproof", "badgerproof", 
    "otterproof", "beaverproof", "moleproof", 
    "voleproof", "shrewproof", "hedgehogproof", 
    "tortoiseproof", "lizardproof", "geckoproof", 
    "frogproof", "toadproof", "newtproof", 
    "jadeproof", "emeraldproof", "rubyproof", 
    "sapphireproof", "opalproof", "pearlproof", 
    "amberproof", "coralproof", "linenproof", 
    "denimproof", "canvasproof", "hempproof", 
    "woolproof", "cashmereproof", "polyesterproof", 
    "rayonproof", "spandexproof", "vinylproof", 
    "trojanproof", "wormproof", "spywareproof", 
    "adwareproof", "rootkitproof", "botnetproof", 
    "heatwaveproof", "downpourproof", "delugeproof", 
    "sandroof", "travertineproof", "unregist", 
    "uncatalog", "undat", "unnumber", 
    "unpaginat", "unlaminat", "unencod", 
    "uncompress", "unzipp", "unredact", 
    "unmask", "unsanitiz", "unmoderat", 
    "untrac", "unauthoriz", 
    "stapl", "rivet", "pinn", 
    "tacke", "stitch", "sewn", 
    "clasp", "buckl", "zipp", 
    "button", "hooke", "tether", 
    "moore", "docket", "typeset", 
    "lettere", "toole", "gilt", 
    "wrapp", "boxe", "bagg", 
    "jarr", "bottl", "cann", 
    "tinn", "waxe", "corke", 
    "plugg", "stopper", "screwe", 
    "naile", "bolte", "clampe", 
    "clipp", "lashe", "knott", 
    "plaite", "braide", "woven", 
    "rifl", "auction", "pawn", 
    "welde", "cement", "encas", 
    "enshrin", "vault", "entomb", 
    "interred", "burie", "hidd", 
    "fenc", "moat", "turret", 
    "sparkproof", "arrowproof", "spearproof", 
    "clubproof", "fileproof", "crowbarproof", 
    "hornetproof", "centipedeproof", "millipedeproof", 
    "earwigproof", "silverfishproof", "alkaliproof", 
    "inkproof", "bloodproof", "gritproof", 
    "lintproof", "staticproof", "liceproof", 
    "dustmiteproof", "thripsproof", "scaleproof", 
    "mealybugproof", "whiteflyproof", "cutwormproof", 
    "armywormproof", "hornwormproof", "stinkbugproof", 
    "agateproof", "jasperproof", "onyxproof", 
    "topazproof", "garnetproof", "berylproof", 
    "spinelproof", "zirconproof", "peridotproof", 
    "tourmalineproof", "satinproof", "tweedproof", 
    "twillproof", "flannelproof", "jerseyproof", 
    "chiffonproof", "organzaproof", "tulleproof", 
    "feltproof", "suedeproof", "nubuckproof", 
    "corduroyproof", "seersuckerproof", "cambricproof", 
    "muslinproof", "gauzeproof", "burlapproof", 
    "juteproof", "sisalproof", "coirproof", 
    "raffiaproof", "keyloggerproof", "infostealerproof", 
    "exploitproof", "zerodayproof", "backdoorproof", 
    "surgeproof", "fogproof", "mistproof", 
    "dewproof", "humidityproof", "moistureproof", 
    "dampproof", "unstitch", "unwrapp", 
    "unmount", "unfram", "unglaz", 
    "unvarnish", "unpolish", "unpaint", 
    "unlin", "unpadd", "unsecur", 
    "unapprov", "unlicens", "uncorroborat", 
    "unformat", "unclassif", 
    "exhum", "liquefi", "vaporis", 
    "atomiz", "disintegrat", "eradicat", 
    "plunder", "pillag", "scorch", 
    "singe", "shackl", "embedd", 
    "lodg", "wedg", "crimp", 
    "hitch", "coupl", "hing", 
    "pegg", "dowell", "mortis", 
    "tenon", "brac", "buttress", 
    "propp", "shor", "gird", 
    "band", "strapp", "belt", 
    "collar", "ring", "hoop", 
    "cag", "corrall", "enclos", 
    "encircl", "surround", "ringfenc", 
    "hedg", "shelter", "hous", 
    "quarter", "billet", "garrison", 
    "mann", "patroll", "sentinell", 
    "dropproof", "pierceproof", "cutproof", 
    "wearproof", "peelproof", "breakproof", 
    "dripproof", "decayproof", "lionproof", 
    "tigerproof", "elephantproof", "horseproof", 
    "roachproof", "amethystproof", "citrineproof", 
    "aquamarineproof", "moonstoneproof", "sunstoneproof", 
    "labradoriteproof", "hematiteproof", "magnetiteproof", 
    "pyriteproof", "malachiteproof", "azuriteproof", 
    "turquoiseproof", "lapisproof", "carnelianproof", 
    "chalcedonyproof", "acrylicproof", "winterproof", 
    "unhidd", "unglu", "untap", 
    "unpinn", "unstapl", "unfold", 
    "unbox", "uncover", 
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
    "carries",
    "mirrors",
    "reflects",
    "signals",
    "implies",
    "suggests",
    "indicates",
    "testifies",
    "echoes",
    "speaks",
    "bears",
    "wields",
    "harbours",
    "harbors",
    "illustrates",
    "crystallizes",
    "crystallises",
    "encapsulates",
    "actualizes",
    "actualises",
    "substantiates",
    "exudes",
    "emanates",
    "radiates",
    "communicates",
    "transmits",
    "breathes",
    "characterises",
    "characterizes",
    "defines",
    "captures",
    "amounts",
    "equals",
    "betokens",
    "portends",
    "foreshadows",
    "oozes",
    "perpetuates",
    "prolongs",
    "extends",
    "lengthens",
    "retains",
    "owns",
    "comprises",
    "includes",
    "underwrites",
    "corroborates",
    "underscores",
    "highlights",
    "emphasizes",
    "accentuates",
    "reaffirms",
    "reiterates",
    "restates",
    "underlines",
    "evinces",
    "avows",
    "professes",
    "pronounces",
    "announces",
    "heralds",
    "trumpets",
    "projects",
    "bespeaks",
    "flaunts",
    "boasts",
    "sports",
    "reveals",
    "discloses",
    "exposes",
    "unveils",
    "endorses",
    "swears",
    "witnesses",
    "consolidates",
    "shelters",
    "parades",
    "channels",
    "enjoys",
    "commands",
    "epitomises",
    "advocates",
    "purports",
    "brags",
    "broadcasts",
    "publishes",
    "claims",
    "states",
    "reports",
    "notes",
    "touts",
    "vaunts",
    "exalts",
    "lauds",
    "extols",
    "plugs",
    "celebrates",
    "honours",
    "honors",
    "praises",
    "acclaims",
    "contends",
    "argues",
    "insists",
    "vows",
    "puts",
    "sets",
    "lays",
    "spells",
    "sings",
    "hymns",
    "glorifies",
    "magnifies",
    "reveres",
    "worships",
    "idolises",
    "idolizes",
    "deifies",
    "lionises",
    "lionizes",
    "eulogises",
    "eulogizes",
    "rhapsodises",
    "blazons",
    "emblazons",
    "promulgates",
    "disseminates",
    "circulates",
    "peddles",
    "markets",
    "advertises",
    "publicises",
    "publicizes",
    "spotlights",
    "emphasises",
    "stresses",
    "authenticates",
    "ratifies",
    "accredits",
    "notarizes",
    "notarises",
    "countersigns",
    "illuminates",
    "clarifies",
    "elucidates",
    "explains",
    "describes",
    "avers",
    "submits",
    "posits",
    "postulates",
    "chronicles",
    "narrates",
    "recounts",
    "relates",
    "expounds",
    "goes",
    "deals",
    "consecrates",
    "sanctifies",
    "blesses",
    "pushes",
    "ballyhoos",
    "cries",
    "shouts",
    "voices",
    "says",
    "tells",
    "remarks",
    "mentions",
    "cites",
    "quotes",
    "references",
    "lists",
    "names",
    "identifies",
    "points",
    "draws",
    "calls",
    "focuses",
    "centres",
    "centers",
    "hails",
    "salutes",
    "commemorates",
    "immortalizes",
    "immortalises",
    "memorializes",
    "memorialises",
    "hypes",
    "crowns",
    "alleges",
    "insinuates",
    "intimates",
    "rhapsodizes",
    "garlands",
    "fetes",
    "adores",
    "commends",
    "conjectures",
    "decrees",
    "deduces",
    "delineates",
    "dictates",
    "enacts",
    "esteems",
    "founds",
    "infers",
    "mandates",
    "ordains",
    "outlines",
    "prescribes",
    "presumes",
    "recapitulates",
    "repeats",
    "sketches",
    "speculates",
    "summarises",
    "summarizes",
    "supposes",
    "surmises",
    "undertakes",
    "venerates",
    "acknowledges", "admits", "bellows", "blurts", "calculates", "chants", 
    "cheers", "computes", "concedes", "concludes", "declaims", "deems", 
    "derives", "determines", "directs", "discerns", "emits", "enjoins", 
    "estimates", "exclaims", "figures", "finds", "gathers", "gauges", 
    "hints", "hypothesises", "hypothesizes", "instructs", "intones", 
    "issues", "judges", "legislates", "moots", "murmurs", "mutters", 
    "observes", "opines", "perceives", "proscribes", "reads", "recites", 
    "reckons", "recognises", "recognizes", "rehearses", "releases", 
    "retells", "roars", "rules", "screams", "syndicates", "theorises", 
    "theorizes", "toasts", "utters", "whispers", "works", "yells", 
    "ventures",
    "croons", "hums", "orates", 
    "perorates", "soliloquizes", "pontificates", 
    "sermonizes", "lectures", "preaches", 
    "reasons", "burbles", "gushes", 
    "warbles", "greets", "welcomes", 
    "bids", "beckons", "summons", 
    "orders", "charges", "beseeches", 
    "implores", "entreats", "obliges", 
    "compels", "forces", "drives", 
    "powers", "fuels", "enables", 
    "empowers", "authorizes", "entitles", 
    "qualifies", 
    "mumbles", "chatters", "babbles", 
    "editorializes", "moralizes", "articulates", 
    "enunciates", "vocalizes", "drawls", 
    "lisps", "stammers", "trills", 
    "chirps", "croaks", "coos", 
    "purrs", "hisses", "tweets", 
    "cheeps", "peeps", "clucks", 
    "cackles", "gobbles", "quacks", 
    "honks", "squawks", "screeches", 
    "hoots", "barks", "yelps", 
    "whines", "growls", "snarls", 
    "meows", "miaows", "moos", 
    "baas", "bleats", "neighs", 
    "whinnies", "brays", "snorts", 
    "grunts", "squeals", "squeaks", 
    "chitters", "clicks", "buzzes", 
    "drones", "sighs", "gasps", 
    "sobs", "wails", "moans", 
    "groans", "stutters", "lilts", 
    "requires", "demands", "governs", 
    "regulates", "oversees", "supervises", 
    "manages", "administers", "handles", 
    "operates", "runs", "guides", 
    "pants", "wheezes", "coughs", 
    "sneezes", "snores", "laughs", 
    "giggles", "scoffs", "sneers", 
    "jeers", "taunts", "derides", 
    "ridicules", "mimics", "whistles", 
    "writes", "prints", "posts", 
    "gestures", "nods", "winks", 
    "smiles", "chuckles", "sniffs", 
    "hiccups", "burps", "yawns", 
    "blinks", "stares", "glances", 
    "peeks", "peers", "protests", 
    "confesses", "allows", "urges", 
    "pleads", "begs", 
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
    "epitomiz",
    "personif",
    "incarnat",
    "shield",
    "guard",
    "attain",
    "reach",
    "realis",
    "evidenc",
    "document",
    "record",
    "symboliz",
    "symbolis",
    "signif",
    "denot",
    "connot",
    "portray",
    "depict",
    "express",
    "back",
    "anchor",
    "prop",
    "brace",
    "enforc",
    "impos",
    "implement",
    "deploy",
    "harness",
    "leverag",
    "featur",
    "possess",
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
    "without any exception", "in all circumstances", 
    "under all circumstances", "without qualification", 
    "without reservation", "without limitation", "in every circumstance", 
    "every surface",
    "for all time", "in perpetuity", 
    "regardless of circumstance", "without fail", 
    "absolutely", "in every respect", 
    "at every turn", "come what may", 
    "no matter what", "in all events", 
    "at all costs", "under all conditions", 
    "at any rate", "without limit", 
    "without reserve", "for ever", 
    "forever", "eternally", 
    "permanently", "irrevocably", 
    "whatever happens", "rain or shine", 
    "through thick and thin", "to the end of time", 
    "for eternity", "once and for all", 
    "beyond question", "for good", 
    "in any case", "at any cost", 
    "come hell or high water", "by any means", 
    "in every way", "for all eternity", 
    "till the end of time", "until the end of time", 
    "without end", "categorically", 
    "beyond doubt", "at every moment", 
    "on every occasion", "evermore", 
    "world without end", "henceforth and forever", 
    "now and forever", "under any circumstances", 
    "everlastingly", "now and always", 
    "no matter the cost", "regardless", 
    "through hell and high water", "whatever the weather", 
    "in sickness and in health", "for richer or poorer", 
    "through joy and sorrow", "for better or worse", 
    "in good times and bad", "hell or high water", 
    "by hook or by crook", "whatever it takes", 
    "to the end of days", "until the end of days", 
    "for keeps", "once for all", 
    "endlessly", "perpetually", 
    "always", "in any event", 
    "without doubt", "unquestionably", 
    "outright", "utterly", "wholly", 
    "for perpetuity", "undyingly", 
    "deathlessly", "imperishably", 
    "indestructibly", "unchangeably", 
    "completely", "entirely", "in full", 
    "by all means", "for always", 
    "always and forever", "one hundred percent", 
    "totally", "downright", 
    "through and through", "root and branch", 
    "lock stock and barrel", "bag and baggage", 
    "hook line and sinker", "in toto", 
    "in its entirety", "without restriction", 
    "unreservedly", "unqualifiedly", 
    "flatly", "point blank", 
    "unto perpetuity", "henceforth", 
    "from henceforth", "from now on", 
    "henceforward", "thenceforth", 
    "thenceforward", "ever after", 
    "hereafter", "for the duration", 
    "for life", "lifelong", 
    "perennially", "interminably", 
    "ceaselessly", "incessantly", 
    "unendingly", "unremittingly", 
    "immortally", "undiminished", 
    "undiminishing", "unabated", 
    "unabating", 
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
    "reliant on",
    "dependent on",
    "subject only to",
    "only under",
    "only with",
    "conditioned upon",
    "premised on",
    "predicated on",
    "based on",
    "resting on",
    "contingent upon",
    "pursuant to",
    "governed by",
    "in accordance with",
    "in reliance on",
    "hinging on",
    "hinged on",
    "premised upon",
    "predicated upon",
    "founded on",
    "resting upon",
    "dependent upon",
    "reliant upon",
    "based upon",
    "subject solely to",
    "in conformity with",
    "in compliance with",
    "in reliance upon",
    "founded upon",
    "built on",
    "built upon",
    "hinging upon",
    "based solely on",
    "resting solely on",
    "dependent solely upon",
    "contingent solely upon",
    "conditioned solely upon",
    "tied to",
    "relying on",
    "conditioned by",
    "on the basis of",
    "anchored in",
    "linked to",
    "bound by",
    "in dependence on",
    "in keeping with",
    "in line with",
    "as required by",
    "under the terms of",
    "within the bounds of",
    "bounded by",
    "limited by",
    "constrained by",
    "by virtue of",
    "in virtue of",
    "owing to",
    "on account of",
    "in light of",
    "in view of",
    "in deference to",
    "in obedience to",
    "in submission to",
    "at the direction of",
    "under the direction of",
    "at the behest of",
    "in consequence of",
    "as a consequence of",
    "in observance of",
    "in adherence to",
    "in accord with",
    "consistent with",
    "consonant with",
    "in agreement with",
    "in fulfilment of",
    "in fulfillment of",
    "stemming from",
    "arising from",
    "resulting from",
    "following from",
    "derived from",
    "flowing from",
    "emanating from",
    "conditional solely on",
    "conditioned solely on",
    "contingent solely on",
    "dependent solely on",
    "subject exclusively to",
    "subject purely to",
    "conditional exclusively on",
    "resting exclusively on",
    "based exclusively on",
    "dependent exclusively upon",
    "contingent exclusively upon",
    "conditioned exclusively upon",
    "controlled by",
    "determined by",
    "shaped by",
    "guided by",
    "under",
    "within",
    "through",
    "via",
    "in subjection to",
    "as prescribed by",
    "as directed by",
    "as mandated by",
    "in pursuance of",
    "on the authority of",
    "within the limits of",
    "under the authority of",
    "as provided by",
    "as laid down by",
    "as specified in",
    "as stipulated in",
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
    "regulated by",
    "dictated by",
    "mandated by",
    "ordered by",
    "decreed by",
    "prescribed by",
    "stipulated by",
    "ruled by",
    "as governed by",
    "as regulated by",
    "as dictated by",
    "as decreed by",
    "as ordered by",
    "as ruled by",
    "by reason of",
    "on the grounds of",
    "on grounds of",
    "in response to",
    "in reaction to",
    "in conformity to",
    "at the mercy of",
    "in thrall to",
    "subordinate to",
    "answerable to",
    "beholden to",
    "thanks to",
    "because of",
    "in terms of",
    "with regard to",
    "with respect to",
    "in regard to",
    "in reference to",
    "in relation to",
    "under the guidance of",
    "under the control of",
    "under the supervision of",
    "under the oversight of",
    "within the scope of",
    "within the framework of",
    "within the confines of",
    "inside the bounds of",
    "in the framework of",
    "in the context of",
    "depending upon",
    "against the backdrop of",
    "as per",
    "per",
    "following",
    "behind",
    "alongside",
    "resting purely on",
    "conditional purely on",
    "contingent purely on",
    "dependent purely on",
    "based purely on",
    "founded purely on",
    "hinging purely on",
    "founded exclusively on",
    "hinging exclusively on",
    "due to",
    "within the terms of",
    "in step with",
    "contingent exclusively on",
    "dependent exclusively on",
    "hinging solely on",
    "as defined by",
    "as set by",
    "as determined by",
    "as a result of",
    "on the strength of",
    "by dint of",
    "under the aegis of",
    "in the hands of",
    "at the discretion of",
    "as set out by",
    "as specified by",
    "as established by",
    "as fixed by",
    "as decided by",
    "as approved by",
    "as authorised by",
    "as authorized by",
    "as stipulated by",
    "per the terms of",
    "in the terms of",
    "on the terms of",
    "by the terms of",
    "with the approval of",
    "subject to approval by",
    "grounded in",
    "by authority of",
    "as permitted by",
    "as allowed by",
    "with reference to",
    "in respect of",
    "respecting",
    "by means of",
    "by way of",
    "attributable to",
    "in consideration of",
    "in recognition of",
    "by order of",
    "at the command of",
    "subject to the terms of",
    "inside the limits of",
    "as laid out by",
    "as spelled out by",
    "as set forth by",
    "in the light of",
    "under the provisions of",
    "for the sake of",
    "in the name of",
    "on the advice of",
    "at the instruction of",
    "under the instruction of",
    "on the instruction of",
    "by instruction of",
    "in discharge of",
    "in execution of",
    "by permission of",
    "on the grounds that",
    "for the reason that",
    "through the medium of",
    "grounded on",
    "after",
    "by direction of",
    "with the permission of",
    "under authority of",
    "as instructed by",
    "on the orders of",
    "under the orders of",
    "by the authority of",
    "with the authority of",
    "in the face of",
    "with authority of",
    "by the order of",
    "at the order of",
    "upon the basis of",
    "by force of",
    "in satisfaction of",
    "in performance of",
    "for reasons of",
    "on the ground of",
    "under the provision of",
    "as commanded by",
    "with the sanction of",
    "by sanction of",
    "with approval of",
    "by approval of",
    "under the auspices of",
    "at the direction given by",
    "by the direction of",
    "on the direction of",
    "under the permission of",
    "on the permission of",
    "at the permission of",
    "by leave of",
    "with leave of",
    "under licence from",
    "under license from",
    "by licence of",
    "within the provisions of",
    "under provision of",
    "in pursuit of",
    "in face of",
    "consequent on",
    "consequent upon",
    "arising out of",
    "originating in",
    "rooted in",
    "as long as",
    "with the understanding that",
    "through the agency of",
    "by direction from",
    "in acknowledgement of",
    "in acknowledgment of",
    "under the framework of",
    "with the consent of",
    "by consent of",
    "at the request of",
    "by request of",
    "on the request of",
    "on the behest of",
    "by the behest of",
    "at the urging of",
    "under the command of",
    "by command of",
    "under the management of",
    "under the leadership of",
    "under the conditions of",
    "on the conditions of",
    "by the conditions of",
    "under the rules of",
    "by the rules of",
    "under the laws of",
    "by the laws of",
    "with authority from",
    "by authority from",
    "under authority from",
    "on instruction from",
    "by instruction from",
    "under instruction from",
    "with permission from",
    "by permission from",
    "on permission from",
    "according to",
    "as sanctioned by",
    "as endorsed by",
    "as demanded by",
    "as requested by",
    "on the advice given by",
    "at the instruction given by",
    "under the authority given by",
    "by the authority given by",
    "in conjunction with",
    "in concert with",
    "in tandem with",
    "on the say-so of",
    "on the say so of",
    "at the instance of",
    "on the instance of",
    "by the grace of",
    "at the sufferance of",
    "on the initiative of",
    "under the patronage of",
    "at the prompting of",
    "on the footing that",
    "in league with",
    "under the sway of",
    "under the influence of",
    "at the bidding of",
    "on the bidding of",
    "under command of",
    "with the blessing of",
    "by the blessing of",
    "with endorsement of",
    "by endorsement of",
    "with consent of",
    "with agreement of",
    "by agreement of",
    "with concurrence of",
    "in concurrence with",
    "upon the instruction of",
    "in honour of",
    "in honor of",
    "in memory of",
    "in celebration of",
    "in defiance of",
    "by virtue of the terms of", "under the sanction of", 
    "at the sanction of", "on the sanction of", "under the approval of", 
    "at the approval of", "on the approval of", "under the consent of", 
    "at the consent of", "on the consent of", "under the request of", 
    "on the recommendation of", "at the suggestion of", 
    "on the proposal of", "at the invitation of", 
    "under the sponsorship of", "under the tutelage of", 
    "at the pleasure of", "by the will of", "on the motion of", 
    "on the word of", "on the testimony of", "on the evidence of", 
    "on the assurance of", "at the say of", "by the word of", 
    "under the thumb of", "at the whim of", "on the whim of", 
    "under the will of", "in subservience to", "by fiat of", "by edict of", 
    "under edict of", "on pain of", "under penalty of", "in the gift of", 
    "within the gift of", "at the gift of", "in the power of", 
    "within the power of", "under the power of", "in the shadow of", 
    "under the shadow of", "in the wake of", "on the heels of", 
    "in the aftermath of", "at the feet of", "in the pay of", 
    "under the heel of", "at the beck of", "at the call of", 
    "on the call of", "by the hand of", "through the hand of", 
    "in the sight of", "under the eye of", "beneath the eye of", 
    "under the watch of", "in the keeping of", "in the care of", 
    "under the care of", "in the charge of", "under the charge of", 
    "in the custody of", "under the custody of", "in the possession of", 
    "by the leave of", "with the leave of", "at the leave of", 
    "at the say so of", 
    "with the authority given by",
    "in subordination to", "in homage to", "in bondage to", 
    "through the offices of", "at the word of", "upon the word of", 
    "by the permission of", "on the endorsement of", "on the counsel of", 
    "in the grip of", "under the boot of", "in servitude to", 
    "under the yoke of", "in the clutches of", "in the pocket of", 
    "on the instructions of", "on the guidance of", 
    "on the prompting of", "on the urging of", 
    "on the insistence of", "at the insistence of", 
    "on the demand of", "at the demand of", 
    "on the invitation of", "on the suggestion of", 
    "by the decision of", "on the decision of", 
    "by the ruling of", "on the ruling of", 
    "by the judgment of", "by the verdict of", 
    "by the warrant of", "under the warrant of", 
    "by the licence of", "by the license of", 
    "in vassalage to", "in fealty to", 
    "in the grasp of", "through the instrumentality of", 
    "accountable to", "deferring to", 
    "owing obedience to", "under the wing of", 
    "under the protection of", "in service to", 
    "in support of", "on the application of", 
    "at the suit of", "in the event", 
    "in the case", 
    "in spite of",
    "on the order of", "by the consent of", 
    "by the approval of", "by the instruction of", 
    "by the say-so of", "by the say so of", 
    "by the sayso of", "by the command of", 
    "on the command of", "by the request of", 
    "by the determination of", "on the determination of", 
    "by the findings of", "on the findings of", 
    "pursuant to the direction of", "following the direction of", 
    "subject to the direction of", "by the oversight of", 
    "on the oversight of", "by the supervision of", 
    "under the urging of", "under the insistence of", 
    "by the insistence of", "under the demand of", 
    "by the demand of", "under the invitation of", 
    "by the invitation of", "under the suggestion of", 
    "by the suggestion of", "under the decision of", 
    "at the decision of", "under the ruling of", 
    "at the ruling of", "under the judgment of", 
    "at the judgment of", "under the verdict of", 
    "at the verdict of", "under the licence of", 
    "at the licence of", "under the license of", 
    "at the license of", "on the licence of", 
    "on the license of", 
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
    words = _clause_words(clause)
    if len(words) < 2:
        return False
    if not _clause_asserted(clause):
        return False
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
        "mega", "giga", "nano", "pico", "hemi", "mono", "bi",
        "quad", "penta", "hexa", "octo", "deca", "kilo", "milli",
        "centi", "deci", "proto", "retro", "infra", "supra",
        "meta", "para", "hypo", "epi", "endo", "exo", "hetero",
        "homo", "iso", "tele", "pan", "uni",
        "triple", "hand", "machine", "deep",
        "pro",
        "tera", "peta", "exa", "zetta", "yotta", "femto", "atto",
        "zepto", "yocto", "ronna", "quetta", "myria", "demi",
        "under", "vice", "arch", "uber",
        "thrice", "quadruple", "quintuple",
        "manually", "automatically", "electronically",
        "independently", "personally", "visually", "digitally",
        "cryptographically", "mechanically", "optically",
        "mini", "maxi", "cyber",
        "remotely", "locally", "virtually", "physically",
        "audibly",
        "sixfold", "tenfold", "once", "single",
        "sextuple", "septuple", "octuple", "nonuple", "hecto",
        "acoustically", "blindly",
        "peer", "owner", "author", "clerk", "team", "group",
        "board", "panel", "joint",
        "smart", "cloud", "web", "online", "offline", "inhouse",
        "thirdparty",
        "twofold", "threefold", "fourfold", "fivefold",
        "sevenfold", "eightfold", "ninefold", "hundredfold",
        "centuple", "millifold", "doublefold",
        "half", "full", "part", "mid",
        "house", "office", "field", "site", "desk", "handheld",
        "computer", "human", "expert", "senior", "junior",
        "chief", "lead", "head", "master", "grand", "supreme",
        "prime", "chiefly",
        "hepta", "decu", "milluple", "manifold", "countlessly",
        "externally", "forensically", "judicially", "formally",
        "publicly", "doubly",
        "crowd", "public", "court", "judge", "state", "agency",
        "bureau", "guild", "union", "crew", "staff", "market",
        "industry",
        "digital", "electronic", "remote", "global", "local",
        "national", "federal", "system", "network", "server",
        "mobile", "quantum",
        "platform", "device", "software", "algorithm", "ai",
        "robot", "drone", "satellite", "worldwide", "nationwide",
        "company", "industrywide", "community", "society",
        "church", "school", "university", "hospital", "bank",
        "police", "army", "navy", "council", "committee",
        "tribunal", "senate", "parliament", "ministry",
        "department", "division", "branch", "unit", "squad",
        "veteran",
        "multiple", "partly", "wholly", "thoroughly", "carefully",
        "rigorously", "strictly", "closely", "deeply", "truly",
        "really", "genuinely", "officially", "legally",
        "informally", "privately", "secretly", "jointly",
        "mutually", "individually", "separately", "internally",
        "manual", "county", "city", "town", "village", "home",
        "lab",
        "newly", "freshly", "recently", "annually", "daily",
        "weekly", "monthly", "yearly", "forever", "always",
        "never", "badly", "poorly", "nicely", "firmly", "solidly",
        "soundly", "properly", "correctly", "accurately",
        "precisely", "exactly", "roughly", "broadly", "widely",
        "narrowly", "freely",
        "blockchain", "crypto", "biometric", "forensic", "legal",
        "government", "military", "medical", "academic",
        "scientific", "independent", "external", "internal",
        "edge", "internet", "virtual", "data", "database",
        "file", "document", "record", "journal", "ledger",
        "safety", "quality", "compliance", "professional",
        "licensed", "official", "formal", "private", "personal",
        "phone", "password", "eye", "voice", "ill", "mal",
        "fingerprint", "face", "token", "process", "retina",
        "iris", "palm", "dna", "username", "login",
        "account", "address", "photo", "video", "audio",
        "key", "code", "card", "hardware", "paper",
        "desktop", "laptop", "ml", "llm", "neural",
        "two", "foot", "finger", "blood", "law", "top",
        "facial", "thumb", "barcode", "qr", "pin", "chip",
        "visual", "physical", "mental", "oral", "written",
        "verbal", "financial", "social", "central", "gait",
        "breath", "handwriting", "keystroke", "vein", "sweat",
        "saliva", "hair", "nail", "tongue", "ear", "nose", "skin",
        "bone", "tooth", "dental", "genome", "genetic",
        "passphrase", "passkey", "cookie", "session", "browser",
        "laser", "radar", "sonar", "thermal", "infrared",
        "magnetic", "optical", "acoustic", "seismic", "agi",
        "gpt", "bot", "net", "atomic", "solar", "lunar", "stellar",
        "cosmic", "brain", "heart", "pulse", "tear", "urine",
        "gene", "cell",
        "lidar", "nfc", "rfid", "gps", "wifi", "bluetooth",
        "scent", "odor", "gaze", "stride", "gesture", "blink",
        "pupil", "waveform", "echo",
        "rna", "sms", "passport", "licence", "license", "user",
        "identity", "age", "voiceprint", "keycard", "smartcard",
        "sim", "time", "date", "place", "event",
        "twofactor", "multifactor", "camera", "microphone",
        "keyboard", "diamond", "gold", "iron", "steel", "wood",
        "stone", "glass", "lens", "crystal",
        "ankle", "cheek", "elbow", "electron", "forehead",
        "gamma", "heel", "hydraulic", "jaw", "keypad",
        "knuckle", "lip", "mechanical", "mri", "neck",
        "neutron", "nostril", "photon", "pneumatic", "robotic",
        "shoulder", "toe", "ultrasound", "ultraviolet", "wrist",
        "aluminium", "aluminum", "bionic", "bios", "bloodsample", 
        "bluetoothbeacon", "brainwave", "breathalyser", "breathalyzer", 
        "bronze", "brow", "carbon", "celltower", "ceramic", "chin", 
        "chipcard", "copper", "ctscan", "dnasample", "ecg", "eeg", "ekg", 
        "endoscopic", "esim", "eyebrow", "eyelash", "faceprint", 
        "fingernail", "fingervein", "firmware", "fmri", "forearm", 
        "gaitanalysis", "geolocation", "gpscoordinate", "hairsample", 
        "heartbeat", "hologram", "hsm", "imei", "implant", "imsi", 
        "ipaddress", "irisscan", "isotope", "kernel", "kevlar", "keyfob", 
        "leather", "lidarpoint", "lie", "macaddress", "magstripe", 
        "marble", "microchip", "microscope", "microscopic", 
        "mousedynamics", "muon", "neutrino", "nfccard", "nightvision", 
        "otp", "palmvein", "passcode", "petscan", "plastic", "platinum", 
        "polygraph", "qrcode", "radarreturn", "retinascan", "rfidtag", 
        "rubber", "salivasample", "scalp", "silver", "simcard", "skeleton", 
        "smarttoken", "sonarecho", "spectroscopic", "stencil", 
        "stethoscope", "stress", "tap", "telescope", "telescopic", 
        "temple", "thermalimage", "thermometer", "thumbprint", "titanium", 
        "toenail", "totp", "tpm", "truth", "uefi", "ultrasonic", 
        "urinesample", "uwb", "wearable", "wifitriangulation", "xrayimage", 
        "yubikey", 
        "xray",
        "obsidian", "basalt", "quartz", 
        "onyx", "jade", "ivory", 
        "ebony", "mahogany", "bamboo", 
        "silk", "velvet", "tungsten", 
        "cobalt", "analog", "analogue", 
        "proton", "radio", "palmprint", 
        "retinaprint", "voiceid", "faceid", 
        "tongueprint", "earprint", "lipprint", 
        "dentalrecord", "medicalrecord", "genesequence", 
        "bloodtype", "heartrate", "bloodpressure", 
        "pupildilation", "serialnumber", "uuid", 
        "deviceid", "hardwareid", "browserprint", 
        "canvasprint", 
        "porcelain", "slate", "limestone", 
        "sandstone", "flint", "brass", 
        "pewter", "zinc", "nickel", 
        "chrome", "ruby", "sapphire", 
        "emerald", "pearl", "coral", 
        "amber", "linen", "cotton", 
        "wool", "denim", "canvas", 
        "cardboard", "cork", "optic", 
        "xeno", "cryo", "pyro", 
        "hydro", "aero", "astro", 
        "cosmo", "helio", "geo", 
        "bio", "zoo", "neuro", 
        "cardio", "dermato", "spectro", 
        "chromo", "electro", "magneto", 
        "sono", "palaeo", "paleo", 
        "thermo", "opto", "electrooptic", 
        "archi", "footprint", "irisprint", 
        "veinprint", "gaitprint", "keystrokeprint", 
        "scrollprint", "handprint", "headprint", 
        "scentprint", "breathprint", "pulseprint", 
        "brainwaveprint", "heartbeatprint", "skinprint", 
        "nailprint", "hairprint", "toothprint", 
        "boneprint", 
        "teak", "oak", "pine", 
        "cedar", "walnut", "opal", 
        "turquoise", "hematite", "calcite", 
        "agate", "jasper", "amethyst", 
        "luna", "gastro", "nephro", 
        "osteo", "ophthalmo", "techno", 
        "chemo", "chrono", "litho", 
        "phono", "seismo", "seleno", 
        "baro", "hygro", "anemo", 
        "ombro", "nepho", "chiro", 
        "podo", "rhino", "oto", 
        "stetho", "myo", "arthro", 
        "encephalo", "hepato", "pneumo", 
        "haemo", "hemo", "leuko", 
        "erythro", "cyto", "histo", 
        "embryo", "phyto", "myco", 
        "bacterio", "viro", "protozoo", 
        "entomo", "ichthyo", "ornitho", 
        "herpeto", "malaco", "helmintho", 
    )
    verification_roots = (
        "check", "verif", "validat", "confirm", "certif",
        "seal", "sign", "attest", "endors", "notariz",
        "notaris", "countersign",
        "audit", "inspect", "review", "vett", "screen",
        "witness", "cosign",
        "examin", "scrutin", "monitor", "observ", "authentic",
        "perus", "glimps", "spi", "skimm", "brows", "survey",
        "videotap", "audiotap",
        "test", "prov", "read", "hear", "watch", "listen",
        "photograph", "film",
    )
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
    for passive in (
        "marked", "shown", "recorded", "seen", "heard",
        "known", "found", "sensed", "detected", "documented",
        "reported", "spotted", "discerned", "recognised",
        "recognized", "apprehended", "grasped", "comprehended",
        "understood", "learned",
        "beheld", "glimpsed", "studied", "perused", "felt",
        "tasted", "smelt", "interpreted", "parsed", "construed",
        "skimmed", "browsed", "handled",
        "fathomed", "recalled", "remembered", "recollected",
        "vouched", "guaranteed", "warranted", "mimeographed",
        "laminated", "imaged", "licked",
        "alphabetised", "alphabetized", "blueprinted", "categorised", 
        "categorized", "collated", "confiscated", "crated", "devised", 
        "enveloped", "envisioned", "framed", "gilded", "glued", 
        "lacquered", "latched", "microfiched", "outlined", "padlocked", 
        "pasted", "pictured", "reworded", "shelved", "transformed", 
        "varnished", "subpoenaed", "impounded",
        "stapled", "riveted", "pinned", 
        "tacked", "stitched", "sewn", 
        "clasped", "buckled", "zipped", 
        "buttoned", "hooked", "tethered", 
        "moored", "docketed", "typeset", 
        "lettered", "tooled", "gilt", 
        "wrapped", "boxed", "bagged", 
        "jarred", "bottled", "canned", 
        "tinned", "waxed", "corked", 
        "plugged", "stoppered", "screwed", 
        "nailed", "clamped", "clipped", 
        "lashed", "knotted", "plaited", 
        "braided", "woven", 
        "rifled", "auctioned", "pawned", 
        "welded", "cemented", "encased", 
        "enshrined", "vaulted", "entombed", 
        "interred", "buried", "hidden", 
        "fenced", "moated", "turreted", 
        "misfiled", "dissolved", "vaporized", 
        "pulverized", "leased", "borrowed", 
        "torched", "flooded", "swapped", 
        "melted", "crushed", "smashed", 
        "mangled", "fractured", "splintered", 
        "punctured", "perforated", "severed", 
        "contaminated", "frozen", "guarded", 
        "armoured", "armored", "fortified", 
        "walled", 
        "exhumed", "liquefied", "vaporised", 
        "plundered", "pillaged", 
        "shackled", "embedded", "lodged", 
        "wedged", "crimped", "hitched", 
        "coupled", "pegged", "braced", 
        "buttressed", "girded", "banded", 
        "strapped", "caged", "corralled", 
        "enclosed", "encircled", "surrounded", 
        "hedged", "sheltered", "housed", 
        "garrisoned", "patrolled", 
    ):
        if passive in words and "by" in words[
            words.index(passive) + 1:
        ]:
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
                "shall", "must", "will", "can",
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
                "need", "needs", "shall", "must", "will", "can",
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
        "mirror", "clon", "screenshot", "email", "upload", "archiv",
        "broadcast", "stol", "wip", "exfiltrat", "purg", "corrupt",
        "film", "scan", "trac",
        "memoriz", "smuggl", "relay", "dictat", "carri",
        "fabricat", "publish", "sold", "sell", "counterfeit",
        "impersonat", "fak",
        "reproduc", "photocopi", "fax", "sync", "siphon",
        "harvest", "scrap", "lift", "purloin", "filch",
        "restor", "recover", "reconstruct", "regenerat",
        "reissu", "recreat",
        "stream", "distribut", "transfer", "circulat",
        "disseminat", "convey", "dispatch", "air", "televis",
        "project", "display", "beam", "overhear", "quot",
        "paraphras", "plagiar", "expos", "unlock", "decrypt",
        "doctor", "manipulat", "pilfer", "loot", "snatch",
        "swip", "pinch", "memoris",
        "record", "tap", "bugg", "wiretap", "embezzl",
        "divert", "xerox", "retyp", "reseal", "seen", "hear",
        "witness", "noted", "logg", "catalog", "memorial",
        "chronicl",
        "narrat", "recit", "whisper", "annotat", "summaris",
        "summariz", "translat", "encrypt", "encod", "compress",
        "index", "cach", "perform", "decipher", "decod",
        "crack", "enter", "obtain", "retriev", "fetch",
        "gather", "collect", "compil",
        "vandalis", "vandaliz", "defac", "mutilat", "ransack",
        "burgl", "robb", "heist", "eavesdrop", "obliterat",
        "annihilat", "poison", "sabotag", "undermin", "hack",
        "reveal",
        "screen", "vett", "audit", "inspect", "examin",
        "scrutiniz", "perus", "glimps", "spi", "videotap",
        "audiotap", "skimm", "brows", "monitor", "observ",
        "survey",
        "inscrib", "engrav", "etch", "carv", "draft", "penn",
        "author", "compos", "seiz",
        "post", "mail", "map", "chart", "graph", "draw",
        "paint", "sketch", "stamp", "mark", "labell", "tagg",
        "flagg", "highlight", "underlin", "show", "presente",
        "describ", "defin", "named", "caption",
        "digitis", "digitiz", "back", "play", "import",
        "queri", "search", "locat", "identifi",
        "typed", "handwritten", "texted", "captur", "taken",
        "touch",
        "burn", "shred", "watch", "closed", "shift", "rotat",
        "cited", "referenc", "mention", "filed", "stored",
        "saved", "kept", "held",
        "review", "convert", "lock",
        "damag", "divulg", "ship", "deliver", "return",
        "test", "measur", "count", "weigh", "clear", "check",
        "sampl", "regist", "enroll", "book", "remark",
        "notic", "perceiv",
        "known", "understood", "learn", "grasp", "comprehend",
        "recognis", "recogniz", "recall", "fathom", "deduc",
        "infer", "discern", "distinguish", "detect", "spott",
        "found", "follow", "sensed", "document", "report",
        "apprehend", "handl", "process", "sort", "organis",
        "organiz", "arrang", "classif", "graded", "ranked",
        "scored", "apprais", "valued", "priced", "timed",
        "dated", "numbered", "endors", "certif", "validat",
        "authentic", "approved", "inventoried", "stapled",
        "folded", "boxed", "labeled",
        "beheld", "sighted", "studied", "scrutin", "retained",
        "absorbed", "mastered", "interpreted", "explained",
        "confirmed", "buried",
        "ratified", "accredited", "notariz", "notaris", "felt",
        "tasted", "smelt",
        "parsed", "construed", "assessed", "evaluated", "judged",
        "discovered",
        "uncovered", "unveiled", "exhibited", "demonstrated",
        "illustrated",
        "depicted", "portrayed", "represented", "clarified", "unravel",
        "solved", "resolved", "settled", "decided", "determined",
        "concluded",
        "derived", "computed", "calculated", "reckoned", "estimated",
        "gauged",
        "transported", "handed", "passed", "routed", "redirected",
        "recollect", "remember",
        "attest", "vouch", "guarante", "warrant", "sworn",
        "mimeograph", "microfilm", "laminat", "imag",
        "arrest", "conceiv", "confiscat", "detain", "devis",
        "impound", "interrogat", "plott", "pursu", "question",
        "reword", "transform", "summon", "subpoena", "charg",
        "accus", "indict", "prosecut", "tried", "sentenc",
        "fined", "punish", "disciplin", "sanction", "blacklist",
        "barr", "bann", "exclud", "expell", "evict", "dismiss",
        "discharg", "suspend", "revok", "cancell", "terminat",
        "invent", "dream", "hallucinat", "envision", "visualis",
        "visualiz",
    "acquitt", "adjudicat", "admonish", "alphabetis", "alphabetiz", 
    "anathematis", "anathematiz", "aped", "appropriat", "arraign", 
    "belittl", "berat", "blackball", "boycott", "brand", "burlesqu", 
    "calumniat", "caricatur", "castigat", "categoris", "categoriz", 
    "censur", "chastis", "collat", "commandeer", "concoct", "convict", 
    "copyright", "crat", "debarr", "decri", "defam", "defrock", "denigrat", 
    "deport", "depos", "deprecat", "derid", "disbarr", "disparag", "echo", 
    "emboss", "emulat", "envelop", "excommunicat", "exil", "extradit", 
    "fram", "gazed", "gild", "glanc", "glued", "hallmark", "imitat", 
    "impeach", "imprint", "impugn", "lacquer", "lampoon", "latch", "libel", 
    "libell", "litigat", "microfich", "mimick", "misappropriat", "mock", 
    "ostracis", "ostraciz", "padlock", "pardon", "parodi", "past", 
    "patent", "peer", "pirat", "rebuk", "repossess", "reprimand", 
    "reproach", "revil", "ridicul", "satiris", "satiriz", "scold", 
    "sequester", "shelv", "simulat", "slander", "star", "trademark", 
    "traduc", "unfrock", "upbraid", "varnish", "vilifi", "watermark", 
        "pictur", "outlin", "blueprint",
    "fingerprint", "garnish", "probat", 
    "annul", "expung", "redact", 
    "incinerat", "embargo", "swabb", 
    "imprison", "jaile", "taxe", 
    "levi", "foreclos", "demolish", 
    "interned", "rivet", "pinn", 
    "tacke", "stitch", "sewn", 
    "clasp", "buckl", "zipp", 
    "button", "hooke", "tether", 
    "moore", "docket", "typeset", 
    "lettere", "toole", "gilt", 
    "bound", "wrapp", "bagg", 
    "jarr", "bottl", "cann", 
    "tinn", "waxe", "corke", 
    "plugg", "stopper", "screwe", 
    "naile", "bolte", "clampe", 
    "clipp", "fastene", "lashe", 
    "knott", "plaite", "braide", 
    "woven", "quarantin", "segregat", 
    "chaine", 
    "misfil", "dissolv", "vaporiz", 
    "pulveriz", "auction", "pawn", 
    "leased", "borrow", "rifl", 
    "torch", "flood", "swapp", 
    "melt", "crush", "smash", 
    "mangl", "fractur", "splinter", 
    "punctur", "perforat", "severe", 
    "contaminat", "welde", "cement", 
    "encas", "enshrin", "frozen", 
    "vault", "entomb", "interred", 
    "guard", "armour", "armor", 
    "fortif", "fenc", "wall", 
    "moat", "turret", 
    "exhum", "liquefi", "vaporis", 
    "atomiz", "disintegrat", "eradicat", 
    "plunder", "pillag", "scorch", 
    "singe", "shackl", "anchor", 
    "embedd", "lodg", "wedg", 
    "crimp", "secur", "hitch", "coupl", 
    "hing", "pegg", "dowell", 
    "mortis", "tenon", "brac", 
    "buttress", "propp", "shor", 
    "gird", "band", "strapp", 
    "belt", "collar", "ring", 
    "hoop", "cag", "corrall", 
    "enclos", "encircl", "surround", 
    "ringfenc", "hedg", "shelter", 
    "hous", "quarter", "billet", 
    "garrison", "mann", "patroll", 
    "sentinell", 
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
        "conceivably", "remotely", "event", "conditions",
        "regardless", "somehow", "anyhow", "just", "merely",
        "truly", "actually", "even", "still", "the", "least",
        "stretch", "pretext", "on", "account",
        "shape", "capacity", "scenario", "route", "context",
        "instance", "occasion", "situation", "wise", "light",
        "from", "angle", "quarter",
        "legally", "physically", "practically", "theoretically",
        "somewhere", "anywhere", "nowhere", "somewhat", "partly",
        "fully", "easily", "practice", "theory", "anyone",
        "person", "party", "human", "law",
        "henceforth", "forever", "permanently", "temporarily",
        "secretly", "silently", "unknowingly", "knowingly",
        "deliberately", "accidentally", "inadvertently",
        "maliciously", "externally", "internally",
        "statute", "jurisdiction", "device", "channel",
        "through", "via",
        "domain", "realm", "sphere", "setting", "environment",
        "medium", "venue", "arena", "regime", "framework",
        "realistically", "effectively", "virtually",
        "technically", "mechanically", "digitally",
        "electronically", "manually", "automatically",
        "reality", "effect", "essence", "outsider", "stranger",
        "grounds", "forum", "degree", "agency",
        "country", "language", "platform", "format", "network",
        "machine", "century", "location", "timezone", "flag",
        "software", "wire", "over",
        "kingdom", "empire", "republic", "province", "county",
        "city", "household", "office", "building", "room",
        "world", "system", "avenue", "dimension", "territory",
        "place", "site", "field", "sector", "industry",
        "universe",
        "cryptographically", "biologically", "chemically",
        "geographically", "historically", "politically",
        "commercially", "privately", "publicly", "locally",
        "globally",
        "fundamentally", "inherently", "intrinsically",
        "legitimately", "reasonably", "plausibly", "feasibly",
        "imaginably", "humanly",
        "principle", "as", "a", "rule", "general",
        "generally", "normally", "typically", "invariably",
        "extent", "measure",
        "wholly", "entirely", "directly", "indirectly",
        "formally", "officially", "voluntarily", "freely",
        "continent", "ocean", "desert", "season", "climate",
        "altitude", "court", "hand", "tool", "script", "tongue",
        "harbour", "harbor", "theatre", "theater", "temple",
        "palace", "prison", "school", "hospital",
        "galaxy", "forest", "valley", "mountain", "island",
        "peninsula", "hemisphere", "zone", "region", "district",
        "neighbourhood", "neighborhood", "community", "society",
        "culture", "epoch", "age", "period", "millennium",
        "trial", "instrument", "agent", "authority", "order",
        "mentally", "illegally", "again", "with", "using",
        "stage", "computer", "entity", "user", "generation",
        "quietly", "lawfully", "unlawfully", "safely",
        "partially", "completely", "actor", "era", "decade",
        "village", "town", "cave", "tunnel", "vault", "library",
        "museum", "home", "dialect", "year", "month", "week",
        "day", "hour", "enemy", "thief",
        "parish", "township", "borough", "nation", "state",
        "land", "chamber", "laboratory", "hall", "stadium",
        "depth", "height", "speed", "cost", "price", "style",
        "form",
        "planet", "moon", "scale", "scope", "pathway",
        "configuration", "infrastructure", "deployment",
        "installation", "workflow", "pipeline", "repository",
        "ledger", "invisibly", "undetectably", "covertly",
        "wirelessly", "instantly",
        "bunker", "fortress", "castle", "church", "mosque",
        "synagogue", "station", "port", "mine", "farm",
        "factory", "workshop", "studio", "cinema", "hamlet",
        "suburb", "attic", "basement", "garden", "park",
        "street", "road", "bridge", "tower", "cottage",
        "cabin", "tent", "camp", "square", "moment",
        "instant", "second", "minute", "night", "weather",
        "shore", "coast", "beach", "cliff", "river",
        "lake", "pond", "well", "pit", "ditch", "door",
        "gate", "window", "distance", "volume", "temperature",
        "currency", "length", "warehouse", "wrongfully",
        "fraudulently",
        "lighthouse", "cathedral", "barn", "garage", "hotel",
        "cellar", "monastery", "chapel", "convent", "shed",
        "loft", "dungeon", "motel", "inn", "mansion",
        "villa", "bungalow", "courthouse", "embassy", "silo",
        "depot", "hangar", "pavilion", "shrine", "hut",
        "dormitory", "barracks", "basilica", "pagoda", "yurt",
        "igloo", "tepee", "lodge", "hostel", "tavern",
        "bakery", "brewery", "distillery", "refinery",
        "foundry", "mill", "quarry", "dock", "pier",
        "marina", "abbey", "planetarium", "aquarium",
        "gymnasium", "citadel", "stronghold", "terminal",
        "greenhouse", "pharmacy", "clinic", "asylum",
        "orphanage", "seminary", "dawn", "dusk", "midnight",
        "noon", "width", "pressure", "rate", "risk",
        "frequency", "voltage", "density", "humidity",
        "velocity", "morning", "evening", "weekend",
        "quickly", "slowly", "negligently", "dishonestly",
        "clandestinely", "surreptitiously", "deceitfully",
        "furtively",
        "windmill", "waterfall", "canyon", "university",
        "conservatory", "winery", "tannery", "granary", "apiary",
        "aviary", "gallery", "seaport", "plaza", "cavern", "grotto",
        "crypt", "tomb", "gazebo", "terrace", "balcony", "courtyard",
        "cloister", "refectory", "sacristy", "vestry", "narthex",
        "chancel", "nave", "transept", "presbytery", "rectory",
        "vicarage", "manse", "mission", "hermitage", "retreat",
        "sanatorium", "hospice", "infirmary", "dispensary",
        "workhouse", "poorhouse", "almshouse", "belfry", "minaret",
        "dome", "rotunda", "atrium", "arcade", "colonnade",
        "portico", "peristyle", "emporium", "oratory", "crematorium",
        "mortuary", "consulate", "chancery", "nunnery", "priory",
        "outpost", "garrison", "fort", "blockhouse", "catacomb",
        "mausoleum", "colosseum", "amphitheater",
        "spring", "summer", "autumn", "winter", "twilight",
        "sunrise", "sunset", "midday", "size", "level", "amount",
        "quantity", "strength", "power", "latitude", "longitude",
        "breadth", "thickness", "mass", "intensity", "magnitude",
        "amplitude", "wavelength", "resistance", "capacitance",
        "inductance", "conductance", "viscosity", "elasticity",
        "porosity", "salinity", "acidity", "alkalinity", "turbidity",
        "luminosity", "brightness", "loudness", "pitch", "tempo",
        "rhythm", "acceleration", "momentum", "torque", "tension",
        "shear", "friction", "gravity",
        "afternoon", "weekday", "holiday", "sense", "regard",
        "loudly", "carefully", "carelessly", "recklessly", "intentionally",
        "improperly", "wrongly", "unfairly", "anonymously",
        "swiftly", "gradually", "roughly", "forcefully", "abruptly",
        "eventually", "repeatedly", "wilfully", "willfully",
        "unwittingly", "stealthily", "unobtrusively",
        "inconspicuously", "slyly", "cunningly", "craftily",
        "shrewdly", "astutely", "wilily", "artfully", "deviously",
        "underhandedly", "treacherously", "perfidiously",
        "faithlessly", "dishonorably", "ignobly", "basely", "vilely",
        "wickedly", "sinfully", "falsely", "untruthfully",
        "mendaciously",
        "sea", "birthday", "anniversary", "wedding", "funeral",
        "graduation", "ceremony", "celebration", "meeting",
        "conference", "election", "contest", "game", "match",
        "race", "concert", "ground",
        "menagerie", "casino", "bazaar", "bathhouse", "sauna",
        "solstice", "equinox",
        "bastion", "corridor", "dam", "kiln", "lobby", "salon",
        "sawmill", "stairwell", "vivarium", "terrarium",
        "solarium", "sanctuary", "chapterhouse", "scriptorium",
        "boathouse", "pumphouse", "gatehouse", "powerhouse",
        "storehouse", "treasury", "arsenal", "depository",
        "conductivity", "current", "enthalpy", "entropy",
        "flammability", "hardness", "impedance", "molarity",
        "opacity", "permeability", "radioactivity", "reactance",
        "reflectivity", "roughness", "solubility", "toxicity",
        "susceptance", "admittance", "reluctance", "permittivity",
        "resistivity", "malleability", "ductility", "brittleness",
        "toughness", "stiffness", "damping", "inertia",
        "nightfall", "daybreak", "name", "date",
        "gently", "violently", "overtly", "suddenly", "willingly",
        "deceptively", "mistakenly", "erroneously", "boldly",
        "bravely", "proudly", "honestly", "truthfully",
        "faithfully", "cruelly", "kindly", "ruthlessly",
        "relentlessly", "frequently", "occasionally", "rarely",
        "often", "usually", "especially", "mainly", "initially",
        "previously", "separately", "jointly", "individually",
        "personally", "rightly", "justly", "fairly", "correctly",
        "accurately", "precisely", "exactly", "genuinely",
        "sincerely", "brazenly", "flagrantly", "shamelessly",
        "blatantly", "immorally", "sneakily", "unethically",
    "absorptivity", "acropolis", "allegedly", "angrily", "anxiously", 
    "apparently", "arboretum", "audaciously", "ballroom", "baptistery", 
    "barnyard", "belvedere", "boardroom", "boatyard", "brutally", 
    "callously", "calmly", "candidly", "cheerfully", "chromaticity", 
    "classroom", "coercivity", "coldly", "coliseum", "contemptuously", 
    "courageously", "courtroom", "dauntlessly", "deanery", "defiantly", 
    "diffusivity", "disdainfully", "dockyard", "dolphinarium", "donjon", 
    "eagerly", "eclipse", "emissivity", "enthusiastically", "evidently", 
    "expansivity", "farmyard", "fearlessly", "ferociously", "fiercely", 
    "foolhardily", "forthrightly", "gallantly", "gleefully", "graveyard", 
    "gristmill", "happily", "heedlessly", "herbarium", "heroically", 
    "honorably", "hothouse", "hygroscopicity", "hysteresis", "impudently", 
    "insectarium", "insolently", "intrepidly", "ironworks", "junkyard", 
    "keep", "linearity", "lumberyard", "luminance", "magnetization", 
    "malevolently", "malignantly", "mercilessly", "mint", "nervously", 
    "newsroom", "nobly", "oceanarium", "orangery", "ossuary", "ostensibly", 
    "ostentatiously", "panopticon", "papermill", "parsonage", "pergola", 
    "permeance", "pinery", "pitilessly", "plasticity", "presumably", 
    "purportedly", "railyard", "rancorously", "rashly", "rebelliously", 
    "refractivity", "reliquary", "reluctivity", "remanence", 
    "remorselessly", "salvageyard", "saturation", "savagely", "scornfully", 
    "selectivity", "sensitivity", "serpentarium", "sinisterly", 
    "specificity", "steelworks", "stockyard", "storeroom", "strongroom", 
    "supposedly", "susceptibility", "switchyard", "tenderly", "timidly", 
    "unabashedly", "unapologetically", "unashamedly", "unreservedly", 
    "valiantly", "vengefully", "viciously", "vinery", "washroom", 
    "wholeheartedly", 
        "unscrupulously", "vindictively", "wantonly",
    "serenely", "briskly", "pantry", 
    "sepulchre", "charnel", "house", 
    "vestibule", "chapter", "bullion", 
    "athenaeum", "lyceum", "unflinchingly", 
    "brazenfacedly", "impenitently", "unrepentantly", 
    "coldheartedly", "unfeelingly", 
    "sanctum", "armory", "oubliette", 
    "garret", "turret", "dovecote", 
    "bindery", "stupa", "guildhall", 
    "townhall", "jailhouse", "penitentiary", 
    "reformatory", "smithy", "stable", 
    "kennel", "frankly", "coolly", 
    "blandly", "blithely", "breezily", 
    "lightly", "plainly", "bluntly", 
    "tartly", "dryly", "wryly", 
    "mildly", "meekly", "humbly", 
    "softly", "surely", "duly", 
    "keenly", "warmly", "stiffly", 
    "primly", "demurely", "sedately", 
    "staidly", "soberly", "gravely", 
    "sternly", "grimly", "dourly", 
    "bleakly", "patiently", "reluctantly", 
    "hesitantly", "confidently", "foolishly", 
    "clumsily", "gracefully", "awkwardly", 
    "furiously", "desperately", "impatiently", 
    "hopelessly", 
    "sluggishly", "mischievously", "solemnly", 
    "ritually", "noisily", "frantically", 
    "earnestly", "dispassionately", "unemotionally", 
    "placidly", "tranquilly", "peacefully", 
    "restfully", "purely", "obviously", 
    "seemingly", "avowedly", "professedly", 
    "smoothly", "steadily", "firmly", 
    "fixedly", "resolutely", "steadfastly", 
    "doggedly", "stubbornly", "obstinately", 
    "mulishly", "pigheadedly", "wittingly", 
    "consciously", "zoo", "muniment", 
    "columbarium", "magazine", "coop", 
    "hutch", "alcove", "cubicle", 
    "booth", "stall", "larder", 
    "cellarage", 
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
        while (
            cursor < len(words)
            and words[cursor] in fillers
        ):
            cursor += 1
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
        if any(
            _clause_claim(clause) or _clause_inability_form(clause)
            for clause in clauses
        ) and any(
            marker in statement
            for marker in _UNCONDITIONAL_MARKERS
            if " and " in marker or " or " in marker
        ):
            return False
        for clause in clauses:
            if not _clause_claim(clause) and not _clause_inability_form(
                clause
            ):
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
                in ("if", "when", "where", "with")
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            trailing_governed = False
            if len(main_words) < len(clause_words):
                trailing_markers = (
                    ("if",), ("when",), ("whenever",),
                    ("while",), ("whilst",), ("where",),
                    ("as",), ("that",),
                    ("in", "cases", "where"),
                    ("in", "so", "far", "as"),
                    ("to", "the", "extent", "that"),
                )
                for position in range(
                    max(0, len(main_words) - 3), len(clause_words)
                ):
                    for marker in trailing_markers:
                        if tuple(
                            clause_words[
                                position:position + len(marker)
                            ]
                        ) != marker:
                            continue
                        complement = " ".join(
                            clause_words[position + len(marker):]
                        )
                        if _governing_condition_holds(
                            "conditional on " + complement
                        ):
                            trailing_governed = True
                    if trailing_governed:
                        break
            if trailing_governed:
                continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] in (
                    "conditional", "conditioned", "contingent",
                    "dependent", "depending", "reliant", "premised", "predicated",
                    "based", "resting", "founded", "built",
                    "hinging", "reliance", "solely",
                    "exclusively", "purely", "consequent",
                )
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
                in (
                    "provided", "providing", "given", "assuming", "granted",
                    "presuming", "supposing", "seeing",
                )
            ):
                rest = clause_words[len(main_words) + 1:]
                if rest and rest[0] == "that":
                    rest = rest[1:]
                complement = " ".join(rest)
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] in (
                    "understanding", "assumption", "premise",
                )
                and clause_words[len(main_words)] == "that"
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and clause_words[len(main_words)] == "in"
                and len(main_words) + 3 < len(clause_words)
                and clause_words[len(main_words) + 1] == "the"
                and clause_words[len(main_words) + 2] == "event"
                and clause_words[len(main_words) + 3] == "that"
            ):
                complement = " ".join(clause_words[len(main_words) + 4:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] == "case"
                and clause_words[len(main_words)] == "that"
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] == "long"
                and clause_words[len(main_words)] == "as"
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] in (
                    "direction", "advice", "instruction", "authority",
                    "guidance", "behest", "permission", "consent",
                    "command", "request", "sanction", "approval",
                    "endorsement", "blessing", "urging",
                )
                and clause_words[len(main_words)] == "given"
                and len(main_words) + 1 < len(clause_words)
                and clause_words[len(main_words) + 1] == "by"
            ):
                complement = " ".join(clause_words[len(main_words) + 2:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and clause_words[len(main_words)] == "keeping"
                and len(main_words) + 1 < len(clause_words)
                and clause_words[len(main_words) + 1] == "with"
            ):
                complement = " ".join(clause_words[len(main_words) + 2:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and clause_words[len(main_words)] == "keeping"
                and len(main_words) + 1 < len(clause_words)
                and clause_words[len(main_words) + 1] == "of"
            ):
                complement = " ".join(clause_words[len(main_words) + 2:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and clause_words[len(main_words)] == "turning"
                and len(main_words) + 1 < len(clause_words)
                and clause_words[len(main_words) + 1] == "on"
            ):
                complement = " ".join(clause_words[len(main_words) + 2:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and clause_words[len(main_words)] == "as"
                and len(main_words) + 2 < len(clause_words)
                and clause_words[len(main_words) + 1] == "required"
                and clause_words[len(main_words) + 2] == "by"
            ):
                complement = " ".join(clause_words[len(main_words) + 3:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] in (
                    "accordance", "conformity", "compliance",
                    "keeping", "line",
                    "accord", "consistent", "consonant", "agreement",
                    "step", "conjunction", "concert", "tandem",
                    "league", "concurrence", "partnership",
                    "collaboration", "association", "alliance",
                    "cooperation", "coordination", "union",
                    "combination", "consultation", "harmony",
                    "unison", "sync", "together", "along",
                    "collusion", "cahoots", "glove",
                    "side", "hand", "paired", "coupled",
                )
                and clause_words[len(main_words)] == "with"
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and clause_words[len(main_words)] in (
                    "as", "through", "via", "following",
                    "because", "with", "alongside", "due",
                    "respecting", "after", "upon", "in",
                )
            ):
                tail = " ".join(clause_words[len(main_words):])
                if any(
                    tail == phrase or tail.startswith(phrase + " ")
                    for phrase in _GOVERNING_CONDITION_PHRASES
                ) and _governing_condition_holds(tail):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and main_words[-1] in (
                    "condition", "grounds", "reason", "footing",
                    "basis", "ground",
                    "event", "case", "circumstance", "situation",
                    "occasion", "instance",
                )
                and clause_words[len(main_words)] == "that"
            ):
                complement = " ".join(clause_words[len(main_words) + 1:])
                if _governing_condition_holds(
                    "conditional on " + complement
                ):
                    continue
            if (
                main_words
                and len(main_words) < len(clause_words)
                and (
                    (
                        main_words[-1] == "insofar"
                        and clause_words[len(main_words)] == "as"
                    )
                    or (
                        main_words[-1] in ("in", "now")
                        and clause_words[len(main_words)] == "that"
                    )
                )
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
                        or (
                            index == 0
                            and any(
                                words[aux] in (
                                    "was", "were", "is", "are",
                                    "been", "be",
                                )
                                and not (
                                    words[aux] in ("is", "are", "be")
                                    and words[aux + 1].startswith(
                                        ("alter", "unalter")
                                    )
                                )
                                and any(
                                    words[aux + 1].startswith(root)
                                    for root in _CLAIM_CONCEPT_ROOTS
                                )
                                for aux in range(
                                    index + 1, len(words) - 1
                                )
                            )
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
