import asyncio
from datetime import datetime
from typing import List
import uuid
from app.models.event_model import Event
from app.dto.event_dto import EventDTO
from app.repositories.event_repo import EventRepository
from app.dto.event_dto import EventResponseDTO
from fastapi import HTTPException

from app.service.file_service import FileService
from app.service.school_service import SchoolService

class EventService:
    
    @staticmethod
    def create_filename(school_code: str, original_filename: str):
        random_uuid = uuid.uuid4().hex
        file_extension = original_filename.split('.')[-1]
        return f"{school_code}_{random_uuid}.{file_extension}"

    @staticmethod
    async def create_event(eventdto: EventDTO):
        try:
            # Process file uploads
            uploaded_fileNames = []
            if eventdto.gallery:
                school_data = await SchoolService.get_school(eventdto.school_id)
                school_code = school_data.school_code

                for file in eventdto.gallery:
                    new_filename = EventService.create_filename(school_code, file.filename)
                    file.filename = new_filename
                    uploaded_fileNames.append(new_filename)

                # Start the file saving process asynchronously without waiting
                asyncio.create_task(FileService.save_uploaded_files(eventdto.gallery))

                print("File saving started in the background")

            # Create the event
            event = Event(**eventdto.dict(exclude={'gallery'}))
            event.gallery = uploaded_fileNames

            # Start the event creation process asynchronously
            create_event_task = asyncio.create_task(EventRepository.create_event(event))

            # Return immediately without waiting for the event creation to complete
            return "Event creation process started"

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while initiating the event creation: {str(e)}")

        

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

    @staticmethod
    async def get_all_event():
        try:
            events = await EventRepository.get_all_event()
            print(events)
            return [await EventService.populate_file_details(event) for event in events]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching all events: {str(e)}")

    @staticmethod
    async def get_school_events(school_id: str) -> List[EventResponseDTO]:
        try:
            events = await EventRepository.get_school_events(school_id)
            return [await EventService.populate_file_details(event) async for event in events]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching school events: {str(e)}")

    @staticmethod
    async def populate_file_details(event: dict) -> EventResponseDTO:
        # print(event)
        gallery = event['gallery']
        if gallery and isinstance(gallery[0], str): # Check if gallery contains only filenames
            file_details = await FileService.download_files(gallery)
            event['gallery'] = file_details
        return EventResponseDTO(**event)

