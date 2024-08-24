from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator


class SchoolInfo(BaseModel):
    school_id: Optional[DBRef]
    classes: Optional[List[DBRef]] = Field(default_factory=list)
    courses: Optional[List[DBRef]] = Field(default_factory=list)

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
    
    @validator('classes', pre=True, always=True)        
    def convert_classes(cls, v):
        if isinstance(v, list):
            return [DBRef(collection='class', id=ObjectId(class_id)) if isinstance(class_id, str) else class_id for class_id in v]
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }

class Teacher(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    phone_num: Optional[str] = None
    profile_pic: Optional[str] = None
    schools: List[SchoolInfo] = Field(default_factory=list)
