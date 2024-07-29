from app.repositories.student_repo import studentRepository
from app.models.student_model import Student
class studentService:
    @staticmethod
    async def create_student(student: Student):
        result = await studentRepository.create_student(student)
        return result
    
    @staticmethod
    async def read_student():
        result = await studentRepository.get_all_student()
        return result
    
    @staticmethod
    async def delete_student(student_id:str):
        result= await studentRepository.delete_student(student_id)
        return result
    @staticmethod
    async def update_student(student_id: str, student: Student):
        result= await studentRepository.update_student(student_id, student)
        return result