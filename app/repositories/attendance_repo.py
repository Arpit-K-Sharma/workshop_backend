from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException
from app.config.db_config import mongodb
from app.dto.attendance_dto import ClassAttendanceDTO, StudentMonthlyAttendanceDTO, ClassMonthlyAttendanceDTO, StudentCourseMonthlyAttendanceDTO

class AttendanceRepository:

    @staticmethod
    async def create_or_update_class_attendance(class_attendance: ClassAttendanceDTO) -> dict:
        result = await mongodb.collections["attendance"].update_one(
            {"date": class_attendance.date, "class_id": class_attendance.class_id},
            {"$set": class_attendance.dict()},
            upsert=True
        )
        return {"modified_count": result.modified_count, "upserted_id": str(result.upserted_id) if result.upserted_id else None}

    @staticmethod
    async def get_student_monthly_attendance(student_id: str, year: int, month: int) -> StudentMonthlyAttendanceDTO:
        start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
        end_date = datetime(year, month + 1, 1).strftime("%Y-%m-%d") if month < 12 else datetime(year + 1, 1, 1).strftime("%Y-%m-%d")
        
        pipeline = [
            {"$match": {
                "date": {"$gte": start_date, "$lt": end_date},
                "students.student_id": student_id
            }},
            {"$project": {
                "date": 1,
                "status": {
                    "$filter": {
                        "input": "$students",
                        "as": "student",
                        "cond": {"$eq": ["$$student.student_id", student_id]}
                    }
                }
            }},
            {"$unwind": "$status"},
            {"$project": {
                "date": 1,
                "status": "$status.status",
                "remarks": "$status.remarks"
            }}
        ]
        
        attendances = await mongodb.collections["attendance"].aggregate(pipeline).to_list(None)
        return StudentMonthlyAttendanceDTO(student_id=student_id, attendances=attendances)

    @staticmethod
    async def get_class_attendance_by_date(class_id: str, date: str) -> Optional[ClassAttendanceDTO]:
       attendance = await mongodb.collections["attendance"].find_one({"class_id": class_id, "date": date})
       if not attendance:
           return None
       return ClassAttendanceDTO(**attendance)


    @staticmethod
    async def get_class_monthly_attendance(class_id: str, year: int, month: int) -> ClassMonthlyAttendanceDTO:
        start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
        end_date = datetime(year, month + 1, 1).strftime("%Y-%m-%d") if month < 12 else datetime(year + 1, 1, 1).strftime("%Y-%m-%d")
        
        attendances = await mongodb.collections["attendance"].find({
            "class_id": class_id,
            "date": {"$gte": start_date, "$lt": end_date}
        }).sort("date", 1).to_list(None)
        
        return ClassMonthlyAttendanceDTO(class_id=class_id, attendances=attendances)
      

    @staticmethod
    async def get_student_course_monthly_attendance(student_id: str, class_id: str, year: int, month: int) -> StudentCourseMonthlyAttendanceDTO:
      start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
      end_date = datetime(year, month + 1, 1).strftime("%Y-%m-%d") if month < 12 else datetime(year + 1, 1, 1).strftime("%Y-%m-%d")
    
      pipeline = [
        {"$match": {
            "date": {"$gte": start_date, "$lt": end_date},
            "class_id": class_id,
            "students.student_id": student_id
        }},
        {"$project": {
            "date": 1,
            "status": {
                "$filter": {
                    "input": "$students",
                    "as": "student",
                    "cond": {"$eq": ["$$student.student_id", student_id]}
                }
            }
        }},
        {"$unwind": "$status"},
        {"$project": {
            "date": 1,
            "status": "$status.status",
            "remarks": "$status.remarks"
        }}
    ]
    
      attendances = await mongodb.collections["attendance"].aggregate(pipeline).to_list(None)
      return StudentCourseMonthlyAttendanceDTO(student_id=student_id, course_id=class_id, attendances=attendances)