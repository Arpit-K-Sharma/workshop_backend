from app.models.feedback_model import Feedback
from app.repositories.feedback_repo import FeedbackRepo
from app.dto.feedback_dto import FeedbackDTO, FeedbackResponseDTO
from fastapi import HTTPException

class FeedbackService:
    @staticmethod
    async def get_all_feedback():
        try:
            results = await FeedbackRepo.get_all_feedback()
            return [FeedbackResponseDTO(**feedback) async for feedback in results if feedback]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching feedback: {str(e)}")
    
    @staticmethod
    async def get_feedback_by_id(feedback_by_id: str):
        try:
            result = await FeedbackRepo.get_feedback_by_id(feedback_by_id)
            return [FeedbackResponseDTO(**by_id) async for by_id in result]
        except Exception:
            raise HTTPException(status_code=404, detail="No feedback found by feedback by id")
        
    @staticmethod
    async def get_feedback_for_id(feedback_for_id: str):
        try:
            result = await FeedbackRepo.get_feedback_for_id(feedback_for_id)
            return [FeedbackResponseDTO(**for_id) async for for_id in result]
        except Exception:
            raise HTTPException(status_code=404, detail="No feedback found by feedback for id")
    
    
    @staticmethod
    async def create_feedback(feedbackdto: FeedbackDTO):
        try:
            feedback = Feedback(**feedbackdto.dict())
            await FeedbackRepo.create_feedback(feedback)
            return {"message": "Feedback created successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while creating feedback: {str(e)}")

    
    @staticmethod
    async def update_feedback(feedback_id: str, feedbackdto: FeedbackDTO):
        feedback = Feedback(**feedbackdto.dict())
        result = await FeedbackRepo.update_feedback(feedback_id, feedback)
        if result:
            return {"message": "Feedback updated successfully"}
        raise HTTPException(status_code=500, detail="Failed to update feedback")
    
    @staticmethod
    async def delete_feedback(feedback_id: str):
        result = await FeedbackRepo.delete_feedback(feedback_id)
        if result:
            return {"message": "Feedback deleted successfully"}
        raise HTTPException(status_code=500, detail="Failed to delete feedback")