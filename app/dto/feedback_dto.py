from typing import Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator


class FeedbackDTO(BaseModel):
    feedback_by: str
    feedback_for: str
    rating: int
    feedback_date: str
    feedback_description: str

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

# FeedbackResponseDTO
class FeedbackResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    feedback_by: str
    feedback_for: str
    rating: int
    feedback_date: str
    feedback_description: str

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('feedback_by', 'feedback_for', pre=True, always=True)
    def convert_dbref_to_str(cls, v):
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