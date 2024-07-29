import os
import shutil
from fastapi import File, UploadFile
from app.config.db_config import mongodb
from bson import ObjectId
from app.models.school_model import School

path=UPLOAD_DIR = "uploads"

class SchoolRepository:

    @staticmethod
    async def create_school(school:School):
        result = await mongodb.collections["school"].insert_one(school.dict())
        return {"inserted_id": str(result.inserted_id)}

    # @staticmethod    
    # async def create_school(school:school ,file: UploadFile = File(...)):
    #     result= await mongodb.collections["school"].insert_one(school.dict())
    #     file_location = f"{path}/{file.filename}"
    #     os.makedirs(os.path.dirname(file_location), exist_ok=True)
    #     with open(file_location, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)
    #     return result, {"info": f"file '{file.filename}' saved at '{file_location}'"}

    @staticmethod
    async def get_all_school():
        cursor = mongodb.collections["school"].find({})
        school = []
        async for admin in cursor:
            admin["_id"] = str(admin["_id"])
            school.append(admin)
        return school
    
    @staticmethod
    async def read_school(school_id: str):
        _id = ObjectId(school_id)
        school = await mongodb.collections["school"].find_one({"_id": _id})
        if school:
            school["_id"] = str(school["_id"])
            return school
        return {"error": "school ID not found"}
        
    @staticmethod
    async def delete_school(mentor_id:str):
        _id=ObjectId(mentor_id)
        result=await mongodb.collections["school"].delete_one({"_id":_id})
        if result:
            return "mentor deleted sucessfully from database"
        else:
            return "Error while deleting"
        
    @staticmethod
    async def update_school(mentor_id: str, school: School):
        _id=ObjectId(mentor_id)
        result=await mongodb.collections["school"].update_one({"_id":_id},{"$set":school.dict()})
        if result.modified_count>0:
            return "mentor updated sucessfully"
        else:
            return "error updating mentor"
        
