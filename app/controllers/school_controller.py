from fastapi import APIRouter
from app.dto.school_dto import SchoolDTO
from app.service.school_service import SchoolService
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

school_route=APIRouter()
logger=get_logger()

@school_route.get("/school")
async def list_school():
    logger.info("ENDPOINT CALLED : /SCHOOL (GET) \n DATA RECEIVED:")
    response = await SchoolService.get_all_school()  # Updated method name
    logger.info(f"RESPONSE SENT: RETRIVED {len(response)} school")
    return get_response(status="success", status_code=200, data=response)

@school_route.get("/school/{school_id}")
async def get_school(school_id:str):
    logger.info("ENDPOINT CALLED: /SCHOOL (GET)")
    response=await SchoolService.get_school(school_id)
    logger.info(f"RESPONSE SENT: RETRIVED {response}")
    return get_response (status="success",status_code=200,data=response)

@school_route.post("/school")
async def create_school(school:SchoolDTO):
    logger.info(f"ENDPOINT CALLED: /SCHOOL(POST)\n DATA SENT:{school.dict}")
    response =await SchoolService.create_school(school)
    logger.info(f"RESPONSE SENT:CREATE SCHOOL{response}")
    return get_response (status="success", status_code=200, message=response)

@school_route.delete("/school/{school_id}")
async def delete_school(school_id: str):
    logger.info(f"ENDPOINT CALLED: /SCHOOL/{school_id} (DELETE)")
    response = await SchoolService.delete_school(school_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)


@school_route.put("/school/{school_id}")
async def update_school(school_id: str, schooldto: SchoolDTO):
    logger.info(f"ENDPOINT CALLED: /SCHOOL/{school_id} (PUT)\n DATA SENT: {schooldto.dict()}")

    response = await SchoolService.update_school(school_id, schooldto)
    
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)





