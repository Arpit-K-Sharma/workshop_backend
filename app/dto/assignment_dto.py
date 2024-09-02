# assignment_dto.py
from datetime import datetime
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional

class AssignmentDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    class_id: Optional[str] = None
    teacher_id: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }


class AssignmentResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    class_id: Optional[str] = None
    teacher_id: Optional[str] = None

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    @validator('teacher_id', 'class_id', pre=True, always=True)
    def convert_teacher_school_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
