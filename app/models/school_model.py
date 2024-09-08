from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator


class School(BaseModel):
    school_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    # banner: Optional[str] = None
    logo: Optional[str] = None
    school_code:Optional[str] = None
    course_id: Optional[List[DBRef]] = Field(default_factory=list)

    @validator('course_id', pre=True, always=True)
    def convert_course_id(cls, v):
        if isinstance(v, list):
            return [DBRef(collection='courses', id=ObjectId(course_id)) if isinstance(course_id, str) else course_id for course_id in v]
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }