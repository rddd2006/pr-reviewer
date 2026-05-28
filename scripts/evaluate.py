import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.pipeline.diff_pipeline import DiffPipeline
from src.core.config import Settings

with open("test.diff", encoding="utf-8") as handle:
    diff = handle.read()

pipeline = DiffPipeline()
chunks = pipeline.run(diff)

max_tokens = Settings.from_env().max_tokens

print("\n====== EVALUATION ======")

violations = [chunk.tokens for chunk in chunks if chunk.tokens > max_tokens]
print("Token violations:", len(violations))

avg_tokens = sum(chunk.tokens for chunk in chunks) / len(chunks) if chunks else 0
print("Avg tokens:", avg_tokens)
print("Efficiency (%):", round((avg_tokens / max_tokens) * 100, 2) if max_tokens else 0)

print("Total chunks:", len(chunks))

file_map = {}
for chunk in chunks:
    for file_path in chunk.files:
        file_map[file_path] = file_map.get(file_path, 0) + 1

print("\nFile appearances:")
for file_path, count in sorted(file_map.items()):
    print(file_path, "->", count)
