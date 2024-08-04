from fastapi import HTTPException
from app.repositories.teacher_repo import TeacherRepository
from app.models.teacher_model import Teacher, SchoolInfo
from app.dto.teacher_dto import TeacherResponseDTO, TeacherDTO

class TeacherService:
    @staticmethod
    async def create_teacher(teacherdto: TeacherDTO):
        teacher=Teacher(**teacherdto.dict())
        result = await TeacherRepository.create_teacher(teacher)
        if result: 
            return "Teacher Created Successfully"
        raise HTTPException(status_code=400, detail="Could not create teacher")

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
    async def update_teacher(teacher_id: str, teacher_dto: TeacherDTO):
        try:
            teacher = Teacher(**teacher_dto.dict())
            result = await TeacherRepository.update_teacher(teacher_id, teacher)
            
            if isinstance(result, str):
                # If result is a string, it's a message from the repository
                return result
            else:
                # If result is not a string, it should be an UpdateResult object
                if result.matched_count == 0:
                    raise HTTPException(status_code=404, detail="Teacher not found")
                
                if result.modified_count > 0:
                    return "Teacher updated successfully"
                else:
                    return "No changes made to the teacher"

        except Exception as e:
            # For any other unexpected errors
            raise HTTPException(status_code=500,detail=f"An error occurred while updating the teacher: {str(e)}")
