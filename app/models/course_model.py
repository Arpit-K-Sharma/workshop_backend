
from typing import Optional
from pydantic import BaseModel
from bson import ObjectId
from pydantic import BaseModel



class Course(BaseModel):
    course_name: Optional[str]
    course_content: Optional[str]
    course_duration: Optional[str]
    description: Optional[str]
    logo: Optional[str]


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

