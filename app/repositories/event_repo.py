from app.config.db_config import mongodb
from bson import ObjectId
from app.models.event_model import Event

class eventRepository:
    @staticmethod
    async def create_event(event: Event):
        result = await mongodb.collections["event"].insert_one(event.dict())
        return {"inserted_id": str(result.inserted_id)}
    
    @staticmethod
    async def get_all_event():
        cursor = mongodb.collections["event"].find({})
        event = []
        async for admin in cursor:
            admin["_id"] = str(admin["_id"])
            event.append(admin)
        return event
    
    @staticmethod
    async def read_event(event_id: str):
        _id = ObjectId(event_id)
        event = await mongodb.collections["event"].find_one({"_id": _id})
        if event:
            event["_id"] = str(event["_id"])
            return event
        return {"error": "event ID not found"}
        
    @staticmethod
    async def delete_event(event_id:str):
        _id=ObjectId(event_id)
        result=await mongodb.collections["event"].delete_one({"_id":_id})
        if result:
            return "Event deleted sucessfully from database"
        else:
            return "Error while deleting"
        
    @staticmethod
    async def update_event(event_id: str, event: Event):
        _id=ObjectId(event_id)
        result=await mongodb.collections["event"].update_one({"_id":_id},{"$set":event.dict()})
        if result.modified_count>0:
            return "event updated sucessfully"
        else:
            return "error updating event"