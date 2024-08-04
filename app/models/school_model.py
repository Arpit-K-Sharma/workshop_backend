from typing import List
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator
from app.models.gallery_model import Gallery


class School(BaseModel):
    school_name: str
    email: str
    password: str
    address: str
    banner: str
    logo: str
    course_id: List[DBRef] = Field(default_factory=list)

    @validator('course_id', pre=True, always=True)
    def convert_course_id(cls, v):
        if isinstance(v, list):
            return [DBRef(collection='courses', id=ObjectId(course_id)) if isinstance(course_id, str) else course_id for course_id in v]
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }