from datetime import datetime
from typing import Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, field_validator

class JournalDTO(BaseModel):
    body: str
    date: Optional[datetime] = Field(default_factory=datetime.now)
    mentor_id: str


class JournalResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    body: str
    date: str 
    mentor_id: str

    @field_validator('id', mode='before')
    def convert_id_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_validator('mentor_id', mode='before')
    def convert_mentor_id_to_str(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        elif isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }



