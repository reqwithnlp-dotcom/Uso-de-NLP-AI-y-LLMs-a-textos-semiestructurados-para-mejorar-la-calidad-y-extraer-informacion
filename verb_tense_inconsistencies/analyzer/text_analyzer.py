from analyzer.analysis_context import AnalysisContext
from analyzer.normalizer import TextNormalizer
from analyzer.sentence_splitter import SentenceSplitter

from extractors.verb_tense_extractor import VerbTenseExtractor
from extractors.adverb_extractor import AdverbExtractor

from models.analysis_result import AnalysisResult

from rules.auxiliary_mismatch_rule import AuxiliaryMismatchRule
from rules.connector_mismatch_rule import ConnectorMismatchRule
from rules.subject_verb_rule import SubjectVerbRule
from rules.temporal_adverb_rule import TemporalAdverbRule
from rules.tense_mismatch_rule import TenseMismatchRule


class TextAnalyzer:

    def __init__(self):

        #
        # Shared extractors
        #
        self.extractors = [
            VerbTenseExtractor(),
            AdverbExtractor()
        ]

        #
        # Rules executed first.
        #
        self.basic_rules = [
            AuxiliaryMismatchRule()
        ]

        #
        # Rules executed only if the sentence
        # contains valid verb phrases.
        #
        self.advanced_rules = [
            SubjectVerbRule(),
            ConnectorMismatchRule(),
            TemporalAdverbRule(),
            TenseMismatchRule()
        ]

    def analyze(self, text: str) -> AnalysisResult:

        normalized_text = TextNormalizer.normalize(text)

        fragments = SentenceSplitter.split(normalized_text)

        contexts = []

        for sentence in fragments:

            context = AnalysisContext(sentence)

            self._run_extractors(context)

            self._run_basic_rules(context)

            #
            # Continue only if some verb phrase
            # could be extracted.
            #
            if context.verb_phrases:

                self._run_advanced_rules(context)

            contexts.append(context)

        return AnalysisResult(

            normalized_text=normalized_text,

            contexts=contexts
        )

    def _run_extractors(self, context):

        for extractor in self.extractors:

            extractor.extract(context)

    def _run_basic_rules(self, context):

        for rule in self.basic_rules:

            rule.evaluate(context)

    def _run_advanced_rules(self, context):

        for rule in self.advanced_rules:

            rule.evaluate(context)