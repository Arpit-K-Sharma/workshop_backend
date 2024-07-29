from app.config.db_config import mongodb
from bson import ObjectId
from app.models.student_model import Student

class studentRepository:
    @staticmethod
    async def create_student(student: Student):
        result = await mongodb.collections["student"].insert_one(student.dict())
        return {"inserted_id": str(result.inserted_id)}
    
    @staticmethod
    async def get_all_student():
        cursor = mongodb.collections["student"].find({})
        student = []
        async for admin in cursor:
            admin["_id"] = str(admin["_id"])
            student.append(admin)
        return student
    
    @staticmethod
    async def read_student(student_id: str):
        _id = ObjectId(student_id)
        student = await mongodb.collections["student"].find_one({"_id": _id})
        if student:
            student["_id"] = str(student["_id"])
            return student
        return {"error": "student ID not found"}
        
    @staticmethod
    async def delete_student(student_id:str):
        _id=ObjectId(student_id)
        result=await mongodb.collections["student"].delete_one({"_id":_id})
        if result:
            return "Student deleted sucessfully from database"
        else:
            return "Error while deleting"
        
    @staticmethod
    async def update_student(student_id: str, student: Student):
        _id=ObjectId(student_id)
        result=await mongodb.collections["student"].update_one({"_id":_id},{"$set":student.dict()})
        if result.modified_count>0:
            return "student updated sucessfully"
        else:
            return "error updating student"