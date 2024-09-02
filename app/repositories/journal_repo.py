from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import HTTPException
from app.config.db_config import mongodb
from app.dto.journal_dto import JournalDTO, JournalResponseDTO
from app.models.journal_model import Journal

class JournalRepository:

    @staticmethod
    async def create_journal_entry(journal: Journal) -> dict:
        result = await mongodb.collections["journal"].insert_one(journal.dict())
        return "Joural Created Successfully !!!"

    @staticmethod
    async def get_journals_by_mentor(mentor_id: str) -> List[JournalResponseDTO]:
        mentor_id_dbref = DBRef(collection="teacher",id= ObjectId(mentor_id))
        journals = await mongodb.collections["journal"].find({"mentor_id": mentor_id_dbref}).to_list(None)
        return [JournalResponseDTO(**journal) for journal in journals]

    @staticmethod
    async def get_journal_by_id(journal_id: str) -> Optional[JournalResponseDTO]:
        try:
            journal = await mongodb.collections["journal"].find_one({"_id": ObjectId(journal_id)})
            if not journal:
                return None
            return JournalResponseDTO(**journal)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving journal: {str(e)}")
        
    @staticmethod
    async def get_missing_journals_by_date(date: str) -> List[str]:
        try:
            missing_journals = await mongodb.collections["missing_journals"].find_one({"date": date})
            if not missing_journals:
                return []
            mentor_ids = missing_journals.get("mentors", [])
            mentor_names = []
            for mentor_id in mentor_ids:
                mentor = await mongodb.collections["teacher"].find_one({"_id": ObjectId(mentor_id)})
                if mentor:
                    mentor_names.append(mentor.get("name", "Unknown"))
            return mentor_names
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving missing journals: {str(e)}")
