from fastapi import HTTPException
from app.config.db_config import mongodb
from bson import DBRef, ObjectId
from app.models.student_model import Student
from app.dto.student_dto import StudentDTO,StudentResponseDTO
from app.utils.password_utils import get_password_hash

class StudentRepository:
    @staticmethod
    async def create_student(student: Student):
        result = await mongodb.collections["student"].insert_one(student)
        return result
    
    @staticmethod
    async def get_student_by_id(student_id: str):
        try:
            _id = ObjectId(student_id)
            result = await mongodb.collections["student"].find_one({"_id": _id})
            print(result)
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
    async def update_student(student_id: ObjectId, student: dict):
        try:
            existing_student = await mongodb.collections["student"].find_one({"_id": student_id})
            if not existing_student:
                raise HTTPException(status_code=404, detail="Student not found")
            
            # Create an update dictionary with only the fields that are set
            update_data ={}
            for key, value in student.items():
                if value is not None:
                    update_data[key] = value
            
            
            result = await mongodb.collections["student"].update_one(
                {"_id": student_id},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return "Student Updated Successfully"
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the student: {str(e)}")
        
    
    @staticmethod
    async def get_student_by_email(email: str):
        try:
            student = await mongodb.collections["student"].find_one({"student_email": email})
            return student
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching the students: {str(e)}")
        
    @staticmethod
    async def change_password(student_id:str, new_password: str):
        try:
            new_password_hashed = get_password_hash(new_password)
            result = await mongodb.collections["student"].update_one(
                {"_id": ObjectId(student_id)},
                {"$set": {"password": new_password_hashed, "is_password_changed": True}}
            )            
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the password:  {str(e)}")
