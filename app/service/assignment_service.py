# assignment_service.py
from typing import List
from bson import ObjectId
from fastapi import HTTPException

from app.dto.assignment_dto import AssignmentDTO, AssignmentResponseDTO
from app.models.assignment_model import Assignment
from app.repositories.assignment_repo import AssignmentRepository


class AssignmentService:
    @staticmethod
    async def create_assignment(assignment: AssignmentDTO) -> AssignmentResponseDTO:
        created_assignment = await AssignmentRepository.create_assignment(Assignment(**assignment.dict()))
        return created_assignment

    @staticmethod
    async def get_assignments_by_class(class_id: str) -> List[AssignmentResponseDTO]:
        assignments = await AssignmentRepository.get_assignments_by_class(class_id)
        return [AssignmentResponseDTO(**assignment) for assignment in assignments]

    @staticmethod
    async def update_assignment(assignment_id: str, assignment: dict) -> AssignmentResponseDTO:
        try:
            _id = ObjectId(assignment_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid class ID: {str(e)}")
        updated_assignment = await AssignmentRepository.update_assignment(_id, assignment)
        if not updated_assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return AssignmentResponseDTO(**updated_assignment)

    @staticmethod
    async def delete_assignment(assignment_id: str) -> dict:
        deleted = await AssignmentRepository.delete_assignment(ObjectId(assignment_id))
        if not deleted:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return {"message": "Assignment deleted successfully"}
