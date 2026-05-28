import argparse
import asyncio
import json
import statistics
import sys
import time
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.pipeline.diff_pipeline import DiffPipeline


DEFAULT_BENCHMARK_FILE = Path(__file__).resolve().parent.parent / "benchmark_prs.json"


def load_benchmarks(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def fetch_pr_diff(repo, pr_number, timeout=30):
    url = f"https://github.com/{repo}/pull/{pr_number}.diff"
    response = requests.get(
        url,
        timeout=timeout,
        headers={
            "Accept": "application/vnd.github.v3.diff",
            "User-Agent": "diff-reviewer-benchmark",
        },
    )
    response.raise_for_status()
    return response.text, url

async def review_one_pr(pipeline, benchmark):
    diff_text, diff_url = fetch_pr_diff(benchmark["repo"], benchmark["pr"])
    start = time.perf_counter()
    chunks = pipeline.run(diff_text)
    final_review = await pipeline.run_review_async(diff_text)
    duration = time.perf_counter() - start
    metrics = {
        "total_score": final_review.total_score,
        "rating": final_review.rating,
        "per_agent": {
            review.agent_name: {
                "findings": [
                    {
                        "severity": finding.normalized_severity(),
                        "category": finding.category,
                        "title": finding.title,
                        "details": finding.details,
                        "confidence": finding.confidence,
                        "file_path": finding.file_path,
                    }
                    for finding in review.findings
                ]
            }
            for review in final_review.reviews
        },
    }
    metrics.update(
        {
            "name": benchmark["name"],
            "repo": benchmark["repo"],
            "pr": benchmark["pr"],
            "kind": benchmark.get("kind", "unknown"),
            "diff_url": diff_url,
            "diff_bytes": len(diff_text.encode("utf-8")),
            "chunk_count": len(chunks),
            "chunk_tokens": [chunk.tokens for chunk in chunks],
            "duration_seconds": round(duration, 3),
            "review_text": pipeline.aggregator.render(final_review),
            "llm_available": getattr(pipeline.llm, "available", False),
            "model": getattr(pipeline.llm, "model", "unknown"),
        }
    )
    return metrics


async def review_with_fallback(benchmark):
    pipeline = DiffPipeline()
    try:
        result = await review_one_pr(pipeline, benchmark)
        result["fallback_used"] = False
        return result
    except Exception as exc:
        if getattr(pipeline.llm, "available", False):
            pipeline.llm.client = None
            pipeline.llm.gemini_api_keys = []
            result = await review_one_pr(pipeline, benchmark)
            result["fallback_used"] = True
            result["fallback_reason"] = f"{exc.__class__.__name__}: {exc}"
            return result
        raise


def summarize(results):
    scores = [result["total_score"] for result in results]
    durations = [result["duration_seconds"] for result in results]
    chunk_counts = [result["chunk_count"] for result in results]
    token_counts = [token for result in results for token in result["chunk_tokens"]]
    invalid_json_reviews = 0
    non_empty_reviews = 0
    total_findings = 0

    summary = {
        "prs_reviewed": len(results),
        "avg_score": round(statistics.mean(scores), 2) if scores else 0,
        "median_score": round(statistics.median(scores), 2) if scores else 0,
        "max_score": max(scores) if scores else 0,
        "avg_duration_seconds": round(statistics.mean(durations), 3) if durations else 0,
        "avg_chunk_count": round(statistics.mean(chunk_counts), 2) if chunk_counts else 0,
        "avg_chunk_tokens": round(statistics.mean(token_counts), 2) if token_counts else 0,
        "rating_distribution": {},
        "invalid_json_rate": 0,
        "non_empty_review_rate": 0,
        "avg_findings_per_pr": 0,
        "docs_low_risk_rate": 0,
        "code_non_empty_rate": 0,
        "fallback_rate": 0,
    }
    docs_total = 0
    docs_low_risk = 0
    code_total = 0
    code_non_empty = 0
    fallback_count = 0

    for result in results:
        rating = result["rating"]
        summary["rating_distribution"][rating] = summary["rating_distribution"].get(rating, 0) + 1
        pr_findings = 0
        for review in result.get("per_agent", {}).values():
            findings = review.get("findings", [])
            pr_findings += len(findings)
            invalid_json_reviews += sum(
                1
                for finding in findings
                if finding.get("title") == "Model output was not valid JSON"
            )
        total_findings += pr_findings
        if pr_findings > 0:
            non_empty_reviews += 1
        if result.get("kind") == "docs":
            docs_total += 1
            if result["rating"] == "low":
                docs_low_risk += 1
        if result.get("kind") == "code":
            code_total += 1
            if pr_findings > 0:
                code_non_empty += 1
        if result.get("fallback_used"):
            fallback_count += 1

    if results:
        summary["invalid_json_rate"] = round(invalid_json_reviews / len(results), 2)
        summary["non_empty_review_rate"] = round(non_empty_reviews / len(results), 2)
        summary["avg_findings_per_pr"] = round(total_findings / len(results), 2)
        summary["fallback_rate"] = round(fallback_count / len(results), 2)
    if docs_total:
        summary["docs_low_risk_rate"] = round(docs_low_risk / docs_total, 2)
    if code_total:
        summary["code_non_empty_rate"] = round(code_non_empty / code_total, 2)

    return summary


async def main():
    parser = argparse.ArgumentParser(description="Benchmark the diff reviewer on real GitHub PRs.")
    parser.add_argument(
        "--benchmarks",
        default=str(DEFAULT_BENCHMARK_FILE),
        help="Path to the benchmark PR definition JSON file.",
    )
    parser.add_argument(
        "--output",
        default="benchmark_results.json",
        help="Where to write the benchmark results JSON.",
    )
    args = parser.parse_args()

    benchmarks = load_benchmarks(args.benchmarks)
    results = []

    for benchmark in benchmarks:
        try:
            result = await review_with_fallback(benchmark)
        except Exception as exc:
            result = {
                "name": benchmark["name"],
                "repo": benchmark["repo"],
                "pr": benchmark["pr"],
                "error": f"{exc.__class__.__name__}: {exc}",
            }
            print(f"{benchmark['repo']}#{benchmark['pr']} failed: {result['error']}")
        else:
            print(
                f"{benchmark['repo']}#{benchmark['pr']} "
                f"rating={result['rating']} score={result['total_score']} "
                f"chunks={result['chunk_count']} duration={result['duration_seconds']}s "
                f"model={result['model']} fallback={result['fallback_used']}"
            )
        results.append(result)

    payload = {
        "summary": summarize([result for result in results if "error" not in result]),
        "results": results,
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    print("\nSummary:")
    print(json.dumps(payload["summary"], indent=2))
    print(f"\nWrote {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
