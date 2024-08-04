from app.config.db_config import mongodb
from app.models.hof_model import Achiever
from app.dto.hof_dto import AchieverResponseDTO
from bson import DBRef, InvalidDocument, ObjectId
from fastapi import HTTPException


class HofRepo:
    @staticmethod
    async def get_all_hofs():
        try:
            cursor = mongodb.collections['hof'].find({})
            return [AchieverResponseDTO(**hof) async for hof in cursor if hof]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve HOF entries: {str(e)}")
    
    @staticmethod
    async def hof_by_achiever_id(achiever_id: str):
        try:
            response = await mongodb.collections['hof'].find_one({"achiever_id": DBRef(collection='achievers', id=ObjectId(achiever_id))})
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    
    @staticmethod
    async def create_hof(hof: Achiever):
        try:
            result = await mongodb.collections['hof'].insert_one(hof.dict(exclude_unset=True))
            return {"success": True, "hof_id": str(result.inserted_id)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create HOF entry: {str(e)}")
    
    @staticmethod
    async def update_hof(hof_id: str, hof: Achiever):
        _id = ObjectId(hof_id)
        response = await mongodb.collections['hof'].update_one({"_id": _id}, {"$set": hof.dict(exclude_unset=True)})
        if response.modified_count:
            return {"hof updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Hof id not found")
        
    @staticmethod
    async def delete_hof(hof_id: str):
        _id = ObjectId(hof_id)
        response = await mongodb.collections['hof'].delete_one({"_id": _id})
        if response.deleted_count:
            return {"hof deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Hof id not found")