from bson import ObjectId,DBRef
from app.models.school_model import School
from app.config.db_config import mongodb
from fastapi import HTTPException
from app.dto.school_dto import SchoolResponseDTO


class SchoolRepository:
    @staticmethod
    async def create_school(school: School):
        result = await mongodb.collections["school"].insert_one(school.dict())
        return {"inserted_id": str(result.inserted_id)}

    @staticmethod
    async def get_all_schools():
        cursor = mongodb.collections["school"].find({})
        schools = []
        async for school in cursor:
            school["_id"] = str(school["_id"].id) if isinstance(school["_id"], DBRef) else str(school["_id"])
            schools.append(school)
        return schools
    

    @staticmethod
    async def get_school(school_id: str) -> SchoolResponseDTO:
        try:
            _id = ObjectId(school_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid school ID: {str(e)}")

        school = await mongodb.collections["school"].find_one({"_id": _id})
        if school:
            school["_id"] = str(school["_id"])
            return school
        raise HTTPException(status_code=404, detail="School not found")

    @staticmethod
    async def delete_school(school_id: str):
        try:
            _id = ObjectId(school_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid school ID: {str(e)}")

        try:
            # Create a DBRef for the school
            school_ref = DBRef(collection="school", id=_id)

            # Delete the school
            school_result = await mongodb.collections["school"].delete_one({"_id": _id})
            if school_result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="School not found")

            # Delete associated classes
            classes_result = await mongodb.collections["class"].delete_many({"school_id": school_ref})

            # Delete associated students
            students_result = await mongodb.collections["student"].delete_many({"school_id": school_id})

            # Update teachers by removing this school from their schools list
            teachers_result = await mongodb.collections["teacher"].update_many(
                {"schools.school_id": school_ref},
                {"$pull": {"schools": {"school_id": school_ref}}}
            )

            return {
                "message": "School and associated data deleted successfully",
                "deleted_school_count": school_result.deleted_count,
                "deleted_classes_count": classes_result.deleted_count,
                "deleted_students_count": students_result.deleted_count,
                "updated_teachers_count": teachers_result.modified_count
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def update_school(school_id: str, school: School):
        try:
            _id = ObjectId(school_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid school ID: {str(e)}")

        result = await mongodb.collections["school"].update_one({"_id": _id}, {"$set": school.dict(exclude_unset=True)})
        if result.matched_count > 0:
            return "School updated successfully"
        else:
            raise HTTPException(status_code=404, detail="School not found or no changes made")
