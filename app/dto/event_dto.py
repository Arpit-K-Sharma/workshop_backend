from typing import List, Optional, Union
from bson import DBRef, ObjectId
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, validator



class EventDTO(BaseModel):
    school_id: str
    school_name: str
    description: str
    organized_date: str
    gallery: List[UploadFile] = []

    @classmethod
    def as_form(
        cls,
        school_id: str = Form(...),
        school_name: str = Form(...),
        description: str = Form(...),
        organized_date: str = Form(...),
        gallery: List[UploadFile] = File(None)
    ):
        return cls(
            school_id=school_id,
            school_name=school_name,
            description=description,
            organized_date=organized_date,
            gallery=gallery or []
        )

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

class EventResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    school_id: Optional[str]
    school_name: Optional[str]
    description: Optional[str]
    organized_date: Optional[str]
    gallery: Optional[List[dict]]

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