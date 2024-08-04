from fastapi import HTTPException
from app.repositories.school_repo import SchoolRepository
from app.models.school_model import School
from app.dto.school_dto import SchoolDTO, SchoolResponseDTO

class SchoolService:
    @staticmethod
    async def create_school(schooldto: SchoolDTO):
        school = School(**schooldto.dict())
        result = await SchoolRepository.create_school(school)
        if result:
            return "School created successfully"
        raise HTTPException(status_code=400, detail="School not created")

    
    @staticmethod
    async def get_all_school():
        results = await SchoolRepository.get_all_schools()  # Update method name here
        return [SchoolResponseDTO(**school) for school in results]

    @staticmethod
    async def get_school(school_id: str) -> SchoolResponseDTO:
        result = await SchoolRepository.get_school(school_id)
        if isinstance(result, dict):
            return SchoolResponseDTO(**result)
        raise HTTPException(status_code=404, detail="School not found")

    @staticmethod
    async def delete_school(school_id: str):
        result = await SchoolRepository.delete_school(school_id)
        if result == "School deleted successfully":
            return result
        raise HTTPException(status_code=404, detail=f"School with id {school_id} not found")

    @staticmethod
    async def update_school(school_id: str, schooldto: SchoolDTO):
        school = School(**schooldto.dict())
        result = await SchoolRepository.update_school(school_id, school)
        if result == "School updated successfully":
            return result
        raise HTTPException(status_code=404, detail=f"School with id {school_id} not found or no changes made")
