from typing import List
from pydantic import BaseModel, Field

class Gallery(BaseModel):
    videos: List[str] = Field(default_factory=list)
    photos: List[str] = Field(default_factory=list)

