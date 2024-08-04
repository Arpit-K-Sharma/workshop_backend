from fastapi import APIRouter
from app.dto.hof_dto import AchieverDTO,AchieverResponseDTO
from app.service.hof_service import HofService
from app.config.logger_config import get_logger
from app.utils.response_util import get_response


hof_route = APIRouter()
logger = get_logger()

@hof_route.get("/hof")
async def get_all_hof():
    logger.info("ENDPOINT CALLED: /HOF (GET) \n DATA RECEIVED:")
    response = await HofService.get_all_hofs()
    logger.info(f"RESPONSE SENT: RETREIVED {len(response)} hof")
    return get_response(status="success" , status_code=200, data=response)

@hof_route.get("/hof/{achiever_id}")
async def get_hof_by_id(achiever_id: str):
    logger.info(f"ENDPOINT CALLED: /HOF/{achiever_id} (GET) \n DATA RECEIVED:")
    response = await HofService.get_hof_by_achiever_id(achiever_id)
    logger.info(f"RESPONSE SENT: RETRIVED{response}")
    return get_response(status="success" , status_code=200 , data=response)

@hof_route.post("/hof")
async def create_hof(hof: AchieverDTO):
    logger.info(f"ENDPOINT CALLED: /HOF(POST) \n DATA SENT:{hof.dict()}")
    response = await HofService.create_hof(hof)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success", status_code=201, message=response)

@hof_route.put("/hof/{hof_id}")
async def update_hof(hof_id:str,hof:AchieverDTO):
    logger.info(f"ENDPOINT CALLED: /HOF/{hof_id} (PUT) \n DATA RECECIVED:")
    response = await HofService.update_hof(hof_id, hof)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success", status_code=200, message=response)

@hof_route.delete("/hof/{hof_id}")
async def delete_hof(hof_id:str):
    logger.info(f"ENDPOINT CALLED: /HOF/{hof_id} (DELETE)")
    response = await HofService.delete_hof(hof_id)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success", status_code=200,message=response)

