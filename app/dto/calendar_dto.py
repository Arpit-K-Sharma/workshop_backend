from typing import List, Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId, DBRef

class EventTitleDTO(BaseModel):
    id : str
    event_name: Optional[str] = Field(default=None)
    event_description: Optional[str] = Field(default=None)


class DayDTO(BaseModel):
    day: int
    events: List[EventTitleDTO] = Field(default_factory=list)

class MonthDTO(BaseModel):
    month: int
    days: List[DayDTO] = Field(default_factory=list)

class SchoolEventsDTO(BaseModel):
    school_id: str
    months: List[MonthDTO] = Field(default_factory=list)

class CalendarDTO(BaseModel):
    year: int
    schools: List[SchoolEventsDTO] = Field(default_factory=list)

##Response

class EventTitleDTOResponse(BaseModel):
    id : str
    event_name: Optional[str] = Field(default=None)
    event_description: Optional[str] = Field(default=None)

    @validator("id", pre=True, always=True)
    def convert_objectid_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    class Config:
        arbitrary_types_allowed = True

class DayDTOResponse(BaseModel):
    day: int
    events: List[EventTitleDTOResponse] = Field(default_factory=list)

class MonthDTOResponse(BaseModel):
    month: int
    days: List[DayDTOResponse] = Field(default_factory=list)

class SchoolEventsDTOResponse(BaseModel):
    school_id: str
    events: List[MonthDTOResponse] = Field(default_factory=list)

    @validator('school_id', pre=True, always=True)
    def convert_school_id(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

class CalendarDTOResponse(BaseModel):
    year: int
    schools: List[SchoolEventsDTOResponse] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
        }



class UpdateEventDTO(BaseModel):
    event_name : str
    event_description : str