from bson import DBRef, ObjectId
from pydantic import BaseModel, validator


class Feedback(BaseModel):
    feedback_by: DBRef
    feedback_for: DBRef
    rating: int
    feedback_description: str

    @validator('feedback_by', 'feedback_for', pre=True, always=True)
    def convert_str_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection='feedback', id=ObjectId(v))
        return v

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }