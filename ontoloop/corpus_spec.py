"""Corpus specification module, slice SPEC-CORPUS form.

The corpus specification surface: the trace shaped corpus
specification, stated as data in this module. It carries
hard negatives in the three named shapes, labelled secret
bearing shapes, a decoding round field on every decoded
candidate, and per shape rate reporting with no single
aggregate, and its pair part stands in commitment form
only, a minimum of 30 labelled pairs of each kind as a
completeness condition, with no production count cited as
specification evidence.

The specification's structure stands grounded in the plan
and the brief, while its worked content stands as authored
specification in the design record of slice SPEC-CORPUS:
the negative cases, the decoded candidates and their
rounds, the rate values, the labelled pairs and their
labels, and the labelling act and protocol names are the
authored specification act of this slice, carrying the
guessed source class, not text transcribed from the brief
or the plan.

What this slice does not build stands unbuilt behind the
module level guard at the foot of this file: the corpus
production at POPULATED and every consuming surface. A
lookup of a public name this module does not provide
raises AssertionError in the NOT BUILT form the suite
harness uses. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.corpus_spec"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "corpus_specification",
    "rate_report",
    "pair_part",
]


# Section: corpus specification data and specification
# return, roster 910.
# Names: _CORPUS_SPECIFICATION_V1, _T03_NAMINGS_V1, and
# corpus_specification.
# Insertion point for the whole section: in
# system/ontoloop/corpus_spec.py, after the module docstring
# and roster 912's constants and __all__ at the head of the
# assembled file, before roster 911's boundary section and
# before roster 912's guard foot at the foot, in the
# composition order the scope act states.
# Cross section contract, stated for the assembly check and
# for roster 911: roster 911's rate_report and pair_part
# read this section's data at call time through the module
# globals, by calling corpus_specification() on each call
# and reading the return by name, in the form this
# section's paper states in full: the per shape rates stand
# at the return's "rates" mapping, keyed by shape, each
# value carrying "rate", "rate_kind", and
# "rate_denominator"; the pair data stands at the return's
# "pair_part" mapping, carrying "kinds", "commitments",
# "labelled_pairs", and "evidence". The stated structure
# below, _CORPUS_SPECIFICATION_V1, is the one source those
# returns are built from, so the boundary returns cannot
# drift from the specification return. No name in this
# section is defined by any other section, and this section
# calls no name another section owns. This section carries
# no in function NOT BUILT seam.

# The authored corpus specification, in whole form, taken
# from the appended specification part of
# design/steps/step-14-spec-corpus-shape.md. The three
# shapes stand in the grounded order. Each shape entry
# carries its label, its authored negative cases, its
# authored decoded candidates with their decoding_round
# values, and its authored rate with its kind and its
# denominator stated in words. The pair part carries the
# two grounded kind keys, the grounded commitment per kind,
# and the 60 authored labelled pairs, 30 per kind, each
# with both members, its pairing ground, and its label. The
# labelling mapping carries the three T03 namings standing
# together: the labeller in its grounded form, and the
# labelling act and protocol under their authored names,
# with the authored statements of what each names.
# Everything authored in this structure stands recorded as
# authored and guessed, never as source text, never as
# transcription, and never as a measured figure, in the
# honesty form the specification part states. Every case,
# candidate, and pair is a synthetic shape example only; no
# real credential, key, or token value stands anywhere in
# this structure.
# Representation discipline, entry 58: every authored value
# carrying a scanner shaped token form (the digest, base64,
# and hex values of the specification part, and the grouped
# identifier of case NC-ID-04 following the part's grouped
# presentation) stands in split source representation
# below, as two adjacent literals split inside the value,
# at the split points the part states. Each such value's
# runtime value is exactly the part's joined value. Every
# other value stands whole, as authored.
# Negative case form, stated once: a mapping with the keys
# "id", "statement", "values", "legitimate_because", and
# "note". The statement names the trace and its load
# bearing content in the part's words, without embedding a
# scanner shaped value; "values" holds the case's salient
# values as strings, in the order the statement names them;
# "legitimate_because" holds the part's legitimacy ground;
# "note" holds the part's further rationale sentence where
# one stands, and stands empty where none stands.
# Decoded candidate form, stated once: a mapping with the
# keys "id", "decoding_round" (an int in the bound 1 to
# 3), "forms" (the decoding forms in chain order),
# "encoded_material", "intermediates" (the intermediate
# decoded values the part prints explicitly, in chain
# order; empty where the part names an intermediate only
# in kind), "decoded_form", "chain" (the chain steps, in
# order, in words), and "statement" (the part's closing
# sentence for the candidate).
_CORPUS_SPECIFICATION_V1 = {
    "hard_negatives": (
        {
            "shape": "hash heavy",
            "label": "secret bearing shape",
            "negative_cases": (
                {
                    "id": "NC-HH-01",
                    "statement": (
                        "A build trace line recording the digest "
                        "of an empty input file kept as a fixture"
                    ),
                    "values": (
                        "e3b0c44298fc1c149afbf4c8996fb924"
                        "27ae41e4649b934ca495991b7852b855",
                    ),
                    "legitimate_because": (
                        "the digest is the whole content of the "
                        "record and no secret stands behind it"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-HH-02",
                    "statement": (
                        "A test trace line recording the digest "
                        "of the synthetic word test"
                    ),
                    "values": (
                        "9f86d081884c7d659a2feaa0c55ad015"
                        "a3bf4f1b2b0b822cd15d6c15b0f00a08",
                    ),
                    "legitimate_because": (
                        "the input is a published synthetic word "
                        "and the digest only proves the fixture ran"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-HH-03",
                    "statement": (
                        "An archive trace line recording the "
                        "digest of the synthetic phrase "
                        "synthetic trace alpha"
                    ),
                    "values": (
                        "f300e2e2d927d6be91ab63ea5fd24134"
                        "ee2c30a131e914ec820a18aa70951fe9",
                    ),
                    "legitimate_because": (
                        "the phrase is invented for this "
                        "specification and the digest is a "
                        "checksum over public text"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-HH-04",
                    "statement": (
                        "A second archive trace line recording "
                        "the digest of the synthetic phrase "
                        "synthetic trace beta"
                    ),
                    "values": (
                        "5c97ce25a6bfd3f993a1ae1b97863414"
                        "a8e80c6372beb03e5137fbe8d6e34c17",
                    ),
                    "legitimate_because": (
                        "the same ground as NC-HH-03"
                    ),
                    "note": (
                        "a fourth case stands here because this "
                        "shape needs more than one archive "
                        "example to show the shape is a "
                        "population, not a single fixture"
                    ),
                },
            ),
            "decoded_candidates": (
                {
                    "id": "DC-HH-01",
                    "decoding_round": 1,
                    "forms": ("base64",),
                    "encoded_material": (
                        "OGJmNDA0NGZhMjU0M2E4YzA1OTRiMzk1NDljNThiY2Ni"
                        "YjkyYzIwNmY2MGNkODA4ZjViMjY5MTJmMmQzZDdlOA=="
                    ),
                    "intermediates": (),
                    "decoded_form": (
                        "8bf4044fa2543a8c0594b39549c58bcc"
                        "bb92c206f60cd808f5b26912f2d3d7e8"
                    ),
                    "chain": (
                        "one base64 decoding step yields the "
                        "decoded form, a digest text",
                    ),
                    "statement": (
                        "that digest is the digest of the "
                        "synthetic phrase ontoloop synthetic "
                        "hash example, so the candidate is hash "
                        "shaped material carried one encoding deep"
                    ),
                },
                {
                    "id": "DC-HH-02",
                    "decoding_round": 2,
                    "forms": ("hex", "base64"),
                    "encoded_material": (
                        "6147467a6143426a614746706269426a6147"
                        "566a6179426a62323177624756305a513d3d"
                    ),
                    "intermediates": (
                        "aGFzaCBjaGFpbiBjaG"
                        "VjayBjb21wbGV0ZQ==",
                    ),
                    "decoded_form": "hash chain check complete",
                    "chain": (
                        "hex decoding yields the base64 text "
                        "in intermediates",
                        "base64 decoding of that text yields "
                        "the decoded form, a plain phrase",
                    ),
                    "statement": (
                        "the candidate shows hash adjacent "
                        "material, a hex wrapper, hiding a "
                        "plain completion phrase two rounds deep"
                    ),
                },
            ),
            "rate": 0.21,
            "rate_kind": "fire rate",
            "rate_denominator": (
                "the share of legitimate traces of the hash "
                "heavy shape in the trace shaped corpus as "
                "specified for production, the full population "
                "of legitimate traces of this shape, counted "
                "one per trace, on which a generic redaction "
                "layer fires, raising a hit, even though the "
                "trace is legitimate"
            ),
        },
        {
            "shape": "identifier heavy",
            "label": "secret bearing shape",
            "negative_cases": (
                {
                    "id": "NC-ID-01",
                    "statement": (
                        "A request trace line carrying the "
                        "request identifier and the trace "
                        "identifier, both invented for this "
                        "specification"
                    ),
                    "values": (
                        "req synthetic 0042",
                        "tr synthetic 0042",
                    ),
                    "legitimate_because": (
                        "the identifiers name a synthetic "
                        "request and disclose nothing beyond "
                        "its place in a trace"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-ID-02",
                    "statement": (
                        "A session trace line carrying the "
                        "session identifier in plain form"
                    ),
                    "values": (
                        "session synthetic 1187, user usr "
                        "synthetic 0091, device dev synthetic 003",
                    ),
                    "legitimate_because": (
                        "every identifier is invented and the "
                        "line records only that a synthetic "
                        "session opened"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-ID-03",
                    "statement": (
                        "A job trace line carrying the job "
                        "identifier and the parent job identifier"
                    ),
                    "values": (
                        "job synthetic 2026 0113",
                        "job synthetic 2026 0112",
                    ),
                    "legitimate_because": (
                        "the pair of identifiers records a "
                        "synthetic job lineage and nothing else"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-ID-04",
                    "statement": (
                        "A lookup trace line carrying a "
                        "universally unique identifier in its "
                        "standard grouped hex form, for a "
                        "synthetic record"
                    ),
                    "values": (
                        "550e8400-e29b-"
                        "41d4-a716-446655440000",
                    ),
                    "legitimate_because": (
                        "the identifier is a published style "
                        "example value with invented content, "
                        "standing in the trace as a record key"
                    ),
                    "note": (
                        "a fourth case stands here because "
                        "this shape needs both word shaped and "
                        "grouped hex shaped identifiers to be "
                        "an honest example of its character"
                    ),
                },
            ),
            "decoded_candidates": (
                {
                    "id": "DC-ID-01",
                    "decoding_round": 1,
                    "forms": ("URL decoding",),
                    "encoded_material": (
                        "request%20id%20req%20synthetic%200042%20traced"
                    ),
                    "intermediates": (),
                    "decoded_form": (
                        "request id req synthetic 0042 traced"
                    ),
                    "chain": (
                        "one URL decoding step yields the "
                        "decoded form, plain identifier text",
                    ),
                    "statement": (
                        "the candidate shows identifier material "
                        "carried under percent encoding one "
                        "round deep"
                    ),
                },
                {
                    "id": "DC-ID-02",
                    "decoding_round": 3,
                    "forms": (
                        "URL decoding",
                        "base64",
                        "hex",
                    ),
                    "encoded_material": (
                        "NzU3MzY1NzIyMDY5NjQyMDc1NzM3MjIwNzM3OTZlNzQ2ODY1NzQ2OTYzMjAzMDMwMzQzMg"
                        "%3D%3D"
                    ),
                    "intermediates": (),
                    "decoded_form": "user id usr synthetic 0042",
                    "chain": (
                        "URL decoding yields a base64 text",
                        "base64 decoding yields a hex string",
                        "hex decoding yields the decoded "
                        "form, plain identifier text",
                    ),
                    "statement": (
                        "the candidate shows identifier material "
                        "at the full grounded depth of 3 rounds"
                    ),
                },
            ),
            "rate": 0.17,
            "rate_kind": "fire rate",
            "rate_denominator": (
                "the share of legitimate traces of the "
                "identifier heavy shape in the trace shaped "
                "corpus as specified for production, the full "
                "population of legitimate traces of this "
                "shape, counted one per trace, on which a "
                "generic redaction layer fires, raising a hit, "
                "even though the trace is legitimate"
            ),
        },
        {
            "shape": "configuration heavy",
            "label": "secret bearing shape",
            "negative_cases": (
                {
                    "id": "NC-CF-01",
                    "statement": (
                        "A pair of settings lines, one for the "
                        "log level and one for the log destination"
                    ),
                    "values": (
                        "log_level = info",
                        "log_destination = local file",
                    ),
                    "legitimate_because": (
                        "both values are plain logging choices"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-CF-02",
                    "statement": (
                        "A pair of settings lines, one for the "
                        "timeout and one for the retry count"
                    ),
                    "values": (
                        "timeout_seconds = 30",
                        "max_retries = 3",
                    ),
                    "legitimate_because": (
                        "both values are small plain numbers"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-CF-03",
                    "statement": (
                        "A pair of settings lines, one for "
                        "each of two feature flags"
                    ),
                    "values": (
                        "feature_flag checkout_v2 = false",
                        "feature_flag new_search = true",
                    ),
                    "legitimate_because": (
                        "flag states are product choices, not "
                        "secrets, and the flag names are invented"
                    ),
                    "note": "",
                },
                {
                    "id": "NC-CF-04",
                    "statement": (
                        "A pair of settings lines, one naming "
                        "where an api key value would come from "
                        "and one naming a database host"
                    ),
                    "values": (
                        "api_key_source = environment variable name only",
                        "database_host = db.internal.example",
                    ),
                    "legitimate_because": (
                        "the first line names where a value "
                        "would come from and states no value at "
                        "all, and the second host name is an "
                        "invented example host"
                    ),
                    "note": (
                        "a fourth case stands here because "
                        "this shape needs a field name case "
                        "with no value, which is the case a "
                        "wide table costs the most on"
                    ),
                },
            ),
            "decoded_candidates": (
                {
                    "id": "DC-CF-01",
                    "decoding_round": 2,
                    "forms": ("base64", "URL decoding"),
                    "encoded_material": (
                        "bG9nX2xldmVsJTIwJTNE"
                        "JTIwaW5mbw=="
                    ),
                    "intermediates": (
                        "log_level%20%3D%20info",
                    ),
                    "decoded_form": "log_level = info",
                    "chain": (
                        "base64 decoding yields the URL "
                        "encoded text in intermediates",
                        "URL decoding yields the decoded "
                        "form, a plain configuration line",
                    ),
                    "statement": (
                        "the candidate shows a configuration "
                        "line carried two rounds deep"
                    ),
                },
                {
                    "id": "DC-CF-02",
                    "decoding_round": 3,
                    "forms": ("hex", "base64", "URL decoding"),
                    "encoded_material": (
                        "64476c745a5739316446397a5a574e76626d"
                        "527a4a5449774a544e454a5449774d7a413d"
                    ),
                    "intermediates": (
                        "timeout_seconds%20%3D%2030",
                    ),
                    "decoded_form": "timeout_seconds = 30",
                    "chain": (
                        "hex decoding yields a base64 text",
                        "base64 decoding yields the URL "
                        "encoded text in intermediates",
                        "URL decoding yields the decoded "
                        "form, a plain configuration line",
                    ),
                    "statement": (
                        "the candidate shows a configuration "
                        "line at the full grounded depth of "
                        "3 rounds"
                    ),
                },
            ),
            "rate": 0.26,
            "rate_kind": "fire rate",
            "rate_denominator": (
                "the share of legitimate traces of the "
                "configuration heavy shape in the trace shaped "
                "corpus as specified for production, the full "
                "population of legitimate traces of this "
                "shape, counted one per trace, on which a "
                "generic redaction layer fires, raising a hit, "
                "even though the trace is legitimate"
            ),
        },
    ),
    "pair_part": {
        "kinds": ("paraphrase pairs", "near verbatim pairs"),
        "commitments": {
            "paraphrase pairs": {"form": "minimum", "count": 30},
            "near verbatim pairs": {"form": "minimum", "count": 30},
        },
        "labelled_pairs": {
            "paraphrase pairs": (
                {
                    "id": "PP-01",
                    "member_1": "Restart the worker after the configuration change takes effect.",
                    "member_2": "Once the new settings are live, bring the worker down and back up.",
                    "pair_ground": "same instruction, restart after a change, with verb, order, and nouns all changed.",
                    "label": "paraphrase pairs / holds / worker restart timing",
                },
                {
                    "id": "PP-02",
                    "member_1": "The scan flags any line that looks like a secret.",
                    "member_2": "Lines resembling credentials are raised by the scanner.",
                    "pair_ground": "same claim about the scanner, restated with subject and verb exchanged.",
                    "label": "paraphrase pairs / holds / scanner flagging rule",
                },
                {
                    "id": "PP-03",
                    "member_1": "Keep the raw traces until the review is finished.",
                    "member_2": "Do not delete the original trace records before reviewers are done.",
                    "pair_ground": "same retention instruction, stated once positively and once as a prohibition.",
                    "label": "paraphrase pairs / holds / trace retention rule",
                },
                {
                    "id": "PP-04",
                    "member_1": "A digest lets a reader check that a file did not change.",
                    "member_2": "Readers can confirm a file is unchanged by comparing its hash.",
                    "pair_ground": "same purpose of a digest, with hash named as the same thing in other words.",
                    "label": "paraphrase pairs / holds / digest check purpose",
                },
                {
                    "id": "PP-05",
                    "member_1": "The operator labels each pair by hand at construction time.",
                    "member_2": "During construction, every pair receives its label from the operator personally.",
                    "pair_ground": "same labelling fact, with hand and personally carrying the same manual sense.",
                    "label": "paraphrase pairs / holds / operator labelling act",
                },
                {
                    "id": "PP-06",
                    "member_1": "Rates are reported for each shape on its own.",
                    "member_2": "No combined figure replaces the separate figure for every shape.",
                    "pair_ground": "same reporting rule, per shape and no aggregate, stated from opposite sides.",
                    "label": "paraphrase pairs / holds / per shape reporting",
                },
                {
                    "id": "PP-07",
                    "member_1": "Encoded text may hide plain text several layers down.",
                    "member_2": "What looks like gibberish can contain ordinary words under repeated decoding.",
                    "pair_ground": "same layering claim, with encoded and gibberish and layers and repeated decoding paired.",
                    "label": "paraphrase pairs / holds / layered encoding claim",
                },
                {
                    "id": "PP-08",
                    "member_1": "The corpus is built before the scanner is tuned on it.",
                    "member_2": "Tuning waits until the corpus exists.",
                    "pair_ground": "same ordering claim, build first and tune second, compressed in Member 2.",
                    "label": "paraphrase pairs / holds / build before tuning",
                },
                {
                    "id": "PP-09",
                    "member_1": "A legitimate trace can still trip a wide filter.",
                    "member_2": "Even harmless records sometimes trigger a broad rule.",
                    "pair_ground": "same false firing claim, with legitimate and harmless and wide and broad paired.",
                    "label": "paraphrase pairs / holds / benign false firing",
                },
                {
                    "id": "PP-10",
                    "member_1": "Each candidate records the round at which it was decoded.",
                    "member_2": "For every decoded item, the depth of its decoding is written down.",
                    "pair_ground": "same field claim, round and depth of decoding carrying the same meaning.",
                    "label": "paraphrase pairs / holds / decoding round field",
                },
                {
                    "id": "PP-11",
                    "member_1": "Configuration lines state choices, not secrets.",
                    "member_2": "Settings text records decisions and holds no credentials.",
                    "pair_ground": "same character claim for configuration material, choices and decisions paired.",
                    "label": "paraphrase pairs / holds / configuration line character",
                },
                {
                    "id": "PP-12",
                    "member_1": "The specification fixes the minimum pair count for each kind.",
                    "member_2": "For every kind, the smallest number of pairs is set by the specification.",
                    "pair_ground": "same commitment claim, minimum and smallest number paired.",
                    "label": "paraphrase pairs / holds / pair count minimum",
                },
                {
                    "id": "PP-13",
                    "member_1": "Identifiers let a reader follow one request through a long trace.",
                    "member_2": "A single request can be tracked across a lengthy record by its identifiers.",
                    "pair_ground": "same purpose claim for identifiers, follow and tracked paired.",
                    "label": "paraphrase pairs / holds / identifier tracking purpose",
                },
                {
                    "id": "PP-14",
                    "member_1": "Production counts are kept apart from the specification counts.",
                    "member_2": "Figures from actually building the corpus never merge into the promised figures.",
                    "pair_ground": "same separation rule, production and actually building paired, counts and figures paired.",
                    "label": "paraphrase pairs / holds / production count separation",
                },
                {
                    "id": "PP-15",
                    "member_1": "A new version of the corpus is recorded whenever its contents change.",
                    "member_2": "Any change to what the corpus holds means a fresh version entry.",
                    "pair_ground": "same versioning rule from plan DQ-SPEC-25 content, change and fresh version paired.",
                    "label": "paraphrase pairs / holds / corpus version rule",
                },
                {
                    "id": "PP-16",
                    "member_1": "The labeller is the person running the build, not a program.",
                    "member_2": "Labelling is done by the operator and never automated.",
                    "pair_ground": "same labeller claim, person running the build and operator paired.",
                    "label": "paraphrase pairs / holds / labeller identity claim",
                },
                {
                    "id": "PP-17",
                    "member_1": "Hard negatives exist so false alarms can be measured.",
                    "member_2": "Benign lookalike cases are included to make the false firing rate countable.",
                    "pair_ground": "same purpose claim, hard negatives and benign lookalike cases paired.",
                    "label": "paraphrase pairs / holds / hard negative purpose",
                },
                {
                    "id": "PP-18",
                    "member_1": "Nothing in the specification counts as a measured result.",
                    "member_2": "Every figure the specification states is a stated figure, not an observed one.",
                    "pair_ground": "same standing claim, measured and observed paired in the negative.",
                    "label": "paraphrase pairs / holds / no measured figures",
                },
                {
                    "id": "PP-19",
                    "member_1": "The pair part closes on its promised counts alone.",
                    "member_2": "Only the commitment inside the specification decides whether this part is complete.",
                    "pair_ground": "same closing claim, promised counts and commitment paired.",
                    "label": "paraphrase pairs / holds / commitment closing form",
                },
                {
                    "id": "PP-20",
                    "member_1": "A trace may carry the name of a key without carrying its value.",
                    "member_2": "Key names can appear in a record while the secret itself stays out.",
                    "pair_ground": "same distinction, name without value and secret stays out paired.",
                    "label": "paraphrase pairs / holds / name without value",
                },
                {
                    "id": "PP-21",
                    "member_1": "Decoding stops after three rounds at the deepest.",
                    "member_2": "No item is unwrapped more than three times.",
                    "pair_ground": "same depth bound claim, rounds and times paired.",
                    "label": "paraphrase pairs / holds / decoding depth bound",
                },
                {
                    "id": "PP-22",
                    "member_1": "Each shape is reported with its own rate.",
                    "member_2": "Every shape gets a rate of its own in the report.",
                    "pair_ground": "same per shape claim in near minimal rewording that still changes the sentence frame.",
                    "label": "paraphrase pairs / holds / own rate per shape",
                },
                {
                    "id": "PP-23",
                    "member_1": "The stage record, not the test run, carries the naming evidence.",
                    "member_2": "Whether the act and protocol are named is judged from the stage record alone.",
                    "pair_ground": "same evidence home claim for row T03, naming evidence and judged from paired.",
                    "label": "paraphrase pairs / holds / naming evidence home",
                },
                {
                    "id": "PP-24",
                    "member_1": "Synthetic examples stand in for real material throughout the specification.",
                    "member_2": "Every worked example here is invented rather than drawn from real traces.",
                    "pair_ground": "same synthetic standing claim, stand in and invented paired.",
                    "label": "paraphrase pairs / holds / synthetic example standing",
                },
                {
                    "id": "PP-25",
                    "member_1": "A wide field name table fires often on configuration material.",
                    "member_2": "Configuration text is where a broad name list produces the most false alarms.",
                    "pair_ground": "same grounded character claim for the configuration shape, wide and broad paired.",
                    "label": "paraphrase pairs / holds / wide table cost",
                },
                {
                    "id": "PP-26",
                    "member_1": "The module returns the specification and nothing about production.",
                    "member_2": "What the surface hands back is the specification only, with no production figures inside.",
                    "pair_ground": "same surface claim, returns and hands back paired.",
                    "label": "paraphrase pairs / holds / surface returns specification",
                },
                {
                    "id": "PP-27",
                    "member_1": "Labels on specification pairs say the pair relation holds.",
                    "member_2": "On each pair in the specification, the label states that its two members match as claimed.",
                    "pair_ground": "same label meaning claim, in the label form this part authors.",
                    "label": "paraphrase pairs / holds / label meaning claim",
                },
                {
                    "id": "PP-28",
                    "member_1": "Worked cases stand beside every rule in a specification.",
                    "member_2": "No rule in a specification stands without example cases next to it.",
                    "pair_ground": "same worked material rule from plan section 4.5, stated positively and negatively.",
                    "label": "paraphrase pairs / holds / worked case rule",
                },
                {
                    "id": "PP-29",
                    "member_1": "The same sentence can be written so a string match misses it.",
                    "member_2": "Rewording a sentence defeats any check that looks for exact text.",
                    "pair_ground": "same paraphrase risk claim, which is the reason this kind exists in the corpus.",
                    "label": "paraphrase pairs / holds / rewording defeats matching",
                },
                {
                    "id": "PP-30",
                    "member_1": "Authored content is recorded as authored wherever it is used.",
                    "member_2": "Anything invented for the specification keeps its invented standing in every record.",
                    "pair_ground": "same recording rule for this very part, authored and invented paired.",
                    "label": "paraphrase pairs / holds / authored standing rule",
                },
            ),
            "near verbatim pairs": (
                {
                    "id": "NV-01",
                    "member_1": "Restart the worker after the configuration change takes effect.",
                    "member_2": "Restart the worker after the configuration update takes effect.",
                    "pair_ground": "one word differs, change against update, all else word for word.",
                    "label": "near verbatim pairs / holds / worker restart wording",
                },
                {
                    "id": "NV-02",
                    "member_1": "The scan flags any line that looks like a secret.",
                    "member_2": "The scan flags every line that looks like a secret.",
                    "pair_ground": "one word differs, any against every.",
                    "label": "near verbatim pairs / holds / scan flag quantifier",
                },
                {
                    "id": "NV-03",
                    "member_1": "Keep the raw traces until the review is finished.",
                    "member_2": "Keep the raw traces until the review is complete.",
                    "pair_ground": "one word differs, finished against complete.",
                    "label": "near verbatim pairs / holds / trace keeping wording",
                },
                {
                    "id": "NV-04",
                    "member_1": "A digest lets a reader check that a file did not change.",
                    "member_2": "A digest lets a reader check that the file did not change.",
                    "pair_ground": "one word differs, a against the before file.",
                    "label": "near verbatim pairs / holds / digest check wording",
                },
                {
                    "id": "NV-05",
                    "member_1": "The operator labels each pair by hand.",
                    "member_2": "The operator labels each pair by hand at construction.",
                    "pair_ground": "Member 2 adds the short phrase at construction and changes nothing else.",
                    "label": "near verbatim pairs / holds / labelling by hand",
                },
                {
                    "id": "NV-06",
                    "member_1": "Rates are reported for each shape on its own.",
                    "member_2": "Rates are reported for each shape on its own, with no aggregate.",
                    "pair_ground": "Member 2 adds a trailing clause and changes nothing else.",
                    "label": "near verbatim pairs / holds / per shape rate clause",
                },
                {
                    "id": "NV-07",
                    "member_1": "Encoded text may hide plain text several layers down.",
                    "member_2": "Encoded text may hide plain text three layers down.",
                    "pair_ground": "one word differs, several against three.",
                    "label": "near verbatim pairs / holds / layers down wording",
                },
                {
                    "id": "NV-08",
                    "member_1": "The corpus is built before the scanner is tuned.",
                    "member_2": "The corpus is built before the scanner is retuned.",
                    "pair_ground": "one word differs, tuned against retuned.",
                    "label": "near verbatim pairs / holds / build before tuning",
                },
                {
                    "id": "NV-09",
                    "member_1": "A legitimate trace can still trip a wide filter.",
                    "member_2": "A legitimate trace can still trip a wider filter.",
                    "pair_ground": "one word differs, wide against wider.",
                    "label": "near verbatim pairs / holds / wide filter wording",
                },
                {
                    "id": "NV-10",
                    "member_1": "Each candidate records the round at which it was decoded.",
                    "member_2": "Each candidate records the round at which it was raised.",
                    "pair_ground": "one word differs, decoded against raised, in the rerun passage sense.",
                    "label": "near verbatim pairs / holds / candidate round wording",
                },
                {
                    "id": "NV-11",
                    "member_1": "Configuration lines state choices, not secrets.",
                    "member_2": "Configuration lines state choices, not secret values.",
                    "pair_ground": "one word added, values after secret, all else the same.",
                    "label": "near verbatim pairs / holds / configuration choices wording",
                },
                {
                    "id": "NV-12",
                    "member_1": "The minimum pair count for each kind is thirty.",
                    "member_2": "The minimum pair count for each kind is 30.",
                    "pair_ground": "the number stands as a word in Member 1 and as figures in Member 2, all else the same.",
                    "label": "near verbatim pairs / holds / pair count number form",
                },
                {
                    "id": "NV-13",
                    "member_1": "Identifiers let a reader follow one request through a trace.",
                    "member_2": "Identifiers let a reader follow one request through the trace.",
                    "pair_ground": "one word differs, a against the before trace.",
                    "label": "near verbatim pairs / holds / identifier following wording",
                },
                {
                    "id": "NV-14",
                    "member_1": "Production counts are kept apart from specification counts.",
                    "member_2": "Production counts are kept separate from specification counts.",
                    "pair_ground": "one word differs, apart against separate.",
                    "label": "near verbatim pairs / holds / counts kept apart",
                },
                {
                    "id": "NV-15",
                    "member_1": "A change to the corpus contents is a new corpus version.",
                    "member_2": "A change to the corpus contents means a new corpus version.",
                    "pair_ground": "one word differs, is against means.",
                    "label": "near verbatim pairs / holds / version change wording",
                },
                {
                    "id": "NV-16",
                    "member_1": "The labeller is the operator.",
                    "member_2": "The labeller is the operator, and no one else.",
                    "pair_ground": "Member 2 adds a short trailing phrase and changes nothing else.",
                    "label": "near verbatim pairs / holds / labeller operator wording",
                },
                {
                    "id": "NV-17",
                    "member_1": "Hard negatives exist so false alarms can be measured.",
                    "member_2": "Hard negatives exist so false alarms can be counted.",
                    "pair_ground": "one word differs, measured against counted.",
                    "label": "near verbatim pairs / holds / false alarm wording",
                },
                {
                    "id": "NV-18",
                    "member_1": "Nothing in the specification counts as a measured result.",
                    "member_2": "Nothing in this specification counts as a measured result.",
                    "pair_ground": "one word differs, the against this before specification.",
                    "label": "near verbatim pairs / holds / measured result wording",
                },
                {
                    "id": "NV-19",
                    "member_1": "The pair part closes on its promised counts alone.",
                    "member_2": "The pair part closes on its promised counts only.",
                    "pair_ground": "one word differs, alone against only.",
                    "label": "near verbatim pairs / holds / closing counts wording",
                },
                {
                    "id": "NV-20",
                    "member_1": "A trace may carry the name of a key without its value.",
                    "member_2": "A trace may carry the name of a key, without its value.",
                    "pair_ground": "punctuation only differs, a comma added, all words the same.",
                    "label": "near verbatim pairs / holds / key name punctuation",
                },
                {
                    "id": "NV-21",
                    "member_1": "Decoding stops after three rounds.",
                    "member_2": "Decoding stops after 3 rounds.",
                    "pair_ground": "the number stands as a word in Member 1 and as a figure in Member 2, all else the same.",
                    "label": "near verbatim pairs / holds / rounds number form",
                },
                {
                    "id": "NV-22",
                    "member_1": "Each shape is reported with its own rate.",
                    "member_2": "Each shape is reported with its own rate value.",
                    "pair_ground": "one word added, value at the end, all else the same.",
                    "label": "near verbatim pairs / holds / own rate wording",
                },
                {
                    "id": "NV-23",
                    "member_1": "The stage record carries the naming evidence.",
                    "member_2": "The stage record alone carries the naming evidence.",
                    "pair_ground": "one word added, alone after record, all else the same.",
                    "label": "near verbatim pairs / holds / naming evidence wording",
                },
                {
                    "id": "NV-24",
                    "member_1": "Synthetic examples stand in for real material.",
                    "member_2": "Synthetic examples stand in place of real material.",
                    "pair_ground": "a short phrase differs, in for against in place of, all else the same.",
                    "label": "near verbatim pairs / holds / synthetic examples wording",
                },
                {
                    "id": "NV-25",
                    "member_1": "A wide table fires often on configuration material.",
                    "member_2": "A wide table fires often on configuration heavy material.",
                    "pair_ground": "one word added, heavy after configuration, all else the same.",
                    "label": "near verbatim pairs / holds / wide table wording",
                },
                {
                    "id": "NV-26",
                    "member_1": "The module returns the specification only.",
                    "member_2": "The module returns only the specification.",
                    "pair_ground": "word order only differs, only moves before specification, all words the same.",
                    "label": "near verbatim pairs / holds / returns only order",
                },
                {
                    "id": "NV-27",
                    "member_1": "Labels on specification pairs say the relation holds.",
                    "member_2": "Labels on specification pairs say the pair relation holds.",
                    "pair_ground": "one word added, pair before relation, all else the same.",
                    "label": "near verbatim pairs / holds / labels say holds",
                },
                {
                    "id": "NV-28",
                    "member_1": "Worked cases stand beside every rule.",
                    "member_2": "Worked cases stand beside every single rule.",
                    "pair_ground": "one word added, single before rule, all else the same.",
                    "label": "near verbatim pairs / holds / worked cases wording",
                },
                {
                    "id": "NV-29",
                    "member_1": "Rewording a sentence defeats exact text matching.",
                    "member_2": "Rewording a sentence defeats an exact text matching.",
                    "pair_ground": "one word added, an before exact, all else the same.",
                    "label": "near verbatim pairs / holds / rewording matching wording",
                },
                {
                    "id": "NV-30",
                    "member_1": "Authored content is recorded as authored.",
                    "member_2": "Authored content is recorded as authored and guessed.",
                    "pair_ground": "Member 2 adds the short phrase and guessed, in the form every record of this part uses, all else the same.",
                    "label": "near verbatim pairs / holds / authored recording wording",
                },
            ),
        },
        "evidence": "specification commitment",
    },
    "labelling": {
        "labeller": "the operator",
        "labelling_act": "operator corpus labelling at construction",
        "labelling_act_statement": (
            "the single act, performed by the operator while "
            "the corpus is being constructed, in which each "
            "labelled pair and each labelled secret bearing "
            "shape receives its label, so that the corpus "
            "carries its labels from construction and not "
            "from any later pass"
        ),
        "labelling_protocol": (
            "the operator labelling protocol, one pass, "
            "kind by kind"
        ),
        "labelling_protocol_statement": (
            "the operator works through the corpus material "
            "in one pass, kind by kind and shape by shape, "
            "states each item kind or shape in the terms of "
            "this specification, applies the label form this "
            "specification states for that part, and records "
            "any item the operator cannot label in that pass "
            "as unlabelled rather than guessing a label for "
            "it, so the labels in the corpus are exactly the "
            "labels of that one pass"
        ),
    },
}

# The T03 namings block, in this seat's authored reading of
# where the specification's naming lives in the module: the
# namings stand as data inside the stated structure, under
# its "labelling" key, and this constant names that same
# stated mapping for the record. The tests read no T03 name
# from the module, and no suite result stands as evidence
# for row T03: the stage record quotation of these namings
# remains the evidence the register judges, in the scope
# act's section 6 form. The labeller value stands grounded;
# the act and protocol names and their statements stand
# authored and guessed.
_T03_NAMINGS_V1 = _CORPUS_SPECIFICATION_V1["labelling"]


def corpus_specification():
    """Return the corpus specification.

    The return is a mapping with four top level keys.
    "hard_negatives" is the pinned key: a mapping keyed by
    exactly the three shapes, in the grounded order, each
    value an entry mapping with exactly the keys "label",
    "negative_cases", and "decoded_candidates", the label
    standing as the pinned string, the cases and candidates
    standing as fresh lists of fresh mappings in the forms
    the header of this section states. The other three keys
    stand unpinned by any test, flagged as such here and in
    this seat's paper: "rates", a mapping keyed by shape,
    each value carrying "rate", "rate_kind", and
    "rate_denominator", holding the authored per shape
    rates for roster 911's rate_report to read by name at
    call time; "pair_part", a mapping carrying "kinds" as
    a fresh list, "commitments" and "labelled_pairs" as
    fresh mappings of fresh values, and "evidence", holding
    the pair data for roster 911's pair_part to read by
    name at call time; and "labelling", a fresh copy of the
    T03 namings mapping the header of this section states.
    A fresh structure is built on each call, containers and
    entry, case, candidate, commitment, and pair mappings
    alike, so a caller cannot mutate the stated
    specification through a returned value.
    """
    stated = _CORPUS_SPECIFICATION_V1
    pair_part = stated["pair_part"]
    return {
        "hard_negatives": {
            entry["shape"]: {
                "label": entry["label"],
                "negative_cases": [
                    {
                        "id": case["id"],
                        "statement": case["statement"],
                        "values": list(case["values"]),
                        "legitimate_because": case["legitimate_because"],
                        "note": case["note"],
                    }
                    for case in entry["negative_cases"]
                ],
                "decoded_candidates": [
                    {
                        "id": candidate["id"],
                        "decoding_round": candidate["decoding_round"],
                        "forms": list(candidate["forms"]),
                        "encoded_material": candidate["encoded_material"],
                        "intermediates": list(candidate["intermediates"]),
                        "decoded_form": candidate["decoded_form"],
                        "chain": list(candidate["chain"]),
                        "statement": candidate["statement"],
                    }
                    for candidate in entry["decoded_candidates"]
                ],
            }
            for entry in stated["hard_negatives"]
        },
        "rates": {
            entry["shape"]: {
                "rate": entry["rate"],
                "rate_kind": entry["rate_kind"],
                "rate_denominator": entry["rate_denominator"],
            }
            for entry in stated["hard_negatives"]
        },
        "pair_part": {
            "kinds": list(pair_part["kinds"]),
            "commitments": {
                kind: dict(commitment)
                for kind, commitment in pair_part["commitments"].items()
            },
            "labelled_pairs": {
                kind: [dict(pair) for pair in pairs]
                for kind, pairs in pair_part["labelled_pairs"].items()
            },
            "evidence": pair_part["evidence"],
        },
        "labelling": dict(stated["labelling"]),
    }


# Section: failure and boundary, roster 911.
# Functions: rate_report, pair_part.
# Insertion point for the whole section: in
# system/ontoloop/corpus_spec.py, in the roster 911 failure
# and boundary section, after roster 910's data and
# specification section and before roster 912's guard foot,
# in the composition order the scope section 8 states.
# Cross section calls, stated for the assembly check:
# both functions read the stated specification data through
# the module globals at call time, and through no other path.
# The primary path calls corpus_specification, which stands
# in roster 910's section, with no argument, exactly as the
# tests call it. The companion path reads a module level
# specification data mapping that roster 910's section may
# present instead, under the global name _SPECIFICATION_DATA
# or SPECIFICATION_DATA. Which path a composed module uses
# depends only on which of those globals roster 910's
# section presents, and the assembly check is charged to
# confirm the presented path against roster 910's paper.
# No rate value, no pair, no pair label, and no pair member
# is copied into this section: every rate and every pair
# returned here is read from that data at call time. The
# only values this section itself states are the boundary
# forms it owns under the scope section 8 charge for this
# seat: the commitment form and count in pair_part, and the
# evidence string in its exact pinned form. No value in
# this section carries a scanner shaped token form, so the
# representation discipline at entry 58 is not engaged by
# any literal in this fragment: the pair content and the
# case and candidate values that may carry that form stay
# in roster 910's data, and this section copies none of it.


def _specification_data():
    """Return the stated specification data, read at call time.

    The data is a single mapping obtained in this order.
    First, if the module globals carry a callable named
    corpus_specification, it is called with no argument and
    its return is used where it carries the part the caller
    needs. Second, a module level mapping under the global
    name _SPECIFICATION_DATA or SPECIFICATION_DATA stands as
    the companion source, used on its own where the first
    path is absent, and used to fill a part the first path
    does not carry where both stand present. No result is
    cached: every call to rate_report or pair_part reads
    the globals again, so a specification stated after this
    section is defined is the specification these functions
    report on.
    """
    merged = {}
    fallback = None
    for fallback_name in ("_SPECIFICATION_DATA", "SPECIFICATION_DATA"):
        candidate = globals().get(fallback_name)
        if isinstance(candidate, dict):
            fallback = candidate
            break
    if fallback is not None:
        merged.update(fallback)
    specification_callable = globals().get("corpus_specification")
    if callable(specification_callable):
        primary = specification_callable()
        if isinstance(primary, dict):
            merged.update(primary)
    return merged


def _rate_value(data, shape):
    """Read the authored rate for one shape from the data.

    Locations are tried in this stated order, all inside the
    one specification mapping _specification_data returns.
    One, a rates mapping keyed by shape, whose value is the
    rate itself or a mapping carrying it under the key rate.
    Two, a rate_report mapping keyed by shape in that same
    value form. Three, the shape entry of the hard_negatives
    mapping, carrying the rate under the key rate. A shape
    with no rate in any location raises KeyError: this
    section states no rate of its own, and an unstated rate
    is a specification gap, not a value to invent.
    """
    for container_name in ("rates", "rate_report", "per_shape_rates"):
        container = data.get(container_name)
        if isinstance(container, dict) and shape in container:
            value = container[shape]
            if isinstance(value, dict):
                return value["rate"]
            return value
    hard_negatives = data.get("hard_negatives")
    if isinstance(hard_negatives, dict) and shape in hard_negatives:
        entry = hard_negatives[shape]
        if isinstance(entry, dict) and "rate" in entry:
            return entry["rate"]
    raise KeyError(shape)


def _shape_keys(data):
    """Return the shape keys the data states, in stated order.

    The key order is the order of the first of these mappings
    the data carries: a rates mapping, a rate_report mapping,
    or the hard_negatives mapping. The two names the rate
    report bars, aggregate and total, are never returned as
    shapes, whatever a data mapping carries under them: the
    aggregate bar is this section's charge, and it is held
    here at the point the shapes are read, not only at the
    point the report is built.
    """
    for container_name in ("rates", "rate_report", "hard_negatives"):
        container = data.get(container_name)
        if isinstance(container, dict) and container:
            return [
                shape
                for shape in container.keys()
                if shape not in ("aggregate", "total")
            ]
    return []


def _labelled_pairs_by_kind(data):
    """Return the labelled pairs mapping the data states.

    Locations are tried in this stated order, all inside the
    one specification mapping _specification_data returns.
    One, a pair_part mapping carrying labelled_pairs. Two, a
    pairs mapping carrying labelled_pairs, or itself keyed
    by kind where its values are pair collections. Three,
    the specification mapping itself carrying labelled_pairs.
    A specification with no labelled pairs in any location
    raises KeyError: this section states no pair of its own.
    """
    pair_part_value = data.get("pair_part")
    if isinstance(pair_part_value, dict):
        labelled = pair_part_value.get("labelled_pairs")
        if isinstance(labelled, dict):
            return labelled
    pairs_value = data.get("pairs")
    if isinstance(pairs_value, dict):
        labelled = pairs_value.get("labelled_pairs")
        if isinstance(labelled, dict):
            return labelled
        if pairs_value:
            return pairs_value
    labelled = data.get("labelled_pairs")
    if isinstance(labelled, dict):
        return labelled
    raise KeyError("labelled_pairs")


def _clean_pair(pair):
    """Return one pair with no production count key in it.

    A mapping pair is copied key by key, omitting any key
    named production_count, so the commitment boundary holds
    at every level this section presents, even if a stated
    pair were to carry such a key into this section. Every
    other key and value, the label among them, stands
    exactly as the specification data states it. A pair
    that is not a mapping stands returned as stated.
    """
    if not isinstance(pair, dict):
        return pair
    return {
        key: value
        for key, value in pair.items()
        if key != "production_count"
    }


# Insertion point: roster 911 failure section, first new
# definition in this section in the assembled file.
def rate_report():
    """Return the per shape rate report, with no aggregate.

    Returns a fresh mapping keyed by exactly the shapes the
    specification data states, read through the module
    globals at call time by _specification_data and
    _shape_keys. Each value is a fresh mapping with exactly
    the one key rate, whose value is the authored per shape
    rate the specification data carries for that shape, read
    by _rate_value and stated in no other form here: the
    authored rates are the fire rate kind, with their
    denominators stated in the authored specification part
    appended to design/steps/step-14-spec-corpus-shape.md,
    and they stand as authored specification figures, never
    as measured figures. No aggregate key and no total key
    stands anywhere in the returned structure, at any level:
    the shape keys exclude those names by construction in
    _shape_keys, and each per shape value is built here with
    the one key rate and nothing else.
    """
    data = _specification_data()
    report = {}
    for shape in _shape_keys(data):
        report[shape] = {"rate": _rate_value(data, shape)}
    return report


# Insertion point: roster 911 failure section, second new
# definition in this section in the assembled file.
def pair_part():
    """Return the pair part in commitment form only.

    Returns a fresh mapping with exactly the four keys kinds,
    commitments, labelled_pairs, and evidence. kinds is a
    fresh list of the kind keys the specification data
    states for its labelled pairs, in the order that data
    states them, read through the module globals at call
    time by _specification_data and _labelled_pairs_by_kind.
    commitments is a fresh mapping keyed by kind, each value
    a fresh mapping with the form minimum and the count 30,
    stated here as the commitment this section owns: the
    count is a completeness condition on the specification
    contents, and it certifies nothing about production or
    about label quality. labelled_pairs is a fresh mapping
    keyed by kind, each value a fresh list holding every
    pair the specification data states for that kind, at
    least the commitment count of them where the data meets
    its commitment, each pair cleaned by _clean_pair and
    carrying the label the data states for it. evidence is
    the exact string specification commitment. No key named
    production_count stands anywhere in the returned
    structure, at the top level or inside any pair, and no
    production count, figure, or result of any kind stands
    in it: the production report form stands in POPULATED,
    beside the commitment and never merged into it, and
    this return presents the commitment side only.
    """
    data = _specification_data()
    labelled_by_kind = _labelled_pairs_by_kind(data)
    kinds = list(labelled_by_kind.keys())
    commitments = {}
    labelled_pairs = {}
    for kind in kinds:
        commitments[kind] = {"form": "minimum", "count": 30}
        labelled_pairs[kind] = [
            _clean_pair(pair) for pair in labelled_by_kind[kind]
        ]
    return {
        "kinds": kinds,
        "commitments": commitments,
        "labelled_pairs": labelled_pairs,
        "evidence": "specification commitment",
    }


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
