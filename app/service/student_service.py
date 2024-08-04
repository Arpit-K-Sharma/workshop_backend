from fastapi import HTTPException
from app.repositories.student_repo import StudentRepository
from app.models.student_model import Student
from app.dto.student_dto import StudentDTO,StudentResponseDTO
class StudentService:
    @staticmethod
    async def create_student(studentdto: StudentDTO):
        try:
            student = Student(**studentdto.dict())
            result = await StudentRepository.create_student(student)
            if result:
                return "Student Created Successfully"
            raise HTTPException(status_code=400, detail="Could not create student")
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while creating the student: {str(e)}")
    
    @staticmethod
    async def get_student_by_id(student_id: str):
        try:
            result = await StudentRepository.get_student_by_id(student_id)
            return StudentResponseDTO(**result)
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while fetching the student: {str(e)}")
        
    @staticmethod
    async def get_students_by_school_id(school_id: str):
        try:
            result = await StudentRepository. get_students_by_school_id(school_id)
            return [StudentResponseDTO(**school) async for school in result]
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while fetching the School: {str(e)}")
    

    @staticmethod
    async def get_all_students():
        try:
            result = await StudentRepository.get_all_student()
            return [StudentResponseDTO(**student) async for student in result]
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while fetching all students: {str(e)}")
    
    @staticmethod
    async def delete_student(student_id: str):
        try:
            result = await StudentRepository.delete_student(student_id)
            return {"message": result}
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while deleting the student: {str(e)}")

    @staticmethod
    async def update_student(student_id: str, student: StudentDTO):
        try:
            result = await StudentRepository.update_student(student_id, student)
            if isinstance(result, str):
                # If result is a string, it's a message from the repository
                return result
            else:
                # If result is not a string, it should be an UpdateResult object
                if result.matched_count == 0:
                    raise HTTPException(status_code=404, detail="Student not found")
                
                if result.modified_count > 0:
                    return "Student updated successfully"
                else:
                    return "No changes made to the student"
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while updating the student: {str(e)}")
        
        