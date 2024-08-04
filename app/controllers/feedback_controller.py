from fastapi import APIRouter
from app.dto.feedback_dto import FeedbackDTO,FeedbackResponseDTO
from app.service.feedback_service import FeedbackService
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

feedback_route = APIRouter()
logger = get_logger()

@feedback_route.get("/feedback")
async def get_all_feedback():
    logger.info("ENDPOINT CALLED: /FEEDBACK (GET) \n DATA RECEIVED:")
    response = await FeedbackService.get_all_feedback()
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, data=response)

@feedback_route.get("/feedback/by/{feedback_by_id}")
async def get_feedback_by_id(feedback_by_id: str):
    logger.info(f"ENDPOINT CALLED: /FEEDBACK/BY/{feedback_by_id} (GET) \n DATA RECEIVED:")
    response = await FeedbackService.get_feedback_by_id(feedback_by_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, data=response)

@feedback_route.get("/feedback/for/{feedback_for_id}")
async def get_feedback_for_id(feedback_for_id: str):
    logger.info(f"ENDPOINT CALLED: /FEEDBACK/FOR/{feedback_for_id} (GET) \n DATA RECEIVED:")
    response = await FeedbackService.get_feedback_for_id(feedback_for_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, data=response)

@feedback_route.post("/feedback")
async def create_feedback(feedback: FeedbackDTO):
    logger.info(f"ENDPOINT CALLED: /FEEDBACK (POST) \n DATA SENT: {feedback.dict()}")
    response = await FeedbackService.create_feedback(feedback)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=201, message=response)

@feedback_route.put("/feedback/{feedback_id}")
async def update_feedback(feedback_id: str, feedback: FeedbackDTO):
    logger.info(f"ENDPOINT CALLED: /FEEDBACK/{feedback_id} (PUT) \n DATA SENT: {feedback.dict()}")
    response = await FeedbackService.update_feedback(feedback_id, feedback)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@feedback_route.delete("/feedback/{feedback_id}")
async def delete_feedback(feedback_id: str):
    logger.info(f"ENDPOINT CALLED: /FEEDBACK/{feedback_id} (DELETE)")
    response = await FeedbackService.delete_feedback(feedback_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)
