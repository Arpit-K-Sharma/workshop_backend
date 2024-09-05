from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator



class Student(BaseModel):
    student_name: Optional[str] = None
    age: Optional[int] = None
    phone_num: Optional[str] = None
    # student_email: Optional[str] = None
    studentId: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    school_id: Optional[DBRef] = None
    class_id: Optional[DBRef] = None
    course_id: Optional[List[DBRef]] = Field(default_factory=list)
    profile_picture: Optional[str] = None
    is_password_changed: Optional[bool] = False

    @validator('school_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='school', id=ObjectId(v))
        return v
    
    @validator('class_id', pre=True, always=True, allow_reuse=True)
    def convert_class_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='class', id=ObjectId(v))
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