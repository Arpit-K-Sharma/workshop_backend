# CourseDTO
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, validator


class CourseDTO(BaseModel):
    course_name: Optional[str]
    course_content: Optional[str]
    course_duration: Optional[str]
    description: Optional[str]
    logo: Optional[str]

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

# CourseResponseDTO
class CourseResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    course_name: Optional[str] = None
    course_content: Optional[str] = None
    course_duration: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None

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