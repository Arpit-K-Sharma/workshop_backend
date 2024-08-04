from fastapi import HTTPException
from app.config.db_config import mongodb
from bson import DBRef, ObjectId
from app.models.student_model import Student
from app.dto.student_dto import StudentDTO,StudentResponseDTO

class StudentRepository:
    @staticmethod
    async def create_student(student: Student):
        result = await mongodb.collections["student"].insert_one(student.dict())
        return result
    
    @staticmethod
    async def get_student_by_id(student_id: str):
        try:
            _id = ObjectId(student_id)
            result = await mongodb.collections["student"].find_one({"_id": _id})
            if result is None:
                raise HTTPException(status_code=404, detail="Student not found")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching the student: {str(e)}")
        
    @staticmethod
    async def get_students_by_school_id(school_id: str):
        try:
            result = mongodb.collections['student'].find({"school_id": DBRef(collection='school', id=ObjectId(school_id))})
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching the students: {str(e)}")

    @staticmethod
    async def get_all_student():
        try:
            cursor = mongodb.collections["student"].find({})
            return cursor
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve students: {str(e)}")
    
        
    @staticmethod
    async def delete_student(student_id: str):
        try:
            _id = ObjectId(student_id)
            result = await mongodb.collections["student"].delete_one({"_id": _id})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Student not found")
            return "Student deleted successfully from database"

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the student: {str(e)}")
        

    @staticmethod
    async def update_student(student_id: str, student: Student):
        try:
            _id = ObjectId(student_id)
            result = await mongodb.collections["student"].update_one({"_id": _id}, {"$set": student.dict(exclude_unset=True)})
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the student: {str(e)}")