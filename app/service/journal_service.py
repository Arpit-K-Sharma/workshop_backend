from fastapi import HTTPException
from app.models.journal_model import Journal
from app.repositories.journal_repo import JournalRepository
from app.dto.journal_dto import JournalDTO, JournalResponseDTO
from typing import List

class JournalService:

    @staticmethod
    async def create_journal_entry(journal: JournalDTO) -> dict:
        try:
            repository = JournalRepository()
            
            # Extract the date from the JournalDTO object
            date = journal.date
            
            # Compute the day of the week
            day_of_week = date.strftime('%A')
            
            # Extract day, month, and year
            day = date.strftime('%d')
            month = date.strftime('%B')
            year = date.strftime('%Y')
            
            # Create the Journal model object
            journal_model = Journal(
                body=journal.body,
                date=date,
                day_of_week=day_of_week,
                day=day,
                month=month,
                year=year,
                mentor_id=journal.mentor_id
            )
            
            # Save the journal entry to the database
            result = await repository.create_journal_entry(journal_model)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating journal entry: {str(e)}")

    @staticmethod
    async def get_journals_by_mentor(mentor_id: str) -> List[JournalResponseDTO]:
        try:
            repository = JournalRepository()
            journals = await repository.get_journals_by_mentor(mentor_id)
            return journals
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving journals: {str(e)}")

    @staticmethod
    async def get_journal_by_id(journal_id: str) -> JournalResponseDTO:
        try:
            repository = JournalRepository()
            journal = await repository.get_journal_by_id(journal_id)
            if not journal:
                raise HTTPException(status_code=404, detail="Journal not found")
            return journal
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving journal: {str(e)}")
        
    @staticmethod
    async def get_missing_journals_by_date(date: str) -> List[str]:
        try:
            repository = JournalRepository()
            mentor_names = await repository.get_missing_journals_by_date(date)
            return mentor_names
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving missing journals: {str(e)}")
