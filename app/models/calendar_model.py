from typing import List, Optional
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, validator

class EventTitle(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    event_name: Optional[str] = Field(default=None)
    event_description: Optional[str] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True

class Day(BaseModel):
    day: int
    events: List[EventTitle]  # This should reference a list of EventTitle objects

class Month(BaseModel):
    month: int
    days: List[Day]  # This should reference a list of Day objects

class SchoolEvents(BaseModel):
    school_id: DBRef
    months: List[Month]  # Changed from events to months

    @validator('school_id', pre=True, always=True)
    def validate_school_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='school', id=ObjectId(v))
        return v
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda v: str(v.id)
        }

class Calendar(BaseModel):
    year: int
    schools: List[SchoolEvents]  # List of SchoolEvents

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda v: str(v.id)
        }