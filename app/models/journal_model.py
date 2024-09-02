from datetime import datetime
from bson import DBRef, ObjectId
from pydantic import BaseModel, Field, field_validator

class Journal(BaseModel):
    title: str
    body: str
    date: str
    mentor_id: DBRef

    @field_validator('date', mode='before')
    def validate_date(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%d-%m-%Y')
        elif isinstance(v, str):
            try:
                # Try to parse the string as a datetime
                dt = datetime.strptime(v, '%Y-%m-%d')  # Assuming input format is YYYY-MM-DD
                return dt.strftime('%d-%m-%Y')
            except ValueError:
                # If it's already in the correct format, return as is
                return v
        raise ValueError('Invalid date format')

    @field_validator('mentor_id', mode='before')
    def validate_mentor_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='teacher', id=ObjectId(v))
        elif isinstance(v, DBRef):
            return v
        raise ValueError('Invalid mentor_id format')

    class Config:
        arbitrary_types_allowed = True
