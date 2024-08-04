from typing import List
from app.models.event_model import Event
from app.dto.event_dto import EventDTO
from app.repositories.event_repo import EventRepository
from app.dto.event_dto import EventResponseDTO
from fastapi import HTTPException

class EventService:
    @staticmethod
    async def create_event(eventdto:EventDTO):
        event=Event(**eventdto.dict())
        result=await EventRepository.create_event(event)
        if result:
            return "Event created successfully"
        raise HTTPException(status_code=400, message="Event is not created")
        

    @staticmethod
    async def get_all_event():
        try:
            results = await EventRepository.get_all_event()
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching all events: {str(e)}")

    @staticmethod
    async def get_school_events(school_id: str) -> List[EventResponseDTO]:
        try:
            events = await EventRepository.get_school_events(school_id)
            return [EventResponseDTO(**event) async for event in events]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching school events: {str(e)}")

    @staticmethod
    async def delete_event(event_id: str):
        result = await EventRepository.delete_event(event_id)
        if result is None:
            raise HTTPException(
                status_code=400,
                detail=f"Event with id {event_id} not found"
            )
        return result

    @staticmethod
    async def update_event(event_id: str, event_dto: EventDTO):
        event = Event(**event_dto.dict())
        result = await EventRepository.update_event(event_id, event)
        if result is None:
            raise HTTPException(
                status_code=400,
                detail=f"Event with id {event_id} not found"
            )
        return result
