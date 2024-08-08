from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator

class ClassDTO(BaseModel):
    class_name: str
    student_id: List[str] = Field(default_factory=list)
    teacher_id: List[str] = Field(default_factory=list)
    course_id: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }

class ClassResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    class_name: str
    student_id: List[DBRef] = Field(default_factory=list)
    teacher_id: List[DBRef] = Field(default_factory=list)
    course_id: List[DBRef] = Field(default_factory=list)

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('student_id', 'teacher_id', 'course_id', pre=True, always=True)
    def convert_to_dbref(cls, v):
        if isinstance(v, list):
            return [DBRef(collection='class', id=ObjectId(item)) if isinstance(item, str) else item for item in v]
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }