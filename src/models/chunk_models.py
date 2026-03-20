from pydantic import BaseModel
from typing import List

class Chunk(BaseModel):
    content: str
    tokens: int
    files: List[str]
