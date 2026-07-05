from analyzer.text_analyzer import TextAnalyzer

from models.response import (
    AnalyzeResponse,
    IssueResponse
)


class VerbTenseService:

    def __init__(self):

        self.analyzer = TextAnalyzer()

    def analyze(self, text: str) -> AnalyzeResponse:

        result = self.analyzer.analyze(text)

        fragments = []

        issues = []

        for context in result.contexts:

            fragments.append(context.sentence.text)

            for issue in context.issues:

                issues.append(

                    IssueResponse(

                        fragment=issue.fragment,

                        position=issue.position,

                        explanation=issue.explanation,

                        error_code=issue.error_code

                    )

                )

        return AnalyzeResponse(

            normalized_text=result.normalized_text,

            fragments=fragments,

            issues=issues

        )