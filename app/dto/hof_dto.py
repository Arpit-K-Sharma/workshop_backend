from typing import Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator

from app.models.gallery_model import Gallery


class AchieverDTO(BaseModel):
    achiever_id: str
    date: str
    description: str
    gallery: Gallery

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

# AchieverResponseDTO
class AchieverResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    achiever_id: str
    date: str
    description: str
    gallery: Gallery

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('achiever_id', pre=True, always=True)
    def convert_achiever_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
