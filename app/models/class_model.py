from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, field_validator

class Class(BaseModel):
    class_name: Optional[str] = None
    students: Optional[List[DBRef]] = Field(default_factory=list)
    teachers: Optional[List[DBRef]] = Field(default_factory=list)
    courses: Optional[List[DBRef]] = Field(default_factory=list)
    school_id: Optional[DBRef] = None

    @field_validator('students', 'teachers', 'courses', mode='before')
    def convert_to_dbref(cls, v, info):
        if isinstance(v, list):
            collection_name = {
                'students': 'student',
                'teachers': 'teacher',
                'courses': 'course'
            }.get(info.field_name, 'class')
            return [DBRef(collection=collection_name, id=item) if isinstance(item, str) else item for item in v]
        return v

    @field_validator('school_id', mode='before')
    def convert_school_id_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection='school', id=v)
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }
