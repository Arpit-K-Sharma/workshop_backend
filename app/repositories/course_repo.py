from bson import ObjectId
from bson.json_util import dumps, loads
from app.models.course_model import Course
from app.config.db_config import mongodb
from app.dto.course_dto import CourseDTO, CourseResponseDTO
from fastapi import HTTPException

class CourseRepository:
    @staticmethod
    async def create_course(course: Course):
        result = await mongodb.collections["course"].insert_one(course.dict())
        return {"inserted_id": str(result.inserted_id)}

    @staticmethod
    async def get_all_courses():
        cursor = mongodb.collections["course"].find({})
        courses = []
        async for course in cursor:
            course["_id"] = str(course["_id"])
            courses.append(course)
        return courses

    @staticmethod
    async def get_course(course_id: str):
        _id = ObjectId(course_id)       
        course = await mongodb.collections["course"].find_one({"_id": _id})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return CourseResponseDTO(**course)
        

    @staticmethod
    async def delete_course(course_id: str):
        try:
            _id = ObjectId(course_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid course ID: {str(e)}")
        
        result = await mongodb.collections["course"].delete_one({"_id": _id})
        if result.deleted_count > 0:
            return "Course deleted successfully from database"
        else:
            raise HTTPException(status_code=404, detail="Course not found")
        
    @staticmethod
    async def update_course(course_id: str, course: Course):
        try:
            _id = ObjectId(course_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid course ID: {str(e)}")
        
        result = await mongodb.collections["course"].update_one({"_id": _id}, {"$set": course.dict()})
        if result.modified_count > 0:
            return "Course updated successfully"
        else:
            raise HTTPException(status_code=404, detail="Course not found or no changes made")
