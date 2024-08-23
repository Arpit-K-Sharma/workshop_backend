# app/controller/class_controller.py
from fastapi import APIRouter
from app.dto.class_dto import ClassDTO
from app.service.class_service import ClassService
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

class_route = APIRouter()
logger = get_logger()

@class_route.post("/class")
async def add_class(class_dto: ClassDTO):
    logger.info(f"ENDPOINT CALLED: /CLASS (POST)\n DATA SENT: {class_dto.dict()}")
    response = await ClassService.add_class(class_dto)
    logger.info(f"RESPONSE SENT: ADD CLASS {response}")
    return get_response(status="success", status_code=201, message=response)

@class_route.put("/class/{class_id}")
async def update_class(class_id: str, class_dto: ClassDTO):
    logger.info(f"ENDPOINT CALLED: /CLASS/{class_id} (PUT)\n DATA SENT: {class_dto.dict()}")
    response = await ClassService.update_class(class_id, class_dto)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@class_route.get("/class/school/{school_id}")
async def get_class_by_school_id(school_id: str):
    logger.info(f"ENDPOINT CALLED: /CLASS/SCHOOL/{school_id} (GET)")
    response = await ClassService.get_class_by_school_id(school_id)
    logger.info(f"RESPONSE SENT: RETRIEVED {len(response)} classes")
    return get_response(status="success", status_code=200, data=response)

@class_route.get("/class/{class_id}")
async def get_class_by_class_id(class_id:str):
    logger.info(f"ENDPOINT CALLED: /CLASS/{class_id} (GET)")
    response = await ClassService.get_class_by_class_id(class_id)
    print(response)
    logger.info("RESPONSE SENT SUCCESSFULLY")
    return get_response(status="success",status_code=200,data=response)


