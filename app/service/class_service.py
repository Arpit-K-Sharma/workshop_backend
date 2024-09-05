# app/service/class_service.py
from bson import ObjectId
from fastapi import HTTPException
from app.dto.course_dto import CourseResponseDTO
from app.dto.school_dto import SchoolResponseDTO
from app.dto.student_dto import StudentResponseDTO
from app.dto.teacher_dto import TeacherResponseDTO
from app.repositories.class_repo import ClassRepository
from app.models.class_model import Class
from app.dto.class_dto import ClassDTO, ClassResponseDTO

class ClassService:
    @staticmethod
    async def add_class(class_dto: ClassDTO):
        class_instance = Class(**class_dto.dict(exclude_unset=True))
        result = await ClassRepository.add_class(class_instance)
        if result:
            return "Class added successfully"
        raise HTTPException(status_code=400, detail="Class is not added")

    @staticmethod
    async def update_class(class_id: str, class_dto: dict):
        try:
            _id = ObjectId(class_id)
            result = await ClassRepository.update_class(_id, class_dto)
            if result is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Class with id {class_id} not found"
                )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the student: {str(e)}")

    @staticmethod
    async def get_class_by_school_id(school_id: str):
        results = await ClassRepository.get_class_by_school_id(school_id)
        
        return [ClassDTO(**class_instance) for class_instance in results]
    
    @staticmethod
    async def get_class_by_class_id(class_id: str):
        result = await ClassRepository.get_class_by_class_id(class_id)
        return ClassResponseDTO(
            id=str(result['_id']),
            class_name=result['class_name'],
            students=[StudentResponseDTO(**student) for student in result['students']],
            teachers=[TeacherResponseDTO(**teacher) for teacher in result['teachers']],
            courses=[CourseResponseDTO(**course) for course in result['courses']],
            school_id=result['school_id']
        )
    
    @staticmethod
    async def delete_class(class_id: str):
        result = await ClassRepository.delete_class(class_id)
        if result:
            return "Class Deleted Successfully !!!"
        raise HTTPException(status_code=404, detail=f"class with id {class_id} not found")
    