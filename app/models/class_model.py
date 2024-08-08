from typing import List
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator

class Class(BaseModel):
    class_name: str
    student_id: List[DBRef] = Field(default_factory=list)
    teacher_id: List[DBRef] = Field(default_factory=list)
    course_id: List[DBRef] = Field(default_factory=list)

    @validator('student_id', 'teacher_id', 'course_id', pre=True, always=True)
    def convert_to_dbref(cls, v):
        if isinstance(v, list):
            return [DBRef(collection='class', id=item) if isinstance(item, str) else item for item in v]
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }