from app.repositories.school_repo import SchoolRepository
from app.models.school_model import School

class schoolService:
    @staticmethod
    async def create_school(school: School):
        result = await SchoolRepository.create_school(school)
        return result
    
    @staticmethod
    async def read_school(school_id):
        result = await SchoolRepository.read_school(school_id)
        return result

    @staticmethod
    async def list_school():
        result = await SchoolRepository.get_all_school()
        return result
    
    @staticmethod
    async def delete_school(school_id:str):
        result= await SchoolRepository.delete_school(school_id)
        return result

    @staticmethod
    async def update_school(school_id: str, school: School):
        result= await SchoolRepository.update_school(school_id, school)
        return result
    
