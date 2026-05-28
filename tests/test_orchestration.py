import asyncio
import tempfile
import unittest
from pathlib import Path

from src.orchestration.digest import PRDigestBuilder
from src.orchestration.models import PRRequest
from src.orchestration.service import PRAgentService
from src.pipeline.diff_pipeline import DiffPipeline


DIFF = """diff --git a/src/auth.py b/src/auth.py
index 1111111..2222222 100644
--- a/src/auth.py
+++ b/src/auth.py
@@ -1,0 +1,5 @@
+def login(token):
+    try:
+        return True
+    except:
+        print("debug")
"""


class OrchestrationTests(unittest.TestCase):
    class UnavailableLLM:
        model = "stub"
        available = False

    def test_digest_detects_status_priority_and_support_docs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "CONTRIBUTING.md").write_text("rules", encoding="utf-8")

            digest = PRDigestBuilder().build(
                PRRequest(diff_text=DIFF, command="review"),
                repo_root=repo_root,
            )

            self.assertEqual("ready_for_review", digest.status)
            self.assertEqual(1, digest.file_count)
            self.assertEqual(["src/auth.py"], digest.prioritized_files)
            self.assertEqual("FUTURE", digest.support_docs[0].label)

    def test_reflect_returns_question_comment(self):
        service = PRAgentService(
            pipeline=DiffPipeline(llm=self.UnavailableLLM()),
            repo_root=".",
        )

        result = asyncio.run(
            service.run(PRRequest(diff_text=DIFF, command="reflect"))
        )

        self.assertEqual("PR comment", result.result_type)
        self.assertTrue(result.plan.wait_for_user)
        self.assertIn("highest-priority concern", result.body)

    def test_generate_labels_returns_expected_shape(self):
        service = PRAgentService(
            pipeline=DiffPipeline(llm=self.UnavailableLLM()),
            repo_root=".",
        )

        result = asyncio.run(
            service.run(PRRequest(diff_text=DIFF, command="generate_labels"))
        )

        self.assertEqual("PR labels", result.result_type)
        self.assertIn("possible security issue", result.body)
        self.assertIn("review effort", result.body)


if __name__ == "__main__":
    unittest.main()
