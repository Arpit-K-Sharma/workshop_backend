# assignment_model.py
from datetime import datetime
from typing import Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator

class Assignment(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    class_id: Optional[DBRef] = None
    teacher_id: Optional[DBRef] = None

    @validator('class_id', pre=True, always=True)
    def convert_class_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='class', id=ObjectId(v))
        return v
    
    @validator('teacher_id', pre=True, always=True)
    def convert_teacher_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='teacher', id=ObjectId(v))
        return v

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }