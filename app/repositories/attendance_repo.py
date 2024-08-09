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


    async def upsert_attendance(self, attendance: Attendance) -> str:
        filter_doc = {"date": attendance.date}
        update_doc = {"$set": attendance.dict()}
        result = await mongodb.collections['attendance'].update_one(filter_doc, update_doc, upsert=True)
        return str(result.upserted_id) if result.upserted_id else "Attendance record updated successfully"

    async def get_all_attendances(self) -> List[AttendanceResponseDTO]:
        attendances = mongodb.collections['attendance'].find({})
        return [AttendanceResponseDTO(**attendance) async for attendance in attendances]

    async def get_attendance_by_date(self, date: str) -> Optional[Attendance]:
        attendance = await mongodb.collections['attendance'].find_one({"date": date})
        return AttendanceResponseDTO(**attendance) if attendance else None

    async def get_student_attendance(self, student_id: str) -> List[AttendanceResponseDTO]:
        attendances = mongodb.collections['attendance'].find(
            {"schools.students.student_id": DBRef(collection='students', id=ObjectId(student_id))}
        )
        return [AttendanceResponseDTO(**{**attendance, "id": str(attendance["_id"])}) async for attendance in attendances]

    async def get_teacher_attendance(self, teacher_id: str) -> List[AttendanceResponseDTO]:
        attendances = mongodb.collections['attendance'].find(
            {"schools.teachers.teacher_id": DBRef(collection='teachers', id=ObjectId(teacher_id))}
        )
        return [AttendanceResponseDTO(**{**attendance, "id": str(attendance["_id"])}) async for attendance in attendances]
