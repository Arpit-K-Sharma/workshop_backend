from fastapi import APIRouter
from app.dto.course_dto import CourseDTO
from app.service.course_service import CourseService
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

course_route = APIRouter()
logger = get_logger()

@course_route.get("/course")
async def get_all_courses():
    logger.info("ENDPOINT CALLED : /COURSE (GET) \n DATA RECEIVED:")
    response = await CourseService.get_all_courses()  # Update method name here
    logger.info(f"RESPONSE SENT: RETRIEVED {len(response)} courses")
    return get_response(status="success", status_code=200, data=response)

@course_route.get("/course/{course_id}")
async def get_course(course_id: str): 
    logger.info("ENDPOINT CALLED: /COURSE (GET)")
    response = await CourseService.get_course(course_id)
    logger.info(f"RESPONSE SENT: RETRIEVED {response}")
    return get_response(status="success", status_code=200, data=response)

@course_route.post("/course")
async def create_course(course: CourseDTO):
    logger.info(f"ENDPOINT CALLED: /COURSE(POST)\n DATA SENT: {course.dict()}")
    response = await CourseService.create_course(course)
    logger.info(f"RESPONSE SENT: CREATE COURSE {response}")
    return get_response(status="success", status_code=200, message=response)

@course_route.delete("/course/{course_id}")
async def delete_course(course_id: str):
    logger.info(f"ENDPOINT CALLED: /COURSE/{course_id} (DELETE)")
    response = await CourseService.delete_course(course_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@course_route.put("/course/{course_id}")
async def update_course(course_id: str, coursedto: CourseDTO):
    logger.info(f"ENDPOINT CALLED: /COURSE/{course_id} (PUT)\n DATA SENT: {coursedto.dict()}")
    response = await CourseService.update_course(course_id, coursedto)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)
