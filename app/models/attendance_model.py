from datetime import datetime
from typing import List, Optional
from bson import ObjectId, DBRef
from pydantic import BaseModel, Field, validator

class StudentStatus(BaseModel):
    student_id: DBRef
    status: str
    remarks: Optional[str] = Field(default=None)

    @validator('student_id', pre=True, always=True)
    def convert_student_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='students', id=ObjectId(v))
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }

class TeacherStatus(BaseModel):
    teacher_id: DBRef
    status: str
    remarks: Optional[str] = Field(default=None)

    @validator('teacher_id', pre=True, always=True)
    def convert_teacher_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='teachers', id=ObjectId(v))
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }

class SchoolStatus(BaseModel):
    school_id: DBRef
    students: List[StudentStatus] = Field(default_factory=list)
    teachers: List[TeacherStatus] = Field(default_factory=list)

    @validator('school_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='schools', id=ObjectId(v))
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }

class Attendance(BaseModel):
    date: str
    schools: List[SchoolStatus]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }