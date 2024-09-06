import asyncio
import configparser
from typing import List
import uuid
from bson import ObjectId
from fastapi import HTTPException
from app.repositories.teacher_repo import TeacherRepository
from app.service.class_service import ClassService
from app.models.teacher_model import Teacher, SchoolInfo
from app.dto.teacher_dto import TeacherResponseDTO, TeacherDTO
from app.service.file_service import FileService
from app.utils.password_utils import get_password_hash

config = configparser.ConfigParser()
config.read('config.ini')

class TeacherService:
    @staticmethod
    async def create_teacher(teacherdto: TeacherDTO):
        file_name = None
        
        # Check if profile picture is provided
        if teacherdto.profile_picture:
            # Generate filename
            file_name = await TeacherService.create_filename(teacherdto.name, teacherdto.profile_picture.filename)

            folder = config['aws'][f'aws_s3_image_path']
            file_path = f"{folder}/{file_name}"
            file = teacherdto.profile_picture
            file_content = await file.read()

            # Upload file asynchronously
            asyncio.create_task(FileService.upload_to_s3(file_content, file_path))

        teacher_data = teacherdto.dict(exclude_unset=True, exclude = {'profile_picture'})
        teacher=Teacher(**teacher_data)
        teacher.profile_picture = file_name

        # Password hashing
        teacher.password = get_password_hash(teacher.password)
        result = await TeacherRepository.create_teacher(teacher)
        
        if result:
            return "Teacher Created Successfully"
        
        raise HTTPException(status_code=400, detail="Could not create teacher")

    
    @staticmethod
    async def create_filename(teacher_name: str, original_file_name: str) -> str:
        try:
            # Generate a random 5-character UUID
            random_uuid = str(uuid.uuid4())[:5]
            # Replace spaces with underscores in the student's name
            sanitized_student_name = teacher_name.replace(" ", "_")
            # Extract the file extension from the original file name
            file_extension = original_file_name.split('.')[-1]
            # Create the unique filename
            unique_filename = f"{sanitized_student_name}_{random_uuid}.{file_extension}"
            return unique_filename
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while generating the filename: {str(e)}")


    @staticmethod
    async def get_teacher_by_id(teacher_id: str):
        try:
            result = await TeacherRepository.get_teacher_by_id(teacher_id)
            if not result:
                raise HTTPException(status_code=404, detail=f"Teacher with id {teacher_id} not found")
            return TeacherResponseDTO(**result)
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while fetching the teacher: {str(e)}")
        
    
    @staticmethod
    async def get_numOfClasses_students(teacher_id: str):
        try:
            teacher_dict = {
                "schoolCount": 0,
                "classCount": 0,
                "studentCount": 0,
            }

            result = await TeacherRepository.get_teacher_by_id(teacher_id)
            if not result:
                raise HTTPException(status_code=404, detail=f"Teacher with id {teacher_id} not found")

            teacherResponse = TeacherResponseDTO(**result)
            for response in teacherResponse.schools:
                teacher_dict["schoolCount"] += 1
                for perClass in response.classes:
                    teacher_dict["classCount"] += 1
                    student = await ClassService.get_class_by_class_id(perClass)
                    teacher_dict["studentCount"] += len(student.students)

            return teacher_dict
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching the teacher: {str(e)}")
            
        
    @staticmethod
    async def get_all_teachers():
        try:
            result = await TeacherRepository.get_all_teacher()
            return [TeacherResponseDTO(**teacher) async for teacher in result]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while fetching all teachers: {str(e)}")
    
    @staticmethod
    async def delete_teacher(teacher_id: str):
        try:
            result = await TeacherRepository.delete_teacher(teacher_id)
            if result:
                return {"message": "Teacher deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Teacher not found")
        except Exception as e:
            # For any other unexpected errors
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while deleting the teacher: {str(e)}"
            )
    
    @staticmethod
    async def update_teacher(teacher_id: str, teacher_dto: dict):
        try:
            _id = ObjectId(teacher_id)
            result = await TeacherRepository.update_teacher(_id, teacher_dto)
            
            if not result:
                raise HTTPException(status_code=404, detail="Teacher not found")
            return result

        except Exception as e:
            # For any other unexpected errors
            raise HTTPException(status_code=500,detail=f"An error occurred while updating the teacher: {str(e)}")
        
    @staticmethod
    async def download_profile_pictures(teachers: List[TeacherResponseDTO]) -> List[dict]:
        tasks = []
        for teacher in teachers:
            if teacher.profile_picture:
                file_path = f"{config['aws']['aws_s3_image_path']}/{teacher.profile_picture}"
                tasks.append(FileService.download_from_s3(file_path))
        return await asyncio.gather(*tasks)
