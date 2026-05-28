import unittest

from src.loaders.diff_parser import parse_diff


SAMPLE_DIFF = """diff --git a/app.py b/app.py
index 1111111..2222222 100644
--- a/app.py
+++ b/app.py
@@ -1,2 +1,3 @@
-print("old")
+print("new")
+print("extra")
diff --git a/lib/util.py b/lib/util.py
index 3333333..4444444 100644
--- a/lib/util.py
+++ b/lib/util.py
@@ -4,0 +5,2 @@
+return True
+print("debug")
"""


class ParseDiffTests(unittest.TestCase):
    def test_parses_multiple_files_and_hunks(self):
        files = parse_diff(SAMPLE_DIFF)

        self.assertEqual(2, len(files))
        self.assertEqual("app.py", files[0].path)
        self.assertEqual("lib/util.py", files[1].path)
        self.assertEqual("@@ -1,2 +1,3 @@", files[0].hunks[0].header)
        self.assertIn('+print("new")', files[0].hunks[0].lines)

    def test_ignores_hunks_before_a_file_header(self):
        files = parse_diff("@@ -1 +1 @@\n+orphan")
        self.assertEqual([], files)


if __name__ == "__main__":
    unittest.main()
