import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.diff_pipeline import DiffPipeline

with open("test.diff", encoding="utf-8") as handle:
    diff = handle.read()

pipeline = DiffPipeline()
chunks = pipeline.run(diff)

print("\nTOTAL CHUNKS:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n--- CHUNK {i} ---")
    print("FILES:", chunk.files)
    print("TOKENS:", chunk.tokens)
    print("CONTENT:\n", chunk.content[:300])
