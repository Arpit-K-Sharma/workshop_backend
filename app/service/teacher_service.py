from app.repositories.teacher_repo import TeacherRepository
from app.models.teacher_model import Teacher

class TeacherService:
    @staticmethod
    async def create_teacher(teacher: Teacher):
        result = await TeacherRepository.create_teacher(teacher)
        return result
    
    @staticmethod
    async def list_teacher(teacher_id):
        result = await TeacherRepository.read_teacher(teacher_id)
        return result

    @staticmethod
    async def read_teacher():
        result = await TeacherRepository.get_all_teacher()
        return result
    
    @staticmethod
    async def delete_teacher(teacher_id:str):
        result= await TeacherRepository.delete_teacher(teacher_id)
        return result

    @staticmethod
    async def update_teacher(teacher_id: str, teacher: Teacher):
        result= await TeacherRepository.update_teacher(teacher_id, teacher)
        return result
    
