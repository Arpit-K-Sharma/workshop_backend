from fastapi import HTTPException
from app.config.db_config import mongodb
from app.models.feedback_model import Feedback
from app.dto.feedback_dto import FeedbackDTO,FeedbackResponseDTO
from bson import ObjectId,DBRef

class FeedbackRepo:
    @staticmethod
    async def get_feedback_by_id(feedback_by_id: str):
        try:
            response = mongodb.collections['feedback'].find({"feedback_by": DBRef(collection='feedback', id=ObjectId(feedback_by_id))})
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

    @staticmethod
    async def get_feedback_for_id(feedback_for_id: str):
        try:
            response = mongodb.collections['feedback'].find({"feedback_for": DBRef(collection='feedback', id=ObjectId(feedback_for_id))})
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def get_all_feedback():
        try:
            cursor = mongodb.collections['feedback'].find({})
            return cursor
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching feedback: {str(e)}")
    

    @staticmethod
    async def create_feedback(feedback: Feedback):
        await mongodb.collections['feedback'].insert_one(feedback.dict(exclude_unset=True))

    @staticmethod
    async def update_feedback(feedback_id: str, feedback: Feedback):
        _id = ObjectId(feedback_id)
        response = await mongodb.collections['feedback'].update_one({"_id": _id}, {"$set": feedback.dict(exclude_unset=True)})
        if response.modified_count:
            return {"feedback updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Feedback id not found")

    @staticmethod
    async def delete_feedback(feedback_id: str):
        _id = ObjectId(feedback_id)
        response = await mongodb.collections['feedback'].delete_one({"_id": _id})
        if response.deleted_count:
            return {"feedback deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Feedback id not found")

