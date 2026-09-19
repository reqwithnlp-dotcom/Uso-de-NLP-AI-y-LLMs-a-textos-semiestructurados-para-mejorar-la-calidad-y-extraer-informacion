from abc import ABC, abstractmethod

from analyzer.analysis_context import AnalysisContext


class Rule(ABC):
    """
    Base class for all verb tense inconsistency rules.
    """

    @abstractmethod
    def evaluate(self, context: AnalysisContext) -> None:
        """
        Evaluates a sentence and appends any detected issues to the context.

        Args:
            context: Analysis context for a single sentence.
        """
        pass