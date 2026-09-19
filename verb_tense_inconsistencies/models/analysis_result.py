from dataclasses import dataclass, field

from analyzer.analysis_context import AnalysisContext


@dataclass
class AnalysisResult:
    """
    Result returned by the TextAnalyzer.
    """

    normalized_text: str

    contexts: list[AnalysisContext] = field(default_factory=list)