from typing import List, Optional
from bson import ObjectId, DBRef
from pydantic import BaseModel, Field, validator



class Event(BaseModel):
    school_id: Optional[DBRef] = None
    school_name: Optional[str] = None
    description: Optional[str] = None
    organized_date: Optional[str] = None
    gallery: Optional[List[str]] = None

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
