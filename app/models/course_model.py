
from pydantic import BaseModel
from bson import ObjectId
from pydantic import BaseModel



class Course(BaseModel):
    course_name: str
    course_content: str
    course_duration: str
    description: str
    logo: str


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

