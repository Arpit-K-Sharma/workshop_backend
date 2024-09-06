# app/service/class_service.py
import base64
from fastapi import HTTPException
from app.dto.course_dto import CourseResponseDTO
from app.dto.school_dto import SchoolResponseDTO
from app.dto.student_dto import StudentResponseDTO
from app.dto.teacher_dto import TeacherResponseDTO
from app.repositories.class_repo import ClassRepository
from app.models.class_model import Class
from app.dto.class_dto import ClassDTO, ClassResponseDTO
from app.service.student_service import StudentService

class ClassService:
    @staticmethod
    async def add_class(class_dto: ClassDTO):
        class_instance = Class(**class_dto.dict(exclude_unset=True))
        result = await ClassRepository.add_class(class_instance)
        if result:
            return "Class added successfully"
        raise HTTPException(status_code=400, detail="Class is not added")

    @staticmethod
    async def update_class(class_id: str, class_dto: ClassDTO):
        class_instance = Class(**class_dto.dict())
        result = await ClassRepository.update_class(class_id, class_instance)
        if result is None:
            raise HTTPException(
                status_code=400,
                detail=f"Class with id {class_id} not found"
            )
        return result

    @staticmethod
    async def get_class_by_school_id(school_id: str):
        results = await ClassRepository.get_class_by_school_id(school_id)
        
        return [ClassDTO(**class_instance) for class_instance in results]
    
    @staticmethod
    async def get_class_by_class_id(class_id: str):
        result = await ClassRepository.get_class_by_class_id(class_id)
        class_response_dto =  ClassResponseDTO(
            id=str(result['_id']),
            class_name=result['class_name'],
            students=[StudentResponseDTO(**student) for student in result['students']],
            teachers=[TeacherResponseDTO(**teacher) for teacher in result['teachers']],
            courses=[CourseResponseDTO(**course) for course in result['courses']],
            school_id=result['school_id']
        )
        students = class_response_dto.students

        profile_pictures = await StudentService.download_profile_pictures(students)

        students_with_pp = []
    
        # Iterate over each student
        for student in students:
            student_data = student.dict()  # Convert Pydantic model to dictionary

            # Check if the student has a profile_picture field
            if student.profile_picture:
                # Extract the profile picture file name
                profile_picture_filename = student.profile_picture
                
                # Find the profile picture content from the profile_pictures list
                profile_picture_content = next(
                    (pic[profile_picture_filename] for pic in profile_pictures if profile_picture_filename in pic), None
                )

                # If the profile picture content is found, encode it as Base64 and add it to the student data
                if profile_picture_content:
                    student_data['profile_picture_content'] = base64.b64encode(profile_picture_content).decode('utf-8')

            # Append the student data to the response list
            students_with_pp.append(student_data)
        
        class_response_dto.students = students_with_pp
        return class_response_dto
    
    @staticmethod
    async def delete_class(class_id: str):
        result = await ClassRepository.delete_class(class_id)
        if result:
            return "Class Deleted Successfully !!!"
        raise HTTPException(status_code=404, detail=f"class with id {class_id} not found")
    