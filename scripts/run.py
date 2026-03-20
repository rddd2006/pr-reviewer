import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.diff_pipeline import DiffPipeline

diff = open("test.diff").read()

pipeline = DiffPipeline()
chunks = pipeline.run(diff)

print("\nTOTAL CHUNKS:", len(chunks))

for i, c in enumerate(chunks):
    print(f"\n--- CHUNK {i} ---")
    print("FILES:", c.files)
    print("TOKENS:", c.tokens)
    print("CONTENT:\n", c.content[:300])
