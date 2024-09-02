from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from app.repositories.attendance_repo import AttendanceRepository
from app.dto.attendance_dto import ClassAttendanceDTO,StudentAttendanceDTO, StudentMonthlyAttendanceDTO, ClassMonthlyAttendanceDTO, StudentCourseMonthlyAttendanceDTO

class AttendanceService:

    @staticmethod
    async def create_or_update_class_attendance(class_attendance: ClassAttendanceDTO) -> dict:
        try:
            repository = AttendanceRepository()
            result = await repository.create_or_update_class_attendance(class_attendance)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating/updating class attendance: {str(e)}")

    @staticmethod
    async def get_student_monthly_attendance(student_id: str, year: int, month: int) -> StudentMonthlyAttendanceDTO:
        try:
            repository = AttendanceRepository()
            attendance = await repository.get_student_monthly_attendance(student_id, year, month)
            return attendance
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving student monthly attendance: {str(e)}")

    @staticmethod
    async def get_class_attendance_by_date(class_id: str, date: str) -> Optional[ClassAttendanceDTO]:
       try:
          repository = AttendanceRepository()
          attendance = await repository.get_class_attendance_by_date(class_id, date)
          return attendance
       except Exception as e:
          raise HTTPException(status_code=500, detail=f"Error retrieving class attendance: {str(e)}")


    @staticmethod
    async def get_student_course_monthly_attendance(student_id: str, class_id: str, year: int, month: int) -> StudentCourseMonthlyAttendanceDTO:
        try:
          print(student_id, class_id, year, month)
          repository = AttendanceRepository()
          attendance = await repository.get_student_course_monthly_attendance(student_id, class_id, year, month)
          return attendance
        except Exception as e:
           raise HTTPException(status_code=500, detail=f"Error retrieving student course monthly attendance: {str(e)}")
