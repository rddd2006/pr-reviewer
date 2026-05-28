import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.pipeline.diff_pipeline import DiffPipeline

with open("test.diff", encoding="utf-8") as handle:
    diff = handle.read()

pipeline = DiffPipeline()

review = asyncio.run(pipeline.run_async(diff))

print(review)
