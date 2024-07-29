from typing import List
from pydantic import BaseModel

class Gallery (BaseModel):
  video:List[str]
  photo:List[str]

class School(BaseModel):
  school_name:str
  email:str
  password: str
  address:str
  banner:str
  logo:str
  course_id:str
  gallery:Gallery