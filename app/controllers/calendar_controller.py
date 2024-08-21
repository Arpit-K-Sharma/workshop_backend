from fastapi import APIRouter
from app.config.logger_config import get_logger
from app.dto.calendar_dto import CalendarDTO, UpdateEventDTO
from app.service.calendar_service import CalendarService
from app.utils.response_util import get_response

logger = get_logger()
calendar_route = APIRouter()

@calendar_route.post("/calendar")
async def create_event(calendar : CalendarDTO):
    logger.info(f"ENDPOINT CALLED: /CALENDAR (POST) \n DATA SENT:{calendar.dict()}")
    response = await CalendarService.create_academic_event(calendar)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", message="Calendar Added Successfully", status_code=200)

@calendar_route.get("/calendar/{year}/{school_id}")
async def get_events_by_year(year : int, school_id : str):
    logger.info(f"ENDPOINT CALLED: /CALENDAR/{year}/{school_id} ")
    response = await CalendarService.get_events_by_year(year, school_id)
    logger.info(f"RESPONSE RECEIVED: {response}")
    return get_response(status="success", message="Calendar Received", status_code=200, data=response)

@calendar_route.get("/calendar/{year}/{school_id}/{month}")
async def get_events_by_month(year : int, school_id : str, month: int):
    logger.info(f"ENDPOINT CALLED: /CALENDAR/{year}/{school_id}/{month} ")
    response = await CalendarService.get_events_by_month(year, school_id, month)
    logger.info(f"RESPONSE RECEIVED: {response}")
    return get_response(status="success", message="Calendar Received", status_code=200, data=response)

@calendar_route.get("/calendar/{year}/{school_id}/{month}/{date}")
async def get_events_by_month(year : int, school_id : str, month: int, date: int):
    logger.info(f"ENDPOINT CALLED: /CALENDAR/{year}/{school_id}/{month}/{date} ")
    response = await CalendarService.get_events_by_date(year, school_id, month, date)
    logger.info(f"RESPONSE RECEIVED: {response}")
    return get_response(status="success", message="Calendar Received", status_code=200, data=response)

@calendar_route.put("/calendar/{year}/{school_id}/{month}/{date}/{eventID}")
async def update_events(year : int, school_id : str, month: int, date: int, eventID: str, updateDTO: UpdateEventDTO):
    logger.info(f"ENDPOINT CALLED: /CALENDAR/{year}/{school_id}/{month}/{date} ")
    response = await CalendarService.update_events(year, school_id, month, date, eventID, updateDTO)
    logger.info(f"RESPONSE RECEIVED: {response}")
    return get_response(status="success", message="Calendar Updated", status_code=200)
