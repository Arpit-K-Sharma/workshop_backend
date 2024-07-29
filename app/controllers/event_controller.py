from fastapi import APIRouter
from app.models.event_model import Event
from app.service.event_service import eventService

event_route = APIRouter()

event_route.get("/event")
async def list_events(event:Event):
    response = await eventService.list_event(event)
    return response
@event_route.get("/event")
async def read_event():
    response =await eventService.read_event()  
    return response
    
@event_route.post("/event")
async def post_event(event:Event):
    response =await eventService.create_event(event)
    return response
    
@event_route.delete("/event/{event_id}")
async def del_event(event_id:str):
    response = await eventService.delete_event(event_id)
    return response
@event_route.put("/event/{event_id}")
async def put_event(event_id:str, event:Event):
    response = await eventService.update_event(event_id, event)
    return response