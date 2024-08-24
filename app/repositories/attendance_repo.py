from datetime import datetime
from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import HTTPException
from app.models.attendance_model import Attendance
from app.dto.attendance_dto import AttendanceDTO, AttendanceResponseDTO
from app.config.db_config import mongodb

class AttendanceRepository:
    @staticmethod
    async def create_attendance(attendance: Attendance):
        result = await mongodb.collections["attendance"].insert_one(attendance.dict())
        return {"inserted_id": str(result.inserted_id)}

    @staticmethod
    async def upsert_attendance(attendance: Attendance) -> str:
        filter_doc = {"date": attendance.date}
        update_doc = {"$set": attendance.dict()}
        result = await mongodb.collections['attendance'].update_one(filter_doc, update_doc, upsert=True)
        return str(result.upserted_id) if result.upserted_id else "Attendance record updated successfully"

    @staticmethod
    async def get_all_attendances() -> List[AttendanceResponseDTO]:
        attendances = mongodb.collections['attendance'].find({})
        return [AttendanceResponseDTO(**attendance) async for attendance in attendances]

    @staticmethod
    async def get_attendance_by_date(date: str) -> Optional[AttendanceResponseDTO]:
        attendance = await mongodb.collections['attendance'].find_one({"date": date})
        return AttendanceResponseDTO(**attendance) if attendance else None

    @staticmethod
    async def get_student_attendance(student_id: str) -> List[AttendanceResponseDTO]:
        student_object_id = ObjectId(student_id)
        attendances_cursor = mongodb.collections['attendance'].find(
            {"schools.classes.students.student_id.$id": student_object_id}
        )
        attendances = await attendances_cursor.to_list(length=None)
        result = [AttendanceResponseDTO(**{**attendance, "id": str(attendance["_id"])}) for attendance in attendances]
        return result
