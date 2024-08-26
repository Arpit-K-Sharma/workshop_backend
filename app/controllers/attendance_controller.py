from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.config.logger_config import get_logger
from app.service.attendance_service import AttendanceService
from app.dto.attendance_dto import ClassAttendanceDTO, StudentMonthlyAttendanceDTO, ClassMonthlyAttendanceDTO, StudentCourseMonthlyAttendanceDTO
from app.utils.response_util import get_response

attendance_route = APIRouter()
logger = get_logger()

@attendance_route.post("/attendances/class", response_model=dict)
async def create_or_update_class_attendance(class_attendance: ClassAttendanceDTO):
    logger.info(f"ENDPOINT CALLED: /attendances/class (POST) \n DATA SENT: {class_attendance.dict()}")
    response = await AttendanceService.create_or_update_class_attendance(class_attendance)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", message="Class Attendance Added/Updated Successfully", status_code=200, data=response)

@attendance_route.get("/attendances/student/{student_id}/month/{year}/{month}", response_model=StudentMonthlyAttendanceDTO)
async def get_student_monthly_attendance(student_id: str, year: int, month: int):
    logger.info(f"ENDPOINT CALLED: /attendances/student/{student_id}/month/{year}/{month} (GET)")
    attendance = await AttendanceService.get_student_monthly_attendance(student_id, year, month)
    logger.info(f"RESPONSE SENT: {attendance}")
    return get_response(status="success", message="Student Monthly Attendance Retrieved Successfully", data=attendance, status_code=200)

@attendance_route.get("/attendances/class/{class_id}/date/{date}", response_model=Optional[ClassAttendanceDTO])
async def get_class_attendance_by_date(class_id: str, date: str):
    logger.info(f"ENDPOINT CALLED: /attendances/class/{class_id}/date/{date} (GET)")
    attendance = await AttendanceService.get_class_attendance_by_date(class_id, date)
    logger.info(f"RESPONSE SENT: {attendance}")
    if attendance is None:
        return get_response(status="success", message="No attendance found for the given date", data={}, status_code=200)
    return get_response(status="success", message="Class Attendance Retrieved Successfully", data=attendance, status_code=200)


@attendance_route.get("/attendances/class/{class_id}/month/{year}/{month}", response_model=ClassMonthlyAttendanceDTO)
async def get_class_monthly_attendance(class_id: str, year: int, month: int):
    logger.info(f"ENDPOINT CALLED: /attendances/class/{class_id}/month/{year}/{month} (GET)")
    attendance = await AttendanceService.get_class_monthly_attendance(class_id, year, month)
    logger.info(f"RESPONSE SENT: {attendance}")
    return get_response(status="success", message="Class Monthly Attendance Retrieved Successfully", data=attendance, status_code=200)

@attendance_route.get("/attendances/student/{student_id}/class/{class_id}/month/{year}/{month}", response_model=StudentCourseMonthlyAttendanceDTO)
async def get_student_course_monthly_attendance(student_id: str, class_id: str, year: int, month: int):
    logger.info(f"ENDPOINT CALLED: /attendances/student/{student_id}/course/{class_id}/month/{year}/{month} (GET)")
    attendance = await AttendanceService.get_student_course_monthly_attendance(student_id, class_id, year, month)
    logger.info(f"RESPONSE SENT: {attendance}")
    return get_response(status="success", message="Student Course Monthly Attendance Retrieved Successfully", data=attendance, status_code=200)