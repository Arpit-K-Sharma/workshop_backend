# assignment_controller.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.dto.assignment_dto import AssignmentDTO, AssignmentResponseDTO
from app.service.assignment_service import AssignmentService


assignment_route = APIRouter()

@assignment_route.post("/assignments")
async def create_assignment(assignment: AssignmentDTO):
    return await AssignmentService.create_assignment(assignment)

@assignment_route.get("/assignments/class/{class_id}", response_model=List[AssignmentResponseDTO])
async def get_assignments_by_class(class_id: str):
    return await AssignmentService.get_assignments_by_class(class_id)

@assignment_route.put("/assignments/{assignment_id}", response_model=AssignmentResponseDTO)
async def update_assignment(assignment_id: str, assignment: dict):
    return await AssignmentService.update_assignment(assignment_id, assignment)

@assignment_route.delete("/assignments/{assignment_id}")
async def delete_assignment(assignment_id: str):
    return await AssignmentService.delete_assignment(assignment_id)
