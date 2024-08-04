from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.config.logger_config import get_logger
from app.service.attendance_service import AttendanceService
from app.repositories.attendance_repo import AttendanceRepository
from app.dto.attendance_dto import AttendanceDTO, AttendanceResponseDTO
from app.utils.response_util import get_response


attendance_route = APIRouter()
attendance_service = AttendanceService(AttendanceRepository())
logger = get_logger()

@attendance_route.post("/attendances", response_model=str)
async def create_attendance(attendance_dto: AttendanceDTO):
    logger.info(f"ENDPOINT CALLED: /attendances (POST) \n DATA SENT: {attendance_dto.dict()}")
    response = await attendance_service.create_attendance(attendance_dto)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", message="Attendance Added Successfully", status_code=200)

@attendance_route.get("/attendances", response_model=List[AttendanceResponseDTO])
async def get_all_attendances():
    logger.info("ENDPOINT CALLED: /attendances (GET)")
    attendances = await attendance_service.get_all_attendances()
    logger.info(f"RESPONSE SENT: {attendances}")
    return get_response(status="success", message="Attendances Retrieved Successfully", data=attendances, status_code=200)

@attendance_route.get("/attendances/date/{date}", response_model=Optional[AttendanceResponseDTO])
async def get_attendance_by_date(date: str):
    logger.info(f"ENDPOINT CALLED: /attendances/date/{date} (GET)")
    attendance = await attendance_service.get_attendance_by_date(date)
    logger.info(f"RESPONSE SENT: {attendance}")
    if attendance:
        return get_response(status="success", message="Attendance Retrieved Successfully", data=attendance, status_code=200)
    else:
        return get_response(status="not_found", message="No attendance found for the given date", status_code=404)

@attendance_route.get("/attendances/student/{student_id}", response_model=List[AttendanceResponseDTO])
async def get_student_attendance(student_id: str):
    logger.info(f"ENDPOINT CALLED: /attendances/student/{student_id} (GET)")
    attendances = await attendance_service.get_student_attendance(student_id)
    logger.info(f"RESPONSE SENT: {attendances}")
    return get_response(status="success", message="Student Attendances Retrieved Successfully", data=attendances, status_code=200)

@attendance_route.get("/attendances/teacher/{teacher_id}", response_model=List[AttendanceResponseDTO])
async def get_teacher_attendance(teacher_id: str):
    logger.info(f"ENDPOINT CALLED: /attendances/teacher/{teacher_id} (GET)")
    attendances = await attendance_service.get_teacher_attendance(teacher_id)
    logger.info(f"RESPONSE SENT: {attendances}")
    return get_response(status="success", message="Teacher Attendances Retrieved Successfully", data=attendances, status_code=200) 