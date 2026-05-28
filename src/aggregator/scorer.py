from src.models.review_models import Finding


SEVERITY_WEIGHTS = {
    "critical": 10,
    "high": 6,
    "medium": 3,
    "low": 1,
    "info": 0,
}

CONFIDENCE_MULTIPLIERS = {
    "high": 1.0,
    "medium": 0.75,
    "low": 0.5,
}


def score_finding(finding: Finding) -> int:
    severity = finding.normalized_severity()
    confidence = finding.confidence.strip().lower()
    multiplier = CONFIDENCE_MULTIPLIERS.get(confidence, CONFIDENCE_MULTIPLIERS["medium"])
    return round(SEVERITY_WEIGHTS[severity] * multiplier)


def score_findings(findings: list[Finding]) -> int:
    return sum(score_finding(finding) for finding in findings)
