from app.dto.hof_dto import AchieverDTO,AchieverResponseDTO
from app.models.hof_model import Achiever
from app.repositories.hof_repo import HofRepo
from fastapi import HTTPException

class HofService:
    @staticmethod
    async def get_all_hofs():
        try:
            result = await HofRepo.get_all_hofs()
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve HOFs: {str(e)}")
    
    @staticmethod
    async def get_hof_by_achiever_id(achiever_id: str):
        result = await HofRepo.hof_by_achiever_id(achiever_id)
        return AchieverResponseDTO(**result)
    
    @staticmethod
    async def create_hof(hofdto: AchieverDTO):
        try:
            hof = Achiever(**hofdto.dict())
            result = await HofRepo.create_hof(hof)
            return {"message": "Hof created successfully", "data": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create Hof: {str(e)}")
    
    @staticmethod
    async def update_hof(hof_id: str, hofdto: AchieverDTO):
        hof = Achiever(**hofdto.dict()) #converting achiverDTO to hof model 
        result = await HofRepo.update_hof(hof_id, hof)
        return {"message": "Hof updated successfully"}
    
    @staticmethod
    async def delete_hof(hof_id: str):
        result = await HofRepo.delete_hof(hof_id)
        return {"message": "Hof deleted successfully"}
    