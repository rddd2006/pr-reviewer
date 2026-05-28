import unittest

from src.chunking.strategies.file_packer import FilePacker
from src.models.diff_models import DiffFile, Hunk


class ChunkingTests(unittest.TestCase):
    def test_large_file_is_split_into_multiple_chunks(self):
        large_hunk = Hunk(
            header="@@ -1 +1 @@",
            lines=["+" + ("x" * 400), "+" + ("y" * 400)],
        )
        diff_file = DiffFile(path="big.py", hunks=[large_hunk])

        chunks = FilePacker(max_tokens=60, compression=None).pack([diff_file])

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunk.files == ["big.py"] for chunk in chunks))
        self.assertTrue(all(chunk.tokens <= 60 for chunk in chunks))

    def test_small_files_are_packed_together(self):
        file_a = DiffFile(path="a.py", hunks=[Hunk(header="@@ -1 +1 @@", lines=["+a = 1"])])
        file_b = DiffFile(path="b.py", hunks=[Hunk(header="@@ -1 +1 @@", lines=["+b = 2"])])

        chunks = FilePacker(max_tokens=200, compression=None).pack([file_a, file_b])

        self.assertEqual(1, len(chunks))
        self.assertEqual(["a.py", "b.py"], chunks[0].files)


if __name__ == "__main__":
    unittest.main()
