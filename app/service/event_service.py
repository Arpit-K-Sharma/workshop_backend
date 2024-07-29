from app.repositories.event_repo import eventRepository
from app.models.event_model import Event
class eventService:
    @staticmethod
    async def create_event(event: Event):
        result = await eventRepository.create_event(event)
        return result
    
    @staticmethod
    async def read_event():
        result = await eventRepository.get_all_event()
        return result
    
    @staticmethod
    async def delete_event(event_id:str):
        result= await eventRepository.delete_event(event_id)
        return result
    @staticmethod
    async def update_event(event_id: str, event: Event):
        result= await eventRepository.update_event(event_id, event)
        return result