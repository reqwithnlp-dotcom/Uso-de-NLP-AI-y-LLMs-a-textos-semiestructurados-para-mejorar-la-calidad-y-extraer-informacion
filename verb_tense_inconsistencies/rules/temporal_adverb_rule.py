from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode
from helpers.time_by_adverb_rules import VERBS_ALLOW_PCONT

class TemporalAdverbRule(Rule):
    """
    Detects inconsistencies between temporal adverbs and verb tenses.

    Examples:
        The system validates the request yesterday.
        The system validated the request tomorrow.
    """


    """
    CLASS ANALYSIS CONTEXT:

    sentence: Span

    verb_phrases: list[VerbPhrase] = field(default_factory=list)

    issues: list[Issue] = field(default_factory=list)
    """

    """
    CLASS ISSUE:
    Represents a detected verb tense inconsistency.
        
    fragment: str
    position: int
    explanation: str
    error_code: str
    """

    """
    CLAS VERB_PHRASE:

    token: Token

    auxiliaries: list[str]

    verb_tag: str    

    tense: str | None
    """


    ERROR_CODE = ErrorCode.TEMPORAL_ADVERB_MISMATCH

    PAST_MARKERS = {
        "yesterday",
        "previous",
        "last",
        "former",
        "past",
        "preceding",
        "prior"
    }

    FUTURE_MARKERS = {
        "tomorrow",
        "next",
        "following",
        "upcoming",
        "coming",
        "future",
        "subsequent"
    }

    def evaluate(self, context: AnalysisContext) -> None:
        test_names = [
            "fut_advb_test",
            "past_advb_test",
            "since_test",
            "now_test",
            "by_test",
            "for_duration_test",
            "yet_test",
            "while_test",
            "when_test",
            "at_present_test",
        ]
        advb_words_to_tests = {test: False for test in test_names}

        simple_tests = {
            "since": "since_test",
            "now": "now_test",
            "by": "by_test",
            "yet": "yet_test",
            "while": "while_test",
            "when": "when_test",
        }

        sentence = context.sentence
        phrase_structure = {}
        for token in sentence.doc:
            phrase_structure[token.pos_] = token.text
            word = token.text.lower()
            if word in simple_tests:
                advb_words_to_tests[simple_tests[word]] = True


            if word in self.PAST_MARKERS:
                advb_words_to_tests["past_advb_test"] = True
            if word in self.FUTURE_MARKERS:
                advb_words_to_tests["fut_advb_test"] = True
            
            if word == "by":
                advb_words_to_tests["by_test"] = True
            if word == "for" and token.i + 1 < len(sentence):
                if token.nbor(1).text.lower() == "duration":
                    advb_words_to_tests["for_duration_test"] = True
            if word == "at" and token.i + 1 < len(sentence):
                if token.nbor(1).text.lower() == "present":
                    advb_words_to_tests["at_present_test"] = True

        for token in sentence.doc:
            
            word = token.text.lower()

            if word in self.PAST_MARKERS:

                self._validate_marker_past(
                    token,
                    expected="past",
                    context=context
                )

            elif word in self.FUTURE_MARKERS:

                self._validate_marker_fut(
                    token,
                    context=context,
                    structure = phrase_structure,
                    adv_pos = token.pos_
                )





    def _validate_marker_fut(
            self,
            marker_token,
            context:AnalysisContext,
            structure,
            adv_pos,
    ) -> None:
        verb_phrase = self._find_related_verb(marker_token, context)
        time_division = verb_phrase.tense.split("-")
        general_time_detected = time_division[1]
        specific_time = time_division[0]
        if general_time_detected == "fut":
            return
        if specific_time == "cont_pres":
            if(self.validate_cont_pres(structure,adv_pos)):
                return

    def validate_cont_pres(structure,adv_pos):
        good_structure = ["PRON","AUX","VERB",adv_pos]
        check_structure = True
        for key,i in structure.keys:
            if(key != good_structure[i]):
                check_structure = False 

        if(structure["VERB"] in VERBS_ALLOW_PCONT and check_structure):
            return True


    def _validate_marker_past(
        self,
        marker_token,
        expected: str,
        context: AnalysisContext
    ) -> None:

        verb_phrase = self._find_related_verb(marker_token, context)

        if verb_phrase is None:
            return

        if verb_phrase.tense is None:
            return

        detected = verb_phrase.tense.split("-")[-1]

        if detected == expected:
            return

        context.issues.append(
            Issue(
                fragment=f"{marker_token.text} → {verb_phrase.token.text}",
                position=marker_token.idx,
                explanation=(
                    f"Temporal reference '{marker_token.text}' "
                    f"is inconsistent with the verb tense."
                ),
                error_code=self.ERROR_CODE
            )
        )

    @staticmethod
    def _find_related_verb(marker_token, context):

        head = marker_token.head

        while head != head.head:

            if head.pos_ == "VERB":
                break

            head = head.head

        if head.pos_ != "VERB":
            return None

        for phrase in context.verb_phrases:

            if phrase.token == head:
                return phrase

        return None