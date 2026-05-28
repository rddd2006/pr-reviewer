from src.aggregator.scorer import score_findings
from src.models.review_models import AgentReview, FinalReview, Finding


class ReviewAggregator:

    def aggregate(self, results):
        reviews = []
        for agent_name, findings in results.items():
            reviews.append(AgentReview(agent_name=agent_name, findings=findings))

        total_score = sum(score_findings(review.findings) for review in reviews)
        rating = self._rating(total_score)
        return FinalReview(reviews=reviews, total_score=total_score, rating=rating)

    def render(self, final_review: FinalReview):
        output = "\n===== FINAL REVIEW =====\n\n"

        for review in final_review.reviews:
            score = score_findings(review.findings)
            output += f"--- {review.agent_name} (score: {score}) ---\n"
            if not review.findings:
                output += "[info] No findings.\n\n"
                continue

            for finding in review.findings:
                severity = finding.normalized_severity()
                location = f" [{finding.file_path}]" if finding.file_path else ""
                output += (
                    f"[{severity}] {finding.category}: {finding.title}{location} "
                    f"(confidence: {finding.confidence})\n"
                )
                output += f"{finding.details}\n"
            output += "\n"

        output += f"\nOVERALL RISK SCORE: {final_review.total_score}\n"
        output += f"OVERALL RATING: {final_review.rating}\n"
        return output

    def _rating(self, score):
        if score >= 18:
            return "critical"
        if score >= 9:
            return "high"
        if score >= 3:
            return "moderate"
        return "low"
