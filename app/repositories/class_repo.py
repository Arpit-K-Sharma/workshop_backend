# app/repositories/class_repo.py
from typing import List
from bson import DBRef, ObjectId
from fastapi import HTTPException
from app.models.class_model import Class
from app.config.db_config import mongodb
from app.dto.class_dto import ClassResponseDTO

class ClassRepository:
    @staticmethod
    async def add_class(class_instance: Class):
        result = await mongodb.collections["class"].insert_one(class_instance.dict())
        return {"inserted_id": str(result.inserted_id)}

    @staticmethod
    async def update_class(class_id: str, class_instance: Class):
        try:
            _id = ObjectId(class_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid class ID: {str(e)}")
        
        result = await mongodb.collections["class"].update_one({"_id": _id}, {"$set": class_instance.dict()})
        if result.modified_count > 0:
            return "Class updated successfully"
        else:
            raise HTTPException(status_code=404, detail="Class not found or no changes made")

    @staticmethod
    async def get_class_by_school_id(school_id: str):
        try:
            _id = ObjectId(school_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid school ID: {str(e)}")
        
        school_ref = DBRef(collection="school", id=_id)
        cursor = mongodb.collections["class"].find({"school_id": school_ref})
        print(cursor)
        return await cursor.to_list(length=None)

    @staticmethod
    async def get_class_by_class_id(class_id: str):
        try:
            _id = ObjectId(class_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid class ID: {str(e)}")
        
        class_dict = await mongodb.collections["class"].find_one({"_id": _id})
        
        if not class_dict:
            raise HTTPException(status_code=404, detail="Class not found")
        
        # Fetch related documents
        student_refs = class_dict.get('students', [])
        teacher_refs = class_dict.get('teachers', [])
        course_refs = class_dict.get('courses', [])
        school_ref = class_dict.get('school_id')

        students = await ClassRepository.get_students_from_refs(student_refs)
        teachers = await ClassRepository.get_teachers_from_refs(teacher_refs)
        courses = await ClassRepository.get_courses_from_refs(course_refs)

        class_dict['students'] = students
        class_dict['teachers'] = teachers
        class_dict['courses'] = courses
        
        if school_ref:
            class_dict['school'] = await ClassRepository.get_school_from_ref(school_ref)
        
        return class_dict
    
    @staticmethod
    async def get_students_from_refs(student_refs: List[DBRef]):
        student_ids = [ObjectId(ref.id) for ref in student_refs]
        students = await mongodb.collections["student"].find({"_id": {"$in": student_ids}}).to_list(None)
        return students

    @staticmethod
    async def get_teachers_from_refs(teacher_refs: List[DBRef]):
        teacher_ids = [ObjectId(ref.id) for ref in teacher_refs]
        teachers = await mongodb.collections["teacher"].find({"_id": {"$in": teacher_ids}}).to_list(None)
        return teachers

    @staticmethod
    async def get_courses_from_refs(course_refs: List[DBRef]):
        course_ids = [ObjectId(ref.id) for ref in course_refs]
        courses = await mongodb.collections["course"].find({"_id": {"$in": course_ids}}).to_list(None)
        return courses

    @staticmethod
    async def get_school_from_ref(school_ref: DBRef):
        return await mongodb.collections["school"].find_one({"_id": ObjectId(school_ref.id)})
