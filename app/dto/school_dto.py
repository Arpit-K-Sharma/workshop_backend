from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import File, UploadFile
from pydantic import BaseModel, Field, validator

from app.models.gallery_model import Gallery


class SchoolDTO(BaseModel):
    school_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    address: Optional[str]
    course_id: Optional[List[str]] = []

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

class SchoolResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    school_name: str
    email: str
    address: str
    banner: str
    logo: str
    course_id: List[str] = Field(default_factory=list)

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