import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.pipeline.diff_pipeline import DiffPipeline
from src.core.config import Settings

diff = open("test.diff").read()

pipeline = DiffPipeline()
chunks = pipeline.run(diff)

MAX = Settings.MAX_TOKENS

print("\n====== EVALUATION ======")

# 1. token safety
violations = [c.tokens for c in chunks if c.tokens > MAX]
print("Token violations:", len(violations))

# 2. efficiency
avg_tokens = sum(c.tokens for c in chunks) / len(chunks)
print("Avg tokens:", avg_tokens)
print("Efficiency (%):", round((avg_tokens / MAX) * 100, 2))

# 3. chunk count
print("Total chunks:", len(chunks))

# 4. file distribution
file_map = {}
for c in chunks:
    for f in c.files:
        file_map[f] = file_map.get(f, 0) + 1

print("\nFile appearances:")
for k, v in file_map.items():
    print(k, "→", v)
from src.pipeline.diff_pipeline import DiffPipeline
from src.core.config import Settings

diff = open("test.diff").read()

pipeline = DiffPipeline()
chunks = pipeline.run(diff)

MAX = Settings.MAX_TOKENS

print("\n====== EVALUATION ======")

# 1. token safety
violations = [c.tokens for c in chunks if c.tokens > MAX]
print("Token violations:", len(violations))

# 2. efficiency
avg_tokens = sum(c.tokens for c in chunks) / len(chunks)
print("Avg tokens:", avg_tokens)
print("Efficiency (%):", round((avg_tokens / MAX) * 100, 2))

# 3. chunk count
print("Total chunks:", len(chunks))

# 4. file distribution
file_map = {}
for c in chunks:
    for f in c.files:
        file_map[f] = file_map.get(f, 0) + 1

print("\nFile appearances:")
for k, v in file_map.items():
    print(k, "→", v)
