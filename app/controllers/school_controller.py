from typing import Optional, Union
from fastapi import APIRouter, BackgroundTasks, File, UploadFile
from app.dto.school_dto import SchoolDTO
from app.service.school_service import SchoolService
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

school_route=APIRouter()
logger=get_logger()

@school_route.get("/school")
async def get_all_school():
    logger.info("ENDPOINT CALLED : /SCHOOL (GET) \n DATA RECEIVED:")
    response = await SchoolService.get_all_school() 
    logger.info(f"RESPONSE SENT: RETRIVED {len(response)} school")
    return get_response(status="success", status_code=200, data=response)

@school_route.get("/school/{school_id}")
async def get_school(school_id:str):
    logger.info("ENDPOINT CALLED: /SCHOOL (GET)")
    response=await SchoolService.get_school(school_id)
    logger.info(f"RESPONSE SENT: RETRIVED {response}")
    return get_response (status="success",status_code=200,data=response)

@school_route.get("/student_per_course")
async def get_course_student_per_school():
    logger.info("ENDPOINT CALLED : /SCHOOL/STUDENT_PER_COURSE (GET) \n DATA RECEIVED:")
    response = await SchoolService.get_students_per_course()
    return get_response(status="success", status_code=200, data=response)



@school_route.post("/school")
async def create_school(schooldto: SchoolDTO):
    logger.info(f"ENDPOINT CALLED: /SCHOOL(POST)\n DATA SENT:{schooldto.dict()}")
    response = await SchoolService.create_school(schooldto)
    logger.info("School creation task added to background tasks")
    return get_response(status="success", status_code=202, message="School creation successfully")




@school_route.delete("/school/{school_id}")
async def delete_school(school_id: str):
    logger.info(f"ENDPOINT CALLED: /SCHOOL/{school_id} (DELETE)")
    response = await SchoolService.delete_school(school_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)


@school_route.put("/school/{school_id}")
async def update_school(school_id: str, schooldto: SchoolDTO):
    print(schooldto)
    logger.info(f"ENDPOINT CALLED: /SCHOOL/{school_id} (PUT)\n DATA SENT: {schooldto.dict()}")
    response = await SchoolService.update_school(school_id, schooldto)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)







