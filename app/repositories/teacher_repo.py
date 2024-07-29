import os
import shutil
from fastapi import File, UploadFile
from app.config.db_config import mongodb
from bson import ObjectId
from app.models.teacher_model import Teacher

path=UPLOAD_DIR = "uploads"

class TeacherRepository:

    @staticmethod
    async def create_teacher(teacher:Teacher):
        result = await mongodb.collections["teacher"].insert_one(teacher.dict())
        return {"inserted_id": str(result.inserted_id)}

    # @staticmethod    
    # async def create_teacher(teacher:Teacher ,file: UploadFile = File(...)):
    #     result= await mongodb.collections["teacher"].insert_one(teacher.dict())
    #     file_location = f"{path}/{file.filename}"
    #     os.makedirs(os.path.dirname(file_location), exist_ok=True)
    #     with open(file_location, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)
    #     return result, {"info": f"file '{file.filename}' saved at '{file_location}'"}

    @staticmethod
    async def get_all_teacher():
        cursor = mongodb.collections["teacher"].find({})
        teacher = []
        async for admin in cursor:
            admin["_id"] = str(admin["_id"])
            teacher.append(admin)
        return teacher
    
    @staticmethod
    async def read_teacher(teacher_id: str):
        _id = ObjectId(teacher_id)
        teacher = await mongodb.collections["teacher"].find_one({"_id": _id})
        if teacher:
            teacher["_id"] = str(teacher["_id"])
            return teacher
        return {"error": "teacher ID not found"}
        
    @staticmethod
    async def delete_teacher(mentor_id:str):
        _id=ObjectId(mentor_id)
        result=await mongodb.collections["teacher"].delete_one({"_id":_id})
        if result:
            return "mentor deleted sucessfully from database"
        else:
            return "Error while deleting"
        
    @staticmethod
    async def update_teacher(mentor_id: str, teacher: Teacher):
        _id=ObjectId(mentor_id)
        result=await mongodb.collections["teacher"].update_one({"_id":_id},{"$set":teacher.dict()})
        if result.modified_count>0:
            return "mentor updated sucessfully"
        else:
            return "error updating mentor"
        
