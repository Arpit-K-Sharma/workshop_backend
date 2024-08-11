from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator


class StudentDTO(BaseModel):
    student_name: str
    age: int
    phone_num: str
    address: str
    school_id: str
    class_id: Optional[str] = None
    course_id: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

class StudentResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    student_name: Optional[str] = None
    age: Optional[int] = None
    phone_num: Optional[str] = None
    address: Optional[str] = None
    school_id: Optional[str] = None
    class_id: Optional[str] = None
    course_id: Optional[List[str]] = Field(default_factory=list)

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('school_id', 'class_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

    @validator('course_id', pre=True, always=True)
    def convert_course_id(cls, v):
        if isinstance(v, list):
            return [str(course.id) if isinstance(course, DBRef) else course for course in v]
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
