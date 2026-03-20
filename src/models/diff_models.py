from pydantic import BaseModel
from typing import List

class Hunk(BaseModel):
    header: str
    lines: List[str]

class DiffFile(BaseModel):
    path: str
    hunks: List[Hunk]
