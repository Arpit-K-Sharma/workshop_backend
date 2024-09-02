from fastapi import APIRouter, Request
from app.dto.teacher_dto import TeacherDTO, TeacherResponseDTO
from app.service.teacher_service import TeacherService
from app.models import teacher_model
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

logger = get_logger()

teacher_route = APIRouter()

@teacher_route.get("/teacher")
async def get_all_teachers():
    logger.info(f"ENDPOINT CALLED:/TEACHER/(GET)\n DATA RECEIVED:")
    response = await TeacherService.get_all_teachers()
    logger.info(f"RESPONSE SENT:RETRIEVED{response}")
    return get_response(status="success",status_code=200,data=response)

@teacher_route.get("/teacher/{teacher_id}")
async def get_teacher_by_id(teacher_id: str):
    logger.info(f"ENDPOINT CALLED:/TEACHER/(GET)\n DATA RECIEVED")
    response = await TeacherService.get_teacher_by_id(teacher_id)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,data=response)

@teacher_route.post("/teacher")
async def create_teacher(teacher: TeacherDTO):
    logger.info(f"ENDPOINT CALLED:/TEACHER/(POST)\n DATA RECEIVED")
    response = await TeacherService.create_teacher(teacher)
    logger.info(F"RESPONSE SENT:RETRIEVED{response}")
    return get_response(status="success",status_code=200,message=response)

@teacher_route.get("/teacher/classes/{teacher_id}")
async def get_numOfClasses_students(teacher_id: str):
    logger.info(f"ENDPOINT CALLED:/TEACHER/CLASSES/(GET)\n DATA RECIEVED")
    response = await TeacherService.get_numOfClasses_students(teacher_id)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,data=response)
        

@teacher_route.delete("/teacher/{teacher_id}")
async def del_teacher(teacher_id: str):
    logger.info(f"ENDPOINT CALLED:/TEACHER/(DELETE)\n DATA RECEIVED")
    response = await TeacherService.delete_teacher(teacher_id)
    logger.info(F"RESPONSE SENT:RETRIEVED{response}")
    return get_response(status="success",status_code=200,message=response)
    
@teacher_route.put("/teacher/{teacher_id}")
async def update_teacher(teacher_id: str,teacher_dto:TeacherDTO):
    logger.info(f"ENDPOINT CALLED:/TEACHER/(UPDATE)\n DATA SENT:{teacher_dto.dict()}")
    response = await TeacherService.update_teacher(teacher_id,teacher_dto)
    logger.info(F"RESPONSE SENT:RETRIEVED{response}")
    return get_response(status="success",status_code=200,message=response)
