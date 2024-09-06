from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, validator

class SchoolInfoDTO(BaseModel):
    school_id: Optional[str]
    classes: Optional[List[str]] = Field(default_factory=list)
    courses: Optional[List[str]] = Field(default_factory=list)


class TeacherDTO(BaseModel):
    name: Optional[str]
    address: Optional[str]
    username: Optional[str]
    password: Optional[str]
    phone_num: Optional[str]
    profile_picture: Optional[UploadFile] = None
    schools: Optional[List[SchoolInfoDTO]] = Field(default_factory=list)

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        address: Optional[str] = Form(None),
        username: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        phone_num: Optional[str] = Form(None),
        profile_picture: Optional[UploadFile] = File(None),
        schools: Optional[List[SchoolInfoDTO]] = Form([])
    ):
        return cls(
            name=name,
            address=address,
            username=username,
            password=password,
            phone_num=phone_num,
            profile_picture=profile_picture,
            schools=schools
        )

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }


class SchoolInfoResponseDTO(BaseModel):
    school_id: Optional[str]
    classes: Optional[List[str]] = Field(default_factory=list)
    courses: Optional[List[str]] = Field(default_factory=list)

    @validator('school_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

    @validator('courses', 'classes', pre=True, always=True)
    def convert_list_items(cls, v):
        if isinstance(v, list):
            return [str(item.id) if isinstance(item, DBRef) else str(item) if isinstance(item, ObjectId) else item for item in v]
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

class TeacherResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: Optional[str] = None
    address: Optional[str] = None
    username: Optional[str] = None
    phone_num: Optional[str] = None
    profile_picture: Optional[str] = None
    profile_picture_content: Optional[bytes] = None
    schools: Optional[List[SchoolInfoResponseDTO]] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
