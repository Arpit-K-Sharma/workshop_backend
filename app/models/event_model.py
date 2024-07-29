from pydantic import BaseModel
from typing import List

class Event(BaseModel):
    school_name:str
    description:str
    organized_date:str
    # gallery
    videos:List[str]
    photos:List[str]