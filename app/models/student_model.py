from typing import List
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator



class Student(BaseModel):
    student_name: str
    age: int
    phone_num: str
    address: str
    school_id: DBRef
    course_id: List[DBRef] = Field(default_factory=list)

    @validator('school_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='school', id=ObjectId(v))
        return v

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