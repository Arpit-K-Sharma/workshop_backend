from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, validator

class SchoolDTO(BaseModel):
    school_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    school_code: Optional[str] = None
    course_id: Optional[List[str]] = Field(default_factory=list)
    logo: Optional[UploadFile] = None

    @classmethod
    def as_form(
        cls,
        school_name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        address: Optional[str] = Form(None),
        course_id: Optional[str] = Form([]),
        logo: Optional[UploadFile] = File(None)
    ):
        if course_id:
            course_id_list = course_id.split(",")
        else:
            course_id_list = []
        return cls(
            school_name=school_name,
            email=email,
            password=password,
            address=address,
            course_id=course_id_list,
            logo=logo
        )

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
    school_code: Optional[str] = None
    course_id: Optional[List[str]] = Field(default_factory=list)
    logo: Optional[str] = None
    logo_content: Optional[bytes] = None

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