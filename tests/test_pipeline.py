import asyncio
import unittest

from src.agents.bug_agent import BugAgent
from src.pipeline.diff_pipeline import DiffPipeline


DIFF = """diff --git a/service.py b/service.py
index 1111111..2222222 100644
--- a/service.py
+++ b/service.py
@@ -10,0 +11,4 @@
+try:
+    run()
+except:
+    print("debug")
"""

DOC_DIFF = """diff --git a/docs/guide.rst b/docs/guide.rst
index 1111111..2222222 100644
--- a/docs/guide.rst
+++ b/docs/guide.rst
@@ -1 +1 @@
-Old text
+New text
"""


class PipelineTests(unittest.TestCase):
    class UnavailableLLM:
        model = "stub"
        available = False

    def test_run_returns_chunks(self):
        pipeline = DiffPipeline(llm=self.UnavailableLLM())
        chunks = pipeline.run(DIFF)

        self.assertEqual(1, len(chunks))
        self.assertEqual(["service.py"], chunks[0].files)

    def test_run_async_produces_rated_review_without_llm(self):
        pipeline = DiffPipeline(llm=self.UnavailableLLM())
        review = asyncio.run(pipeline.run_async(DIFF))

        self.assertIn("BugAgent", review)
        self.assertIn("SecurityAgent", review)
        self.assertIn("StyleAgent", review)
        self.assertIn("OVERALL RATING:", review)
        self.assertIn("[high] reliability: Bare except detected", review)

    def test_run_review_async_returns_structured_review(self):
        pipeline = DiffPipeline(llm=self.UnavailableLLM())
        final_review = asyncio.run(pipeline.run_review_async(DIFF))

        self.assertEqual("moderate", final_review.rating)
        self.assertGreater(final_review.total_score, 0)
        self.assertEqual(3, len(final_review.reviews))

    def test_agent_parses_fenced_json(self):
        agent = BugAgent(self.UnavailableLLM())
        chunk = type("Chunk", (), {"files": ["service.py"]})()
        findings = agent.parse_response(
            """```json
[
  {
    "severity": "high",
    "category": "logic",
    "title": "Bad branch",
    "details": "Missing failure path",
    "confidence": "high",
    "file_path": "service.py"
  }
]
```""",
            chunk,
        )

        self.assertEqual(1, len(findings))
        self.assertEqual("high", findings[0].normalized_severity())
        self.assertEqual("Bad branch", findings[0].title)

    def test_docs_only_pr_is_reviewed_conservatively(self):
        pipeline = DiffPipeline(llm=self.UnavailableLLM())
        final_review = asyncio.run(pipeline.run_review_async(DOC_DIFF))

        self.assertEqual("low", final_review.rating)
        self.assertEqual(0, final_review.total_score)
        self.assertTrue(all(not review.findings for review in final_review.reviews))


if __name__ == "__main__":
    unittest.main()
