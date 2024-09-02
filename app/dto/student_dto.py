from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, validator


class StudentDTO(BaseModel):
    student_name: Optional[str]
    age: Optional[int]
    phone_num: Optional[str]
    address: Optional[str]
    school_id: Optional[str]
    class_id: Optional[str]
    course_id: Optional[List[str]] = Field(default_factory=list)
    profile_picture: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        student_name: Optional[str] = Form(None),
        age: Optional[int] = Form(None),
        phone_num: Optional[str] = Form(None),
        address: Optional[str] = Form(None),
        school_id: Optional[str] = Form(None),
        class_id: Optional[str] = Form(None),
        course_id: Optional[List[str]] = Form([]),
        profile_picture: Optional[UploadFile] = File(None)
    ):
        return cls(
            student_name=student_name,
            age=age,
            phone_num=phone_num,
            address=address,
            school_id=school_id,
            class_id=class_id,
            course_id=course_id,
            profile_picture=profile_picture
        )

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
    student_email: Optional[str] = None
    address: Optional[str] = None
    school_id: Optional[str] = None
    class_id: Optional[str] = None
    course_id: Optional[List[str]] = Field(default_factory=list)
    profile_picture: Optional[str] = None

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
