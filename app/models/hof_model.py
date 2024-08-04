from bson import DBRef, ObjectId
from pydantic import BaseModel, validator   
from app.models.gallery_model import Gallery


class Achiever(BaseModel):
    achiever_id: DBRef
    date: str
    description: str
    gallery: Gallery

    @validator('achiever_id', pre=True, always=True)
    def convert_achiever_id(cls, v):
        if isinstance(v, str):
            return DBRef(collection='achievers', id=ObjectId(v))
        return v

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }