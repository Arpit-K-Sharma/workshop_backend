from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId, DBRef


class StudentStatusDTO(BaseModel):
    student_id: str
    status: str
    remarks: Optional[str] = Field(default=None)

class TeacherStatusDTO(BaseModel):
    teacher_id: str
    status: str
    remarks: Optional[str] = Field(default=None)

class SchoolStatusDTO(BaseModel):
    school_id: str
    students: List[StudentStatusDTO] = Field(default_factory=list)
    teachers: List[TeacherStatusDTO] = Field(default_factory=list)

class AttendanceDTO(BaseModel):
    date: str
    schools: List[SchoolStatusDTO]

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

# Response DTO models

class StudentStatusResponseDTO(BaseModel):
    student_id: str
    status: str
    remarks: Optional[str] = Field(default=None)

    @validator('student_id', pre=True, always=True)
    def convert_student_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

class TeacherStatusResponseDTO(BaseModel):
    teacher_id: str
    status: str
    remarks: Optional[str] = Field(default=None)

    @validator('teacher_id', pre=True, always=True)
    def convert_teacher_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

class SchoolStatusResponseDTO(BaseModel):
    school_id: str
    students: List[StudentStatusResponseDTO] = Field(default_factory=list)
    teachers: List[TeacherStatusResponseDTO] = Field(default_factory=list)

    @validator('school_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

class AttendanceResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    date: str
    schools: List[SchoolStatusResponseDTO]

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }