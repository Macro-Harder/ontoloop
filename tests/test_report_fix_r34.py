"""Fix round 34, Region 1: report seal claim scan pins.

Rulings 2021 to 2029 of the Round 34 triage. Each class
pins the probed forms of its ruling beside the standing
forms that must keep deciding as they decide. Statements
stand built from the probed word and phrase sets of the
raising papers, the Report and golden span paper findings
S15-R34-REPG-1 to 8 and the Confinement paper findings
S15-R34-CONF-1 to 12 in their absorbed limbs, on the
templates those papers state. A form probed in both
raising papers on the one template stands counted once,
in the form of the triage merges. Divided forms standing
at pole on the governing base in one construction stand
pinned in the controls of their class in that construction.
Ruling 2023 stands as the SURVIVES cure of ruling 1890:
its class pins the abjuration instrument forms, by the
abjuration of and under the abjuration of, at both poles.
"""

import unittest

from tests import harness


def _scan(mod, statement):
    return mod._seal_claim_scan(statement)


def _travel(mod, statement):
    result = mod.fixed_text_travel_lint(
        assembly="export", content=statement)
    return result["passed"]


_GOVERNED_CLAIM = ("The seal guarantees protection conditional on "
                   "the deployment confinement fact")

class SealClaimScanInabilityFixR34Tests(unittest.TestCase):
    """Ruling 2021: inability limb, followers and windows."""

    MODAL_REPG_WORDS = dict.fromkeys((
        "zinced", "japanned", "serrated",
        "dimpled", "stippled", "bored",
        "furrowed", "louvred", "beveled",
        "braised", "simmered",
    ))

    MODAL_CONF_WORDS = dict.fromkeys((
        "asphalted", "battened", "beveled",
        "blasted", "bored", "bowed",
        "bridged", "caned", "carded",
        "carpeted", "cased", "chalked",
        "channeled", "churned", "clawed",
        "cleaved", "clogged", "clothed",
        "combed", "corrugated", "cottoned",
        "crenellated", "creped", "creviced",
        "crinkled", "cropped", "crosshatched",
        "crowned", "crusted", "cubed",
        "cupped", "curbed", "curled",
        "curved", "cycled", "dabbed",
        "dagged", "damasked", "dammed",
        "damped", "darned", "darted",
        "dashed", "daubed", "deadened",
        "debarked", "debussed", "defoamed",
        "deglazed", "degreased", "degummed",
        "dehorned", "dehulled", "deiced",
        "delaminated", "delinted", "deloused",
        "demisted", "buffered", "cabled",
        "carted", "cloaked", "clouded",
        "coded",
    ))

    ASSERTED_WORDS = dict.fromkeys((
        "zinced", "japanned", "serrated",
        "dimpled", "stippled", "bored",
        "furrowed", "louvred", "beveled",
        "braised", "simmered", "asphalted",
        "battened", "blasted", "bowed",
        "bridged", "caned", "carded",
        "carpeted", "cased", "chalked",
        "channeled", "churned", "clawed",
        "cleaved", "clogged", "clothed",
        "combed", "corrugated", "cottoned",
        "crenellated", "creped", "creviced",
        "crinkled", "cropped", "crosshatched",
        "crowned", "crusted", "cubed",
        "cupped", "curbed", "curled",
        "curved", "cycled", "dabbed",
        "dagged", "damasked", "dammed",
        "damped", "darned", "darted",
        "dashed", "daubed", "deadened",
        "debarked", "debussed", "defoamed",
        "deglazed", "degreased", "degummed",
        "dehorned", "dehulled", "deiced",
        "delaminated", "delinted", "deloused",
        "demisted", "debarred",
    ))

    WINDOW_WORDS = dict.fromkeys((
        "vexedly", "cholerically", "splenetically",
        "pricklily", "crabbedly", "crustily",
        "gruffly", "derisively", "superciliously",
        "haughtily", "pompously", "pretentiously",
        "imperiously", "dogmatically", "ably",
        "absorbingly", "acceptably", "achingly",
        "actively", "acutely", "admiringly",
        "adorably", "adventurously", "adversely",
        "advisedly", "affectionately", "affirmatively",
        "agilely", "agonizingly", "agreeably",
        "aimlessly", "deftly", "delicately",
        "delightfully", "deplorably", "dexterously",
        "direly", "discreetly", "disgustedly",
        "docilely", "doubtfully", "eerily",
        "elegantly", "eloquently", "enchantingly",
        "energetically", "engagingly", "enormously",
        "erratically", "evasively", "evenly",
        "excitedly", "exhaustively", "expectantly",
        "expertly", "expressively", "exquisitely",
        "extravagantly", "exuberantly", "exultantly",
        "famously", "fancifully", "fascinatingly",
        "fashionably", "fatally", "faultlessly",
        "feelingly", "fervently", "festively",
        "fierily", "filthily", "fittingly",
        "flamboyantly", "flatteringly", "flawlessly",
        "flexibly", "flippantly", "fluently",
        "fluidly", "fondly", "formerly",
        "fortunately", "foully", "freakishly",
        "freshly", "frightfully", "frigidly",
        "friskily", "frivolously", "frontally",
        "frothily", "frownily", "fruitfully",
        "fumblingly", "funnily", "fussily",
        "gainfully", "gamely", "gapingly",
        "garishly", "garrulously", "gaudily",
        "gauntly", "gawkily", "gayly",
        "generously", "geometrically", "giddily",
        "gingerly", "girlishly", "givenly",
        "glamourously", "glaringly", "glibly",
        "glimmeringly", "gloatingly", "glossily",
        "glowingly", "gluttonously", "gnashingly",
        "goldenly", "gorgeously", "governably",
        "gracelessly", "grainily", "grandiosely",
        "grandly", "gravily", "grazingly",
        "greasily", "greatly", "greenly",
        "gregariously", "grievingly", "grimacingly",
        "grinningly", "gripingly", "grittily",
        "grizzlily", "groaningly", "groggily",
        "grossly", "grotesquely", "groundlessly",
        "growlingly", "grubbily", "gruesomely",
        "grumblingly", "gruntingly", "guessingly",
        "guilefully", "guiltlessly", "gullibly",
        "gushingly", "gustily", "gutsily",
        "habitually", "haggardly", "haltingly",
        "hamperingly", "handily", "handsomely",
        "haplessly", "harrowingly", "hatefully",
        "hauntingly", "hazardously", "hazily",
        "headily", "headstrongly", "healthily",
        "healthfully", "heavilily", "hecklingly",
        "heedfully", "heftily", "heighteningly",
        "heinously", "helpfully", "henpeckedly",
        "heraldically", "herbally", "hermetically",
        "hesitatingly", "hibernally", "hideously",
        "hierarchically", "highhandedly", "highly",
        "hilariously", "hinderedly", "hinderingly",
        "hintingly", "hissingly", "hoardedly",
        "hoarsely", "hoaxingly", "hobblingly",
        "hoistly", "hollowly",
    ))

    MODAL = tuple(
        "Records cannot be %s by outsiders." % word
        for word in MODAL_REPG_WORDS) + tuple(
        "Records cannot be %s after writing." % word
        for word in MODAL_CONF_WORDS)

    ASSERTED = tuple(
        "Records are %s by outsiders." % word
        for word in ASSERTED_WORDS)

    WINDOWS = tuple(
        "Records cannot %s be altered after writing." % word
        for word in WINDOW_WORDS)

    def test_modal_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.MODAL:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_followers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_windows_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WINDOWS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(
            _scan(mod, "Records cannot be electroplated by outsiders."))
        self.assertFalse(
            _scan(mod, "Records are electroplated by outsiders."))
        self.assertFalse(_scan(
            mod, "Records cannot truculently be altered "
            "after writing."))
        for word in ("buffered", "cabled", "carted", "cloaked",
                     "clouded", "coded"):
            self.assertFalse(_scan(
                mod, "Records are %s by outsiders." % word))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanGoverningFixR34Tests(unittest.TestCase):
    """Ruling 2022: governing condition limb."""

    PHRASINGS = dict.fromkeys((
        "by the gavel of", "under the gavel of",
        "by the hammer of", "under the hammer of",
        "by the truncheon of", "under the truncheon of",
        "by the rod of", "under the switch of",
        "under the cane of", "by the cane of",
        "under the birch of", "under the ferule of",
        "under the keys of", "by the keys of",
        "under the lock of", "under the chain of",
        "by the chain of", "under the seal ring of",
        "by the privy seal of", "under the privy seal of",
        "by the great seal of", "under the great seal of",
        "by the sign manual of", "by the abnegation of",
        "by the abrogation of", "by the acquittal of",
        "by the adjournment of", "by the adjustment of",
        "by the admission of", "by the advancement of",
        "by the allocation of", "by the allotment of",
        "by the alteration of", "by the amalgamation of",
        "by the amnesty of", "by the amplification of",
        "by the annulment of", "by the appeal of",
        "by the application of", "by the apportionment of",
        "by the appraisal of", "by the audit of",
        "by the augmentation of", "by the benediction of",
        "by the bequest of", "by the bestowal of",
        "by the bylaw of", "by the certification of",
        "by the challenge of", "by the clarification of",
        "by the classification of", "by the clearance of",
        "by the clemency of", "by the closure of",
        "by the codicil of", "by the collaboration of",
        "by the collateral of", "by the collection of",
        "by the combination of", "by the commencement of",
        "by the commendation of", "by the commitment of",
        "by the committee of", "by the communication of",
        "by the comparison of", "by the compensation of",
        "by the compilation of", "by the complaint of",
        "by the completion of", "by the compliance of",
        "by the composition of", "by the compromise of",
        "by the compulsion of", "by the computation of",
        "by the conciliation of", "by the conclusion of",
        "by the condition of", "by the confederation of",
        "by the conference of", "by the confession of",
        "by the confidence of", "by the configuration of",
        "by the confirmation of", "by the confiscation of",
        "by the conformance of", "by the conformity of",
        "by the conservation of", "by the consideration of",
        "by the consignment of", "by the consolidation of",
        "by the constraint of", "by the construction of",
        "by the consultation of", "by the consummation of",
        "by the contention of", "by the contest of",
        "by the contingency of", "by the continuation of",
        "by the contract of", "by the contribution of",
        "by the conveyance of", "by the conviction of",
        "by the cooperation of", "by the coordination of",
        "by the coronation of", "by the correction of",
        "by the correspondence of", "by the corroboration of",
        "by the council of", "by the counsel of",
        "by the coverage of", "by the creation of",
        "by the credit of", "by the criterion of",
        "by the custody of", "by the deadline of",
        "by the debate of", "by the debt of",
        "by the dedication of", "by the deduction of",
        "by the deed of", "by the default of",
        "by the defence of", "by the defense of",
        "by the deferment of", "by the definition of",
        "by the delay of", "by the delegation of",
        "by the deletion of", "by the deliberation of",
        "by the delivery of", "by the demonstration of",
        "by the denial of", "by the departure of",
        "by the dependence of", "by the deployment of",
        "by the deposit of", "by the deposition of",
        "by the depreciation of", "by the deprivation of",
        "by the destruction of", "by the detachment of",
        "by the detection of", "by the detention of",
        "by the development of", "by the deviation of",
        "by the devotion of", "by the diagnosis of",
        "by the dialogue of", "by the dictation of",
        "by the diligence of", "by the dimension of",
        "by the diminution of", "by the diploma of",
        "by the disability of", "by the disagreement of",
        "by the disappearance of", "by the disapproval of",
        "by the disarmament of", "by the disbelief of",
        "by the discernment of", "by the discharge of",
        "by the disclosure of", "by the discount of",
        "by the discourse of", "by the discovery of",
        "by the discretion of", "by the discrimination of",
        "by the discussion of", "by the disguise of",
        "by the dismissal of", "by the disobedience of",
        "by the dispatch of", "by the dispersal of",
        "by the displacement of", "by the display of",
        "by the disposal of", "by the dispute of",
        "by the disqualification of", "by the disregard of",
        "by the disruption of", "by the dissatisfaction of",
        "by the dissemination of", "by the dissent of",
        "by the dissolution of", "by the distinction of",
        "by the distortion of", "by the distraction of",
        "by the distribution of", "by the distrust of",
        "by the divergence of", "by the diversification of",
        "by the diversion of", "by the diversity of",
        "by the dividend of", "by the division of",
        "by the divorce of", "by the document of",
        "by the documentation of", "by the domain of",
        "by the donation of", "by the draft of",
        "by the duty of", "by the indictment of",
        "by the judgement of", "by the legislation of",
        "by the promulgation of", "by the ratification of",
        "by the rescission of", "by the revocation of",
        "by the specification of", "under the abnegation of",
        "under the abrogation of", "under the acquittal of",
        "under the adjournment of", "under the adjustment of",
        "under the admission of", "under the advancement of",
        "under the allocation of", "under the allotment of",
        "under the alteration of", "under the amalgamation of",
        "under the amnesty of", "under the amplification of",
        "under the annulment of", "under the appeal of",
        "under the application of", "under the apportionment of",
        "under the appraisal of", "under the audit of",
        "under the augmentation of", "under the benediction of",
        "under the bequest of", "under the bestowal of",
        "under the bylaw of", "under the certification of",
        "under the challenge of", "under the clarification of",
        "under the classification of", "under the clearance of",
        "under the clemency of", "under the closure of",
        "under the codicil of", "under the collaboration of",
        "under the collateral of", "under the collection of",
        "under the combination of", "under the commencement of",
        "under the commendation of", "under the commitment of",
        "under the committee of", "under the communication of",
        "under the comparison of", "under the compensation of",
        "under the compilation of", "under the complaint of",
        "under the completion of", "under the compliance of",
        "under the composition of", "under the compromise of",
        "under the compulsion of", "under the computation of",
        "under the conciliation of", "under the conclusion of",
        "under the condition of", "under the confederation of",
        "under the conference of", "under the confession of",
        "under the confidence of", "under the configuration of",
        "under the confirmation of", "under the confiscation of",
        "under the conformance of", "under the conformity of",
        "under the conservation of", "under the consideration of",
        "under the consignment of", "under the consolidation of",
        "under the constraint of", "under the construction of",
        "under the consultation of", "under the consummation of",
        "under the contention of", "under the contest of",
        "under the contingency of", "under the continuation of",
        "under the contract of", "under the contribution of",
        "under the conveyance of", "under the conviction of",
        "under the cooperation of", "under the coordination of",
        "under the coronation of", "under the correction of",
        "under the correspondence of", "under the corroboration of",
        "under the council of", "under the counsel of",
        "under the coverage of", "under the creation of",
        "under the credit of", "under the criterion of",
        "under the deadline of", "under the debate of",
        "under the debt of", "under the dedication of",
        "under the deduction of", "under the deed of",
        "under the default of", "under the defence of",
        "under the defense of", "under the deferment of",
        "under the definition of", "under the delay of",
        "under the delegation of", "under the deletion of",
        "under the deliberation of", "under the delivery of",
        "under the demonstration of", "under the denial of",
        "under the departure of", "under the dependence of",
        "under the deployment of", "under the deposit of",
        "under the deposition of", "under the depreciation of",
        "under the deprivation of", "under the destruction of",
        "under the detachment of", "under the detection of",
        "under the detention of", "under the development of",
        "under the deviation of", "under the devotion of",
        "under the diagnosis of", "under the dialogue of",
        "under the dictation of", "under the diligence of",
        "under the dimension of", "under the diminution of",
        "under the diploma of", "under the disability of",
        "under the disagreement of", "under the disappearance of",
        "under the disapproval of", "under the disarmament of",
        "under the disbelief of", "under the discernment of",
        "under the discharge of", "under the disclosure of",
        "under the discount of", "under the discourse of",
        "under the discovery of", "under the discretion of",
        "under the discrimination of", "under the discussion of",
        "under the disguise of", "under the dismissal of",
        "under the disobedience of", "under the dispatch of",
        "under the dispersal of", "under the displacement of",
        "under the display of", "under the disposal of",
        "under the dispute of", "under the disqualification of",
        "under the disregard of", "under the disruption of",
        "under the dissatisfaction of", "under the dissemination of",
        "under the dissent of", "under the dissolution of",
        "under the distinction of", "under the distortion of",
        "under the distraction of", "under the distribution of",
        "under the distrust of", "under the divergence of",
        "under the diversification of", "under the diversion of",
        "under the diversity of", "under the dividend of",
        "under the division of", "under the divorce of",
        "under the document of", "under the documentation of",
        "under the domain of", "under the donation of",
        "under the draft of", "under the duty of",
        "under the indictment of", "under the judgement of",
        "under the legislation of", "under the promulgation of",
        "under the ratification of", "under the rescission of",
        "under the revocation of", "under the specification of",
        "under the designation of", "under the blessing of",
        "under the concession of", "under the concurrence of",
        "under the call of", "under the desire of",
        "under the franchise of",
    ))

    TRAILING = dict.fromkeys((
        "in whatsoever province the deployment confinement fact holds",
        "through whatsoever province the deployment confinement fact holds",
        "in whatsoever district the deployment confinement fact holds",
        "through whatsoever district the deployment confinement fact holds",
        "in whatsoever township the deployment confinement fact holds",
        "through whatsoever township the deployment confinement fact holds",
        "in whatsoever village the deployment confinement fact holds",
        "through whatsoever village the deployment confinement fact holds",
        "in whatsoever hamlet the deployment confinement fact holds",
        "through whatsoever hamlet the deployment confinement fact holds",
        "in whatsoever city the deployment confinement fact holds",
        "through whatsoever city the deployment confinement fact holds",
        "in whatsoever town the deployment confinement fact holds",
        "through whatsoever town the deployment confinement fact holds",
        "in whatsoever kingdom the deployment confinement fact holds",
        "through whatsoever kingdom the deployment confinement fact holds",
        "in whatsoever dominion the deployment confinement fact holds",
        "through whatsoever dominion the deployment confinement fact holds",
        "in whatsoever territory the deployment confinement fact holds",
        "through whatsoever territory the deployment confinement fact holds",
        "in whatsoever region the deployment confinement fact holds",
        "through whatsoever region the deployment confinement fact holds",
        "in whatsoever zone the deployment confinement fact holds",
        "through whatsoever zone the deployment confinement fact holds",
        "in whatsoever ward the deployment confinement fact holds",
        "through whatsoever ward the deployment confinement fact holds",
        "in whatsoever diocese the deployment confinement fact holds",
        "through whatsoever diocese the deployment confinement fact holds",
        "in whatsoever hemisphere the deployment confinement fact holds",
        "through whatsoever hemisphere the deployment confinement fact holds",
        "in whatsoever continent the deployment confinement fact holds",
        "through whatsoever continent the deployment confinement fact holds",
        "in whatsoever country the deployment confinement fact holds",
        "through whatsoever country the deployment confinement fact holds",
        "in whatsoever nation the deployment confinement fact holds",
        "through whatsoever nation the deployment confinement fact holds",
        "in whatsoever state the deployment confinement fact holds",
        "through whatsoever state the deployment confinement fact holds",
        "in whatsoever commonwealth the deployment confinement fact holds",
        "through whatsoever commonwealth the deployment confinement fact holds",
        "in whatsoever republic the deployment confinement fact holds",
        "through whatsoever republic the deployment confinement fact holds",
        "in whatsoever principality the deployment confinement fact holds",
        "through whatsoever principality the deployment confinement fact holds",
        "in whatsoever duchy the deployment confinement fact holds",
        "through whatsoever duchy the deployment confinement fact holds",
        "in whatsoever climate the deployment confinement fact holds",
        "through whatsoever climate the deployment confinement fact holds",
        "in whatsoever latitude the deployment confinement fact holds",
        "through whatsoever latitude the deployment confinement fact holds",
        "for whatsoever period the deployment confinement fact holds",
        "for whatsoever interval the deployment confinement fact holds",
        "for whatsoever age the deployment confinement fact holds",
        "for whatsoever stretch the deployment confinement fact holds",
    ))

    TRAILING_CONF = (
        "wherever and howsoever",
        "whithersoever and howsoever",
        "wherever and wherein",
    )

    GOVERNED = tuple(
        "The seal guarantees protection %s "
        "the deployment confinement fact." % phrase
        for phrase in PHRASINGS) + tuple(
        "The seal guarantees protection %s." % form
        for form in TRAILING) + tuple(
        "The seal guarantees protection %s "
        "the deployment confinement fact holds." % form
        for form in TRAILING_CONF)

    WEATHER = tuple(
        "The seal guarantees protection %s the weather." % phrase
        for phrase in PHRASINGS) + tuple(
        "The seal guarantees protection %s." % form.replace(
            "the deployment confinement fact holds", "the weather holds")
        for form in TRAILING) + tuple(
        "The seal guarantees protection %s the weather holds." % form
        for form in TRAILING_CONF)

    def test_phrasings_and_trailing_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_weather_conditions_still_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the reign of "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection in whatsoever "
            "manner the deployment confinement fact holds."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the rod of "
            "the deployment confinement fact."))
        self.assertTrue(_scan(
            mod, "The seal guarantees protection under the sign "
            "manual of the deployment confinement fact."))
        self.assertFalse(_scan(
            mod, "The seal guarantees protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanAbjurationFixR34Tests(unittest.TestCase):
    """Ruling 2023: the SURVIVES cure of ruling 1890.

    The abjuration instrument forms stand added to the
    governing condition phrase list and pinned here, in
    the pin class of ruling 1890 in its Round 34 form,
    at both poles.
    """

    GOVERNED = (
        "The seal guarantees protection by the abjuration of "
        "the deployment confinement fact.",
        "The seal guarantees protection under the abjuration of "
        "the deployment confinement fact.",
    )

    WEATHER = (
        "The seal guarantees protection by the abjuration of "
        "the weather.",
        "The seal guarantees protection under the abjuration of "
        "the weather.",
    )

    def test_abjuration_forms_stand_governed(self):
        mod = harness.require("ontoloop.report")
        for statement in self.GOVERNED:
            self.assertTrue(_scan(mod, statement), statement)
            self.assertTrue(_travel(mod, statement), statement)

    def test_abjuration_weather_still_fails(self):
        mod = harness.require("ontoloop.report")
        for statement in self.WEATHER:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertTrue(_scan(
            mod, "The seal guarantees protection by the adjuration "
            "of the deployment confinement fact."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanCompoundFixR34Tests(unittest.TestCase):
    """Ruling 2024: prefixed compound limb."""

    PREFIXES = dict.fromkeys((
        "astato", "francio", "polono",
        "thoro", "urano", "plutono",
        "neptuno", "americo", "curio",
        "berkelio", "californio", "einsteinio",
        "fermio", "mendelevio", "nobelio",
        "lawrencio", "dubnio", "seaborgio",
        "bohrio", "hassio", "meitnerio",
        "darmstadto", "roentgenio", "copernicio",
        "nihonio", "flerovio", "moscovio",
        "livermorio", "tennessio", "oganesso",
        "bismuto", "antimonio", "acro",
        "ambi", "andro", "ante",
        "auxo", "axio", "batho",
        "blasto", "bucco", "carpo",
        "cerato", "cheiro", "chryso",
        "cirro", "clado", "clino",
        "coeno", "cole", "colla",
        "colo", "cordi", "corneo",
        "cortico", "cteno", "cubito",
        "cuneo", "cyclo", "cymo",
        "desmo", "deutero", "dichoto",
        "dictyo", "diplo", "disco",
        "dolicho", "ento", "ethmo",
        "eury", "fibro", "gymno",
        "gynae", "gynaeco", "halo",
        "haplo", "homeo", "hymeno",
        "ibero", "icon", "ideo",
        "idio", "ilio", "intro",
        "ischio", "italo", "jejuno",
        "jugo", "juxta", "kata",
        "katharo", "kino", "kion",
        "kiono", "koilo", "kolo",
        "kolpo", "konio", "koni",
        "kopro", "kosmo",
    ))

    FIRST_ELEMENTS = dict.fromkeys((
        "briarwood", "marblewood", "leopardwood",
        "padaukwood", "bubingawood", "ipewood",
        "cumaruwood", "afzelia", "agatis",
        "amapa", "amaranth", "andiroba",
        "baboen", "balata", "banaba",
        "bangkirai", "baromalli", "basralocus",
        "beanwood", "beefwood", "belian",
        "bintangor", "bongossi", "bulletwood",
        "canarium", "candlenut", "capirona",
        "carapa", "ceiba", "chechen",
        "chengal", "chinkapin", "courbaril",
        "cupay", "curupay", "dabema",
        "dahoma", "daniellia", "danta",
    ))

    PREFIX_FORMS = tuple(
        "Every record stands %sverified before use." % prefix
        for prefix in PREFIXES) + tuple(
        "Every record stands %schecked before use." % prefix
        for prefix in PREFIXES) + (
        "Every record stands coprochecked before use.",)

    ELEMENT_FORMS = tuple(
        "Every record stands %s-verified before use." % element
        for element in FIRST_ELEMENTS)

    def test_prefixes_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.PREFIX_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_elements_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ELEMENT_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "Every record stands amphiverified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands apricotwood-verified "
            "before use."))
        self.assertFalse(_scan(
            mod, "Every record stands coproverified before use."))
        self.assertFalse(_scan(
            mod, "Every record stands verified before use."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanLexiconFixR34Tests(unittest.TestCase):
    """Ruling 2025: concept roots, un and resistant wordings."""

    WORDINGS = dict.fromkeys((
        "uncrenellated", "unpartitioned", "unchambered",
        "uncorridored", "unvestibuled", "unporticoed",
        "unarcaded", "unpedimented", "uncorniced",
        "unfriezed", "undadoed", "unmoulded",
        "unmolded", "unparqueted", "unmosaiced",
        "unfrescoed", "unwhitewashed", "undistempered",
        "ashresistant", "vacuumresistant", "neutronresistant",
        "mineproof", "torpedoproof", "anvilproof",
        "augerproof", "awlproof", "bayonetproof",
        "billowproof", "blightproof", "blockproof",
        "blowproof", "boarproof", "boulderproof",
        "bowproof", "branchproof", "breezeproof",
        "brineproof", "bristleproof", "broomproof",
        "brushproof", "bubbleproof", "bushproof",
        "bustproof", "buttproof", "buzzproof",
        "cactusproof", "caimanproof", "anvilresistant",
        "augerresistant", "avalancheresistant", "awlresistant",
        "axeresistant", "bayonetresistant", "bearresistant",
        "beetleresistant", "billowresistant", "birdresistant",
        "biteresistant", "blockresistant", "blowresistant",
        "boarresistant", "borerresistant", "boulderresistant",
        "bowresistant", "branchresistant", "breezeresistant",
        "brineresistant", "bristleresistant", "broomresistant",
        "brushresistant", "bubbleresistant", "bulletresistant",
        "burstresistant", "bushresistant", "bustresistant",
        "buttresistant", "buzzresistant", "cactusresistant",
        "caimanresistant", "unbadged", "unbagged",
        "unballasted", "unbannered", "unbasted",
        "unbayoneted", "unbeaconed", "unbereted",
        "unbespectacled", "unbibbed", "unblazered",
        "unbloused", "unbraced", "unbracketed",
        "unbraided", "unbranded", "unbrocaded",
        "unbrooched", "unbuoyed", "uncabined",
        "uncabled", "uncanvassed", "uncasked",
        "uncassocked", "uncharmed", "uncharted",
        "unchastened", "uncheered", "unchequered",
        "unchewed", "unchilled", "unchinked",
        "unchinned", "unchirped", "unchiseled",
        "unchiselled", "unchivalrous", "unchlorinated",
        "unchocked", "unchoked", "unchoosable",
        "unchoosing", "unchopped", "unchorused",
        "unchristian", "unchromed", "unchronicled",
        "unchucked", "unchurned", "unchuted",
        "unciliated", "uncinctured", "uncindered",
    ))

    RECORDS = tuple(
        "The records are %s by outside writers." % word
        for word in WORDINGS)

    STORE = tuple(
        "The store is %s." % word
        for word in WORDINGS)

    def test_record_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.RECORDS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_store_wordings_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.STORE:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The records are unescorted by outside writers."))
        self.assertFalse(_scan(mod, "The store is unescorted."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanAssertedFixR34Tests(unittest.TestCase):
    """Ruling 2026: asserted form reading, journal verbs."""

    VERBS = dict.fromkeys((
        "smolders", "kindles", "ignites",
        "phosphoresces", "fluoresces", "luminesces",
        "incandesces", "thaws", "distils",
        "decants", "vaporizes", "atomizes",
        "mortifies", "gangrenes", "necroses",
        "atrophies", "hypertrophies", "ossifies",
        "vitrifies", "reduces", "corrodes",
        "rusts", "mildews", "blights",
        "shrivels", "wrinkles", "folds",
        "bends", "warps", "twists",
        "ablates", "absorbs", "adsorbs",
        "aerates", "anneals", "anodizes",
        "attenuates", "autoclaves", "bituminizes",
        "borates", "brominates", "calcines",
        "carburizes", "carboxylates", "chelates",
        "chromates", "coats", "cokes",
        "collimates", "comminutes", "compacts",
        "conglomerates", "conjugates", "converts",
        "copolymerizes", "crosslinks", "cures",
        "cyclizes", "decalcifies", "decarbonizes",
        "decarboxylates", "decontaminates", "deflocculates",
        "defoams", "degasses", "degreases",
        "dehumidifies", "dehydrogenates", "deionizes",
        "delaminates", "demagnetizes", "demineralizes",
        "demulsifies", "denitrifies", "deoxidizes",
        "depolymerizes", "deposits", "desorbs",
        "dewaxes", "dextrinizes", "diazotizes",
        "digests", "dilutes", "disaggregates",
        "disinfects", "disproportionates", "dissociates",
        "dopes", "dries", "effloresces",
        "elutes", "elutriates", "embrittles",
        "entrains", "epoxidizes", "equilibrates",
        "etches", "etherifies", "exfoliates",
        "extracts", "fertilizes", "fibrillates",
        "filters", "fissions", "fixes",
        "flocculates", "fluidizes", "fluoridates",
        "foliates", "forges", "formulates",
        "fumes", "fumigates", "functionalizes",
        "fuses", "galvanizes", "gasifies",
        "gels", "generates", "halogenates",
        "hardens", "hemolyzes", "heterolyzes",
        "homolyzes",
    ))

    FORMS = tuple(
        "The journal %s integrity for every reader." % verb
        for verb in VERBS)

    def test_journal_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, "The journal undulates integrity for every reader."))
        self.assertTrue(_scan(
            mod, "Integrity label for the journal schedule."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanMarkerFixR34Tests(unittest.TestCase):
    """Ruling 2027: unconditional marker reading."""

    APPENDED_MARKERS = dict.fromkeys((
        "when the cows come home", "when pigs fly",
        "while the world lasts", "till the stars burn out",
        "until the stars burn out", "until the final trumpet",
        "when the trumpet sounds", "while the grass grows",
        "until the rivers run dry", "unto the end of the world",
        "until the heavens fall", "until the sky falls",
        "while the earth remains", "as long as the earth remains",
        "as long as the rivers run", "as long as the tides turn",
        "as long as the winds blow", "as long as the rain falls",
        "as long as the snow falls", "as long as the trees grow",
        "till time stops", "until time stops",
        "as long as the earth shall last", "as long as the sun shall rise",
        "while time remains", "so long as the world lasts",
        "so long as time lasts", "so long as the sun rises",
        "through every age", "age after age",
        "until the sun dies", "till the final trumpet",
        "as long as the hills stand", "as long as the valleys stand",
        "as long as the forests stand", "as long as the deserts stand",
        "as long as the plains stand", "as long as the cliffs stand",
        "as long as the beaches stand", "as long as the islands stand",
        "as long as the continents stand", "as long as the world endures",
        "as long as the shores stand",
    ))

    COMMA_MARKERS = dict.fromkeys((
        "when the cows come home", "when pigs fly",
        "while the world lasts", "till the stars burn out",
        "until the stars burn out", "until the final trumpet",
        "when the trumpet sounds", "while the grass grows",
        "until the rivers run dry", "unto the end of the world",
        "until the heavens fall", "until the sky falls",
        "while the earth remains", "as long as the earth remains",
        "for evermore", "as long as the rivers run",
        "as long as the tides turn", "as long as the winds blow",
        "as long as the rain falls", "as long as the snow falls",
        "as long as the trees grow", "till time stops",
        "until time stops", "as long as the earth shall last",
        "as long as the sun shall rise", "while time remains",
        "so long as the world lasts", "so long as time lasts",
        "so long as the sun rises", "through every age",
        "age after age", "until the sun dies",
        "till the final trumpet", "as long as the hills stand",
        "as long as the valleys stand", "as long as the forests stand",
        "as long as the deserts stand", "as long as the plains stand",
        "as long as the cliffs stand", "as long as the beaches stand",
        "as long as the islands stand", "as long as the continents stand",
        "till the seas dry up", "till the rivers dry up",
    ))

    APPENDED = tuple(
        _GOVERNED_CLAIM + " %s." % marker
        for marker in APPENDED_MARKERS)

    COMMA = tuple(
        _GOVERNED_CLAIM + ", %s." % marker
        for marker in COMMA_MARKERS)

    def test_appended_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.APPENDED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_comma_clause_markers_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.COMMA:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + " right or wrong."))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + ", right or wrong."))
        self.assertFalse(_scan(
            mod, _GOVERNED_CLAIM + " for evermore."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanNegationFixR34Tests(unittest.TestCase):
    """Ruling 2028: negation narrowing, judged roots."""

    REPG_ROOTS = dict.fromkeys((
        "collated", "confiscated", "demolished",
        "embargoed", "franked", "fumigated",
        "immunised", "magnetised", "magnetized",
        "memorized", "mutilated", "packaged",
        "patrolled", "pillaged", "piped",
        "pitched", "pivoted", "plagiarised",
        "plagiarized", "plundered", "poached",
        "pocketed", "pointed", "poisoned",
        "powdered", "presented", "pressed",
        "prevented", "primed", "probated",
        "attachable", "convertible", "countable",
        "leviable", "scanable",
    ))

    CONF_CAN_BE = dict.fromkeys((
        "categorized", "collated", "condensed",
        "converted", "counted", "described",
        "layered", "lined", "linked",
        "measured", "nested", "packaged",
        "painted", "paneled", "papered",
        "penciled", "piled", "piped",
        "queried", "rotated", "saved",
        "shifted", "split", "tailored",
        "tested", "tiled", "trimmed",
        "typed", "unpacked", "unzipped",
        "updated", "weighed", "stretched",
    ))

    CONF_IS = dict.fromkeys((
        "collatable", "condensable", "convertable",
        "countable", "describable", "labellable",
        "mappable", "measurable", "paintable",
        "pennable", "referenceable", "rotatable",
        "splittable", "stretchable", "testable",
        "tileable", "transformable", "unpackable",
        "unzippable", "updatable", "weighable",
    ))

    NO_FORMS = tuple(
        "No record is %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % verb
        for verb in CONF_CAN_BE) + tuple(
        "No record is %s after writing." % root
        for root in CONF_IS)

    ASSERTED = tuple(
        "Records are %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "Records are %s after writing." % verb
        for verb in CONF_CAN_BE) + tuple(
        "Records are %s after writing." % root
        for root in CONF_IS)

    def test_probed_no_forms_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.NO_FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_asserted_analogues_and_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for statement in self.ASSERTED:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)
        self.assertTrue(_scan(
            mod, "No bundle name was hidden in this record."))
        self.assertFalse(_scan(
            mod, "Records are hidden by outsiders."))
        self.assertFalse(_scan(mod, "No data leaves the store."))
        self.assertTrue(
            _scan(mod, "The seal does not guarantee protection."))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))

class SealClaimScanConceptFixR34Tests(unittest.TestCase):
    """Ruling 2029: roots outside the judged concept roots."""

    REPG_ROOTS = dict.fromkeys((
        "accessioned", "appraised", "benchmarked",
        "consigned", "declassified", "degaussed",
        "deregistered", "donated", "enciphered",
        "forfeited", "gazetted", "hyphenated",
        "illustrated", "jettisoned", "laminated",
        "liquidated", "loaned", "manifested",
        "marketed", "marshalled", "negotiated",
        "outsourced", "parceled", "partitioned",
        "actionable", "admissible", "alienable",
        "amendable", "appealable", "attributable",
        "classifiable", "compensable", "contestable",
        "creditable", "dutiable", "foreseeable",
        "forfeitable", "grantable", "heritable",
        "marketable", "negotiable", "ratable",
        "recordable", "redeemable", "registrable",
        "remittable", "rentable", "reportable",
        "rescindable", "returnable", "revocable",
        "saleable", "salvageable", "serviceable",
        "summonable", "taxable", "vendible",
        "voidable", "withdrawable",
    ))

    CONF_ROOTS = dict.fromkeys((
        "markable", "matchable", "modelable",
        "mountable", "nameable", "nestable",
        "notable", "numberable", "orderable",
        "packageable", "pairable", "partitionable",
        "patternable", "placeable", "plotable",
        "projectable", "rankable", "ratable",
        "recordable", "recyclable", "refreshable",
        "reloadable", "reorderable", "repairable",
        "repeatable", "replicable", "reportable",
        "requestable", "rescalable", "reschedulable",
        "resettable", "resolvable", "resumable",
        "returnable", "reusable", "reversible",
        "revisable", "revocable", "runnable",
        "savable", "schedulable", "scopable",
        "scriptable", "sectionable", "separable",
        "sequenceable", "shiftable", "shrinkable",
        "simulatable", "spannable", "startable",
        "stoppable", "strippable", "stylable",
        "submittable", "summable", "supportable",
        "suppressible", "suspendable", "switchable",
        "tailorable", "targetable", "themeable",
        "throttleable", "timeable", "titleable",
        "toggleable", "tradable", "trainable",
        "transmissible", "treatable", "trimmable",
        "truncatable", "tunable", "typeable",
        "upgradable", "vectorizable", "vendible",
        "virtualizable", "voidable", "weldable",
        "yieldable", "zoomable",
    ))

    CONF_VERBS = dict.fromkeys((
        "marked", "matched", "modeled",
        "mounted", "named", "ordered",
        "paired", "partitioned", "patterned",
        "placed", "ranked", "rated",
        "recycled", "refreshed", "reloaded",
        "reordered", "repaired", "repeated",
        "reported", "requested", "rescaled",
        "rescheduled", "reset", "resolved",
        "resumed", "returned", "reused",
        "reversed", "revised", "revoked",
        "run", "scoped", "scripted",
        "sectioned", "sent", "separated",
        "sequenced", "shrunk", "simulated",
        "spaced", "spanned", "started",
        "stopped", "styled", "submitted",
        "summed", "supported", "suppressed",
        "suspended", "targeted", "themed",
        "throttled", "timed", "toggled",
        "traded", "trained", "treated",
        "truncated", "tuned", "valued",
        "vectorized", "virtualized", "voided",
        "yielded", "zoomed",
    ))

    FORMS = tuple(
        "No record is %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "No record can be %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "Records are %s after writing." % root
        for root in REPG_ROOTS) + tuple(
        "The record is %s after writing." % root
        for root in CONF_ROOTS) + tuple(
        "No record is %s after writing." % root
        for root in CONF_ROOTS) + tuple(
        "Records are %s after writing." % verb
        for verb in CONF_VERBS) + tuple(
        "No record can be %s after writing." % verb
        for verb in CONF_VERBS)

    def test_roots_and_verbs_fail(self):
        mod = harness.require("ontoloop.report")
        for statement in self.FORMS:
            self.assertFalse(_scan(mod, statement), statement)
            self.assertFalse(_travel(mod, statement), statement)

    def test_controls_stand(self):
        mod = harness.require("ontoloop.report")
        for root in ("excerpted", "leased", "rescanned"):
            self.assertFalse(_scan(
                mod, "Records are %s after writing." % root))
            self.assertFalse(_scan(
                mod, "No record is %s after writing." % root))
        self.assertTrue(_scan(mod, _GOVERNED_CLAIM + "."))
