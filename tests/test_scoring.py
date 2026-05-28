import unittest

from src.aggregator.review_aggregator import ReviewAggregator
from src.aggregator.scorer import score_finding, score_findings
from src.models.review_models import Finding


class ScoringTests(unittest.TestCase):
    def test_score_finding_respects_severity_and_confidence(self):
        finding = Finding(
            severity="high",
            category="security",
            title="shell=True",
            details="Risky shell invocation",
            confidence="medium",
        )
        self.assertEqual(4, score_finding(finding))

    def test_aggregate_returns_structured_review_and_rating(self):
        final_review = ReviewAggregator().aggregate(
            {
                "BugAgent": [
                    Finding(
                        severity="high",
                        category="logic",
                        title="Logic flaw",
                        details="A failure path is missing.",
                        confidence="high",
                    )
                ],
                "SecurityAgent": [
                    Finding(
                        severity="critical",
                        category="injection",
                        title="eval found",
                        details="Dynamic code execution is present.",
                        confidence="high",
                    )
                ],
                "StyleAgent": [
                    Finding(
                        severity="low",
                        category="readability",
                        title="Long line",
                        details="The line is too long.",
                        confidence="high",
                    )
                ],
            }
        )

        self.assertEqual(17, final_review.total_score)
        self.assertEqual("high", final_review.rating)

        rendered = ReviewAggregator().render(final_review)
        self.assertIn("OVERALL RISK SCORE: 17", rendered)
        self.assertIn("OVERALL RATING: high", rendered)
        self.assertIn("Logic flaw", rendered)

    def test_score_findings_sums_multiple_findings(self):
        findings = [
            Finding("critical", "security", "A", "A", confidence="high"),
            Finding("medium", "bug", "B", "B", confidence="low"),
        ]
        self.assertEqual(12, score_findings(findings))


if __name__ == "__main__":
    unittest.main()
