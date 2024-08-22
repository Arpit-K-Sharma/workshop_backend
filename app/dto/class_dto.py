from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, field_validator, validator

from app.dto.course_dto import CourseResponseDTO
from app.dto.student_dto import StudentResponseDTO
from app.dto.teacher_dto import TeacherResponseDTO

class ClassDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    class_name: str
    students: Optional[List[str]] = Field(default_factory=list)
    teachers: Optional[List[str]] = Field(default_factory=list)
    courses: Optional[List[str]] = Field(default_factory=list)
    school_id: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }

    @field_validator('students', 'teachers', 'courses', mode='before')
    def convert_dbref_list(cls, v):
        if isinstance(v, list):
            return [str(item.id) if isinstance(item, DBRef) else str(item) for item in v]
        return v

    @field_validator('school_id', mode='before')
    def convert_dbref(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return str(v) if v is not None else None
    
    @field_validator('id', mode='before')
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class ClassResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    class_name: str
    students: Optional[List[StudentResponseDTO]] = Field(default_factory=list)
    teachers: Optional[List[TeacherResponseDTO]] = Field(default_factory=list)
    courses: Optional[List[CourseResponseDTO]] = Field(default_factory=list)
    school_id: Optional[str] = Field(default=None)
    @field_validator('id', mode='before')
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    
    @validator('school_id',pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }
