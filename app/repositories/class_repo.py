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
    async def update_class(class_id: ObjectId, class_instance: dict):
        try:
            existing_class = await mongodb.collections["class"].find_one({"_id": class_id})
            if not existing_class:
                raise HTTPException(status_code=404, detail="Class not found")
            
            update_data ={}
            for key, value in class_instance.items():
                if value is not None:
                    update_data[key] = value

            result = await mongodb.collections["class"].update_one(
                {"_id": class_id},
                {"$set": update_data})
            
            if result.modified_count > 0:
                return "Class updated successfully"
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid class ID: {str(e)}")
        
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
    

    @staticmethod
    async def delete_class(class_id: str):
        try:
            # Convert class_id to ObjectId
            _id = ObjectId(class_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid class ID: {str(e)}")

        try:
            # Create a DBRef for the class
            class_ref = DBRef(collection="class", id=_id)

            # Delete the class
            class_result = await mongodb.collections["class"].delete_one({"_id": _id})
            if class_result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Class not found")

            # Delete associated students
            students_result = await mongodb.collections["student"].delete_many({"class_id": class_id})

            # Update teachers by removing this class from their schools.classes list
            teachers_result = await mongodb.collections["teacher"].update_many(
                {"schools.classes": class_ref},
                {"$pull": {"schools.$[].classes": class_ref}}
            )

            return {
                "message": "Class and associated data deleted successfully",
                "deleted_class_count": class_result.deleted_count,
                "deleted_students_count": students_result.deleted_count,
                "updated_teachers_count": teachers_result.modified_count
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
