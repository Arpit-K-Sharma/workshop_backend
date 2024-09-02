# assignment_repo.py
from bson import DBRef, ObjectId
from typing import List, Dict

from fastapi import HTTPException
from app.config.db_config import mongodb
from app.dto.assignment_dto import AssignmentResponseDTO
from app.models.assignment_model import Assignment
from app.models.attendance_model import Attendance
class AssignmentRepository:

    async def create_assignment(assignment: Assignment):
        result = await mongodb.collections["assignment"].insert_one(assignment.dict())
        response = await mongodb.collections["assignment"].find_one({"_id": result.inserted_id})
        return AssignmentResponseDTO(**response)

    async def get_assignments_by_class(class_id: str) -> List[Dict]:
        classId_object = ObjectId(class_id)
        cursor = mongodb.collections["assignment"].find({"class_id": DBRef(collection='class', id=classId_object)})
        return await cursor.to_list(length=None)

    async def update_assignment(_id: ObjectId, assignment_update: dict):
        try:
            # Fetch the existing assignment
            existing_assignment = await mongodb.collections["assignment"].find_one({"_id": _id})
            print(existing_assignment)
            
            if not existing_assignment:
                raise HTTPException(status_code=404, detail="Assignment not found")

            # Update only the fields that are provided
            update_data = {}
            for key, value in assignment_update.items():
                if value is not None:
                    update_data[key] = value

            # Perform the update
            result = await mongodb.collections["assignment"].update_one(
                {"_id": _id},
                {"$set": update_data}
            )

            if result.modified_count:
                # Fetch and return the updated assignment
                updated_assignment = await mongodb.collections["assignment"].find_one({"_id": _id})
                return updated_assignment
            else:
                # No changes were made
                return existing_assignment

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


    async def delete_assignment(assignment_id: str) -> bool:
        assignment_id_object = ObjectId(assignment_id)
        result = await mongodb.collections["assignment"].delete_one({"_id": assignment_id_object})
        return result.deleted_count > 0
