from fastapi import APIRouter, Depends, HTTPException, Response
from app.dto.event_dto import EventDTO
from app.service.event_service import EventService
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

event_route = APIRouter()
logger = get_logger()

@event_route.get("/event")
async def get_all_event():
    logger.info("ENDPOINT CALLED : /EVENT (GET) \n DATA RECEIVED:")
    response = await EventService.get_all_event()
    logger.info(f"RESPONSE SENT: RETRIEVED {len(response)} events")
    return get_response(status="success", status_code=200, data=response)

@event_route.get("/event/{school_id}")
async def get_event_by_school_Id(school_id: str):
    logger.info("ENDPOINT CALLED: /EVENT (GET)")
    response = await EventService.get_school_events(school_id)
    logger.info(f"RESPONSE SENT: RETRIEVED {response}")
    return get_response(status="success", status_code=200, data=response)

@event_route.post("/event")
async def create_event(event: EventDTO = Depends(EventDTO.as_form)):
    # print(event.school_name)
    # logger.info(f"ENDPOINT CALLED: /EVENT (POST)\n DATA SENT: {event.dict()}")
    response = await EventService.create_event(event)
    # logger.info(f"RESPONSE SENT: CREATED EVENT {response}")
    return get_response(status="success", status_code=201, message=response)

@event_route.delete("/event/{event_id}")
async def delete_event(event_id: str):
    logger.info(f"ENDPOINT CALLED: /EVENT/{event_id} (DELETE)")
    response = await EventService.delete_event(event_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@event_route.put("/event/{event_id}")
async def update_event(event_id: str, event_dto: EventDTO):
    logger.info(f"ENDPOINT CALLED: /EVENT/{event_id} (PUT)\n DATA SENT: {event_dto.dict()}")
    response = await EventService.update_event(event_id, event_dto)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)
