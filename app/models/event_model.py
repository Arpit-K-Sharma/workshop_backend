from typing import List, Optional
from bson import ObjectId, DBRef
from pydantic import BaseModel, Field, validator

from app.models.gallery_model import Gallery


class Event(BaseModel):
    school_id: DBRef
    school_name: str
    description: str
    organized_date: str
    gallery: Gallery

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
