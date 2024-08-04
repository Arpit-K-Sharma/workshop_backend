from typing import List
from bson import ObjectId,DBRef
from bson.json_util import dumps, loads
from app.models.event_model import Event
from app.config.db_config import mongodb
from app.dto.event_dto import EventResponseDTO
from fastapi import HTTPException

class EventRepository:
    @staticmethod
    async def create_event(event: Event):
        result = await mongodb.collections["event"].insert_one(event.dict())
        return {"inserted_id": str(result.inserted_id)}

    @staticmethod
    async def get_all_event():
        cursor = mongodb.collections["event"].find({})
        return [EventResponseDTO(**event) async for event in cursor]

    


    @staticmethod
    async def get_school_events(school_id: str) -> List[EventResponseDTO]:
        try:
            cursor = mongodb.collections['event'].find({"school_id": DBRef(collection='schools', id=ObjectId(school_id))})
            return cursor
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"An error occurred while fetching events: {str(e)}")



    @staticmethod
    async def delete_event(event_id: str):
        _id = ObjectId(event_id)
        result = await mongodb.collections["event"].delete_one({"_id": _id})
        if result.deleted_count > 0:
            return "event deleted successfully from database"
        else:
            return "Error while deleting event"

    @staticmethod
    async def update_event(event_id: str, event: Event):
        _id = ObjectId(event_id)
        result = await mongodb.collections["event"].update_one({"_id": _id}, {"$set": event.dict()})
        if result.modified_count > 0:
            return "event updated successfully"
        else:
            return "Error updating event"