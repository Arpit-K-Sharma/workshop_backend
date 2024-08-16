from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator


class SchoolInfo(BaseModel):
    school_id: DBRef
    courses: List[DBRef] = Field(default_factory=list)

    @validator('school_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='school', id=ObjectId(v))
        return v

    @validator('courses', pre=True, always=True)
    def convert_courses(cls, v):
        if isinstance(v, list):
            return [DBRef(collection='course', id=ObjectId(course_id)) if isinstance(course_id, str) else course_id for course_id in v]
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }

class Teacher(BaseModel):
    name: str
    address: str
    username: str
    password: str
    phone_num: str
    profile_pic: Optional[str] = None
    schools: List[SchoolInfo] = Field(default_factory=list)
