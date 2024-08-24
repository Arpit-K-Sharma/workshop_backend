from typing import List, Optional
from bson import DBRef, ObjectId
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
    profile_pic: Optional[str] = None
    schools: Optional[List[SchoolInfoDTO]] = Field(default_factory=list)

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

    @validator('courses', pre=True, always=True)
    def convert_courses(cls, v):
        if isinstance(v, list):
            return [str(course.id) if isinstance(course, DBRef) else course for course in v]
        return v
    
    @validator('classes', pre=True, always=True)
    def convert_courses(cls, v):
        if isinstance(v, list):
            return [str(clas.id) if isinstance(clas, DBRef) else clas for clas in v]
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
    password: Optional[str] = None
    phone_num: Optional[str] = None
    profile_pic: Optional[str] = None
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

