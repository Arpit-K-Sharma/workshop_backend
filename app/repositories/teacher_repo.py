import os
import shutil
from fastapi import File, HTTPException, UploadFile
from app.config.db_config import mongodb
from bson import ObjectId
from app.models.teacher_model import Teacher
from app.dto.teacher_dto import TeacherDTO,TeacherResponseDTO

class TeacherRepository:

    @staticmethod
    async def create_teacher(teacher:Teacher):
        result = await mongodb.collections["teacher"].insert_one(teacher.dict())
        return {"inserted_id": str(result.inserted_id)}

    
    @staticmethod
    async def get_teacher_by_id(teacher_id:str):
        _id=ObjectId(teacher_id)
        result=await mongodb.collections["teacher"].find_one({"_id":_id})
        return result
    
    @staticmethod
    async def get_all_teacher():
        try:
            cursor = mongodb.collections["teacher"].find({})
            return cursor
        except Exception as e:
            raise HTTPException(status_code=404, detail= f"Failed to retrieve teachers: {str(e)}")
        
    @staticmethod
    async def delete_teacher(teacher_id: str):
        try:
            _id = ObjectId(teacher_id)
            result = await mongodb.collections["teacher"].delete_one({"_id": _id})
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the teacher: {str(e)}")
        
    @staticmethod
    async def update_teacher(teacher_id: str, teacher: Teacher):
        try:
            _id = ObjectId(teacher_id)
            result = await mongodb.collections["teacher"].update_one(
                {"_id": _id},
                {"$set": teacher.dict(exclude_unset=True)}
            )
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the teacher: {str(e)}")
