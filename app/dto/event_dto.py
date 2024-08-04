from typing import Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator

from app.models.gallery_model import Gallery


class EventDTO(BaseModel):
    school_id: str
    school_name: str
    description: str
    organized_date: str
    gallery: Gallery

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

class EventResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    school_id: str
    school_name: str
    description: str
    organized_date: str
    gallery: Gallery

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('school_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }