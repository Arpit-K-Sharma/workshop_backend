from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import File, UploadFile
from pydantic import BaseModel, Field, validator



class SchoolDTO(BaseModel):
    school_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    course_id: Optional[List[str]] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

class SchoolResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    school_name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    # banner: Optional[str]
    # logo: Optional[str]
    school_code: Optional[str] = None
    course_id: Optional[List[str]] = Field(default_factory=list)

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
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