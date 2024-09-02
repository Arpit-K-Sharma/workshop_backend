from fastapi import APIRouter, HTTPException
from typing import List
from app.config.logger_config import get_logger
from app.service.journal_service import JournalService
from app.dto.journal_dto import JournalDTO, JournalResponseDTO
from app.utils.response_util import get_response

journal_route = APIRouter()
logger = get_logger()

@journal_route.post("/journals", response_model=dict)
async def create_journal_entry(journal: JournalDTO):
    logger.info(f"ENDPOINT CALLED: /journals (POST) \n DATA SENT: {journal.dict()}")
    response = await JournalService.create_journal_entry(journal)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", message="Journal Entry Created Successfully", status_code=201, data=response)

@journal_route.get("/journals/mentor/{mentor_id}", response_model=List[JournalResponseDTO])
async def get_journals_by_mentor(mentor_id: str):
    logger.info(f"ENDPOINT CALLED: /journals/mentor/{mentor_id} (GET)")
    journals = await JournalService.get_journals_by_mentor(mentor_id)
    logger.info(f"RESPONSE SENT: {journals}")
    return get_response(status="success", message="Journals Retrieved Successfully", data=journals, status_code=200)

@journal_route.get("/journals/{journal_id}", response_model=JournalResponseDTO)
async def get_journal_by_id(journal_id: str):
    logger.info(f"ENDPOINT CALLED: /journals/{journal_id} (GET)")
    journal = await JournalService.get_journal_by_id(journal_id)
    logger.info(f"RESPONSE SENT: {journal}")
    return get_response(status="success", message="Journal Retrieved Successfully", data=journal, status_code=200)

@journal_route.get("/journals/missing/{date}", response_model=List[str])
async def get_missing_journals_by_date(date: str):
    logger.info(f"ENDPOINT CALLED: /journals/missing/{date} (GET)")
    mentor_names = await JournalService.get_missing_journals_by_date(date)
    logger.info(f"RESPONSE SENT: {mentor_names}")
    return get_response(status="success", message="Missing Journals Retrieved Successfully", data=mentor_names, status_code=200)
